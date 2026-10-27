# rimworld_dump.py — đọc save RimWorld và xuất TOÀN BỘ state

Công cụ Python 3 (chỉ dùng thư viện chuẩn), đọc file `.rws` (XML) và ghi ra **Markdown + JSON + CSV**.
Không tóm tắt, không bỏ mục nào: mọi object trên map, mọi skill/need/thought/hediff/work-priority của pawn,
mọi ô của từng zone, mọi stack vật phẩm, mọi cây (kể cả cây hoang).

## Chạy

```bash
# cơ bản (xuất vào ./dump)
python3 tools/rimworld_dump.py "vãi ò.rws"

# đổi thư mục ra
python3 tools/rimworld_dump.py "vãi ò.rws" -o out

# chỉ Markdown (không JSON/CSV)
python3 tools/rimworld_dump.py "vãi ò.rws" --md-only

# kèm XML gốc từng pawn + bỏ bảng "toàn bộ trường XML" cho gọn
python3 tools/rimworld_dump.py "vãi ò.rws" --raw --no-full-fields

# tuỳ chỉnh ánh xạ thứ tự work type (nếu bản game của bạn khác)
python3 tools/rimworld_dump.py save.rws --worktypes my_worktypes.json
```

Script **chỉ đọc** file save; không bao giờ ghi/sửa `.rws`.

## Kết quả

| File | Nội dung |
|---|---|
| `report.md` | Báo cáo đầy đủ 19 mục, dễ đọc |
| `state.json` | Toàn bộ state dạng máy đọc (kể cả mọi trường XML của pawn) |
| `things_all.csv` | **Mọi** object trên map (25.481 dòng với save này) |
| `plants.csv` | Mọi cây (21.891 dòng, gồm cây hoang + cây chết) |
| `items.csv` | Mọi stack vật phẩm rời |
| `buildings.csv` | Mọi công trình (của bạn và của map) |
| `pawns_skills.csv` | Skill từng pawn |
| `pawns_needs.csv` | Nhu cầu từng pawn |
| `pawns_work.csv` | 23 ưu tiên công việc từng pawn |
| `zones_cells.csv` | Từng ô của từng zone |
| `pawn_*.xml` | XML gốc từng pawn (khi dùng `--raw`) |

## Báo cáo Markdown gồm

0. Nguồn & mod
1. Tổng quan game (ngày, tick, kịch bản, storyteller, difficulty, thống kê đột kích)
2. Thế giới & phe (quan hệ + thiện chí với từng phe)
3. Tôn giáo: mọi tín điều, meme, chức danh, deity
4. Nghiên cứu: đang làm, đã xong, **toàn bộ bảng 124 dự án**
5. **PAWN đầy đủ**: hồ sơ, tính cách, 12 skill, 9 nhu cầu, mọi suy nghĩ/ký ức (13–14 cái/pawn),
   sức khỏe, trang bị + hành trang, 23 ưu tiên công việc, chính sách, lịch 24h, job hiện tại
6. Động vật (kể cả thú hoang)
7. Công trình: tổng hợp theo loại + chi tiết từng cái + sơ đồ ASCII khu căn cứ
8. Môi trường: thời tiết, biome, area (Home, BuildRoof), rác, khối đá, thống kê theo lớp object
9. Zone: số ô, bbox, cây trồng, **danh sách 826 def được phép**, nội dung thực tế trong zone
10. Vật phẩm: tổng hợp theo loại + từng stack
11. Cây: cây trồng (từng cây) + cây hoang (theo loài, min/avg/max độ lớn)
12. Designation: Haul / CutPlant / HarvestPlant …
13. Xác chết (kèm tên pawn bên trong)
14. Nhật ký/thư: 30 sự kiện
15. Nhiệm vụ (quest + các phần)
16. Anomaly (monolith, level)
17. World pawn: 23 pawn còn sống ngoài map + 18 pawn đã chết
18. **Kiểm tra độ phủ**: chứng minh mọi object đều được phân loại (save này: 25.479/25.481)
19. Danh sách file xuất kèm

## Ghi chú kỹ thuật

- **Tên tiếng Việt**: script có từ điển cho def phổ biến (skill, need, trait, thought, hediff, item,
  building, plant, backstory, research, zone). Def lạ sẽ được hiển thị bằng tên đã tách chữ
  (`Plant_TreeOak` → "Tree Oak") chứ không mất dữ liệu — tên gốc luôn nằm trong cột `Def`/`def`.
- **Giới tính**: save RimWorld không lưu `gender` cho colonist trên map (chỉ lưu cho world pawn),
  nên script suy ra từ `headType` (`Male_*` / `Female_*`) và ghi rõ là suy ra.
- **Thứ tự work type**: `workSettings/priorities/vals` là mảng theo thứ tự nạp def:
  Core 20 loại → Biotech `Childcare` → Anomaly `DarkStudy` → Odyssey `Fishing` (23 phần tử với save này).
  Đã kiểm chứng chéo: chỉ Nikolay bật Doctor, chỉ Anthony bật Warden và Research cao — khớp kỹ năng.
  Nếu bản game của bạn khác, xuất file JSON và dùng `--worktypes`.
- **Zone ID**: `ID` trong zone là số thứ tự nội bộ, còn `Ideo_12` là **loadID** chứ không phải index —
  script tự dò loadID thật từ các tham chiếu trong save.
- **Biome**: không nằm trong `mapInfo`; script lấy từ `surroundings` của tale ứng với ô định cư.
- **Ảnh grid** (terrain/temperature/fog) trong save là deflate-base64; script không giải nén vì
  không cần cho các mục trên.

## Cấu trúc code

```
SaveFile      đọc XML, index thing theo ID, faction, ideo, world pawn, date
MapData       tách things / zones / areas / size của từng map
extract_*     biến XML -> dict (pawn, map, research, quest, letter, anomaly)
render_markdown / render_pawn_md / ascii_map   -> báo cáo
export_csvs   -> 8 file CSV
```

Thêm DLC/mod mới: chỉ cần bổ sung từ điển tên hoặc nhánh xử lý trong `extract_map`, mọi thứ khác
vẫn chạy vì script dựa trên cấu trúc XML chứ không hard-code danh sách def.
