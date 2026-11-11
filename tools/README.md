# rimworld_dump.py — đọc save RimWorld và xuất state (có bản dành cho AI)

Công cụ Python 3 (chỉ dùng thư viện chuẩn), đọc file `.rws` (XML) và ghi ra:

- **`ai_state.md`** — một file duy nhất để đưa cho AI: đọc xong là nắm được chuyện gì đang xảy ra
  (cảnh báo, từng người, việc, căn cứ, kho, ruộng, đe doạ, nhiệm vụ, dòng thời gian, nhật ký chiến đấu,
  nhật ký trò chuyện).
- **`report.md` / `state.json` / CSV** (chế độ đầy đủ, tuỳ chọn) — bản từng dòng để tra cứu: mọi object
  trên map, mọi skill/need/thought/hediff/work-priority của pawn, mọi ô của từng zone, mọi stack vật phẩm,
  mọi cây.

Script **chỉ đọc** file save; không bao giờ ghi/sửa `.rws`.

Hiện repo chỉ lưu **`ai_state.md` ở thư mục gốc** (tạo từ `Autosave-4.rws` bằng lệnh đầu tiên bên dưới);
thư mục `dump/` của chế độ đầy đủ không được giữ trong repo.

## Chạy

```bash
# ★ CHỈ ghi đúng 1 file cho AI (tự chứa đủ, không nhắc tới report/JSON/CSV), không tạo thư mục dump
python3 tools/rimworld_dump.py "Autosave-4.rws" --ai-only ai_state.md
```

Mỗi lần có save mới chỉ cần chạy lại lệnh trên với tên file save đó (khoảng 2–3 giây). Ngay dưới tiêu đề
của `ai_state.md` có ngày giờ trong game, tick, kích thước và mã SHA-1 của file save đã dùng — nhìn vào đó
là biết file có khớp với save hiện tại hay không (so với `sha1sum "Autosave-4.rws"`).

Chế độ đầy đủ (ghi thêm report, JSON, CSV — khoảng 7 MB — vào một thư mục):

```bash
# xuất vào ./dump (ghi đè bản cũ)
python3 tools/rimworld_dump.py "Autosave-4.rws"

# kèm XML gốc của từng người trên map
python3 tools/rimworld_dump.py "Autosave-4.rws" --raw

# đổi thư mục ra
python3 tools/rimworld_dump.py "Autosave-4.rws" -o out

# chỉ 2 file Markdown (ai_state.md + report.md)
python3 tools/rimworld_dump.py "Autosave-4.rws" --md-only

# Markdown + JSON, không CSV; bỏ bảng "toàn bộ trường XML" trong report cho gọn
python3 tools/rimworld_dump.py "Autosave-4.rws" --no-csv --no-full-fields

# tuỳ chỉnh ánh xạ thứ tự work type (nếu bản game của bạn khác)
python3 tools/rimworld_dump.py save.rws --worktypes my_worktypes.json
```

Tên file save có dấu cách hoặc dấu tiếng Việt (ví dụ `"vãi ò.rws"`) thì nhớ đặt trong dấu nháy kép.

## Đưa cho AI như thế nào

1. Dán hoặc đính kèm **`ai_state.md`** (≈ 100 KB, khoảng 89 nghìn ký tự — cỡ 30–45 nghìn token
   tuỳ mô hình). File tự giải thích: mục 0 nói cách đọc toạ độ, thời gian, defName và có mục lục.
2. Hỏi thẳng, ví dụ: *"Đây là trạng thái thuộc địa RimWorld của tôi. Việc gì cần làm trước?"*
3. Khi AI cần chi tiết hơn (từng ô, từng cây, mọi trường của một pawn) thì chạy chế độ đầy đủ rồi đưa
   thêm `report.md`, `state.json` hoặc file CSV tương ứng.

Lưu ý: file save chứa cả thứ **người chơi chưa nhìn thấy** (vùng còn sương mù, bên trong kén ngủ đông
cổ). `ai_state.md` luôn ghi rõ «trong sương mù» ở những chỗ đó.

## Kết quả

`--ai-only FILE` chỉ ghi đúng một file (`ai_state.md`). Chế độ đầy đủ ghi các file sau vào thư mục ra:

| File | Nội dung | Số dòng với `Autosave-4.rws` |
|---|---|---|
| **`ai_state.md`** | ★ Bản cô đọng cho AI, 19 mục (0–18) | 905 |
| `report.md` | Báo cáo đầy đủ, mục ★ + 0–20 | 5.8k |
| `state.json` | Toàn bộ state dạng máy đọc (kể cả mọi trường XML của pawn) | — |
| `things_all.csv` | **Mọi** object trên map | 25.801 |
| `terrain.csv` | Địa hình / nền dưới / mái / đá-quặng / sương mù / Home / nhiệt độ của **từng ô** | 62.500 |
| `plants.csv` | Mọi cây (gồm cây hoang + cây chết) | 22.133 |
| `items.csv` | Mọi stack vật phẩm rời | 118 |
| `buildings.csv` | Mọi công trình (của bạn và của map) | 647 |
| `pawns_skills.csv` | Kỹ năng từng người | 48 |
| `pawns_needs.csv` | Nhu cầu từng người | 36 |
| `pawns_work.csv` | Ưu tiên công việc từng người | 69 |
| `pawns_health.csv` | Từng vết thương / bệnh / cấy ghép của từng người | 28 |
| `zones_cells.csv` | Từng ô của từng zone | 635 |
| `pawn_<id>.xml` | XML gốc của từng người trên map (khi dùng `--raw`) | 4 file |

`ai_state.md` của hai chế độ giống hệt nhau, chỉ khác hai dòng ở phần đầu (bản `--ai-only` không nhắc tới
các file phụ).

## `ai_state.md` gồm

0. Cách đọc file (toạ độ, đơn vị thời gian, defName, thông tin trong sương mù) và mục lục
1. Ảnh chụp nhanh: ngày giờ, mùa, dân số, đột kích và mối đe doạ lớn gần nhất, thời tiết + biên độ nhiệt 5 ngày,
   tài sản, tâm trạng
2. **Việc cần chú ý ngay** — cảnh báo tự rà, 3 mức KHẨN / QUAN TRỌNG / lưu ý, mỗi dòng kèm số liệu gốc
3. Con người trên map: bảng tóm tắt + hồ sơ từng người (đang làm gì, tâm trạng, nhu cầu, ký ức,
   sức khoẻ từng vết thương, kỹ năng, trang bị, quan hệ, lịch, chính sách)
4. Ma trận công việc: ai bật việc gì, mức ưu tiên, việc nào không ai làm
5. Căn cứ: sơ đồ ASCII, từng phòng (vai trò, nhiệt độ, giường, đồ đạc), công trình, bàn chế tạo + bill, bản vẽ chưa xây
6. Kho & tài nguyên, ước tính số ngày lương thực
7. Trồng trọt: từng ruộng, cây gì, bao nhiêu cây, lớn tới đâu
8. Việc đã đánh dấu (chặt / thu hoạch / săn / đào / tháo dỡ)
9. Mối đe doạ & địa điểm đáng chú ý: mech ngủ đông, hầm cổ, kén ngủ đông, vật quý ngoài căn cứ
10. Động vật (hoang + đã thuần), thú săn mồi gần căn cứ
11. Bản đồ: sơ đồ toàn map, địa hình, mái, sương mù, khí, mạch quặng, khu vực, vùng nước
12. Xác chết: của ai, ở đâu, tươi / đang thối / đã khô
13. Nghiên cứu
14. Nhiệm vụ: chưa nhận (hạn, thưởng, người liên quan + quan hệ với người trên map), đang chạy, đã kết thúc
15. Phe phái, thiện chí, điểm đặc biệt trên bản đồ thế giới
16. Dòng thời gian: mọi thư, thông báo 5 ngày gần nhất, sự kiện game ghi (tale),
    **nhật ký chiến đấu** (`battleLog`: từng trận ai bắn/đánh ai bằng gì, bao nhiêu phát, trúng bao nhiêu,
    ai gục/chết; kèm thành tích từng người) và **nhật ký tương tác xã hội** (`playLog`: 150 lần trò chuyện /
    xúc phạm / huấn luyện gần nhất, đếm theo từng cặp)
17. Chính sách thuốc / trang phục / ăn uống
18. Giới hạn của dữ liệu (những gì file save không lưu, những gì là suy luận)

## `report.md` gồm

★. Cảnh báo tự động · 0. Nguồn & mod · 1. Tổng quan game · 2. Thế giới & phe · 3. Tôn giáo ·
4. Nghiên cứu (toàn bộ bảng dự án) · 5. PAWN đầy đủ + ma trận công việc · 6. Động vật, mech & nhóm AI ·
7. Công trình, phòng, sơ đồ · 8. Môi trường / địa hình / quặng / khu vực / rác · 9. Vùng (zone) ·
10. Vật phẩm trên map · 11. Cây trồng & thảm thực vật · 12. Đánh dấu (designations) · 13. Xác chết ·
14. Nhật ký / thư / sự kiện (gồm nhật ký chiến đấu và toàn bộ 150 dòng tương tác xã hội) · 15. Nhiệm vụ ·
16. Anomaly · 17. Pawn ngoài map ·
18. **Kiểm tra độ phủ** (`Autosave-4.rws`: 25.801/25.801 object đã phân loại, 0 chưa phân loại) ·
19. Số liệu lịch sử & chính sách · 20. File dữ liệu kèm theo

## Ghi chú kỹ thuật

- **Ngày giờ**: `tickManager/ticksGame` là số tick đã chơi; ngày tuyệt đối = `gameStartAbsTick + ticksGame`,
  cộng thêm múi giờ của ô bản đồ. Game đặt `gameStartAbsTick = 300000·quý + 2500·(6 + (24 − múi giờ) mod 24)`
  để ván bắt đầu lúc 06:00 giờ địa phương, nên suy ngược được múi giờ (save này: UTC-3). 1 giờ = 2.500 tick,
  1 ngày = 60.000 tick, 1 quý = 15 ngày. Bản công cụ cũ bỏ qua hai thứ này nên in sai ngày.
- **Lưới nén**: `terrainGrid`, `roofGrid`, `fogGrid`, `compressedThingMapDeflate`, `temperatureCache`,
  `snowGrid`, `gasGrid`, `deepResourceGrid`, `areaManager/…/innerGrid` là base64 của **raw deflate**
  (`zlib.decompress(raw, -15)`), chỉ số ô = `z·rộng + x`. Lưới ushort chứa *short hash* của def;
  lưới bool đóng gói 8 ô/byte, bit thấp trước; nhiệt độ = `(v − 32768)/16` °C;
  lưới khí là 4 byte/ô (BlindSmoke, ToxGas, RotStink, DeadlifeDust). Ở cả hai save đã thử, lưới khí và lưới
  tài nguyên sâu toàn số 0, nên hai phần giải mã này mới chỉ được thử bằng dữ liệu giả lập.
- **Short hash**: `(ushort)(StableStringHash(defName) % 65535)` với `h = 23; h = h·31 + ký_tự` (int32 tràn số).
  Công cụ băm sẵn danh sách tên def vanilla + DLC để tra ngược. Khi hai def trùng hash, game cộng 1 cho def
  nạp sau (ví dụ `MineableSteel` băm ra 27292 nhưng save lưu 27293) — công cụ cho phép lệch nhỏ và ghi lại
  ở `grids.hash_inexact`. Mã không nhận ra hiện dạng `Terrain#12345` và được liệt kê ở mục 18 của `ai_state.md`.
- **Vách đá và quặng** không nằm trong `<things>` mà nằm trong lưới nén ở trên; mạch quặng do công cụ tự gom
  các ô liền nhau.
- **Phòng**: game không lưu. Công cụ loang tìm vùng kín (bao bởi tường, đá, cửa), suy vai trò từ đồ đạc,
  lấy nhiệt độ từ lưới nhiệt. Chỉ số ấn tượng/đẹp/sạch thì không có trong save.
- **Nghiên cứu**: `researchManager/progress` lưu **điểm thô** (không phải tỉ lệ, không có cờ "đã xong").
  Khi xong, game gán điểm bằng đúng chi phí gốc (số nguyên tròn), còn tiến độ dở dang là số lẻ — nên điểm > 0,
  là số nguyên và không phải dự án đang chọn thì công cụ coi là đã xong (suy luận, có ghi rõ trong file).
  Bản công cụ cũ đem điểm này nhân 100 thành phần trăm nên ra các con số kiểu "30000%".
- **Vai trò của người**: suy từ `faction`, `guest/hostFaction` và `guest/guestStatus`
  (thuộc địa viên / khách / tù nhân / nô lệ / kẻ địch). `guest/joinStatus` là giá trị mặc định, không dùng.
- **Giới tính**: game chỉ ghi `<gender>` khi khác `Male`; không có thẻ nghĩa là nam.
- **Bộ phận cơ thể**: hediff lưu chỉ số bộ phận; công cụ có bảng thứ tự bộ phận của cơ thể người để ra tên.
- **Nhóm AI (lord)**: `lordManager` cho biết nhóm nào đang làm gì (ví dụ mech `LordJob_SleepThenAssaultColony`).
  Mech được tách khỏi danh sách động vật.
- **Nhiệm vụ**: trạng thái lấy từ `acceptanceTick`, `ended`, `endOutcome`, `acceptanceExpireTick`; người liên quan
  được dò trong world pawn (phần tử `<li>` có `kindDef`), kèm quan hệ với người đang ở trên map.
- **Tale**: mỗi sự kiện game ghi kèm `surroundings` (nhiệt độ, loại phòng lúc đó) — công cụ dùng để lấy biên độ
  nhiệt mấy ngày gần nhất, vì nhiệt độ trong save chỉ là tại thời điểm lưu. Tên trong tale là tên lúc xảy ra;
  công cụ đổi sang biệt danh hiện tại nếu pawn còn tồn tại. Trong tale `Wounded`: `first` là nạn nhân,
  `second` là kẻ gây thương tích.
- **Nhật ký chiến đấu** (`game/battleLog`): game gom các dòng gần nhau thành «trận». Loại dòng:
  `RangedFire` (một lần bóp cò), `RangedImpact` (mỗi viên đạn rơi vào đâu: `recipientPawn` nếu trúng người/thú,
  `recipientThing` nếu găm vào cây/tường/đá, cả hai rỗng là trượt hẳn), `MeleeCombat` (một đòn cận chiến;
  trúng / trượt / né / bị giáp chặn nằm ở đuôi `ruleDef`), `StateTransition` (gục / chết, kèm ai gây ra và hediff
  gây ra), `Event` (choáng), `ExplosionImpact`. Công cụ gộp theo cặp (ai → ai, bằng gì).
  `ticksAbs` là tick tuyệt đối (trừ `gameStartAbsTick` ra tick ván).
  Hai nhánh mới chỉ được thử bằng dữ liệu giả lập vì hai save đã thử không có trường hợp đó: súng bắn loạt
  (`RangedFire` có `burst=True` — một dòng cho cả loạt, nên số trúng tính theo viên chứ không theo lần bắn) và
  pawn được nhắc trong log nhưng không còn trong save (khi đó chỉ suy được loài từ ID, ví dụ
  `Thing_WildBoar75683` → `WildBoar`). Ở hai save đã thử, mọi pawn trong log đều còn tra được tên.
- **Nhật ký tương tác xã hội** (`game/playLog`): game chỉ giữ 150 dòng mới nhất (`intDef`, người mở lời,
  người nghe, `ticksAbs`).
- **Ký ức xã hội** (`Thought_MemorySocial` có `otherPawn`): là ký ức VỀ việc pawn kia đã làm (ví dụ
  `AteRawHumanlikeMeat` → một con quạ ăn xác người), không phải việc của chính người mang ký ức.
- **Lịch sử**: `history/autoRecorderGroups` là base64 của float32, mỗi mẫu cách 30.000 tick (tài sản, tâm trạng…).
- **Thứ tự work type**: `workSettings/priorities/vals` là mảng theo thứ tự nạp def:
  Core 20 loại → Biotech `Childcare` → Anomaly `DarkStudy` → Odyssey `Fishing` (23 phần tử với save này).
  Nếu bản game của bạn khác, xuất file JSON và dùng `--worktypes`.
- **Tên tiếng Việt**: script có từ điển cho def phổ biến. Def lạ sẽ được hiển thị bằng tên đã tách chữ
  (`Plant_TreeOak` → "Tree Oak") chứ không mất dữ liệu — tên gốc luôn nằm trong cột `Def`/`def`.
- **Ước tính** (ghi rõ trong file): số ngày lương thực, thời điểm thức ăn/xác bắt đầu hỏng, ngưỡng tâm trạng
  35/20/5% — đều theo giá trị def vanilla, mod có thể làm lệch.

## Cấu trúc code

```
short_hash / MapGrids      giải mã các lưới nén theo ô
SaveFile                   đọc XML, index thing theo ID, phe, ideo, world pawn, ngày giờ
MapData                    tách things / zones / areas / lưới của từng map
extract_*                  XML -> dict (pawn, map, lord, research, quest, letter, tale, history, policy,
                           battle_log, play_log)
detect_rooms / find_ore_clusters / summarize_food   phần công cụ tự suy ra
derive_alerts              rà cảnh báo theo quy tắc
render_ai_state            -> ai_state.md   (dùng các block_* và ascii_*_map; standalone=True khi --ai-only)
render_markdown / render_pawn_md   -> report.md
export_csvs                -> 10 file CSV
```

Công cụ mới được chạy trên hai save thật của cùng một ván (`vãi ò.rws` và `Autosave-4.rws`, bản 1.7 + 5 DLC)
và trên các biến thể cố ý làm hỏng từ hai save đó (thiếu mục, thiếu trường, 2 map, tù nhân/nô lệ/kẻ địch,
thú đã thuần, nhật ký thiếu trường hoặc trỏ tới pawn không còn…). Save từ bản game khác hoặc nhiều mod có thể
cần bổ sung bảng tên.

Thêm DLC/mod mới: bổ sung tên def vào các bảng ở đầu file (để tra ngược hash và hiện tên tiếng Việt) hoặc
thêm nhánh xử lý trong `extract_map`. Mọi thứ khác vẫn chạy vì script dựa trên cấu trúc XML chứ không
hard-code danh sách def; object lạ sẽ rơi vào mục «chưa phân loại» của phần kiểm tra độ phủ chứ không biến mất.
