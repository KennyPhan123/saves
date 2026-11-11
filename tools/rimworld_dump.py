#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rimworld_dump.py — Đọc file save RimWorld (.rws) và xuất TOÀN BỘ state ra
Markdown + JSON + CSV (không bỏ sót mục nào), kèm một bản cô đọng để đưa cho AI.

Cách dùng nhanh nhất — CHỈ ghi đúng 1 file cho AI đọc (tự chứa đủ, không tạo thư mục dump):
    python3 tools/rimworld_dump.py "Autosave-4.rws" --ai-only ai_state.md

Chế độ đầy đủ:
    python3 tools/rimworld_dump.py "Autosave-4.rws"

Kết quả của chế độ đầy đủ mặc định nằm trong thư mục ./dump/:
    dump/ai_state.md          — ★ FILE ĐƯA CHO AI: cảnh báo cần xử lý ngay, từng người,
                                 ma trận công việc, sơ đồ căn cứ + phòng, kho, ruộng,
                                 đe doạ, nhiệm vụ, dòng thời gian, nhật ký chiến đấu,
                                 nhật ký trò chuyện… (một file, ~100 KB)
    dump/report.md            — báo cáo đầy đủ từng dòng để tra cứu
    dump/state.json           — toàn bộ state dạng máy đọc được
    dump/things_all.csv       — MỌI object trên map (25k+ dòng)
    dump/terrain.csv          — địa hình / mái / đá-quặng / sương mù / nhiệt độ của TỪNG ô
    dump/plants.csv           — MỌI cây (kể cả cây hoang)
    dump/items.csv            — mọi stack vật phẩm
    dump/buildings.csv        — mọi công trình
    dump/pawns_skills.csv     — kỹ năng từng pawn
    dump/pawns_needs.csv      — nhu cầu từng pawn
    dump/pawns_work.csv       — ưu tiên công việc từng pawn
    dump/pawns_health.csv     — từng vết thương / bệnh của từng pawn
    dump/zones_cells.csv      — từng ô của từng zone
    dump/pawn_<id>.xml        — XML gốc của từng pawn (nếu --raw)

Ví dụ khác:
    python3 tools/rimworld_dump.py save.rws -o out --raw
    python3 tools/rimworld_dump.py save.rws --no-csv --md-only

Những thứ được giải mã thêm ngoài XML thường (xem tools/README.md):
    - các lưới nén (địa hình, mái, sương mù, vách đá/quặng, nhiệt độ, khu vực, khí, tài nguyên sâu);
    - ngày giờ địa phương đúng theo múi giờ của ô bản đồ;
    - phòng (game không lưu, công cụ tự loang tìm vùng kín);
    - nhiệm vụ, nhóm AI (lord), mech, bản vẽ xây dựng, lịch sử của cải/tâm trạng;
    - nhật ký chiến đấu (battleLog: ai bắn/đánh ai, trúng bao nhiêu, ai gục/chết) và
      nhật ký tương tác xã hội (playLog: ai nói gì với ai).

Script chỉ ĐỌC file save, không bao giờ ghi/sửa file .rws.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import math
import os
import re
import struct
import sys
import zlib
import xml.etree.ElementTree as ET
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

# --------------------------------------------------------------------------
# Hằng số & bảng tên
# --------------------------------------------------------------------------

TICKS_PER_HOUR = 2_500
TICKS_PER_DAY = 60_000
TICKS_PER_TWELFTH = 300_000
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
    "DiningChair": "Ghế ăn",
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


def other_pawn_label(save, ref):
    """Tên pawn được nhắc tới trong một ký ức / quan hệ; thú không tên -> 'Crow (thú hoang)'."""
    if not ref or ref in ("null", "None"):
        return None
    el = save.ref_el(ref)
    if el is not None:
        nm = pawn_nick(el)
        if nm:
            return nm
        d = el.findtext("def") or "?"
        if d == "Human":
            return f"người không tên ({ref.replace('Thing_', '')})"
        fac = el.findtext("faction")
        return f"{d} (thú hoang)" if not fac or fac == "null" else f"{d} (thú có chủ)"
    m = re.match(r"^Thing_(.+?)(\d+)$", ref)
    return f"{m.group(1)} (không còn trong save)" if m else ref


def infer_gender(p):
    """Game chỉ ghi <gender> khi khác mặc định (Male); mech ghi 'None'."""
    g = p.findtext("gender")
    if g:
        return g
    return "Male"


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
# Giải mã dữ liệu nén trong save (lưới địa hình, mái, sương mù, đá/quặng nén…)
# --------------------------------------------------------------------------
# RimWorld lưu các lưới theo ô dưới dạng base64(deflate(mảng ushort/bit)).
# Mỗi ô của lưới địa hình/mái/"đồ vật nén" chứa shortHash của def:
#     shortHash = (ushort)(GenText.StableStringHash(defName) % 65535)
# Save không lưu bảng hash -> tự băm lại tên def đã biết để tra ngược.
# Thứ tự ô: index = z * width + x (x tăng về Đông, z tăng về Bắc).

def stable_string_hash(s):
    """Verse.GenText.StableStringHash (int32 có dấu)."""
    h = 23
    for ch in s:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return h - 0x100000000 if h >= 0x80000000 else h


def short_hash(def_name):
    """Verse.ShortHashGiver — chưa tính trường hợp va chạm (game sẽ +1 khi trùng)."""
    return int(math.fmod(stable_string_hash(def_name), 65535)) & 0xFFFF


_STONES = ["Sandstone", "Granite", "Limestone", "Slate", "Marble"]

TERRAIN_DEF_NAMES = (
    ["Soil", "SoilRich", "MossyTerrain", "MarshyTerrain", "Gravel", "Sand", "SoftSand",
     "Mud", "Ice", "ThinIce", "PackedDirt", "Marsh", "Riverbank",
     "WaterDeep", "WaterOceanDeep", "WaterMovingChestDeep", "WaterShallow",
     "WaterOceanShallow", "WaterMovingShallow",
     "Underwall", "BurnedWoodPlankFloor", "BurnedCarpet", "Bridge", "HeavyBridge",
     "BrokenAsphalt", "Concrete", "PavedTile", "WoodPlankFloor", "MetalTile",
     "SilverTile", "GoldTile", "SterileTile", "StrawMatting",
     "CarpetRed", "CarpetGreen", "CarpetBlue", "CarpetCream", "CarpetDark",
     "FungalGravel", "AncientTile", "AncientConcrete", "Voidmetal", "Flesh",
     "Substructure", "GravshipSubstructure", "OrbitalPlatform", "MechanoidPlatform",
     "AncientMegastructure", "Space", "LavaDeep", "LavaShallow", "CooledLava",
     "VolcanicRock"]
    + [f"{s}_{k}" for s in _STONES for k in ("Rough", "RoughHewn", "Smooth")]
    + [f"Tile{s}" for s in _STONES]
    + [f"Flagstone{s}" for s in _STONES]
)

ROOF_DEF_NAMES = ["RoofConstructed", "RoofRockThick", "RoofRockThin"]

# ThingDef có saveCompressible = true (không nằm trong <things> mà nằm trong
# <compressedThingMapDeflate>): vách đá tự nhiên, quặng, đá đã mài, khối đá vụn…
MINEABLE_ORE_DEF_NAMES = [
    "MineableSteel", "MineableSilver", "MineableGold", "MineableUranium",
    "MineablePlasteel", "MineableJade", "MineableComponentsIndustrial",
    "MineableGravlite", "MineableObsidian", "MineableVacstone", "MineableBioferrite",
]
COMPRESSIBLE_THING_DEF_NAMES = (
    list(_STONES) + ["Vacstone", "Obsidian", "Basalt"]
    + MINEABLE_ORE_DEF_NAMES
    + [f"Smoothed{s}" for s in _STONES]
    + [f"Chunk{s}" for s in _STONES]
    + ["ChunkSlagSteel", "ChunkMechanoidSlag", "ChunkVacstone", "ChunkObsidian",
       "CollapsedRocks", "RaisedRocks"]
)

TERRAIN_VI = {
    "Soil": "đất", "SoilRich": "đất màu mỡ", "Gravel": "sỏi", "Sand": "cát",
    "SoftSand": "cát mềm", "Mud": "bùn", "MarshyTerrain": "đất lầy", "Marsh": "đầm lầy",
    "MossyTerrain": "đất rêu", "Ice": "băng", "PackedDirt": "đất nện",
    "WaterShallow": "nước nông", "WaterDeep": "nước sâu",
    "WaterMovingShallow": "nước chảy nông", "WaterMovingChestDeep": "nước chảy sâu",
    "WaterOceanShallow": "biển nông", "WaterOceanDeep": "biển sâu",
    "BrokenAsphalt": "nhựa đường vỡ (đường cổ)", "WoodPlankFloor": "sàn gỗ",
    "Concrete": "bê tông", "PavedTile": "gạch lát", "AncientConcrete": "bê tông cổ",
    "AncientTile": "gạch cổ", "MetalTile": "sàn kim loại", "SterileTile": "sàn vô trùng",
    "StrawMatting": "thảm rơm", "Bridge": "cầu", "Underwall": "dưới tường",
}
for _s, _vi in (("Sandstone", "sa thạch"), ("Granite", "granite"), ("Limestone", "đá vôi"),
                ("Slate", "đá phiến"), ("Marble", "cẩm thạch")):
    TERRAIN_VI[f"{_s}_Rough"] = f"nền {_vi} thô"
    TERRAIN_VI[f"{_s}_RoughHewn"] = f"nền {_vi} đẽo thô"
    TERRAIN_VI[f"{_s}_Smooth"] = f"nền {_vi} mài nhẵn"
    TERRAIN_VI[f"Tile{_s}"] = f"gạch {_vi}"
    TERRAIN_VI[f"Flagstone{_s}"] = f"đá lát {_vi}"

ROOF_VI = {"RoofConstructed": "mái xây", "RoofRockThin": "mái đá mỏng",
           "RoofRockThick": "mái núi dày (không phá được)"}


def _hash_table(names):
    table = {}
    for n in names:
        table.setdefault(short_hash(n), n)
    return table


TERRAIN_HASH = _hash_table(TERRAIN_DEF_NAMES)
ROOF_HASH = _hash_table(ROOF_DEF_NAMES)
COMPRESSED_HASH = _hash_table(COMPRESSIBLE_THING_DEF_NAMES)
# Tài nguyên dưới lòng đất (máy quét sâu + khoan sâu): lưới lưu hash của vật phẩm đào được.
DEEP_RESOURCE_HASH = _hash_table((
    "Steel", "Silver", "Gold", "Uranium", "Plasteel", "Jade", "ComponentIndustrial",
    "Chemfuel", "Bioferrite", "VacstoneChunk",
))
# GasGrid: mỗi ô một int32 (little-endian) — byte 0..3 lần lượt là mật độ (0..255) của:
GAS_TYPES = ("BlindSmoke", "ToxGas", "RotStink", "DeadlifeDust")
GAS_VI = {
    "BlindSmoke": "khói mù", "ToxGas": "khí độc", "RotStink": "mùi xác thối", "DeadlifeDust": "bụi hồi sinh xác",
}


def lookup_hash(table, value, prefix, tolerance=3):
    """shortHash -> (defName, khớp_chính_xác?).

    Khi hai def cùng loại trùng hash, game cộng dồn +1 cho def nạp sau, nên nếu
    không khớp chính xác thì thử các giá trị nhỏ hơn 1..tolerance."""
    if value in table:
        return table[value], True
    for delta in range(1, tolerance + 1):
        if value - delta in table:
            return table[value - delta], False
    return f"{prefix}#{value}", False


def inflate_b64(text):
    """base64 -> (raw deflate) -> bytes. Bản game cũ không nén thì trả nguyên."""
    if not text:
        return b""
    raw = base64.b64decode("".join(text.split()))
    try:
        return zlib.decompress(raw, -15)
    except zlib.error:
        return raw


def decode_ushort_grid(text, n):
    b = inflate_b64(text)
    if len(b) < n * 2:
        return None
    return struct.unpack(f"<{n}H", b[:n * 2])


def decode_bit_grid(text, n):
    """Mảng bool đóng gói 8 ô/byte, bit thấp trước."""
    b = inflate_b64(text)
    if len(b) * 8 < n:
        return None
    return bytearray((b[i >> 3] >> (i & 7)) & 1 for i in range(n))


def decode_float_series(text):
    """HistoryAutoRecorder.records: base64 của mảng float32 little-endian."""
    if not text or not text.strip():
        return []
    b = base64.b64decode("".join(text.split()))
    n = len(b) // 4
    return [round(v, 2) for v in struct.unpack(f"<{n}f", b[:n * 4])]


class MapGrids:
    """Các lớp dữ liệu theo ô của một map, giải mã từ phần nén trong save."""

    def __init__(self, el, size):
        self.w, self.h = size
        n = self.w * self.h
        self.n = n
        self.errors = []
        self.inexact = {}       # defName -> hash thực trong save (khớp gần đúng do va chạm hash)
        self.unknown = Counter()  # "Terrain#123" -> số ô

        def names(path, table, prefix):
            try:
                raw = decode_ushort_grid(el.findtext(path), n)
            except Exception as exc:  # dữ liệu hỏng -> bỏ qua lớp này
                self.errors.append(f"{path}: {exc}")
                return None
            if raw is None:
                return None
            cache = {0: None}
            out = [None] * n
            for i, v in enumerate(raw):
                nm = cache.get(v, False)
                if nm is False:
                    nm, exact = lookup_hash(table, v, prefix)
                    cache[v] = nm
                    if not exact and not nm.startswith(prefix + "#"):
                        self.inexact[nm] = v
                out[i] = nm
            for v, nm in cache.items():
                if nm and nm.startswith(prefix + "#"):
                    self.unknown[nm] = sum(1 for x in raw if x == v)
            return out

        self.terrain = names("terrainGrid/topGridDeflate", TERRAIN_HASH, "Terrain")
        self.under = names("terrainGrid/underGridDeflate", TERRAIN_HASH, "Terrain")
        self.foundation = names("terrainGrid/foundationGridDeflate", TERRAIN_HASH, "Terrain")
        self.roof = names("roofGrid/roofsDeflate", ROOF_HASH, "Roof")
        self.rock = names("compressedThingMapDeflate", COMPRESSED_HASH, "Thing")

        def bits(path):
            try:
                return decode_bit_grid(el.findtext(path), n)
            except Exception as exc:
                self.errors.append(f"{path}: {exc}")
                return None

        self.fog = bits("fogGrid/fogGridDeflate")
        self.pollution = bits("pollutionGrid/grid/arrDeflate")

        self.temp = None
        try:
            raw = decode_ushort_grid(el.findtext("temperatureCache/temperaturesDeflate"), n)
            if raw is not None:
                self.temp = [(v - 32768) / 16.0 for v in raw]
        except Exception as exc:
            self.errors.append(f"temperatureCache: {exc}")

        self.snow = None
        try:
            raw = decode_ushort_grid(el.findtext("snowGrid/depthGridDeflate"), n)
            if raw is not None and any(raw):
                self.snow = [v / 65535.0 for v in raw]
        except Exception as exc:
            self.errors.append(f"snowGrid: {exc}")

        self.gas = {}           # tên khí -> [chỉ số ô đang có khí]
        try:
            b = inflate_b64(el.findtext("gasGrid/gasDensityDeflate"))
            if len(b) >= n * 4 and any(b):
                for k, gname in enumerate(GAS_TYPES):
                    cells = [i for i in range(n) if b[i * 4 + k]]
                    if cells:
                        self.gas[gname] = cells
        except Exception as exc:
            self.errors.append(f"gasGrid: {exc}")

        self.deep = {}          # defName -> {"cells": [chỉ số ô], "count": tổng trữ lượng}
        try:
            dg = decode_ushort_grid(el.findtext("deepResourceGrid/defGridDeflate"), n)
            cg = decode_ushort_grid(el.findtext("deepResourceGrid/countGridDeflate"), n)
            if dg is not None and cg is not None and any(cg):
                for i in range(n):
                    if cg[i]:
                        nm, _exact = lookup_hash(DEEP_RESOURCE_HASH, dg[i], "Thing")
                        rec = self.deep.setdefault(nm, {"cells": [], "count": 0})
                        rec["cells"].append(i)
                        rec["count"] += cg[i]
        except Exception as exc:
            self.errors.append(f"deepResourceGrid: {exc}")

        self.areas = {}
        for a in el.findall("areaManager/areas/li"):
            key = a.findtext("label") or a.attrib.get("Class", "Area")
            try:
                self.areas[key] = decode_bit_grid(a.findtext("innerGrid/arrDeflate"), n)
            except Exception as exc:
                self.errors.append(f"area {key}: {exc}")

    # -- truy cập theo ô ----------------------------------------------
    def idx(self, x, z):
        return z * self.w + x

    def inside(self, x, z):
        return 0 <= x < self.w and 0 <= z < self.h

    def at(self, layer, x, z):
        g = getattr(self, layer, None)
        if g is None or not self.inside(x, z):
            return None
        return g[z * self.w + x]

    def fogged(self, x, z):
        return bool(self.fog[z * self.w + x]) if self.fog is not None and self.inside(x, z) else False

    def outdoor_temp(self):
        """Nhiệt độ ngoài trời = giá trị phổ biến nhất của lưới nhiệt (mọi ô ngoài trời dùng chung)."""
        if not self.temp:
            return None
        return Counter(self.temp).most_common(1)[0][0]


def is_rock_wall(name):
    """Tên def trong lớp 'đồ vật nén' có phải vách đá/quặng đặc (chắn đường) không."""
    if not name:
        return False
    return not name.startswith("Chunk")


def is_ore(name):
    return bool(name) and name.startswith("Mineable")


def terrain_kind(name):
    """Phân loại thô địa hình để vẽ bản đồ: water / mud / rock / floor / road / rich / soil / poor."""
    if not name:
        return "soil"
    if name.startswith("Water") or name == "Marsh":
        return "water"
    if name in ("Mud", "MarshyTerrain"):
        return "mud"
    if name.endswith(("_Rough", "_RoughHewn", "_Smooth")):
        return "rock"
    if name in ("BrokenAsphalt", "PackedDirt"):
        return "road"
    if name == "SoilRich":
        return "rich"
    if name in ("Soil", "MossyTerrain"):
        return "soil"
    if name in ("Gravel", "Sand", "SoftSand", "Ice", "ThinIce"):
        return "poor"
    return "floor"


# --------------------------------------------------------------------------
# Bộ phận cơ thể người (BodyDef "Human", thứ tự duyệt cây trước-sau = part index
# trong save). Đã đối chiếu với save: Crack chỉ rơi vào xương, LungRot ở 7/8,
# cấy ghép não ở 15, "right fourth toe" = 60, "left kidney" = 9…
# --------------------------------------------------------------------------

def _human_body_parts():
    parts = [
        ("Torso", "thân"), ("Ribcage", "lồng ngực"), ("Sternum", "xương ức"),
        ("Pelvis", "xương chậu"), ("Spine", "cột sống"), ("Stomach", "dạ dày"),
        ("Heart", "tim"), ("Lung", "phổi trái"), ("Lung", "phổi phải"),
        ("Kidney", "thận trái"), ("Kidney", "thận phải"), ("Liver", "gan"),
        ("Neck", "cổ"), ("Head", "đầu"), ("Skull", "hộp sọ"), ("Brain", "não"),
        ("Eye", "mắt trái"), ("Eye", "mắt phải"), ("Ear", "tai trái"), ("Ear", "tai phải"),
        ("Nose", "mũi"), ("Jaw", "hàm"), ("Tongue", "lưỡi"),
    ]
    for side in ("trái", "phải"):
        parts += [
            ("Shoulder", f"vai {side}"), ("Clavicle", f"xương đòn {side}"),
            ("Arm", f"tay {side}"), ("Humerus", f"xương cánh tay {side}"),
            ("Radius", f"xương cẳng tay {side}"), ("Hand", f"bàn tay {side}"),
            ("Finger", f"ngón út tay {side}"), ("Finger", f"ngón nhẫn tay {side}"),
            ("Finger", f"ngón giữa tay {side}"), ("Finger", f"ngón trỏ tay {side}"),
            ("Finger", f"ngón cái tay {side}"),
        ]
    parts.append(("Waist", "eo"))
    for side in ("trái", "phải"):
        parts += [
            ("Leg", f"chân {side}"), ("Femur", f"xương đùi {side}"),
            ("Tibia", f"xương chày {side}"), ("Foot", f"bàn chân {side}"),
            ("Toe", f"ngón út chân {side}"), ("Toe", f"ngón áp út chân {side}"),
            ("Toe", f"ngón giữa chân {side}"), ("Toe", f"ngón thứ hai chân {side}"),
            ("Toe", f"ngón cái chân {side}"),
        ]
    return parts


HUMAN_BODY_PARTS = _human_body_parts()   # 64 phần, index 0..63


def body_part_name(body, index):
    """Tên bộ phận từ (body, index) lưu trong hediff. Chỉ biết chắc với body 'Human'."""
    if index is None:
        return None
    if body == "Human" and 0 <= index < len(HUMAN_BODY_PARTS):
        d, vi = HUMAN_BODY_PARTS[index]
        return f"{vi} ({d})"
    return f"{body or '?'}#{index}"


# --------------------------------------------------------------------------
# Văn bản trong save có thẻ màu / thẻ ngữ pháp của game -> làm sạch để đọc.
# --------------------------------------------------------------------------

_TAG_RE = re.compile(r"</?(?:color|b|i|size)[^>]*>")
_GRAMMAR_RE = re.compile(r"\(\*[^)]*\)|\(/[^)]*\)")


def clean_text(s, limit=None):
    if not s:
        return ""
    s = _TAG_RE.sub("", s)
    s = _GRAMMAR_RE.sub("", s)
    s = re.sub(r"\s+", " ", s).strip()
    if limit and len(s) > limit:
        s = s[:limit - 1].rstrip() + "…"
    return s


# --------------------------------------------------------------------------
# Thời gian trong game (theo RimWorld.GenDate)
# --------------------------------------------------------------------------

SEASON_VI = {"Spring": "Xuân", "Summer": "Hè", "Fall": "Thu", "Winter": "Đông",
             "PermanentSummer": "Hè quanh năm", "PermanentWinter": "Đông quanh năm"}
_SEASONS_NORTH = ["Spring", "Summer", "Fall", "Winter"]    # Aprimay, Jugust, Septober, Decembary
_SEASONS_SOUTH = ["Fall", "Winter", "Spring", "Summer"]


def timezone_from_game_start(game_start_abs):
    """Game luôn bắt đầu lúc 06:00 giờ địa phương của ngày đầu một 'twelfth':
        gameStartAbsTick = 300000*twelfth + 2500*(6 + (24 - tz) % 24)
    -> suy ngược múi giờ (tz = round(kinh độ / 15)) của ô xuất phát."""
    rem = game_start_abs % TICKS_PER_TWELFTH
    if rem % TICKS_PER_HOUR:
        return None
    k = rem // TICKS_PER_HOUR - 6
    if not 0 <= k <= 23:
        return None
    tz = (24 - k) % 24
    return tz - 24 if tz > 12 else tz


def timezone_from_midnight_resets(game_start_abs, stamps):
    """Mỗi pawn lưu tick lần cuối reset 'XP trong ngày' — game làm việc đó đúng
    00h giờ địa phương (trễ < 1 giờ). Dùng để kiểm chứng múi giờ ở VỊ TRÍ HIỆN TẠI."""
    votes = Counter()
    for ts in stamps:
        if ts is None or ts < 0:
            continue
        x = (game_start_abs + ts) % TICKS_PER_DAY
        k = ((-x) % TICKS_PER_DAY) / TICKS_PER_HOUR
        tz = math.ceil(k - 1e-6) % 24
        votes[tz - 24 if tz > 12 else tz] += 1
    return votes.most_common(1)[0][0] if votes else None


def bearing(dx, dz):
    """Hướng la bàn 8 phía của vector (dx, dz); +x = Đông, +z = Bắc."""
    if dx == 0 and dz == 0:
        return "tại chỗ"
    ang = math.degrees(math.atan2(dx, dz)) % 360
    return ["Bắc", "Đông Bắc", "Đông", "Đông Nam", "Nam", "Tây Nam", "Tây", "Tây Bắc"][int((ang + 22.5) // 45) % 8]


def fmt_pos(pos):
    return f"({pos[0]},{pos[1]})" if pos else "—"


def fmt_bbox(bb):
    return f"x {bb[0]}–{bb[1]}, z {bb[2]}–{bb[3]}" if bb else "—"


def bbox_of(cells):
    cells = list(cells)
    if not cells:
        return None
    xs = [c[0] for c in cells]
    zs = [c[1] for c in cells]
    return [min(xs), max(xs), min(zs), max(zs)]


def ticks_to_days(t, nd=2):
    return None if t is None else round(t / TICKS_PER_DAY, nd)


def fmt_duration(ticks):
    """Khoảng thời gian game dễ đọc: '2.1 ngày' / '7.3 giờ'."""
    if ticks is None:
        return "—"
    a = abs(ticks)
    if a >= TICKS_PER_DAY:
        return f"{ticks / TICKS_PER_DAY:.1f} ngày"
    return f"{ticks / TICKS_PER_HOUR:.1f} giờ"


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
                "hidden": f.findtext("hidden") == "True",
                "temporary": f.findtext("temporary") == "True",
                "defeated": f.findtext("defeated") == "True",
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
            if (f["def"] or "").startswith("Player"):       # PlayerColony, PlayerTribe, …
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

        # múi giờ địa phương (giờ) — cần để đổi tick tuyệt đối sang ngày/giờ game
        self.tz_start = timezone_from_game_start(self.game_start_abs)
        self.tz_now = None
        self.tz = self.tz_start if self.tz_start is not None else 0
        self.tz_source = "start" if self.tz_start is not None else "none"
        self.season_saved = txt(self.game, "dateNotifier/lastSeason")

        self.things_by_id = {}
        self.world_pawns = []
        self.maps = []
        self._index()
        self.resolve_ideo_ids()
        self._resolve_timezone()

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
                            "gender": infer_gender(li),
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
        m = re.match(r"^Thing_(.+?)(\d+)$", ref)
        if m:        # vật không nằm rời trên map: đang được bê / nằm trong túi, trong vật chứa
            d = m.group(1)
            return f"{label(d, {**ITEMS, **BUILDINGS, **PLANTS})} `{d}` (đang được bê/giữ, không nằm rời trên map)"
        return ref

    def zone_of(self, pos, map_index=0):
        if pos is None:
            return None
        for md in self.maps:
            if md.index != map_index:
                continue
            return md.zone_lookup.get(pos)
        return None

    def relation_to_player(self, fid):
        """'Hostile' / 'Neutral' / 'Ally' / 'Player' / None (không phe)."""
        if not fid or fid == "null":
            return None
        if fid == self.player_faction:
            return "Player"
        f = self.factions.get(fid)
        if not f:
            return None
        for r in f["relations"]:
            if r["other"] == self.player_faction:
                return r["kind"]
        return "Neutral"

    # -- thời gian -----------------------------------------------------
    def _resolve_timezone(self):
        """Kiểm chứng múi giờ bằng tick 'reset XP lúc 00h' của các pawn đang ở trên map."""
        stamps = []
        for md in self.maps:
            for th in md.things:
                if th.attrib.get("Class") != "Pawn":
                    continue
                v = num(txt(th, "skills/lastXpSinceMidnightResetTimestamp"))
                if v is not None and 0 <= self.ticks_game - v < 2 * TICKS_PER_DAY:
                    stamps.append(v)
        self.tz_now = timezone_from_midnight_resets(self.game_start_abs, stamps)
        if self.tz_now is not None:
            self.tz = self.tz_now
            if self.tz_start is None:
                self.tz_source = "pawn"
            elif self.tz_start == self.tz_now:
                self.tz_source = "pawn+start"
            else:
                self.tz_source = "pawn (khác ô xuất phát: thuộc địa đã di chuyển?)"

    def date_at(self, game_tick):
        """Ngày/giờ địa phương tại một tick game — theo RimWorld.GenDate.

        tick tuyệt đối = gameStartAbsTick + ticksGame; giờ địa phương lệch tz*2500 tick."""
        local = self.game_start_abs + int(game_tick) + self.tz * TICKS_PER_HOUR
        doy = (local % TICKS_PER_YEAR) // TICKS_PER_DAY
        tod = local % TICKS_PER_DAY
        hour = tod / TICKS_PER_HOUR
        q = int(doy // DAYS_PER_QUADRUM)
        return {
            "year": int(self.starting_year + local // TICKS_PER_YEAR),
            "quadrum_index": q,
            "quadrum": QUADRUM_NAMES[q],
            "day_in_quadrum": int(doy % DAYS_PER_QUADRUM) + 1,
            "day_of_year": int(doy) + 1,
            "hour": round(hour, 2),
            "hour_int": int(hour),
            "minute": int((hour % 1) * 60),
            "tick_of_day": int(tod),
        }

    def fmt_tick(self, game_tick, time=True):
        """'15 Decembary 5500 03:45' cho một tick game."""
        if game_tick is None:
            return "—"
        d = self.date_at(game_tick)
        s = f"{d['day_in_quadrum']} {d['quadrum']} {d['year']}"
        if time:
            s += f" {d['hour_int']:02d}:{d['minute']:02d}"
        return s

    def date_info(self):
        d = self.date_at(self.ticks_game)
        days = self.ticks_game / TICKS_PER_DAY
        q = d["quadrum_index"]
        season = self.season_saved
        hemisphere = next_season = None
        if season in _SEASONS_NORTH:
            if _SEASONS_NORTH[q] == season:
                hemisphere, next_season = "Bắc", _SEASONS_NORTH[(q + 1) % 4]
            elif _SEASONS_SOUTH[q] == season:
                hemisphere, next_season = "Nam", _SEASONS_SOUTH[(q + 1) % 4]
        to_midnight = TICKS_PER_DAY - d["tick_of_day"]
        to_quadrum = (DAYS_PER_QUADRUM - d["day_in_quadrum"]) * TICKS_PER_DAY + to_midnight
        d.update({
            "days_played": round(days, 3),
            "timezone": self.tz,
            "tz_source": self.tz_source,
            "season": season,
            "hemisphere": hemisphere,
            "next_quadrum": QUADRUM_NAMES[(q + 1) % 4],
            "next_season": next_season,
            "ticks_to_midnight": int(to_midnight),
            "ticks_to_next_quadrum": int(to_quadrum),
            "display": f"ngày {d['day_in_quadrum']} {d['quadrum']} năm {d['year']}, {d['hour_int']:02d}:{d['minute']:02d}",
        })
        return d


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

        # thing theo ô (để tra nhanh: phòng, zone, sơ đồ)
        self.cell_things = defaultdict(list)
        for th in self.things:
            p = parse_pos(th.findtext("pos"))
            if p:
                self.cell_things[p].append(th)

        # các lưới nén (địa hình, mái, sương mù, đá/quặng, nhiệt độ)
        self.grids = None
        if self.size:
            try:
                self.grids = MapGrids(el, self.size)
            except Exception as exc:  # save lạ/hỏng: vẫn xuất được phần còn lại
                print(f"  ! không giải mã được lưới map {index}: {exc}", file=sys.stderr)

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

def extract_hediffs(p):
    """Mọi hediff (thương tích / bệnh / nghiện / cấy ghép) của một pawn, kèm tình trạng băng bó."""
    out = []
    hs = p.find("healthTracker/hediffSet")
    if hs is None:
        return out
    for h in hs.findall("hediffs/li"):
        part = h.find("part")
        body = txt(part, "body") if part is not None else None
        pidx = num(txt(part, "index")) if part is not None else None
        cls = h.attrib.get("Class") or "Hediff"
        hdef = h.findtext("def") or ""
        tend_left = num(h.findtext("tendTicksLeft"))
        tend_q = num(h.findtext("tendQuality"))
        permanent = h.findtext("isPermanent") == "True"
        fresh = h.findtext("isFresh") == "True"
        if tend_left is not None and tend_left > 0:
            tend = "tended"
        elif tend_left is not None:
            tend = "expired"          # đã từng chăm, nay hết hiệu lực -> cần chăm lại
        elif cls == "Hediff_Injury" and not permanent:
            tend = "untended"
        elif cls == "Hediff_MissingPart" and fresh:
            tend = "untended"
        else:
            tend = None
        sev = num(h.findtext("severity"))
        spd = num(h.findtext("severityPerDay"))
        out.append({
            "class": cls,
            "def": hdef,
            "name": label(hdef, HEDIFFS),
            "severity": sev,
            "part_body": body,
            "part_index": pidx,
            "part_name": body_part_name(body, pidx),
            "isPermanent": h.findtext("isPermanent"),
            "isFresh": h.findtext("isFresh"),
            "painCategory": h.findtext("painCategory"),
            "age_ticks": num(h.findtext("ageTicks")),
            "tickAdded": num(h.findtext("tickAdded")),
            "visible": h.findtext("visible"),
            "source": clean_text(h.findtext("sourceLabel")) or None,
            "sourceTool": clean_text(h.findtext("sourceToolLabel")) or None,
            "combatLog": clean_text(h.findtext("combatLogText")) or None,
            "tend": tend,
            "tendTicksLeft": tend_left,
            "tendQuality": tend_q,
            "severityPerDay": spd,
            "days_to_zero": (round(sev / -spd, 2) if sev is not None and spd is not None and spd < 0 else None),
            "ticksToDisappear": num(h.findtext("ticksToDisappear")),
            "lastInjury": h.findtext("lastInjury"),
            "level": num(h.findtext("level")),
        })
    return out


def job_target_pawn(save, ref):
    """Tên pawn nếu mục tiêu B của job là một pawn (vd. bệnh nhân của FeedPatient); ngược lại None."""
    el = save.ref_el(ref)
    if el is None or el.find("kindDef") is None:
        return None
    return other_pawn_label(save, ref)


def extract_job(save, p):
    cj = p.find("jobs/curJob")
    if cj is None or cj.attrib.get("IsNull") == "True" or cj.findtext("def") is None:
        return None
    drv = p.find("jobs/curDriver")
    return {
        "def": cj.findtext("def"),
        "targetA": cj.findtext("targetA"),
        "targetA_desc": save.describe_ref(cj.findtext("targetA")),
        "targetB": cj.findtext("targetB"),
        "targetB_desc": save.describe_ref(cj.findtext("targetB")),
        "targetB_pawn": job_target_pawn(save, cj.findtext("targetB")),
        "count": num(cj.findtext("count")),
        "workGiverDef": cj.findtext("workGiverDef"),
        "bill": cj.findtext("bill"),
        "lord": cj.findtext("lord"),
        "startTick": num(cj.findtext("startTick")),
        "playerForced": cj.findtext("playerForced"),
        "forceSleep": cj.findtext("forceSleep"),
        "driver": drv.attrib.get("Class") if drv is not None else None,
        "asleep": txt(drv, "asleep") == "True" if drv is not None else False,
        "posture": txt(p, "jobs/posture"),
        "lastJobTag": txt(p, "mindState/lastJobTag"),
        "queued": [j.findtext("job/def") or j.findtext("def") for j in p.findall("jobs/jobQueue/jobs/li")],
    }


def extract_mental(p):
    ms = p.find("mindState")
    cur = ms.find("mentalStateHandler/curState") if ms is not None else None
    state = None
    if cur is not None and cur.findtext("def"):
        state = {"def": cur.findtext("def"), "class": cur.attrib.get("Class")}
        for c in cur:
            if c.tag != "def" and not list(c) and (c.text or "").strip() not in ("", "null"):
                state[c.tag] = num(c.text, c.text.strip())
    breaker = {}
    for k in ("ticksBelowExtreme", "ticksBelowMajor", "ticksBelowMinor", "ticksUntilCanDoMentalBreak"):
        v = num(txt(ms, f"mentalBreaker/{k}"))
        if v is not None:
            breaker[k] = v
    return state, breaker


def extract_pawn(save: SaveFile, p, mapdata=None, full_fields=False):
    cls = p.attrib.get("Class")
    faction = p.findtext("faction")
    d = {
        "id": p.findtext("id"),
        "def": p.findtext("def"),
        "class": cls,
        "kindDef": p.findtext("kindDef"),
        "faction": faction,
        "faction_name": save.faction_name(faction),
        "faction_relation": save.relation_to_player(faction),
        "name": name_of_pawn_el(p),
        "nick": pawn_nick(p),
        "gender": infer_gender(p),
        "gender_inferred": False,
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
    d["beard"] = txt(p, "style/beardDef") or txt(st, "beardDef")
    d["tattoo_face"] = txt(p, "style/faceTattoo") or txt(st, "faceTattoo")
    d["tattoo_body"] = txt(p, "style/bodyTattoo") or txt(st, "bodyTattoo")
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

    # nhu cầu + suy nghĩ (save chỉ lưu thought dạng KÝ ỨC; thought tình huống do game tính lúc chạy)
    d["needs"] = []
    d["mood"] = None
    d["thoughts"] = []
    for nd in p.findall("needs/needs/li"):
        defn = nd.findtext("def")
        d["needs"].append({
            "def": defn,
            "name": label(defn, NEEDS),
            "class": nd.attrib.get("Class"),
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
                    "otherPawn_name": other_pawn_label(save, li.findtext("otherPawn")),
                    "opinionOffset": num(li.findtext("opinionOffset")),
                    "moodPowerFactor": num(li.findtext("moodPowerFactor")),
                    "food": li.findtext("foodThoughtDescription"),
                    "stage": li.findtext("stage"),
                    "sourcePrecept": li.findtext("sourcePrecept") if li.findtext("sourcePrecept") not in (None, "null") else None,
                })
    # tổng độ lệch thiện cảm từ ký ức xã hội, theo từng người
    opin = defaultdict(float)
    for t in d["thoughts"]:
        if t["opinionOffset"] is not None and t["otherPawn_name"]:
            opin[t["otherPawn_name"]] += t["opinionOffset"]
    d["opinion_from_memories"] = {k: round(v, 1) for k, v in opin.items()}

    # sức khỏe
    d["hediffs"] = extract_hediffs(p)
    hs = p.find("healthTracker/hediffSet")
    if hs is not None:
        d["hediffSet_other"] = flatten_el(hs, "hediffSet", skip=("hediffSet/hediffs",))
    d["healthState"] = txt(p, "healthTracker/healthState") or "Mobile"   # game chỉ ghi khi khác Mobile
    d["immunity"] = [
        {"def": im.findtext("hediffDef"), "immunity": num(im.findtext("immunity"))}
        for im in p.findall("healthTracker/immunity/imList/li")
    ]
    d["surgery_bills"] = [b.findtext("recipe") for b in p.findall("healthTracker/surgeryBills/bills/li")]

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
                "rotProg": num(li.findtext("rotProg")),
            })
        return out

    d["apparel"] = gear("apparel/wornApparel/innerList/li")
    d["equipment"] = gear("equipment/equipment/innerList/li")
    d["inventory"] = gear("inventory/innerContainer/innerList/li")
    d["carrying"] = gear("carryTracker/innerContainer/innerList/li")
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
    d["selfTend"] = txt(p, "playerSettings/selfTend")
    d["master"] = txt(p, "playerSettings/master")
    d["displayOrder"] = num(txt(p, "playerSettings/displayOrder"))
    d["joinTick"] = num(txt(p, "playerSettings/joinTick"))
    d["allowedAreas"] = [
        {"key": k.findtext("key"), "value": (k.findtext("value") or "")}
        for k in p.findall("playerSettings/allowedAreas/keys/li")
    ]
    d["outfit"] = txt(p, "outfits/curOutfit")
    d["drugPolicy"] = txt(p, "drugs/curAssignedDrugs")
    d["foodPolicy"] = txt(p, "foodRestriction/curRestriction")
    d["readingPolicy"] = txt(p, "reading/curAssignment")
    d["timetable"] = [(x.text or "").strip() for x in p.findall("timetable/times/li")]
    hour_now = save.date_at(save.ticks_game)["hour_int"]
    d["schedule_now"] = d["timetable"][hour_now] if len(d["timetable"]) == 24 else None
    d["drug_records"] = [
        {"drug": r.findtext("drug"), "lastTakenTicks": num(r.findtext("lastTakenTicks"))}
        for r in p.findall("drugs/drugTakeRecords/li")
    ]
    d["inventoryStock"] = [
        {"group": k.text, "thingDef": v.findtext("thingDef"), "count": num(v.findtext("count"), 0)}
        for k, v in zip(p.findall("inventoryStock/stockEntries/keys/li"),
                        p.findall("inventoryStock/stockEntries/values/li"))
    ]

    # thân phận: thuộc địa viên / khách / tù / nô lệ
    gs = p.find("guest")
    d["joinStatus"] = txt(gs, "joinStatus")
    d["guest"] = None
    if gs is not None and gs.attrib.get("IsNull") != "True":
        host = txt(gs, "hostFaction")
        d["guest"] = {
            "hostFaction": host if host not in (None, "null") else None,
            # game chỉ ghi guestStatus khi khác Guest; không có chủ nhà (hostFaction) thì không phải khách
            "guestStatus": txt(gs, "guestStatus") or ("Guest" if host not in (None, "null") else None),
            "slaveFaction": txt(gs, "slaveFaction") if txt(gs, "slaveFaction") not in (None, "null") else None,
            "interactionMode": txt(gs, "interactionMode"),
            "resistance": num(txt(gs, "resistance")),
            "will": num(txt(gs, "will")),
            "released": txt(gs, "released"),
            "timesTendedByPlayer": num(txt(p, "mindState/timesGuestTendedToByPlayer")),
        }
    player = save.player_faction
    host = (d["guest"] or {}).get("hostFaction")
    gstatus = (d["guest"] or {}).get("guestStatus")
    if faction == player and not host:
        d["role"] = "colonist"
    elif faction == player and gstatus == "Slave":
        d["role"] = "slave"
    elif host == player and gstatus == "Prisoner":
        d["role"] = "prisoner"
    elif host == player and gstatus == "Slave":
        d["role"] = "slave"
    elif host == player:
        d["role"] = "guest"
    elif d["faction_relation"] == "Hostile":
        d["role"] = "hostile"
    else:
        d["role"] = "other"

    # trạng thái hiện tại
    d["job"] = extract_job(save, p)
    d["drafted"] = txt(p, "drafter/drafted") == "True"
    state, breaker = extract_mental(p)
    d["mentalState"] = state["def"] if state else None
    d["mentalState_class"] = state["class"] if state else None
    d["mentalState_detail"] = state
    d["mentalBreaker"] = breaker
    ms = p.find("mindState")
    d["inspiration"] = txt(ms, "inspirationHandler/curState/def")
    d["ticksBelowMinor"] = breaker.get("ticksBelowMinor")
    d["duty"] = txt(ms, "duty/def")
    d["enemyTarget"] = txt(ms, "enemyTarget") if txt(ms, "enemyTarget") not in (None, "null") else None
    d["lastHarmTick"] = num(txt(ms, "lastHarmTick"))
    d["lastIngestTick"] = num(txt(ms, "lastIngestTick"))
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
    if d["ownedBed"] in ("null", ""):
        d["ownedBed"] = None
    bed_el = save.ref_el(d["ownedBed"])
    d["ownedBed_pos"] = parse_pos(bed_el.findtext("pos")) if bed_el is not None else None
    d["meditationSpot"] = txt(p, "ownership/assignedMeditationSpot")
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


def extract_creature(save: SaveFile, th):
    """Pawn không phải người: động vật, mechanoid, thực thể…"""
    d = th.findtext("def") or ""
    faction = th.findtext("faction")
    needs = {nd.findtext("def"): num(nd.findtext("curLevel")) for nd in th.findall("needs/needs/li")}
    state, _ = extract_mental(th)
    job = extract_job(save, th)
    hediffs = extract_hediffs(th)
    if d.startswith("Mech_") or (save.factions.get(faction) or {}).get("def") == "Mechanoid":
        kind = "mech"
    elif th.find("story") is not None and th.find("story").attrib.get("IsNull") != "True":
        kind = "humanlike"
    else:
        kind = "animal"
    return {
        "id": th.findtext("id"),
        "def": d,
        "kind": kind,
        "name": name_of_pawn_el(th),
        "gender": infer_gender(th),
        "age_bio": round((num(txt(th, "ageTracker/ageBiologicalTicks"), 0) or 0) / TICKS_PER_YEAR, 2),
        "faction": faction,
        "faction_name": save.faction_name(faction) if faction else "hoang dã",
        "faction_relation": save.relation_to_player(faction) if faction else None,
        "pos": parse_pos(th.findtext("pos")),
        "kindDef": th.findtext("kindDef"),
        "hunger": needs.get("Food"),
        "rest": needs.get("Rest"),
        "health": len(hediffs),
        "hediffs": hediffs,
        "healthState": txt(th, "healthTracker/healthState") or "Mobile",
        "job": job["def"] if job else None,
        "job_target": job["targetA"] if job else None,
        "asleep": job["asleep"] if job else False,
        "lord": job["lord"] if job else None,
        "duty": txt(th, "mindState/duty/def"),
        "mentalState": state["def"] if state else None,
        "enemyTarget": txt(th, "mindState/enemyTarget") if txt(th, "mindState/enemyTarget") not in (None, "null") else None,
        # CompCanBeDormant: có wakeUpSignalTag mà chưa từng có wokeUpTick => đang ngủ đông
        "dormant": th.find("wakeUpSignalTag") is not None and th.findtext("wokeUpTick") is None,
        "master": txt(th, "playerSettings/master") if txt(th, "playerSettings/master") not in (None, "null") else None,
        "spawnedTick": num(th.findtext("spawnedTick")),
    }


# Ngưỡng phân hủy của xác (ThingDef Corpse_* vanilla: daysToRotStart 2.5, daysToDessicated 5).
CORPSE_ROT_START_TICKS = 150_000
CORPSE_DESSICATED_TICKS = 300_000

# Số ngày (ở ≥10°C, không tủ lạnh) trước khi thực phẩm hỏng — theo def vanilla.
ROT_START_DAYS = {
    "MealSimple": 4, "MealFine": 4, "MealLavish": 4, "MealNutrientPaste": 0.75,
    "Pemmican": 70, "RawRice": 40, "RawPotatoes": 30, "RawCorn": 60, "RawBerries": 14,
}

# Dinh dưỡng mỗi đơn vị — theo def vanilla (người lớn tiêu ~1.6 dinh dưỡng/ngày).
NUTRITION = {
    "MealSimple": 0.9, "MealFine": 0.9, "MealLavish": 1.0, "MealSurvivalPack": 0.9,
    "MealNutrientPaste": 0.9, "Pemmican": 0.05, "RawRice": 0.05, "RawPotatoes": 0.05,
    "RawCorn": 0.05, "RawBerries": 0.05, "RawFungus": 0.05, "RawAgave": 0.05,
    "Milk": 0.05, "InsectJelly": 0.05, "Chocolate": 0.1, "Kibble": 0.05,
}
HUMAN_NUTRITION_PER_DAY = 1.6

# Công trình đặc (fillPercent = 1) chắn phòng như tường.
WALL_LIKE_DEFS = {"Wall", "Cooler", "Vent"}

_THING_SKIP_TAGS = {
    "def", "id", "map", "pos", "rot", "health", "stuff", "faction", "questTags",
    "spawnedTick", "despawnedTick", "tickDelta", "overrideGraphicIndex", "sourcePrecept",
    "everSeenByPlayer", "taleRef", "lastUser", "beenRevealed", "quality", "instigator",
    "approachingPawn", "lastFriendlyTouchTick", "startedGrowingAtTick", "stackCount",
}

# Loại designation -> loại công việc (WorkTypeDef) thực hiện nó.
DESIGNATION_WORK = {
    "Mine": "Mining", "MineVein": "Mining", "SmoothWall": "Construction",
    "SmoothFloor": "Construction", "RemoveFloor": "Construction",
    "Deconstruct": "Construction", "Uninstall": "Construction",
    "CutPlant": "PlantCutting", "HarvestPlant": "PlantCutting", "ExtractTree": "PlantCutting",
    "Hunt": "Hunting", "Tame": "Handling", "Slaughter": "Handling",
    "Haul": "Hauling", "Strip": "Hauling", "Flick": "BasicWorker", "Open": "BasicWorker",
}


def rot_days_left(defname, rot_prog):
    """Số ngày còn lại trước khi hỏng (None nếu không biết def hoặc không lưu rotProg)."""
    if rot_prog is None or not defname:
        return None
    days = None
    for key, v in ROT_START_DAYS.items():
        if defname == key or defname.startswith(key + "_"):
            days = v
            break
    if days is None and defname.startswith("Meat_"):
        days = 2
    if days is None:
        return None
    return round((days * TICKS_PER_DAY - rot_prog) / TICKS_PER_DAY, 2)


def nutrition_of(defname):
    if not defname:
        return None
    for key, v in NUTRITION.items():
        if defname == key or defname.startswith(key + "_"):
            return v
    if defname.startswith("Meat_"):
        return 0.05
    return None


def scalar_fields(th, skip=_THING_SKIP_TAGS):
    """Mọi trường con dạng giá trị đơn của một thing (nhiên liệu, công tắc, nhiệt độ đặt…)."""
    out = {}
    for c in th:
        if c.tag in skip or list(c):
            continue
        v = (c.text or "").strip()
        if v and v != "null":
            out[c.tag] = v
    return out


def describe_inner(save, li):
    """Mô tả 1 phần tử trong innerContainer (pawn trong kén, xác, vật phẩm…)."""
    if not list(li):
        ref = (li.text or "").strip()
        el = save.ref_el(ref)
        return {"ref": ref, "def": el.findtext("def") if el is not None else None,
                "name": name_of_pawn_el(el) if el is not None else None}
    rec = {
        "class": li.attrib.get("Class"),
        "def": li.findtext("def"),
        "id": li.findtext("id"),
        "stackCount": num(li.findtext("stackCount"), 1),
    }
    if li.attrib.get("Class") == "Pawn":
        rec.update({
            "name": name_of_pawn_el(li),
            "kindDef": li.findtext("kindDef"),
            "faction": li.findtext("faction"),
            "faction_name": save.faction_name(li.findtext("faction")),
            "faction_relation": save.relation_to_player(li.findtext("faction")),
            "gender": infer_gender(li),
            "age_bio": round((num(txt(li, "ageTracker/ageBiologicalTicks"), 0) or 0) / TICKS_PER_YEAR, 1),
            "equipment": [e.findtext("def") for e in li.findall("equipment/equipment/innerList/li")],
            "apparel": [e.findtext("def") for e in li.findall("apparel/wornApparel/innerList/li")],
        })
    elif li.attrib.get("Class") == "Corpse":
        inner = li.find("innerContainer/innerList/li")
        ref = (inner.text or "").strip() if inner is not None else None
        el = save.ref_el(ref)
        rec["corpse_of"] = ref
        rec["name"] = name_of_pawn_el(el) if el is not None else None
    return rec


def fmt_inner(inner):
    """Chuỗi mô tả nội dung một innerContainer, gộp các mục giống nhau."""
    parts = Counter()
    for x in inner:
        s = x.get("def") or x.get("ref") or "?"
        if x.get("class") == "Corpse":
            s = f"xác {x.get('name') or s}"
        elif x.get("name"):
            s += f" «{x['name']}»"
        if x.get("kindDef"):
            if x.get("faction"):
                s += f" [{x['kindDef']}, {x.get('age_bio')} tuổi, phe {x['faction_name']}, quan hệ {x['faction_relation']}"
                if x.get("equipment"):
                    s += f", vũ khí {'/'.join(x['equipment'])}"
                s += "]"
            else:
                s += " [không phe]"
        elif (x.get("stackCount") or 1) > 1:
            s += f" ×{x['stackCount']}"
        parts[s] += 1
    return "; ".join(k + (f" ×{v}" if v > 1 else "") for k, v in parts.items())


def extract_bills(th):
    bills = []
    for b in th.findall("billStack/bills/li"):
        bills.append({
            "recipe": b.findtext("recipe"),
            "repeatMode": b.findtext("repeatMode") or "RepeatCount",
            "repeatCount": num(b.findtext("repeatCount"), 1),
            "targetCount": num(b.findtext("targetCount")),
            "unpauseWhenYouHave": num(b.findtext("unpauseWhenYouHave")),
            "paused": b.findtext("paused"),
            "suspended": b.findtext("suspended"),
            "storeMode": b.findtext("storeMode"),
            "ingredientSearchRadius": num(b.findtext("ingredientSearchRadius")),
            "allowedSkillRange": b.findtext("allowedSkillRange"),
            "pawnRestriction": b.findtext("pawnRestriction") if b.findtext("pawnRestriction") not in (None, "null") else None,
        })
    return bills


def fmt_bill(b):
    mode = b.get("repeatMode")
    if mode == "Forever":
        s = f"{b['recipe']} (lặp mãi)"
    elif mode == "TargetCount":
        s = f"{b['recipe']} (làm đến khi có {fmt_num(b.get('targetCount'))})"
    else:
        s = f"{b['recipe']} ×{fmt_num(b.get('repeatCount'))}"
    if b.get("suspended") == "True":
        s += " [TẠM DỪNG]"
    if b.get("pawnRestriction"):
        s += f" [chỉ {b['pawnRestriction']}]"
    return s


def extract_map(save: SaveFile, md: MapData, full_fields=False):
    out = {
        "index": md.index,
        "size": md.size,
        "weather": txt(md.el, "weatherManager/curWeather"),
        "weather_age": num(txt(md.el, "weatherManager/curWeatherAge")),
        "weather_last": txt(md.el, "weatherManager/lastWeather"),
        "conditions": [
            {"def": c.findtext("def"), "class": c.attrib.get("Class"),
             "duration": num(c.findtext("duration")), "permanent": c.findtext("permanent"),
             "startTick": num(c.findtext("startTick"))}
            for c in md.el.findall("gameConditionManager/activeConditions/li")
        ],
        "designations": [],
        "buildings_player": [],
        "buildings_other": [],
        "construction": [],
        "mineables": [],
        "items": [],
        "plants_sown": [],
        "plants_wild": Counter(),
        "plants_wild_growth": defaultdict(list),
        "dead_plants": Counter(),
        "corpses": [],
        "pawns": [],
        "animals": [],
        "mechs": [],
        "filth": Counter(),
        "chunks": Counter(),
        "zones": [],
        "areas": [],
        "unclassified": [],
        "pawns_offmap": [],
        "class_counts": Counter(),
    }

    player = save.player_faction
    g = md.grids

    # -- story state của map ----------------------------------------------
    ss = md.el.find("storyState")
    out["story"] = {
        "lastThreatBigTick": num(txt(ss, "lastThreatBigTick")),
        "lastRaidFaction": txt(ss, "lastRaidFaction"),
        "lastRaidFaction_name": save.faction_name(txt(ss, "lastRaidFaction")),
        "lastIncidents": sorted(
            ({"incident": k.text, "tick": num(v.text)}
             for k, v in zip(ss.findall("lastFireTicks/keys/li"), ss.findall("lastFireTicks/values/li"))),
            key=lambda r: r["tick"] or 0) if ss is not None else [],
    }
    out["roads_edge_cells"] = [parse_pos(x.text) for x in md.el.findall("components/li/roadEdgeTiles/li")]
    out["water_bodies"] = [
        {"rootCell": parse_pos(wb.findtext("rootCell")), "cells": num(wb.findtext("cellCount")),
         "fishType": wb.findtext("fishType"), "population": num(wb.findtext("population")),
         "shouldHaveFish": wb.findtext("shouldHaveFish") == "True",
         "commonFish": [x.text for x in wb.findall("commonFish/li")],
         "uncommonFish": [x.text for x in wb.findall("uncommonFish/li")]}
        for wb in md.el.findall("waterBodyTracker/waterBodies/li")
    ]

    # -- areas ---------------------------------------------------------------
    for a in md.el.findall("areaManager/areas/li"):
        key = a.findtext("label") or a.attrib.get("Class", "Area")
        grid = g.areas.get(key) if g is not None else None
        cells = [(i % g.w, i // g.w) for i, v in enumerate(grid) if v] if grid is not None else []
        out["areas"].append({
            "class": a.attrib.get("Class"),
            "id": a.findtext("ID"),
            "label": a.findtext("label"),
            "trueCount": num(txt(a, "innerGrid/trueCount"), 0) or len(cells),
            "bbox": bbox_of(cells),
        })

    # -- designations --------------------------------------------------------
    for li in md.el.findall("designationManager/allDesignations/li"):
        target = li.findtext("target")
        el = md.by_id.get(target) or save.things_by_id.get(target)
        pos = parse_pos(el.findtext("pos")) if el is not None else parse_pos(target)
        tdef = el.findtext("def") if el is not None else None
        if tdef is None and pos and g is not None and g.rock is not None and g.inside(*pos):
            tdef = g.rock[g.idx(*pos)]          # designation trên ô (Mine/MineVein…): xem ô đó là đá/quặng gì
            if tdef is None:
                for th in md.cell_things.get(pos, []):
                    if th.attrib.get("Class") == "Mineable":
                        tdef = th.findtext("def")
        out["designations"].append({
            "def": li.findtext("def"),
            "target": target,
            "target_def": tdef,
            "target_pos": pos,
        })

    # -- things --------------------------------------------------------------
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
                "id": th.findtext("id"), "zone": md.zone_name_at(pos),
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
            rot_prog = num(th.findtext("rotProg"))
            if rot_prog is None:
                stage = "NoRot"                 # xác mech… không phân hủy
            elif rot_prog < CORPSE_ROT_START_TICKS:
                stage = "Fresh"
            elif rot_prog < CORPSE_DESSICATED_TICKS:
                stage = "Rotting"
            else:
                stage = "Dessicated"
            out["corpses"].append({
                "def": d,
                "id": th.findtext("id"),
                "pos": pos,
                "inner": inner_id,
                "inner_def": target.findtext("def") if target is not None else None,
                "inner_name": (name_of_pawn_el(target) if target is not None else (wp or {}).get("name"))
                              or (target.findtext("def") if target is not None else None),
                "inner_faction": save.faction_name(target.findtext("faction")) if target is not None and target.findtext("faction") else None,
                "zone": md.zone_name_at(pos),
                "rotProg": rot_prog,
                "rot_stage": stage,
                "ticks_to_rot": (CORPSE_ROT_START_TICKS - rot_prog) if stage == "Fresh" else None,
                "timeOfDeath": num(th.findtext("timeOfDeath")),
                "forbidden": th.findtext("forbidden") == "True",
                "fogged": g.fogged(*pos) if g is not None and pos else False,
            })
            continue

        if cls == "Pawn":
            story = th.find("story")
            humanlike = d == "Human" or (story is not None and story.attrib.get("IsNull") != "True")
            if humanlike:
                pmap = th.findtext("map")
                if pmap is not None and pmap not in (str(md.index), ""):
                    out.setdefault("pawns_offmap", []).append(extract_pawn(save, th, md, full_fields))
                    continue
                out["pawns"].append(extract_pawn(save, th, md, full_fields))
            else:
                rec = extract_creature(save, th)
                rec["fogged"] = g.fogged(*pos) if g is not None and pos else False
                out["mechs" if rec["kind"] == "mech" else "animals"].append(rec)
            continue

        if cls.startswith("Blueprint") or cls == "Frame" or d.startswith(("Blueprint_", "Frame_")):
            contents = [
                {"def": li.findtext("def"), "stackCount": num(li.findtext("stackCount"), 1)}
                for li in th.findall("resourceContainer/innerList/li")
            ]
            out["construction"].append({
                "kind": "frame" if (cls == "Frame" or d.startswith("Frame_")) else "blueprint",
                "class": cls,
                "def": d,
                "build_def": d.split("_", 1)[1] if "_" in d else d,
                "id": th.findtext("id"),
                "pos": pos,
                "rot": th.findtext("rot"),
                "stuff": th.findtext("stuff") or th.findtext("stuffToUse"),
                "faction": faction,
                "spawnedTick": num(th.findtext("spawnedTick")),
                "workDone": num(th.findtext("workDone")),
                "contents": contents,
            })
            continue

        if cls == "Mineable":
            out["mineables"].append({
                "def": d, "id": th.findtext("id"), "pos": pos,
                "health": num(th.findtext("health")),
                "yieldPct": num(th.findtext("yieldPct")),
            })
            continue

        if cls.startswith("Building") or d in BUILDINGS:
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
                "rot": th.findtext("rot"),              # hướng xoay 0..3 (Bắc, Đông, Nam, Tây)
                "spawnedTick": num(th.findtext("spawnedTick")),
                "fogged": g.fogged(*pos) if g is not None and pos else False,
                "extra": scalar_fields(th),
            }
            bills = extract_bills(th)
            if bills:
                rec["extra"]["bills"] = bills
            owners = [(x.text or "").strip() for x in th.findall("assignedPawns/li")]
            if th.find("assignedPawns") is not None:
                rec["extra"]["assignedPawns"] = [
                    {"ref": o, "name": pawn_nick(save.ref_el(o)) or o} for o in owners]
            res = th.find("resourceContainer")
            if res is not None:
                cont = []
                for li in res.findall("innerList/li"):
                    cont.append({"def": li.findtext("def"), "stackCount": num(li.findtext("stackCount"), 1)})
                if cont:
                    rec["extra"]["contents"] = cont
            inner = [describe_inner(save, li) for li in th.findall("innerContainer/innerList/li")]
            if inner:
                rec["extra"]["inner"] = inner
            if faction == player:
                out["buildings_player"].append(rec)
            else:
                out["buildings_other"].append(rec)
            continue

        if "Chunk" in d and th.find("stackCount") is None:
            out["chunks"][d] += 1
            continue

        # vật phẩm rời (mọi lớp còn lại có stackCount, hoặc các lớp vật phẩm đã biết)
        if (th.find("stackCount") is not None
                or cls in ("ThingWithComps", "Medicine", "Apparel", "Thing", "Book",
                           "MinifiedThing", "UnfinishedThing", "Genepack", "Xenogerm")):
            count = num(th.findtext("stackCount"), 1) or 1
            rot_prog = num(th.findtext("rotProg"))
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
                "rotProg": rot_prog,
                "rot_days_left": rot_days_left(d, rot_prog),
                "inner_def": txt(th, "innerContainer/innerList/li/def"),
                "fogged": g.fogged(*pos) if g is not None and pos else False,
            })
            continue

        out["unclassified"].append({
            "class": cls, "def": d, "id": th.findtext("id"), "pos": pos,
        })

    # -- zones (cần danh sách thing theo ô) --------------------------------
    for z in md.zones:
        cells = z["cells"]
        rec = {
            "label": z["label"],
            "type": z["type"],
            "class": z["class"],
            "id": z["id"],
            "plantDefToGrow": z["plantDefToGrow"],
            "allowSow": z["el"].findtext("allowSow") != "False",
            "allowCut": z["el"].findtext("allowCut") != "False",
            "cell_count": len(cells),
            "bbox": bbox_of(cells),
            "cells": cells,
            "settings": z["settings"],
        }
        if "Growing" in z["class"]:
            crop, other = [], Counter()
            for c in cells:
                for th in md.cell_things.get(c, []):
                    if th.attrib.get("Class") != "Plant":
                        continue
                    if th.findtext("def") == z["plantDefToGrow"]:
                        crop.append(num(th.findtext("growth"), 0) or 0)
                    else:
                        other[th.findtext("def")] += 1
            rec["crop_count"] = len(crop)
            rec["crop_growth_avg"] = round(sum(crop) / len(crop), 3) if crop else None
            rec["crop_growth_min"] = round(min(crop), 3) if crop else None
            rec["crop_growth_max"] = round(max(crop), 3) if crop else None
            rec["crop_mature"] = sum(1 for x in crop if x >= 0.999)
            rec["other_plants"] = dict(other)
            if g is not None and g.terrain is not None:
                rec["soil"] = dict(Counter(g.terrain[g.idx(*c)] for c in cells if g.inside(*c)))
        else:
            occupied = 0
            for c in cells:
                if any(th.attrib.get("Class") not in ("Filth", "Plant", "Pawn") for th in md.cell_things.get(c, [])):
                    occupied += 1
            rec["occupied_cells"] = occupied
            if g is not None and g.roof is not None:
                rec["roofed_cells"] = sum(1 for c in cells if g.inside(*c) and g.roof[g.idx(*c)])
        out["zones"].append(rec)

    # -- tổng hợp ------------------------------------------------------------
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

    # -- tâm căn cứ + khoảng cách ------------------------------------------
    structural = [b["pos"] for b in out["buildings_player"]
                  if b["pos"] and (b["def"] in WALL_LIKE_DEFS or "Door" in b["class"])]
    anchor = structural or [b["pos"] for b in out["buildings_player"] if b["pos"]] \
        or [p["pos"] for p in out["pawns"] if p["pos"] and p["faction"] == player]
    if anchor:
        cx = round(sum(p[0] for p in anchor) / len(anchor))
        cz = round(sum(p[1] for p in anchor) / len(anchor))
        out["base_center"] = (cx, cz)
        out["base_bbox"] = bbox_of(anchor)
    else:
        out["base_center"] = None
        out["base_bbox"] = None

    out["lords"] = extract_lords(save, md)
    out["grids"] = summarize_grids(md, out)
    out["ores"] = find_ore_clusters(md, out)
    out["rooms"] = detect_rooms(save, md, out)
    out["food"] = summarize_food(out)
    return out


def rel_to_base(mp, pos):
    """(khoảng cách ô, hướng) từ tâm căn cứ tới pos."""
    bc = mp.get("base_center")
    if not bc or not pos:
        return None, None
    dx, dz = pos[0] - bc[0], pos[1] - bc[1]
    return round(math.hypot(dx, dz)), bearing(dx, dz)


def fmt_rel(mp, pos):
    dist, direction = rel_to_base(mp, pos)
    if dist is None:
        return "—"
    return f"{dist} ô {direction}" if dist else "tại tâm căn cứ"


def extract_lords(save, md):
    """Lord = nhóm pawn do AI điều khiển chung (đột kích, khách, cụm mech ngủ đông…)."""
    out = []
    for li in md.el.findall("lordManager/lords/li"):
        job = li.find("lordJob")
        pawns = []
        for ref in li.findall("ownedPawns/li"):
            el = save.ref_el((ref.text or "").strip())
            pawns.append({
                "ref": (ref.text or "").strip(),
                "def": el.findtext("def") if el is not None else None,
                "name": name_of_pawn_el(el) if el is not None else None,
                "pos": parse_pos(el.findtext("pos")) if el is not None else None,
            })
        fid = li.findtext("faction")
        out.append({
            "id": f"Lord_{li.findtext('loadID') or 0}",
            "faction": fid,
            "faction_name": save.faction_name(fid),
            "faction_relation": save.relation_to_player(fid),
            "job_class": job.attrib.get("Class") if job is not None else None,
            "job_fields": {c.tag: (c.text or "").strip() for c in job
                           if not list(c) and (c.text or "").strip()} if job is not None else {},
            "pawns": pawns,
            "buildings": [(x.text or "").strip() for x in li.findall("ownedBuildings/li")],
            "curLordToilIdx": num(li.findtext("curLordToilIdx")),
            "ticksInToil": num(li.findtext("ticksInToil")),
            "questTags": [x.text for x in li.findall("questTags/li")],
        })
    return out


def gas_line(gs):
    gas = (gs or {}).get("gas") or {}
    if not gas:
        return "không có (lưới khí toàn 0)"
    return "; ".join(f"`{k}` ({GAS_VI.get(k, k)}) phủ {v['cells']} ô trong {fmt_bbox(v['bbox'])}" for k, v in gas.items())


def deep_line(gs):
    deep = (gs or {}).get("deep_resources") or {}
    if not deep:
        return "chưa có (chưa quét bằng máy quét sâu, hoặc không có gì)"
    return "; ".join(f"`{k}` {v['count']:,} đơn vị trên {v['cells']} ô trong {fmt_bbox(v['bbox'])}" for k, v in deep.items())


def summarize_grids(md, mp):
    """Thống kê địa hình / mái / sương mù / đá từ các lưới đã giải mã."""
    g = md.grids
    if g is None:
        return None
    out = {
        "terrain": dict(Counter(g.terrain).most_common()) if g.terrain else {},
        "roof": dict(Counter(x for x in g.roof if x).most_common()) if g.roof else {},
        "rock": dict(Counter(x for x in g.rock if x).most_common()) if g.rock else {},
        "fogged_cells": sum(g.fog) if g.fog is not None else None,
        "polluted_cells": sum(g.pollution) if g.pollution is not None else None,
        "snow": g.snow is not None,
        "gas": {
            name: {"cells": len(cells), "bbox": bbox_of([(i % g.w, i // g.w) for i in cells])}
            for name, cells in g.gas.items()
        },
        "deep_resources": {
            name: {"cells": len(rec["cells"]), "count": rec["count"],
                   "bbox": bbox_of([(i % g.w, i // g.w) for i in rec["cells"]])}
            for name, rec in g.deep.items()
        },
        "outdoor_temp": round(g.outdoor_temp(), 1) if g.temp else None,
        "hash_inexact": dict(g.inexact),
        "hash_unknown": dict(g.unknown),
        "errors": list(g.errors),
    }
    return out


def find_ore_clusters(md, mp):
    """Gom các ô quặng liền nhau (8 hướng) thành mạch; gồm cả quặng nén lẫn quặng đã bị đào dở."""
    g = md.grids
    cells = defaultdict(set)
    if g is not None and g.rock is not None:
        for i, nm in enumerate(g.rock):
            if is_ore(nm):
                cells[nm].add((i % g.w, i // g.w))
    for m in mp["mineables"]:
        if is_ore(m["def"]) and m["pos"]:
            cells[m["def"]].add(m["pos"])
    designated = {d["target_pos"] for d in mp["designations"] if d["def"] in ("Mine", "MineVein")}
    clusters = []
    for nm, cs in cells.items():
        left = set(cs)
        while left:
            start = left.pop()
            comp, stack = [start], [start]
            while stack:
                x, z = stack.pop()
                for dx in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        nb = (x + dx, z + dz)
                        if nb in left:
                            left.discard(nb)
                            comp.append(nb)
                            stack.append(nb)
            center = (round(sum(c[0] for c in comp) / len(comp)), round(sum(c[1] for c in comp) / len(comp)))
            dist, direction = rel_to_base(mp, center)
            clusters.append({
                "def": nm,
                "cells": len(comp),
                "bbox": bbox_of(comp),
                "center": center,
                "fogged_cells": sum(1 for c in comp if g is not None and g.fogged(*c)),
                "designated_cells": sum(1 for c in comp if c in designated),
                "dist": dist,
                "bearing": direction,
                "hash_exact": not (g is not None and nm in g.inexact),
            })
    clusters.sort(key=lambda c: (c["dist"] if c["dist"] is not None else 1e9, -c["cells"]))
    return clusters


def detect_rooms(save, md, mp):
    """Tìm các vùng kín (bị tường/đá/cửa bao quanh) trên toàn map bằng loang.

    Game không lưu danh sách phòng (tự dựng lại khi nạp save) nên phải tính lại.
    Vùng lớn nhất chạm mép map coi là 'ngoài trời' và bị bỏ qua."""
    g = md.grids
    if g is None or g.rock is None:
        return []
    w, h = g.w, g.h
    blocked = bytearray(w * h)       # 1 = tường/đá, 2 = cửa
    door_cells = []
    for i, nm in enumerate(g.rock):
        if is_rock_wall(nm):
            blocked[i] = 1
    for th in md.things:
        cls = th.attrib.get("Class", "")
        pos = parse_pos(th.findtext("pos"))
        if not pos or not g.inside(*pos):
            continue
        d = th.findtext("def") or ""
        if "Door" in cls:
            blocked[g.idx(*pos)] = 2
            door_cells.append(pos)
        elif cls == "Mineable" or d in WALL_LIKE_DEFS or d.startswith("Smoothed"):
            if cls.startswith(("Blueprint", "Frame")) or d.startswith(("Blueprint_", "Frame_")):
                continue
            blocked[g.idx(*pos)] = 1

    region = [-1] * (w * h)
    regions = []
    for start in range(w * h):
        if blocked[start] or region[start] != -1:
            continue
        rid = len(regions)
        region[start] = rid
        stack = [start]
        cells = []
        edge = False
        while stack:
            i = stack.pop()
            cells.append(i)
            x, z = i % w, i // w
            if x == 0 or z == 0 or x == w - 1 or z == h - 1:
                edge = True
            for j in (i - 1 if x > 0 else -1, i + 1 if x < w - 1 else -1,
                      i - w if z > 0 else -1, i + w if z < h - 1 else -1):
                if j >= 0 and not blocked[j] and region[j] == -1:
                    region[j] = rid
                    stack.append(j)
        regions.append({"cells": cells, "edge": edge})

    home = g.areas.get("Area_Home")
    player = save.player_faction
    by_cell_building = defaultdict(list)
    for b in mp["buildings_player"] + mp["buildings_other"]:
        if b["pos"]:
            by_cell_building[b["pos"]].append(b)
    zone_at = md.zone_lookup
    pawn_at = defaultdict(list)
    for p in mp["pawns"]:
        if p["pos"]:
            pawn_at[p["pos"]].append(p["nick"] or p["name"] or p["id"])
    for a in mp["animals"] + mp["mechs"]:
        if a["pos"]:
            pawn_at[a["pos"]].append(a["def"])
    item_at = defaultdict(list)
    for it in mp["items"]:
        if it["pos"]:
            item_at[it["pos"]].append(it)
    corpse_at = defaultdict(list)
    for c in mp["corpses"]:
        if c["pos"]:
            corpse_at[c["pos"]].append(c)
    cons_at = defaultdict(list)
    for c in mp["construction"]:
        if c["pos"]:
            cons_at[c["pos"]].append(c)
    filth_cells = Counter()
    for th in md.things:
        if th.attrib.get("Class") == "Filth":
            pos = parse_pos(th.findtext("pos"))
            if pos:
                filth_cells[pos] += 1

    doors_of = defaultdict(list)
    for (x, z) in door_cells:
        for nb in ((x - 1, z), (x + 1, z), (x, z - 1), (x, z + 1)):
            if g.inside(*nb):
                rid = region[g.idx(*nb)]
                if rid >= 0:
                    doors_of[rid].append((x, z))

    rooms = []
    for rid, reg in enumerate(regions):
        if reg["edge"]:
            continue
        cells = [(i % w, i // w) for i in reg["cells"]]
        rec = {
            "cells": len(cells),
            "bbox": bbox_of(cells),
            "roofed": sum(1 for i in reg["cells"] if g.roof and g.roof[i]),
            "roof_types": dict(Counter(g.roof[i] for i in reg["cells"] if g.roof and g.roof[i])),
            "temperature": round(g.temp[reg["cells"][0]], 1) if g.temp else None,
            "floors": dict(Counter(g.terrain[i] for i in reg["cells"]).most_common()) if g.terrain else {},
            "fogged": sum(1 for i in reg["cells"] if g.fog is not None and g.fog[i]),
            "home_cells": sum(1 for i in reg["cells"] if home is not None and home[i]),
            "doors": sorted(set(doors_of.get(rid, []))),
            "player_buildings": Counter(),
            "other_buildings": Counter(),
            "beds": [],
            "details": [],
            "items": Counter(),
            "corpses": Counter(),
            "pawns": [],
            "zones": Counter(),
            "construction": Counter(),
            "filth": 0,
        }
        for c in cells:
            for b in by_cell_building.get(c, []):
                key = "player_buildings" if b["faction"] == player else "other_buildings"
                rec[key][b["def"]] += 1
                ex = b["extra"]
                if "Bed" in b["class"]:
                    rec["beds"].append({
                        "id": b["id"], "pos": b["pos"],
                        "owners": [o["name"] for o in ex.get("assignedPawns", [])],
                        "medical": ex.get("medical") == "True",
                        "forPrisoners": ex.get("forPrisoners") == "True",
                    })
                if ex.get("inner"):
                    rec["details"].append(f"{b['def']}@{fmt_pos(b['pos'])} chứa " + fmt_inner(ex["inner"]))
            for it in item_at.get(c, []):
                rec["items"][it["def"]] += it["stackCount"]
            for cp in corpse_at.get(c, []):
                rec["corpses"][f"{cp['def']} ({ROT_STAGE_VI.get(cp['rot_stage'], cp['rot_stage'])})"] += 1
            for cn in cons_at.get(c, []):
                rec["construction"][cn["def"]] += 1
            rec["pawns"].extend(pawn_at.get(c, []))
            rec["filth"] += filth_cells.get(c, 0)
            z = zone_at.get(c)
            if z:
                rec["zones"][z["label"]] += 1
        for k in ("player_buildings", "other_buildings", "items", "corpses", "zones", "construction"):
            rec[k] = dict(rec[k])
        rec["is_base"] = bool(rec["player_buildings"] or rec["home_cells"] or rec["zones"])
        interesting = (rec["is_base"] or rec["other_buildings"] or rec["items"] or rec["corpses"]
                       or rec["pawns"] or rec["doors"])
        if not interesting:
            continue
        if not rec["is_base"] and rec["cells"] < 4 and not rec["pawns"] and not rec["other_buildings"]:
            continue        # hốc đá 1-3 ô (ô vừa đào dở…) — bỏ cho đỡ nhiễu
        rec["dist"], rec["bearing"] = rel_to_base(mp, ((rec["bbox"][0] + rec["bbox"][1]) // 2,
                                                      (rec["bbox"][2] + rec["bbox"][3]) // 2))
        rooms.append(rec)
    rooms.sort(key=lambda r: (not r["is_base"], r["dist"] if r["dist"] is not None else 0, r["bbox"]))
    for i, r in enumerate(rooms, 1):
        r["id"] = f"R{i}"
    return rooms


def summarize_food(mp):
    """Tổng hợp thực phẩm cho người (theo bảng dinh dưỡng vanilla)."""
    rows = []
    total = 0.0
    meals = 0
    raw_units = 0
    by_def = defaultdict(lambda: {"count": 0, "min_days_left": None})
    for it in mp["items"]:
        nut = nutrition_of(it["def"])
        if nut is None or it.get("fogged") or it.get("forbidden") == "True":
            continue
        rec = by_def[it["def"]]
        rec["count"] += it["stackCount"]
        dl = it.get("rot_days_left")
        if dl is not None and (rec["min_days_left"] is None or dl < rec["min_days_left"]):
            rec["min_days_left"] = dl
    for p in mp["pawns"]:
        if p.get("role") not in ("colonist", "slave"):
            continue
        for it in p["inventory"]:
            nut = nutrition_of(it["def"])
            if nut is None:
                continue
            by_def[it["def"]]["count"] += it["stackCount"] or 1
    for defn, rec in by_def.items():
        nut = nutrition_of(defn)
        sub = nut * rec["count"]
        total += sub
        if defn.startswith("Meal"):
            meals += rec["count"]
        elif defn.startswith(("Raw", "Meat_")):
            raw_units += rec["count"]
        rows.append({"def": defn, "count": rec["count"], "nutrition_each": nut,
                     "nutrition": round(sub, 2), "min_rot_days_left": rec["min_days_left"]})
    rows.sort(key=lambda r: -r["nutrition"])
    eaters = [p for p in mp["pawns"] if p.get("role") in ("colonist", "slave", "guest", "prisoner")]
    need = HUMAN_NUTRITION_PER_DAY * len(eaters)
    # nấu suất đơn giản: 0.5 dinh dưỡng nguyên liệu (10 đơn vị) -> 1 suất 0.9
    cooked = meals * 0.9 + (raw_units // 10) * 0.9 + (raw_units % 10) * 0.05
    return {
        "rows": rows,
        "meals": meals,
        "raw_units": raw_units,
        "nutrition_total_as_is": round(total, 2),
        "nutrition_total_if_cooked": round(cooked, 2),
        "eaters": len(eaters),
        "nutrition_needed_per_day": round(need, 2),
        "days_as_is": round(total / need, 1) if need else None,
        "days_if_cooked": round(cooked / need, 1) if need else None,
    }


def file_sha1(path):
    """Mã SHA-1 của file save — để biết bản dump này sinh từ đúng phiên bản save nào."""
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_state(save: SaveFile, full_fields=False, all_pawns=False):
    g = save.game
    first_map = save.maps[0].el if save.maps else None
    last_raid = txt(g, "storyState/lastRaidFaction") or txt(first_map, "storyState/lastRaidFaction")
    player_settlements = [
        o.findtext("nameInt") for o in save.world.findall("worldObjects/worldObjects/li")
        if o.findtext("faction") == save.player_faction and o.findtext("nameInt")
    ]
    st = {
        "source": {
            "file": str(save.path),
            "size_bytes": save.path.stat().st_size,
            "sha1": file_sha1(save.path),
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
            "colonyName": player_settlements[0] if player_settlements else None,
            "playerFaction": (save.factions.get(save.player_faction) or {}).get("name"),
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
            "lastIncidentTick": num(txt(g, "storyteller/lastIncidentTick")),
            "queuedIncidents": len(g.findall("storyteller/incidentQueue/queuedIncidents/li")),
            "playSettings": {
                k: txt(g, f"playSettings/{k}")
                for k in ("useWorkPriorities", "showZones", "autoHomeArea", "showRoomStats")
            },
            "storyState": {
                "lastThreatBigTick": num(txt(g, "storyState/lastThreatBigTick")
                                         or txt(first_map, "storyState/lastThreatBigTick")),
                "lastRaidFaction": last_raid,
                "lastRaidFaction_name": save.faction_name(last_raid),
            },
            "storyWatcher": {
                "numRaidsEnemy": num(txt(g, "storyWatcher/statsRecord/numRaidsEnemy")),
                "numThreatsQueued": num(txt(g, "storyWatcher/statsRecord/numThreatsQueued")),
                "adaptDays": num(txt(g, "storyWatcher/watcherPopAdaptation/adaptDays")),
            },
            "unreadLetters": [(x.text or "").strip() for x in g.findall("letterStack/letters/li")],
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
                    "leader_name": name_of_pawn_el(save.ref_el(f["leader"])),
                    "hidden": f.get("hidden"),
                    "temporary": f.get("temporary"),
                    "defeated": f.get("defeated"),
                    "player": f["id"] == save.player_faction,
                    "relations": f["relations"],
                }
                for f in save.factions.values()
            ],
            "objects": extract_world_objects(save),
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
        "quests": extract_quests(save),
        "anomaly": extract_anomaly(g),
        "letters": extract_letters(save),
        "tales": extract_tales(save),
        "battle_log": extract_battle_log(save),
        "play_log": extract_play_log(save),
        "history": extract_history(save),
        "policies": extract_policies(g),
        "transport_ships": [
            {"def": s.findtext("def"), "thing": txt(s, "shipThing/def"),
             "faction": save.faction_name(txt(s, "shipThing/faction")),
             "questTags": [x.text for x in s.findall("shipThing/questTags/li")]}
            for s in g.findall("transportShipManager/ships/li")
        ],
        "world_pawns": [
            {k: v for k, v in w.items() if k != "el"} for w in save.world_pawns
        ],
        "maps": [],
    }
    for md in save.maps:
        st["maps"].append(extract_map(save, md, full_fields))
    link_quest_pawns(st)
    st["game"]["recent_temperature"] = recent_temperature(save, st["tales"])
    st["work_coverage"] = work_coverage(st)
    st["alerts"] = derive_alerts(save, st)
    return st


def recent_temperature(save, tales, days=5):
    """Biên độ nhiệt mà game ghi kèm các tale trong `days` ngày gần nhất (nhiệt độ tại chỗ pawn lúc đó)."""
    now = save.ticks_game
    samples = []
    for t in tales:
        sur = t.get("surroundings")
        if not sur or t["tick"] is None or sur.get("temperature") is None:
            continue
        if now - t["tick"] > days * TICKS_PER_DAY:
            continue
        samples.append({"tick": t["tick"], "date": save.fmt_tick(t["tick"]), "temp": round(sur["temperature"], 1),
                        "outdoors": sur.get("roomRole") in (None, "None")})
    if not samples:
        return None
    out = [x for x in samples if x["outdoors"]]
    ins = [x for x in samples if not x["outdoors"]]
    return {
        "days": days, "samples": len(samples),
        "outdoor_max": max(out, key=lambda x: x["temp"]) if out else None,
        "outdoor_min": min(out, key=lambda x: x["temp"]) if out else None,
        "indoor_max": max(ins, key=lambda x: x["temp"]) if ins else None,
        "indoor_min": min(ins, key=lambda x: x["temp"]) if ins else None,
    }


def link_quest_pawns(st):
    """Ghi chú quan hệ ruột thịt/hôn nhân giữa nhân vật trong nhiệm vụ và người đang ở trên map."""
    on_map = {"Thing_" + p["id"]: p for mp in st["maps"] for p in mp["pawns"]}
    for q in st["quests"]:
        for qp in q["pawns"]:
            links = []
            for ref, p in on_map.items():
                if ref == qp["ref"]:
                    continue
                role = ROLE_VI.get(p.get("role"), p.get("role"))
                for r in p["relations"]:
                    if r["otherPawn"] == qp["ref"]:
                        links.append(f"là `{r['def']}` của {who(p)} ({role} đang ở trên map)")
            for r in qp.pop("own_relations", []):
                p = on_map.get(r["otherPawn"])
                if p is not None:
                    txt_ = f"có `{r['def']}` là {who(p)} ({ROLE_VI.get(p.get('role'), p.get('role'))} đang ở trên map)"
                    if not any(who(p) in x and f"`{r['def']}`" in x for x in links):
                        links.append(txt_)
            qp["links"] = links


def extract_world_objects(save):
    objs = save.world.findall("worldObjects/worldObjects/li")
    by_faction = Counter()
    special = []
    for o in objs:
        d = o.findtext("def")
        fid = o.findtext("faction")
        if d == "Settlement":
            by_faction[fid] += 1
            if fid != save.player_faction:
                continue
        special.append({
            "class": o.attrib.get("Class"),
            "def": d,
            "tile": o.findtext("tile"),
            "name": o.findtext("nameInt"),
            "faction": save.faction_name(fid) if fid and fid != "null" else None,
            "questTags": [x.text for x in o.findall("questTags/li")],
            "extra": {c.tag: (c.text or "").strip() for c in o
                      if c.tag in ("preciousResource", "creationGameTicks", "expiration") and (c.text or "").strip()},
        })
    return {
        "total": len(objs),
        "settlements_by_faction": [
            {"faction": fid, "name": save.faction_name(fid), "count": n}
            for fid, n in by_faction.most_common()
        ],
        "special": special,
    }


def extract_research(g):
    """Save chỉ lưu SỐ ĐIỂM đã tích luỹ cho từng dự án (không lưu chi phí, không có cờ 'xong').

    Khi một dự án hoàn thành, game gán điểm = đúng chi phí gốc (số nguyên tròn),
    còn tiến độ dở dang luôn là số lẻ. Vì vậy: điểm > 0, là số nguyên và không phải
    dự án đang chọn => coi là ĐÃ XONG (suy luận, độ tin cậy cao)."""
    rm = g.find("researchManager")
    if rm is None:
        return {"current": None, "current_points": None, "completed": [], "partial": [], "all": [],
                "anomaly_knowledge": {}, "techprints": {}}
    keys = [x.text for x in rm.findall("progress/keys/li")]
    vals = [num(x.text, 0) or 0 for x in rm.findall("progress/values/li")]
    current = rm.findtext("currentProj")
    if current in ("null", ""):
        current = None
    done, partial, all_ = [], [], []
    for k, v in zip(keys, vals):
        if k == current:
            status = "in_progress"
        elif v <= 0:
            status = "none"
        elif float(v).is_integer():
            status = "done"
        else:
            status = "partial"
        if status == "done":
            done.append(k)
        elif status == "partial":
            partial.append({"def": k, "progress": v})
        all_.append({"def": k, "progress": v, "name": RESEARCH_VI.get(k, pretty_def(k)), "status": status})
    know = {k.text: num(v.text, 0) for k, v in zip(rm.findall("knowledge/keys/li"),
                                                 rm.findall("knowledge/values/li"))}
    return {
        "current": current,
        "current_points": dict(zip(keys, vals)).get(current) if current else None,
        "completed": done,
        "partial": partial,
        "all": all_,
        "anomaly_knowledge": {k: v for k, v in know.items() if v},
        "techprints": {k.text: num(v.text, 0) for k, v in zip(rm.findall("techprints/keys/li"),
                                                             rm.findall("techprints/values/li"))},
    }


QUEST_STATE_VI = {
    "NotYetAccepted": "CHƯA NHẬN (đang chờ quyết định)",
    "Ongoing": "ĐANG DIỄN RA",
    "EndedSuccess": "đã kết thúc: thành công",
    "EndedFailed": "đã kết thúc: thất bại",
    "EndedUnknownOutcome": "đã kết thúc",
    "EndedInvalid": "đã huỷ (không hợp lệ)",
    "EndedOfferExpired": "đã hết hạn nhận",
}


def extract_quests(save):
    g = save.game
    now = save.ticks_game
    out = []
    ref_re = re.compile(r"^Thing_[A-Za-z_]+\d+$")
    for q in g.findall("questManager/quests/li"):
        qid = num(q.findtext("id"), 0) or 0            # game không ghi id = 0
        appearance = num(q.findtext("appearanceTick"))
        accept = num(q.findtext("acceptanceTick"))
        expire = num(q.findtext("acceptanceExpireTick"))
        ended = q.findtext("ended") == "True"
        outcome = q.findtext("endOutcome")
        if ended:
            state = {"Success": "EndedSuccess", "Fail": "EndedFailed",
                     "InvalidPreAcceptance": "EndedInvalid"}.get(outcome, "EndedUnknownOutcome")
        elif accept is None or accept < 0:
            expired = expire is not None and expire >= 0 and now >= expire
            state = "EndedOfferExpired" if expired else "NotYetAccepted"
        else:
            state = "Ongoing"

        # thing định nghĩa ngay trong quest (vật thưởng thả pod…) để tra tên phần thưởng
        local = {}
        for el in q.iter():
            i, d = el.findtext("id"), el.findtext("def")
            if i and d:
                local["Thing_" + i] = el

        def describe_thing(ref):
            el = local.get(ref)
            if el is None:
                el = save.ref_el(ref)
            if el is None:
                return ref
            bits = [el.findtext("def") or ref]
            cnt = num(el.findtext("stackCount"), 1)
            if cnt and cnt != 1:
                bits.append(f"×{cnt}")
            if el.findtext("quality"):
                bits.append(f"({el.findtext('quality')})")
            if el.findtext("title"):
                bits.append(f"«{el.findtext('title')}»")
            return " ".join(bits)

        rewards = []
        for part in q.findall("parts/li"):
            if part.attrib.get("Class") != "QuestPart_Choice":
                continue
            for choice in part.findall("choices/li"):
                opts = []
                for rw in choice.findall("rewards/li"):
                    cls = (rw.attrib.get("Class") or "").replace("Reward_", "")
                    desc = cls
                    amount = rw.findtext("amount")
                    fac = rw.findtext("faction")
                    if cls == "Items":
                        desc = "Vật phẩm: " + ", ".join(describe_thing((x.text or "").strip())
                                                         for x in rw.findall("items/li"))
                    elif cls == "DefinedThingDef":
                        desc = f"Vật: {rw.findtext('thingDef')}"
                    elif amount:
                        desc = f"{cls} +{amount}"
                    if fac and fac != "null":
                        desc += f" [{save.faction_name(fac)}]"
                    opts.append(desc)
                if opts:
                    rewards.append(opts)

        timers = []
        for part in q.findall("parts/li"):
            cls = part.attrib.get("Class") or ""
            delay = num(part.findtext("delayTicks"))
            if "Delay" not in cls or delay is None:
                continue
            enable = num(part.findtext("enableTick"))
            lbl = clean_text(part.findtext("expiryInfoPart") or part.findtext("debugLabel")
                             or part.findtext("inspectString") or cls.replace("QuestPart_", ""))
            timers.append({
                "label": lbl.replace("{0}", "…"),
                "delayTicks": delay,
                "enableTick": enable,
                "state": part.findtext("state") or "NeverEnabled",
                "dueTick": (enable + delay) if enable is not None and enable >= 0 else None,
            })

        ends = []
        for part in q.findall("parts/li"):
            if part.attrib.get("Class") == "QuestPart_QuestEnd":
                sig = re.sub(r"^Quest\d+\.", "", part.findtext("inSignal") or "")
                rec = (sig, part.findtext("outcome") or "Unknown")
                if rec not in ends:
                    ends.append(rec)

        pawns, things, factions = [], [], []
        seen = set()
        parts_el = q.find("parts")
        for el in (parts_el.iter() if parts_el is not None else []):
            t = (el.text or "").strip()
            if t in seen:
                continue
            if ref_re.match(t):
                seen.add(t)
                target = save.ref_el(t)
                is_pawn = target is not None and (target.attrib.get("Class") == "Pawn"
                                                  or target.find("kindDef") is not None)
                if is_pawn and target.findtext("faction") == save.player_faction \
                        and not target.findall("questTags/li"):
                    continue        # thuộc địa viên chỉ được quest dùng để định vị map
                if is_pawn:
                    wp = next((w for w in save.world_pawns if w["pawn"] == t), None)
                    pawns.append({
                        "ref": t,
                        "name": name_of_pawn_el(target) or target.findtext("def"),
                        "kindDef": target.findtext("kindDef"),
                        "age": round((num(txt(target, "ageTracker/ageBiologicalTicks"), 0) or 0) / TICKS_PER_YEAR, 1),
                        "gender": infer_gender(target),
                        "faction": save.faction_name(target.findtext("faction")),
                        "where": ("đã chết" if (wp or {}).get("dead") else "đang ở ngoài map") if wp is not None
                                 else "đang ở trên map",
                        "questTags": [x.text for x in target.findall("questTags/li")],
                        "own_relations": [
                            {"def": r.findtext("def"), "otherPawn": r.findtext("otherPawn")}
                            for r in target.findall("social/directRelations/li")
                        ],
                        "links": [],
                    })
                elif target is not None:
                    things.append({"ref": t, "def": target.findtext("def"),
                                   "pos": parse_pos(target.findtext("pos"))})
            elif re.match(r"^Faction_\d+$", t):
                seen.add(t)
                factions.append(save.faction_name(t))

        out.append({
            "id": qid,
            "name": q.findtext("name"),
            "root": q.findtext("root"),
            "state": state,
            "state_vi": QUEST_STATE_VI.get(state, state),
            "appearanceTick": appearance,
            "acceptanceTick": accept,
            "acceptanceExpireTick": expire,
            "ticksUntilOfferExpires": (expire - now) if state == "NotYetAccepted" and expire is not None and expire >= 0 else None,
            "acceptedBy": q.findtext("acceptedBy"),
            "challengeRating": num(q.findtext("challengeRating")),
            "charity": q.findtext("charity") == "True",
            "hidden": q.findtext("hidden") == "True" or q.findtext("hiddenInUI") == "True",
            "initiallyAccepted": q.findtext("initiallyAccepted") == "True",
            "description": q.findtext("description"),
            "description_clean": clean_text(q.findtext("description")),
            "parts": [p.attrib.get("Class") for p in q.findall("parts/li")],
            "ended": q.findtext("ended"),
            "endOutcome": outcome,
            "cleanupTick": num(q.findtext("cleanupTick")),
            "rewards": rewards,
            "timers": timers,
            "end_conditions": [{"signal": s, "outcome": o} for s, o in ends],
            "pawns": pawns,
            "things": things,
            "factions": factions,
            "tags": [x.text for x in q.findall("tags/li")],
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
                "monolithAnomalyKnowledge": num(li.findtext("monolithAnomalyKnowledge")),
            }
    return None


def extract_letters(save):
    """Thư + thông báo trong kho lưu trữ (history/archive), kèm ngày giờ game."""
    g = save.game
    unread = {(x.text or "").strip() for x in g.findall("letterStack/letters/li")}
    out = []
    for li in g.findall("history/archive/archivables/li"):
        cls = li.attrib.get("Class")
        is_msg = cls == "Message"
        arrival = num(li.findtext("arrivalTick"))
        tick = num(li.findtext("startingTick")) if is_msg else arrival
        lid = li.findtext("ID")
        fac = li.findtext("relatedFaction")
        quest = li.findtext("quest")
        out.append({
            "class": cls,
            "def": li.findtext("def"),
            "label": clean_text(li.findtext("label")) or None,
            "text": clean_text(li.findtext("text")),
            "tick": tick,
            "date": save.fmt_tick(tick) if tick is not None else None,
            "arrivalTick": arrival,
            "messageID": lid,
            "relatedFaction": fac if fac not in (None, "null") else None,
            "relatedFaction_name": save.faction_name(fac) if fac not in (None, "null") else None,
            "quest": quest if quest not in (None, "null") else None,
            "unread": (not is_msg) and f"Letter_{lid or 0}" in unread,
        })
    return out


def extract_tales(save):
    """Tale = sự kiện đáng nhớ game ghi lại (đột kích, hạ gục, giết, săn, giao dịch…)."""
    out = []
    for tl in save.game.findall("taleManager/tales/li"):
        date = num(tl.findtext("date"))
        tick = (date - save.game_start_abs) if date is not None else None

        def pd(tag):
            e = tl.find(tag)
            if e is None:
                return None
            n = e.find("name")
            nm = None
            if n is not None:
                nm = n.findtext("nick") or n.findtext("first") or (n.text or "").strip() or None
            ref = e.findtext("pawn")
            cur = pawn_nick(save.ref_el(ref))       # tên/biệt danh HIỆN TẠI nếu pawn còn tồn tại
            return {"pawn": ref, "kind": e.findtext("kind"), "faction": e.findtext("faction"),
                    "name": cur or nm or e.findtext("kind"),
                    "name_then": nm if cur and nm and nm != cur else None}

        sur = tl.find("surroundings")
        out.append({
            "def": tl.findtext("def"),
            "class": tl.attrib.get("Class"),
            "tick": tick,
            "date": save.fmt_tick(tick) if tick is not None else None,
            "pawn": pd("pawnData"),
            "first": pd("firstPawnData"),
            "second": pd("secondPawnData"),
            "thing": txt(tl, "defData/defName"),
            "label": tl.findtext("customLabel"),
            "surroundings": {
                "temperature": num(sur.findtext("temperature")),
                "roomRole": sur.findtext("roomRole"),
                "roomImpressiveness": num(sur.findtext("roomImpressiveness")),
                "roomBeauty": num(sur.findtext("roomBeauty")),
                "roomCleanliness": num(sur.findtext("roomCleanliness")),
                "weather": sur.findtext("weather"),
            } if sur is not None and sur.attrib.get("IsNull") != "True" else None,
        })
    return out


# --------------------------------------------------------------------------
# Nhật ký chiến đấu (battleLog) & nhật ký tương tác xã hội (playLog)
# --------------------------------------------------------------------------

_COLOR_TAG_RE = re.compile(r"</?color[^>]*>")
_THING_REF_RE = re.compile(r"^Thing_(.+?)(\d+)$")

INTERACTION_VI = {
    "Chitchat": "chuyện phiếm", "DeepTalk": "tâm sự sâu", "KindWords": "nói lời tử tế",
    "Insult": "xúc phạm", "Slight": "nói mỉa / coi thường",
    "RomanceAttempt": "tán tỉnh", "MarriageProposal": "cầu hôn", "Breakup": "chia tay",
    "RecruitAttempt": "chiêu mộ tù nhân", "BuildRapport": "tạo thiện cảm với tù nhân",
    "ConvertIdeoAttempt": "truyền đạo", "ReduceWill": "bào mòn ý chí tù nhân", "EnslaveAttempt": "bắt làm nô lệ",
    "SparkJailbreak": "xúi vượt ngục", "PrisonerRelease": "thả tù nhân", "InterrogateIdentity": "tra hỏi danh tính",
    "AnimalChat": "trò chuyện với thú", "TameAttempt": "thuần hoá thú", "TrainAttempt": "huấn luyện thú",
    "Nuzzle": "thú dụi vào người", "ReleaseToWild": "thả thú về tự nhiên",
    "Counsel_Success": "khuyên nhủ thành công", "Counsel_Failure": "khuyên nhủ thất bại",
    "Reassure": "trấn an", "Trial_Accuse": "buộc tội", "Trial_Defend": "bào chữa",
    "BabyPlay": "chơi với em bé", "LessonSpeech": "dạy học", "Suppress": "trấn áp nô lệ",
}
# Tương tác "nền" — chỉ đếm, không liệt kê từng dòng.
INTERACTION_ROUTINE = {"Chitchat", "AnimalChat", "Nuzzle", "BabyPlay"}


def log_pawn(save, ref):
    """Tham chiếu pawn trong log -> dict mô tả ngắn; None nếu rỗng.

    Pawn đã chết vẫn nằm trong worldPawns/pawnsDead nên thường còn tra được tên;
    pawn đã bị xoá hẳn khỏi save thì chỉ còn suy được loài từ ID (Thing_WildBoar75683)."""
    if not ref or ref in ("null", "None"):
        return None
    el = save.ref_el(ref)
    if el is not None:
        d = el.findtext("def") or "?"
        fid = el.findtext("faction")
        fid = fid if fid and fid != "null" else None
        return {"ref": ref, "label": pawn_nick(el) or d, "def": d, "human": d == "Human",
                "faction": fid, "faction_name": save.faction_name(fid) if fid else None,
                "side": save.relation_to_player(fid), "gone": False,
                "dead": el.findtext("healthTracker/healthState") == "Dead"}
    m = _THING_REF_RE.match(ref)
    d = m.group(1) if m else ref
    return {"ref": ref, "label": (f"Human#{m.group(2)}" if m and d == "Human" else d), "def": d,
            "human": d == "Human", "faction": None, "faction_name": None, "side": None, "gone": True, "dead": None}


def extract_battle_log(save):
    """battleLog: game gom các đòn đánh / phát bắn gần nhau thành từng 'trận' (kể cả thú hoang săn nhau).

    Dòng gốc gồm: RangedFire (một phát bắn ra), RangedImpact (viên đạn rơi vào đâu), MeleeCombat (một đòn
    cận chiến; trúng/trượt nằm ở đuôi ruleDef), StateTransition (gục / chết), Event (choáng), ExplosionImpact.
    Hàm này gộp theo cặp (ai → ai, bằng gì) và giữ nguyên các kết cục."""
    out = []
    for b in save.game.findall("battleLog/battles/li"):
        entries = b.findall("entries/li")
        if not entries:
            continue
        people = {}

        def P(ref, thing=None):
            if not ref or ref in ("null", "None"):
                if not thing or thing in ("null", "None"):
                    return None
                ref = "thing:" + thing            # đòn đánh vào đồ vật (cửa, tường…)
                people.setdefault(ref, {"ref": ref, "label": f"vật `{thing}`", "def": thing, "human": False,
                                        "faction": None, "faction_name": None, "side": None, "gone": False,
                                        "is_thing": True})
                return ref
            if ref not in people:
                people[ref] = log_pawn(save, ref)
            return ref

        ex = {}

        def X(a, c, mode, weapon, tick):
            key = (a, c, mode, weapon)
            r = ex.get(key)
            if r is None:
                r = ex[key] = {"from": a, "to": c, "mode": mode, "weapon": weapon, "attempts": 0, "hits": 0,
                               "damaging": 0, "parts_destroyed": 0, "deflected": 0, "blocked": 0, "bursts": 0,
                               "first_tick": tick, "last_tick": tick}
            if tick is not None:
                r["first_tick"] = tick if r["first_tick"] is None else min(r["first_tick"], tick)
                r["last_tick"] = tick if r["last_tick"] is None else max(r["last_tick"], tick)
            return r

        outcomes, events, other, ticks = [], [], Counter(), []
        blocked_by = Counter()                # đạn trượt mục tiêu nhưng trúng vật gì (cây, tường, đá…)
        for e in entries:
            cls = (e.attrib.get("Class") or "").replace("BattleLogEntry_", "")
            ta = num(e.findtext("ticksAbs"))
            tick = int(ta - save.game_start_abs) if ta is not None else None
            if tick is not None:
                ticks.append(tick)
            n_parts = len(e.findall("damagedParts/li"))
            n_destroyed = sum(1 for x in e.findall("damagedPartsDestroyed/li") if (x.text or "").strip() == "True")
            deflected = e.findtext("deflected") == "True"

            def score(r, hit):
                if hit:
                    r["hits"] += 1
                    r["damaging"] += 1 if n_parts else 0
                    r["parts_destroyed"] += n_destroyed
                    r["deflected"] += 1 if deflected else 0

            if cls == "RangedFire":
                a, c = P(e.findtext("initiatorPawn")), P(e.findtext("recipientPawn"))
                r = X(a, c, "ranged", e.findtext("weaponDef"), tick)
                r["attempts"] += 1                      # 1 dòng = 1 lần bóp cò (súng bắn loạt: 1 loạt nhiều viên)
                if e.findtext("burst") == "True":
                    r["bursts"] += 1
            elif cls == "RangedImpact":
                a = P(e.findtext("initiatorPawn"))
                orig = P(e.findtext("originalTargetPawn"))
                hit = P(e.findtext("recipientPawn"))
                if hit is None:                                # trượt: đạn rơi xuống đất hoặc trúng vật cản
                    thing = e.findtext("recipientThing")
                    if thing and thing != "null":
                        X(a, orig, "ranged", e.findtext("weaponDef"), tick)["blocked"] += 1
                        blocked_by[thing] += 1
                    continue
                mode = "ranged" if (orig is None or hit == orig) else "stray"
                score(X(a, hit, mode, e.findtext("weaponDef"), tick), True)
            elif cls == "MeleeCombat":
                a = P(e.findtext("initiator"))
                c = P(e.findtext("recipientPawn"), e.findtext("recipientThing"))
                impl = e.findtext("implementType")
                weapon = e.findtext("ownerDef") if impl == "Weapon" else None
                kind = e.findtext("def") or "MeleeAttack"
                rule = e.findtext("ruleDef") or ""
                r = X(a, c, "melee" if kind == "MeleeAttack" else kind, weapon, tick)
                r["attempts"] += 1
                score(r, rule.endswith("Hit") or n_parts > 0)
            elif cls == "ExplosionImpact":
                a, c = P(e.findtext("initiatorPawn")), P(e.findtext("recipientPawn"), e.findtext("recipientThing"))
                r = X(a, c, "explosion", e.findtext("damageDef"), tick)
                r["attempts"] += 1
                score(r, True)
            elif cls == "StateTransition":
                outcomes.append({
                    "what": (e.findtext("transitionDef") or "").replace("Transition_", ""),
                    "who": P(e.findtext("subjectPawn")), "by": P(e.findtext("initiator")),
                    "cause": e.findtext("culpritHediffDef"), "tick": tick,
                    "date": save.fmt_tick(tick) if tick is not None else None,
                })
            elif cls == "Event":
                events.append({"def": (e.findtext("eventDef") or "").replace("Event_", ""),
                               "who": P(e.findtext("subjectPawn")), "by": P(e.findtext("initiatorPawn")), "tick": tick})
            else:
                other[cls] += 1

        # nhãn trùng nhau trong cùng một trận (hai con sóc khác nhau…) -> đánh số
        by_label = defaultdict(list)
        for ref, p in people.items():
            by_label[p["label"]].append(ref)
        for lab, refs in by_label.items():
            if len(refs) > 1:
                for k, ref in enumerate(sorted(refs), 1):
                    people[ref]["label"] = f"{lab}#{k}"

        created = num(b.findtext("creationTimestamp"))
        start = min(ticks) if ticks else created
        end = max(ticks) if ticks else created
        exchanges = sorted(ex.values(), key=lambda r: (r["first_tick"] if r["first_tick"] is not None else 0))
        outcomes.sort(key=lambda o: o["tick"] if o["tick"] is not None else 0)
        out.append({
            "id": b.findtext("loadID"),
            "name": _COLOR_TAG_RE.sub("", b.findtext("battleName") or "").strip() or None,
            "start_tick": start, "end_tick": end,
            "date": save.fmt_tick(start) if start is not None else None,
            "date_end": save.fmt_tick(end) if end is not None else None,
            "entries": len(entries),
            "participants": list(people.values()),
            "exchanges": exchanges,
            "outcomes": outcomes,
            "events": events,
            "blocked_by": dict(blocked_by),
            "other_entries": dict(other),
            "involves_humans": any(p["human"] for p in people.values()),
            "involves_colony": any(p["side"] == "Player" for p in people.values()),
        })
    out.sort(key=lambda r: r["start_tick"] if r["start_tick"] is not None else 0)
    return out


def extract_play_log(save):
    """playLog: các tương tác xã hội gần nhất (game chỉ giữ một số dòng mới nhất)."""
    out = []
    for e in save.game.findall("playLog/entries/li"):
        ta = num(e.findtext("ticksAbs"))
        tick = int(ta - save.game_start_abs) if ta is not None else None
        out.append({
            "tick": tick,
            "date": save.fmt_tick(tick) if tick is not None else None,
            "class": (e.attrib.get("Class") or "").replace("PlayLogEntry_", ""),
            "def": e.findtext("intDef") or e.findtext("def"),
            "initiator": log_pawn(save, e.findtext("initiator")),
            "recipient": log_pawn(save, e.findtext("recipient")),
            "extras": [x.text for x in e.findall("extras/li") if x.text],
        })
    out.sort(key=lambda r: r["tick"] if r["tick"] is not None else 0)
    return out


def battle_people(b):
    return {p["ref"]: p for p in b["participants"]}


def battle_sides(b):
    """'bac si, Protein ↔ Elphy (Khí độc đàn ông)' — gom người tham chiến theo phe."""
    groups = defaultdict(list)
    for p in b["participants"]:
        if p.get("is_thing"):
            continue
        if p["side"] == "Player":
            key = (0, "thuộc địa")
        elif p.get("gone"):
            key = (4, "không còn trong save")
        elif p["faction_name"]:
            key = (1, p["faction_name"])
        elif p["human"]:
            key = (2, "người không rõ phe")
        else:
            key = (3, "thú hoang")
        groups[key].append(p["label"])
    bits = []
    for (order, name), labels in sorted(groups.items()):
        cnt = Counter(re.sub(r"#\d+$", "", x) for x in labels)
        names = ", ".join(f"{k}×{v}" if v > 1 else k for k, v in cnt.items())
        bits.append(names if order == 0 else f"{names} ({name})")
    return " ↔ ".join(bits) or "—"


def battle_pairs(b):
    """Gộp các exchange theo cặp (ai → ai) và theo kiểu: bắn / cận chiến / lạc đạn / nổ."""
    ppl = battle_people(b)
    pairs = {}
    for x in b["exchanges"]:
        cat = x["mode"] if x["mode"] in ("ranged", "stray", "explosion") else "melee"
        rec = pairs.setdefault((x["from"], x["to"]), {})
        c = rec.setdefault(cat, {"attempts": 0, "hits": 0, "weapons": [], "parts_destroyed": 0, "deflected": 0,
                                 "blocked": 0, "sand": 0, "bursts": 0})
        for k in ("attempts", "hits", "parts_destroyed", "deflected", "blocked", "bursts"):
            c[k] += x.get(k, 0)
        if x["mode"] == "SandInEyes":
            c["sand"] += x["attempts"]
            continue
        if x["weapon"]:
            w = f"`{x['weapon']}`"
        elif x["mode"] not in ("melee", "ranged", "stray", "explosion"):
            w = f"`{x['mode']}`"
        elif cat == "melee" and (ppl.get(x["from"]) or {}).get("human"):
            w = "tay không"
        else:
            w = None
        if w and w not in c["weapons"]:
            c["weapons"].append(w)
    return pairs


def battle_text(b, with_exchanges=True):
    """Một dòng diễn biến: ai đánh ai bằng gì, bao nhiêu đòn, trúng bao nhiêu; rồi tới ai gục / chết."""
    ppl = battle_people(b)

    def L(ref):
        return ppl[ref]["label"] if ref in ppl else "không rõ"

    bits = []
    if with_exchanges:
        for (a, c), rec in battle_pairs(b).items():
            parts = []
            for cat, verb in (("ranged", "bắn"), ("melee", "cận chiến"), ("stray", "bắn lạc trúng"), ("explosion", "nổ/lửa")):
                x = rec.get(cat)
                if not x:
                    continue
                w = f" ({', '.join(x['weapons'])})" if x["weapons"] else ""
                if cat in ("ranged", "melee"):
                    t = f"{verb} {x['attempts']} trúng {x['hits']}{w}"
                else:
                    t = f"{verb} ×{x['hits']}{w}"
                extra = []
                if x["bursts"]:
                    extra.append(f"{x['bursts']} lần là bắn loạt nhiều viên — số trúng/vướng tính theo viên")
                if x["sand"]:
                    extra.append(f"{x['sand']} lần là hất đất vào mắt")
                if x["blocked"]:
                    extra.append(f"{x['blocked']} phát vướng vật cản")
                if x["deflected"]:
                    extra.append(f"{x['deflected']} bị giáp chặn")
                if x["parts_destroyed"]:
                    extra.append(f"huỷ {x['parts_destroyed']} bộ phận")
                parts.append(t + (f" [{', '.join(extra)}]" if extra else ""))
            bits.append(f"{L(a)} → {L(c)}: " + " + ".join(parts))
    for o in b["outcomes"]:
        verb = {"Died": "CHẾT", "Downed": "gục"}.get(o["what"], o["what"])
        why = []
        if o["by"]:
            why.append(f"do {L(o['by'])}")
        if o["cause"]:
            why.append(f"`{o['cause']}`")
        bits.append(f"**{L(o['who'])} {verb}**" + (f" ({', '.join(why)})" if why else ""))
    return "; ".join(bits) or "—"


def combat_record(battles):
    """Thành tích của từng pawn thuộc địa trên toàn bộ battleLog: bắn / cận chiến / bị trúng / hạ được ai."""
    rec = {}

    def R(p):
        return rec.setdefault(p["ref"], {"label": re.sub(r"#\d+$", "", p["label"]), "human": p["human"],
                                         "ranged": defaultdict(lambda: [0, 0, 0, 0]),
                                         "melee": [0, 0], "taken": 0, "downed": 0, "kills": Counter(), "downs_dealt": 0})

    for b in battles:
        ppl = battle_people(b)
        for x in b["exchanges"]:
            a, c = ppl.get(x["from"]), ppl.get(x["to"])
            if a and a["side"] == "Player":
                r = R(a)
                if x["mode"] == "ranged":
                    r["ranged"][x["weapon"] or "?"][0] += x["attempts"]
                    r["ranged"][x["weapon"] or "?"][1] += x["hits"]
                    r["ranged"][x["weapon"] or "?"][2] += x.get("blocked", 0)
                    r["ranged"][x["weapon"] or "?"][3] += x.get("bursts", 0)
                elif x["mode"] not in ("stray", "explosion"):
                    r["melee"][0] += x["attempts"]
                    r["melee"][1] += x["hits"]
            if c and c["side"] == "Player":
                R(c)["taken"] += x["hits"]
        for o in b["outcomes"]:
            who, by = ppl.get(o["who"]), ppl.get(o["by"])
            if who and who["side"] == "Player" and o["what"] == "Downed":
                R(who)["downed"] += 1
            if by and by["side"] == "Player" and who:
                if o["what"] == "Died":
                    R(by)["kills"][re.sub(r"#\d+$", "", who["label"]) if who["human"] else who["def"]] += 1
                elif o["what"] == "Downed":
                    R(by)["downs_dealt"] += 1
    return rec


def last_threat_line(save, state):
    """'4 lần đột kích (phe gần nhất …); mối đe doạ lớn gần nhất: `ManhunterPack` lúc …'.

    lastThreatBigTick là của MỌI loại đe doạ lớn (đột kích, bầy thú điên, vây hãm…), còn lastRaidFaction chỉ là
    phe của lần ĐỘT KÍCH gần nhất — hai thứ không nhất thiết cùng một sự kiện, nên tra tên sự cố theo tick."""
    g = state["game"]
    now = save.ticks_game
    ss = g.get("storyState") or {}
    raids = (g.get("storyWatcher") or {}).get("numRaidsEnemy")
    bits = [f"{raids} lần đột kích" if raids is not None else "số lần đột kích: không rõ"]
    incidents = []
    for mp in state["maps"]:
        incidents += (mp.get("story") or {}).get("lastIncidents") or []
    raid = max((i for i in incidents if i["incident"].startswith("Raid") and i.get("tick") is not None),
               key=lambda i: i["tick"], default=None)
    if ss.get("lastRaidFaction_name"):
        bits[0] += (f" (gần nhất: {ss['lastRaidFaction_name']}"
                    + (f", lúc {save.fmt_tick(raid['tick'])}" if raid else "") + ")")
    t = ss.get("lastThreatBigTick")
    if t is not None and t >= 0:
        what = [i["incident"] for i in incidents if i.get("tick") == t]
        bits.append("mối đe doạ lớn gần nhất: " + (", ".join(f"`{w}`" for w in what) + " " if what else "")
                    + f"lúc {save.fmt_tick(t)} ({fmt_duration(now - t)} trước)")
    return "; ".join(bits)


def block_battle_log(d, save, state, level=3):
    """Nhật ký chiến đấu: thành tích từng người + một dòng cho mỗi trận."""
    battles = state.get("battle_log") or []
    if not battles:
        return False
    n_entries = sum(b["entries"] for b in battles)
    d.h(level, f"Nhật ký chiến đấu (`battleLog`: {len(battles)} trận, {n_entries:,} dòng gốc)")
    d.p("Game ghi lại từng phát bắn, từng đòn đánh (kể cả đi săn và thú hoang săn nhau) rồi gom thành «trận». "
        "Ở đây đã gộp theo cặp: «bắn 12 trúng 3» = bắn ra 12 phát, 3 phát trúng đúng mục tiêu; "
        "«cận chiến 5 trúng 2» = ra 5 đòn, trúng 2 (cận chiến kèm tên súng = dùng báng/nòng súng để đánh). "
        "«vướng vật cản» = viên đạn trượt mục tiêu và găm vào cây/tường/đá. Tên dạng `Loài` là thú không có tên riêng; "
        "`#1`, `#2` phân biệt các con cùng loài trong một trận. Dòng chỉ có kết cục (không có đòn đánh) là "
        "con vật/người gục hoặc chết sau trận vì mất máu, bệnh…")

    rec = combat_record(battles)
    if rec:
        lines = []
        for r in sorted(rec.values(), key=lambda r: (not r["human"], r["label"])):
            bits = []
            for w, (att, hit, blocked, bursts) in sorted(r["ranged"].items(), key=lambda kv: -kv[1][0]):
                if not att:
                    bits.append(f"`{w}`: {hit} viên trúng (không có dòng khai hoả)")
                elif bursts:
                    bits.append(f"bắn `{w}` {att} lần ({bursts} lần là loạt nhiều viên), {hit} viên trúng mục tiêu"
                                + (f", {blocked} viên vướng vật cản" if blocked else ""))
                else:
                    bits.append(f"bắn `{w}` {att} phát, trúng mục tiêu {hit} ({hit / att:.0%})"
                                + (f", {blocked} phát vướng vật cản" if blocked else ""))
            if r["melee"][0]:
                bits.append(f"cận chiến {r['melee'][0]} đòn, trúng {r['melee'][1]} ({r['melee'][1] / r['melee'][0]:.0%})")
            bits.append(f"bị đánh trúng {r['taken']} lần")
            if r["downed"]:
                bits.append(f"bị gục {r['downed']} lần")
            if r["kills"]:
                bits.append("đã giết: " + ", ".join(f"{k}×{v}" if v > 1 else k for k, v in r["kills"].most_common()))
            lines.append(f"- **{r['label']}**" + ("" if r["human"] else " (thú của thuộc địa)") + ": " + "; ".join(bits) + ".")
        blocked = Counter()
        for b in battles:
            blocked.update(b.get("blocked_by") or {})
        d.p("**Thành tích của phía thuộc địa trên toàn bộ log** (tính cả đi săn):\n" + "\n".join(lines)
            + (f"\n- Đạn trượt mục tiêu nhưng găm vào vật cản ({sum(blocked.values())} viên): "
               + ", ".join(f"`{k}` ×{v}" for k, v in blocked.most_common(15))
               + (f", … và {len(blocked) - 15} loại khác" if len(blocked) > 15 else "") + "."
               if blocked else ""))

    d.table(["Lúc", "Các bên", "Diễn biến → kết cục"],
            [[battle_when(b), battle_sides(b), battle_text(b)] for b in battles])
    return True


def block_play_log(d, save, state, level=3, full=False):
    """Nhật ký tương tác xã hội."""
    log = state.get("play_log") or []
    if not log:
        return False
    on_map = {"Thing_" + p["id"]: (p["nick"] or p["name"]) for mp in state["maps"] for p in mp["pawns"]}
    d.h(level, f"Tương tác xã hội gần đây (`playLog`: {len(log)} dòng)")
    span = [x for x in log if x["tick"] is not None]
    d.p(f"Game chỉ giữ {len(log)} tương tác mới nhất — ở đây là từ {span[0]['date']} đến {span[-1]['date']}. "
        "Chiều mũi tên: người mở lời → người nghe." if span else f"{len(log)} dòng, không có mốc thời gian.")

    def nm(p):
        return p["label"] if p else "?"

    def vi(dn):
        return f"`{dn}`" + (f" ({INTERACTION_VI[dn]})" if dn in INTERACTION_VI else "")

    inside = [x for x in log if x["initiator"] and x["recipient"]
              and x["initiator"]["ref"] in on_map and x["recipient"]["ref"] in on_map]
    outside = [x for x in log if x not in inside]
    if inside:
        cnt = defaultdict(Counter)
        for x in inside:
            cnt[(nm(x["initiator"]), nm(x["recipient"]))][x["def"]] += 1
        d.table(["Ai → ai (đều đang ở trên map)", "Số lần theo loại"],
                [[f"{a} → {b}", ", ".join(f"{vi(k)} ×{v}" for k, v in c.most_common())]
                 for (a, b), c in sorted(cnt.items(), key=lambda kv: -sum(kv[1].values()))])
    notable = [x for x in log if x["def"] not in INTERACTION_ROUTINE]
    if notable:
        d.p("**Đáng chú ý (không phải chuyện phiếm):** " + "; ".join(
            f"{x['date']} — {nm(x['initiator'])} → {nm(x['recipient'])}: {vi(x['def'])}"
            + (f" [{', '.join(x['extras'])}]" if x["extras"] else "") for x in notable) + ".")
    else:
        d.p("Không có tương tác nào ngoài chuyện phiếm.")
    if outside:
        cnt = Counter()
        who = Counter()
        for x in outside:
            cnt[x["def"]] += 1
            for p in (x["initiator"], x["recipient"]):
                if p and p["ref"] not in on_map:
                    tag = ("không còn trong save" if p.get("gone") else
                           ("thú của thuộc địa" if not p["human"] else "người của thuộc địa") if p["side"] == "Player" else
                           p["faction_name"] or ("người không phe" if p["human"] else "thú hoang"))
                    who[f"{p['label']} [{tag}{', đã chết' if p.get('dead') else ''}]"] += 1
        d.p(f"**Có người/thú hiện không ở trên map** (khách đã rời đi, thú đã chết…): {len(outside)} dòng — "
            + ", ".join(f"{vi(k)} ×{v}" for k, v in cnt.most_common())
            + "; số dòng theo từng cá thể: " + ", ".join(f"{k} ×{v}" for k, v in who.most_common(12))
            + (f", … và {len(who) - 12} cá thể khác" if len(who) > 12 else "") + ".")
    if full:
        d.h(level + 1, "Toàn bộ các dòng")
        d.table(["Lúc", "Người mở lời", "Người nghe", "Loại", "Kèm theo"],
                [[x["date"], nm(x["initiator"]), nm(x["recipient"]), vi(x["def"]), ", ".join(x["extras"])] for x in log])
    return True


def battle_when(b):
    if not b.get("date"):
        return "—"
    if b.get("date_end") and b["date_end"] != b["date"]:
        d1, d2 = b["date"], b["date_end"]
        same_day = d1.rsplit(" ", 1)[0] == d2.rsplit(" ", 1)[0]
        return f"{d1}–{d2.rsplit(' ', 1)[-1] if same_day else d2}"
    return b["date"]



def extract_history(save):
    """Chuỗi số liệu game tự ghi định kỳ: tài sản, tâm trạng trung bình…"""
    out = {"series": {}, "interval_ticks": None}
    n_max = 0
    for rec in save.game.findall("history/autoRecorderGroups/li/recorders/li"):
        vals = decode_float_series(rec.findtext("records"))
        if vals:
            out["series"][rec.findtext("def")] = vals
            n_max = max(n_max, len(vals))
    if n_max > 1:
        for f in (60_000, 30_000, 20_000, 15_000, 10_000, 7_500, 5_000, 2_500):
            if save.ticks_game // f + 1 == n_max:
                out["interval_ticks"] = f
                out["last_sample_tick"] = (n_max - 1) * f
                break
    return out


def extract_policies(g):
    def flt(pol):
        return {
            "allowed_count": len(pol.findall("filter/allowedDefs/li")),
            "hp": pol.findtext("filter/allowedHitPointsPercents"),
            "quality": pol.findtext("filter/allowedQualityLevels"),
        }
    drugs = []
    for pol in g.findall("drugPolicyDatabase/policies/li"):
        entries = []
        for e in pol.findall("drugs/li"):
            entries.append({
                "drug": e.findtext("drug"),
                "allowedForAddiction": e.findtext("allowedForAddiction") == "True",
                "allowedForJoy": e.findtext("allowedForJoy") == "True",
                "allowScheduled": e.findtext("allowScheduled") == "True",
                "daysFrequency": num(e.findtext("daysFrequency")),
                "takeToInventory": num(e.findtext("takeToInventory"), 0),
            })
        drugs.append({"id": pol.findtext("id"), "label": pol.findtext("label"), "entries": entries})
    return {
        "drug": drugs,
        "outfit": [{"id": p.findtext("id"), "label": p.findtext("label"), **flt(p)}
                   for p in g.findall("outfitDatabase/outfits/li")],
        "food": [{"id": p.findtext("id"), "label": p.findtext("label"), **flt(p)}
                 for p in g.findall("foodRestrictionDatabase/foodRestrictions/li")],
        "reading": [{"id": p.findtext("id"), "label": p.findtext("label")}
                    for p in g.findall("readingPolicyDatabase/policies/li")],
    }


def policy_label(ref):
    """'DrugPolicy_Chính sách thuốc_87699' -> 'Chính sách thuốc'."""
    if not ref or ref == "null":
        return "—"
    m = re.match(r"^[A-Za-z]+Policy_(.*)_\d+$", ref)
    return m.group(1) if m else ref


# --------------------------------------------------------------------------
# Suy diễn từ state: ai làm việc gì, cảnh báo cần chú ý
# --------------------------------------------------------------------------

def colonists_of(mp):
    return [p for p in mp["pawns"] if p.get("role") == "colonist"]


def work_coverage(state):
    """Với mỗi loại việc: thuộc địa viên nào đang bật (ưu tiên 1-4), ai tắt."""
    out = []
    people = [p for mp in state["maps"] for p in colonists_of(mp)]
    if not people:
        return out
    n = max((len(p["work_priorities"]) for p in people), default=0)
    for i in range(n):
        row = None
        workers = []
        for p in people:
            if i < len(p["work_priorities"]):
                wp = p["work_priorities"][i]
                row = row or {"index": i, "def": wp["def"], "name": wp["name"]}
                if wp["value"]:
                    workers.append({"pawn": p["nick"] or p["name"], "priority": wp["value"]})
        if row:
            row["workers"] = sorted(workers, key=lambda x: x["priority"])
            out.append(row)
    return out


WORK_SKILL = {
    "Doctor": "Medicine", "Cooking": "Cooking", "Hunting": "Shooting", "Construction": "Construction",
    "Growing": "Plants", "Mining": "Mining", "PlantCutting": "Plants", "Smithing": "Crafting",
    "Tailoring": "Crafting", "Art": "Artistic", "Crafting": "Crafting", "Research": "Intellectual",
    "Handling": "Animals", "Warden": "Social", "DarkStudy": "Intellectual", "Fishing": "Animals",
}

MOOD_BREAK_MINOR = 0.35      # ngưỡng gốc vanilla (chưa tính trait thay đổi ngưỡng)
MOOD_BREAK_MAJOR = 0.20
MOOD_BREAK_EXTREME = 0.05
PREDATOR_DEFS = {
    "Wolf_Timber", "Wolf_Arctic", "Warg", "Bear_Grizzly", "Bear_Polar", "Cougar", "Panther",
    "Lynx", "Cobra", "Fox_Red", "Fox_Arctic", "Fox_Fennec", "Tiger", "Wolverine", "Wolf_Great",
    "Cat_Scimitar", "Alligator", "Megaspider", "BogHound",
}


def derive_alerts(save, state):
    """Danh sách điều cần chú ý, mỗi mục kèm số liệu gốc. sev: 3 = khẩn, 2 = quan trọng, 1 = lưu ý."""
    A = []

    def add(sev, cat, text):
        A.append({"sev": sev, "cat": cat, "text": text})

    now = save.ticks_game
    date = state["game"]["date"]
    coverage = {w["def"]: w for w in state.get("work_coverage", [])}

    def workers_of(wdef):
        return (coverage.get(wdef) or {}).get("workers", [])

    for mp in state["maps"]:
        cols = colonists_of(mp)
        able = []      # thuộc địa viên đang làm việc được
        for p in mp["pawns"]:
            nm = p["nick"] or p["name"] or p["id"]
            role = p.get("role")
            mine = role in ("colonist", "slave")
            # --- tinh thần ---
            ms = p.get("mentalState_detail")
            if ms:
                extra = f", chất: {ms['chemical']}" if ms.get("chemical") else ""
                add(3 if mine else 2, "Tinh thần",
                    f"{nm} đang trong cơn khủng hoảng `{ms['def']}`{extra} (đã {fmt_duration(ms.get('age'))}"
                    f"{', do tâm trạng thấp' if ms.get('causedByMood') == 'True' else ''}) — không điều khiển/giao việc được.")
            mood = p.get("mood")
            if mine and mood is not None and mood < MOOD_BREAK_MINOR:
                lvl = ("dưới ngưỡng khủng hoảng CỰC ĐOAN 5%" if mood < MOOD_BREAK_EXTREME else
                       "dưới ngưỡng khủng hoảng NẶNG 20%" if mood < MOOD_BREAK_MAJOR else
                       "dưới ngưỡng khủng hoảng nhẹ 35%")
                br = p.get("mentalBreaker") or {}
                add(3 if mood < MOOD_BREAK_MAJOR else 2, "Tinh thần",
                    f"{nm}: tâm trạng {pct(mood)} — {lvl} (ngưỡng gốc vanilla; "
                    f"đã dưới ngưỡng nhẹ {fmt_duration(br.get('ticksBelowMinor', 0))}).")
            # --- nhu cầu ---
            if mine or role in ("guest", "prisoner"):
                for nd in p["needs"]:
                    lv = nd["level"]
                    if lv is None or nd["def"] in ("Mood", "DrugDesire", "Beauty", "RoomSize", "Outdoors"):
                        continue
                    if (nd.get("class") or "") == "Need_Chemical":
                        if lv <= 0.01:
                            add(2, "Nghiện", f"{nm}: nhu cầu `{nd['def']}` = {pct(lv)} → đang VẬT (cai) thuốc.")
                        continue
                    if lv < 0.15:
                        add(2 if nd["def"] in ("Food", "Rest", "Joy") else 1, "Nhu cầu",
                            f"{nm}: {nd['name']} (`{nd['def']}`) chỉ còn {pct(lv)}.")
            # --- sức khỏe ---
            untended = [h for h in p["hediffs"] if h["tend"] == "untended"]
            expired = [h for h in p["hediffs"] if h["tend"] == "expired"]
            if (mine or role in ("guest", "prisoner")) and untended:
                add(3, "Y tế", f"{nm}: {len(untended)} vết thương CHƯA băng: "
                    + ", ".join(f"{h['def']} {h['part_name'] or ''}".strip() for h in untended[:6]) + ".")
            if (mine or role in ("guest", "prisoner")) and expired:
                add(2, "Y tế", f"{nm}: cần chăm sóc lại (lần chăm trước đã hết hiệu lực): "
                    + ", ".join(f"{h['def']} {h['part_name'] or ''} (mức {fmt_num(h['severity'], 3)})".strip()
                                for h in expired[:6]) + ".")
            if mine or role in ("guest", "prisoner"):
                for h in p["hediffs"]:
                    if h["def"] == "BloodLoss" and (h["severity"] or 0) >= 0.3:
                        add(2, "Y tế", f"{nm}: mất máu {pct(h['severity'])}.")
                    if h["class"] == "Hediff_Addiction":
                        dz = h.get("days_to_zero")
                        add(2, "Nghiện", f"{nm}: `{h['def']}` mức {fmt_num(h['severity'], 3)}"
                            + (f" — tự hết sau ~{dz} ngày nếu không dùng lại" if dz else "") + ".")
                if p.get("healthState") != "Mobile":
                    add(3, "Y tế", f"{nm} đang ở trạng thái `{p['healthState']}` (gục/không đi được).")
            if role == "guest":
                add(1, "Khách", f"{nm} ({p['faction_name']}) là KHÁCH đang ở căn cứ"
                    + (f", đang nằm giường tại {fmt_pos(p['pos'])}" if (p.get('job') or {}).get('posture') == 'LayingInBed' else "")
                    + f"; quest tag: {', '.join(p['questTags']) or '—'}.")
            if role == "prisoner":
                add(1, "Tù nhân", f"{nm} là tù nhân (resistance {fmt_num((p['guest'] or {}).get('resistance'))}).")
            if role == "hostile":
                add(3, "Đe doạ", f"Kẻ địch {nm} ({p['faction_name']}) đang trên map tại {fmt_pos(p['pos'])}, "
                    f"cách căn cứ {fmt_rel(mp, p['pos'])}.")
            if role == "colonist":
                if not p.get("ownedBed"):
                    add(1, "Chỗ ở", f"{nm} chưa được gán giường riêng (ownedBed = null).")
                if not p.get("equipment"):
                    stock = [it for it in mp["items"] if not it.get("fogged")
                             and it["def"].startswith(("Gun_", "MeleeWeapon_", "Bow_", "Weapon_"))]
                    last = None                 # vũ khí người này dùng gần nhất theo nhật ký chiến đấu
                    for b in state.get("battle_log") or []:
                        for x in b["exchanges"]:
                            if x["from"] == "Thing_" + p["id"] and x["weapon"] and (last is None or (x["last_tick"] or 0) >= last[0]):
                                last = ((x["last_tick"] or 0), x["weapon"])
                    danger = any(a.get("mentalState") for a in mp["animals"]) or any(
                        q.get("role") == "hostile" for q in mp["pawns"])
                    add(2 if danger else 1, "Vũ trang",
                        f"{nm} đang KHÔNG cầm vũ khí nào"
                        + (f" (lần giao tranh gần nhất dùng `{last[1]}`, lúc {save.fmt_tick(last[0])})" if last else "")
                        + (". Vũ khí đang nằm trên map: " + "; ".join(
                            f"`{it['def']}`" + (f" [{it['quality']}]" if it.get("quality") else "") + f" tại {fmt_pos(it['pos'])}"
                            + (f" trong «{it['zone']}»" if it.get("zone") else "")
                            + (" — đang bị CẤM (forbidden), phải bỏ cấm mới nhặt được" if it.get("forbidden") == "True" else "")
                            for it in stock) if stock else ". Trên map không có vũ khí rời nào")
                        + ("; trên map đang có thú điên/kẻ địch." if danger else "."))
                if not ms and p.get("healthState") == "Mobile":
                    able.append(p)

        # --- đe doạ thù địch trên map ---
        for lord in mp["lords"]:
            if lord["faction_relation"] != "Hostile":
                continue
            poss = [x["pos"] for x in lord["pawns"] if x["pos"]]
            kinds = Counter(x["def"] for x in lord["pawns"])
            center = (round(sum(p[0] for p in poss) / len(poss)), round(sum(p[1] for p in poss) / len(poss))) if poss else None
            dormant = "Sleep" in (lord["job_class"] or "")
            add(2 if dormant else 3, "Đe doạ",
                f"Nhóm thù địch `{lord['job_class']}` ({lord['faction_name']}): "
                + ", ".join(f"{k}×{v}" for k, v in kinds.items())
                + (f" quanh {fmt_pos(center)}, cách căn cứ {fmt_rel(mp, center)}" if center else "")
                + (" — đang NGỦ ĐÔNG, sẽ thức và tấn công khi bị đánh động"
                   + (" / khi có pawn làm lộ vùng sương mù ở đó" if lord["job_fields"].get("wakeOnPawnUnfogged") == "True" else "")
                   if dormant else " — ĐANG HOẠT ĐỘNG") + ".")
        loose = [m for m in mp["mechs"] if m["faction_relation"] == "Hostile" and not m["lord"]]
        if loose:
            add(3, "Đe doạ", "Mech thù địch không thuộc nhóm nào: "
                + ", ".join(f"{m['def']}@{fmt_pos(m['pos'])}" for m in loose[:8]) + ".")
        crazed = defaultdict(list)
        for a in mp["animals"]:
            if a.get("mentalState"):
                crazed[(a["def"], a["mentalState"])].append(a)
        friendly = [p for p in mp["pawns"] if p.get("role") in ("colonist", "slave", "guest", "prisoner") and p.get("pos")]
        for (adef, mstate), lst in crazed.items():
            spots = []
            for a in sorted(lst, key=lambda a: rel_to_base(mp, a["pos"])[0] or 0):
                near = min(friendly, key=lambda p: math.hypot(p["pos"][0] - a["pos"][0], p["pos"][1] - a["pos"][1]), default=None) if a.get("pos") else None
                spots.append(f"{fmt_pos(a['pos'])} (cách tâm căn cứ {fmt_rel(mp, a['pos'])}"
                             + (f"; người gần nhất: {near['nick'] or near['name']}, cách "
                                f"{round(math.hypot(near['pos'][0] - a['pos'][0], near['pos'][1] - a['pos'][1]))} ô" if near else "")
                             + (f"; job `{a['job']}`" if a.get("job") else "") + ")")
            hunting = "Manhunter" in mstate
            add(3, "Đe doạ", f"`{adef}` ×{len(lst)} đang ở trạng thái `{mstate}`"
                + (" (thú điên — tấn công mọi người nó thấy)" if hunting else "") + ": " + "; ".join(spots[:10])
                + (f"; … và {len(spots) - 10} con nữa" if len(spots) > 10 else "") + ".")
        for a in mp["animals"]:
            if a["def"] in PREDATOR_DEFS and not a["faction"]:
                dist, _ = rel_to_base(mp, a["pos"])
                if dist is not None and dist <= 40:
                    add(2, "Đe doạ", f"Thú săn mồi hoang `{a['def']}` tại {fmt_pos(a['pos'])}, cách tâm căn cứ {fmt_rel(mp, a['pos'])}; "
                        f"mức thức ăn {fmt_num(a['hunger'], 2)}, {'đang ngủ' if a['asleep'] else 'job ' + str(a['job'])}"
                        + (f", ĐANG NHẮM {a['job_target']}" if a["job"] and "Hunt" in a["job"] else "") + ".")

        # --- lương thực ---
        food = mp.get("food") or {}
        if food.get("eaters"):
            sev = 3 if (food["days_if_cooked"] or 0) < 2 else 2 if (food["days_if_cooked"] or 0) < 5 else 1
            add(sev, "Lương thực",
                f"{food['meals']} suất ăn sẵn + {food['raw_units']} đơn vị nguyên liệu thô cho {food['eaters']} người: "
                f"≈ {food['days_as_is']} ngày nếu ăn nguyên trạng, ≈ {food['days_if_cooked']} ngày nếu nấu hết thành suất đơn giản "
                f"(ước tính theo dinh dưỡng vanilla, {HUMAN_NUTRITION_PER_DAY}/người/ngày).")
            for r in food["rows"]:
                dl = r.get("min_rot_days_left")
                if dl is not None and dl < 2:
                    add(2, "Lương thực", f"`{r['def']}` ×{r['count']}: lô sớm nhất sẽ hỏng sau ~{dl} ngày (ở ≥10°C, không bảo quản lạnh).")
        grow = [z for z in mp["zones"] if "Growing" in z["class"]]
        empty = [z for z in grow if z.get("crop_count") == 0]
        for z in empty:
            add(2, "Trồng trọt", f"Ruộng «{z['label']}» ({z['cell_count']} ô, {fmt_bbox(z['bbox'])}) đặt trồng `{z['plantDefToGrow']}` "
                f"nhưng hiện có 0 cây trồng (có {sum(z['other_plants'].values())} cây dại mọc lẫn).")
        if grow and not workers_of("Growing"):
            add(2, "Trồng trọt", "Có ruộng nhưng không thuộc địa viên nào bật việc Growing.")

        # --- xác chết ---
        near = []
        for c in mp["corpses"]:
            dist, _ = rel_to_base(mp, c["pos"])
            if dist is not None and dist <= 45 and c["rot_stage"] in ("Fresh", "Rotting") and not c["fogged"]:
                near.append((c, dist))
        for c, dist in near:
            if c["rot_stage"] == "Rotting":
                add(2, "Vệ sinh", f"Xác `{c['def']}` «{c['inner_name']}» tại {fmt_pos(c['pos'])} ĐANG THỐI RỮA (toả khí thối → nguy cơ LungRot), cách căn cứ {dist} ô.")
            else:
                add(1, "Vệ sinh", f"Xác tươi `{c['def']}` «{c['inner_name']}» tại {fmt_pos(c['pos'])} (cách tâm căn cứ {dist} ô) sẽ bắt đầu thối sau ~{fmt_duration(c['ticks_to_rot'])} (ở ≥10°C).")
        for r in mp["rooms"]:
            if r["is_base"] and r["corpses"] and r["roofed"]:
                add(1, "Vệ sinh", f"Phòng {r['id']} ({fmt_bbox(r['bbox'])}) trong căn cứ đang chứa xác: "
                    + ", ".join(f"{k}×{v}" for k, v in r["corpses"].items()) + ".")

        # --- việc đang chờ mà không ai làm ---
        desig = Counter(d["def"] for d in mp["designations"])
        by_work = defaultdict(list)
        for dname, cnt in desig.items():
            by_work[DESIGNATION_WORK.get(dname)].append(f"{dname}×{cnt}")
        for wdef, lst in by_work.items():
            if wdef and not workers_of(wdef):
                add(2, "Công việc", f"Có {', '.join(lst)} đang chờ nhưng KHÔNG thuộc địa viên nào bật việc `{wdef}`.")
        if mp["construction"]:
            agg = Counter(c["build_def"] for c in mp["construction"])
            oldest = min((c["spawnedTick"] for c in mp["construction"] if c["spawnedTick"] is not None), default=None)
            add(1 if workers_of("Construction") else 2, "Công việc",
                "Công trình chưa xây: " + ", ".join(f"{k}×{v}" for k, v in agg.items())
                + (f" (bản vẽ cũ nhất đặt {fmt_duration(now - oldest)} trước)" if oldest is not None else "")
                + ("" if workers_of("Construction") else " — KHÔNG ai bật việc Construction") + ".")
        for w in state.get("work_coverage", []):
            if w["def"] in ("Cooking", "Doctor", "Firefighter", "Hauling", "Cleaning", "Construction", "Growing") and not w["workers"]:
                add(2, "Công việc", f"Không thuộc địa viên nào bật việc `{w['def']}` ({w['name']}).")
        if cols and len(able) < len(cols):
            add(2, "Nhân lực", f"Chỉ {len(able)}/{len(cols)} thuộc địa viên đang làm việc bình thường được "
                f"(số còn lại đang khủng hoảng tinh thần hoặc gục).")

        # --- điện ---
        power_defs = ("Generator", "SolarGenerator", "WindTurbine", "Battery", "GeothermalGenerator", "WatermillGenerator")
        has_power = any(any(k in b["def"] for k in power_defs) for b in mp["buildings_player"])
        if not has_power and "Electricity" in (state["research"].get("completed") or []):
            add(1, "Hạ tầng", "Đã nghiên cứu Electricity nhưng chưa có máy phát/pin nào được xây xong.")

        # --- nhiệt độ ---
        gsum = mp.get("grids") or {}
        hot = [r for r in mp["rooms"] if r["is_base"] and r.get("temperature") is not None and r["beds"]]
        slept_heat = [p["nick"] for p in cols if any(t["def"] == "SleptInHeat" for t in p["thoughts"])]
        slept_cold = [p["nick"] for p in cols if any(t["def"] == "SleptInCold" for t in p["thoughts"])]
        rt = state["game"].get("recent_temperature") or {}
        if slept_heat:
            add(1, "Nhiệt độ", f"{', '.join(slept_heat)} có ký ức `SleptInHeat` (ngủ nơi nóng). Ngoài trời hiện {gsum.get('outdoor_temp')}°C"
                + (", phòng có giường: " + ", ".join(f"{r['id']} {r['temperature']}°C" for r in hot) if hot else "")
                + (f"; nhưng {rt['days']} ngày qua ban ngày lên tới {rt['outdoor_max']['temp']}°C ngoài trời ({rt['outdoor_max']['date']})"
                   if rt.get("outdoor_max") else "")
                + (f" và {rt['indoor_max']['temp']}°C trong phòng ({rt['indoor_max']['date']})" if rt.get("indoor_max") else "") + ".")
        if slept_cold:
            add(1, "Nhiệt độ", f"{', '.join(slept_cold)} có ký ức `SleptInCold` (ngủ nơi lạnh).")

        # --- khí ---
        for gname, gv in (gsum.get("gas") or {}).items():
            bb = gv["bbox"]
            centre = ((bb[0] + bb[1]) // 2, (bb[2] + bb[3]) // 2)
            add(2 if gname in ("ToxGas", "DeadlifeDust") else 1, "Môi trường",
                f"`{gname}` ({GAS_VI.get(gname, gname)}) đang phủ {gv['cells']} ô trong {fmt_bbox(bb)}; "
                f"tâm vùng khí so với tâm căn cứ: {fmt_rel(mp, centre)}.")

        # --- vật phẩm đáng chú ý ngoài kho ---
        loose_val = Counter()
        for it in mp["items"]:
            if not it["zone"] and not it.get("fogged") and it.get("forbidden") != "True":
                loose_val[it["def"]] += it["stackCount"]
        if loose_val:
            add(1, "Kho", "Vật phẩm nằm ngoài mọi vùng kho (chưa bị cấm, không trong sương mù): "
                + ", ".join(f"{k}×{v}" for k, v in loose_val.most_common(8)) + ".")

    # --- nghiên cứu ---
    r = state["research"]
    if r and r.get("all"):
        res_workers = workers_of("Research")
        if not r.get("current"):
            add(1, "Nghiên cứu", "Chưa chọn dự án nghiên cứu nào.")
        elif not res_workers:
            add(2, "Nghiên cứu", f"Đang chọn `{r['current']}` nhưng không ai bật việc Research.")

    # --- nhiệm vụ ---
    for q in state["quests"]:
        if q["state"] == "NotYetAccepted" and not q["hidden"]:
            left = q["ticksUntilOfferExpires"]
            links = [f"{x['name']} {l}" for x in q["pawns"] for l in x.get("links", [])]
            add(2 if left is not None and left < 3 * TICKS_PER_DAY else 1, "Nhiệm vụ",
                f"«{q['name']}» (`{q['root']}`) chưa nhận" + (f" — hết hạn nhận sau {fmt_duration(left)}" if left is not None else "")
                + (" — có người quen: " + "; ".join(links) if links else "") + ".")
        elif q["state"] == "Ongoing" and not q["hidden"]:
            add(1, "Nhiệm vụ", f"«{q['name']}» đang diễn ra"
                + (" — thành công khi có tín hiệu: " + ", ".join(quest_signals(q, "Success")) if quest_signals(q, "Success") else "") + ".")

    # --- thư chưa đọc ---
    unread = [x for x in state["letters"] if x.get("unread")]
    if unread:
        add(1, "Thư", "Thư còn treo trên màn hình (chưa đóng): " + "; ".join(f"«{x['label']}» ({x['date']})" for x in unread) + ".")

    # --- lịch ---
    if date.get("ticks_to_next_quadrum") is not None and date["ticks_to_next_quadrum"] < 2 * TICKS_PER_DAY:
        nxt = date.get("next_season")
        add(1, "Lịch", f"Còn {fmt_duration(date['ticks_to_next_quadrum'])} nữa sang quý {date['next_quadrum']}"
            + (f" (mùa {SEASON_VI.get(nxt, nxt)} — suy luận theo bán cầu {date['hemisphere']})" if nxt else "") + ".")

    A.sort(key=lambda a: -a["sev"])
    return A


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
        return "\n".join(self.lines).strip("\n") + "\n"


def render_markdown(save: SaveFile, state: dict) -> str:
    """report.md — bản đầy đủ nhất (mọi bảng, mọi dòng). Bản cô đọng cho AI: ai_state.md."""
    d = Doc()
    g = state["game"]
    date = g["date"]
    d.h(1, f"RIMWORLD SAVE DUMP — {save.path.name}")
    m0 = state["maps"][0] if state["maps"] else None
    d.p(f"*Sinh tự động bởi `rimworld_dump.py` · phiên bản game `{state['meta']['gameVersion']}` · "
        f"{date['display']} · {date['days_played']} ngày đã chơi · "
        f"{sum(len(m['pawns']) for m in state['maps'])} pawn người · "
        + (f"map {m0['size'][0]}×{m0['size'][1]}" if m0 and m0.get("size") else "không rõ kích thước map") + "*")
    d.p("> Muốn đưa cho AI đọc nhanh: dùng **`ai_state.md`** (cô đọng, có cảnh báo + sơ đồ). "
        "File này là bản đầy đủ từng dòng để tra cứu.")

    d.h(2, "Mục lục")
    d.p("★. Cảnh báo tự động\n0. Nguồn & mod\n1. Tổng quan game\n2. Thế giới & phe\n3. Tôn giáo\n4. Nghiên cứu\n"
        "5. PAWN (đầy đủ) + ma trận công việc\n6. Động vật, mech & nhóm AI\n7. Công trình, phòng, sơ đồ\n"
        "8. Môi trường / địa hình / quặng / khu vực / rác\n9. Vùng (zone)\n10. Vật phẩm trên map\n"
        "11. Cây trồng & thảm thực vật\n12. Đánh dấu (designations)\n13. Xác chết\n14. Nhật ký / thư / sự kiện\n"
        "15. Nhiệm vụ\n16. Anomaly\n17. Pawn ngoài map\n18. Kiểm tra độ phủ\n19. Số liệu lịch sử & chính sách\n"
        "20. File dữ liệu kèm theo")

    d.h(2, "★. Cảnh báo tự động")
    d.p("*Tự rà từ dữ liệu theo quy tắc; ngưỡng tâm trạng 35/20/5% là ngưỡng gốc vanilla.*")
    block_alerts(d, state)

    # 0
    d.h(2, "0. Nguồn & mod")
    d.kv([
        ("File", f"`{state['source']['file']}`"),
        ("Kích thước", f"{state['source']['size_bytes']:,} bytes"),
        ("SHA-1", state["source"]["sha1"]),
        ("Game version", state["meta"]["gameVersion"]),
        ("Mods", "<br>".join(state["meta"]["modNames"])),
        ("Mod IDs", "<br>".join(state["meta"]["modIds"])),
    ])

    # 1
    d.h(2, "1. Tổng quan game")
    d.kv([
        ("Ngày giờ trong game", f"{date['display']} (ngày {date['day_of_year']}/60 của năm)"),
        ("Mùa (game ghi)", f"{date['season']} — bán cầu {date['hemisphere'] or '?'} (suy luận)"),
        ("Múi giờ địa phương", f"UTC{date['timezone']:+d} (nguồn: {date['tz_source']})"),
        ("Tick", f"{g['ticksGame']:,} ({date['days_played']} ngày); gameStartAbsTick {save.game_start_abs:,}"),
        ("Ván bắt đầu", save.fmt_tick(0)),
        ("Tên thuộc địa / phe", f"{g.get('colonyName')} / {g.get('playerFaction')}"),
        ("Kịch bản", g["scenario"]["name"]),
        ("Tóm tắt", g["scenario"]["summary"] or ""),
        ("Mô tả", (g["scenario"]["description"] or "").replace("\n", "<br>")),
        ("Các phần kịch bản", ", ".join(f"{p['def']}" for p in g["scenario"]["parts"])),
        ("Người kể chuyện", g["storyteller"]),
        ("Độ khó", g["difficulty"]),
        ("Ưu tiên công việc thủ công", g["playSettings"]["useWorkPriorities"]),
        ("Số vụ đột kích", g["storyWatcher"]["numRaidsEnemy"]),
        ("Số mối đe dọa đã xếp hàng (thống kê)", g["storyWatcher"]["numThreatsQueued"]),
        ("Đột kích / đe doạ lớn", last_threat_line(save, state)),
        ("Sự cố gần nhất của người kể chuyện", save.fmt_tick(g.get("lastIncidentTick"))),
        ("Thư chưa đóng", ", ".join(g.get("unreadLetters") or []) or "—"),
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
        ("Tổng world object", w["objects"]["total"]),
    ])
    d.h(3, "Các phe")
    settle = {x["faction"]: x["count"] for x in w["objects"]["settlements_by_faction"]}
    rows = []
    for f in w["factions"]:
        rel = {r["other"]: r for r in f["relations"]}
        player = rel.get(save.player_faction) or {}
        rows.append([
            f["id"], f["name"], f["def"],
            player.get("kind", "—"), player.get("goodwill", "—"),
            settle.get(f["id"], 0), f.get("leader_name") or "—",
            "CÓ" if f["player"] else "",
            ", ".join(x for x in ("ẩn" if f.get("hidden") else "", "tạm thời" if f.get("temporary") else "",
                                  "đã bị diệt" if f.get("defeated") else "") if x),
        ])
    d.table(["ID", "Tên", "Def", "Quan hệ với bạn", "Thiện chí", "Số khu định cư", "Thủ lĩnh",
             "Phe người chơi", "Ghi chú"], rows)
    d.h(3, "Điểm đặc biệt trên bản đồ thế giới")
    d.table(["Lớp", "Def", "Ô", "Tên", "Phe", "Quest tag", "Khác"],
            [[o["class"], o["def"], o["tile"], o["name"] or "—", o["faction"] or "—",
              ", ".join(o["questTags"]), ", ".join(f"{k}={v}" for k, v in o["extra"].items())]
             for o in w["objects"]["special"]])

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
    d.p("*Save chỉ lưu SỐ ĐIỂM đã tích luỹ, không lưu chi phí hay cờ hoàn thành. Dự án có điểm là số nguyên tròn "
        "(game gán điểm = chi phí khi xong) và không phải dự án đang chọn được coi là ĐÃ XONG — suy luận, độ tin cậy cao.*")
    cur = r.get("current")
    d.p(f"**Đang nghiên cứu:** " + (f"`{cur}` ({RESEARCH_VI.get(cur, pretty_def(cur))}) — đã có "
                                   f"{fmt_num(r.get('current_points') or 0, 1)} điểm" if cur else "chưa chọn"))
    d.h(3, f"Đã hoàn thành ({len(r['completed'])})")
    pts = {x["def"]: x["progress"] for x in r["all"]}
    d.table(["Def", "Tên", "Điểm (= chi phí)"],
            [[k, RESEARCH_VI.get(k, pretty_def(k)), fmt_num(pts.get(k), 1)] for k in r["completed"]])
    if r["partial"]:
        d.h(3, "Đang làm dở")
        d.table(["Def", "Điểm đã có"], [[p["def"], fmt_num(p["progress"], 1)] for p in r["partial"]])
    status_vi = {"done": "xong", "partial": "dở dang", "in_progress": "ĐANG CHỌN", "none": ""}
    d.h(3, f"Toàn bộ bảng nghiên cứu ({len(r['all'])})")
    d.table(["Def", "Tên", "Điểm", "Trạng thái"],
            [[x["def"], x["name"], fmt_num(x["progress"], 1), status_vi.get(x["status"], x["status"])] for x in r["all"]])
    if r.get("anomaly_knowledge"):
        d.p("Kiến thức Anomaly: " + ", ".join(f"`{k}` {v}" for k, v in r["anomaly_knowledge"].items()))

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
    d.h(3, "Ma trận công việc")
    d.p("Số = mức ưu tiên (1 cao nhất), `·` = tắt; `kn` = cấp kỹ năng liên quan.")
    block_work_matrix(d, state)

    # 6 animals + mechs + lords
    d.h(2, "6. Động vật, mech & nhóm AI trên map")
    for mp in state["maps"]:
        d.h(3, f"Map {mp['index']} — {len(mp['animals'])} động vật · {len(mp['mechs'])} mech · {len(mp['lords'])} lord")
        d.h(4, "Động vật")
        d.table(["ID", "Loài", "Tên", "Giới", "Tuổi", "Phe", "Ô", "Thức ăn", "Job", "Ngủ", "Tinh thần", "Hediff", "Cách căn cứ"],
                [[a["id"], a["def"], a["name"] or "—", a["gender"], a["age_bio"],
                  a["faction_name"], fmt_pos(a["pos"]), fmt_num(a["hunger"], 2), a["job"] or "—",
                  "có" if a["asleep"] else "", a["mentalState"] or "",
                  ", ".join(sorted(set(h["def"] for h in a["hediffs"]))), fmt_rel(mp, a["pos"])]
                 for a in mp["animals"]])
        if mp["mechs"]:
            d.h(4, "Mechanoid")
            d.table(["ID", "Loại", "Phe", "Quan hệ", "Ô", "Ngủ đông", "Job", "Duty", "Lord", "Sương mù", "Cách căn cứ"],
                    [[m["id"], m["def"], m["faction_name"], m["faction_relation"], fmt_pos(m["pos"]),
                      "có" if m["dormant"] else "không", m["job"] or "—", m["duty"] or "—", m["lord"] or "—",
                      "có" if m.get("fogged") else "", fmt_rel(mp, m["pos"])] for m in mp["mechs"]])
        if mp["lords"]:
            d.h(4, "Lord (nhóm pawn do AI điều khiển chung)")
            d.table(["Lord", "Phe", "Quan hệ", "Kiểu hành vi", "Tham số", "Thành viên", "Toil", "Tick trong toil"],
                    [[lo["id"], lo["faction_name"], lo["faction_relation"], lo["job_class"],
                      ", ".join(f"{k}={v}" for k, v in lo["job_fields"].items()),
                      "; ".join(f"{x['ref']} {fmt_pos(x['pos'])}" for x in lo["pawns"]),
                      lo["curLordToilIdx"], lo["ticksInToil"]] for lo in mp["lords"]])

    # 7 buildings
    d.h(2, "7. Công trình, phòng, sơ đồ")
    for mp in state["maps"]:
        md = save.maps[mp["index"]]
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
        d.p("**Chi tiết từng công trình:** (cột «Xoay»: 0 Bắc, 1 Đông, 2 Nam, 3 Tây; trống = 0)")
        d.w()
        mp["buildings_player"].sort(key=lambda b: (b["def"], b["pos"] or (0, 0)))
        rows = []
        for b in mp["buildings_player"]:
            ex = b["extra"]
            extra = []
            if ex.get("bills"):
                extra.append("bill: " + "; ".join(fmt_bill(x) for x in ex["bills"]))
            if ex.get("contents"):
                extra.append("chứa: " + ", ".join(
                    f"{label(c['def'], ITEMS)}×{c['stackCount']}" for c in ex["contents"]))
            if ex.get("assignedPawns") is not None:
                extra.append("gán cho: " + (", ".join(o["name"] for o in ex["assignedPawns"]) or "chưa ai"))
            if ex.get("inner"):
                extra.append("bên trong: " + fmt_inner(ex["inner"]))
            for k, v in ex.items():
                if k not in ("bills", "contents", "assignedPawns", "inner"):
                    extra.append(f"{k}={v}")
            rows.append([
                b["id"], b["name"], f"`{b['def']}`", fmt_pos(b["pos"]),
                b["stuff"] or "—", b["quality"] or "—",
                f"{fmt_num(b['health'])}", b["rot"] or "",
                "; ".join(extra),
            ])
        d.table(["ID", "Tên", "Def", "Ô", "Vật liệu", "Phẩm chất", "HP", "Xoay", "Ghi chú"], rows)

        d.h(4, f"Bản vẽ / khung chưa xây ({len(mp['construction'])})")
        d.table(["ID", "Loại", "Sẽ xây", "Ô", "Xoay", "Vật liệu", "Đặt lúc", "Công đã làm", "Đã có trong khung"],
                [[c["id"], c["kind"], f"`{c['build_def']}`", fmt_pos(c["pos"]), c["rot"] or "", c["stuff"] or "—",
                  save.fmt_tick(c["spawnedTick"]), fmt_num(c["workDone"]),
                  ", ".join(f"{x['def']}×{x['stackCount']}" for x in c["contents"])] for c in mp["construction"]])

        d.h(4, f"Phòng / vùng kín ({len(mp['rooms'])})")
        d.p("*Game không lưu phòng; công cụ tự loang tìm vùng bị tường/đá/cửa bao kín trên toàn map. "
            "Vùng không chạm công trình/zone/khu Home của bạn được xếp là «khác».*")
        block_rooms(d, mp)

        d.h(4, f"Công trình khác / cổ ({len(mp['buildings_other'])})")
        grouped = OrderedDict()
        for b in mp["buildings_other"]:
            grouped.setdefault((b["def"], b["name"]), []).append(b)
        rows = []
        for (defn, nm), lst in sorted(grouped.items(), key=lambda kv: -len(kv[1])):
            poss = ", ".join(f"({b['pos'][0]},{b['pos'][1]})" for b in lst[:8] if b["pos"])
            if len(lst) > 8:
                poss += f" … (+{len(lst) - 8})"
            inner = "; ".join(f"{fmt_pos(b['pos'])}: {fmt_inner(b['extra']['inner'])}" for b in lst if b["extra"].get("inner"))
            fog = sum(1 for b in lst if b.get("fogged"))
            rows.append([nm, f"`{defn}`", len(lst), poss, f"{fog}/{len(lst)}" if fog else "", inner])
        d.table(["Tên", "Def", "SL", "Vị trí (tối đa 8)", "Trong sương mù", "Bên trong"], rows)

        d.h(4, "Sơ đồ khu căn cứ")
        text, note = ascii_base_map(save, md, mp)
        d.p("```\n" + text + "\n```")
        d.p(note)

    # 8 environment
    d.h(2, "8. Môi trường, địa hình, quặng, khu vực (area), rác")
    for mp in state["maps"]:
        md = save.maps[mp["index"]]
        gs = mp.get("grids") or {}
        d.h(3, f"Map {mp['index']}")
        d.kv([
            ("Kích thước", f"{mp['size'][0]} × {mp['size'][1]}" if mp["size"] else "—"),
            ("Biome", state["world"].get("biome") or "—"),
            ("Thời tiết", mp["weather"]),
            ("Thời tiết trước", mp["weather_last"]),
            ("Tuổi thời tiết (tick)", mp["weather_age"]),
            ("Nhiệt độ ngoài trời", f"{gs.get('outdoor_temp')}°C" if gs.get("outdoor_temp") is not None else "—"),
            ("Điều kiện đang hoạt động", ", ".join(
                f"{clean(c['def'])}" + (f" ({c['class']})" if c['class'] else "")
                for c in mp["conditions"]) or "—"),
            ("Ô còn sương mù", gs.get("fogged_cells")),
            ("Ô nhiễm / tuyết", f"{gs.get('polluted_cells') or 0} ô ô nhiễm; tuyết: {'có' if gs.get('snow') else 'không'}"),
            ("Khí đang lơ lửng", gas_line(gs)),
            ("Tài nguyên sâu đã dò ra (cho khoan sâu)", deep_line(gs)),
            ("Tâm căn cứ / bao tường", f"{fmt_pos(mp.get('base_center'))} / {fmt_bbox(mp.get('base_bbox'))}"),
            ("Đường cổ cắt mép map", ", ".join(fmt_pos(p) for p in mp["roads_edge_cells"]) or "—"),
        ])
        d.h(4, "Sự cố gần nhất theo loại (storyState của map)")
        d.table(["Sự cố", "Lúc", "Tick"],
                [[x["incident"], save.fmt_tick(x["tick"]), x["tick"]] for x in mp["story"]["lastIncidents"]])
        d.h(4, "Khu vực (areas)")
        d.table(["Lớp", "ID", "Nhãn", "Số ô", "Bao"],
                [[a["class"], a["id"], a["label"] or "", a["trueCount"], fmt_bbox(a.get("bbox"))] for a in mp["areas"]])
        if gs:
            d.h(4, "Địa hình (giải mã từ terrainGrid)")
            d.table(["Def", "Tên", "Số ô"], [[k, TERRAIN_VI.get(k, ""), v] for k, v in gs["terrain"].items()])
            d.h(4, "Mái (roofGrid)")
            d.table(["Def", "Tên", "Số ô"], [[k, ROOF_VI.get(k, ""), v] for k, v in gs["roof"].items()])
            d.h(4, "Vách đá / quặng / đá vụn lưu dạng nén (compressedThingMap)")
            d.table(["Def", "Số ô", "Khớp mã băm"],
                    [[k, v, "gần đúng (+va chạm)" if k in gs["hash_inexact"] else "chính xác"] for k, v in gs["rock"].items()])
        d.h(4, f"Mạch quặng ({len(mp['ores'])})")
        d.table(["Quặng", "Số ô", "Bao", "Tâm", "Cách căn cứ", "Ô còn sương mù", "Ô đã đánh dấu đào"],
                [[o["def"], o["cells"], fmt_bbox(o["bbox"]), fmt_pos(o["center"]),
                  f"{o['dist']} ô {o['bearing']}" if o["dist"] is not None else "—",
                  o["fogged_cells"], o["designated_cells"]] for o in mp["ores"]])
        if mp["mineables"]:
            d.h(4, f"Đá/quặng đã bị đào dở hoặc hư hại (lưu rời, {len(mp['mineables'])})")
            d.table(["Def", "ID", "Ô", "HP", "yieldPct"],
                    [[m["def"], m["id"], fmt_pos(m["pos"]), fmt_num(m["health"]), fmt_num(m["yieldPct"], 2)] for m in mp["mineables"]])
        d.h(4, "Vùng nước")
        d.table(["Ô gốc", "Số ô", "Loại", "Quần thể cá", "Có cá", "Cá thường gặp"],
                [[fmt_pos(wb["rootCell"]), wb["cells"], wb["fishType"], fmt_num(wb["population"], 1),
                  "có" if wb["shouldHaveFish"] else "không", ", ".join(wb["commonFish"] + wb["uncommonFish"])]
                 for wb in mp["water_bodies"]])
        d.h(4, "Toàn cảnh map")
        text, note = ascii_overview_map(save, md, mp)
        d.p("```\n" + text + "\n```")
        d.p(note)
        d.h(4, f"Rác/bẩn ({sum(mp['filth'].values())})")
        d.table(["Def", "SL"], [[k, v] for k, v in sorted(mp["filth"].items(), key=lambda kv: -kv[1])])
        if mp["chunks"]:
            d.h(4, f"Khối đá/đống đổ nát lưu rời ({sum(mp['chunks'].values())})")
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
            if "Growing" in z["class"]:
                pairs += [
                    ("Số cây trồng hiện có", z.get("crop_count")),
                    ("Độ lớn (min / TB / max)", f"{pct(z.get('crop_growth_min'))} / {pct(z.get('crop_growth_avg'))} / {pct(z.get('crop_growth_max'))}"),
                    ("Cây đã chín", z.get("crop_mature")),
                    ("Cây dại mọc lẫn", ", ".join(f"{k}×{v}" for k, v in (z.get("other_plants") or {}).items()) or "—"),
                    ("Đất", ", ".join(f"{k}×{v}" for k, v in (z.get("soil") or {}).items()) or "—"),
                    ("Cho phép gieo / cắt", f"{z['allowSow']} / {z['allowCut']}"),
                ]
            else:
                pairs += [
                    ("Ô đang có đồ", f"{z.get('occupied_cells')}/{z['cell_count']}"),
                    ("Ô có mái", z.get("roofed_cells")),
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

    # 10 items
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
        food = mp.get("food") or {}
        if food.get("rows"):
            d.p(f"**Lương thực cho người** *(ước tính theo dinh dưỡng vanilla; gồm cả đồ trong túi thuộc địa viên)*: "
                + ", ".join(f"`{x['def']}`×{x['count']} (={x['nutrition']})" for x in food["rows"])
                + f" → {food['nutrition_total_as_is']} dinh dưỡng nguyên trạng / {food['nutrition_total_if_cooked']} nếu nấu thành suất đơn giản; "
                  f"{food['eaters']} người cần {food['nutrition_needed_per_day']}/ngày → ≈ {food['days_as_is']}–{food['days_if_cooked']} ngày.")

        d.h(4, f"Từng stack ({len(mp['items'])})")
        d.table(["ID", "Def", "Ô", "SL", "Vật liệu", "Phẩm chất", "HP", "Zone", "Cấm", "Sương mù", "rotProg (tick)", "Còn (ngày) trước khi hỏng"],
                [[i["id"], i["def"], f"({i['pos'][0]},{i['pos'][1]})" if i["pos"] else "—",
                  i["stackCount"], i["stuff"] or "—", i["quality"] or "—",
                  fmt_num(i["health"]), i["zone"] or "—",
                  "CẤM" if i.get("forbidden") == "True" else "", "có" if i.get("fogged") else "",
                  fmt_num(i["rotProg"], 0) if i.get("rotProg") is not None else "",
                  i["rot_days_left"] if i.get("rot_days_left") is not None else ""] for i in mp["items"]])

    # 11 plants
    d.h(2, "11. Cây trồng & thảm thực vật")
    for mp in state["maps"]:
        d.h(3, f"Map {mp['index']}")
        d.h(4, f"Cây do người chơi trồng ({len(mp['plants_sown'])})")
        rows = []
        for p in mp["plants_sown"]:
            rows.append([p["def"], label(p["def"], PLANTS),
                         f"({p['pos'][0]},{p['pos'][1]})" if p["pos"] else "—",
                         pct(p["growth"]), fmt_num(p["health"]),
                         f"{p['age'] / TICKS_PER_DAY:.2f}" if p["age"] else "—", p.get("zone") or "—"])
        d.table(["Def", "Tên", "Ô", "Lớn", "HP", "Tuổi (ngày)", "Zone"], rows)
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

    # 12 designations
    d.h(2, "12. Đánh dấu (designations)")
    for mp in state["maps"]:
        if not mp["designations"]:
            continue
        counts = Counter(x["def"] for x in mp["designations"])
        d.h(3, f"Map {mp['index']} — " + ", ".join(f"{k}: {v}" for k, v in counts.items()))
        d.h(4, "Tổng hợp")
        d.table(["Lệnh", "Mục tiêu", "SL", "Phạm vi", "Gần căn cứ nhất", "Thuộc việc"], designation_summary(mp))
        d.h(4, "Từng lệnh")
        d.table(["Loại", "Mục tiêu", "Def mục tiêu", "Ô"],
                [[x["def"], x["target"], x["target_def"] or "—",
                  f"({x['target_pos'][0]},{x['target_pos'][1]})" if x["target_pos"] else "—"]
                 for x in mp["designations"]])

    # 13 corpses
    d.h(2, "13. Xác chết")
    d.p("*rotProg tính bằng tick: < 150.000 = tươi, 150.000–300.000 = đang thối (toả khí thối), ≥ 300.000 = đã khô "
        "(ngưỡng def vanilla của Corpse_*). Xác mech không có rotProg.*")
    for mp in state["maps"]:
        if not mp["corpses"]:
            continue
        d.table(["Def", "Ô", "Bên trong", "Tên", "Phe", "Zone", "Tình trạng", "rotProg", "Chết lúc", "Cách căn cứ"],
                [[c["def"], f"({c['pos'][0]},{c['pos'][1]})" if c["pos"] else "—",
                  c["inner"] or "—", c["inner_name"] or "—", c.get("inner_faction") or "—", c["zone"] or "—",
                  ROT_STAGE_VI.get(c["rot_stage"], c["rot_stage"]),
                  fmt_num(c["rotProg"], 0) if c["rotProg"] is not None else "—",
                  save.fmt_tick(c["timeOfDeath"]), fmt_rel(mp, c["pos"])]
                 for c in mp["corpses"]])

    # 14 letters
    d.h(2, "14. Nhật ký / thư / sự kiện")
    d.h(3, "Thư & thông báo (theo thời gian)")
    rows = []
    for x in sorted(state["letters"], key=lambda x: (x["tick"] is None, x["tick"] or 0)):
        rows.append([
            x["date"] or "—", x["tick"] if x["tick"] is not None else "",
            x["class"] + (" (chưa đóng)" if x.get("unread") else ""), x["def"] or "—",
            x["label"] or "—", x["text"][:500],
        ])
    d.table(["Lúc", "Tick", "Loại", "Mức", "Tiêu đề", "Nội dung"], rows)
    tales = state.get("tales") or []
    if tales:
        d.h(3, f"Sự kiện đáng nhớ game ghi lại (tale) — {len(tales)}")
        d.table(["Lúc", "Tick", "Loại", "Diễn biến", "Nhiệt độ", "Loại phòng", "Ấn tượng phòng"],
                [[t["date"], t["tick"], t["def"], tale_sentence(t),
                  fmt_num((t["surroundings"] or {}).get("temperature"), 1) if t["surroundings"] else "",
                  (t["surroundings"] or {}).get("roomRole") or "",
                  fmt_num((t["surroundings"] or {}).get("roomImpressiveness"), 1) if t["surroundings"] else ""]
                 for t in tales])
    block_battle_log(d, save, state, level=3)
    block_play_log(d, save, state, level=3, full=True)

    # 15 quests
    d.h(2, "15. Nhiệm vụ")
    if state["quests"]:
        for q in state["quests"]:
            block_quest(d, save, q, level=3)
    else:
        d.p("*(không có nhiệm vụ)*")

    # 16 anomaly
    d.h(2, "16. Anomaly")
    a = state["anomaly"]
    if a:
        d.kv([(k, v) for k, v in a.items()])
    else:
        d.p("*(không có dữ liệu anomaly)*")

    # 17 world pawns
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
        classified = (len(mp["pawns"]) + len(mp.get("pawns_offmap", [])) + len(mp["animals"]) + len(mp["mechs"])
                      + len(mp["buildings_player"]) + len(mp["buildings_other"]) + len(mp["construction"])
                      + len(mp["mineables"]) + len(mp["items"]) + len(mp["plants_sown"])
                      + sum(mp["plants_wild"].values()) + sum(mp["dead_plants"].values())
                      + sum(mp["filth"].values()) + sum(mp["chunks"].values())
                      + len(mp["corpses"]))
        d.kv([
            ("Tổng object trong <things>", total),
            ("Đã phân loại", classified),
            ("Chưa phân loại", len(mp["unclassified"])),
            ("Khớp tổng", "CÓ" if classified + len(mp["unclassified"]) == total else "KHÔNG — cần kiểm tra"),
        ])
        if mp["unclassified"]:
            d.table(["Lớp", "Def", "ID", "Ô"],
                    [[u["class"], u["def"], u["id"],
                      f"({u['pos'][0]},{u['pos'][1]})" if u["pos"] else "—"] for u in mp["unclassified"]])
        gs = mp.get("grids") or {}
        if gs.get("hash_unknown"):
            d.p("Mã băm chưa nhận ra trong các lưới nén: " + ", ".join(f"{k} ({v} ô)" for k, v in gs["hash_unknown"].items()))
        if gs.get("errors"):
            d.p("Lỗi giải mã lưới: " + "; ".join(gs["errors"]))

    # 19 history + policies
    d.h(2, "19. Số liệu lịch sử & chính sách")
    hist = state["history"]
    step = hist.get("interval_ticks")
    d.p(f"Chuỗi số liệu game tự ghi mỗi {fmt_duration(step) if step else '?'}; mẫu cuối tại tick {hist.get('last_sample_tick')}.")
    for name, vals in hist["series"].items():
        d.w(f"- **{name}** ({len(vals)} mẫu): " + ", ".join(fmt_num(v, 1) for v in vals))
    d.w()
    pol = state["policies"]
    for dp in pol["drug"]:
        d.h(4, f"Chính sách thuốc «{dp['label']}» (id {dp['id']})")
        d.table(["Chất", "Dùng giải trí", "Dùng khi nghiện", "Theo lịch", "Chu kỳ (ngày)", "Mang theo"],
                [[e["drug"], "có" if e["allowedForJoy"] else "", "có" if e["allowedForAddiction"] else "",
                  "có" if e["allowScheduled"] else "", fmt_num(e["daysFrequency"]), e["takeToInventory"] or ""] for e in dp["entries"]])
    d.table(["Loại", "ID", "Tên", "Số def cho phép"],
            [["Trang phục", x["id"], x["label"], x["allowed_count"]] for x in pol["outfit"]]
            + [["Ăn uống", x["id"], x["label"], x["allowed_count"]] for x in pol["food"]]
            + [["Đọc sách", x["id"], x["label"], ""] for x in pol["reading"]])

    # 20 files
    d.h(2, "20. File dữ liệu kèm theo")
    d.p("- `ai_state.md` — bản cô đọng để đưa cho AI đọc (cảnh báo, người, căn cứ, kho, đe doạ, nhiệm vụ, dòng thời gian)\n"
        "- `state.json` — toàn bộ state ở trên dạng JSON (đầy đủ, kể cả mọi trường XML của pawn)\n"
        "- `things_all.csv` — mọi object trên map\n"
        "- `plants.csv` — mọi cây\n"
        "- `items.csv` — mọi stack vật phẩm\n"
        "- `buildings.csv` — mọi công trình\n"
        "- `terrain.csv` — địa hình / mái / sương mù / đá của TỪNG ô (giải mã từ lưới nén)\n"
        "- `pawns_skills.csv`, `pawns_needs.csv`, `pawns_work.csv`, `pawns_health.csv`\n"
        "- `zones_cells.csv` — từng ô của từng zone")
    return d.text()


def render_pawn_md(d: Doc, save: SaveFile, pw: dict):
    title = pw["name"] or pw["id"]
    d.h(3, f"{title} — `{pw['id']}`")

    g = pw.get("guest") or {}
    ms = pw.get("mentalState_detail")
    br = pw.get("mentalBreaker") or {}
    d.h(4, "Hồ sơ")
    d.kv([
        ("Def / Kind", f"`{pw['def']}` / `{pw['kindDef']}`"),
        ("Vai trò", ROLE_VI.get(pw.get("role"), pw.get("role"))),
        ("Phe", f"{pw['faction_name']} — quan hệ với bạn: {pw.get('faction_relation') or '—'}"),
        ("Giới tính", pw["gender"]),
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
        ("Thân phận (guest)", "không áp dụng (thuộc địa viên)" if pw.get("role") == "colonist" else
                              f"chủ nhà (hostFaction)={save.faction_name(g.get('hostFaction'))} · guestStatus={g.get('guestStatus') or '—'} · "
                              f"được người của bạn chữa {fmt_num(g.get('timesTendedByPlayer') or 0)} lần"),
        ("Quest tag", ", ".join(pw["questTags"]) or "—"),
        ("Vào map lúc", save.fmt_tick(pw["spawnedTick"]) if pw.get("spawnedTick") else "—"),
        ("Tâm trạng", f"**{pw['mood'] * 100:.1f}%**" + (" ⚠" if pw["mood"] < 0.4 else "") if pw.get("mood") is not None else "—"),
        ("Thời gian liên tục dưới ngưỡng nhẹ / nặng / cực đoan",
         f"{fmt_duration(br.get('ticksBelowMinor', 0))} / {fmt_duration(br.get('ticksBelowMajor', 0))} / {fmt_duration(br.get('ticksBelowExtreme', 0))}"),
        ("Trạng thái sức khỏe (healthState)", pw.get("healthState")),
        ("Med care", clean(pw["medCare"])),
        ("Tự băng bó", clean(pw.get("selfTend"))),
        ("Phản ứng", clean(pw["hostilityResponse"])),
        ("Thứ tự hiển thị", pw["displayOrder"]),
        ("Giường riêng", f"{pw['ownedBed']} @{fmt_pos(pw.get('ownedBed_pos'))}" if pw.get("ownedBed") else "chưa có"),
        ("Điểm thiền", clean(pw.get("meditationSpot"))),
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
    d.p("*Save chỉ lưu thought dạng ký ức; thought tình huống (đau, nghiện, phòng xấu…) do game tính lúc chạy.*")
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
        d.table(["Bệnh/tật", "Def", "Lớp", "Severity", "Bộ phận", "Chăm sóc", "Vĩnh viễn", "Tuổi (ngày)", "Nguồn / ghi chú"],
                [[h["name"], f"`{h['def']}`", h["class"], fmt_num(h["severity"], 3),
                  h["part_name"] or "toàn thân",
                  TEND_VI.get(h["tend"], "—") + (f" ({pct(h['tendQuality'])})" if h["tend"] in ("tended", "expired") and h.get("tendQuality") is not None else ""),
                  h["isPermanent"] or "—",
                  f"{h['age_ticks'] / TICKS_PER_DAY:.2f}" if h["age_ticks"] else "—",
                  "; ".join(x for x in (
                      h.get("combatLog") or ((h.get("source") or "") + ("/" + h["sourceTool"] if h.get("sourceTool") else "")),
                      f"{h['severityPerDay']:+.3f}/ngày" if h.get("severityPerDay") else "",
                      f"hết sau ~{h['days_to_zero']} ngày" if h.get("days_to_zero") is not None else "",
                      f"tự biến mất sau {fmt_duration(h['ticksToDisappear'])}" if h.get("ticksToDisappear") is not None else "",
                      f"do {h['lastInjury']}" if h.get("lastInjury") else "",
                  ) if x)]
                 for h in pw["hediffs"]])
    else:
        d.p("*(khỏe mạnh, không có hediff nào)*")
    if pw.get("immunity"):
        d.p("Miễn dịch: " + ", ".join(f"{i['def']} {pct(i['immunity'])}" for i in pw["immunity"]))

    d.h(4, "Trang bị & hành trang")
    d.table(["Loại", "Def", "Tên", "Vật liệu", "Phẩm chất", "HP", "SL"],
            [["Mặc", f"`{a['def']}`", a["name"], a["stuff"] or "—", a["quality"] or "—", fmt_num(a["health"]), a["stackCount"]]
             for a in pw["apparel"]]
            + [["Cầm", f"`{a['def']}`", a["name"], a["stuff"] or "—", a["quality"] or "—", fmt_num(a["health"]), a["stackCount"]]
               for a in pw["equipment"]]
            + [["Trong túi", f"`{a['def']}`", a["name"], a["stuff"] or "—", a["quality"] or "—", fmt_num(a["health"]), a["stackCount"]]
               for a in pw["inventory"]]
            + [["Đang bê", f"`{a['def']}`", a["name"], a["stuff"] or "—", a["quality"] or "—", fmt_num(a["health"]), a["stackCount"]]
               for a in pw.get("carrying", [])])
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
        ("Lần dùng chất gần nhất", ", ".join(f"{r['drug']} (tick {r['lastTakenTicks']})" for r in pw.get("drug_records", [])) or "—"),
    ])
    if pw["timetable"]:
        d.p("**Lịch 24 giờ:** " + " · ".join(
            f"{i:02d}h:{v}" for i, v in enumerate(pw["timetable"])) + f" — giờ này: **{pw.get('schedule_now')}**")

    d.h(4, "Trạng thái hiện tại")
    job = pw["job"] or {}
    d.kv([
        ("Job", f"`{job.get('def')}` ({job.get('workGiverDef')})" if job.get("def") else "— (đang rảnh)"),
        ("Mục tiêu A", clean(job.get("targetA_desc"))),
        ("Mục tiêu B", clean(job.get("targetB_desc"))),
        ("Số lượng", clean(job.get("count"))),
        ("Driver", clean(job.get("driver"))),
        ("Tư thế / đang ngủ", f"{clean(job.get('posture'))} / {'có' if job.get('asleep') else 'không'}"),
        ("Bắt đầu job lúc", save.fmt_tick(job.get("startTick")) if job.get("startTick") is not None else "—"),
        ("Nhập ngũ (drafted)", "CÓ" if pw.get("drafted") else "không"),
        ("Trạng thái tinh thần", ", ".join(f"{k}={v}" for k, v in ms.items()) if ms else "bình thường"),
        ("Cảm hứng", pw["inspiration"] or "—"),
        ("Tương tác cuối", clean(pw["lastInteraction"])),
    ])
    if pw["relations"]:
        d.h(4, "Quan hệ trực tiếp")
        d.table(["Loại", "Pawn", "Tên"],
                [[r["def"], r["otherPawn"], r["otherPawn_name"]] for r in pw["relations"]])
    if pw.get("opinion_from_memories"):
        d.p("Tổng độ lệch thiện cảm từ ký ức xã hội: " + ", ".join(f"{k} {v:+.1f}" for k, v in pw["opinion_from_memories"].items()))

    if pw.get("raw_fields"):
        d.h(4, f"Toàn bộ trường XML ({len(pw['raw_fields'])})")
        rows = [[f"`{k}`", (v[:160] + "…") if len(v) > 160 else v] for k, v in pw["raw_fields"].items()]
        d.table(["Đường dẫn", "Giá trị"], rows)


# --------------------------------------------------------------------------
# Các khối hiển thị dùng chung cho report.md và ai_state.md
# --------------------------------------------------------------------------

ROLE_VI = {"colonist": "thuộc địa viên", "guest": "khách", "prisoner": "tù nhân",
           "slave": "nô lệ", "hostile": "KẺ ĐỊCH", "other": "người ngoài"}
SEV_VI = {3: "KHẨN", 2: "QUAN TRỌNG", 1: "lưu ý"}
TEND_VI = {"tended": "đã băng/chăm", "expired": "HẾT HẠN chăm — cần chăm lại",
           "untended": "CHƯA băng", None: "—"}
ROT_STAGE_VI = {"Fresh": "tươi", "Rotting": "ĐANG THỐI", "Dessicated": "đã khô", "NoRot": "không phân hủy"}


def who(p):
    return p.get("nick") or p.get("name") or p.get("id")


def compress_timetable(tt):
    """['Sleep','Sleep',...,'Joy'] -> '00–05 Sleep · 06 Meditate · …'."""
    if not tt:
        return "—"
    runs = []
    start = 0
    for i in range(1, len(tt) + 1):
        if i == len(tt) or tt[i] != tt[start]:
            span = f"{start:02d}" if i - 1 == start else f"{start:02d}–{i - 1:02d}"
            runs.append(f"{span} {tt[start]}")
            start = i
    return " · ".join(runs)


def skill_line(p):
    star = {"Minor": "★", "Major": "★★"}
    return " · ".join(f"{s['def']} {fmt_num(s['level'])}{star.get(s['passion'], '')}" for s in p["skills"])


def work_line(p):
    if not p["work_priorities"]:
        return "— (không có bảng ưu tiên: không phải thuộc địa viên)"
    groups = defaultdict(list)
    for w in p["work_priorities"]:
        groups[w["value"]].append(w["def"])
    bits = [f"**{k}**: {', '.join(groups[k])}" for k in sorted(k for k in groups if k)]
    if groups.get(0):
        bits.append(f"tắt (0): {', '.join(groups[0])}")
    return " · ".join(bits)


def status_line(p):
    job = p.get("job") or {}
    if p.get("mentalState"):
        base = f"KHỦNG HOẢNG `{p['mentalState']}`"
        if job.get("def"):
            base += f" (job `{job['def']}`)"
        return base
    if p.get("healthState") and p["healthState"] != "Mobile":
        return f"GỤC (`{p['healthState']}`)"
    if not job.get("def"):
        return "rảnh (không có job)"
    s = f"`{job['def']}`"
    if job.get("asleep"):
        s += " — đang ngủ"
    elif job.get("posture") == "LayingInBed":
        s += " — nằm trên giường (thức)"
    if job.get("targetA") and job["targetA"] not in ("null", "None"):
        s += f" → {job['targetA_desc']}"
    if job.get("targetB_pawn"):
        s += f" (đối tượng: {job['targetB_pawn']})"
    if p.get("drafted"):
        s += " [ĐANG NHẬP NGŨ]"
    return s


def gear_line(lst):
    out = []
    for a in lst:
        s = a["def"]
        extra = [x for x in (a.get("stuff"), a.get("quality")) if x]
        if extra:
            s += f" ({', '.join(extra)})"
        if (a.get("stackCount") or 1) > 1:
            s += f" ×{a['stackCount']}"
        out.append(s)
    return ", ".join(out) or "—"


def hediff_rows(p):
    rows = []
    for h in p["hediffs"]:
        tend = TEND_VI.get(h["tend"], "—")
        if h["tend"] in ("tended", "expired") and h.get("tendQuality") is not None:
            tend += f" ({pct(h['tendQuality'])})"
        notes = []
        if h.get("isPermanent") == "True":
            notes.append("vĩnh viễn")
        if h.get("source"):
            notes.append("do " + h["source"] + (f"/{h['sourceTool']}" if h.get("sourceTool") else ""))
        if h.get("lastInjury"):
            notes.append(f"vì {h['lastInjury']}")
        if h.get("days_to_zero") is not None:
            notes.append(f"giảm {fmt_num(-h['severityPerDay'], 3)}/ngày → hết sau ~{h['days_to_zero']} ngày")
        elif h.get("severityPerDay"):
            notes.append(f"{'+' if h['severityPerDay'] > 0 else ''}{fmt_num(h['severityPerDay'], 3)}/ngày")
        if h.get("ticksToDisappear") is not None:
            notes.append(f"tự hết sau {fmt_duration(h['ticksToDisappear'])}")
        if h.get("level") is not None:
            notes.append(f"cấp {h['level']}")
        age = f"{h['age_ticks'] / TICKS_PER_DAY:.1f}" if h.get("age_ticks") else "—"
        rows.append([f"`{h['def']}`", h["part_name"] or "toàn thân", fmt_num(h["severity"], 2), tend, age, "; ".join(notes)])
    return rows


def thought_line(p):
    bits = []
    for t in p["thoughts"]:
        s = f"`{t['def']}`"
        if t.get("otherPawn_name"):
            s += f"→{t['otherPawn_name']}"
        extra = []
        if t.get("opinionOffset") is not None:
            extra.append(f"thiện cảm {t['opinionOffset']:+.0f}")
        if t.get("age_ticks") is not None:
            extra.append(f"{t['age_ticks'] / TICKS_PER_DAY:.1f} ngày trước")
        if extra:
            s += f" ({', '.join(extra)})"
        bits.append(s)
    return " · ".join(bits) or "—"


def block_alerts(d, state):
    alerts = state.get("alerts") or []
    if not alerts:
        d.p("*(không phát hiện điều gì bất thường theo các quy tắc kiểm tra)*")
        return
    for a in alerts:
        d.w(f"- **[{SEV_VI[a['sev']]}] {a['cat']}** — {a['text']}")
    d.w()


def block_people_detail(d, save, p, level=3):
    now = save.ticks_game
    nm = who(p)
    d.h(level, f"{nm} — `{p['id']}` ({ROLE_VI.get(p.get('role'), p.get('role'))})")
    traits = ", ".join(t["def"] + (f"({t['degree']:+d})" if isinstance(t["degree"], int) else "") for t in p["traits"]) or "—"
    g = p.get("guest") or {}
    lines = [
        f"- **Danh tính:** {p['name']} · {p['gender']} · {fmt_num(p['age_bio'], 1)} tuổi (niên đại {fmt_num(p['age_chrono'], 0)}) · "
        f"phe {p['faction_name']} · kind `{p['kindDef']}` · xenotype {clean(p['xenotype'])} · tôn giáo {p['ideo_name']} ({pct(p['ideo_certainty'])})",
        f"- **Xuất thân / tính cách:** {clean(p['childhood'])} / {clean(p['adulthood'])} · trait: {traits}",
        f"- **Hiện tại:** ô {fmt_pos(p['pos'])} · {status_line(p)} · lịch giờ này: {p.get('schedule_now') or '—'}"
        + (f" · cảm hứng `{p['inspiration']}`" if p.get("inspiration") else ""),
    ]
    if p.get("role") != "colonist":
        lines.append(f"- **Thân phận:** hostFaction={save.faction_name(g.get('hostFaction')) if g.get('hostFaction') else '—'} · "
                     f"guestStatus={g.get('guestStatus') or '—'} · "
                     f"đã được chữa {fmt_num(g.get('timesTendedByPlayer') or 0)} lần · questTags: {', '.join(p['questTags']) or '—'}"
                     + (f" · vào map lúc {save.fmt_tick(p['spawnedTick'])}" if p.get("spawnedTick") else ""))
    ms = p.get("mentalState_detail")
    br = p.get("mentalBreaker") or {}
    mood = f"- **Tâm trạng:** {p['mood'] * 100:.1f}%" if p.get("mood") is not None else "- **Tâm trạng:** —"
    if br:
        mood += (f" · thời gian liên tục dưới ngưỡng nhẹ/nặng/cực đoan: {fmt_duration(br.get('ticksBelowMinor', 0))} / "
                 f"{fmt_duration(br.get('ticksBelowMajor', 0))} / {fmt_duration(br.get('ticksBelowExtreme', 0))}"
                 + (" *(bộ đếm đứng yên trong lúc đang khủng hoảng)*" if ms else ""))
    if ms:
        bits = [f"`{ms.get('def')}`"]
        if ms.get("chemical"):
            bits.append(f"chất `{ms['chemical']}`" + (f" (nhóm {ms['drugCategory']})" if ms.get("drugCategory") else ""))
        if ms.get("age") is not None:
            bits.append(f"đã kéo dài {fmt_duration(ms['age'])}")
        if ms.get("causedByMood") == "True":
            bits.append("do tâm trạng thấp gây ra")
        fr = ms.get("forceRecoverAfterTicks")
        if fr is not None:
            bits.append("không có hạn tự hết cưỡng bức (forceRecoverAfterTicks = -1)" if fr < 0
                        else f"buộc hồi phục khi cơn kéo dài tới {fmt_duration(fr)}")
        known = {"class", "def", "chemical", "drugCategory", "age", "causedByMood", "forceRecoverAfterTicks"}
        bits += [f"{k}={v}" for k, v in ms.items() if k not in known]
        mood += " · **đang khủng hoảng:** " + ", ".join(bits)
    lines.append(mood)
    lines.append("- **Nhu cầu:** " + " · ".join(f"{n['def']} {pct(n['level'])}" for n in p["needs"] if n["def"] != "Mood"))
    lines.append(f"- **Ký ức ảnh hưởng tâm trạng/thiện cảm ({len(p['thoughts'])}; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, "
                 f"kéo theo thiện cảm với X):** {thought_line(p)}")
    if p.get("opinion_from_memories"):
        lines.append("- **Tổng thiện cảm từ ký ức:** " + ", ".join(f"{k} {v:+.0f}" for k, v in p["opinion_from_memories"].items()))
    for ln in lines:
        d.w(ln)
    d.w(f"- **Sức khỏe** (trạng thái `{p.get('healthState')}`; {len(p['hediffs'])} hediff):")
    d.w()
    rows = hediff_rows(p)
    if rows:
        d.table(["Hediff", "Bộ phận", "Mức", "Chăm sóc", "Tuổi (ngày)", "Ghi chú"], rows)
    else:
        d.p("*(không có hediff nào)*")
    if p.get("immunity"):
        d.w("- **Miễn dịch:** " + ", ".join(f"{i['def']} {pct(i['immunity'])}" for i in p["immunity"]))
    d.w(f"- **Kỹ năng:** {skill_line(p)}")
    d.w(f"- **Ưu tiên việc:** {work_line(p)}")
    d.w(f"- **Mặc:** {gear_line(p['apparel'])} · **Cầm:** {gear_line(p['equipment'])} · **Túi:** {gear_line(p['inventory'])}"
        + (f" · **Đang bê:** {gear_line(p['carrying'])}" if p.get("carrying") else ""))
    bed = f"{p['ownedBed']} @{fmt_pos(p.get('ownedBed_pos'))}" if p.get("ownedBed") else "chưa có"
    d.w(f"- **Thiết lập:** giường riêng: {bed} · y tế: {clean(p['medCare'])} · tự băng: {clean(p.get('selfTend'))} · "
        f"phản ứng địch: {clean(p['hostilityResponse'])} · trang phục «{policy_label(p['outfit'])}» · "
        f"thuốc «{policy_label(p['drugPolicy'])}» · ăn «{policy_label(p['foodPolicy'])}»")
    if p["timetable"]:
        d.w(f"- **Lịch 24h:** {compress_timetable(p['timetable'])}")
    if p.get("drug_records"):
        d.w("- **Lần dùng chất gần nhất:** " + ", ".join(
            f"{r['drug']} ({fmt_duration(now - r['lastTakenTicks'])} trước)" for r in p["drug_records"] if r["lastTakenTicks"] is not None))
    if p["relations"]:
        d.w("- **Quan hệ:** " + ", ".join(f"{r['def']}: {r['otherPawn_name'] or r['otherPawn']}" for r in p["relations"]))
    d.w()


def block_work_matrix(d, state):
    people = [p for mp in state["maps"] for p in colonists_of(mp)]
    if not people:
        d.p("*(không có thuộc địa viên)*")
        return
    rows = []
    for w in state.get("work_coverage", []):
        cells = []
        skill = WORK_SKILL.get(w["def"])
        for p in people:
            v = p["work_priorities"][w["index"]]["value"] if w["index"] < len(p["work_priorities"]) else None
            lv = next((s["level"] for s in p["skills"] if s["def"] == skill), None) if skill else None
            cell = "·" if not v else str(v)
            if lv is not None:
                cell += f" (kn {fmt_num(lv)})"
            cells.append(cell)
        rows.append([f"`{w['def']}`", w["name"]] + cells + ["" if w["workers"] else "**KHÔNG AI LÀM**"])
    d.table(["Việc", "Tên"] + [who(p) for p in people] + ["Ghi chú"], rows)


def block_rooms(d, mp, base_only=None):
    rooms = [r for r in mp["rooms"] if base_only is None or r["is_base"] == base_only]
    if not rooms:
        d.p("*(không tìm thấy vùng kín nào)*")
        return
    rows = []
    for r in rooms:
        inside = []
        for k, v in r["player_buildings"].items():
            inside.append(f"{k}×{v}")
        for b in r["beds"]:
            tag = "giường bệnh" if b["medical"] else ("giường tù" if b["forPrisoners"] else "giường")
            inside.append(f"[{tag} {fmt_pos(b['pos'])}: {', '.join(b['owners']) or 'chưa gán'}]")
        for k, v in r["other_buildings"].items():
            inside.append(f"{k}×{v} (không phải của bạn)")
        inside += r["details"]
        if r["items"]:
            inside.append("vật phẩm: " + ", ".join(f"{k}×{v}" for k, v in r["items"].items()))
        if r["corpses"]:
            inside.append("XÁC: " + ", ".join(f"{k}×{v}" for k, v in r["corpses"].items()))
        if r["construction"]:
            inside.append("bản vẽ: " + ", ".join(f"{k}×{v}" for k, v in r["construction"].items()))
        if r["pawns"]:
            inside.append("đang ở trong: " + ", ".join(r["pawns"]))
        if r["zones"]:
            inside.append("zone: " + ", ".join(f"{k} ({v} ô)" for k, v in r["zones"].items()))
        if r["filth"]:
            inside.append(f"bẩn ×{r['filth']}")
        floors = ", ".join(f"{k}×{v}" for k, v in list(r["floors"].items())[:3])
        roof = f"{r['roofed']}/{r['cells']}"
        if r["fogged"] == r["cells"]:
            inside.insert(0, "**TOÀN BỘ TRONG SƯƠNG MÙ — người chơi chưa nhìn thấy bên trong**")
        elif r["fogged"]:
            roof += f" · sương mù {r['fogged']}/{r['cells']}"
        rows.append([r["id"], fmt_bbox(r["bbox"]), r["cells"], roof,
                     f"{r['temperature']}°C" if r["temperature"] is not None else "—",
                     floors, ", ".join(fmt_pos(x) for x in r["doors"]) or "—",
                     "; ".join(inside) or "trống",
                     f"{r['dist']} ô {r['bearing']}" if not r["is_base"] and r["dist"] is not None else ""])
    hdr = ["Phòng", "Bao", "Số ô", "Có mái", "Nhiệt độ", "Sàn", "Cửa tại", "Bên trong"]
    if base_only is False or base_only is None:
        hdr.append("Cách căn cứ")
    else:
        rows = [r[:-1] for r in rows]
    d.table(hdr, rows)


def block_quest(d, save, q, level=3):
    now = save.ticks_game
    d.h(level, f"«{q['name'] or q['root']}» — {q['state_vi']}")
    pairs = [
        ("Loại (root)", f"`{q['root']}`" + (" · từ thiện" if q["charity"] else "") + (" · ẩn trên giao diện" if q["hidden"] else "")),
        ("Xuất hiện", f"{save.fmt_tick(q['appearanceTick'])} (tick {q['appearanceTick']})"),
    ]
    if q["acceptanceTick"] is not None and q["acceptanceTick"] >= 0:
        pairs.append(("Đã nhận lúc", f"{save.fmt_tick(q['acceptanceTick'])}" + (" (tự động)" if q["initiallyAccepted"] else "")))
    if q["state"] == "NotYetAccepted" and q["ticksUntilOfferExpires"] is not None:
        pairs.append(("Hạn nhận", f"{save.fmt_tick(q['acceptanceExpireTick'])} — còn **{fmt_duration(q['ticksUntilOfferExpires'])}**"))
    elif q["acceptanceExpireTick"] is not None and q["state"] == "EndedOfferExpired":
        pairs.append(("Hạn nhận", f"đã qua lúc {save.fmt_tick(q['acceptanceExpireTick'])}"))
    if q["challengeRating"] is not None and q["challengeRating"] >= 0:
        pairs.append(("Độ khó", f"{q['challengeRating']} sao"))
    if q["description_clean"]:
        pairs.append(("Mô tả", q["description_clean"]))
    if q["rewards"]:
        if len(q["rewards"]) == 1:
            pairs.append(("Phần thưởng", "; ".join(q["rewards"][0])))
        else:
            pairs.append(("Phần thưởng (chọn 1)", " **HOẶC** ".join("; ".join(o) for o in q["rewards"])))
    timers = [t for t in q["timers"] if t["state"] != "Disabled"]
    if timers:
        ts = []
        for t in timers:
            s = f"{t['label']}: {fmt_duration(t['delayTicks'])}"
            if t["dueTick"] is not None and t["state"] == "Enabled":
                s += f" (đang chạy, đến hạn sau {fmt_duration(t['dueTick'] - now)})"
            elif t["dueTick"] is not None:
                s += f" (đã kích hoạt lúc {save.fmt_tick(t['enableTick'])}, trạng thái {t['state']})"
            ts.append(s)
        pairs.append(("Mốc thời gian trong nhiệm vụ", "; ".join(ts)))
    if q["pawns"]:
        pairs.append(("Nhân vật liên quan", "; ".join(
            f"{x['name']} ({x['gender']}, {x['age']} tuổi, `{x['kindDef']}`, {x['faction']}, {x['where']}"
            + (f"; quest tag: {', '.join(x['questTags'])}" if x.get("questTags") else "")
            + (f"; **{'; '.join(x['links'])}**" if x.get("links") else "") + ")"
            for x in q["pawns"])))
    if q["things"]:
        pairs.append(("Vật liên quan", "; ".join(f"`{x['def']}` {fmt_pos(x['pos'])}" for x in q["things"])))
    if q["factions"]:
        pairs.append(("Phe liên quan", ", ".join(q["factions"])))
    if q["end_conditions"] and not q["state"].startswith("Ended"):
        ok = quest_signals(q, "Success")
        bad = quest_signals(q, "Fail")
        if ok:
            pairs.append(("Thành công khi (tín hiệu)", ", ".join(ok)))
        if bad:
            pairs.append(("Thất bại khi (tín hiệu)", ", ".join(bad)))
    d.kv(pairs)


def glyph_for_building(defname, cls, extra, used, mine=True):
    table = {
        "Wall": "#", "Door": "+", "Bed": "B", "Bedroll": "B", "DoubleBed": "B", "RoyalBed": "B",
        "TorchLamp": "*", "StandingLamp": "*", "Campfire": "F", "PassiveCooler": "P",
        "Table1x2c": "T", "Table2x2c": "T", "Table2x4c": "T", "Table3x3c": "T",
        "Stool": "c", "DiningChair": "c", "Armchair": "c",
        "FueledStove": "S", "ElectricStove": "S", "TableButcher": "K",
        "SimpleResearchBench": "R", "HiTechResearchBench": "R",
        "HorseshoesPin": "J", "ChessTable": "J", "MeditationSpot": "o",
        "WoodFiredGenerator": "G", "ChemfuelPoweredGenerator": "G", "SolarGenerator": "G",
        "WindTurbine": "G", "GeothermalGenerator": "G", "Battery": "=", "Cooler": "C", "Heater": "h",
        "SteamGeyser": "V", "Column": "I",
    }
    if "Door" in cls:
        return "+"
    if "Bed" in cls:
        return "M" if extra.get("medical") == "True" else "B"
    if defname in table:
        return table[defname]
    if not mine:
        return "%"              # phế tích / đồ cổ không phải của bạn
    if defname in used:
        return used[defname]
    taken = set(table.values()) | set(used.values()) | set("MBXiax&:,~^$_.%")
    for ch in (defname[:1].upper() + "ADEHLNQUWYZ"):
        if ch not in taken:
            used[defname] = ch
            return ch
    used[defname] = "?"
    return "?"


GLYPH_LEGEND = {
    "#": "tường", "+": "cửa", "B": "giường", "M": "giường bệnh", "*": "đuốc/đèn", "F": "lửa trại",
    "T": "bàn ăn", "c": "ghế", "S": "bếp", "K": "bàn mổ thịt", "R": "bàn nghiên cứu",
    "J": "đồ giải trí (cọc móng ngựa/bàn cờ)", "o": "điểm thiền", "G": "máy phát", "=": "pin",
    "C": "máy lạnh", "h": "máy sưởi", "P": "máy làm mát thụ động", "V": "mạch nước nóng", "I": "cột",
    "x": "bản vẽ/khung chưa xây", "&": "xác chết", "i": "vật phẩm", "a": "động vật", "!": "pawn thù địch",
    "%": "phế tích/đồ cổ không phải của bạn",
    '"': "cây trồng", ",": "ô ruộng trống", ":": "ô kho trống", "^": "vách đá tự nhiên",
    "$": "quặng", "~": "nước", "_": "sàn đã lát", ".": "nền tự nhiên", "?": "sương mù (chưa khám phá)",
}


def ascii_base_map(save, md, mp, pad_x=9, pad_z=6, max_w=140, max_h=80):
    """Sơ đồ ký tự khu căn cứ (Bắc ở trên). Trả (văn_bản, chú_thích)."""
    bb = mp.get("base_bbox")
    if not bb:
        return "(chưa có công trình nào của người chơi)", ""
    g = md.grids
    w, h = md.size or (0, 0)
    x0, x1 = max(0, bb[0] - pad_x), min(w - 1, bb[1] + pad_x)
    z0, z1 = max(0, bb[2] - pad_z), min(h - 1, bb[3] + pad_z)
    if x1 - x0 + 1 > max_w:
        mid = (x0 + x1) // 2
        x0, x1 = mid - max_w // 2, mid + max_w // 2 - 1
    if z1 - z0 + 1 > max_h:
        mid = (z0 + z1) // 2
        z0, z1 = mid - max_h // 2, mid + max_h // 2 - 1

    marks = {}
    used_letters = {}
    legend_dyn = {}

    def put(pos, ch):
        if pos and x0 <= pos[0] <= x1 and z0 <= pos[1] <= z1:
            marks[pos] = ch

    # lớp nền: địa hình / đá / sương mù
    if g is not None:
        for z in range(z0, z1 + 1):
            for x in range(x0, x1 + 1):
                i = g.idx(x, z)
                if g.fog is not None and g.fog[i]:
                    marks[(x, z)] = "?"
                    continue
                rock = g.rock[i] if g.rock else None
                if is_ore(rock):
                    marks[(x, z)] = "$"
                elif is_rock_wall(rock):
                    marks[(x, z)] = "^"
                else:
                    kind = terrain_kind(g.terrain[i]) if g.terrain else "soil"
                    marks[(x, z)] = "~" if kind == "water" else "_" if kind == "floor" else "."
    # zone
    for z in md.zones:
        ch = "," if "Growing" in z["class"] else ":"
        for p in z["cells"]:
            if marks.get(p) != "?":
                put(p, ch)
    for pl in mp["plants_sown"]:
        put(pl["pos"], '"')
    for it in mp["items"]:
        put(it["pos"], "i")
    for c in mp["corpses"]:
        put(c["pos"], "&")
    for m in mp["mineables"]:
        put(m["pos"], "$" if is_ore(m["def"]) else "^")
    for b in mp["buildings_other"] + mp["buildings_player"]:
        mine = b["faction"] == save.player_faction
        if not b["pos"] or (b.get("fogged") and not mine):
            continue
        ch = glyph_for_building(b["def"], b["class"], b["extra"], used_letters, mine)
        if b["def"] in used_letters:
            legend_dyn[ch] = b["def"]
        put(b["pos"], ch)
    for c in mp["construction"]:
        put(c["pos"], "x")
    for a in mp["animals"]:
        put(a["pos"], "a")
    for m in mp["mechs"]:
        if not m.get("fogged"):
            put(m["pos"], "!" if m["faction_relation"] == "Hostile" else "a")
    people = []
    for i, p in enumerate(mp["pawns"], 1):
        ch = str(i) if i < 10 else chr(ord("a") + i - 10)
        if p["pos"] and x0 <= p["pos"][0] <= x1 and z0 <= p["pos"][1] <= z1:
            marks[p["pos"]] = ch if p.get("role") != "hostile" else "!"
            people.append(f"{ch} = {who(p)} {fmt_pos(p['pos'])}")

    lines = []
    for z in range(z1, z0 - 1, -1):
        lines.append(f"{z:4} " + "".join(marks.get((x, z), ".") for x in range(x0, x1 + 1)))
    for div in (100, 10, 1):
        lines.append("     " + "".join(str(x // div % 10) for x in range(x0, x1 + 1)))
    used = set(ch for ch in "".join(l[5:] for l in lines[:-3]))
    legend = [f"`{ch}` {GLYPH_LEGEND[ch]}" for ch in GLYPH_LEGEND if ch in used and ch not in legend_dyn]
    legend += [f"`{ch}` {dn}" for ch, dn in sorted(legend_dyn.items()) if ch in used]
    note = (f"Khung vẽ: x {x0}–{x1}, z {z0}–{z1}. BẮC ở trên (z lớn), ĐÔNG bên phải (x lớn). "
            f"Số bên trái = z của hàng; 3 hàng số dưới cùng = x của cột (trăm/chục/đơn vị). "
            f"Mỗi công trình chỉ vẽ tại ô gốc (pos); công trình nhiều ô (giường 1×2, bếp 3×1, bàn…) chiếm thêm ô bên cạnh. "
            f"Ký tự trên cùng che ký tự dưới (người > động vật > bản vẽ > công trình > xác > vật phẩm > zone > nền).\n"
            f"Chú thích: " + " · ".join(legend)
            + ("\nNgười: " + " · ".join(people) if people else ""))
    return "\n".join(lines), note


def ascii_overview_map(save, md, mp, target=50):
    """Bản đồ toàn map thu nhỏ: mỗi ký tự = 1 khối block×block ô. Bắc ở trên."""
    g = md.grids
    if g is None or not md.size:
        return "(không giải mã được lưới địa hình)", ""
    w, h = md.size
    block = max(1, math.ceil(max(w, h) / target))
    cols, rows = math.ceil(w / block), math.ceil(h / block)
    special = {}

    def mark(pos, ch, prio):
        if not pos:
            return
        key = (pos[0] // block, pos[1] // block)
        if key not in special or special[key][1] < prio:
            special[key] = (ch, prio)

    for it in mp["ores"]:
        if it["fogged_cells"] < it["cells"]:
            mark(it["center"], "$", 1)
    for z in md.zones:
        for c in z["cells"][:: max(1, len(z["cells"]) // 6)]:
            mark(c, "z", 2)
    for b in mp["buildings_other"]:
        ch = {"SteamGeyser": "S", "AncientCryptosleepCasket": "K", "VoidMonolith": "V",
              "GravEngine": "G"}.get(b["def"])
        if ch:
            mark(b["pos"], ch, 4 if ch != "S" else 3)
    for b in mp["buildings_player"]:
        if b["def"] in WALL_LIKE_DEFS or "Door" in b["class"]:
            mark(b["pos"], "B", 5)
    for m in mp["mechs"]:
        if m["faction_relation"] == "Hostile":
            mark(m["pos"], "!", 6)
    for p in mp["pawns"]:
        if p.get("role") == "hostile":
            mark(p["pos"], "!", 6)

    lines = []
    for r in range(rows - 1, -1, -1):
        row = []
        for c in range(cols):
            if (c, r) in special:
                row.append(special[(c, r)][0])
                continue
            cnt = Counter()
            n = 0
            for z in range(r * block, min(h, (r + 1) * block)):
                for x in range(c * block, min(w, (c + 1) * block)):
                    i = z * w + x
                    n += 1
                    if g.fog is not None and g.fog[i]:
                        cnt["fog"] += 1
                    elif g.rock and is_rock_wall(g.rock[i]):
                        cnt["rock"] += 1
                    else:
                        cnt[terrain_kind(g.terrain[i]) if g.terrain else "soil"] += 1
            if cnt["fog"] * 2 >= n:
                ch = "?"
            elif cnt["rock"] * 2 >= n:
                ch = "^"
            elif cnt["water"] * 5 >= n * 2:
                ch = "~"
            elif cnt["road"] * 5 >= n:
                ch = "="
            elif cnt["mud"] * 2 >= n:
                ch = ","
            elif cnt["rich"] * 2 >= n:
                ch = '"'
            elif cnt["floor"] * 2 >= n:
                ch = "_"
            elif cnt["rock"] * 5 >= n:
                ch = "'"
            else:
                ch = "."
            row.append(ch)
        lines.append(f"{r * block:4} " + "".join(row))
    for div in (100, 10):
        lines.append("     " + "".join(str((c * block) // div % 10) for c in range(cols)))
    note = (f"Mỗi ký tự = khối {block}×{block} ô; số bên trái = z của mép dưới khối, 2 hàng số dưới = x (trăm/chục) của mép trái khối. "
            f"BẮC ở trên, ĐÔNG bên phải.\n"
            "Chú thích: `B` căn cứ (tường/cửa của bạn) · `z` zone của bạn nằm ngoài căn cứ · `!` pawn thù địch · `K` kén ngủ đông cổ · "
            "`V` void monolith · `G` grav engine · `S` mạch nước nóng · `$` mạch quặng đã lộ · `^` núi/vách đá (≥50% khối) · "
            "`'` lác đác đá · `~` nước · `=` đường nhựa cổ · `,` bùn/lầy · `\"` đất màu mỡ · `_` nền lát/nền đá · `?` sương mù · `.` đất thường")
    return "\n".join(lines), note


NOTABLE_OTHER_DEFS = {
    "AncientCryptosleepCasket", "AncientHermeticCrate", "AncientSecurityCrate",
    "AncientMechDropBeacon", "AncientShipBeacon",
}


def block_other_buildings(d, mp):
    grouped = defaultdict(list)
    for b in mp["buildings_other"]:
        grouped[b["def"]].append(b)
    rows, minor = [], []
    for defn, lst in sorted(grouped.items(), key=lambda kv: -len(kv[1])):
        poss = [b["pos"] for b in lst if b["pos"]]
        nearest = min(poss, key=lambda p: rel_to_base(mp, p)[0] or 0) if poss else None
        extra = []
        for b in lst:
            for k in ("gravshipName", "progress", "studyEnabled"):
                if k in b["extra"]:
                    extra.append(f"{k}={b['extra'][k]}")
            if b["extra"].get("inner"):
                extra.append(f"{fmt_pos(b['pos'])} chứa " + fmt_inner(b["extra"]["inner"]))
        fog = sum(1 for b in lst if b.get("fogged"))
        if not extra and defn.startswith("Ancient") and defn not in NOTABLE_OTHER_DEFS:
            minor.append(f"`{defn}`×{len(lst)} (gần nhất {fmt_pos(nearest)})")
            continue
        rows.append([f"`{defn}`", len(lst),
                     ", ".join(fmt_pos(p) for p in poss) if len(poss) <= 6 else fmt_bbox(bbox_of(poss)),
                     f"{fmt_pos(nearest)} ({fmt_rel(mp, nearest)})" if nearest else "—",
                     f"{fog}/{len(lst)}" if fog else "", "; ".join(extra[:8])])
    d.table(["Def", "SL", "Vị trí", "Gần căn cứ nhất", "Trong sương mù", "Chi tiết"], rows)
    if minor:
        d.p("Đồ cổ/phế tích khác (trang trí, không chứa gì): " + ", ".join(minor) + ".")


def quest_signals(q, outcome):
    """Tín hiệu kết thúc nhiệm vụ, bỏ các tên nội bộ vô nghĩa và gộp biến thể."""
    out = []
    for e in q["end_conditions"]:
        if e["outcome"] != outcome:
            continue
        sig = re.sub(r"_(AssaultColony|LeaveColony|BadThought)$", "", e["signal"])
        if re.match(r"^(OuterNodeCompleted\d*|FilterPass\d*)$", sig):
            continue
        if sig not in out:
            out.append(sig)
    return out


def tale_sentence(t):
    a = (t.get("first") or {}).get("name")
    b = (t.get("second") or {}).get("name")
    solo = (t.get("pawn") or {}).get("name")
    thing = t.get("thing")
    via = f" (bằng {thing})" if thing else ""
    d = t["def"]
    if d == "Downed":
        return f"{a} bị hạ gục" + (f" bởi {b}{via}" if b and b != "None" else " (không do ai gây trực tiếp — kiệt sức/mất máu/đau)")
    if d == "KilledBy":
        return f"{a} bị {b} giết"
    if d in ("KilledMelee", "KilledLongRange", "KilledMajorThreat", "KilledMortar", "KilledChild"):
        return f"{a} giết {b}{via}"
    if d == "KilledCapacity":
        return f"{a} giết {b} (nạn nhân mất chức năng {thing})"
    if d == "Hunted":
        return f"{a} săn được {b}"
    if d == "Stripped":
        return f"{a} lột đồ {b}"
    if d == "TradedWith":
        return f"{a} giao dịch với {b}"
    if d == "TrainedAnimal":
        return f"{a} huấn luyện {b} ({thing})"
    if d == "Raid":
        return f"Đột kích bắt đầu (người chứng kiến: {solo})"
    if d == "LandedInPod":
        return f"{solo} đáp xuống bằng pod"
    if d in ("HeatstrokeRevealed", "HypothermiaRevealed", "IllnessRevealed", "ToxicityRevealed"):
        return f"{solo} phát bệnh {thing}"
    if d == "Wounded":
        return f"{a} bị thương" + (f" do {b} gây ra" if b and b != "None" else "") + via
    if d == "ReadBook":
        return f"{solo} đọc sách"
    if d == "PlayedGame":
        return f"{solo} chơi giải trí{via}"
    if d == "Meditated":
        return f"{solo} thiền"
    if d == "Prayed":
        return f"{solo} cầu nguyện"
    if d == "MajorThreat":
        return f"Mối đe doạ lớn: {t.get('label') or '—'}"
    if d == "ManhunterPack":
        return f"Bầy thú điên (manhunter) kéo vào map (người chứng kiến: {solo})"
    bits = [x for x in (solo, a, b) if x and x != "None"]
    return (t.get("label") or " / ".join(bits) or "—") + via


def designation_summary(mp):
    groups = defaultdict(list)
    for x in mp["designations"]:
        groups[(x["def"], x["target_def"])].append(x["target_pos"])
    rows = []
    for (dname, tdef), poss in sorted(groups.items(), key=lambda kv: (kv[0][0], -len(kv[1]))):
        poss = [p for p in poss if p]
        nearest = min(poss, key=lambda p: rel_to_base(mp, p)[0] or 0) if poss else None
        rows.append([dname, f"`{tdef}`" if tdef else "—", len(groups[(dname, tdef)]), fmt_bbox(bbox_of(poss)),
                     f"{fmt_pos(nearest)} ({fmt_rel(mp, nearest)})" if nearest else "—",
                     DESIGNATION_WORK.get(dname, "?")])
    return rows


def render_ai_state(save: SaveFile, state: dict, standalone: bool = False) -> str:
    """Bản state cô đọng cho AI đọc: đủ mọi thứ đang diễn ra, bỏ phần thô lặp lại."""
    d = Doc()
    g = state["game"]
    date = g["date"]
    now = save.ticks_game
    colony = g.get("colonyName") or g.get("playerFaction") or "thuộc địa"
    d.h(1, f"TRẠNG THÁI THUỘC ĐỊA «{colony}» — RimWorld {state['meta']['gameVersion']}")
    d.p(f"*Ảnh chụp tại **{date['display']}** (tick {now:,}, ngày chơi thứ {date['days_played']}). "
        f"Sinh tự động từ file save `{save.path.name}` ({state['source']['size_bytes']:,} byte, "
        f"SHA-1 `{state['source']['sha1']}`) "
        + ("bằng script phân tích" if standalone else "bởi `tools/rimworld_dump.py`")
        + "; không có nội dung nào do người viết tay. File chỉ đúng tại thời điểm lưu nói trên — "
          "nếu ván chơi đã đi tiếp (file save được lưu lại) thì bản này đã cũ"
        + ("." if standalone else " — chạy lại công cụ.") + "*")

    d.h(2, "0. Cách đọc file này")
    d.p("- Đây là **ảnh chụp trạng thái** một ván RimWorld tại đúng thời điểm lưu. Mọi con số lấy trực tiếp từ file save; "
        "chỗ nào ghi *(suy luận)* / *(ước tính)* là do công cụ tính thêm, kèm giả định.\n"
        "- **Toạ độ** `(x,z)`: gốc (0,0) ở góc Tây-Nam map; x tăng về **Đông**, z tăng về **Bắc**. Khoảng cách tính bằng ô.\n"
        "- **Thời gian**: 1 giờ game = 2.500 tick, 1 ngày = 60.000 tick, 1 quý = 15 ngày, 1 năm = 4 quý "
        "(Aprimay, Jugust, Septober, Decembary).\n"
        "- Tên trong dấu `` ` `` là **defName** gốc của game (tiếng Anh) — dùng để tra wiki chính xác.\n"
        "- Mức nhu cầu/tâm trạng là 0–100%. Ưu tiên việc: 1 = cao nhất … 4 = thấp nhất, 0 = tắt.\n"
        "- Mục 2 là danh sách **việc cần chú ý** do công cụ tự rà theo quy tắc; các mục sau là dữ liệu đầy đủ để kiểm chứng.\n"
        "- File save chứa cả những thứ **người chơi chưa nhìn thấy** (vùng còn sương mù, bên trong kén/hòm cổ). "
        "Các chỗ đó đều được ghi rõ «trong sương mù» — hãy coi là thông tin biết trước, người chơi trong game chưa có.\n"
        + ("- File này **tự chứa đủ**, không kèm file phụ nào. Thứ duy nhất chi tiết hơn (từng ô đất, từng cây, mọi trường XML) "
           f"là chính file save `{save.path.name}`.\n" if standalone else
           "- Cần chi tiết hơn nữa (từng ô, từng cây, mọi trường XML của pawn): xem `report.md`, `state.json` và các file CSV cùng thư mục.\n")
        + "- **Mục lục:** @@TOC@@")

    # 1 -------------------------------------------------------------------
    d.h(2, "1. Ảnh chụp nhanh")
    mp0 = state["maps"][0] if state["maps"] else None
    humans = mp0["pawns"] if mp0 else []
    roles = Counter(p.get("role") for p in humans)
    hist = state["history"]
    wealth = hist["series"].get("Wealth_Total") or []
    moods = hist["series"].get("ColonistMood") or []
    step = hist.get("interval_ticks")
    pairs = [
        ("Ngày giờ trong game", f"**{date['display']}** — mùa {SEASON_VI.get(date['season'], date['season'] or '?')} "
                               f"(ngày {date['day_of_year']}/60 của năm; múi giờ UTC{date['timezone']:+d})"),
        ("Sắp tới", f"sang ngày mới sau {fmt_duration(date['ticks_to_midnight'])}; sang quý {date['next_quadrum']} sau "
                    f"{fmt_duration(date['ticks_to_next_quadrum'])}"
                    + (f" (mùa {SEASON_VI.get(date['next_season'], date['next_season'])} — suy luận, bán cầu {date['hemisphere']})" if date.get("next_season") else "")),
        ("Đã chơi", f"{date['days_played']} ngày game (tick {now:,}); bắt đầu ngày {save.fmt_tick(0)}"),
        ("Thuộc địa", f"«{colony}» — phe «{g.get('playerFaction')}» — ô thế giới {state['world']['startingTile']} — "
                      f"biome `{state['world'].get('biome')}` — hành tinh {state['world']['name']}"),
        ("Kịch bản / người kể chuyện", f"{g['scenario']['name']} · `{g['storyteller']}` · độ khó `{g['difficulty']}`"),
        ("Dân số trên map", ", ".join(f"{v} {ROLE_VI.get(k, k)}" for k, v in roles.items()) or "—"),
        ("Đột kích / đe doạ lớn", last_threat_line(save, state)),
    ]
    if mp0:
        gs = mp0.get("grids") or {}
        rt = g.get("recent_temperature") or {}
        rt_txt = ""
        if rt.get("outdoor_max"):
            rt_txt = (f" · {rt['days']} ngày qua game ghi kèm sự kiện: ngoài trời {rt['outdoor_min']['temp']}–{rt['outdoor_max']['temp']}°C "
                      f"(cao nhất lúc {rt['outdoor_max']['date']})")
            if rt.get("indoor_max"):
                rt_txt += f", trong phòng tới {rt['indoor_max']['temp']}°C (lúc {rt['indoor_max']['date']})"
        pairs.append(("Thời tiết / nhiệt độ", f"`{mp0['weather']}` · ngoài trời {gs.get('outdoor_temp')}°C (đang là {date['hour_int']:02d}:{date['minute']:02d}) · điều kiện đặc biệt: "
                      + (", ".join(c["def"] for c in mp0["conditions"]) or "không") + rt_txt))
    if wealth:
        ago = f" (mẫu gần nhất {fmt_duration(now - hist['last_sample_tick'])} trước)" if hist.get("last_sample_tick") is not None else ""
        pairs.append(("Tài sản thuộc địa", f"{wealth[-1]:,.0f}{ago}; vật phẩm {hist['series'].get('Wealth_Items', [0])[-1]:,.0f}"
                      + (f"; 1 ngày trước {wealth[-1 - TICKS_PER_DAY // step]:,.0f}" if step and len(wealth) > TICKS_PER_DAY // step else "")))
    if moods:
        k = 8
        pairs.append(("Tâm trạng TB thuộc địa (game ghi)", " → ".join(f"{v:.0f}%" for v in moods[-k:])
                      + (f" (mỗi mẫu cách {fmt_duration(step)})" if step else "")))
    pairs.append(("Mods", ", ".join(state["meta"]["modNames"])))
    d.kv(pairs)

    # 2 -------------------------------------------------------------------
    d.h(2, "2. Việc cần chú ý ngay")
    d.p("*Tự rà từ dữ liệu, xếp theo mức độ. Ngưỡng tâm trạng 35/20/5% là ngưỡng gốc vanilla (trait có thể làm lệch).*")
    block_alerts(d, state)

    for mp in state["maps"]:
        md = save.maps[mp["index"]]
        multi = len(state["maps"]) > 1
        if multi:
            d.h(1, f"MAP {mp['index']}")

        # 3 ---------------------------------------------------------------
        d.h(2, "3. Con người trên map")
        rows = []
        for i, p in enumerate(mp["pawns"], 1):
            needs = {n["def"]: n["level"] for n in p["needs"]}
            inj = [h for h in p["hediffs"] if h["class"] == "Hediff_Injury" and h.get("isPermanent") != "True"]
            other = [h["def"] for h in p["hediffs"] if h["class"] != "Hediff_Injury"]
            health = []
            if inj:
                health.append(f"{len(inj)} vết thương")
            health += sorted(set(other))
            rows.append([
                i, f"**{who(p)}**", ROLE_VI.get(p.get("role"), p.get("role")),
                f"{p['gender'][:1]}, {fmt_num(p['age_bio'], 0)}t", fmt_pos(p["pos"]),
                status_line(p), pct(p["mood"]),
                " / ".join(pct(needs.get(k)) for k in ("Food", "Rest", "Joy")),
                ", ".join(health) or "khỏe",
                gear_line(p["equipment"]),
            ])
        d.table(["#", "Tên", "Vai trò", "Giới, tuổi", "Ô", "Đang làm gì", "Tâm trạng", "Ăn / Ngủ / Giải trí",
                 "Sức khỏe (tóm tắt)", "Vũ khí"], rows)
        for p in mp["pawns"]:
            block_people_detail(d, save, p, level=3)

        # 4 ---------------------------------------------------------------
        d.h(2, "4. Ma trận công việc (ai bật việc gì)")
        d.p("Số = mức ưu tiên (1 cao nhất), `·` = tắt; `kn` = cấp kỹ năng liên quan. "
            "Thứ tự hàng = thứ tự game xét khi cùng mức ưu tiên (trên trước). "
            f"Chế độ ưu tiên thủ công: {g['playSettings'].get('useWorkPriorities')}.")
        block_work_matrix(d, state)

        # 5 ---------------------------------------------------------------
        d.h(2, "5. Căn cứ")
        bc = mp.get("base_center")
        d.p(f"Tâm căn cứ (trung bình toạ độ tường/cửa của bạn): {fmt_pos(bc)}; bao tường: {fmt_bbox(mp.get('base_bbox'))}. "
            f"Tổng {len(mp['buildings_player'])} công trình của bạn.")
        d.h(3, "5.1 Sơ đồ căn cứ")
        text, note = ascii_base_map(save, md, mp)
        d.p("```\n" + text + "\n```")
        d.p(note)
        d.h(3, "5.2 Phòng / vùng kín thuộc căn cứ")
        d.p("*Game không lưu danh sách phòng; công cụ tự loang tìm vùng bị tường/đá/cửa bao kín. "
            "Nhiệt độ lấy từ lưới nhiệt lưu trong save.*")
        block_rooms(d, mp, base_only=True)
        role_stats = latest_room_stats(state)
        if role_stats:
            d.p("**Chỉ số phòng do chính game tính** (lấy từ sự kiện gần nhất có ghi kèm bối cảnh; ấn tượng/đẹp/sạch càng âm càng tệ): "
                + "; ".join(f"`{r}`: ấn tượng {fmt_num(s['roomImpressiveness'], 1)}, đẹp {fmt_num(s['roomBeauty'], 1)}, "
                            f"sạch {fmt_num(s['roomCleanliness'], 1)} (lúc {s['date']})" for r, s in role_stats.items()))
        d.h(3, "5.3 Công trình của bạn")
        agg = defaultdict(list)
        for b in mp["buildings_player"]:
            agg[(b["def"], b["stuff"] or "—")].append(b)
        rows = []
        for (defn, stuff), lst in sorted(agg.items(), key=lambda kv: -len(kv[1])):
            if len(lst) > 6:
                where = f"{len(lst)} cái trong {fmt_bbox(bbox_of(b['pos'] for b in lst if b['pos']))}"
            else:
                where = ", ".join(fmt_pos(b["pos"]) for b in lst)
            notes = []
            for b in lst:
                ex = b["extra"]
                bits = []
                if ex.get("bills"):
                    bits.append("bill: " + "; ".join(fmt_bill(x) for x in ex["bills"]))
                if "fuel" in ex:
                    bits.append(f"nhiên liệu {fmt_num(num(ex['fuel']), 1)}")
                if ex.get("assignedPawns") is not None and len(lst) <= 6:
                    bits.append("gán cho: " + (", ".join(o["name"] for o in ex["assignedPawns"]) or "chưa ai"))
                if ex.get("medical") == "True":
                    bits.append("giường bệnh")
                for k in ("powerOn", "storedPower", "targetTemperature", "switchOn", "holdOpen", "brokenDown"):
                    if k in ex:
                        bits.append(f"{k}={ex[k]}")
                if bits and len(lst) <= 6:
                    notes.append(f"{fmt_pos(b['pos'])}: " + ", ".join(bits))
            hp = [b["health"] for b in lst if b["health"] is not None]
            rows.append([f"`{defn}`", stuff, len(lst), where,
                         (f"{min(hp):.0f}" if min(hp) == max(hp) else f"{min(hp):.0f}–{max(hp):.0f}") if hp else "—",
                         " · ".join(notes)])
        d.table(["Def", "Vật liệu", "SL", "Vị trí", "HP", "Chi tiết"], rows)
        if mp["construction"]:
            d.h(3, "5.4 Công trình CHƯA xây (bản vẽ / khung)")
            d.table(["Loại", "Sẽ xây", "Ô", "Vật liệu", "Đặt lúc", "Đã có trong khung"],
                    [["khung (đang xây)" if c["kind"] == "frame" else "bản vẽ", f"`{c['build_def']}`", fmt_pos(c["pos"]),
                      c["stuff"] or "—",
                      f"{save.fmt_tick(c['spawnedTick'])} ({fmt_duration(now - c['spawnedTick'])} trước)" if c["spawnedTick"] is not None else "—",
                      ", ".join(f"{x['def']}×{x['stackCount']}" for x in c["contents"]) or "—"]
                     for c in sorted(mp["construction"], key=lambda c: (c["def"], c["pos"] or (0, 0)))])

        # 6 ---------------------------------------------------------------
        d.h(2, "6. Kho & tài nguyên")
        zone_tot = defaultdict(lambda: defaultdict(int))
        notes = defaultdict(list)
        for it in mp["items"]:
            where = it["zone"] or ("trong sương mù" if it.get("fogged") else "ngoài zone")
            zone_tot[it["def"]][where] += it["stackCount"]
            if it.get("forbidden") == "True":
                notes[it["def"]].append(f"bị cấm ×{it['stackCount']} tại {fmt_pos(it['pos'])}")
            if it.get("rot_days_left") is not None and it["rot_days_left"] < 5:
                notes[it["def"]].append(f"×{it['stackCount']} hỏng sau ~{it['rot_days_left']} ngày")
            if it.get("quality"):
                notes[it["def"]].append(f"{it['quality']}" + (f"/{it['stuff']}" if it.get("stuff") else ""))
        rows = []
        for defn, total in sorted(mp["item_totals"].items(), key=lambda kv: -kv[1]):
            rows.append([f"`{defn}`", label(defn, ITEMS), total,
                         ", ".join(f"{zn}: {n}" for zn, n in sorted(zone_tot[defn].items(), key=lambda kv: -kv[1])),
                         "; ".join(notes[defn][:4])])
        d.table(["Def", "Tên", "Tổng", "Nằm ở đâu", "Ghi chú"], rows)
        carried = Counter()
        for p in mp["pawns"]:
            if p.get("role") in ("colonist", "slave"):
                for it in p["inventory"]:
                    carried[it["def"]] += it["stackCount"] or 1
        if carried:
            d.p("Trong túi thuộc địa viên (chưa tính ở bảng trên): " + ", ".join(f"`{k}`×{v}" for k, v in carried.items()) + ".")
        food = mp.get("food") or {}
        if food.get("rows"):
            d.p("**Lương thực cho người** *(ước tính theo dinh dưỡng vanilla; đã gồm cả đồ ăn trong túi thuộc địa viên)*: "
                + ", ".join(f"`{r['def']}`×{r['count']} (={r['nutrition']})" for r in food["rows"])
                + f" → tổng {food['nutrition_total_as_is']} dinh dưỡng nguyên trạng, {food['nutrition_total_if_cooked']} nếu nấu hết thành suất đơn giản; "
                  f"{food['eaters']} người ăn cần {food['nutrition_needed_per_day']}/ngày → **≈ {food['days_as_is']}–{food['days_if_cooked']} ngày**.")
        stock = [z for z in mp["zones"] if "Stockpile" in z["class"]]
        if stock:
            d.h(3, "Vùng kho")
            rows = []
            for z in stock:
                contents = Counter()
                for it in mp["items"]:
                    if it["zone"] == z["label"]:
                        contents[it["def"]] += it["stackCount"]
                for c in mp["corpses"]:
                    if c["zone"] == z["label"]:
                        contents[f"{c['def']} ({ROT_STAGE_VI.get(c['rot_stage'], c['rot_stage'])})"] += 1
                st = z["settings"] or {}
                allowed = st.get("allowedDefs") or []
                kinds = Counter("xác" if a.startswith("Corpse_") else "khác" for a in allowed)
                rows.append([z["label"], fmt_bbox(z["bbox"]), f"{z.get('occupied_cells', 0)}/{z['cell_count']}",
                             f"{z.get('roofed_cells', '—')}/{z['cell_count']}", st.get("priority") or "—",
                             f"{len(allowed)} def" + (f" ({kinds['xác']} loại xác)" if kinds["xác"] else "")
                             + (f"; cấm: {', '.join(st.get('disallowedSpecialFilters') or [])}" if st.get("disallowedSpecialFilters") else ""),
                             fmt_rel(mp, ((z["bbox"][0] + z["bbox"][1]) // 2, (z["bbox"][2] + z["bbox"][3]) // 2)) if z["bbox"] else "—",
                             ", ".join(f"{k}×{v}" for k, v in contents.most_common(10)) or "trống"])
            d.table(["Zone", "Bao", "Ô đã dùng", "Ô có mái", "Ưu tiên", "Cho phép", "Cách tâm căn cứ", "Đang chứa"], rows)

        # 7 ---------------------------------------------------------------
        d.h(2, "7. Trồng trọt")
        grow = [z for z in mp["zones"] if "Growing" in z["class"]]
        if grow:
            rows = []
            for z in grow:
                gr = (f"{pct(z['crop_growth_min'])}–{pct(z['crop_growth_max'])} (TB {pct(z['crop_growth_avg'])}), chín: {z['crop_mature']}"
                      if z.get("crop_count") else "—")
                rows.append([z["label"], f"`{z['plantDefToGrow']}`", z["cell_count"], fmt_bbox(z["bbox"]),
                             f"**{z.get('crop_count', 0)}**", gr,
                             ", ".join(f"{k}×{v}" for k, v in (z.get("other_plants") or {}).items()) or "—",
                             ", ".join(f"{k}×{v}" for k, v in (z.get("soil") or {}).items()) or "—",
                             ("gieo: có" if z["allowSow"] else "gieo: TẮT") + (", cắt: có" if z["allowCut"] else ", cắt: TẮT"),
                             fmt_rel(mp, ((z["bbox"][0] + z["bbox"][1]) // 2, (z["bbox"][2] + z["bbox"][3]) // 2)) if z["bbox"] else "—"])
            d.table(["Ruộng", "Cây đặt trồng", "Số ô", "Bao", "Số cây trồng hiện có", "Độ lớn", "Cây dại mọc lẫn", "Đất",
                     "Cho phép", "Cách tâm căn cứ"], rows)
        else:
            d.p("*(chưa có ruộng nào)*")
        wild = mp["plants_wild"]
        useful = {k: v for k, v in wild.items() if k in ("Plant_Berry", "Plant_HealrootWild", "Plant_Ambrosia", "Plant_TreeAnima")}
        trees = sum(v for k, v in wild.items() if "Tree" in k)
        d.p(f"Thực vật hoang trên map: {sum(wild.values()):,} cây, trong đó {trees:,} cây gỗ"
            + (", " + ", ".join(f"`{k}`×{v}" for k, v in useful.items()) if useful else "") + ".")

        # 8 ---------------------------------------------------------------
        d.h(2, "8. Việc đã đánh dấu (designations)")
        rows = designation_summary(mp)
        if rows:
            d.table(["Lệnh", "Mục tiêu", "SL", "Phạm vi", "Gần căn cứ nhất", "Thuộc việc"], rows)
        else:
            d.p("*(không có lệnh nào đang chờ)*")

        # 12 (đặt trước nghiên cứu/quest trong vòng map vì phụ thuộc map) ----
        d.h(2, "9. Mối đe doạ & địa điểm đáng chú ý trên map")
        if mp["lords"]:
            d.h(3, "Nhóm pawn do AI điều khiển (lord)")
            rows = []
            for lord in mp["lords"]:
                rows.append([lord["id"], lord["faction_name"], lord["faction_relation"] or "—", f"`{lord['job_class']}`",
                             ", ".join(f"{k}={v}" for k, v in lord["job_fields"].items()) or "—",
                             "; ".join(f"{x['def']}{' «' + x['name'] + '»' if x['name'] else ''} {fmt_pos(x['pos'])}" for x in lord["pawns"]),
                             fmt_rel(mp, lord["pawns"][0]["pos"]) if lord["pawns"] else "—"])
            d.table(["Lord", "Phe", "Quan hệ", "Kiểu hành vi", "Tham số", "Thành viên", "Cách căn cứ"], rows)
        if mp["mechs"]:
            d.table(["Mech", "Ô", "Phe", "Trạng thái", "Trong sương mù", "Cách căn cứ"],
                    [[f"`{m['def']}`", fmt_pos(m["pos"]), m["faction_name"],
                      ("ngủ đông (dormant)" if m["dormant"] else "hoạt động") + f", job `{m['job']}`, duty `{m['duty']}`",
                      "có" if m.get("fogged") else "không", fmt_rel(mp, m["pos"])] for m in mp["mechs"]])
        others = [r for r in mp["rooms"] if not r["is_base"]]
        if others:
            d.h(3, "Vùng kín khác trên map (phế tích, hầm cổ…)")
            block_rooms(d, mp, base_only=False)
        d.h(3, "Công trình không phải của bạn")
        block_other_buildings(d, mp)
        a = state.get("anomaly")
        if a:
            d.p(f"**Anomaly:** cấp `{a['levelDef']}` · monolith `{a['monolith']}` · kiến thức từ monolith {a.get('monolithAnomalyKnowledge')}.")

        # 10 --------------------------------------------------------------
        d.h(2, "10. Động vật")
        tame = [x for x in mp["animals"] if x["faction"] == save.player_faction]
        d.p(f"{len(mp['animals'])} con trên map, trong đó {len(tame)} con đã thuần của bạn.")
        if tame:
            d.table(["ID", "Loài", "Tên", "Ô", "Thức ăn", "Chủ"],
                    [[x["id"], x["def"], x["name"] or "—", fmt_pos(x["pos"]), fmt_num(x["hunger"], 2), x["master"] or "—"] for x in tame])
        hunt = Counter(x["target_def"] for x in mp["designations"] if x["def"] == "Hunt")
        sp = defaultdict(list)
        for x in mp["animals"]:
            if x["faction"] != save.player_faction:
                sp[x["def"]].append(x)
        rows = []
        for defn, lst in sorted(sp.items(), key=lambda kv: -len(kv[1])):
            nearest = min(lst, key=lambda x: rel_to_base(mp, x["pos"])[0] or 0)
            flags = []
            if defn in PREDATOR_DEFS:
                flags.append("THÚ SĂN MỒI")
            if hunt.get(defn):
                flags.append(f"đã đánh dấu săn ×{hunt[defn]}")
            ms = [x for x in lst if x.get("mentalState")]
            if ms:
                flags.append(f"{len(ms)} con `{ms[0]['mentalState']}`")
            hurt = sum(1 for x in lst if x["hediffs"])
            if hurt:
                flags.append(f"{hurt} con có thương tật")
            rows.append([f"`{defn}`", len(lst), f"{fmt_pos(nearest['pos'])} ({fmt_rel(mp, nearest['pos'])})",
                         f"thức ăn {fmt_num(nearest['hunger'], 2)}, {'ngủ' if nearest['asleep'] else 'job ' + str(nearest['job'])}",
                         "; ".join(flags)])
        d.table(["Loài (hoang)", "SL", "Con gần căn cứ nhất", "Trạng thái con đó", "Ghi chú"], rows)
        d.p("*«thức ăn» = mức dinh dưỡng đang có trong bụng (đơn vị dinh dưỡng; mức tối đa tuỳ kích cỡ loài, người = 1.0).*")

        # 11 --------------------------------------------------------------
        d.h(2, "11. Bản đồ")
        gs = mp.get("grids") or {}
        size = mp["size"] or (0, 0)
        total = size[0] * size[1] or 1
        if gs:
            d.kv([
                ("Kích thước", f"{size[0]} × {size[1]} ô"),
                ("Địa hình (số ô)", ", ".join(f"`{k}` {v:,}" for k, v in gs["terrain"].items())),
                ("Mái", ", ".join(f"`{k}` {v:,} ({ROOF_VI.get(k, k)})" for k, v in gs["roof"].items()) or "—"),
                ("Vách đá / quặng / đá vụn (lớp nén)", ", ".join(f"`{k}` {v:,}" for k, v in gs["rock"].items()) or "—"),
                ("Sương mù", f"{gs['fogged_cells']:,} ô chưa khám phá ({gs['fogged_cells'] / total:.1%})" if gs.get("fogged_cells") is not None else "—"),
                ("Ô nhiễm / tuyết", f"{gs.get('polluted_cells') or 0} ô ô nhiễm; tuyết: {'có' if gs.get('snow') else 'không'}"),
                ("Khí đang lơ lửng", gas_line(gs)),
                ("Tài nguyên sâu đã dò ra (cho khoan sâu)", deep_line(gs)),
                ("Khu vực (area)", ", ".join(f"{a['label'] or a['class']} {a['trueCount']} ô" + (f" [{fmt_bbox(a['bbox'])}]" if a.get("bbox") else "")
                                             for a in mp["areas"])),
                ("Đường cổ cắt mép map tại", ", ".join(fmt_pos(p) for p in mp["roads_edge_cells"]) or "—"),
            ])
        d.h(3, "11.1 Toàn cảnh map")
        text, note = ascii_overview_map(save, md, mp)
        d.p("```\n" + text + "\n```")
        d.p(note)
        d.h(3, "11.2 Mạch quặng")
        if mp["ores"]:
            d.table(["Quặng", "Số ô", "Bao", "Tâm", "Cách căn cứ", "Đã lộ", "Đã đánh dấu đào"],
                    [[f"`{o['def']}`" + ("" if o["hash_exact"] else " *"), o["cells"], fmt_bbox(o["bbox"]), fmt_pos(o["center"]),
                      f"{o['dist']} ô {o['bearing']}" if o["dist"] is not None else "—",
                      "có" if o["fogged_cells"] == 0 else ("một phần" if o["fogged_cells"] < o["cells"] else "KHÔNG (trong sương mù)"),
                      o["designated_cells"] or ""] for o in mp["ores"]])
            if any(not o["hash_exact"] for o in mp["ores"]):
                d.p("\\* tên def suy từ mã băm gần đúng (game +1 khi hai def trùng mã) — khớp với ô đã đánh dấu đào/quặng đào dở liền kề.")
        else:
            d.p("*(không thấy quặng)*")
        chunks = Counter(mp["chunks"])
        for k, v in (gs.get("rock") or {}).items():
            if k.startswith("Chunk"):
                chunks[k] += v
        if chunks:
            d.p("**Đá vụn/xỉ nằm trên mặt đất** (vật liệu xây/đẽo gạch): " + ", ".join(f"`{k}`×{v}" for k, v in chunks.most_common()) + ".")
        geysers = [b for b in mp["buildings_other"] if b["def"] == "SteamGeyser"]
        if geysers:
            d.p("**Mạch nước nóng:** " + ", ".join(f"{fmt_pos(b['pos'])} ({fmt_rel(mp, b['pos'])})" for b in geysers) + ".")
        fish = [wb for wb in mp["water_bodies"] if wb["shouldHaveFish"]]
        if mp["water_bodies"]:
            d.p(f"**Vùng nước:** {len(mp['water_bodies'])} vùng; có cá: "
                + (", ".join(f"gốc {fmt_pos(wb['rootCell'])} {wb['cells']} ô, quần thể {fmt_num(wb['population'], 1)}, "
                             f"{'/'.join(wb['commonFish']) or '?'} ({fmt_rel(mp, wb['rootCell'])})" for wb in fish) or "không") + ".")

        # 12 --------------------------------------------------------------
        d.h(2, "12. Xác chết trên map")
        if mp["corpses"]:
            groups = defaultdict(list)
            for c in mp["corpses"]:
                groups[(c["zone"] or "ngoài zone", c["rot_stage"])].append(c)
            rows = []
            for (zone, stage), lst in sorted(groups.items()):
                kinds = Counter(c["def"] for c in lst)
                poss = [c["pos"] for c in lst if c["pos"]]
                named = [f"{c['inner_name']} ({c['inner_faction'] or '—'}, chết {save.fmt_tick(c['timeOfDeath'], time=False)})"
                         for c in lst if c["def"] == "Corpse_Human"]
                rows.append([zone, ROT_STAGE_VI.get(stage, stage), len(lst), ", ".join(f"{k}×{v}" for k, v in kinds.items()),
                             fmt_bbox(bbox_of(poss)), fmt_rel(mp, poss[0]) if poss else "—", "; ".join(named)])
            d.table(["Nơi", "Tình trạng", "SL", "Loại", "Phạm vi", "Cách căn cứ", "Xác người"], rows)
            d.p("*Xác tươi (<2,5 ngày ở ≥10°C) → thối rữa (toả khí gây LungRot, 2,5–5 ngày) → khô. Xác mech không phân hủy.*")
        else:
            d.p("*(không có)*")

    # 13 research ---------------------------------------------------------
    r = state["research"]
    d.h(2, "13. Nghiên cứu")
    if r:
        cur = r.get("current")
        d.p(f"**Đang chọn:** " + (f"`{cur}` — đã tích luỹ {fmt_num(r.get('current_points') or 0, 1)} điểm" if cur else "chưa chọn dự án nào")
            + f". **Đã xong ({len(r['completed'])}):** " + (", ".join(f"`{k}`" for k in r["completed"]) or "—")
            + (". **Dở dang:** " + ", ".join(f"`{p['def']}` {fmt_num(p['progress'], 1)} điểm" for p in r["partial"]) if r["partial"] else "")
            + f". Còn {sum(1 for x in r['all'] if x['status'] == 'none')} dự án chưa đụng tới.")
        d.p("*Save chỉ lưu số điểm, không lưu chi phí hay cờ hoàn thành. Dự án có điểm là số nguyên tròn (game gán = chi phí khi xong) "
            "được coi là đã xong — suy luận, độ tin cậy cao.*")
        if r.get("anomaly_knowledge"):
            d.p("Kiến thức Anomaly: " + ", ".join(f"`{k}` {v}" for k, v in r["anomaly_knowledge"].items()))

    # 14 quests -----------------------------------------------------------
    d.h(2, "14. Nhiệm vụ")
    if state["quests"]:
        order = {"NotYetAccepted": 0, "Ongoing": 1}
        live = [q for q in state["quests"] if q["state"] in order]
        for q in sorted(live, key=lambda q: (order[q["state"]], -(q["appearanceTick"] or 0))):
            block_quest(d, save, q, level=3)
        done = [q for q in state["quests"] if q["state"] not in order]
        if done:
            d.h(3, "Nhiệm vụ đã kết thúc / hết hạn")
            d.table(["Nhiệm vụ", "Loại", "Kết cục", "Xuất hiện", "Ghi chú"],
                    [[f"«{q['name'] or q['root']}»", f"`{q['root']}`", q["state_vi"], save.fmt_tick(q["appearanceTick"]),
                      "; ".join(x for x in (
                          ("liên quan: " + ", ".join(f"{x['name']} ({x['where']})" for x in q["pawns"])) if q["pawns"] else "",
                          ("thưởng lẽ ra: " + " HOẶC ".join("; ".join(o) for o in q["rewards"])) if q["rewards"] and q["state"] == "EndedOfferExpired" else "",
                      ) if x)] for q in done])
    else:
        d.p("*(không có nhiệm vụ)*")

    # 15 factions ---------------------------------------------------------
    d.h(2, "15. Phe phái")
    w = state["world"]
    settle = {s["faction"]: s["count"] for s in w["objects"]["settlements_by_faction"]}
    rows = []
    for f in w["factions"]:
        if f["player"]:
            continue
        rel = next((x for x in f["relations"] if x["other"] == save.player_faction), {})
        rows.append([f["id"], f["name"], f"`{f['def']}`", rel.get("kind", "—"), rel.get("goodwill", "—"),
                     settle.get(f["id"], 0), f["leader_name"] or "—",
                     ", ".join(x for x in ("ẩn" if f.get("hidden") else "", "tạm thời" if f.get("temporary") else "",
                                           "đã bị diệt" if f.get("defeated") else "") if x)])
    rows.sort(key=lambda r: ({"Ally": 0, "Neutral": 1, "Hostile": 2}.get(r[3], 3), -(r[4] if isinstance(r[4], (int, float)) else 0)))
    d.table(["ID", "Tên", "Loại", "Quan hệ với bạn", "Thiện chí", "Số khu định cư", "Thủ lĩnh", "Ghi chú"], rows)
    if w["objects"]["special"]:
        bits = []
        plain = defaultdict(list)
        for o in w["objects"]["special"]:
            if o["questTags"] or o["def"] == "Settlement":
                bits.append(f"`{o['def']}`" + (f" «{o['name']}»" if o["name"] else "") + f" tại ô thế giới {o['tile']}"
                            + (f" [{', '.join(o['questTags'])}]" if o["questTags"] else " (khu định cư của bạn)"))
            else:
                plain[o["def"]].append(o)
        for defn, lst in plain.items():
            res = Counter(o["extra"].get("preciousResource") for o in lst if o["extra"].get("preciousResource"))
            facs = Counter(o["faction"] for o in lst if o["faction"])
            bits.append(f"`{defn}`×{len(lst)}"
                        + (f" (phe: {', '.join(facs)})" if facs else "")
                        + (f" (tài nguyên quý: {', '.join(f'{k}×{v}' for k, v in res.most_common())})" if res else ""))
        d.p("**Điểm đặc biệt trên bản đồ thế giới:** " + "; ".join(bits) + ".")
    if state.get("transport_ships"):
        d.p("**Tàu vận chuyển đang được game theo dõi:** " + "; ".join(
            f"`{s['thing']}` ({s['faction']}) [{', '.join(s['questTags'])}]" for s in state["transport_ships"]) + ".")

    # 16 timeline ---------------------------------------------------------
    d.h(2, "16. Dòng thời gian")
    letters = sorted([x for x in state["letters"] if x["tick"] is not None], key=lambda x: x["tick"])
    recent_cut = now - 5 * TICKS_PER_DAY
    d.h(3, "Thư (mọi thư từ đầu ván) và thông báo trong 5 ngày gần nhất")
    rows = []
    for x in letters:
        is_msg = x["class"] == "Message"
        if is_msg and x["tick"] < recent_cut:
            continue
        rows.append([x["date"], f"{(now - x['tick']) / TICKS_PER_DAY:.1f}",
                     ("thông báo" if is_msg else "THƯ") + (" (chưa đóng)" if x.get("unread") else ""),
                     x["def"] or "—", x["label"] or "", clean_text(x["text"], 240)])
    d.table(["Lúc", "Cách đây (ngày)", "Loại", "Mức", "Tiêu đề", "Nội dung"], rows)
    old = Counter()
    for x in letters:
        if x["class"] == "Message" and x["tick"] < recent_cut:
            old[re.sub(r"\d+", "N", clean_text(x["text"], 60))] += 1
    if old:
        d.p("Thông báo cũ hơn 5 ngày (gộp theo nội dung): " + "; ".join(f"«{k}» ×{v}" for k, v in old.most_common(12)) + ".")
    tales = state.get("tales") or []
    if tales:
        d.h(3, "Sự kiện đáng nhớ game ghi lại (tale)")
        cnt = Counter(t["def"] for t in tales)
        d.p("Tổng: " + ", ".join(f"`{k}`×{v}" for k, v in cnt.most_common()) + ".")
        key_defs = {"Raid", "Downed", "KilledBy", "KilledMelee", "KilledCapacity", "Hunted", "TradedWith", "TrainedAnimal",
                    "Stripped", "HeatstrokeRevealed", "LandedInPod", "TileSettled", "Captured", "Recruited", "BecameLover",
                    "Marriage", "Breakup", "IllnessRevealed", "DefeatedHostileFactionLeader", "KidnappedColonist", "Butchered",
                    "ManhunterPack", "Infestation", "MechCluster"}
        rows = []
        for t in tales:
            if t["def"] not in key_defs or t["tick"] is None:
                continue
            rows.append([t["date"], f"`{t['def']}`", tale_sentence(t)])
        d.table(["Lúc", "Loại", "Diễn biến"], rows[-45:])
        fights = defaultdict(lambda: {"n": 0, "weapons": Counter(), "first": None, "last": None})
        for t in tales:
            if state.get("battle_log"):
                break                       # đã có nhật ký chiến đấu chi tiết hơn ở dưới
            if t["def"] != "Wounded" or t["tick"] is None or now - t["tick"] > 5 * TICKS_PER_DAY:
                continue
            a = (t.get("first") or {}).get("name") or "?"
            b = (t.get("second") or {}).get("name")
            f = fights[(b or "không rõ/tai nạn", a)]
            f["n"] += 1
            f["weapons"][t.get("thing") or "tay không/khác"] += 1
            f["first"] = t["tick"] if f["first"] is None else min(f["first"], t["tick"])
            f["last"] = t["tick"] if f["last"] is None else max(f["last"], t["tick"])
        if fights:
            d.p("**Giao tranh 5 ngày gần nhất** (gộp các tale `Wounded`: ai gây thương tích cho ai, bao nhiêu lần, bằng gì): "
                + "; ".join(
                    f"{att} → {vic} ×{f['n']} ({', '.join(f'{k}×{v}' if v > 1 else k for k, v in f['weapons'].most_common())}; "
                    f"{save.fmt_tick(f['first'])}" + (f"–{save.fmt_tick(f['last']).split(' ')[-1]}" if f["last"] != f["first"] else "") + ")"
                    for (att, vic), f in sorted(fights.items(), key=lambda kv: kv[1]["first"])) + ".")

    block_battle_log(d, save, state, level=3)
    block_play_log(d, save, state, level=3)

    # 17 policies ---------------------------------------------------------
    d.h(2, "17. Chính sách đang dùng")
    pol = state["policies"]
    in_use = Counter(policy_label(p["drugPolicy"]) for mp in state["maps"] for p in colonists_of(mp))
    for dp in pol["drug"]:
        if dp["label"] not in in_use:
            continue
        ents = []
        for e in dp["entries"]:
            flags = [x for x, on in (("giải trí", e["allowedForJoy"]), ("khi nghiện", e["allowedForAddiction"]),
                                     ("theo lịch", e["allowScheduled"])) if on]
            ents.append(f"{e['drug']}: {'/'.join(flags) or 'cấm'}")
        d.p(f"**Chính sách thuốc «{dp['label']}»** ({in_use[dp['label']]} người dùng): " + "; ".join(ents) + ".")
    d.p("Chính sách có sẵn — thuốc: " + ", ".join(f"«{x['label']}»" for x in pol["drug"])
        + " · trang phục: " + ", ".join(f"«{x['label']}»" for x in pol["outfit"])
        + " · ăn uống: " + ", ".join(f"«{x['label']}»" for x in pol["food"]) + ".")

    # 18 caveats ----------------------------------------------------------
    d.h(2, "18. Giới hạn của dữ liệu")
    tz_note = ("múi giờ suy từ tick bắt đầu ván và kiểm chứng bằng tick reset XP lúc nửa đêm của pawn"
               if date.get("tz_source") == "pawn+start" else f"múi giờ lấy theo: {date.get('tz_source')}")
    d.p("- File save **không lưu** các giá trị game tự tính lúc chạy: chỉ số phòng (ấn tượng/đẹp/sạch), tốc độ di chuyển, "
        "mức đau, năng lực cơ thể (Consciousness, Moving…), tốc độ chảy máu, HP tối đa, điện lưới, vùng phủ sáng, "
        "và các *thought tình huống* (đau, phòng xấu, thiếu giải trí, nghiện…). Mục «ký ức» ở trên chỉ gồm thought dạng ký ức.\n"
        "- Giới tính: game chỉ ghi khi khác `Male`; không có thẻ nghĩa là Male.\n"
        f"- Ngày giờ: {tz_note}.\n"
        "- Bảng nghiên cứu, ngưỡng thối của thực phẩm/xác, dinh dưỡng, ngưỡng tâm trạng: dựa trên giá trị def **vanilla** "
        "(mod có thể thay đổi).\n"
        "- Phòng, mạch quặng, khoảng cách, cảnh báo ở mục 2: do công cụ suy ra từ dữ liệu thô (không phải do game ghi).\n"
        "- Tên def của địa hình/đá/mái được tra ngược từ mã băm; mã không nhận ra sẽ hiện dạng `Terrain#12345`."
        + ("\n- Mã băm chưa nhận ra: " + ", ".join(f"{k} ({v} ô)" for mp in state["maps"] for k, v in ((mp.get("grids") or {}).get("hash_unknown") or {}).items())
           if any((mp.get("grids") or {}).get("hash_unknown") for mp in state["maps"]) else ""))
    toc = " · ".join(ln[3:] for ln in d.lines if ln.startswith("## ") and not ln.startswith("## 0."))
    return d.text().replace("@@TOC@@", toc)


def latest_room_stats(state):
    """Chỉ số phòng (do game tính) lấy từ 'surroundings' của tale mới nhất theo từng loại phòng."""
    out = {}
    for t in state.get("tales") or []:
        s = t.get("surroundings")
        if not s or s.get("roomRole") in (None, "", "None") or s.get("roomImpressiveness") is None:
            continue
        cur = out.get(s["roomRole"])
        if cur is None or (t["tick"] or 0) > cur["tick"]:
            out[s["roomRole"]] = dict(s, tick=t["tick"] or 0, date=t["date"])
    return out


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
    health = []
    zone_cells = []
    terrain = []

    for md in save.maps:
        mp = state["maps"][md.index]
        zone_of = md.zone_lookup
        g = md.grids
        if g is not None and g.terrain is not None:
            home = g.areas.get("Area_Home")
            for z_ in range(g.h):
                base = z_ * g.w
                for x_ in range(g.w):
                    i = base + x_
                    terrain.append([
                        mp["index"], x_, z_, g.terrain[i] or "",
                        (g.under[i] or "") if g.under is not None else "",
                        (g.roof[i] or "") if g.roof is not None else "",
                        (g.rock[i] or "") if g.rock is not None else "",
                        (1 if g.fog[i] else 0) if g.fog is not None else "",
                        (1 if home[i] else 0) if home is not None else "",
                        f"{g.temp[i]:.1f}" if g.temp is not None else "",
                    ])
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
            for h in pw["hediffs"]:
                health.append([pw["id"], pw["name"], h["def"], h["name"], h["class"],
                               h["severity"] if h["severity"] is not None else "",
                               h["part_index"] if h["part_index"] is not None else "", h["part_name"] or "",
                               h["tend"] or "", h["tendQuality"] if h["tendQuality"] is not None else "",
                               h["tendTicksLeft"] if h["tendTicksLeft"] is not None else "",
                               h["isPermanent"] or "", h["age_ticks"] if h["age_ticks"] is not None else "",
                               h.get("source") or "", h.get("sourceTool") or "", h.get("combatLog") or ""])

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
    write_csv(outdir / "pawns_health.csv",
              ["pawn_id", "pawn", "hediff", "name", "class", "severity", "part_index", "part", "tend",
               "tend_quality", "tend_ticks_left", "permanent", "age_ticks", "source", "source_tool", "combat_log"], health)
    write_csv(outdir / "zones_cells.csv",
              ["map", "zone", "type", "x", "z"], zone_cells)
    if terrain:
        write_csv(outdir / "terrain.csv",
                  ["map", "x", "z", "terrain", "under_terrain", "roof", "rock_or_ore", "fogged", "home_area", "temp_c"], terrain)


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
    ap.add_argument("--ai-only", metavar="FILE",
                    help="chỉ ghi DUY NHẤT bản state cho AI ra FILE (tự chứa đủ, không nhắc tới file phụ); bỏ qua -o")
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

    if args.ai_only:
        ai = render_ai_state(save, state, standalone=True)
        target = Path(args.ai_only)
        if target.parent != Path(""):
            target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(ai, encoding="utf-8")
        print(f"  → {target} ({len(ai):,} ký tự, {len(ai.encode('utf-8')):,} byte)")
        print(f"  {state['game']['date']['display']} · {len(state['alerts'])} cảnh báo "
              f"({sum(1 for a in state['alerts'] if a['sev'] == 3)} khẩn) · "
              f"{sum(len(mp['unclassified']) for mp in state['maps'])} object chưa phân loại")
        return 0

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

    ai = render_ai_state(save, state)
    (outdir / "ai_state.md").write_text(ai, encoding="utf-8")
    print(f"  → {outdir / 'ai_state.md'} ({len(ai):,} ký tự) ← FILE ĐƯA CHO AI ĐỌC")

    md = render_markdown(save, state)
    (outdir / "report.md").write_text(md, encoding="utf-8")
    print(f"  → {outdir / 'report.md'} ({len(md):,} ký tự)")

    if args.raw:
        for old in outdir.glob("pawn_*.xml"):     # xoá XML của lần chạy trước (pawn có thể đã rời map)
            old.unlink()
        for mp in state["maps"]:
            for pw in mp["pawns"]:
                el = save.things_by_id.get("Thing_" + pw["id"])
                if el is None:
                    continue
                raw_path = outdir / f"pawn_{pw['id']}.xml"
                raw_path.write_text(ET.tostring(el, encoding="unicode"), encoding="utf-8")
        print(f"  → XML gốc của pawn trong {outdir}")

    print(f"  {state['game']['date']['display']} · {len(state['alerts'])} cảnh báo "
          f"({sum(1 for a in state['alerts'] if a['sev'] == 3)} khẩn)")
    for mp in state["maps"]:
        print(f"  map {mp['index']}: {len(mp['pawns'])} pawn · {len(mp['buildings_player'])} công trình "
              f"· {len(mp['construction'])} bản vẽ · {len(mp['items'])} stack · {len(mp['animals'])} động vật "
              f"· {len(mp['mechs'])} mech · {sum(mp['plants_wild'].values())} cây hoang "
              f"· {len(mp['zones'])} zone · {len(mp['unclassified'])} chưa phân loại")
    return 0


if __name__ == "__main__":
    sys.exit(main())
