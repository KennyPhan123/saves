#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rimworld_dump.py — Đọc file save RimWorld (.rws) và xuất TOÀN BỘ state ra
Markdown + JSON + CSV (không tóm tắt, không bỏ sót mục nào).

Cách dùng cơ bản:
    python3 tools/rimworld_dump.py "vãi ò.rws"

Kết quả mặc định nằm trong thư mục ./dump/:
    dump/report.md            — báo cáo đầy đủ, dễ đọc
    dump/state.json           — toàn bộ state dạng máy đọc được
    dump/things_all.csv       — MỌI object trên map (25k+ dòng)
    dump/plants.csv           — MỌI cây (kể cả cây hoang)
    dump/items.csv            — mọi stack vật phẩm
    dump/buildings.csv        — mọi công trình
    dump/pawns_skills.csv     — kỹ năng từng pawn
    dump/pawns_needs.csv      — nhu cầu từng pawn
    dump/pawns_work.csv       — ưu tiên công việc từng pawn
    dump/zones_cells.csv      — từng ô của từng zone
    dump/pawn_<id>.xml        — XML gốc của từng pawn (nếu --raw)

Ví dụ khác:
    python3 tools/rimworld_dump.py save.rws -o out --all-pawns --raw
    python3 tools/rimworld_dump.py save.rws --no-csv --md-only

Script chỉ ĐỌC file save, không bao giờ ghi/sửa file .rws.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

# --------------------------------------------------------------------------
# Hằng số & bảng tên
# --------------------------------------------------------------------------

TICKS_PER_DAY = 60_000
TICKS_PER_YEAR = 3_600_000
DAYS_PER_QUADRUM = 15
QUADRUM_NAMES = ["Aprimay", "Jugust", "Septober", "Decembary"]

# Thứ tự WorkTypeDef trong save = thứ tự nạp def (DefMap<T> lưu theo def index).
# Core (20) -> Biotech (Childcare) -> Anomaly (DarkStudy) -> Odyssey (Fishing)
# Khớp với RimWorld 1.7 + đủ 6 DLC. Có thể ghi đè bằng --worktypes file.json
WORK_TYPES = [
    ("Firefighter", "Chữa cháy"),
    ("Patient", "Bệnh nhân"),
    ("Doctor", "Bác sĩ"),
    ("PatientBedRest", "Nằm nghỉ dưỡng"),
    ("BasicWorker", "Việc cơ bản"),
    ("Warden", "Cai ngục"),
    ("Handling", "Thuần hóa"),
    ("Cooking", "Nấu ăn"),
    ("Hunting", "Săn bắn"),
    ("Construction", "Xây dựng"),
    ("Growing", "Trồng trọt"),
    ("Mining", "Khai thác"),
    ("PlantCutting", "Chặt cây"),
    ("Smithing", "Rèn"),
    ("Tailoring", "May mặc"),
    ("Art", "Nghệ thuật"),
    ("Crafting", "Chế tạo"),
    ("Hauling", "Khiêng vác"),
    ("Cleaning", "Dọn dẹp"),
    ("Research", "Nghiên cứu"),
    ("Childcare", "Chăm trẻ"),
    ("DarkStudy", "Nghiên cứu hắc ám"),
    ("Fishing", "Câu cá"),
]

SKILLS = {
    "Shooting": "Bắn súng", "Melee": "Cận chiến", "Construction": "Xây dựng",
    "Mining": "Khai thác", "Cooking": "Nấu ăn", "Plants": "Trồng trọt",
    "Animals": "Động vật", "Crafting": "Chế tạo", "Artistic": "Nghệ thuật",
    "Medicine": "Y học", "Social": "Xã hội", "Intellectual": "Trí tuệ",
}

PASSION = {None: "—", "": "—", "None": "—", "Minor": "★ (nhỏ)", "Major": "★★ (lớn)"}

NEEDS = {
    "Mood": "Tâm trạng", "Food": "Thức ăn", "Rest": "Nghỉ ngơi", "Joy": "Giải trí",
    "Beauty": "Cái đẹp", "Comfort": "Thoải mái", "Outdoors": "Ngoài trời",
    "DrugDesire": "Thèm thuốc", "RoomSize": "Kích thước phòng",
    "Chemical_Smokeleaf": "Thèm cần sa", "Chemical_Alcohol": "Thèm rượu",
    "Chemical_Psychite": "Thèm psychite", "Chemical_WakeUp": "Thèm wake-up",
    "Chemical_GoJuice": "Thèm go-juice", "Chemical_Ambrosia": "Thèm ambrosia",
    "Learning": "Học tập", "Play": "Chơi", "Indoors": "Trong nhà",
    "Bladder": "Đi vệ sinh", "Hygiene": "Vệ sinh", "Sleep": "Ngủ",
}

TRAITS = {
    "FastLearner": "Học nhanh", "ShootingAccuracy": "Độ chính xác bắn",
    "BodyPurist": "Bài cấy ghép", "Transhumanist": "Siêu nhân học",
    "DrugDesire": "Thèm thuốc", "Kind": "Tốt bụng", "Psychopath": "Tâm thần",
    "Bloodlust": "Khát máu", "Cannibal": "Ăn thịt người", "Nimble": "Nhanh nhẹn",
    "Tough": "Cứng cỏi", "IronWilled": "Ý chí sắt", "Sanguine": "Lạc quan",
    "Depressive": "Trầm cảm", "Jealous": "Ghen tị", "Greedy": "Tham lam",
    "Workaholic": "Cuồng việc", "NightOwl": "Cú đêm", "EarlyRiser": "Dậy sớm",
    "QuickSleeper": "Ngủ nhanh", "Slowpoke": "Chậm chạp", "Jogger": "Chạy bộ",
    "Pyromaniac": "Cuồng lửa", "Ascetic": "Khổ hạnh", "Gourmand": "Phàm ăn",
    "GreatMemory": "Trí nhớ tốt", "TooSmart": "Quá thông minh",
    "Nervous": "Lo lắng", "Volatile": "Dễ nổi nóng", "Abrasive": "Thô lỗ",
}

THOUGHTS = {
    "CrashedTogether": "Cùng rơi tàu", "Chitchat": "Tán gẫu", "DeepTalk": "Nói chuyện sâu",
    "NewColonyHope": "Hy vọng thuộc địa mới", "Slighted": "Bị xúc phạm",
    "SleepDisturbed": "Bị đánh thức", "AteRawFood": "Ăn đồ sống",
    "SleptInHeat": "Ngủ nơi nóng", "SleptOnGround": "Ngủ dưới đất",
    "SleptInBedroom": "Ngủ trong phòng ngủ", "SleptOutside": "Ngủ ngoài trời",
    "AteWithoutTable": "Ăn không có bàn", "AteInBed": "Ăn trên giường",
    "Hungry": "Đói", "Starving": "Đang chết đói", "Tired": "Mệt",
    "Exhausted": "Kiệt sức", "RecreationDrained": "Hết năng lượng giải trí",
    "ApparelDamaged": "Quần áo rách", "Naked": "Khỏa thân",
    "Pain": "Đau", "Wounded": "Bị thương", "Sick": "Bệnh",
    "InDarkness": "Trong bóng tối", "VeryUglyRoom": "Phòng rất xấu",
}

HEDIFFS = {
    "SmokeleafAddiction": "Nghiện cần sa", "SmokeleafTolerance": "Dung nạp cần sa",
    "AlcoholAddiction": "Nghiện rượu", "PsychiteAddiction": "Nghiện psychite",
    "Flu": "Cúm", "Plague": "Dịch hạch", "Malaria": "Sốt rét",
    "CryptosleepSickness": "Say ngủ đông", "Bite": "Vết cắn", "Cut": "Vết cắt",
    "Gunshot": "Vết đạn", "Bruise": "Vết bầm", "Burn": "Bỏng",
    "HeartArteryBlockage": "Tắc động mạch tim", "Cataract": "Đục thủy tinh thể",
    "Asthma": "Hen suyễn", "HearingLoss": "Mất thính lực",
    "MissingPart": "Mất bộ phận", "Scar": "Sẹo",
}

ITEMS = {
    "WoodLog": "Gỗ", "Steel": "Thép", "Silver": "Bạc", "Gold": "Vàng",
    "RawRice": "Gạo sống", "RawCorn": "Ngô sống", "RawPotatoes": "Khoai tây sống",
    "ComponentIndustrial": "Linh kiện công nghiệp", "ComponentSpacer": "Linh kiện vũ trụ",
    "MedicineIndustrial": "Thuốc công nghiệp", "MedicineHerbal": "Thuốc thảo dược",
    "MedicineUltratech": "Thuốc siêu công nghệ", "Luciferium": "Luciferium",
    "GravlitePanel": "Tấm Gravlite", "MealSurvivalPack": "Gói thức ăn sinh tồn",
    "MealSimple": "Suất ăn đơn giản", "MealFine": "Suất ăn ngon",
    "MealLavish": "Suất ăn thịnh soạn", "Pemmican": "Pemmican", "Kibble": "Thức ăn gia súc",
    "MeleeWeapon_Knife": "Dao", "Gun_Autopistol": "Súng ngắn tự động",
    "Gun_Revolver": "Súng lục ổ xoay", "Gun_BoltActionRifle": "Súng trường bolt-action",
    "Gun_PumpShotgun": "Súng shotgun bơm", "Gun_AssaultRifle": "Súng trường tấn công",
    "Apparel_Pants": "Quần", "Apparel_BasicShirt": "Áo sơ mi cơ bản",
    "Apparel_CollarShirt": "Áo cổ", "Apparel_FlakVest": "Áo giáp Flak",
    "Apparel_FlakPants": "Quần giáp Flak", "Apparel_Parka": "Áo khoác parka",
    "Apparel_AdvancedHelmet": "Mũ giáp tiên tiến", "Apparel_SimpleHelmet": "Mũ giáp đơn giản",
    "Apparel_Duster": "Áo choàng dài", "Apparel_TribalA": "Trang phục bộ lạc",
    "Hay": "Cỏ khô", "Chocolate": "Sô-cô-la", "Beer": "Bia",
    "SmokeleafJoint": "Cần sa cuộn", "HemogenPack": "Gói hemogen",
    "Corpse_Human": "Xác người", "Corpse_Rat": "Xác chuột", "Corpse_Mink": "Xác chồn",
    "Corpse_Tortoise": "Xác rùa", "BiomutationPulser": "Máy tạo đột biến",
}

PLANTS = {
    "Plant_Rice": "Lúa", "Plant_TreeOak": "Sồi", "Plant_Grass": "Cỏ",
    "Plant_TallGrass": "Cỏ cao", "Plant_Brambles": "Bụi gai", "Plant_TreePoplar": "Dương",
    "Plant_Bush": "Bụi cây", "Plant_Dandelion": "Bồ công anh", "Plant_Reeds": "Sậy",
    "Plant_Berry": "Cây quả dại", "Plant_HealrootWild": "Cỏ chữa bệnh hoang",
    "Plant_LilyPad": "Bèo", "Plant_Bulrush": "Cói", "Plant_Ambrosia": "Ambrosia",
    "Plant_Corn": "Ngô", "Plant_Potato": "Khoai tây", "Plant_Cotton": "Bông",
    "Plant_Healroot": "Cỏ chữa bệnh", "Plant_Hops": "Hoa bia", "Plant_Smokeleaf": "Cần sa",
    "Plant_Psychoid": "Psychoid", "Plant_TreeTeak": "Gỗ teak", "Plant_TreeCecropia": "Cecropia",
    "Plant_TreeMaple": "Phong", "Plant_TreeWillow": "Liễu", "Plant_TreeElm": "Du",
    "Plant_TreeBirch": "Bạch dương", "Plant_TreePine": "Thông", "Plant_TreeCocoa": "Ca cao",
}

BUILDINGS = {
    "Wall": "Tường", "Door": "Cửa", "Bed": "Giường", "Bedroll": "Túi ngủ",
    "TorchLamp": "Đuốc", "StandingLamp": "Đèn đứng", "Table1x2c": "Bàn ăn 1×2",
    "Table2x2c": "Bàn ăn 2×2", "Table3x3c": "Bàn ăn 3×3", "Stool": "Ghế đẩu",
    "DiningChair": "Ghế ăn", "HorseshoesPin": "Cọc chơi móng ngựa",
    "FueledStove": "Bếp củi", "ElectricStove": "Bếp điện",
    "SimpleResearchBench": "Bàn nghiên cứu đơn giản", "ResearchBench": "Bàn nghiên cứu",
    "Frame_DiningChair": "Khung ghế ăn", "Column": "Cột", "Sarcophagus": "Quan tài",
    "SteamGeyser": "Mạch nước nóng", "VoidMonolith": "Monolith",
    "AncientCryptosleepCasket": "Kén ngủ đông cổ", "AncientConcreteBarrier": "Rào bê tông cổ",
    "AncientFence": "Hàng rào cổ", "AncientWheel": "Bánh xe cổ",
    "AncientGiantWheel": "Bánh xe khổng lồ cổ", "AncientLamppost": "Đèn đường cổ",
    "AncientRazorWire": "Dây kẽm gai cổ", "AncientRustedCar": "Xe gỉ cổ",
    "AncientRustedCarFrame": "Khung xe gỉ cổ", "AncientRustedEngineBlock": "Khối động cơ gỉ cổ",
    "AncientOperatingTable": "Bàn mổ cổ", "AncientPipelineSection": "Ống dẫn cổ",
    "AncientPodCar": "Pod xe cổ", "AncientSmallCrate": "Thùng nhỏ cổ",
    "AncientHermeticCrate": "Thùng kín cổ", "AncientShipBeacon": "Đèn hiệu tàu cổ",
    "AncientRefrigerator": "Tủ lạnh cổ", "AncientGenerator": "Máy phát cổ",
    "AncientMechDropBeacon": "Đèn thả mech cổ", "AncientBarrel": "Thùng phuy cổ",
    "AncientExostriderLeg": "Chân exostrider cổ", "AncientExostriderHead": "Đầu exostrider cổ",
    "AncientExostriderCannon": "Pháo exostrider cổ", "AncientExostriderRemains": "Xác exostrider cổ",
    "AncientMiniWarwalkerRemains": "Xác warwalker cổ", "AncientMechRemains": "Xác mech cổ",
    "ShipChunk": "Mảnh tàu", "ShipChunk_Mech": "Mảnh tàu cơ khí",
    "GravEngine": "Động cơ trọng lực", "SteleLarge": "Bia đá lớn",
    "HorseshoesPin": "Cọc móng ngựa", "Grave": "Mộ",
}

BACKSTORIES = {
    "MedicalAssistant": "Trợ lý y tế", "WreckageExplorer": "Người khám phá xác tàu",
    "LowWageWorker": "Lao động lương thấp", "StoryWriter": "Nhà văn",
    "Bartender": "Nhân viên pha chế", "Colonist": "Người thuộc địa",
    "TribeChild": "Trẻ bộ lạc", "Scavenger": "Người nhặt rác",
    "SpaceMarine": "Lính không gian", "Scientist": "Nhà khoa học",
    "CaveChild": "Trẻ sống trong hang", "FarmKid": "Trẻ nông trại",
}

RESEARCH_VI = {
    "Electricity": "Điện", "Batteries": "Pin", "AirConditioning": "Điều hòa",
    "ComplexFurniture": "Nội thất phức tạp", "PassiveCooler": "Máy làm mát thụ động",
    "Stonecutting": "Đẽo đá", "ComplexClothing": "Quần áo phức tạp",
    "NutrientPaste": "Bột dinh dưỡng", "MicroelectronicsBasics": "Điện tử cơ bản",
    "Smithing": "Rèn", "Fabrication": "Chế tạo máy", "Machining": "Gia công",
    "GunTurrets": "Tháp súng", "Mortars": "Pháo", "Fishing": "Câu cá",
    "Pemmican": "Pemmican", "Brewing": "Nấu bia", "PsychoidBrewing": "Nấu psychoid",
    "TreeSowing": "Gieo cây", "Cocoa": "Ca cao", "Devilstrand": "Devilstrand",
    "CarpetMaking": "Làm thảm", "DrugProduction": "Sản xuất thuốc",
    "RecurveBow": "Cung recurve", "Greatbow": "Đại cung", "LongBlades": "Kiếm dài",
    "PlateArmor": "Giáp tấm", "PoweredArmor": "Giáp năng lượng",
    "CataphractArmor": "Giáp cataphract", "JumpPack": "Ba lô nhảy",
}

ZONE_TYPES = {
    "Zone_Growing": "Vùng trồng trọt", "Zone_Stockpile": "Vùng kho chứa",
    "Zone_Dumping": "Vùng đổ rác", "Zone_Fishing": "Vùng câu cá",
}

# --------------------------------------------------------------------------
# Tiện ích
# --------------------------------------------------------------------------

POS_RE = re.compile(r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*\)")


def parse_pos(text):
    if not text:
        return None
    m = POS_RE.search(text)
    if not m:
        return None
    return (int(m.group(1)), int(m.group(3)))


def txt(el, path, default=None):
    if el is None:
        return default
    v = el.findtext(path)
    if v is None:
        return default
    return v


def num(v, default=None):
    if v is None:
        return default
    try:
        f = float(v)
    except (TypeError, ValueError):
        return default
    return int(f) if f.is_integer() else f


def pretty_def(defname):
    """Tên dễ đọc cho def chưa có trong từ điển."""
    if not defname:
        return "?"
    s = defname
    for prefix in ("Building_", "Plant_", "Apparel_", "MeleeWeapon_", "Gun_",
                   "Corpse_", "Hediff_", "Thought_", "Zone_", "Frame_"):
        if s.startswith(prefix) and len(s) > len(prefix):
            s = s[len(prefix):]
            break
    s = re.sub(r"(\d+)$", "", s)
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", s)
    return s.replace("_", " ").strip() or defname


def label(d, table):
    vi = table.get(d)
    return vi if vi else pretty_def(d)


def clean(v, dash="—"):
    if v is None:
        return dash
    if isinstance(v, str) and v.strip() in ("", "null", "None"):
        return dash
    return v


def md_cell(v):
    if v is None:
        return ""
    s = str(v)
    return s.replace("|", "\\|").replace("\n", "<br>").replace("\r", "")


def fmt_num(v, nd=1):
    if v is None:
        return "—"
    if isinstance(v, float):
        if v != v:  # NaN
            return "—"
        if abs(v - round(v)) < 1e-9:
            return str(int(round(v)))
        return f"{v:.{nd}f}"
    return str(v)


def pct(v):
    if v is None:
        return "—"
    try:
        return f"{float(v) * 100:.0f}%"
    except (TypeError, ValueError):
        return str(v)


def name_of_pawn_el(p):
    """Tên hiển thị của pawn."""
    if p is None:
        return None
    n = p.find("name")
    if n is None:
        return None
    if n.find("first") is not None or n.find("nick") is not None:
        first = n.findtext("first") or ""
        nick = n.findtext("nick")
        last = n.findtext("last") or ""
        if nick:
            return f"{first} “{nick}” {last}".strip()
        return f"{first} {last}".strip()
    return (n.findtext("name") or "").strip() or None


def pawn_nick(p):
    if p is None:
        return None
    n = p.find("name")
    if n is None:
        return None
    return (n.findtext("nick") or n.findtext("first") or n.findtext("name") or "").strip() or None


def infer_gender(p):
    g = p.findtext("gender")
    if g and g != "None":
        return g
    head = txt(p, "story/headType") or ""
    if head.startswith("Male_"):
        return "Male"
    if head.startswith("Female_"):
        return "Female"
    return "?"


def flatten_el(el, prefix="", skip=(), depth=0, max_depth=25):
    """Đổi cây XML thành danh sách (đường_dẫn, giá_trị)."""
    out = []
    if depth > max_depth:
        return out
    children = list(el)
    if not children:
        v = (el.text or "").strip()
        if v:
            out.append((prefix or el.tag, v))
        return out
    counters = Counter()
    for ch in children:
        counters[ch.tag] += 1
        idx = counters[ch.tag]
        path = f"{prefix}/{ch.tag}" if prefix else ch.tag
        if counters[ch.tag] > 1:
            path = f"{path}[{idx}]"
        if any(path.startswith(s) for s in skip):
            continue
        out.extend(flatten_el(ch, path, skip, depth + 1, max_depth))
    return out


# --------------------------------------------------------------------------
# Đọc save
# --------------------------------------------------------------------------

class SaveFile:
    def __init__(self, path: Path):
        self.path = path
        self.tree = ET.parse(str(path))
        self.root = self.tree.getroot()
        self.meta = self.root.find("meta")
        self.game = self.root.find("game")
        self.world = self.game.find("world")

        self.ticks_game = num(txt(self.game, "tickManager/ticksGame"), 0) or 0
        self.game_start_abs = num(txt(self.game, "tickManager/gameStartAbsTick"), 0) or 0
        self.starting_year = num(txt(self.game, "tickManager/startingYear"), 5500) or 5500
        self.abs_tick = self.game_start_abs + self.ticks_game

        self.factions = {}          # "Faction_16" -> dict
        self.faction_order = []
        for i, f in enumerate(self.world.findall("factionManager/allFactions/li")):
            load = f.findtext("loadID")
            fid = f"Faction_{load if load is not None else i}"
            self.factions[fid] = {
                "id": fid,
                "def": f.findtext("def"),
                "name": f.findtext("name"),
                "leader": f.findtext("leader"),
                "relations": [
                    {
                        "other": r.findtext("other"),
                        "kind": r.findtext("kind") or "Neutral",
                        "goodwill": num(r.findtext("goodwill"), 0),
                    }
                    for r in f.findall("relations/li")
                ],
            }
            self.faction_order.append(fid)

        self.player_faction = None
        for fid, f in self.factions.items():
            if f["def"] == "PlayerColony":
                self.player_faction = fid
                break

        self.ideos = [
            {
                "index": i,
                "id": f"Ideo_{i}",
                "name": f.findtext("name"),
                "memberName": f.findtext("memberName"),
                "foundation": (f.find("foundation").attrib.get("Class") if f.find("foundation") is not None else None),
                "deity": f.findtext("foundation/def"),
                "culture": f.findtext("culture"),
                "hidden": f.findtext("hiddenIdeoMode"),
                "description": f.findtext("description"),
                "leaderTitleMale": f.findtext("leaderTitleMale"),
                "leaderTitleFemale": f.findtext("leaderTitleFemale"),
                "memes": [m.text for m in f.findall("memes/li")],
                "precepts": [
                    {
                        "class": pr.attrib.get("Class"),
                        "def": pr.findtext("def"),
                        "name": pr.findtext("name"),
                    }
                    for pr in f.findall("precepts/li")
                ],
                "el": f,
            }
            for i, f in enumerate(self.world.findall("ideoManager/ideos/li"))
        ]

        self.things_by_id = {}
        self.world_pawns = []
        self.maps = []
        self._index()
        self.resolve_ideo_ids()

    # -- index ---------------------------------------------------------
    def _index(self):
        wp = self.world.find("worldPawns")
        if wp is not None:
            for group in ("pawnsForcefullyKeptAsWorldPawns", "pawnsMothballed",
                          "pawnsAlive", "pawnsDead"):
                for li in wp.findall(f"{group}/li"):
                    if list(li):  # full Pawn element
                        pid = li.findtext("id")
                        rec = {
                            "group": group,
                            "pawn": "Thing_" + pid if pid else None,
                            "id": pid,
                            "def": li.findtext("def"),
                            "kind": li.findtext("kindDef"),
                            "faction": li.findtext("faction"),
                            "gender": li.findtext("gender"),
                            "age": round((num(txt(li, "ageTracker/ageBiologicalTicks"), 0) or 0) / TICKS_PER_YEAR, 2),
                            "chrono": round((self.abs_tick - (num(txt(li, "ageTracker/birthAbsTicks"), 0) or 0)) / TICKS_PER_YEAR, 2),
                            "name": name_of_pawn_el(li),
                            "map": li.findtext("map"),
                            "dead": group == "pawnsDead",
                            "el": li,
                        }
                        if pid:
                            self.things_by_id.setdefault("Thing_" + pid, li)
                    else:  # chỉ là tham chiếu
                        rec = {
                            "group": group,
                            "pawn": (li.text or "").strip(),
                            "id": ((li.text or "").strip() or "").replace("Thing_", ""),
                            "def": None, "kind": None, "faction": None, "gender": None,
                            "age": None, "chrono": None, "name": None, "map": None,
                            "dead": False,
                            "el": li,
                        }
                    self.world_pawns.append(rec)

        for i, m in enumerate(self.game.findall("maps/li")):
            md = MapData(self, m, i)
            self.maps.append(md)

    # -- tra cứu -------------------------------------------------------
    def resolve_ideo_ids(self):
        """Ideo_12 trong save là loadID, không phải index. Tìm id thật từ các tham chiếu."""
        ref_counts = Counter()
        for el in self.root.iter():
            t = (el.text or "").strip()
            if t.startswith("Ideo_"):
                ref_counts[t] += 1
        ids = [k for k, _ in ref_counts.most_common()]
        for i, ideo in enumerate(self.ideos):
            if i < len(ids) and len(self.ideos) == 1:
                ideo["id"] = ids[0]
        for i, ideo in enumerate(self.ideos):
            if len(self.ideos) > 1:
                # thử map theo thứ tự xuất hiện hiếm gặp; ưu tiên Ideo_<index>
                if f"Ideo_{i}" in ref_counts:
                    ideo["id"] = f"Ideo_{i}"

    def find_biome(self, tile=None):
        """Biome không lưu trong mapInfo; lấy từ surroundings của tale gần ô định cư nhất."""
        tm = self.game.find("taleManager")
        counts = Counter()
        if tm is None:
            return None
        for sur in tm.iter("surroundings"):
            b = sur.findtext("biome")
            if not b:
                continue
            counts[b] += 1
            if tile and (sur.findtext("tile") or "").strip() == tile:
                return b
        return counts.most_common(1)[0][0] if counts else None

    def idea_name(self, ideo_id):
        if not ideo_id:
            return None
        for ideo in self.ideos:
            if ideo["id"] == ideo_id:
                return ideo["name"]
        m = re.match(r"Ideo_(\d+)$", ideo_id)
        if m:
            idx = int(m.group(1))
            if idx < len(self.ideos):
                return self.ideos[idx]["name"]
        if len(self.ideos) == 1:
            return self.ideos[0]["name"]
        return ideo_id

    def faction_name(self, fid):
        if not fid or fid == "null":
            return "—"
        f = self.factions.get(fid)
        if not f:
            return fid
        return f"{f['name']} ({f['def']})"

    def ref_el(self, ref):
        if not ref or ref in ("null", "None"):
            return None
        return self.things_by_id.get(ref)

    def describe_ref(self, ref):
        """Mô tả 1 tham chiếu Thing_xxx hoặc 1 ô (x,0,z)."""
        if not ref or ref in ("null", "None"):
            return "—"
        el = self.ref_el(ref)
        if el is not None:
            d = el.findtext("def") or "?"
            nm = name_of_pawn_el(el) if el.attrib.get("Class") == "Pawn" else None
            pos = parse_pos(el.findtext("pos"))
            bits = [label(d, {**ITEMS, **BUILDINGS, **PLANTS}),
                    f"`{d}`"]
            if nm:
                bits.append(f"«{nm}»")
            if pos:
                bits.append(f"@({pos[0]}, {pos[1]})")
            return " ".join(bits)
        pos = parse_pos(ref)
        if pos:
            return f"ô ({pos[0]}, {pos[1]})"
        return ref

    def zone_of(self, pos, map_index=0):
        if pos is None:
            return None
        for md in self.maps:
            if md.index != map_index:
                continue
            return md.zone_lookup.get(pos)
        return None

    # -- thời gian -----------------------------------------------------
    def date_info(self):
        days = self.ticks_game / TICKS_PER_DAY
        day_of_year = days % 60
        quadrum_idx = int(day_of_year // DAYS_PER_QUADRUM) % 4
        day_in_quadrum = int(day_of_year % DAYS_PER_QUADRUM) + 1
        hour = (days % 1) * 24
        year = int(self.starting_year + days // 60)
        return {
            "year": year,
            "quadrum": QUADRUM_NAMES[quadrum_idx],
            "day_in_quadrum": day_in_quadrum,
            "day_of_year": round(day_of_year + 1, 2),
            "hour": round(hour, 2),
            "days_played": round(days, 3),
            "display": f"{year}, ngày {day_in_quadrum} {QUADRUM_NAMES[quadrum_idx]} ({int(hour):02d}:{int((hour % 1) * 60):02d})",
        }


class MapData:
    def __init__(self, save: SaveFile, el, index):
        self.save = save
        self.el = el
        self.index = index
        self.things = [c for c in el.findall("things/thing")]
        self.by_id = {}
        for th in self.things:
            i = th.findtext("id")
            if i:
                self.by_id["Thing_" + i] = th
                self.by_id[i] = th
                save.things_by_id.setdefault("Thing_" + i, th)

        self.zones = []
        self.zone_lookup = {}
        for z in el.findall("zoneManager/allZones/li"):
            cells = []
            for li in z.findall("cells/li"):
                p = parse_pos(li.text)
                if p:
                    cells.append(p)
            ztype = z.attrib.get("Class", "")
            zone = {
                "class": ztype,
                "type": ZONE_TYPES.get(ztype, pretty_def(ztype)),
                "id": z.findtext("ID"),
                "label": z.findtext("label"),
                "baseLabel": z.findtext("baseLabel"),
                "color": z.findtext("color"),
                "plantDefToGrow": z.findtext("plantDefToGrow"),
                "cells": cells,
                "settings": None,
                "el": z,
            }
            st = z.find("settings")
            if st is not None:
                zone["settings"] = {
                    "priority": st.findtext("priority"),
                    "allowedDefs": [x.text for x in st.findall("filter/allowedDefs/li") if x.text],
                    "disallowedSpecialFilters": [x.text for x in st.findall("filter/disallowedSpecialFilters/li") if x.text],
                    "allowAll": st.findtext("filter/allowAll"),
                    "disallowAll": st.findtext("filter/disallowAll"),
                }
            self.zones.append(zone)
            for p in cells:
                self.zone_lookup[p] = zone

        self.size = parse_size(el.findtext("mapInfo/size"))

    # -- tiện ích ------------------------------------------------------
    def pos(self, el):
        return parse_pos(el.findtext("pos"))

    def zone_name_at(self, pos):
        z = self.zone_lookup.get(pos)
        return z["label"] if z else None


def parse_size(s):
    if not s:
        return None
    m = re.search(r"\((\d+),\s*(\d+),\s*(\d+)\)", s)
    if m:
        return (int(m.group(1)), int(m.group(3)))
    return None


# --------------------------------------------------------------------------
# Trích xuất state
# --------------------------------------------------------------------------

def extract_pawn(save: SaveFile, p, mapdata=None, full_fields=False):
    cls = p.attrib.get("Class")
    d = {
        "id": p.findtext("id"),
        "def": p.findtext("def"),
        "class": cls,
        "kindDef": p.findtext("kindDef"),
        "faction": p.findtext("faction"),
        "faction_name": save.faction_name(p.findtext("faction")),
        "name": name_of_pawn_el(p),
        "nick": pawn_nick(p),
        "gender": infer_gender(p),
        "gender_inferred": p.findtext("gender") in (None, "", "None"),
        "map": p.findtext("map"),
        "pos": parse_pos(p.findtext("pos")),
        "pos_raw": p.findtext("pos"),
        "rot": p.findtext("rot"),
        "questTags": [x.text for x in p.findall("questTags/li")],
        "spawnedTick": num(p.findtext("spawnedTick")),
        "despawnedTick": num(p.findtext("despawnedTick")),
    }

    # tuổi
    bio = num(txt(p, "ageTracker/ageBiologicalTicks"), 0) or 0
    birth = num(txt(p, "ageTracker/birthAbsTicks"), 0) or 0
    d["age_bio"] = round(bio / TICKS_PER_YEAR, 2)
    d["age_chrono"] = round((save.abs_tick - birth) / TICKS_PER_YEAR, 2) if birth else None
    d["growth"] = num(txt(p, "ageTracker/growth"))

    # ngoại hình / xuất thân
    st = p.find("story")
    d["bodyType"] = txt(st, "bodyType")
    d["headType"] = txt(st, "headType")
    d["hairDef"] = txt(st, "hairDef")
    d["hairColor"] = txt(st, "hairColor")
    d["beard"] = txt(st, "beardDef")
    d["tattoo_face"] = txt(st, "faceTattoo")
    d["tattoo_body"] = txt(st, "bodyTattoo")
    d["favoriteColor"] = txt(st, "favoriteColorDef")
    d["childhood"] = txt(st, "childhood")
    d["adulthood"] = txt(st, "adulthood")
    d["title"] = txt(st, "title")
    d["traits"] = []
    for tr in st.findall("traits/allTraits/li") if st is not None else []:
        d["traits"].append({
            "def": tr.findtext("def"),
            "name": label(tr.findtext("def"), TRAITS),
            "degree": num(tr.findtext("degree")),
            "sourceGene": tr.findtext("sourceGene"),
        })

    # gene / xenotype
    d["xenotype"] = txt(p, "genes/xenotype")
    d["endogenes"] = [g.findtext("def") for g in p.findall("genes/endogenes/li")]
    d["xenogenes"] = [g.findtext("def") for g in p.findall("genes/xenogenes/li")]

    # ideo
    d["ideo"] = txt(p, "ideo/ideo")
    d["ideo_name"] = save.idea_name(d["ideo"])
    d["ideo_certainty"] = num(txt(p, "ideo/certainty"))

    # kỹ năng
    d["skills"] = []
    for s in p.findall("skills/skills/li"):
        d["skills"].append({
            "def": s.findtext("def"),
            "name": label(s.findtext("def"), SKILLS),
            "level": num(s.findtext("level"), 0),
            "passion": s.findtext("passion"),
            "xp": num(s.findtext("xpSinceLastLevel")),
            "xp_today": num(s.findtext("xpSinceMidnight")),
        })

    # nhu cầu + suy nghĩ
    d["needs"] = []
    d["mood"] = None
    d["thoughts"] = []
    for nd in p.findall("needs/needs/li"):
        defn = nd.findtext("def")
        d["needs"].append({
            "def": defn,
            "name": label(defn, NEEDS),
            "level": num(nd.findtext("curLevel")),
            "lastNonStarvingTick": num(nd.findtext("lastNonStarvingTick")),
        })
        if defn == "Mood":
            d["mood"] = num(nd.findtext("curLevel"))
            seen = set()
            for li in nd.find("thoughts").iter("li") if nd.find("thoughts") is not None else []:
                tdef = li.findtext("def")
                if not tdef:
                    continue
                key = (tdef, li.findtext("otherPawn"), li.findtext("age"))
                if key in seen:
                    continue
                seen.add(key)
                d["thoughts"].append({
                    "def": tdef,
                    "name": label(tdef, THOUGHTS),
                    "class": li.attrib.get("Class"),
                    "age_ticks": num(li.findtext("age")),
                    "otherPawn": li.findtext("otherPawn"),
                    "otherPawn_name": pawn_nick(save.ref_el(li.findtext("otherPawn"))) if li.findtext("otherPawn") not in (None, "null") else None,
                    "opinionOffset": num(li.findtext("opinionOffset")),
                    "moodPowerFactor": num(li.findtext("moodPowerFactor")),
                    "food": li.findtext("foodThoughtDescription"),
                    "stage": li.findtext("stage"),
                })

    # sức khỏe
    d["hediffs"] = []
    hs = p.find("healthTracker/hediffSet")
    if hs is not None:
        for h in hs.findall("hediffs/li"):
            part = h.find("part")
            d["hediffs"].append({
                "class": h.attrib.get("Class"),
                "def": h.findtext("def"),
                "name": label(h.findtext("def") or "", HEDIFFS),
                "severity": num(h.findtext("severity")),
                "part_body": txt(part, "body") if part is not None else None,
                "part_index": num(txt(part, "index")) if part is not None else None,
                "isPermanent": h.findtext("isPermanent"),
                "painCategory": h.findtext("painCategory"),
                "age_ticks": num(h.findtext("ageTicks")),
                "visible": h.findtext("visible"),
            })
        d["hediffSet_other"] = flatten_el(hs, "hediffSet", skip=("hediffSet/hediffs",))

    # trang bị
    def gear(container_path):
        out = []
        for li in p.findall(container_path):
            out.append({
                "def": li.findtext("def"),
                "name": label(li.findtext("def") or "", {**ITEMS, **BUILDINGS}),
                "id": li.findtext("id"),
                "stuff": li.findtext("stuff"),
                "quality": li.findtext("quality"),
                "health": num(li.findtext("health")),
                "stackCount": num(li.findtext("stackCount"), 1),
                "color": li.findtext("color"),
                "sourcePrecept": li.findtext("sourcePrecept"),
            })
        return out

    d["apparel"] = gear("apparel/wornApparel/innerList/li")
    d["equipment"] = gear("equipment/equipment/innerList/li")
    d["inventory"] = gear("inventory/innerContainer/innerList/li")
    d["carried_filth"] = [
        {"def": f.findtext("def"), "thickness": num(f.findtext("thickness"))}
        for f in p.findall("filth/carriedFilth/li")
    ]

    # công việc
    vals = []
    for li in p.findall("workSettings/priorities/vals/li"):
        vals.append(num((li.text or "0").strip(), 0) or 0)
    if len(vals) == len(WORK_TYPES):
        names = WORK_TYPES
    elif len(vals) <= len(WORK_TYPES):
        names = WORK_TYPES[:len(vals)]  # bản game cũ/ít DLC: vẫn đúng thứ tự Core
    else:
        names = [(f"W{i:02d}", f"W{i:02d}") for i in range(len(vals))]
    d["work_priorities"] = [
        {"index": i, "def": names[i][0], "name": names[i][1], "value": v}
        for i, v in enumerate(vals)
    ]
    d["work_raw"] = vals
    d["medCare"] = txt(p, "playerSettings/medCare")
    d["hostilityResponse"] = txt(p, "playerSettings/hostilityResponse")
    d["master"] = txt(p, "playerSettings/master")
    d["displayOrder"] = num(txt(p, "playerSettings/displayOrder"))
    d["allowedAreas"] = [
        {"key": k.findtext("key"), "value": (k.findtext("value") or "")}
        for k in p.findall("playerSettings/allowedAreas/keys/li")
    ]
    d["outfit"] = txt(p, "outfits/curOutfit")
    d["drugPolicy"] = txt(p, "drugs/curAssignedDrugs")
    d["foodPolicy"] = txt(p, "foodRestriction/curRestriction")
    d["readingPolicy"] = txt(p, "reading/curAssignment")
    d["timetable"] = [(x.text or "").strip() for x in p.findall("timetable/times/li")]
    d["joinStatus"] = txt(p, "guest/joinStatus")

    # trạng thái hiện tại
    cj = p.find("jobs/curJob")
    d["job"] = None
    if cj is not None:
        d["job"] = {
            "def": cj.findtext("def"),
            "targetA": cj.findtext("targetA"),
            "targetA_desc": save.describe_ref(cj.findtext("targetA")),
            "targetB": cj.findtext("targetB"),
            "targetB_desc": save.describe_ref(cj.findtext("targetB")),
            "count": num(cj.findtext("count")),
            "workGiverDef": cj.findtext("workGiverDef"),
            "startTick": num(cj.findtext("startTick")),
            "driver": (p.find("jobs/curDriver").attrib.get("Class") if p.find("jobs/curDriver") is not None else None),
            "lastJobTag": txt(p, "mindState/lastJobTag"),
        }
    ms = p.find("mindState")
    d["mentalState"] = txt(ms, "mentalStateHandler/curState/def")
    d["mentalState_class"] = (ms.find("mentalStateHandler/curState").attrib.get("Class") if ms is not None and ms.find("mentalStateHandler/curState") is not None else None)
    d["inspiration"] = txt(ms, "inspirationHandler/curState/def")
    d["ticksBelowMinor"] = num(txt(ms, "mentalBreaker/ticksBelowMinor"))
    d["lastSleepDisturbedTick"] = num(p.findtext("lastSleepDisturbedTick"))
    d["psychicEntropy"] = num(txt(p, "psychicEntropy/currentPsyfocus"))
    d["psyfocus_limit"] = txt(p, "psychicEntropy/limitEntropyAmount")

    # quan hệ
    d["relations"] = []
    for r in p.findall("social/directRelations/li"):
        other = r.findtext("otherPawn")
        d["relations"].append({
            "def": r.findtext("def"),
            "otherPawn": other,
            "otherPawn_name": pawn_nick(save.ref_el(other)) if other and other != "null" else None,
        })
    d["lastInteraction"] = txt(p, "interactions/lastInteraction")

    # sở hữu / hoàng gia
    d["ownedBed"] = txt(p, "ownership/ownedBed")
    d["royalty_titles"] = [t.findtext("def") for t in p.findall("royalty/titles/li")]
    d["abilities"] = [a.findtext("def") for a in p.findall("abilities/abilities/li")]

    if full_fields:
        d["raw_fields"] = dict(flatten_el(
            p, "",
            skip=("records/", "mindState/thinkData", "verbTracker", "natives",
                  "meleeVerbs", "jobs/curJob/targetQueue", "rotationTracker",
                  "pather", "traits", "needs/needs/li[1]/thoughts"),
        ))
    return d


def extract_map(save: SaveFile, md: MapData, full_fields=False):
    out = {
        "index": md.index,
        "size": md.size,
        "weather": txt(md.el, "weatherManager/curWeather"),
        "weather_age": num(txt(md.el, "weatherManager/curWeatherAge")),
        "weather_last": txt(md.el, "weatherManager/lastWeather"),
        "conditions": [
            {"def": c.findtext("def"), "class": c.attrib.get("Class"),
             "duration": num(c.findtext("duration")), "permanent": c.findtext("permanent")}
            for c in md.el.findall("gameConditionManager/activeConditions/li")
        ],
        "designations": [],
        "buildings_player": [],
        "buildings_other": [],
        "items": [],
        "plants_sown": [],
        "plants_wild": Counter(),
        "plants_wild_growth": defaultdict(list),
        "dead_plants": Counter(),
        "corpses": [],
        "pawns": [],
        "animals": [],
        "filth": Counter(),
        "chunks": Counter(),
        "zones": [],
        "areas": [],
        "unclassified": [],
        "pawns_offmap": [],
        "class_counts": Counter(),
    }

    player = save.player_faction

    # zones
    for z in md.zones:
        out["zones"].append({
            "label": z["label"],
            "type": z["type"],
            "id": z["id"],
            "plantDefToGrow": z["plantDefToGrow"],
            "cell_count": len(z["cells"]),
            "bbox": (
                [min(c[0] for c in z["cells"]), max(c[0] for c in z["cells"]),
                 min(c[1] for c in z["cells"]), max(c[1] for c in z["cells"])]
                if z["cells"] else None
            ),
            "cells": z["cells"],
            "settings": z["settings"],
        })

    # areas
    for a in md.el.findall("areaManager/areas/li"):
        out["areas"].append({
            "class": a.attrib.get("Class"),
            "id": a.findtext("ID"),
            "trueCount": num(txt(a, "innerGrid/trueCount")),
        })

    # designations
    for li in md.el.findall("designationManager/allDesignations/li"):
        target = li.findtext("target")
        el = md.by_id.get(target) or save.things_by_id.get(target)
        out["designations"].append({
            "def": li.findtext("def"),
            "target": target,
            "target_def": el.findtext("def") if el is not None else None,
            "target_pos": parse_pos(el.findtext("pos")) if el is not None else parse_pos(target),
        })

    # things
    for th in md.things:
        cls = th.attrib.get("Class", "")
        d = th.findtext("def") or ""
        pos = parse_pos(th.findtext("pos"))
        faction = th.findtext("faction")
        out["class_counts"][cls or "(không có Class)"] += 1

        if cls == "Plant" or cls == "DeadPlant":
            growth = num(th.findtext("growth"))
            health = num(th.findtext("health"))
            sown = th.findtext("sown") == "True"
            rec = {
                "def": d, "class": cls, "pos": pos, "growth": growth,
                "health": health, "sown": sown, "age": num(th.findtext("age")),
                "id": th.findtext("id"),
            }
            if cls == "DeadPlant":
                out["dead_plants"][d] += 1
            elif sown:
                out["plants_sown"].append(rec)
            else:
                out["plants_wild"][d] += 1
                if growth is not None:
                    out["plants_wild_growth"][d].append(growth)
            continue

        if cls == "Filth":
            out["filth"][d] += 1
            continue

        if cls == "Corpse":
            inner = th.find("innerContainer/innerList/li")
            inner_id = inner.text.strip() if inner is not None and inner.text else None
            target = save.things_by_id.get(inner_id) if inner_id else None
            wp = next((w for w in save.world_pawns if w["pawn"] == inner_id), None)
            out["corpses"].append({
                "def": d,
                "id": th.findtext("id"),
                "pos": pos,
                "inner": inner_id,
                "inner_def": target.findtext("def") if target is not None else None,
                "inner_name": (name_of_pawn_el(target) if target is not None else (wp or {}).get("name"))
                              or (target.findtext("def") if target is not None else None),
                "zone": md.zone_name_at(pos),
                "rot": num(th.findtext("rotProgress"), num(th.findtext("rot"))),
            })
            continue

        if cls == "Pawn":
            if d == "Human":
                pmap = th.findtext("map")
                if pmap is not None and pmap not in (str(md.index), ""):
                    out.setdefault("pawns_offmap", []).append(extract_pawn(save, th, md, full_fields))
                    continue
                out["pawns"].append(extract_pawn(save, th, md, full_fields))
            else:
                out["animals"].append({
                    "id": th.findtext("id"),
                    "def": d,
                    "name": name_of_pawn_el(th),
                    "gender": infer_gender(th),
                    "age_bio": round((num(txt(th, "ageTracker/ageBiologicalTicks"), 0) or 0) / TICKS_PER_YEAR, 2),
                    "faction": faction,
                    "faction_name": save.faction_name(faction) if faction else "hoang dã",
                    "pos": pos,
                    "kindDef": th.findtext("kindDef"),
                    "hunger": num(txt(th, "needs/needs/li[2]/curLevel")),
                    "health": num(txt(th, "healthTracker/hediffSet/hediffs/li/severity")),
                })
            continue

        if cls.startswith("Building") or cls == "Frame" or d in BUILDINGS:
            rec = {
                "def": d,
                "name": label(d, BUILDINGS),
                "class": cls,
                "id": th.findtext("id"),
                "pos": pos,
                "stuff": th.findtext("stuff"),
                "quality": th.findtext("quality"),
                "health": num(th.findtext("health")),
                "maxHealth": num(th.findtext("maxHealth")),
                "faction": faction,
                "rot": num(th.findtext("rotProgress"), num(th.findtext("rot"))),
                "spawnedTick": num(th.findtext("spawnedTick")),
                "extra": {},
            }
            # nội dung đặc biệt
            for tag in ("fuel", "allowAutoRefuel", "opened", "forbidden", "glowOn"):
                v = th.findtext(tag)
                if v is not None:
                    rec["extra"][tag] = v
            bills = []
            for b in th.findall("billStack/bills/li"):
                bills.append({
                    "recipe": b.findtext("recipe"),
                    "repeatCount": num(b.findtext("repeatCount")),
                    "targetCount": num(b.findtext("targetCount")),
                    "suspended": b.findtext("suspended"),
                    "allowedSkillRange": b.findtext("allowedSkillRange"),
                })
            if bills:
                rec["extra"]["bills"] = bills
            res = th.find("resourceContainer")
            if res is not None:
                cont = []
                for li in res.findall("innerList/li"):
                    cont.append({"def": li.findtext("def"), "stackCount": num(li.findtext("stackCount"), 1)})
                if cont:
                    rec["extra"]["contents"] = cont
            if th.findtext("gravshipName"):
                rec["extra"]["gravshipName"] = th.findtext("gravshipName")
            if faction == player:
                out["buildings_player"].append(rec)
            else:
                out["buildings_other"].append(rec)
            continue

        # vật phẩm rời
        if cls in ("ThingWithComps", "Medicine", "Apparel", "Thing"):
            count = num(th.findtext("stackCount"), 1) or 1
            out["items"].append({
                "def": d,
                "name": label(d, ITEMS),
                "class": cls,
                "id": th.findtext("id"),
                "pos": pos,
                "stackCount": count,
                "stuff": th.findtext("stuff"),
                "quality": th.findtext("quality"),
                "health": num(th.findtext("health")),
                "zone": md.zone_name_at(pos),
                "forbidden": th.findtext("forbidden"),
            })
            continue

        if "Chunk" in d:
            out["chunks"][d] += 1
            continue

        out["unclassified"].append({
            "class": cls, "def": d, "id": th.findtext("id"), "pos": pos,
        })

    # tổng hợp vật phẩm theo def
    totals = Counter()
    for it in out["items"]:
        totals[it["def"]] += it["stackCount"]
    out["item_totals"] = dict(totals)

    out["class_counts"] = dict(out["class_counts"])
    out["filth"] = dict(out["filth"])
    out["chunks"] = dict(out["chunks"])
    out["plants_wild"] = dict(out["plants_wild"])
    out["dead_plants"] = dict(out["dead_plants"])
    out["plants_wild_growth"] = {
        k: {"count": len(v), "min": min(v), "max": max(v), "avg": sum(v) / len(v)}
        for k, v in out["plants_wild_growth"].items()
    }
    return out


def extract_state(save: SaveFile, full_fields=False, all_pawns=False):
    g = save.game
    st = {
        "source": {
            "file": str(save.path),
            "size_bytes": save.path.stat().st_size,
        },
        "meta": {
            "gameVersion": txt(save.meta, "gameVersion"),
            "modIds": [x.text for x in save.meta.findall("modIds/li")],
            "modSteamIds": [x.text for x in save.meta.findall("modSteamIds/li")],
            "modNames": [x.text for x in save.meta.findall("modNames/li")],
        },
        "game": {
            "ticksGame": save.ticks_game,
            "date": save.date_info(),
            "playTimeSeconds": num(txt(g, "info/realPlayTimeInteracting")),
            "scenario": {
                "name": txt(g, "scenario/name"),
                "summary": txt(g, "scenario/summary"),
                "description": txt(g, "scenario/description"),
                "parts": [
                    {"class": p.attrib.get("Class"), "def": p.findtext("def")}
                    for p in g.findall("scenario/parts/li")
                ],
            },
            "storyteller": txt(g, "storyteller/def"),
            "difficulty": txt(g, "storyteller/difficulty"),
            "playSettings": {
                k: txt(g, f"playSettings/{k}")
                for k in ("useWorkPriorities", "showZones", "autoHomeArea", "showRoomStats")
            },
            "storyState": {
                "lastThreatBigTick": num(txt(g, "storyState/lastThreatBigTick")),
                "lastRaidFaction": txt(g, "storyState/lastRaidFaction") or txt(save.maps[0].el, "storyState/lastRaidFaction") if save.maps else txt(g, "storyState/lastRaidFaction"),
                "lastRaidFaction_name": save.faction_name(txt(g, "storyState/lastRaidFaction") or (txt(save.maps[0].el, "storyState/lastRaidFaction") if save.maps else None)),
            },
            "storyWatcher": {
                "numRaidsEnemy": num(txt(g, "storyWatcher/statsRecord/numRaidsEnemy")),
                "numThreatsQueued": num(txt(g, "storyWatcher/statsRecord/numThreatsQueued")),
                "adaptDays": num(txt(g, "storyWatcher/watcherPopAdaptation/adaptDays")),
            },
        },
        "world": {
            "name": txt(save.world, "info/name"),
            "seed": txt(save.world, "info/seedString"),
            "coverage": num(txt(save.world, "info/planetCoverage")),
            "rainfall": txt(save.world, "info/overallRainfall"),
            "temperature": txt(save.world, "info/overallTemperature"),
            "pollution": num(txt(save.world, "info/pollution")),
            "startingTile": txt(g, "info/startingTile"),
            "biome": save.find_biome(txt(g, "info/startingTile")),
            "startingPawns": [x.text for x in g.findall("info/startingAndOptionalPawns/li")],
            "factions": [
                {
                    "id": f["id"],
                    "def": f["def"],
                    "name": f["name"],
                    "leader": f["leader"],
                    "player": f["id"] == save.player_faction,
                    "relations": f["relations"],
                }
                for f in save.factions.values()
            ],
        },
        "ideoligion": [
            {
                "index": i["index"],
                "id": i["id"],
                "name": i["name"],
                "memberName": i["memberName"],
                "foundation": i["foundation"],
                "deity": i["deity"],
                "culture": i["culture"],
                "hidden": i["hidden"],
                "leaderTitleMale": i["leaderTitleMale"],
                "leaderTitleFemale": i["leaderTitleFemale"],
                "description": i["description"],
                "memes": i["memes"],
                "precepts": i["precepts"],
            }
            for i in save.ideos
        ],
        "research": extract_research(g),
        "quests": extract_quests(g),
        "anomaly": extract_anomaly(g),
        "letters": extract_letters(g),
        "world_pawns": [
            {k: v for k, v in w.items() if k != "el"} for w in save.world_pawns
        ],
        "maps": [],
    }
    for md in save.maps:
        st["maps"].append(extract_map(save, md, full_fields))
    return st


def extract_research(g):
    rm = g.find("researchManager")
    if rm is None:
        return {}
    keys = [x.text for x in rm.findall("progress/keys/li")]
    vals = [num(x.text, 0) for x in rm.findall("progress/values/li")]
    done, partial = [], []
    for k, v in zip(keys, vals):
        if v and v >= 1:
            done.append(k)
        elif v:
            partial.append({"def": k, "progress": v})
    return {
        "current": rm.findtext("currentProj"),
        "completed": done,
        "partial": partial,
        "all": [
            {"def": k, "progress": v, "name": RESEARCH_VI.get(k, pretty_def(k))}
            for k, v in zip(keys, vals)
        ],
    }


def extract_quests(g):
    out = []
    for q in g.findall("questManager/quests/li"):
        out.append({
            "name": q.findtext("name"),
            "root": q.findtext("root"),
            "appearanceTick": num(q.findtext("appearanceTick")),
            "acceptanceTick": num(q.findtext("acceptanceTick")),
            "acceptedBy": q.findtext("acceptedBy"),
            "description": q.findtext("description"),
            "parts": [p.attrib.get("Class") for p in q.findall("parts/li")],
            "ended": q.findtext("ended"),
            "endOutcome": q.findtext("endOutcome"),
        })
    return out


def extract_anomaly(g):
    for li in g.findall("components/li"):
        if li.attrib.get("Class") == "GameComponent_Anomaly":
            return {
                "levelDef": li.findtext("levelDef"),
                "monolith": li.findtext("monolith"),
                "nextHarbingerTreeCheckTick": num(li.findtext("nextHarbingerTreeCheckTick")),
                "voidNodeActivator": li.findtext("voidNodeActivator"),
                "metalHellReturnTick": num(li.findtext("metalHellReturnTick")),
            }
    return None


def extract_letters(g):
    out = []
    for li in g.findall("history/archive/archivables/li"):
        out.append({
            "class": li.attrib.get("Class"),
            "def": li.findtext("def"),
            "label": li.findtext("label"),
            "text": li.findtext("text"),
            "arrivalTick": num(li.findtext("arrivalTick")),
            "messageID": li.findtext("ID"),
            "relatedFaction": li.findtext("relatedFaction"),
        })
    return out


# --------------------------------------------------------------------------
# Render Markdown
# --------------------------------------------------------------------------

class Doc:
    def __init__(self):
        self.lines = []

    def w(self, s=""):
        self.lines.append(s)

    def h(self, level, text):
        self.w()
        self.w("#" * level + " " + text)
        self.w()

    def p(self, text):
        self.w(text)
        self.w()

    def table(self, headers, rows, max_rows=None):
        if not rows:
            self.w("*(trống)*")
            self.w()
            return
        self.w("| " + " | ".join(md_cell(h) for h in headers) + " |")
        self.w("|" + "|".join(["---"] * len(headers)) + "|")
        for r in rows[: max_rows or len(rows)]:
            self.w("| " + " | ".join(md_cell(c) for c in r) + " |")
        if max_rows and len(rows) > max_rows:
            self.w(f"| ... | *còn {len(rows) - max_rows} dòng, xem JSON/CSV* |" + " |" * (len(headers) - 2))
        self.w()

    def kv(self, pairs):
        self.table(["Thuộc tính", "Giá trị"], pairs)

    def text(self):
        return "\n".join(self.lines).rstrip() + "\n"


def render_markdown(save: SaveFile, state: dict) -> str:
    d = Doc()
    d.h(1, f"RIMWORLD SAVE DUMP — {save.path.name}")
    d.p(f"*Sinh tự động bởi `rimworld_dump.py` · phiên bản game `{state['meta']['gameVersion']}` · "
        f"{state['game']['date']['display']} · {state['game']['date']['days_played']} ngày đã chơi · "
        f"{len(state['maps'][0]['pawns'])} pawn người · map {state['maps'][0]['size'][0]}×{state['maps'][0]['size'][1]}*")

    d.h(2, "Mục lục")
    d.p("0. Nguồn & mod\n1. Tổng quan game\n2. Thế giới & phe\n3. Tôn giáo\n4. Nghiên cứu\n"
        "5. PAWN (đầy đủ)\n6. Động vật\n7. Công trình\n8. Môi trường / khu vực / rác\n"
        "9. Vùng (zone)\n10. Vật phẩm trên map\n"
        "11. Cây trồng & thảm thực vật\n12. Đánh dấu (designations)\n13. Xác chết\n14. Nhật ký / thư\n"
        "15. Nhiệm vụ\n16. Anomaly\n17. Pawn ngoài map\n18. Kiểm tra độ phủ\n19. File dữ liệu kèm theo")

    # 0
    d.h(2, "0. Nguồn & mod")
    d.kv([
        ("File", f"`{state['source']['file']}`"),
        ("Kích thước", f"{state['source']['size_bytes']:,} bytes"),
        ("Game version", state["meta"]["gameVersion"]),
        ("Mods", "<br>".join(state["meta"]["modNames"])),
        ("Mod IDs", "<br>".join(state["meta"]["modIds"])),
    ])

    # 1
    g = state["game"]
    d.h(2, "1. Tổng quan game")
    d.kv([
        ("Ngày trong game", g["date"]["display"]),
        ("Tick", f"{g['ticksGame']:,} ({g['date']['days_played']} ngày)"),
        ("Kịch bản", g["scenario"]["name"]),
        ("Tóm tắt", g["scenario"]["summary"] or ""),
        ("Mô tả", (g["scenario"]["description"] or "").replace("\n", "<br>")),
        ("Các phần kịch bản", ", ".join(f"{p['def']}" for p in g["scenario"]["parts"])),
        ("Người kể chuyện", g["storyteller"]),
        ("Độ khó", g["difficulty"]),
        ("Ưu tiên công việc thủ công", g["playSettings"]["useWorkPriorities"]),
        ("Số vụ đột kích", g["storyWatcher"]["numRaidsEnemy"]),
        ("Số mối đe dọa đang chờ", g["storyWatcher"]["numThreatsQueued"]),
        ("Phe đột kích gần nhất", g["storyState"]["lastRaidFaction_name"]),
    ])

    # 2
    d.h(2, "2. Thế giới & phe")
    w = state["world"]
    d.kv([
        ("Hành tinh", w["name"]),
        ("Seed", w["seed"]),
        ("Độ phủ", w["coverage"]),
        ("Lượng mưa", w["rainfall"]),
        ("Nhiệt độ", w["temperature"]),
        ("Ô bắt đầu", w["startingTile"]),
        ("Biome", w.get("biome") or "—"),
        ("Pawn khởi đầu", ", ".join(w["startingPawns"])),
    ])
    d.h(3, "Các phe")
    rows = []
    for f in w["factions"]:
        rel = {r["other"]: r for r in f["relations"]}
        player = rel.get(save.player_faction) or {}
        rows.append([
            f["id"], f["name"], f["def"],
            player.get("kind", "—"), player.get("goodwill", "—"),
            "CÓ" if f["player"] else "",
        ])
    d.table(["ID", "Tên", "Def", "Quan hệ với bạn", "Thiện chí", "Phe người chơi"], rows)

    # 3
    d.h(2, "3. Tôn giáo (Ideoligion)")
    for ideo in state["ideoligion"]:
        d.h(3, f"{ideo['name']} (`{ideo['id']}`)")
        d.kv([
            ("Tên gọi thành viên", ideo["memberName"]),
            ("Nền tảng", ideo["foundation"]),
            ("Deity", ideo["deity"]),
            ("Văn hóa", ideo["culture"]),
            ("Ẩn", ideo["hidden"]),
            ("Chức danh nam", ideo["leaderTitleMale"]),
            ("Chức danh nữ", ideo["leaderTitleFemale"]),
            ("Memes", ", ".join(ideo["memes"]) or "—"),
            ("Mô tả", ideo["description"] or "—"),
        ])
        d.h(4, f"Tín điều ({len(ideo['precepts'])})")
        d.table(["#", "Lớp", "Def", "Tên"],
                [[i + 1, p["class"], p["def"], p["name"]] for i, p in enumerate(ideo["precepts"])])

    # 4
    r = state["research"]
    d.h(2, "4. Nghiên cứu")
    d.p(f"**Đang nghiên cứu:** `{r['current']}` ({RESEARCH_VI.get(r['current'], pretty_def(r['current'] or ''))})")
    d.h(3, f"Đã hoàn thành ({len(r['completed'])})")
    d.table(["Def", "Tên"],
            [[k, RESEARCH_VI.get(k, pretty_def(k))] for k in r["completed"]])
    if r["partial"]:
        d.h(3, "Đang làm dở")
        d.table(["Def", "Tiến độ"], [[p["def"], pct(p["progress"])] for p in r["partial"]])
    d.h(3, f"Toàn bộ bảng nghiên cứu ({len(r['all'])})")
    d.table(["Def", "Tên", "Tiến độ"], [[x["def"], x["name"], pct(x["progress"])] for x in r["all"]])

    # 5 pawns
    d.h(2, "5. PAWN — toàn bộ chỉ số")
    for mp in state["maps"]:
        if not mp["pawns"]:
            continue
        d.h(3, f"Map {mp['index']} — {len(mp['pawns'])} pawn người")
        for pw in mp["pawns"]:
            render_pawn_md(d, save, pw)
        if mp.get("pawns_offmap"):
            d.h(3, f"Pawn nằm trong <things> nhưng ở map khác ({len(mp['pawns_offmap'])})")
            d.table(["ID", "Tên", "Def/Kind", "Phe", "Map"],
                    [[pw["id"], pw["name"] or "—", f"{pw['def']}/{pw['kindDef']}",
                      pw["faction_name"], clean(pw["map"])] for pw in mp["pawns_offmap"]])

    # 6 animals
    d.h(2, "6. Động vật trên map")
    for mp in state["maps"]:
        if not mp["animals"]:
            continue
        d.h(3, f"Map {mp['index']} — {len(mp['animals'])} con")
        d.table(["ID", "Loài", "Tên", "Giới", "Tuổi", "Phe", "Ô"],
                [[a["id"], a["def"], a["name"] or "—", a["gender"], a["age_bio"],
                  a["faction_name"], f"({a['pos'][0]}, {a['pos'][1]})" if a["pos"] else "—"]
                 for a in mp["animals"]])

    # 7 buildings
    d.h(2, "7. Công trình")
    for mp in state["maps"]:
        d.h(3, f"Map {mp['index']}")
        d.h(4, f"Công trình của người chơi ({len(mp['buildings_player'])})")
        d.p("**Tổng hợp theo loại:**")
        d.w()
        agg = Counter()
        mats = defaultdict(Counter)
        for b in mp["buildings_player"]:
            agg[b["def"]] += 1
            mats[b["def"]][b["stuff"] or "—"] += 1
        d.table(["Tên", "Def", "SL", "Vật liệu"],
                [[label(k, BUILDINGS), f"`{k}`", v,
                  ", ".join(f"{m}×{c}" for m, c in mats[k].most_common())] for k, v in agg.most_common()])
        d.p("**Chi tiết từng công trình:**")
        d.w()
        mp["buildings_player"].sort(key=lambda b: (b["def"], b["pos"] or (0, 0)))
        rows = []
        for b in mp["buildings_player"]:
            extra = []
            if b["extra"].get("bills"):
                extra.append("bill: " + ", ".join(
                    f"{x['recipe']}×{x['repeatCount'] or x['targetCount']}" for x in b["extra"]["bills"]))
            if b["extra"].get("contents"):
                extra.append("chứa: " + ", ".join(
                    f"{label(c['def'], ITEMS)}×{c['stackCount']}" for c in b["extra"]["contents"]))
            for k in ("fuel", "opened", "gravshipName", "allowAutoRefuel"):
                if k in b["extra"]:
                    extra.append(f"{k}={b['extra'][k]}")
            rows.append([
                b["id"], b["name"], f"`{b['def']}`",
                f"({b['pos'][0]}, {b['pos'][1]})" if b["pos"] else "—",
                b["stuff"] or "—", b["quality"] or "—",
                f"{fmt_num(b['health'])}", b["rot"],
                "; ".join(extra),
            ])
        d.table(["ID", "Tên", "Def", "Ô", "Vật liệu", "Phẩm chất", "HP", "Rot", "Ghi chú"], rows)

        d.h(4, f"Công trình khác / cổ ({len(mp['buildings_other'])})")
        grouped = OrderedDict()
        for b in mp["buildings_other"]:
            grouped.setdefault((b["def"], b["name"]), []).append(b)
        rows = []
        for (defn, nm), lst in sorted(grouped.items(), key=lambda kv: -len(kv[1])):
            poss = ", ".join(f"({b['pos'][0]},{b['pos'][1]})" for b in lst[:8] if b["pos"])
            if len(lst) > 8:
                poss += f" … (+{len(lst) - 8})"
            rows.append([nm, f"`{defn}`", len(lst), poss])
        d.table(["Tên", "Def", "SL", "Vị trí (tối đa 8)"], rows)

        d.h(4, "Sơ đồ ASCII khu căn cứ")
        d.p("```\n" + ascii_map(save, save.maps[mp["index"]]) + "\n```")

    # 7b environment
    d.h(2, "8. Môi trường, thời tiết, khu vực (area), rác")
    for mp in state["maps"]:
        md = save.maps[mp["index"]]
        d.h(3, f"Map {mp['index']}")
        d.kv([
            ("Kích thước", f"{mp['size'][0]} × {mp['size'][1]}" if mp["size"] else "—"),
            ("Biome", state["world"].get("biome") or "—"),
            ("Thời tiết", mp["weather"]),
            ("Thời tiết trước", mp["weather_last"]),
            ("Tuổi thời tiết (tick)", mp["weather_age"]),
            ("Điều kiện đang hoạt động", ", ".join(
                f"{clean(c['def'])}" + (f" ({c['class']})" if c['class'] else "")
                for c in mp["conditions"]) or "—"),
        ])
        d.h(4, "Khu vực (areas)")
        d.table(["Lớp", "ID", "Số ô"],
                [[a["class"], a["id"], a["trueCount"]] for a in mp["areas"]])
        d.h(4, f"Rác/bẩn ({sum(mp['filth'].values())})")
        d.table(["Def", "SL"], [[k, v] for k, v in sorted(mp["filth"].items(), key=lambda kv: -kv[1])])
        if mp["chunks"]:
            d.h(4, f"Khối đá/đống đổ nát ({sum(mp['chunks'].values())})")
            d.table(["Def", "SL"], [[k, v] for k, v in sorted(mp["chunks"].items(), key=lambda kv: -kv[1])])
        d.h(4, "Thống kê object theo lớp")
        d.table(["Lớp", "SL"], [[k, v] for k, v in sorted(mp["class_counts"].items(), key=lambda kv: -kv[1])])

    # 9 zones
    d.h(2, "9. Vùng (zones)")
    for mp in state["maps"]:
        if not mp["zones"]:
            continue
        d.h(3, f"Map {mp['index']}")
        for z in mp["zones"]:
            d.h(4, f"{z['label']} — {z['type']} ({z['cell_count']} ô)")
            bb = z["bbox"]
            pairs = [
                ("Lớp", z["type"]),
                ("ID", z["id"]),
                ("Số ô", z["cell_count"]),
                ("Bao", f"x {bb[0]}–{bb[1]}, z {bb[2]}–{bb[3]}" if bb else "—"),
                ("Cây trồng", f"{label(z['plantDefToGrow'], PLANTS)} (`{z['plantDefToGrow']}`)" if z["plantDefToGrow"] else "—"),
            ]
            if z["settings"]:
                pairs.append(("Ưu tiên", z["settings"]["priority"]))
                pairs.append(("Số def được phép", len(z["settings"]["allowedDefs"])))
                pairs.append(("Bộ lọc đặc biệt bị cấm", ", ".join(z["settings"]["disallowedSpecialFilters"]) or "—"))
            d.kv(pairs)
            contents = defaultdict(int)
            for it in mp["items"]:
                if it["zone"] == z["label"]:
                    contents[it["def"]] += it["stackCount"]
            for c in mp["corpses"]:
                if c["zone"] == z["label"]:
                    contents[c["def"]] += 1
            if contents:
                d.w("**Nội dung trong zone:**")
                d.w()
                d.table(["Def", "Tên", "SL"],
                        [[k, label(k, ITEMS), v] for k, v in sorted(contents.items(), key=lambda x: -x[1])])
            if z["settings"] and z["settings"]["allowedDefs"]:
                d.w(f"**Danh sách {len(z['settings']['allowedDefs'])} def được phép:**")
                d.w()
                d.w("```")
                line = []
                for i, x in enumerate(z["settings"]["allowedDefs"]):
                    line.append(x)
                    if len(line) == 4:
                        d.w("  ".join(f"{v:<32}" for v in line))
                        line = []
                if line:
                    d.w("  ".join(f"{v:<32}" for v in line))
                d.w("```")
                d.w()

    # 9 items
    d.h(2, "10. Vật phẩm trên map")
    for mp in state["maps"]:
        if not mp["items"]:
            continue
        d.h(3, f"Map {mp['index']}")
        d.h(4, f"Tổng hợp theo loại ({len(mp['item_totals'])} loại)")
        zone_tot = defaultdict(lambda: defaultdict(int))
        for it in mp["items"]:
            zone_tot[it["zone"] or "ngoài zone"][it["def"]] += it["stackCount"]
        rows = []
        for defn, total in sorted(mp["item_totals"].items(), key=lambda kv: -kv[1]):
            parts = ", ".join(f"{zn}: {zone_tot[zn][defn]}" for zn in sorted(zone_tot) if zone_tot[zn][defn])
            rows.append([label(defn, ITEMS), f"`{defn}`", total, parts])
        d.table(["Tên", "Def", "Tổng SL", "Phân bố"], rows)

        d.h(4, f"Từng stack ({len(mp['items'])})")
        d.table(["ID", "Def", "Ô", "SL", "Vật liệu", "Phẩm chất", "HP", "Zone"],
                [[i["id"], i["def"], f"({i['pos'][0]},{i['pos'][1]})" if i["pos"] else "—",
                  i["stackCount"], i["stuff"] or "—", i["quality"] or "—",
                  fmt_num(i["health"]), i["zone"] or "—"] for i in mp["items"]])

    # 10 plants
    d.h(2, "11. Cây trồng & thảm thực vật")
    for mp in state["maps"]:
        d.h(3, f"Map {mp['index']}")
        d.h(4, f"Cây do người chơi trồng ({len(mp['plants_sown'])})")
        rows = []
        for p in mp["plants_sown"]:
            rows.append([p["def"], label(p["def"], PLANTS),
                         f"({p['pos'][0]},{p['pos'][1]})" if p["pos"] else "—",
                         pct(p["growth"]), fmt_num(p["health"]),
                         f"{p['age'] / TICKS_PER_DAY:.2f}" if p["age"] else "—"])
        d.table(["Def", "Tên", "Ô", "Lớn", "HP", "Tuổi (ngày)"], rows)
        if mp["plants_sown"]:
            grows = [p["growth"] for p in mp["plants_sown"] if p["growth"] is not None]
            d.p(f"Thống kê lớn: min {pct(min(grows))} · max {pct(max(grows))} · TB {pct(sum(grows) / len(grows))}")
        d.h(4, f"Cây hoang ({sum(mp['plants_wild'].values())})")
        rows = []
        for defn, count in sorted(mp["plants_wild"].items(), key=lambda kv: -kv[1]):
            st = mp["plants_wild_growth"].get(defn)
            rows.append([defn, label(defn, PLANTS), count,
                         pct(st["min"]) if st else "—", pct(st["avg"]) if st else "—",
                         pct(st["max"]) if st else "—"])
        d.table(["Def", "Tên", "SL", "Lớn min", "Lớn TB", "Lớn max"], rows)
        if mp["dead_plants"]:
            d.h(4, "Cây chết")
            d.table(["Def", "Tên", "SL"],
                    [[k, label(k, PLANTS), v] for k, v in sorted(mp["dead_plants"].items(), key=lambda kv: -kv[1])])

    # 11 designations
    d.h(2, "12. Đánh dấu (designations)")
    for mp in state["maps"]:
        if not mp["designations"]:
            continue
        counts = Counter(x["def"] for x in mp["designations"])
        d.h(3, f"Map {mp['index']} — " + ", ".join(f"{k}: {v}" for k, v in counts.items()))
        d.table(["Loại", "Mục tiêu", "Def mục tiêu", "Ô"],
                [[x["def"], x["target"], x["target_def"] or "—",
                  f"({x['target_pos'][0]},{x['target_pos'][1]})" if x["target_pos"] else "—"]
                 for x in mp["designations"]])

    # 12 corpses
    d.h(2, "13. Xác chết")
    for mp in state["maps"]:
        if not mp["corpses"]:
            continue
        d.table(["Def", "Ô", "Bên trong", "Tên", "Zone", "Rot"],
                [[c["def"], f"({c['pos'][0]},{c['pos'][1]})" if c["pos"] else "—",
                  c["inner"] or "—", c["inner_name"] or "—", c["zone"] or "—", c["rot"] or 0]
                 for c in mp["corpses"]])

    # 13 letters
    d.h(2, "14. Nhật ký / thư")
    rows = []
    for x in state["letters"]:
        rows.append([
            x["class"], x["label"] or x["def"] or "—",
            x["arrivalTick"] if x["arrivalTick"] is not None else (x["messageID"] or ""),
            (x["text"] or "").replace("\n", " ")[:400],
        ])
    d.table(["Loại", "Tiêu đề", "Tick/ID", "Nội dung"], rows)

    # 14 quests
    d.h(2, "15. Nhiệm vụ")
    if state["quests"]:
        for q in state["quests"]:
            d.h(3, q["name"] or q["root"])
            d.kv([
                ("Root", q["root"]),
                ("Xuất hiện", q["appearanceTick"]),
                ("Chấp nhận", q["acceptanceTick"]),
                ("Người nhận", clean(q["acceptedBy"])),
                ("Mô tả", (q["description"] or "").replace("\n", "<br>")),
                ("Số phần", len(q["parts"])),
            ])
    else:
        d.p("*(không có nhiệm vụ)*")

    # 15 anomaly
    d.h(2, "16. Anomaly")
    a = state["anomaly"]
    if a:
        d.kv([(k, v) for k, v in a.items()])
    else:
        d.p("*(không có dữ liệu anomaly)*")

    # 16 world pawns
    d.h(2, "17. Pawn ngoài map (world pawns)")
    groups = Counter(x["group"] for x in state["world_pawns"])
    d.p("Tổng: " + ", ".join(f"{k}: {v}" for k, v in groups.items())
        + " — pawn còn sống ngoài map là dân các phe, khách, thương nhân…; pawn chết là người đã chết ở nơi khác.")
    refs = [x for x in state["world_pawns"] if x["group"] == "pawnsForcefullyKeptAsWorldPawns"]
    if refs:
        d.p(f"*({len(refs)} mục `pawnsForcefullyKeptAsWorldPawns` chỉ là tham chiếu ID tới các pawn "
            f"đã có trong bảng dưới — bỏ qua để khỏi trùng.)*")
    d.table(["Nhóm", "Pawn ID", "Tên", "Def/Kind", "Phe", "Giới", "Tuổi", "Niên đại", "Map"],
            [[x["group"], x["id"] or x["pawn"], x["name"] or "—",
              f"{x['def'] or ''}/{x['kind'] or ''}", save.faction_name(x["faction"]) if x["faction"] else "—",
              x["gender"] or "—", fmt_num(x["age"], 2), fmt_num(x["chrono"], 2), x["map"] or "—"]
             for x in state["world_pawns"] if x["group"] != "pawnsForcefullyKeptAsWorldPawns"])

    # 18 coverage
    d.h(2, "18. Kiểm tra độ phủ — mọi object đều được phân loại")
    for mp in state["maps"]:
        total = sum(mp["class_counts"].values())
        classified = (len(mp["pawns"]) + len(mp.get("pawns_offmap", [])) + len(mp["animals"]) + len(mp["buildings_player"])
                      + len(mp["buildings_other"]) + len(mp["items"]) + len(mp["plants_sown"])
                      + sum(mp["plants_wild"].values()) + sum(mp["dead_plants"].values())
                      + sum(mp["filth"].values()) + sum(mp["chunks"].values())
                      + len(mp["corpses"]))
        d.kv([
            ("Tổng object trong <things>", total),
            ("Đã phân loại", classified),
            ("Chưa phân loại", len(mp["unclassified"])),
        ])
        if mp["unclassified"]:
            d.table(["Lớp", "Def", "ID", "Ô"],
                    [[u["class"], u["def"], u["id"],
                      f"({u['pos'][0]},{u['pos'][1]})" if u["pos"] else "—"] for u in mp["unclassified"]])

    # 19 files
    d.h(2, "19. File dữ liệu kèm theo")
    d.p("- `state.json` — toàn bộ state ở trên dạng JSON (đầy đủ, kể cả mọi trường XML của pawn)\n"
        "- `things_all.csv` — mọi object trên map\n"
        "- `plants.csv` — mọi cây\n"
        "- `items.csv` — mọi stack vật phẩm\n"
        "- `buildings.csv` — mọi công trình\n"
        "- `pawns_skills.csv`, `pawns_needs.csv`, `pawns_work.csv`\n"
        "- `zones_cells.csv` — từng ô của từng zone")
    return d.text()


def render_pawn_md(d: Doc, save: SaveFile, pw: dict):
    title = pw["name"] or pw["id"]
    d.h(3, f"{title} — `{pw['id']}`")

    d.h(4, "Hồ sơ")
    d.kv([
        ("Def / Kind", f"`{pw['def']}` / `{pw['kindDef']}`"),
        ("Phe", pw["faction_name"]),
        ("Giới tính", pw["gender"] + (" *(save không lưu, suy ra từ headType)*" if pw.get("gender_inferred") else "")),
        ("Tuổi sinh học", fmt_num(pw["age_bio"], 2)),
        ("Tuổi niên đại", fmt_num(pw["age_chrono"], 2)),
        ("Ô", f"({pw['pos'][0]}, {pw['pos'][1]})" if pw["pos"] else "—"),
        ("Body type", clean(pw["bodyType"])),
        ("Đầu / tóc / râu", f"{clean(pw['headType'])} / {clean(pw['hairDef'])} / {clean(pw['beard'])}"),
        ("Màu tóc", pw["hairColor"]),
        ("Hình xăm", f"mặt: {pw['tattoo_face'] or '—'} · người: {pw['tattoo_body'] or '—'}"),
        ("Màu yêu thích", pw["favoriteColor"] or "—"),
        ("Xuất thân (nhỏ)", f"{clean(pw['childhood'])} — {BACKSTORIES.get((pw['childhood'] or '').rstrip('0123456789'), '—')}"),
        ("Xuất thân (lớn)", f"{clean(pw['adulthood'])} — {BACKSTORIES.get((pw['adulthood'] or '').rstrip('0123456789'), '—')}"),
        ("Chức danh", pw["title"] or "—"),
        ("Xenotype", clean(pw["xenotype"])),
        ("Gen nội sinh", ", ".join(pw["endogenes"]) or "—"),
        ("Gen ngoại sinh", ", ".join(pw["xenogenes"]) or "—"),
        ("Tôn giáo", f"{pw['ideo_name']} (tin cậy {pct(pw['ideo_certainty'])})"),
        ("Trạng thái guest", pw["joinStatus"] or "—"),
        ("Tâm trạng", f"**{pct(pw['mood'])}**" + (" ⚠" if (pw["mood"] or 1) < 0.4 else "")),
        ("Số ngày dưới ngưỡng xấu", fmt_num((pw["ticksBelowMinor"] or 0) / TICKS_PER_DAY, 2)),
        ("Med care", clean(pw["medCare"])),
        ("Phản ứng", clean(pw["hostilityResponse"])),
        ("Thứ tự hiển thị", pw["displayOrder"]),
        ("Chủ sở hữu giường", pw["ownedBed"] or "—"),
        ("Chức tước", ", ".join(pw["royalty_titles"]) or "—"),
        ("Kỹ năng (ability)", ", ".join(pw["abilities"]) or "—"),
        ("Psyfocus", pw["psychicEntropy"]),
    ])

    d.h(4, "Tính cách")
    d.table(["Def", "Tên", "Degree", "Gene nguồn"],
            [[t["def"], t["name"], t["degree"] if t["degree"] is not None else "—", clean(t["sourceGene"])]
             for t in pw["traits"]])

    d.h(4, "Kỹ năng")
    rows = []
    for s in pw["skills"]:
        rows.append([s["name"], f"`{s['def']}`", fmt_num(s["level"]), PASSION.get(s["passion"], s["passion"]),
                     fmt_num(s["xp"]), fmt_num(s["xp_today"])])
    d.table(["Kỹ năng", "Def", "Cấp", "Đam mê", "XP", "XP hôm nay"], rows)

    d.h(4, "Nhu cầu")
    d.table(["Nhu cầu", "Def", "Mức"],
            [[n["name"], f"`{n['def']}`", f"{pct(n['level'])}"] for n in pw["needs"]])

    d.h(4, f"Suy nghĩ / ký ức ({len(pw['thoughts'])})")
    rows = []
    for t in pw["thoughts"]:
        age_d = f"{t['age_ticks'] / TICKS_PER_DAY:.2f}" if t["age_ticks"] is not None else "—"
        rows.append([t["name"], f"`{t['def']}`", age_d,
                     t["otherPawn_name"] or "—",
                     fmt_num(t["opinionOffset"], 2),
                     fmt_num(t["moodPowerFactor"], 3),
                     t["food"] or ""])
    d.table(["Suy nghĩ", "Def", "Tuổi (ngày)", "Pawn liên quan", "Opinion", "Mood power", "Ghi chú"], rows)

    d.h(4, "Sức khỏe")
    if pw["hediffs"]:
        d.table(["Bệnh/tật", "Def", "Lớp", "Severity", "Bộ phận", "Vĩnh viễn", "Đau", "Tuổi (ngày)"],
                [[h["name"], f"`{h['def']}`", h["class"], fmt_num(h["severity"], 3),
                  f"{h['part_body'] or '—'}#{h['part_index'] if h['part_index'] is not None else '—'}",
                  h["isPermanent"] or "—", h["painCategory"] or "—",
                  f"{h['age_ticks'] / TICKS_PER_DAY:.2f}" if h["age_ticks"] else "—"]
                 for h in pw["hediffs"]])
    else:
        d.p("*(khỏe mạnh, không có hediff nào)*")

    d.h(4, "Trang bị & hành trang")
    d.table(["Loại", "Def", "Tên", "Vật liệu", "Phẩm chất", "HP", "SL"],
            [["Mặc", f"`{a['def']}`", a["name"], a["stuff"] or "—", a["quality"] or "—", fmt_num(a["health"]), a["stackCount"]]
             for a in pw["apparel"]]
            + [["Cầm", f"`{a['def']}`", a["name"], a["stuff"] or "—", a["quality"] or "—", fmt_num(a["health"]), a["stackCount"]]
               for a in pw["equipment"]]
            + [["Trong túi", f"`{a['def']}`", a["name"], a["stuff"] or "—", a["quality"] or "—", fmt_num(a["health"]), a["stackCount"]]
               for a in pw["inventory"]])
    if pw["carried_filth"]:
        d.p("Bẩn đang mang: " + ", ".join(
            f"{f['def']}" + (f"×{fmt_num(f['thickness'])}" if f["thickness"] is not None else "")
            for f in pw["carried_filth"]))

    d.h(4, "Ưu tiên công việc")
    d.p(f"0 = tắt · 1 = cao nhất · 4 = thấp nhất. Có {len(pw['work_priorities'])} mục, theo thứ tự nạp "
        f"WorkTypeDef: Core 20 loại → Biotech `Childcare` → Anomaly `DarkStudy` → Odyssey `Fishing`. "
        f"Tên def lạ sẽ hiện dạng `Wxx`; có thể nạp ánh xạ riêng bằng `--worktypes`.")
    d.table(["#", "Công việc", "Def", "Ưu tiên"],
            [[w["index"], w["name"], f"`{w['def']}`", w["value"]] for w in pw["work_priorities"]])

    d.h(4, "Chính sách & lịch")
    d.kv([
        ("Trang phục", clean(pw["outfit"])),
        ("Thuốc", clean(pw["drugPolicy"])),
        ("Thức ăn", clean(pw["foodPolicy"])),
        ("Đọc sách", clean(pw["readingPolicy"])),
        ("Khu vực được phép", ", ".join(f"{a['key']}={a['value']}" for a in pw["allowedAreas"]) or "—"),
    ])
    if pw["timetable"]:
        d.p("**Lịch 24 giờ:** " + " · ".join(
            f"{i:02d}h:{v}" for i, v in enumerate(pw["timetable"])))

    d.h(4, "Trạng thái hiện tại")
    job = pw["job"] or {}
    d.kv([
        ("Job", f"`{job.get('def')}` ({job.get('workGiverDef')})" if job.get("def") else "— (đang rảnh)"),
        ("Mục tiêu A", clean(job.get("targetA_desc"))),
        ("Mục tiêu B", clean(job.get("targetB_desc"))),
        ("Số lượng", clean(job.get("count"))),
        ("Driver", clean(job.get("driver"))),
        ("Trạng thái tinh thần", pw["mentalState"] or "bình thường"),
        ("Cảm hứng", pw["inspiration"] or "—"),
        ("Tương tác cuối", clean(pw["lastInteraction"])),
    ])
    if pw["relations"]:
        d.h(4, "Quan hệ trực tiếp")
        d.table(["Loại", "Pawn", "Tên"],
                [[r["def"], r["otherPawn"], r["otherPawn_name"]] for r in pw["relations"]])

    if pw.get("raw_fields"):
        d.h(4, f"Toàn bộ trường XML ({len(pw['raw_fields'])})")
        rows = [[f"`{k}`", (v[:160] + "…") if len(v) > 160 else v] for k, v in pw["raw_fields"].items()]
        d.table(["Đường dẫn", "Giá trị"], rows)


def ascii_map(save: SaveFile, md: MapData, max_w=150, max_h=90):
    """Sơ đồ ASCII quanh khu căn cứ của người chơi (chỉ công trình của bạn)."""
    glyphs = {
        "Wall": "#", "Door": "+", "Bed": "B", "Bedroll": "b", "TorchLamp": "*",
        "StandingLamp": "l", "Table1x2c": "T", "Table2x2c": "T", "Table3x3c": "T",
        "Stool": "o", "DiningChair": "c", "HorseshoesPin": "H", "FueledStove": "F",
        "ElectricStove": "F", "SimpleResearchBench": "R", "ResearchBench": "R",
        "Column": "I", "Sarcophagus": "X", "Frame_DiningChair": "d",
        "FueledGenerator": "G", "WoodFiredGenerator": "G", "Battery": "=",
        "SolarGenerator": "S", "WindTurbine": "W", "GeothermalGenerator": "E",
        "Cooler": "C", "Heater": "h", "Grave": "X",
    }
    marks = {}
    for z in md.zones:
        ch = "~" if "Growing" in z["class"] else ("s" if "Stockpile" in z["class"] else "z")
        for p in z["cells"]:
            marks[p] = ch

    pts = []
    for th in md.things:
        cls = th.attrib.get("Class", "")
        if not cls.startswith("Building") and cls != "Frame":
            continue
        if th.findtext("faction") != save.player_faction:
            continue
        pos = parse_pos(th.findtext("pos"))
        if not pos:
            continue
        d = th.findtext("def") or ""
        marks[pos] = glyphs.get(d, (d[:1] or "?").upper())
        pts.append(pos)

    if not pts:
        return "(chưa có công trình nào của người chơi)"

    xs = [p[0] for p in pts]
    zs = [p[1] for p in pts]
    x0, x1 = min(xs) - 4, max(xs) + 4
    z0, z1 = min(zs) - 3, max(zs) + 3
    if x1 - x0 > max_w:
        mid = (x0 + x1) // 2
        x0, x1 = mid - max_w // 2, mid + max_w // 2
    if z1 - z0 > max_h:
        mid = (z0 + z1) // 2
        z0, z1 = mid - max_h // 2, mid + max_h // 2

    lines = []
    for z in range(z0, z1 + 1):
        lines.append(f"{z:4} " + "".join(marks.get((x, z), ".") for x in range(x0, x1 + 1)))
    lines.append("     " + "".join(str(x // 10 % 10) for x in range(x0, x1 + 1)))
    lines.append("     " + "".join(str(x % 10) for x in range(x0, x1 + 1)))
    legend = ("Chú thích: # tường · + cửa · B giường · T bàn · o ghế đẩu · c ghế ăn · F bếp · R bàn nghiên cứu · "
              "* đuốc · H móng ngựa · ~ ruộng · s kho · I cột · d khung xây dở · "
              "chữ cái khác = chữ đầu của def (ví dụ G = máy phát)")
    return "\n".join(lines) + "\n" + legend


# --------------------------------------------------------------------------
# CSV
# --------------------------------------------------------------------------

def write_csv(path: Path, headers, rows):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(headers)
        for r in rows:
            w.writerow(r)


def export_csvs(save: SaveFile, state: dict, outdir: Path):
    all_things = []
    plants = []
    items = []
    buildings = []
    skills = []
    needs = []
    work = []
    zone_cells = []

    for md in save.maps:
        mp = state["maps"][md.index]
        zone_of = md.zone_lookup
        for th in md.things:
            cls = th.attrib.get("Class", "")
            d = th.findtext("def") or ""
            pos = parse_pos(th.findtext("pos"))
            z = zone_of.get(pos)
            all_things.append([
                th.findtext("id"), cls, d, pos[0] if pos else "", pos[1] if pos else "",
                th.findtext("rot") if th.findtext("rot") is not None else "",
                th.findtext("stackCount") if th.findtext("stackCount") is not None else "",
                th.findtext("stuff") if th.findtext("stuff") is not None else "",
                th.findtext("quality") if th.findtext("quality") is not None else "",
                th.findtext("health") if th.findtext("health") is not None else "",
                th.findtext("growth") if th.findtext("growth") is not None else "",
                th.findtext("faction") if th.findtext("faction") is not None else "",
                th.findtext("sown") if th.findtext("sown") is not None else "",
                z["label"] if z else "",
                mp["index"],
            ])
            if cls in ("Plant", "DeadPlant"):
                plants.append([th.findtext("id"), d, cls, pos[0] if pos else "", pos[1] if pos else "",
                               th.findtext("growth") or "", th.findtext("health") or "",
                               th.findtext("age") or "", th.findtext("sown") or "",
                               th.findtext("defoliator") or "", z["label"] if z else ""])
        for it in mp["items"]:
            items.append([it["id"], it["def"], it["name"], it["pos"][0] if it["pos"] else "",
                          it["pos"][1] if it["pos"] else "", it["stackCount"], it["stuff"] or "",
                          it["quality"] or "", it["health"] or "", it["zone"] or ""])
        for owner, lst in (("player", mp["buildings_player"]), ("other", mp["buildings_other"])):
            for b in lst:
                extra = json.dumps({k: v for k, v in b["extra"].items() if k != "contents"}, ensure_ascii=False)
                buildings.append([b["id"], b["def"], b["name"], b["pos"][0] if b["pos"] else "",
                                  b["pos"][1] if b["pos"] else "", b["stuff"] or "", b["quality"] or "",
                                  b["health"] or "", b["faction"] or "", b["rot"] or "", extra, owner])
        for z in mp["zones"]:
            for (x, zz) in z["cells"]:
                zone_cells.append([mp["index"], z["label"], z["type"], x, zz])
        for pw in mp["pawns"]:
            for s in pw["skills"]:
                skills.append([pw["id"], pw["name"], s["def"], s["name"], s["level"], s["passion"] or "", s["xp"] or ""])
            for n in pw["needs"]:
                needs.append([pw["id"], pw["name"], n["def"], n["name"], n["level"]])
            for w_ in pw["work_priorities"]:
                work.append([pw["id"], pw["name"], w_["index"], w_["def"], w_["name"], w_["value"]])

    write_csv(outdir / "things_all.csv",
              ["id", "class", "def", "x", "z", "rot", "stack", "stuff", "quality",
               "health", "growth", "faction", "sown", "zone", "map"], all_things)
    write_csv(outdir / "plants.csv",
              ["id", "def", "class", "x", "z", "growth", "health", "age_ticks", "sown",
               "defoliator", "zone"], plants)
    write_csv(outdir / "items.csv",
              ["id", "def", "name", "x", "z", "stack", "stuff", "quality", "health", "zone"], items)
    write_csv(outdir / "buildings.csv",
              ["id", "def", "name", "x", "z", "stuff", "quality", "health", "faction",
               "rot", "extra", "owner"], buildings)
    write_csv(outdir / "pawns_skills.csv",
              ["pawn_id", "pawn", "skill", "name", "level", "passion", "xp"], skills)
    write_csv(outdir / "pawns_needs.csv",
              ["pawn_id", "pawn", "need", "name", "level"], needs)
    write_csv(outdir / "pawns_work.csv",
              ["pawn_id", "pawn", "index", "work_type", "name", "priority"], work)
    write_csv(outdir / "zones_cells.csv",
              ["map", "zone", "type", "x", "z"], zone_cells)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Đọc file save RimWorld (.rws) và xuất toàn bộ state ra Markdown/JSON/CSV.")
    ap.add_argument("save", help="đường dẫn file .rws")
    ap.add_argument("-o", "--out", default="dump", help="thư mục xuất (mặc định: ./dump)")
    ap.add_argument("--no-csv", action="store_true", help="không xuất CSV")
    ap.add_argument("--md-only", action="store_true", help="chỉ xuất Markdown")
    ap.add_argument("--raw", action="store_true", help="xuất XML gốc của từng pawn")
    ap.add_argument("--no-full-fields", action="store_true",
                    help="không kèm bảng 'toàn bộ trường XML' trong báo cáo")
    ap.add_argument("--all-pawns", action="store_true",
                    help="(mặc định đã có) coi mọi pawn Human, kể cả không thuộc phe người chơi")
    ap.add_argument("--worktypes", help="file JSON tuỳ chỉnh ánh xạ index -> tên work type")
    args = ap.parse_args(argv)

    if args.worktypes:
        data = json.loads(Path(args.worktypes).read_text(encoding="utf-8"))
        global WORK_TYPES
        WORK_TYPES = [(x["def"], x["name"]) for x in data]

    path = Path(args.save)
    if not path.exists():
        print(f"Không tìm thấy file: {path}", file=sys.stderr)
        return 2

    print(f"Đang đọc {path} …")
    save = SaveFile(path)
    print(f"  game {txt(save.meta, 'gameVersion')} · {len(save.maps)} map · "
          f"{sum(len(m.things) for m in save.maps):,} object")

    state = extract_state(save, full_fields=not args.no_full_fields)

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    if not args.md_only:
        (outdir / "state.json").write_text(
            json.dumps(state, ensure_ascii=False, indent=1, default=str),
            encoding="utf-8")
        print(f"  → {outdir / 'state.json'}")

    if not args.no_csv and not args.md_only:
        export_csvs(save, state, outdir)
        print(f"  → CSV trong {outdir}")

    md = render_markdown(save, state)
    (outdir / "report.md").write_text(md, encoding="utf-8")
    print(f"  → {outdir / 'report.md'} ({len(md):,} ký tự)")

    if args.raw:
        for mp in state["maps"]:
            for pw in mp["pawns"]:
                el = save.things_by_id.get("Thing_" + pw["id"])
                if el is None:
                    continue
                raw_path = outdir / f"pawn_{pw['id']}.xml"
                raw_path.write_text(ET.tostring(el, encoding="unicode"), encoding="utf-8")
        print(f"  → XML gốc của pawn trong {outdir}")

    for mp in state["maps"]:
        print(f"  map {mp['index']}: {len(mp['pawns'])} pawn · {len(mp['buildings_player'])} công trình "
              f"· {len(mp['items'])} stack · {sum(mp['plants_wild'].values())} cây hoang "
              f"· {len(mp['zones'])} zone")
    return 0


if __name__ == "__main__":
    sys.exit(main())
