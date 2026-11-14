# TRẠNG THÁI THUỘC ĐỊA «nhung nguoi cung kho» — RimWorld 1.7.5000 rev1275

*Ảnh chụp tại **ngày 9 Aprimay năm 5501, 12:48** (tick 1,997,000, ngày chơi thứ 33.283). Sinh tự động từ file save `vãi ò.rws` (16,360,280 byte, SHA-1 `b33e1d480ddf27f0cc75f4a47141453e393340cd`) bằng script phân tích; không có nội dung nào do người viết tay. File chỉ đúng tại thời điểm lưu nói trên — nếu ván chơi đã đi tiếp (file save được lưu lại) thì bản này đã cũ.*


## 0. Cách đọc file này

- Đây là **ảnh chụp trạng thái** một ván RimWorld tại đúng thời điểm lưu. Mọi con số lấy trực tiếp từ file save; chỗ nào ghi *(suy luận)* / *(ước tính)* là do công cụ tính thêm, kèm giả định; chỗ nào ghi *(mặc định)* là giá trị game tự bỏ qua không ghi vào XML khi bằng đúng mặc định.
- **Toạ độ** `(x,z)`: gốc (0,0) ở góc Tây-Nam map; x tăng về **Đông**, z tăng về **Bắc**. Khoảng cách tính bằng ô.
- **Thời gian & lịch**: 1 giờ game = 2.500 tick, 1 ngày = 60.000 tick, **1 quý (tháng) chỉ có đúng 15 ngày** (từ ngày 1 đến ngày 15), 1 năm = 4 quý = 60 ngày theo thứ tự: Aprimay → Jugust → Septober → Decembary (ví dụ: sau ngày 15 Septober là ngày 1 Decembary — chỉ cách nhau 1 ngày, không phải vài tháng). Các bảng sự kiện đều có cột «Cách đây (ngày)» tính sẵn.
- Tên trong dấu `` ` `` là **defName** gốc của game (tiếng Anh) — dùng để tra wiki chính xác.
- Mức nhu cầu/tâm trạng là 0–100%. Ưu tiên việc: 1 = cao nhất … 4 = thấp nhất, 0 = tắt.
- Mục 2 là danh sách **việc cần chú ý** do công cụ tự rà theo quy tắc; các mục sau là dữ liệu đầy đủ để kiểm chứng.
- File save chứa cả những thứ **người chơi chưa nhìn thấy** (vùng còn sương mù, bên trong kén/hòm cổ). Các chỗ đó đều được ghi rõ «trong sương mù» — hãy coi là thông tin biết trước, người chơi trong game chưa có.
- File này **tự chứa đủ**, không kèm file phụ nào. Thứ duy nhất chi tiết hơn (từng ô đất, từng cây, mọi trường XML) là chính file save `vãi ò.rws`.
- **Mục lục:** 1. Ảnh chụp nhanh · 2. Việc cần chú ý ngay · 3. Con người trên map · 4. Ma trận công việc (ai bật việc gì) · 5. Căn cứ · 6. Kho & tài nguyên · 7. Trồng trọt · 8. Việc đã đánh dấu (designations) · 9. Mối đe doạ & địa điểm đáng chú ý trên map · 10. Động vật · 11. Bản đồ · 12. Xác chết trên map · 13. Nghiên cứu · 14. Nhiệm vụ · 15. Phe phái · 16. Dòng thời gian · 17. Chính sách đang dùng · 18. Giới hạn của dữ liệu


## 1. Ảnh chụp nhanh

| Thuộc tính | Giá trị |
|---|---|
| Ngày giờ trong game | **ngày 9 Aprimay năm 5501, 12:48** — mùa Thu (ngày 9/60 của năm; múi giờ UTC-3) |
| Sắp tới | sang ngày mới sau 11.2 giờ; sang quý Jugust sau 6.5 ngày (mùa Đông — suy luận, bán cầu Nam) |
| Đã chơi | 33.283 ngày game (tick 1,997,000); bắt đầu ngày 6 Septober 5500 06:00 |
| Thuộc địa | «nhung nguoi cung kho» — phe «AnkerGames's faction» — ô thế giới 162296,0 — biome `TemperateForest` — hành tinh EC-666 Secondary |
| Kịch bản / người kể chuyện | Hạ cánh khẩn cấp · `Cassandra` · độ khó `Medium` |
| Dân số trên map | 3 thuộc địa viên, 20 người ngoài, 1 KẺ ĐỊCH |
| Đột kích / đe doạ lớn | 5 lần đột kích (gần nhất: Khí độc đàn ông (PirateWaster), lúc 9 Aprimay 5501 12:48); mối đe doạ lớn gần nhất: `RaidEnemy` lúc 9 Aprimay 5501 12:48 (0.0 giờ trước) |
| Thời tiết / nhiệt độ | `Clear` · ngoài trời 14.9°C (đang là 12:48) · điều kiện đặc biệt: không · 5 ngày qua game ghi kèm sự kiện: ngoài trời 5.4–17.3°C (cao nhất lúc 8 Aprimay 5501 20:17), trong phòng tới 23.4°C (lúc 6 Aprimay 5501 20:47) |
| Tài sản thuộc địa | 26,433 (mẫu gần nhất 6.8 giờ trước); vật phẩm 14,868; 1 ngày trước 25,413 |
| Tâm trạng TB thuộc địa (game ghi) | cũ → mới: 52% → 42% → 49% → 52% → 55% → 31% → 53% → 63% (mỗi mẫu cách 12.0 giờ, mẫu cuối 6.8 giờ trước; TB trực tiếp tại thời điểm lưu: 77%) |
| Mods | Harmony, Core, Royalty, Ideology, Biotech, Anomaly, Odyssey, (1.7)Multiplayer-temp, RimHUD, SimpleCameraSetting |


## 2. Việc cần chú ý ngay

*Tự rà từ dữ liệu, xếp theo mức độ. Ngưỡng tâm trạng 35/20/5% là ngưỡng gốc vanilla (trait có thể làm lệch).*

- **[KHẨN] Đe doạ** — Kẻ địch Dude (Khí độc đàn ông (PirateWaster)) đang trên map tại (0,72), cách căn cứ 147 ô Tây Nam.
- **[KHẨN] Đe doạ** — Nhóm thù địch `LordJob_StageThenAttack` (Khí độc đàn ông (PirateWaster)): Human×1 quanh (0,72), cách căn cứ 147 ô Tây Nam — ĐANG HOẠT ĐỘNG.
- **[QUAN TRỌNG] Vũ trang** — Protein đang KHÔNG cầm vũ khí nào (lần giao tranh gần nhất dùng `Gun_Revolver`, lúc 13 Decembary 5500 16:44). Vũ khí đang nằm trên map: `Gun_Autopistol` [Normal] tại (97,142) trong «Vùng kho chứa 1»; `Gun_Revolver` [Normal] tại (103,131) trong «Vùng kho chứa 1» — đang bị CẤM (forbidden), phải bỏ cấm mới nhặt được; `MeleeWeapon_Knife` [Poor] tại (96,141) trong «Vùng kho chứa 1»; `Gun_BoltActionRifle` [Normal] tại (104,139) trong «Vùng kho chứa 1»; trên map đang có thú điên/kẻ địch.
- **[QUAN TRỌNG] Đe doạ** — Nhóm thù địch `LordJob_SleepThenAssaultColony` (bầy cỗ máy chiến đấu cơ (Mechanoid)): Mech_Militor×2, Mech_Scorcher×1 quanh (201,69), cách căn cứ 103 ô Đông Nam — đang NGỦ ĐÔNG, sẽ thức và tấn công khi bị đánh động / khi có pawn làm lộ vùng sương mù ở đó.
- **[QUAN TRỌNG] Lương thực** — `MealFine` ×34: lô sớm nhất sẽ hỏng sau ~1.57 ngày (ở ≥10°C, không bảo quản lạnh).
- **[QUAN TRỌNG] Lương thực** — `MealSimple` ×9: lô sớm nhất sẽ hỏng sau ~1.31 ngày (ở ≥10°C, không bảo quản lạnh).
- **[QUAN TRỌNG] Lương thực** — `Meat_Alpaca` ×81: lô sớm nhất sẽ hỏng sau ~1.97 ngày (ở ≥10°C, không bảo quản lạnh).
- **[QUAN TRỌNG] Lương thực** — `Meat_Pig` ×3: lô sớm nhất sẽ hỏng sau ~1.3 ngày (ở ≥10°C, không bảo quản lạnh).
- **[QUAN TRỌNG] Trồng trọt** — Ruộng «Vùng trồng trọt 2» (11 ô, x 114–117, z 148–151) đặt trồng `Plant_Rice` nhưng hiện có 0 cây trồng (có 0 cây dại mọc lẫn).
- **[QUAN TRỌNG] Nhiệm vụ** — «Pollution Dump» (`PollutionDump`) chưa nhận — hết hạn nhận sau 10.1 giờ.
- **[lưu ý] Chỗ ở** — bac si chưa được gán giường riêng (ownedBed = null).
- **[lưu ý] Chỗ ở** — eistein chưa được gán giường riêng (ownedBed = null).
- **[lưu ý] Chỗ ở** — Protein chưa được gán giường riêng (ownedBed = null).
- **[lưu ý] Lương thực** — 43 suất ăn sẵn + 117 đơn vị nguyên liệu thô cho 3 người: ≈ 9.3 ngày nếu ăn nguyên trạng, ≈ 10.2 ngày nếu nấu hết thành suất đơn giản (ước tính theo dinh dưỡng vanilla, 1.6/người/ngày).
- **[lưu ý] Vệ sinh** — Xác tươi `Corpse_WildBoar` «WildBoar» tại (137,140) (cách tâm căn cứ 9 ô) sẽ bắt đầu thối sau ~2.2 ngày (ở ≥10°C).
- **[lưu ý] Hạ tầng** — Đã nghiên cứu Electricity nhưng chưa có máy phát/pin nào được xây xong.
- **[lưu ý] Nhiệt độ** — eistein có ký ức `SleptInCold` (ngủ nơi lạnh).
- **[lưu ý] Môi trường** — `RotStink` (mùi xác thối) đang phủ 4 ô trong x 43–45, z 123–124; tâm vùng khí so với tâm căn cứ: 87 ô Tây.
- **[lưu ý] Kho** — Vật phẩm nằm ngoài mọi vùng kho (chưa bị cấm, không trong sương mù): GravlitePanel×348, Steel×266, WoodLog×142, Leather_Camel×26, MedicineHerbal×8, Meat_Alpaca×6, Meat_Pig×3.
- **[lưu ý] Nhiệm vụ** — «Tín hiệu cơ học» đang diễn ra — thành công khi có tín hiệu: gravEngine.Inspected.
- **[lưu ý] Nhiệm vụ** — «Ship to the Stars» đang diễn ra — thành công khi có tín hiệu: escapeShip.LaunchedShip.
- **[lưu ý] Nhiệm vụ** — «The Revered Artifact» (`RelicHunt`) chưa nhận.
- **[lưu ý] Nhiệm vụ** — «Temporary Workers» (`PawnLend`) chưa nhận — hết hạn nhận sau 7.6 ngày.
- **[lưu ý] Thư** — Thư còn treo trên màn hình (chưa đóng): «Quest available: The Revered Artifact» (8 Aprimay 5501 10:48); «Quest available: Temporary Workers» (9 Aprimay 5501 10:00); «Slaver from Camro dân tộc» (9 Aprimay 5501 11:35).


## 3. Con người trên map

| # | Tên | Vai trò | Giới, tuổi | Ô | Đang làm gì | Tâm trạng | Ăn / Ngủ / Giải trí | Sức khỏe (tóm tắt) | Vũ khí |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **bac si** | thuộc địa viên | M, 16t | (78,24) | `Hunt` → Boomrat `Corpse_Boomrat` (đang được bê/giữ, không nằm rời trên map) | 70% | 88% / 56% / 83% | khỏe | Gun_BoltActionRifle (Normal) |
| 2 | **eistein** | thuộc địa viên | M, 47t | (127,138) | `DoBill` → Bếp củi `FueledStove` @(125, 139) | 61% | 63% / 58% / 89% | MissingBodyPart, SmokeleafTolerance | MeleeWeapon_Knife (Plasteel, Normal) |
| 3 | **Abanqueiro** | người ngoài | M, 56t | (56,203) | `Goto` → ô (153, 160) | 53% | 92% / 91% / — | khỏe | MeleeWeapon_Spear (Steel, Normal) |
| 4 | **Seara** | người ngoài | M, 14t | (56,203) | `Goto` → ô (150, 168) | 59% | 92% / 95% / — | khỏe | Pila (Good) |
| 5 | **Rababarne** | người ngoài | M, 39t | (59,210) | `Goto` → ô (155, 169) | 62% | 92% / 93% / — | khỏe | MeleeWeapon_Spear (Steel, Good) |
| 6 | **Hare** | người ngoài | M, 53t | (55,203) | `Goto` → ô (151, 169) | 62% | 92% / 94% / — | khỏe | MeleeWeapon_Ikwa (Steel, Poor) |
| 7 | **Wyshesh** | người ngoài | M, 70t | (192,104) | `GotoWander` → ô (191, 104) | 62% | 43% / 70% / — | HearingLoss | — |
| 8 | **Bat** | người ngoài | F, 32t | (57,202) | `Goto` → ô (157, 169) | 62% | 92% / 88% / — | khỏe | Bow_Recurve (Good) |
| 9 | **Orange** | người ngoài | F, 50t | (56,203) | `Goto` → ô (157, 168) | 50% | 92% / 92% / — | khỏe | Bow_Short (Poor) |
| 10 | **Protein** | thuộc địa viên | M, 31t | (145,155) | `LayDown` — nằm trên giường (thức) → Giường `Bed` @(145, 155) | 100% | 28% / 76% / 70% | 1 vết thương | — |
| 11 | **Badger** | người ngoài | F, 46t | (54,204) | `Goto` → ô (157, 169) | 62% | 92% / 88% / — | AlcoholAddiction, AlcoholTolerance | Bow_Great (Normal) |
| 12 | **Chimpanzee** | người ngoài | M, 38t | (58,201) | `Goto` → ô (154, 163) | 62% | 92% / 93% / — | khỏe | Bow_Recurve (Good) |
| 13 | **Petronas** | người ngoài | M, 15t | (57,202) | `Goto` → ô (156, 165) | 59% | 88% / 95% / — | khỏe | — |
| 14 | **Lobster** | người ngoài | M, 15t | (59,210) | `Goto` → ô (154, 166) | 49% | 94% / 89% / — | khỏe | — |
| 15 | **Zeeurke** | người ngoài | M, 35t | (55,203) | `Goto` → ô (152, 160) | 59% | 92% / 90% / — | khỏe | — |
| 16 | **Toad** | người ngoài | F, 43t | (53,204) | `Goto` → ô (154, 164) | 62% | 92% / 92% / — | khỏe | MeleeWeapon_Spear (Steel, Normal) |
| 17 | **Daga** | người ngoài | F, 36t | (54,204) | `Goto` → ô (155, 162) | 64% | 92% / 89% / — | khỏe | Bow_Short (Normal) |
| 18 | **Grasshopper** | người ngoài | M, 41t | (55,203) | `Goto` → ô (154, 168) | 58% | 92% / 87% / — | khỏe | Bow_Great (Normal) |
| 19 | **Crow** | người ngoài | M, 43t | (55,203) | `Goto` → ô (154, 170) | 52% | 92% / 86% / — | khỏe | Bow_Recurve (Normal) |
| 20 | **Dobreibo** | người ngoài | F, 18t | (56,203) | `Goto` → ô (158, 165) | 62% | 92% / 87% / — | khỏe | Bow_Short (Poor) |
| 21 | **Snail** | người ngoài | F, 49t | (57,202) | `Goto` → ô (154, 159) | 64% | 92% / 86% / — | khỏe | MeleeWeapon_Ikwa (Steel, Poor) |
| 22 | **Black** | người ngoài | F, 30t | (54,204) | `Goto` → ô (157, 169) | 62% | 92% / 91% / — | khỏe | MeleeWeapon_Ikwa (Steel, Poor) |
| 23 | **Hedgehog** | người ngoài | F, 27t | (55,203) | `Goto` → ô (157, 168) | 62% | 92% / 87% / — | khỏe | MeleeWeapon_Spear (Steel, Normal) |
| 24 | **Dude** | KẺ ĐỊCH | M, 57t | (0,72) | rảnh (không có job) | 50% | 80% / 94% / — | khỏe | MeleeWeapon_Club (BlocksMarble) |


### bac si — `Human665` (thuộc địa viên)

- **Danh tính:** Nikolay “bac si” Bishop · Male · 16.3 tuổi (niên đại 872) · phe AnkerGames's faction (PlayerColony) · kind `Colonist` · xenotype Baseliner · tôn giáo Astropolitan (86%)
- **Xuất thân / tính cách:** MedicalAssistant12 / — · trait: ShootingAccuracy(-1), FastLearner, BodyPurist
- **Hiện tại:** ô (78,24) · `Hunt` → Boomrat `Corpse_Boomrat` (đang được bê/giữ, không nằm rời trên map) · lịch giờ này: Anything
- **Tâm trạng:** 69.7%
- **Nhu cầu:** Food 88% · Rest 56% · Joy 83% · Beauty 43% · Comfort 30% · Outdoors 100% · DrugDesire 50% · RoomSize 100%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (6, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** `AteFineMeal` (0.1 ngày trước) · `AteWithoutTable` (0.1 ngày trước) · `Chitchat`→eistein (thiện cảm +43, 0.3 ngày trước) · `Chitchat`→Protein (thiện cảm +25, 0.3 ngày trước) · `SleepDisturbed` (0.9 ngày trước) · `Insulted`→eistein (thiện cảm -14, 16.1 ngày trước)
- **Tổng thiện cảm từ ký ức:** eistein +29, Protein +25
- **Sức khỏe** (trạng thái `Mobile`; 0 hediff):

*(không có hediff nào)*

- **Kỹ năng:** Shooting 10★ · Melee 5★ · Construction 4 · Mining 1 · Cooking 1 · Plants 4 · Animals 2 · Crafting 0 · Artistic 3★★ · Medicine 8★★ · Social 2 · Intellectual 2
- **Ưu tiên việc:** **1**: Patient, Doctor, Hunting, Construction, Hauling, Cleaning · **2**: PlantCutting · **3**: PatientBedRest, BasicWorker · tắt (0): Firefighter, Warden, Handling, Cooking, Growing, Mining, Smithing, Tailoring, Art, Crafting, Research, Childcare, DarkStudy, Fishing
- **Mặc:** Apparel_CollarShirt (Synthread, Normal), Apparel_Pants (Synthread, Normal) · **Cầm:** Gun_BoltActionRifle (Normal) · **Túi:** MedicineIndustrial ×3 · **Đang bê:** Corpse_Boomrat
- **Thiết lập:** giường riêng: chưa có · y tế: Best · tự băng: True · phản ứng địch: Attack · trang phục «Gì cũng mặc» · thuốc «Chính sách thuốc» · ăn «Xa hoa»
- **Lịch 24h:** 00–05 Sleep · 06 Meditate · 07 Joy · 08–19 Anything · 20 Joy · 21 Meditate · 22–23 Sleep
- **Lần dùng chất gần nhất:** Beer (29.9 ngày trước)


### eistein — `Human668` (thuộc địa viên)

- **Danh tính:** Anthony “eistein” Hayes · Male · 46.8 tuổi (niên đại 542) · phe AnkerGames's faction (PlayerColony) · kind `Colonist` · xenotype Baseliner · tôn giáo Astropolitan (93%)
- **Xuất thân / tính cách:** StoryWriter67 / Bartender62 · trait: FastLearner, DrugDesire(+2)
- **Hiện tại:** ô (127,138) · `DoBill` → Bếp củi `FueledStove` @(125, 139) · lịch giờ này: Anything
- **Tâm trạng:** 60.7%
- **Nhu cầu:** Food 63% · Rest 58% · Joy 89% · Beauty 38% · Comfort 60% · Outdoors 100% · DrugDesire 0% · RoomSize 71%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (11, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** `Chitchat`→Protein (thiện cảm +36, 0.1 ngày trước) · `AteFineMeal` (0.2 ngày trước) · `Chitchat`→bac si (thiện cảm +35, 0.2 ngày trước) · `SleptInCold` (0.3 ngày trước) · `SleepDisturbed` (0.4 ngày trước) · `SleepDisturbed` (0.6 ngày trước) · `AteWithoutTable` (0.8 ngày trước) · `Slighted`→bac si (thiện cảm -4, 3.0 ngày trước) · `Slighted`→Protein (thiện cảm -5, 6.1 ngày trước) · `Insulted`→Protein (thiện cảm -9, 10.7 ngày trước) · `Insulted`→Protein (thiện cảm -13, 10.9 ngày trước)
- **Tổng thiện cảm từ ký ức:** Protein +9, bac si +31
- **Sức khỏe** (trạng thái `Mobile`; 3 hediff):

| Hediff | Bộ phận | Mức | Chăm sóc | Tuổi (ngày) | Ghi chú |
|---|---|---|---|---|---|
| `SmokeleafTolerance` | toàn thân | 0.38 | — | 29.5 | giảm 0.015/ngày → hết sau ~25.2 ngày |
| `MissingBodyPart` | ngón áp út chân phải (Toe) | 0.50 | đã băng/chăm (71%) | 14.2 | vì Bite |
| `Scratch` | mắt phải (Eye) | 4.70 | — | 8.9 | vĩnh viễn; do raccoon/claw |

- **Kỹ năng:** Shooting 1 · Melee 9★ · Construction 5 · Mining 3 · Cooking 7 · Plants 3 · Animals 4 · Crafting 2 · Artistic 7 · Medicine 4 · Social 9★ · Intellectual 9★
- **Ưu tiên việc:** **1**: Firefighter, Patient, Cooking, Construction, Hauling, Cleaning, Research · **2**: Mining, PlantCutting · **3**: PatientBedRest, BasicWorker, Warden · tắt (0): Doctor, Handling, Hunting, Growing, Smithing, Tailoring, Art, Crafting, Childcare, DarkStudy, Fishing
- **Mặc:** Apparel_FlakPants (Normal), Apparel_Parka (Synthread, Normal), Apparel_AdvancedHelmet (Plasteel, Normal) · **Cầm:** MeleeWeapon_Knife (Plasteel, Normal) · **Túi:** MealFine
- **Thiết lập:** giường riêng: chưa có · y tế: Best · tự băng: True · phản ứng địch: Attack · trang phục «Gì cũng mặc» · thuốc «Chính sách thuốc» · ăn «Xa hoa»
- **Lịch 24h:** 00–05 Sleep · 06 Meditate · 07 Joy · 08–19 Anything · 20 Joy · 21 Meditate · 22–23 Sleep
- **Lần dùng chất gần nhất:** Beer (32.9 ngày trước), SmokeleafJoint (29.5 ngày trước), GoJuice (9.6 ngày trước)


### Abanqueiro — `Human120257` (người ngoài)

- **Danh tính:** Abanqueiro Rogua · Male · 56.0 tuổi (niên đại 56) · phe Camro dân tộc (TribeCivil) · kind `Tribal_Berserker` · xenotype Baseliner · tôn giáo Astropolitan (97%)
- **Xuất thân / tính cách:** BuddingArtist44 / Logger16 · trait: PsychicSensitivity(+1)
- **Hiện tại:** ô (56,203) · `Goto` → ô (153, 160) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 53.0%
- **Nhu cầu:** Food 92% · Rest 91%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (0, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** —
- **Sức khỏe** (trạng thái `Mobile`; 1 hediff):

| Hediff | Bộ phận | Mức | Chăm sóc | Tuổi (ngày) | Ghi chú |
|---|---|---|---|---|---|
| `Bite` | tay phải (Arm) | 3 | — | 0.0 | vĩnh viễn |

- **Kỹ năng:** Shooting 4★ · Melee 4★ · Construction 4 · Mining 0 · Cooking 4 · Plants 12★★ · Animals 0 · Crafting 2 · Artistic 10★ · Medicine 4 · Social 4 · Intellectual 3
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_CollarShirt (WoolMuffalo, Normal), Apparel_Tuque (Cloth, Normal) · **Cầm:** MeleeWeapon_Spear (Steel, Normal) · **Túi:** Pemmican ×51
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Seara — `Human120227` (người ngoài)

- **Danh tính:** Seara Comareiro · Male · 14.4 tuổi (niên đại 14) · phe Camro dân tộc (TribeCivil) · kind `Tribal_HeavyArcher` · xenotype Baseliner · tôn giáo Astropolitan (86%)
- **Xuất thân / tính cách:** CaveChild30 / — · trait: Undergrounder, DislikesMen
- **Hiện tại:** ô (56,203) · `Goto` → ô (150, 168) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 59.0%
- **Nhu cầu:** Food 92% · Rest 95%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (0, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** —
- **Sức khỏe** (trạng thái `Mobile`; 0 hediff):

*(không có hediff nào)*

- **Kỹ năng:** Shooting 0 · Melee 2 · Construction 4★ · Mining 5★ · Cooking 3 · Plants 0 · Animals 7★★ · Crafting 2 · Artistic 0 · Medicine 3 · Social 2 · Intellectual 2
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_TribalA (WoolBison, Normal), Apparel_Parka (Cloth, Poor), Apparel_Tuque (Cloth, Poor) · **Cầm:** Pila (Good) · **Túi:** Pemmican ×51
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Rababarne — `Human120251` (người ngoài)

- **Danh tính:** Rababarne Reivexa · Male · 39.0 tuổi (niên đại 39) · phe Camro dân tộc (TribeCivil) · kind `Tribal_Berserker` · xenotype Baseliner · tôn giáo Astropolitan (81%)
- **Xuất thân / tính cách:** Hideaway7 / PlankCutter72 · trait: Delicate, Wimp
- **Hiện tại:** ô (59,210) · `Goto` → ô (155, 169) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 62.0%
- **Nhu cầu:** Food 92% · Rest 93%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (2, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** `Chitchat`→Grasshopper (thiện cảm +1, 0.0 ngày trước) · `Chitchat`→Snail (thiện cảm +1, 0.0 ngày trước)
- **Tổng thiện cảm từ ký ức:** Grasshopper +0, Snail +0
- **Sức khỏe** (trạng thái `Mobile`; 2 hediff):

| Hediff | Bộ phận | Mức | Chăm sóc | Tuổi (ngày) | Ghi chú |
|---|---|---|---|---|---|
| `Scratch` | chân phải (Leg) | 5 | — | 0.0 | vĩnh viễn |
| `Gunshot` | chân phải (Leg) | 5 | — | 0.0 | vĩnh viễn |

- **Kỹ năng:** Shooting 1 · Melee 4 · Construction 2 · Mining 3 · Cooking 1 · Plants 9★★ · Animals 5★ · Crafting 5 · Artistic 2 · Medicine 3 · Social 0 · Intellectual 7★★
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_TribalA (Cloth, Normal), Apparel_Parka (WoolMegasloth, Normal), Apparel_WarMask (WoodLog, Normal) · **Cầm:** MeleeWeapon_Spear (Steel, Good) · **Túi:** Pemmican ×51
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Hare — `Human120208` (người ngoài)

- **Danh tính:** Hare Canto · Male · 53.1 tuổi (niên đại 53) · phe Camro dân tộc (TribeCivil) · kind `Tribal_Warrior` · xenotype Baseliner · tôn giáo Astropolitan (81%)
- **Xuất thân / tính cách:** BuddingArtist44 / Weaver63 · trait: Cannibal, DislikesMen
- **Hiện tại:** ô (55,203) · `Goto` → ô (151, 169) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 62.0%
- **Nhu cầu:** Food 92% · Rest 94%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (1, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** `Chitchat`→Daga (thiện cảm +1, 0.0 ngày trước)
- **Tổng thiện cảm từ ký ức:** Daga +1
- **Sức khỏe** (trạng thái `Mobile`; 0 hediff):

*(không có hediff nào)*

- **Kỹ năng:** Shooting 0 · Melee 2 · Construction 1 · Mining 4 · Cooking 1 · Plants 6★★ · Animals 4 · Crafting 11★★ · Artistic 5★ · Medicine 1 · Social 0 · Intellectual 2
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_TribalA (Leather_Bear), Apparel_Parka (Cloth, Poor), Apparel_Tuque (Cloth, Poor) · **Cầm:** MeleeWeapon_Ikwa (Steel, Poor) · **Túi:** Pemmican ×51
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Wyshesh — `Human112143` (người ngoài)

- **Danh tính:** Wyshesh Barark · Male · 69.9 tuổi (niên đại 70) · phe — · kind `WildMan` · xenotype Yttakin · tôn giáo Astropolitan (88%)
- **Xuất thân / tính cách:** UrbworldUrchin61 / Policeman45 · trait: Immunity(+1), PsychicSensitivity(-1)
- **Hiện tại:** ô (192,104) · `GotoWander` → ô (191, 104) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 15 Decembary 5500 16:23
- **Tâm trạng:** 62.0%
- **Nhu cầu:** Food 43% · Rest 70%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (0, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** —
- **Sức khỏe** (trạng thái `Mobile`; 2 hediff):

| Hediff | Bộ phận | Mức | Chăm sóc | Tuổi (ngày) | Ghi chú |
|---|---|---|---|---|---|
| `HearingLoss` | tai phải (Ear) | 0.00 | — | 8.8 |  |
| `HearingLoss` | tai trái (Ear) | 0.00 | — | 8.8 |  |

- **Kỹ năng:** Shooting 12★★ · Melee 9★ · Construction 2 · Mining 4 · Cooking 4★ · Plants 1 · Animals 3★ · Crafting 1 · Artistic 0 · Medicine 1 · Social 4 · Intellectual 0
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** — · **Cầm:** — · **Túi:** —
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Bat — `Human120202` (người ngoài)

- **Danh tính:** Bat Croidor · Female · 31.7 tuổi (niên đại 32) · phe Camro dân tộc (TribeCivil) · kind `Tribal_Hunter` · xenotype Baseliner · tôn giáo Astropolitan (64%)
- **Xuất thân / tính cách:** ReclusiveChild81 / Loner61 · trait: QuickSleeper, Nerves(-2), Industriousness(+2)
- **Hiện tại:** ô (57,202) · `Goto` → ô (157, 169) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 62.0%
- **Nhu cầu:** Food 92% · Rest 88%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (1, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** `Chitchat`→Dobreibo (thiện cảm +1, 0.0 ngày trước)
- **Tổng thiện cảm từ ký ức:** Dobreibo +1
- **Sức khỏe** (trạng thái `Mobile`; 0 hediff):

*(không có hediff nào)*

- **Kỹ năng:** Shooting 3 · Melee 11★★ · Construction 5★ · Mining 0 · Cooking 2 · Plants 8★ · Animals 2 · Crafting 6★ · Artistic 2 · Medicine 1 · Social 3 · Intellectual 2
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_TribalA (WoolMuffalo, Normal), Apparel_Duster (Cloth, Normal), Apparel_Tuque (Cloth, Normal) · **Cầm:** Bow_Recurve (Good) · **Túi:** Pemmican ×51
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Orange — `Human120262` (người ngoài)

- **Danh tính:** Orange Grouse · Female · 50.4 tuổi (niên đại 50) · phe Camro dân tộc (TribeCivil) · kind `Tribal_Archer` · xenotype Baseliner · tôn giáo Astropolitan (81%)
- **Xuất thân / tính cách:** AbandonedChild23 / Weaver63 · trait: NaturalMood(-2)
- **Hiện tại:** ô (56,203) · `Goto` → ô (157, 168) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 50.0%
- **Nhu cầu:** Food 92% · Rest 92%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (0, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** —
- **Sức khỏe** (trạng thái `Mobile`; 1 hediff):

| Hediff | Bộ phận | Mức | Chăm sóc | Tuổi (ngày) | Ghi chú |
|---|---|---|---|---|---|
| `Stab` | thân (Torso) | 4 | — | 0.0 | vĩnh viễn |

- **Kỹ năng:** Shooting 0 · Melee 5★ · Construction 4★ · Mining 0 · Cooking 3★ · Plants 4★ · Animals 4★ · Crafting 14★★ · Artistic 1 · Medicine 2 · Social 0 · Intellectual 3
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_TribalA (Cloth, Poor), Apparel_Duster (Leather_Light, Poor), Apparel_Tuque (Cloth, Poor) · **Cầm:** Bow_Short (Poor) · **Túi:** Pemmican ×51
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»
- **Quan hệ:** Parent: Crocodile, Parent: Tasdaga, Spouse: Porcupine


### Protein — `Human672` (thuộc địa viên)

- **Danh tính:** Ichabod “Protein” Andrade · Male · 31.4 tuổi (niên đại 86) · phe AnkerGames's faction (PlayerColony) · kind `Colonist` · xenotype Baseliner · tôn giáo Astropolitan (95%)
- **Xuất thân / tính cách:** WreckageExplorer93 / LowWageWorker7 · trait: Transhumanist
- **Hiện tại:** ô (145,155) · `LayDown` — nằm trên giường (thức) → Giường `Bed` @(145, 155) · lịch giờ này: Anything
- **Tâm trạng:** 100.0% · thời gian liên tục dưới ngưỡng nhẹ/nặng/cực đoan: 0.0 giờ / 0.0 giờ / 0.0 giờ
- **Nhu cầu:** Food 28% · Rest 76% · Joy 70% · Beauty 38% · Comfort 75% · Outdoors 98% · DrugDesire 50% · RoomSize 57%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (9, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** `Chitchat`→eistein (thiện cảm +38, 0.1 ngày trước) · `Chitchat`→bac si (thiện cảm +22, 0.3 ngày trước) · `AteFineMeal` (0.4 ngày trước) · `AteInImpressiveDiningRoom` (0.4 ngày trước) · `Catharsis` (1.4 ngày trước) · `Slighted`→eistein (thiện cảm -5, 1.8 ngày trước) · `RescuedMe`→bac si (thiện cảm +15, 10.3 ngày trước) · `Slighted`→eistein (thiện cảm -5, 11.8 ngày trước) · `Slighted`→eistein (thiện cảm -4, 14.3 ngày trước)
- **Tổng thiện cảm từ ký ức:** eistein +24, bac si +37
- **Sức khỏe** (trạng thái `Mobile`; 1 hediff):

| Hediff | Bộ phận | Mức | Chăm sóc | Tuổi (ngày) | Ghi chú |
|---|---|---|---|---|---|
| `Gunshot` | thân (Torso) | 1.14 | đã băng/chăm (66%) | 1.7 | do bolt-action rifle |

- **Kỹ năng:** Shooting 3 · Melee 3 · Construction 2 · Mining 3 · Cooking 8★★ · Plants 11★★ · Animals 6★ · Crafting 4 · Artistic 2 · Medicine 4 · Social 4 · Intellectual 6★
- **Ưu tiên việc:** **1**: Firefighter, Patient, Handling, Cooking, Hunting, Growing, PlantCutting, Hauling, Cleaning, Research · **3**: PatientBedRest, BasicWorker, Mining · tắt (0): Doctor, Warden, Construction, Smithing, Tailoring, Art, Crafting, Childcare, DarkStudy, Fishing
- **Mặc:** Apparel_Pants (Synthread, Normal), Apparel_BasicShirt (Synthread, Normal), Apparel_FlakVest (Normal) · **Cầm:** — · **Túi:** MealSimple
- **Thiết lập:** giường riêng: chưa có · y tế: Best · tự băng: True · phản ứng địch: Attack · trang phục «Gì cũng mặc» · thuốc «Chính sách thuốc» · ăn «Xa hoa»
- **Lịch 24h:** 00–05 Sleep · 06 Meditate · 07 Joy · 08–19 Anything · 20 Joy · 21 Meditate · 22–23 Sleep
- **Lần dùng chất gần nhất:** Beer (28.9 ngày trước)
- **Quan hệ:** Parent: Eva, Parent: Isaias


### Badger — `Human120233` (người ngoài)

- **Danh tính:** Badger Breica · Female · 45.9 tuổi (niên đại 46) · phe Camro dân tộc (TribeCivil) · kind `Tribal_HeavyArcher` · xenotype Baseliner · tôn giáo Astropolitan (67%)
- **Xuất thân / tính cách:** BuddingArtist44 / Framer37 · trait: Jealous, Beauty(-2)
- **Hiện tại:** ô (54,204) · `Goto` → ô (157, 169) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 62.0%
- **Nhu cầu:** Food 92% · Rest 88% · Chemical_Alcohol 86%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (0, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** —
- **Sức khỏe** (trạng thái `Mobile`; 2 hediff):

| Hediff | Bộ phận | Mức | Chăm sóc | Tuổi (ngày) | Ghi chú |
|---|---|---|---|---|---|
| `AlcoholAddiction` | toàn thân | 0.84 | — | 0.0 | giảm 0.033/ngày → hết sau ~25.33 ngày |
| `AlcoholTolerance` | toàn thân | 0.53 | — | 0.0 | giảm 0.016/ngày → hết sau ~33.26 ngày |

- **Kỹ năng:** Shooting 4 · Melee 4 · Construction 8★★ · Mining 1 · Cooking 2 · Plants 3 · Animals 4 · Crafting 5★ · Artistic 7★★ · Medicine 1 · Social 4 · Intellectual 4
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_TribalA (Cloth, Normal), Apparel_Tuque (Cloth, Good) · **Cầm:** Bow_Great (Normal) · **Túi:** Pemmican ×51, Beer ×4
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»
- **Quan hệ:** Parent: Vexabilque


### Chimpanzee — `Human120108` (người ngoài)

- **Danh tính:** Chimpanzee Lernene · Male · 37.9 tuổi (niên đại 38) · phe Camro dân tộc (TribeCivil) · kind `Tribal_Trader` · xenotype Baseliner · tôn giáo Astropolitan (82%)
- **Xuất thân / tính cách:** TribeChild40 / Archer25 · trait: Ascetic, Nimble, ShootingAccuracy(-1)
- **Hiện tại:** ô (58,201) · `Goto` → ô (154, 163) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 62.0%
- **Nhu cầu:** Food 92% · Rest 93%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (0, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** —
- **Sức khỏe** (trạng thái `Mobile`; 0 hediff):

*(không có hediff nào)*

- **Kỹ năng:** Shooting 11★★ · Melee 7★★ · Construction 1 · Mining 3 · Cooking 0 · Plants 6★ · Animals 4★ · Crafting 1 · Artistic 3 · Medicine 3 · Social 4 · Intellectual 0
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_TribalA (Cloth, Normal), Apparel_Parka (Leather_Pig, Normal), Apparel_Tuque (Cloth, Normal) · **Cầm:** Bow_Recurve (Good) · **Túi:** Pemmican ×51
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Petronas — `Human120127` (người ngoài)

- **Danh tính:** Petronas Lisneare · Male · 15.1 tuổi (niên đại 15) · phe Camro dân tộc (TribeCivil) · kind `Slave` · xenotype Baseliner · tôn giáo Astropolitan (86%)
- **Xuất thân / tính cách:** FrightenedChild43 / — · trait: DislikesWomen, Tough, Gourmand
- **Hiện tại:** ô (57,202) · `Goto` → ô (156, 165) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 59.0%
- **Nhu cầu:** Food 88% · Rest 95%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (0, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** —
- **Sức khỏe** (trạng thái `Mobile`; 0 hediff):

*(không có hediff nào)*

- **Kỹ năng:** Shooting 1 · Melee 3 · Construction 3★ · Mining 3 · Cooking 8★★ · Plants 3 · Animals 2 · Crafting 3 · Artistic 3 · Medicine 6★★ · Social 0 · Intellectual 3
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_Pants (Cloth, Normal), Apparel_BasicShirt (Cloth, Normal), Apparel_Tuque (Cloth, Poor) · **Cầm:** — · **Túi:** Pemmican ×20
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Lobster — `Human120117` (người ngoài)

- **Danh tính:** Bico “Lobster” Croibarro · Male · 14.6 tuổi (niên đại 15) · phe Camro dân tộc (TribeCivil) · kind `Slave` · xenotype Neanderthal · tôn giáo Astropolitan (75%)
- **Xuất thân / tính cách:** IndustrialOrphan13 / — · trait: Kind, ShootingAccuracy(+1), NightOwl
- **Hiện tại:** ô (59,210) · `Goto` → ô (154, 166) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 49.0%
- **Nhu cầu:** Food 94% · Rest 89%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (0, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** —
- **Sức khỏe** (trạng thái `Mobile`; 0 hediff):

*(không có hediff nào)*

- **Kỹ năng:** Shooting 0 · Melee 3★★ · Construction 0 · Mining 5★★ · Cooking 3★ · Plants 2★ · Animals 2 · Crafting 6★★ · Artistic 0 · Medicine 0 · Social 1 · Intellectual 1
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_Pants (WoolBison, Poor), Apparel_Jacket (Cloth, Poor), Apparel_Tuque (Cloth, Poor) · **Cầm:** — · **Túi:** Pemmican ×20
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Zeeurke — `Human120122` (người ngoài)

- **Danh tính:** Zeeurke Meme · Male · 34.9 tuổi (niên đại 35) · phe Camro dân tộc (TribeCivil) · kind `Slave` · xenotype Baseliner · tôn giáo Astropolitan (86%)
- **Xuất thân / tính cách:** ComaChild93 / StarshipJanitor33 · trait: Immunity(-1)
- **Hiện tại:** ô (55,203) · `Goto` → ô (152, 160) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 59.0%
- **Nhu cầu:** Food 92% · Rest 90%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (0, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** —
- **Sức khỏe** (trạng thái `Mobile`; 0 hediff):

*(không có hediff nào)*

- **Kỹ năng:** Shooting 0 · Melee 1 · Construction 2 · Mining 1 · Cooking 0 · Plants 4★ · Animals 4★ · Crafting 4 · Artistic 4 · Medicine 7★★ · Social 9★★ · Intellectual 0
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_Pants (Cloth, Poor), Apparel_BasicShirt (Leather_Bear, Poor), Apparel_Tuque (Cloth, Normal) · **Cầm:** — · **Túi:** Pemmican ×20
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Toad — `Human120146` (người ngoài)

- **Danh tính:** Toad Netradordoa · Female · 43.4 tuổi (niên đại 43) · phe Camro dân tộc (TribeCivil) · kind `Tribal_Berserker` · xenotype Baseliner · tôn giáo Astropolitan (72%)
- **Xuất thân / tính cách:** VengefulChild43 / LoreKeeper51 · trait: Nerves(+2), Immunity(-1), Abrasive
- **Hiện tại:** ô (53,204) · `Goto` → ô (154, 164) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 62.0%
- **Nhu cầu:** Food 92% · Rest 92%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (0, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** —
- **Sức khỏe** (trạng thái `Mobile`; 1 hediff):

| Hediff | Bộ phận | Mức | Chăm sóc | Tuổi (ngày) | Ghi chú |
|---|---|---|---|---|---|
| `Scratch` | tay phải (Arm) | 6 | — | 0.0 | vĩnh viễn |

- **Kỹ năng:** Shooting 6★ · Melee 5★ · Construction 4★ · Mining 4 · Cooking 3 · Plants 4 · Animals 2 · Crafting 3 · Artistic 2 · Medicine 9 · Social 8★★ · Intellectual 2
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_TribalA (Cloth, Poor), Apparel_Duster (Cloth, Normal), Apparel_Tuque (Cloth, Normal) · **Cầm:** MeleeWeapon_Spear (Steel, Normal) · **Túi:** Pemmican ×51
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»
- **Quan hệ:** Parent: Red


### Daga — `Human120164` (người ngoài)

- **Danh tính:** Daga Goléroalbo · Female · 36.4 tuổi (niên đại 36) · phe Camro dân tộc (TribeCivil) · kind `Tribal_Archer` · xenotype Baseliner · tôn giáo Astropolitan (62%)
- **Xuất thân / tính cách:** CrashBaby32 / Butcher40 · trait: SpeedOffset(-1), NaturalMood(+1), FastLearner
- **Hiện tại:** ô (54,204) · `Goto` → ô (155, 162) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 64.4%
- **Nhu cầu:** Food 92% · Rest 89%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (1, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** `Chitchat`→Hare (thiện cảm +1, 0.0 ngày trước)
- **Tổng thiện cảm từ ký ức:** Hare +0
- **Sức khỏe** (trạng thái `Mobile`; 0 hediff):

*(không có hediff nào)*

- **Kỹ năng:** Shooting 4★ · Melee 4★ · Construction 4 · Mining 4 · Cooking 8★★ · Plants 2 · Animals 6★ · Crafting 4 · Artistic 3 · Medicine 3 · Social 8★★ · Intellectual 4
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_TribalA (WoolMegasloth, Poor), Apparel_Parka (Cloth) · **Cầm:** Bow_Short (Normal) · **Túi:** Pemmican ×51
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Grasshopper — `Human120169` (người ngoài)

- **Danh tính:** Grasshopper Breixos · Male · 40.6 tuổi (niên đại 41) · phe Camro dân tộc (TribeCivil) · kind `Tribal_HeavyArcher` · xenotype Baseliner · tôn giáo Astropolitan (61%)
- **Xuất thân / tính cách:** AbandonedChild23 / Hunter74 · trait: Transhumanist, Jealous, FastLearner
- **Hiện tại:** ô (55,203) · `Goto` → ô (154, 168) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 58.0%
- **Nhu cầu:** Food 92% · Rest 87%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (1, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** `Chitchat`→Rababarne (thiện cảm +1, 0.0 ngày trước)
- **Tổng thiện cảm từ ký ức:** Rababarne +0
- **Sức khỏe** (trạng thái `Mobile`; 1 hediff):

| Hediff | Bộ phận | Mức | Chăm sóc | Tuổi (ngày) | Ghi chú |
|---|---|---|---|---|---|
| `Gunshot` | tay phải (Arm) | 5 | — | 0.0 | vĩnh viễn |

- **Kỹ năng:** Shooting 6★ · Melee 9★★ · Construction 4★ · Mining 1 · Cooking 2 · Plants 2 · Animals 6★ · Crafting 8★ · Artistic 1 · Medicine 3 · Social 0 · Intellectual 4★
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_TribalA (Leather_Light, Normal), Apparel_Parka (WoolSheep, Normal), Apparel_WarMask (WoodLog, Good) · **Cầm:** Bow_Great (Normal) · **Túi:** Pemmican ×51
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Crow — `Human120175` (người ngoài)

- **Danh tính:** Govasre “Crow” Lemeada · Male · 43.3 tuổi (niên đại 43) · phe Camro dân tộc (TribeCivil) · kind `Tribal_Hunter` · xenotype Baseliner · tôn giáo Astropolitan (69%)
- **Xuất thân / tính cách:** FireKeeper44 / Butcher40 · trait: NightOwl, TooSmart
- **Hiện tại:** ô (55,203) · `Goto` → ô (154, 170) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 52.0%
- **Nhu cầu:** Food 92% · Rest 86%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (0, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** —
- **Sức khỏe** (trạng thái `Mobile`; 1 hediff):

| Hediff | Bộ phận | Mức | Chăm sóc | Tuổi (ngày) | Ghi chú |
|---|---|---|---|---|---|
| `Stab` | tay trái (Arm) | 4 | — | 0.0 | vĩnh viễn |

- **Kỹ năng:** Shooting 5★ · Melee 0 · Construction 4 · Mining 3 · Cooking 12★★ · Plants 4 · Animals 5★ · Crafting 7★★ · Artistic 1 · Medicine 2 · Social 0 · Intellectual 1
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_TribalA (WoolMuffalo, Normal), Apparel_Tuque (Cloth, Normal) · **Cầm:** Bow_Recurve (Normal) · **Túi:** Pemmican ×51
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Dobreibo — `Human120180` (người ngoài)

- **Danh tính:** Dobreibo Combo · Female · 17.8 tuổi (niên đại 18) · phe Camro dân tộc (TribeCivil) · kind `Tribal_Archer` · xenotype Baseliner · tôn giáo Astropolitan (87%)
- **Xuất thân / tính cách:** AbandonedChild23 / — · trait: AnnoyingVoice, Tough
- **Hiện tại:** ô (56,203) · `Goto` → ô (158, 165) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 62.0%
- **Nhu cầu:** Food 92% · Rest 87%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (1, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** `Chitchat`→Bat (thiện cảm +1, 0.0 ngày trước)
- **Tổng thiện cảm từ ký ức:** Bat +0
- **Sức khỏe** (trạng thái `Mobile`; 0 hediff):

*(không có hediff nào)*

- **Kỹ năng:** Shooting 4★ · Melee 3 · Construction 3 · Mining 3 · Cooking 0 · Plants 0 · Animals 4★ · Crafting 6★★ · Artistic 2 · Medicine 1 · Social 1 · Intellectual 1
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_TribalA (WoolSheep, Poor), Apparel_Parka (Cloth, Poor), Apparel_Tuque (Cloth, Poor) · **Cầm:** Bow_Short (Poor) · **Túi:** Pemmican ×51
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Snail — `Human120186` (người ngoài)

- **Danh tính:** Snail Ñoba · Female · 48.9 tuổi (niên đại 49) · phe Camro dân tộc (TribeCivil) · kind `Tribal_Warrior` · xenotype Baseliner · tôn giáo Astropolitan (74%)
- **Xuất thân / tính cách:** TribeChild40 / Loner61 · trait: NaturalMood(+1), Greedy
- **Hiện tại:** ô (57,202) · `Goto` → ô (154, 159) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 64.4%
- **Nhu cầu:** Food 92% · Rest 86%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (2, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** `Chitchat`→Hedgehog (thiện cảm +1, 0.0 ngày trước) · `Chitchat`→Rababarne (thiện cảm +1, 0.0 ngày trước)
- **Tổng thiện cảm từ ký ức:** Hedgehog +1, Rababarne +0
- **Sức khỏe** (trạng thái `Mobile`; 0 hediff):

*(không có hediff nào)*

- **Kỹ năng:** Shooting 10★★ · Melee 6★★ · Construction 6★ · Mining 1 · Cooking 4 · Plants 12★★ · Animals 4 · Crafting 1 · Artistic 1 · Medicine 2 · Social 1 · Intellectual 0
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_TribalA (Leather_Light, Poor), Apparel_Tuque (Cloth, Poor) · **Cầm:** MeleeWeapon_Ikwa (Steel, Poor) · **Túi:** Pemmican ×51
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Black — `Human120191` (người ngoài)

- **Danh tính:** Black Mouse · Female · 30.2 tuổi (niên đại 30) · phe Camro dân tộc (TribeCivil) · kind `Tribal_Warrior` · xenotype Baseliner · tôn giáo Astropolitan (71%)
- **Xuất thân / tính cách:** Hideaway7 / Gatherer70 · trait: CreepyBreathing, SlowLearner
- **Hiện tại:** ô (54,204) · `Goto` → ô (157, 169) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 62.0%
- **Nhu cầu:** Food 92% · Rest 91%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (0, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** —
- **Sức khỏe** (trạng thái `Mobile`; 0 hediff):

*(không có hediff nào)*

- **Kỹ năng:** Shooting 1 · Melee 3 · Construction 4★ · Mining 0 · Cooking 3 · Plants 11★★ · Animals 4 · Crafting 4 · Artistic 1 · Medicine 3 · Social 0 · Intellectual 5★★
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_TribalA (Leather_Elephant, Poor), Apparel_Tuque (Cloth, Poor) · **Cầm:** MeleeWeapon_Ikwa (Steel, Poor) · **Túi:** Pemmican ×51
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Hedgehog — `Human120196` (người ngoài)

- **Danh tính:** Hedgehog Maulo · Female · 26.8 tuổi (niên đại 27) · phe Camro dân tộc (TribeCivil) · kind `Tribal_Berserker` · xenotype Baseliner · tôn giáo Astropolitan (67%)
- **Xuất thân / tính cách:** Herder19 / Herder33 · trait: QuickSleeper
- **Hiện tại:** ô (55,203) · `Goto` → ô (157, 168) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 11:35
- **Tâm trạng:** 62.0%
- **Nhu cầu:** Food 92% · Rest 87%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (1, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** `Chitchat`→Snail (thiện cảm +1, 0.0 ngày trước)
- **Tổng thiện cảm từ ký ức:** Snail +0
- **Sức khỏe** (trạng thái `Mobile`; 0 hediff):

*(không có hediff nào)*

- **Kỹ năng:** Shooting 6★ · Melee 6★ · Construction 1 · Mining 4 · Cooking 2 · Plants 2 · Animals 13★★ · Crafting 4 · Artistic 0 · Medicine 3 · Social 1 · Intellectual 4
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_TribalA (WoolBison, Normal), Apparel_Duster (Cloth, Normal), Apparel_Tuque (Cloth, Normal) · **Cầm:** MeleeWeapon_Spear (Steel, Normal) · **Túi:** Pemmican ×51
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


### Dude — `Human120361` (KẺ ĐỊCH)

- **Danh tính:** Shinichi “Dude” Henry · Male · 56.5 tuổi (niên đại 57) · phe Khí độc đàn ông (PirateWaster) · kind `Drifter` · xenotype Baseliner · tôn giáo Astropolitan (69%)
- **Xuất thân / tính cách:** UrbworldUrchin61 / CaveworldIlluminator95 · trait: Undergrounder
- **Hiện tại:** ô (0,72) · rảnh (không có job) · lịch giờ này: —
- **Thân phận:** hostFaction=— · guestStatus=— · đã được chữa 0 lần · questTags: — · vào map lúc 9 Aprimay 5501 12:48
- **Tâm trạng:** 50.0%
- **Nhu cầu:** Food 80% · Rest 94%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (0, xếp từ mới → cũ; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** —
- **Sức khỏe** (trạng thái `Mobile`; 0 hediff):

*(không có hediff nào)*

- **Kỹ năng:** Shooting 8★★ · Melee 6 · Construction 6 · Mining 9★★ · Cooking 3 · Plants 4 · Animals 1 · Crafting 0 · Artistic 4 · Medicine 1 · Social 7★ · Intellectual 4
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_Pants (Leather_Light, Poor), Apparel_CollarShirt (Cloth, Poor), Apparel_Tuque (Cloth, Poor) · **Cầm:** MeleeWeapon_Club (BlocksMarble) · **Túi:** WakeUp ×2
- **Thiết lập:** giường riêng: chưa có · y tế: — · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «—»


## 4. Ma trận công việc (ai bật việc gì)

Số = mức ưu tiên (1 cao nhất), `·` = tắt; `kn` = cấp kỹ năng liên quan. Thứ tự hàng = thứ tự game xét khi cùng mức ưu tiên (trên trước). Chế độ ưu tiên thủ công: True.

| Việc | Tên | bac si | eistein | Protein | Ghi chú |
|---|---|---|---|---|---|
| `Firefighter` | Chữa cháy | · | 1 | 1 |  |
| `Patient` | Bệnh nhân | 1 | 1 | 1 |  |
| `Doctor` | Bác sĩ | 1 (kn 8) | · (kn 4) | · (kn 4) |  |
| `PatientBedRest` | Nằm nghỉ dưỡng | 3 | 3 | 3 |  |
| `BasicWorker` | Việc cơ bản | 3 | 3 | 3 |  |
| `Warden` | Cai ngục | · (kn 2) | 3 (kn 9) | · (kn 4) |  |
| `Handling` | Thuần hóa | · (kn 2) | · (kn 4) | 1 (kn 6) |  |
| `Cooking` | Nấu ăn | · (kn 1) | 1 (kn 7) | 1 (kn 8) |  |
| `Hunting` | Săn bắn | 1 (kn 10) | · (kn 1) | 1 (kn 3) |  |
| `Construction` | Xây dựng | 1 (kn 4) | 1 (kn 5) | · (kn 2) |  |
| `Growing` | Trồng trọt | · (kn 4) | · (kn 3) | 1 (kn 11) |  |
| `Mining` | Khai thác | · (kn 1) | 2 (kn 3) | 3 (kn 3) |  |
| `PlantCutting` | Chặt cây | 2 (kn 4) | 2 (kn 3) | 1 (kn 11) |  |
| `Smithing` | Rèn | · (kn 0) | · (kn 2) | · (kn 4) | **KHÔNG AI LÀM** |
| `Tailoring` | May mặc | · (kn 0) | · (kn 2) | · (kn 4) | **KHÔNG AI LÀM** |
| `Art` | Nghệ thuật | · (kn 3) | · (kn 7) | · (kn 2) | **KHÔNG AI LÀM** |
| `Crafting` | Chế tạo | · (kn 0) | · (kn 2) | · (kn 4) | **KHÔNG AI LÀM** |
| `Hauling` | Khiêng vác | 1 | 1 | 1 |  |
| `Cleaning` | Dọn dẹp | 1 | 1 | 1 |  |
| `Research` | Nghiên cứu | · (kn 2) | 1 (kn 9) | 1 (kn 6) |  |
| `Childcare` | Chăm trẻ | · | · | · | **KHÔNG AI LÀM** |
| `DarkStudy` | Nghiên cứu hắc ám | · (kn 2) | · (kn 9) | · (kn 6) | **KHÔNG AI LÀM** |
| `Fishing` | Câu cá | · (kn 2) | · (kn 4) | · (kn 6) | **KHÔNG AI LÀM** |


## 5. Căn cứ

Tâm căn cứ (trung bình toạ độ tường/cửa của bạn): (129,143); bao tường: x 93–152, z 129–156. Tổng 271 công trình của bạn.


### 5.1 Sơ đồ căn cứ

```
 162 .............................................................................^
 161 .............................................................................^
 160 .............................................................................^
 159 .............................................................................^
 158 ..............................................................................
 157 ..............................................................................
 156 ..................................................###################.........
 155 ..................................................#_____#____a#____M#.........
 154 ..................................................#_____#__o__#__o__#.........
 153 ..................................................#_____#_____#_____#.........
 152 ..................................................#_____#__*__#_____#.........
 151 ..............................,,.............V....#_____#_____#_____#.........
 150 ..............................,i,.................#_____#+#####+#####.........
 149 ..............................,,,,................#_________________#.........
 148 ...............................,,.....######+###############+########.........
 147 ......................................#___________M#________________#.........
 146 ......................................#_________o__#___R____________#.........
 145 ::&&:::&:###############..............#____________#___c____*_______#.........
 144 :::&::&::#ii::::iii:iii#..............#______*_____+________________#.........
 143 &&&:&::::#:i::::i::ii::#..............#____________#________________#.........
 142 &:&:&&:::#ii:ii:iiii:::#..............#____________#________________#.........
 141 :&:&&&:&&#iiiiii::i::i:#""""""""",,,,,######+########################.........
 140 :::&&&&::#ii::ii::i::::#,,""""""",,,,,#____________##&:::i:i::::::::#.........
 139 .........#iiiiii:ii:ii:#,,"","""",,,,"#_iS___c_____##:::::::::::::::#.........
 138 .........#iiiiii:ii:::i#,,"""""""",,""#_cc_2_J_____##:::::::::::::::#.........
 137 .........#i:iiiii:ii:::#,,"",,""""""""#Tc__*_c__c__##:::::::::::::::#.........
 136 .........#i:iiiiii:ii::#""""",""""""""#_________K__++:::::::::::::::#.........
 135 .........#iiiii:ii::::i#""""""""""""""######+###############C########.........
 134 .........#iiii:ii:::i::#......................................................
 133 .........#:i:iii:i:i:::+......................................................
 132 .........#i:i:i:i::i:::#......................................................
 131 .........#:i::iiii:i:::#......................................................
 130 .........#:i:i::i::::::#......................................................
 129 .........###############.........................%............................
 128 ....................................F............%............................
 127 ...................................J........%.................................
 126 ...................................................J.........V................
 125 ..............................................................................
 124 ..............................................................................
 123 ......................................................%.......................
     000000000000000011111111111111111111111111111111111111111111111111111111111111
     888888999999999900000000001111111111222222222233333333334444444444555555555566
     456789012345678901234567890123456789012345678901234567890123456789012345678901
```

Khung vẽ: x 84–161, z 123–162. BẮC ở trên (z lớn), ĐÔNG bên phải (x lớn). Số bên trái = z của hàng; 3 hàng số dưới cùng = x của cột (trăm/chục/đơn vị). Mỗi công trình chỉ vẽ tại ô gốc (pos); công trình nhiều ô (giường 1×2, bếp 3×1, bàn…) chiếm thêm ô bên cạnh. Ký tự trên cùng che ký tự dưới (người > động vật > bản vẽ > công trình > xác > vật phẩm > zone > nền).
Chú thích: `#` tường · `+` cửa · `M` giường bệnh · `*` đuốc/đèn · `F` lửa trại · `T` bàn ăn · `c` ghế · `S` bếp · `K` bàn mổ thịt · `R` bàn nghiên cứu · `J` đồ giải trí (cọc móng ngựa/bàn cờ) · `o` điểm thiền · `C` máy lạnh · `V` mạch nước nóng · `&` xác chết · `i` vật phẩm · `a` động vật · `%` phế tích/đồ cổ không phải của bạn · `"` cây trồng · `,` ô ruộng trống · `:` ô kho trống · `^` vách đá tự nhiên · `_` sàn đã lát · `.` nền tự nhiên
Người: 2 = eistein (127,138) · a = Protein (145,155)


### 5.2 Phòng / vùng kín thuộc căn cứ

*Game không lưu danh sách phòng; công cụ tự loang tìm vùng bị tường/đá/cửa bao kín. Nhiệt độ lấy từ lưới nhiệt lưu trong save.*

| Phòng | Bao | Số ô | Có mái | Nhiệt độ | Sàn | Cửa tại | Bên trong |
|---|---|---|---|---|---|---|---|
| R1 | x 123–134, z 142–147 | 72 | 72/72 | 18.1°C | WoodPlankFloor×72 | (128,141), (128,148), (135,144) | TorchLamp×1; Bed×1; MeditationSpot×1; [giường bệnh (134,147): chưa gán]; bẩn ×20 |
| R2 | x 123–134, z 136–140 | 60 | 60/60 | 18.2°C | WoodPlankFloor×60 | (128,135), (128,141), (135,136) | Table1x2c×1; FueledStove×1; DiningChair×4; TorchLamp×1; ChessTable×1; TableButcher×1; Stool×2; vật phẩm: Meat_Alpaca×6, Leather_Camel×26, Meat_Pig×3; đang ở trong: eistein; bẩn ×6 |
| R3 | x 136–151, z 142–147 | 96 | 96/96 | 16.9°C | WoodPlankFloor×96 | (135,144), (144,148) | TorchLamp×1; DiningChair×1; SimpleResearchBench×1; bẩn ×11 |
| R4 | x 137–151, z 136–140 | 75 | 0/75 | 14.9°C | WoodPlankFloor×75 | (136,136) | vật phẩm: RawRice×23, Meat_Alpaca×75; XÁC: Corpse_WildBoar (tươi)×1; zone: Stockpile zone 1 (75 ô); bẩn ×29 |
| R5 | x 135–151, z 149–155 | 47 | 47/47 | 15.9°C | WoodPlankFloor×47 | (141,150), (144,148), (147,150) | bẩn ×2 |
| R6 | x 141–145, z 151–155 | 25 | 25/25 | 23.0°C | WoodPlankFloor×25 | (141,150) | MeditationSpot×1; TorchLamp×1; Bed×1; [giường bệnh (145,155): chưa gán]; đang ở trong: Protein; bẩn ×2 |
| R7 | x 147–151, z 151–155 | 25 | 25/25 | 14.6°C | WoodPlankFloor×25 | (147,150) | MeditationSpot×1; Bed×1; [giường bệnh (151,155): chưa gán]; bẩn ×3 |
| R8 | x 94–106, z 130–144 | 195 | 192/195 | 10.9°C | WoodPlankFloor×195 | (107,133) | vật phẩm: Steel×655, WoodLog×3360, MeleeWeapon_Knife×1, Leather_Light×54, ComponentIndustrial×27, Leather_Plain×26, Silver×742, Leather_Camel×50, MealFine×33, Gun_BoltActionRifle×1, Apparel_Pants×1, Leather_Pig×71, Apparel_BasicShirt×1, MedicineHerbal×19, Leather_Wolf×26, Gun_Revolver×1, MedicineIndustrial×4, MealSimple×8, Gun_Autopistol×1; zone: Vùng kho chứa 1 (195 ô); bẩn ×25 |

**Chỉ số phòng do chính game tính** (lấy từ sự kiện gần nhất có ghi kèm bối cảnh; ấn tượng/đẹp/sạch càng âm càng tệ): `Bedroom`: ấn tượng 20.2, đẹp -0.1, sạch -0.2 (lúc 7 Aprimay 5501 09:04); `Room`: ấn tượng 11.4, đẹp -2.5, sạch -0.4 (lúc 14 Decembary 5500 01:52); `Kitchen`: ấn tượng -17.3, đẹp -2.2, sạch -2.8 (lúc 8 Aprimay 5501 20:31); `Hospital`: ấn tượng 23.9, đẹp 0, sạch 0 (lúc 3 Aprimay 5501 00:18)


### 5.3 Công trình của bạn

| Def | Vật liệu | SL | Vị trí | HP | Chi tiết |
|---|---|---|---|---|---|
| `Wall` | WoodLog | 190 | 190 cái trong x 93–152, z 129–156 | 177–195 |  |
| `Wall` | Steel | 45 | 45 cái trong x 135–152, z 135–141 | 300 |  |
| `Door` | WoodLog | 10 | 10 cái trong x 107–147, z 133–150 | 104 |  |
| `DiningChair` | WoodLog | 5 | (125,138), (132,137), (139,145), (129,139), (129,137) | 65 |  |
| `TorchLamp` | — | 4 | (127,137), (144,145), (129,144), (143,152) | 75 | (127,137): nhiên liệu 10.3 · (144,145): nhiên liệu 10.4 · (129,144): nhiên liệu 10.2 · (143,152): nhiên liệu 10.3 |
| `MeditationSpot` | — | 3 | (132,146), (143,154), (149,154) | — | (132,146): gán cho: bac si · (143,154): gán cho: eistein · (149,154): gán cho: Protein |
| `Bed` | WoodLog | 3 | (134,147), (151,155), (145,155) | 91 | (134,147): gán cho: chưa ai, giường bệnh · (151,155): gán cho: chưa ai, giường bệnh · (145,155): gán cho: chưa ai, giường bệnh |
| `HorseshoesPin` | WoodLog | 2 | (119,127), (135,126) | 25–49 |  |
| `Stool` | WoodLog | 2 | (124,137), (124,138) | 49 |  |
| `Cooler` | — | 1 | (144,135) | 100 | (144,135): powerOn=False, targetTemperature=21 |
| `Campfire` | — | 1 | (120,128) | 80 | (120,128): nhiên liệu 2.9 |
| `ChessTable` | WoodLog | 1 | (129,138) | 65 |  |
| `Table1x2c` | WoodLog | 1 | (123,137) | 49 |  |
| `TableButcher` | WoodLog | 1 | (132,136) | 117 | (132,136): bill: ButcherCorpseFlesh (lặp mãi) |
| `FueledStove` | — | 1 | (125,139) | 180 | (125,139): bill: CookMealFineBulk (lặp mãi), nhiên liệu 19.3 |
| `SimpleResearchBench` | WoodLog | 1 | (139,146) | 162 |  |


## 6. Kho & tài nguyên

| Def | Tên | Tổng | Nằm ở đâu | Ghi chú |
|---|---|---|---|---|
| `WoodLog` | Gỗ | 3935 | Vùng kho chứa 1: 3360, Growing zone 1: 433, ngoài zone: 142 |  |
| `Steel` | Thép | 921 | Vùng kho chứa 1: 655, ngoài zone: 266 |  |
| `Silver` | Bạc | 742 | Vùng kho chứa 1: 742 |  |
| `GravlitePanel` | Tấm Gravlite | 348 | ngoài zone: 348 |  |
| `Meat_Alpaca` | Meat Alpaca | 81 | Stockpile zone 1: 75, ngoài zone: 6 | ×6 hỏng sau ~1.97 ngày; ×75 hỏng sau ~1.97 ngày |
| `Leather_Camel` | Leather Camel | 76 | Vùng kho chứa 1: 50, ngoài zone: 26 |  |
| `Leather_Pig` | Leather Pig | 71 | Vùng kho chứa 1: 71 |  |
| `Leather_Light` | Leather Light | 54 | Vùng kho chứa 1: 54 |  |
| `MedicineHerbal` | Thuốc thảo dược | 34 | Vùng kho chứa 1: 19, ngoài zone: 8, Growing zone 1: 7 |  |
| `MealFine` | Suất ăn ngon | 33 | Vùng kho chứa 1: 33 | ×10 hỏng sau ~3.54 ngày; ×10 hỏng sau ~3.28 ngày; ×10 hỏng sau ~2.62 ngày; ×3 hỏng sau ~1.57 ngày |
| `RawRice` | Gạo sống | 33 | Stockpile zone 1: 23, Vùng trồng trọt 2: 10 |  |
| `ComponentIndustrial` | Linh kiện công nghiệp | 27 | Vùng kho chứa 1: 27 |  |
| `Leather_Wolf` | Leather Wolf | 26 | Vùng kho chứa 1: 26 |  |
| `Leather_Plain` | Leather Plain | 26 | Vùng kho chứa 1: 26 |  |
| `Luciferium` | Luciferium | 15 | trong sương mù: 15 | bị cấm ×15 tại (201,74) |
| `MealSimple` | Suất ăn đơn giản | 8 | Vùng kho chứa 1: 8 | ×8 hỏng sau ~1.31 ngày |
| `MedicineIndustrial` | Thuốc công nghiệp | 4 | Vùng kho chứa 1: 4 |  |
| `Meat_Pig` | Meat Pig | 3 | ngoài zone: 3 | ×3 hỏng sau ~1.3 ngày |
| `BiomutationPulser` | Máy tạo đột biến | 1 | trong sương mù: 1 | bị cấm ×1 tại (198,77) |
| `Apparel_BasicShirt` | Áo sơ mi cơ bản | 1 | Vùng kho chứa 1: 1 | Normal/Cloth |
| `Gun_Autopistol` | Súng ngắn tự động | 1 | Vùng kho chứa 1: 1 | Normal |
| `Apparel_Pants` | Quần | 1 | Vùng kho chứa 1: 1 | Normal/Synthread |
| `Gun_Revolver` | Súng lục ổ xoay | 1 | Vùng kho chứa 1: 1 | bị cấm ×1 tại (103,131); Normal |
| `MeleeWeapon_Knife` | Dao | 1 | Vùng kho chứa 1: 1 | Poor/Steel |
| `Gun_BoltActionRifle` | Súng trường bolt-action | 1 | Vùng kho chứa 1: 1 | Normal |

Trong túi thuộc địa viên (chưa tính ở bảng trên): `MedicineIndustrial`×3, `MealFine`×1, `MealSimple`×1.

**Lương thực cho người** *(ước tính theo dinh dưỡng vanilla; đã gồm cả đồ ăn trong túi thuộc địa viên)*: `MealFine`×34 (=30.6), `MealSimple`×9 (=8.1), `Meat_Alpaca`×81 (=4.05), `RawRice`×33 (=1.65), `Meat_Pig`×3 (=0.15) → tổng 44.55 dinh dưỡng nguyên trạng, 48.95 nếu nấu hết thành suất đơn giản; 3 người ăn cần 4.8/ngày → **≈ 9.3–10.2 ngày**.


### Vùng kho

| Zone | Bao | Ô đã dùng | Ô có mái | Ưu tiên | Cho phép | Cách tâm căn cứ | Đang chứa |
|---|---|---|---|---|---|---|---|
| Vùng kho chứa 1 | x 94–106, z 130–144 | 104/195 | 192/195 | Normal | 834 def | 30 ô Tây | WoodLog×3360, Silver×742, Steel×655, Leather_Pig×71, Leather_Light×54, Leather_Camel×50, MealFine×33, ComponentIndustrial×27, Leather_Wolf×26, Leather_Plain×26 |
| Vùng kho chứa 2 | x 234–244, z 143–151 | 14/99 | 0/99 | Normal | 39 def (38 loại xác) | 110 ô Đông | Corpse_Human (đã khô)×6, Corpse_Mech_Pikeman (không phân hủy)×3, Corpse_Mech_Scyther (không phân hủy)×2, Corpse_Ibex (đã khô)×1, Corpse_Rat (đã khô)×1, Corpse_Human (tươi)×1 |
| Stockpile zone 1 | x 136–151, z 136–140 | 4/76 | 0/76 | Important | 271 def (115 loại xác); cấm: AllowRotten | 15 ô Đông | Meat_Alpaca×75, RawRice×23, Corpse_WildBoar (tươi)×1 |
| Dumping stockpile zone 1 | x 84–92, z 140–145 | 23/54 | 0/54 | Normal | 153 def (152 loại xác); cấm: AllowCorpsesColonist, AllowCorpsesStranger, AllowCorpsesSlave, AllowCorpsesUnnatural | 41 ô Tây | Corpse_Horse (đã khô)×5, Corpse_Rat (đã khô)×3, Corpse_Squirrel (đã khô)×3, Corpse_Tortoise (đã khô)×2, Corpse_Ibex (đã khô)×2, Corpse_Raccoon (đã khô)×2, Corpse_Hare (đã khô)×2, Corpse_Warg (đã khô)×1, Corpse_Donkey (đã khô)×1, Corpse_Mink (đã khô)×1 |


## 7. Trồng trọt

| Ruộng | Cây đặt trồng | Số ô | Bao | Số cây trồng hiện có | Độ lớn | Cây dại mọc lẫn | Đất | Cho phép | Cách tâm căn cứ |
|---|---|---|---|---|---|---|---|---|---|
| Vùng trồng trọt 1 | `Plant_Rice` | 98 | x 108–121, z 135–141 | **70** | 62%–100% (TB 100%), chín: 69 | Plant_TreeOak×1 | Soil×98 | gieo: có, cắt: có | 16 ô Tây |
| Vùng trồng trọt 2 | `Plant_Rice` | 11 | x 114–117, z 148–151 | **0** | — | — | SoilRich×11 | gieo: có, cắt: có | 15 ô Tây Bắc |
| Growing zone 1 | `Plant_Healroot` | 83 | x 131–145, z 174–188 | **76** | 38%–100% (TB 53%), chín: 7 | Plant_TallGrass×1 | SoilRich×83 | gieo: có, cắt: có | 39 ô Bắc |
| Growing zone 2 | `Plant_Healroot` | 15 | x 131–138, z 172–176 | **15** | 43%–65% (TB 56%), chín: 0 | — | SoilRich×15 | gieo: có, cắt: có | 31 ô Bắc |

Thực vật hoang trên map: 22,296 cây, trong đó 10,291 cây gỗ, `Plant_Berry`×72, `Plant_HealrootWild`×67, `Plant_TreeAnima`×1.


## 8. Việc đã đánh dấu (designations)

| Lệnh | Mục tiêu | SL | Phạm vi | Gần căn cứ nhất | Thuộc việc |
|---|---|---|---|---|---|
| HarvestPlant | `Plant_HealrootWild` | 9 | x 57–211, z 0–123 | (80,123) (53 ô Tây) | PlantCutting |
| MineVein | `MineableSteel` | 9 | x 169–172, z 189–194 | (169,189) (61 ô Đông Bắc) | Mining |


## 9. Mối đe doạ & địa điểm đáng chú ý trên map


### Nhóm pawn do AI điều khiển (lord)

| Lord | Phe | Quan hệ | Kiểu hành vi | Tham số | Thành viên | Cách căn cứ |
|---|---|---|---|---|---|---|
| Lord_0 | bầy cỗ máy chiến đấu cơ (Mechanoid) | Hostile | `LordJob_SleepThenAssaultColony` | faction=Faction_8, wakeOnPawnUnfogged=True | Mech_Militor (205,67); Mech_Scorcher (198,66); Mech_Militor (201,74) | 107 ô Đông Nam |
| Lord_20 | Camro dân tộc (TribeCivil) | Neutral | `LordJob_TradeWithColony` | faction=Faction_2, chillSpot=(154, 0, 164) | Human «Chimpanzee Lernene» (58,201); Human «Petronas Lisneare» (57,202); Human «Bico “Lobster” Croibarro» (59,210); Human «Zeeurke Meme» (55,203); Muffalo (57,212); Human «Toad Netradordoa» (53,204); Human «Daga Goléroalbo» (54,204); Human «Grasshopper Breixos» (55,203); Human «Govasre “Crow” Lemeada» (55,203); Human «Dobreibo Combo» (56,203); Human «Snail Ñoba» (57,202); Human «Black Mouse» (54,204); Human «Hedgehog Maulo» (55,203); Human «Bat Croidor» (57,202); Human «Hare Canto» (55,203); Human «Seara Comareiro» (56,203); Human «Badger Breica» (54,204); Human «Rababarne Reivexa» (59,210); Human «Abanqueiro Rogua» (56,203); Human «Orange Grouse» (56,203) | 92 ô Tây Bắc |
| Lord_21 | Khí độc đàn ông (PirateWaster) | Hostile | `LordJob_StageThenAttack` | faction=Faction_6, stageLoc=(24, 0, 78), raidSeed=-1261668895, canTimeoutFlee=True, canKidnap=True, canSteal=True, delay=5000~15000 | Human «Shinichi “Dude” Henry» (0,72) | 147 ô Tây Nam |

| Mech | Ô | Phe | Trạng thái | Trong sương mù | Cách căn cứ |
|---|---|---|---|---|---|
| `Mech_Militor` | (205,67) | bầy cỗ máy chiến đấu cơ (Mechanoid) | ngủ đông (dormant), job `LayDown`, duty `SleepForever` | có | 107 ô Đông Nam |
| `Mech_Scorcher` | (198,66) | bầy cỗ máy chiến đấu cơ (Mechanoid) | ngủ đông (dormant), job `LayDown`, duty `SleepForever` | có | 103 ô Đông Nam |
| `Mech_Militor` | (201,74) | bầy cỗ máy chiến đấu cơ (Mechanoid) | ngủ đông (dormant), job `LayDown`, duty `SleepForever` | có | 100 ô Đông Nam |


### Vùng kín khác trên map (phế tích, hầm cổ…)

| Phòng | Bao | Số ô | Có mái | Nhiệt độ | Sàn | Cửa tại | Bên trong | Cách căn cứ |
|---|---|---|---|---|---|---|---|---|
| R9 | x 191–205, z 63–80 | 204 | 204/204 | 10.5°C | TileMarble×142, AncientTile×50, AncientConcrete×12 | — | **TOÀN BỘ TRONG SƯƠNG MÙ — người chơi chưa nhìn thấy bên trong**; AncientBarrel×1 (không phải của bạn); SteleLarge×3 (không phải của bạn); AncientCryptosleepCasket×6 (không phải của bạn); Sarcophagus×1 (không phải của bạn); Table2x2c×1 (không phải của bạn); AncientHermeticCrate×1 (không phải của bạn); AncientCryptosleepCasket@(202,71) chứa Human «Sarah “Four Eyes” Renault» [AncientSoldier, 21.5 tuổi, phe Người cổ đại (Ancients), quan hệ Neutral, vũ khí Gun_Incinerator]; AncientCryptosleepCasket@(196,67) chứa Human «Beryl “Zamora” Zamora» [AncientSoldier, 45.1 tuổi, phe Người cổ đại (AncientsHostile), quan hệ Hostile, vũ khí Gun_EmpLauncher]; AncientCryptosleepCasket@(196,73) chứa Human «Amaya “Lover” Farrell» [AncientSoldier, 88.6 tuổi, phe Người cổ đại (Ancients), quan hệ Neutral, vũ khí Gun_HeavySMG]; AncientCryptosleepCasket@(193,67) chứa xác Manuel “Lutz” Lutz; AncientCryptosleepCasket@(199,71) chứa Human «Rachel “Melton” Melton» [AncientSoldier, 41.2 tuổi, phe Người cổ đại (Ancients), quan hệ Neutral, vũ khí Gun_MachinePistol]; AncientCryptosleepCasket@(199,67) chứa Human «Andreas “Lauv” Lauvhjell» [AncientSoldier, 53.8 tuổi, phe Người cổ đại (Ancients), quan hệ Neutral, vũ khí Gun_HellcatRifle]; Megascarab [không phe] ×3; AncientHermeticCrate@(203,69) chứa Techprint_SkinHardening; vật phẩm: BiomutationPulser×1, Luciferium×15; đang ở trong: Mech_Scorcher, Mech_Militor, Mech_Militor | 100 ô Đông Nam |


### Công trình không phải của bạn

| Def | SL | Vị trí | Gần căn cứ nhất | Trong sương mù | Chi tiết |
|---|---|---|---|---|---|
| `Wall` | 186 | x 101–232, z 24–199 | (105,119) (34 ô Tây Nam) | 23/186 |  |
| `Door` | 10 | x 103–232, z 26–194 | (103,119) (35 ô Tây Nam) |  |  |
| `Column` | 9 | x 157–227, z 25–197 | (157,197) (61 ô Đông Bắc) |  |  |
| `ShipChunk` | 8 | x 40–196, z 15–213 | (135,165) (23 ô Bắc) |  |  |
| `AncientCryptosleepCasket` | 6 | (199,67), (196,67), (199,71), (196,73), (202,71), (193,67) | (196,73) (97 ô Đông Nam) | 6/6 | (199,67) chứa Human «Andreas “Lauv” Lauvhjell» [AncientSoldier, 53.8 tuổi, phe Người cổ đại (Ancients), quan hệ Neutral, vũ khí Gun_HellcatRifle]; Megascarab [không phe] ×3; (196,67) chứa Human «Beryl “Zamora” Zamora» [AncientSoldier, 45.1 tuổi, phe Người cổ đại (AncientsHostile), quan hệ Hostile, vũ khí Gun_EmpLauncher]; (199,71) chứa Human «Rachel “Melton” Melton» [AncientSoldier, 41.2 tuổi, phe Người cổ đại (Ancients), quan hệ Neutral, vũ khí Gun_MachinePistol]; (196,73) chứa Human «Amaya “Lover” Farrell» [AncientSoldier, 88.6 tuổi, phe Người cổ đại (Ancients), quan hệ Neutral, vũ khí Gun_HeavySMG]; (202,71) chứa Human «Sarah “Four Eyes” Renault» [AncientSoldier, 21.5 tuổi, phe Người cổ đại (Ancients), quan hệ Neutral, vũ khí Gun_Incinerator]; (193,67) chứa xác Manuel “Lutz” Lutz |
| `ShipChunk_Mech` | 6 | (232,2), (212,3), (221,16), (231,10), (214,8), (225,17) | (221,16) (157 ô Đông Nam) |  |  |
| `SteamGeyser` | 5 | (129,151), (132,78), (102,48), (145,126), (62,128) | (129,151) (8 ô Bắc) |  |  |
| `Sarcophagus` | 3 | (196,76), (231,47), (231,44) | (196,76) (95 ô Đông Nam) | 1/3 |  |
| `SteleLarge` | 3 | (202,75), (202,67), (198,75) | (198,75) (97 ô Đông Nam) | 3/3 |  |
| `AncientShipBeacon` | 2 | (56,31), (65,31) | (65,31) (129 ô Tây Nam) |  |  |
| `AncientMechDropBeacon` | 1 | (80,76) | (80,76) (83 ô Tây Nam) |  |  |
| `AncientHermeticCrate` | 1 | (203,69) | (203,69) (105 ô Đông Nam) | 1/1 | (203,69) chứa Techprint_SkinHardening |
| `Table2x2c` | 1 | (203,72) | (203,72) (103 ô Đông Nam) | 1/1 |  |
| `GravEngine` | 1 | (230,13) | (230,13) (165 ô Đông Nam) |  | gravshipName=tàu hấp dẫn |
| `VoidMonolith` | 1 | (43,114) | (43,114) (91 ô Tây) |  | progress=0; studyEnabled=False |

Đồ cổ/phế tích khác (trang trí, không chứa gì): `AncientConcreteBarrier`×41 (gần nhất (138,113)), `AncientFence`×23 (gần nhất (120,73)), `AncientWheel`×12 (gần nhất (133,129)), `AncientRazorWire`×12 (gần nhất (61,201)), `AncientGiantWheel`×11 (gần nhất (65,63)), `AncientLamppost`×9 (gần nhất (147,111)), `AncientExostriderLeg`×3 (gần nhất (195,197)), `AncientRustedCar`×3 (gần nhất (128,119)), `AncientRustedEngineBlock`×2 (gần nhất (131,112)), `AncientSmallCrate`×2 (gần nhất (212,34)), `AncientPipelineSection`×2 (gần nhất (31,103)), `AncientOperatingTable`×2 (gần nhất (214,29)), `AncientRustedCarFrame`×2 (gần nhất (138,123)), `AncientPodCar`×2 (gần nhất (128,127)), `AncientBarrel`×1 (gần nhất (202,77)), `AncientRefrigerator`×1 (gần nhất (211,32)), `AncientExostriderHead`×1 (gần nhất (201,197)), `AncientGenerator`×1 (gần nhất (164,35)), `AncientExostriderCannon`×1 (gần nhất (198,199)), `AncientExostriderRemains`×1 (gần nhất (199,197)), `AncientMiniWarwalkerRemains`×1 (gần nhất (85,38)).

**Anomaly:** cấp `Inactive` · monolith `Thing_VoidMonolith36663` · kiến thức từ monolith 0.


## 10. Động vật

43 con trên map, trong đó 0 con đã thuần của bạn.

| Loài (hoang) | SL | Con gần căn cứ nhất | Trạng thái con đó | Ghi chú |
|---|---|---|---|---|
| `Deer` | 7 | (225,208) (116 ô Đông Bắc) | thức ăn 0.64, job GotoWander |  |
| `Alpaca` | 5 | (14,190) (124 ô Tây) | thức ăn 0.88, job Wait_MaintainPosture | 1 con có thương tật |
| `Quail` | 4 | (214,181) (93 ô Đông Bắc) | thức ăn 0.16, job GotoWander |  |
| `Turkey` | 3 | (123,15) (128 ô Nam) | thức ăn 0.54, job Wait_Wander | 1 con có thương tật |
| `Tortoise` | 3 | (217,152) (88 ô Đông) | thức ăn 0.41, job GotoWander |  |
| `Boomrat` | 3 | (119,220) (78 ô Bắc) | thức ăn 0.14, job Wait_MaintainPosture |  |
| `Hare` | 3 | (64,95) (81 ô Tây Nam) | thức ăn 0.20, job Wait_MaintainPosture |  |
| `Megasloth` | 2 | (175,122) (51 ô Đông Nam) | thức ăn 1.93, job Wait_Wander |  |
| `Squirrel` | 2 | (27,217) (126 ô Tây Bắc) | thức ăn 0.16, job Wait_Wander |  |
| `Raccoon` | 2 | (154,173) (39 ô Đông Bắc) | thức ăn 0.32, job Wait_Wander |  |
| `Bluebird` | 1 | (225,109) (102 ô Đông) | thức ăn 0.15, job GotoWander |  |
| `Wolf_Timber` | 1 | (59,86) (90 ô Tây Nam) | thức ăn 0.60, job GotoWander | THÚ SĂN MỒI |
| `Porcupine` | 1 | (225,214) (119 ô Đông Bắc) | thức ăn 0.29, job GotoWander |  |
| `Rhinoceros` | 1 | (61,37) (126 ô Tây Nam) | thức ăn 1.52, job Wait_Wander |  |
| `Fox_Red` | 1 | (203,204) (96 ô Đông Bắc) | thức ăn 0.35, job GotoWander | THÚ SĂN MỒI |
| `Bear_Grizzly` | 1 | (107,40) (105 ô Nam) | thức ăn 1.44, job GotoWander | THÚ SĂN MỒI |
| `Crow` | 1 | (139,184) (42 ô Bắc) | thức ăn 0.02, job Wait_Wander |  |
| `Badger` | 1 | (98,50) (98 ô Nam) | thức ăn 0.30, job GotoWander |  |
| `Muffalo` | 1 | (57,212) (100 ô Tây Bắc) | thức ăn 2.36, job Goto |  |

*«thức ăn» = mức dinh dưỡng đang có trong bụng (đơn vị dinh dưỡng; mức tối đa tuỳ kích cỡ loài, người = 1.0).*


## 11. Bản đồ

| Thuộc tính | Giá trị |
|---|---|
| Kích thước | 250 × 250 ô |
| Địa hình (số ô) | `Soil` 40,899, `Gravel` 6,391, `Marble_Rough` 5,162, `Granite_Rough` 2,792, `SoilRich` 2,219, `WaterShallow` 1,757, `Mud` 1,458, `BrokenAsphalt` 634, `WoodPlankFloor` 622, `AncientConcrete` 208, `TileMarble` 150, `FlagstoneGranite` 76, `TileSandstone` 72, `AncientTile` 50, `TileLimestone` 10 |
| Mái | `RoofRockThin` 1,769 (mái đá mỏng), `RoofConstructed` 925 (mái xây), `RoofRockThick` 806 (mái núi dày (không phá được)) |
| Vách đá / quặng / đá vụn (lớp nén) | `Marble` 2,073, `Granite` 997, `ChunkGranite` 713, `ChunkMarble` 646, `MineableSteel` 328, `MineableComponentsIndustrial` 44, `MineableSilver` 17, `MineableJade` 16, `ChunkSlagSteel` 6 |
| Sương mù | 2,869 ô chưa khám phá (4.6%) |
| Ô nhiễm / tuyết | 0 ô ô nhiễm; tuyết: không |
| Khí đang lơ lửng | `RotStink` (mùi xác thối) phủ 4 ô trong x 43–45, z 123–124 |
| Tài nguyên sâu đã dò ra (cho khoan sâu) | chưa có (chưa quét bằng máy quét sâu, hoặc không có gì) |
| Khu vực (area) | Area_Home 1137 ô [x 93–156, z 129–159], Area_BuildRoof 717 ô [x 93–152, z 129–164], Area_NoRoof 222 ô [x 122–152, z 135–156], Area_SnowOrSandClear 0 ô, Area_PollutionClear 0 ô, Khu vực 1 0 ô |
| Đường cổ cắt mép map tại | (0,95), (0,96), (0,97), (0,98), (249,197), (249,198), (249,199), (249,200) |


### 11.1 Toàn cảnh map

```
 245 ..."""""........'^^^^^.'...................^^^^^^.
 240 ...""""".......'..........................^'.'^^^.
 235 ....."".................................."....'^^'
 230 ..'$^'....................^.............."......^^
 225 ..^??^'............'.....'^.....................''
 220 ..'??^^.........'^'^.....''.......................
 215 ...^?^...................^''........'^^.........'^
 210 ..'^$^'................'^^'^.....'^^^?^..........^
 205 .....^^..............^^^^^^^"..^^^^^?$$'..........
 200 ......^.............^^^^^^^^...^^^^????^..........
 195 .......'.............'^'.......'^^^????^.........=
 190 .........,".....................^^?$???^.......==^
 185 .......,",".................z...^^?????^......='??
 180 ...,,",~~,"................zz...'^???^^'"....=='$?
 175 .~~~~~,,~,,...............zzz...'^???^'"""..==..^^
 170 .~~~~~~,"..................z...'^$??^."""".==.'.''
 165 .~~~~~~,"......................^^??^""""""==..'...
 160 .~~~~~~,.......................'??^'.""""==.......
 155 .~~~~~~,..................BBBBB.^^'.....==........
 150 .",~~~,.....^^........zz.SB_BBB..'.....==......zz.
 145 ...~~~.....'^'^'.zBBBBzzBBBBBBB.......==........z.
 140 ...~~.".,...''^.zzBzzB.zBBBBBBB......==........zz.
 135 ...,..",,.........B_zBzzBBBBBBB.....==............
 130 ..."..............B_zB.............==.............
 125 ......,."...S.....BBBB.......S....==..............
 120 ......,,,........................==...............
 115 ........=.....................====................
 110 ........V=.................===....................
 105 .......................====^..............'.......
 100 ^..................====.'^^^'...'^'.......'....,..
  95 ==========,,.=======..'^^^^^....^^^^..........~~..
  90 ...........,,,........^'^^'^....$??^.......,~~~~~~
  85 ...............................'^???'......~~~~~~~
  80 ...............................'^???^''...",~~~~~~
  75 ..........................S"...'^????$???...~~~~,'
  70 !..............................^???????K!...~~~...
  65 ...............................^^?????K!?!..~~~...
  60 ................................^??????^'...,~~...
  55 ................................^??$??^'.....,....
  50 .^..............................^^^^?^^...........
  45 .^'.'''^'........'^.S...........'^^^^^....".......
  40 .^^'^?^^^^.......^^............___.'^^....".._....
  35 ...^^???$^......'^^.............__..."..."......'.
  30 ...^???$?^.....^^^^.................."...._....'^^
  25 ...'^^$?^^.__..^^?^'......................_..'^^^^
  20 .....''^'......'^^?^'..........................'^^
  15 ...............'^^???$............................
  10 .................^???^'..........,............G...
   5 ......'^'........'$?^..........~~,................
   0 ......^^^'........^^'..........~..................
     00000000000000000000111111111111111111112222222222
     00112233445566778899001122334455667788990011223344
```

Mỗi ký tự = khối 5×5 ô; số bên trái = z của mép dưới khối, 2 hàng số dưới = x (trăm/chục) của mép trái khối. BẮC ở trên, ĐÔNG bên phải.
Chú thích: `B` căn cứ (tường/cửa của bạn) · `z` zone của bạn nằm ngoài căn cứ · `!` pawn thù địch · `K` kén ngủ đông cổ · `V` void monolith · `G` grav engine · `S` mạch nước nóng · `$` mạch quặng đã lộ · `^` núi/vách đá (≥50% khối) · `'` lác đác đá · `~` nước · `=` đường nhựa cổ · `,` bùn/lầy · `"` đất màu mỡ · `_` nền lát/nền đá · `?` sương mù · `.` đất thường


### 11.2 Mạch quặng

| Quặng | Số ô | Bao | Tâm | Cách căn cứ | Đã lộ | Đã đánh dấu đào |
|---|---|---|---|---|---|---|
| `MineableComponentsIndustrial` | 3 | x 167–168, z 172–173 | (168,172) | 49 ô Đông Bắc | một phần |  |
| `MineableComponentsIndustrial` | 6 | x 163–165, z 90–92 | (164,91) | 63 ô Đông Nam | một phần |  |
| `MineableSteel` * | 98 | x 169–185, z 189–199 | (178,193) | 70 ô Đông Bắc | một phần | 9 |
| `MineableComponentsIndustrial` | 4 | x 174–175, z 80–81 | (174,80) | 77 ô Đông Nam | KHÔNG (trong sương mù) |  |
| `MineableSilver` | 9 | x 163–165, z 70–72 | (164,71) | 80 ô Đông Nam | KHÔNG (trong sương mù) |  |
| `MineableJade` | 8 | x 173–174, z 72–75 | (174,74) | 82 ô Đông Nam | KHÔNG (trong sương mù) |  |
| `MineableJade` | 8 | x 184–186, z 78–80 | (185,79) | 85 ô Đông Nam | một phần |  |
| `MineableSteel` * | 37 | x 181–188, z 206–212 | (185,209) | 87 ô Đông Bắc | một phần |  |
| `MineableSilver` | 8 | x 177–179, z 62–65 | (178,64) | 93 ô Đông Nam | KHÔNG (trong sương mù) |  |
| `MineableComponentsIndustrial` | 5 | x 186–187, z 69–71 | (186,70) | 93 ô Đông Nam | KHÔNG (trong sương mù) |  |
| `MineableComponentsIndustrial` | 3 | x 193–194, z 209–210 | (194,209) | 93 ô Đông Bắc | có |  |
| `MineableComponentsIndustrial` | 3 | x 183–184, z 66–67 | (184,66) | 95 ô Đông Nam | KHÔNG (trong sương mù) |  |
| `MineableSteel` * | 33 | x 172–178, z 52–58 | (175,55) | 99 ô Đông Nam | một phần |  |
| `MineableComponentsIndustrial` | 5 | x 182–184, z 54–55 | (183,54) | 104 ô Đông Nam | KHÔNG (trong sương mù) |  |
| `MineableSteel` * | 33 | x 238–244, z 181–186 | (241,184) | 119 ô Đông | một phần |  |
| `MineableSteel` * | 32 | x 21–26, z 209–214 | (23,212) | 126 ô Tây Bắc | một phần |  |
| `MineableComponentsIndustrial` | 3 | x 104–105, z 16–17 | (105,17) | 128 ô Nam | một phần |  |
| `MineableSteel` * | 32 | x 40–45, z 35–41 | (43,38) | 136 ô Tây Nam | một phần |  |
| `MineableComponentsIndustrial` | 3 | x 18–19, z 230–231 | (19,231) | 141 ô Tây Bắc | có |  |
| `MineableComponentsIndustrial` | 4 | x 91–92, z 5–6 | (92,6) | 142 ô Nam | một phần |  |
| `MineableSteel` * | 64 | x 32–41, z 25–35 | (36,30) | 146 ô Tây Nam | một phần |  |
| `MineableComponentsIndustrial` | 5 | x 32–33, z 25–27 | (32,26) | 152 ô Tây Nam | một phần |  |

\* tên def suy từ mã băm gần đúng (game +1 khi hai def trùng mã) — khớp với ô đã đánh dấu đào/quặng đào dở liền kề.

**Đá vụn/xỉ nằm trên mặt đất** (vật liệu xây/đẽo gạch): `ChunkGranite`×735, `ChunkMarble`×672, `ChunkMechanoidSlag`×10, `ChunkSlagSteel`×6.

**Mạch nước nóng:** (129,151) (8 ô Bắc), (132,78) (65 ô Nam), (102,48) (99 ô Nam), (145,126) (23 ô Đông Nam), (62,128) (69 ô Tây).

**Vùng nước:** 8 vùng; có cá: gốc (225,61) 777 ô, quần thể 31.8, Fish_Bass (126 ô Đông Nam), gốc (19,139) 864 ô, quần thể 34.1, Fish_Salmon (110 ô Tây).


## 12. Xác chết trên map

| Nơi | Tình trạng | SL | Loại | Phạm vi | Cách căn cứ | Xác người |
|---|---|---|---|---|---|---|
| Dumping stockpile zone 1 | đã khô | 23 | Corpse_Rat×3, Corpse_Horse×5, Corpse_Tortoise×2, Corpse_Ibex×2, Corpse_Squirrel×3, Corpse_Raccoon×2, Corpse_Warg×1, Corpse_Hare×2, Corpse_Donkey×1, Corpse_Mink×1, Corpse_Sparrow×1 | x 84–92, z 140–145 | 45 ô Tây |  |
| Stockpile zone 1 | tươi | 1 | Corpse_WildBoar×1 | x 137–137, z 140–140 | 9 ô Đông |  |
| Vùng kho chứa 2 | đã khô | 8 | Corpse_Human×6, Corpse_Ibex×1, Corpse_Rat×1 | x 234–243, z 143–149 | 105 ô Đông | Diana “Diana” Stokes (Khí độc đàn ông (PirateWaster), chết 5 Decembary 5500); Azskar “Gray” akman (Khí độc đàn ông (PirateWaster), chết 11 Septober 5500); Nikolay “Reks” Reks (—, chết 5 Septober 5498 — từ trước khi lập thuộc địa); Oshul wttytt (—, chết 1 Decembary 5498 — từ trước khi lập thuộc địa); Buxdun aksmoke (Khí độc đàn ông (PirateWaster), chết 3 Decembary 5500); Jarod “Elphy” Elphinstone (Khí độc đàn ông (PirateWaster), chết 13 Decembary 5500) |
| Vùng kho chứa 2 | tươi | 1 | Corpse_Human×1 | x 237–237, z 147–147 | 108 ô Đông | Calvin “Tangle” Northwood (thực thể Bóng tối (Entities), chết 8 Aprimay 5501) |
| Vùng kho chứa 2 | không phân hủy | 5 | Corpse_Mech_Scyther×2, Corpse_Mech_Pikeman×3 | x 235–241, z 146–149 | 108 ô Đông |  |
| ngoài zone | đã khô | 2 | Corpse_Ibex×1, Corpse_Lynx×1 | x 39–235, z 68–76 | 130 ô Đông Nam |  |
| ngoài zone | không phân hủy | 3 | Corpse_Mech_Pikeman×3 | x 213–232, z 1–2 | 174 ô Đông Nam |  |
| ngoài zone | ĐANG THỐI | 1 | Corpse_Human×1 | x 44–44, z 123–123 | 87 ô Tây | Pigag “Rasher” Squiliork (Moigleoo (OutlanderRoughPig), chết 4 Aprimay 5501) |

*Xác tươi (<2,5 ngày ở ≥10°C) → thối rữa (toả khí gây LungRot, 2,5–5 ngày) → khô. Xác mech không phân hủy.*


## 13. Nghiên cứu

**Đang chọn:** `Batteries` — đã tích luỹ 0 điểm. **Đã xong (7):** `ComplexFurniture`, `PassiveCooler`, `Stonecutting`, `ComplexClothing`, `Electricity`, `NutrientPaste`, `AirConditioning`. Còn 116 dự án chưa đụng tới.

*Save chỉ lưu số điểm, không lưu chi phí hay cờ hoàn thành. Dự án có điểm là số nguyên tròn (game gán = chi phí khi xong) được coi là đã xong — suy luận, độ tin cậy cao.*


## 14. Nhiệm vụ


### «Temporary Workers» — CHƯA NHẬN (đang chờ quyết định)

| Thuộc tính | Giá trị |
|---|---|
| Loại (root) | `PawnLend` |
| Xuất hiện | 9 Aprimay 5501 10:00 (tick 1990000) |
| Hạn nhận | 2 Jugust 5501 02:07 — còn **7.6 ngày** |
| Độ khó | 2 sao |
| Mô tả | Nhà lãnh đạo Ryoko 'Onesan' Minese of Công ty thương gia needs extra hands to help watch for raiders. She is asking you to lend her 1 colonist 13 years old or older for 16 days. She will send a shuttle to pick up the colonist. |
| Phần thưởng (chọn 1) | Vật phẩm: PsychicAnimalPulser, Uranium ×90 **HOẶC** Pawn **HOẶC** Goodwill +23 [Công ty thương gia (TradersGuild)] |
| Mốc thời gian trong nhiệm vụ | Shuttle arrives in …: 1.4 giờ; Delay: 0.1 giờ |
| Nhân vật liên quan | Alistair “Alistair” Giles (Male, 46.4 tuổi, `SpaceRefugee`, —, đang ở ngoài map) |
| Phe liên quan | Công ty thương gia (TradersGuild) |
| Thất bại khi (tín hiệu) | map.MapRemoved |


### «The Revered Artifact» — CHƯA NHẬN (đang chờ quyết định)

| Thuộc tính | Giá trị |
|---|---|
| Loại (root) | `RelicHunt` |
| Xuất hiện | 8 Aprimay 5501 10:48 (tick 1932000) |
| Độ khó | 3 sao |
| Mô tả | You've learned that a valuable relic is nearby. The Horlink is one of 2 ancient objects venerated by many people. If you could collect it, you could build a reliquary to make your colonists happy and attract wealthy pilgrims. |
| Phần thưởng | Vật phẩm: Flamebow (Legendary) |
| Mốc thời gian trong nhiệm vụ | Delay: 3.0 ngày |
| Phe liên quan | Người cổ đại (AncientsHostile) |
| Thành công khi (tín hiệu) | RelicLostFromMap |
| Thất bại khi (tín hiệu) | relicThing.Destroyed |


### «Pollution Dump» — CHƯA NHẬN (đang chờ quyết định)

| Thuộc tính | Giá trị |
|---|---|
| Loại (root) | `PollutionDump` |
| Xuất hiện | 4 Aprimay 5501 10:48 (tick 1692000) |
| Hạn nhận | 9 Aprimay 5501 22:51 — còn **10.1 giờ** |
| Mô tả | Nhà lãnh đạo Petronella ere pus kio of Đế chế tan nát has a special request. Someone has dumped an abundance of toxic wastepacks near one of her settlements and she is unable to safely store them. If you accept, Petronella will deliver 90 toxic wastepacks by transport pod. If not kept frozen, toxic wastepacks will dissolve over time, polluting nearby terrain. |
| Phần thưởng (chọn 1) | Vật phẩm: ArchiteCapsule, Jade ×43 **HOẶC** Vật phẩm: Schematic (Good) «The Haunting Tube Televisions Dictionary», Uranium ×122 **HOẶC** Vật phẩm: MedicineUltratech ×19 |
| Mốc thời gian trong nhiệm vụ | Delay: 1.0 giờ |


### «Ship to the Stars» — ĐANG DIỄN RA

| Thuộc tính | Giá trị |
|---|---|
| Loại (root) | `EndGame_ShipEscape` |
| Xuất hiện | 11 Decembary 5500 06:00 (tick 1200000) |
| Đã nhận lúc | 11 Decembary 5500 06:00 (tự động) |
| Độ khó | 4 sao |
| Mô tả | A friendly AI from your past named Charlon Whitestone has sent you a message! He reveals that he has a starship hidden on this planet, and sends you its world coordinates. The starship is in deep hibernation mode. You'll have to start it up when you arrive, then defend it from raiders trying to steal it until the startup sequence completes. It will be a long, difficult series of battles. If you can get the ship off the ground, Charlon Whitestone will take you off this rimworld, to the stars. |
| Phần thưởng | PassageOffworld |
| Thành công khi (tín hiệu) | escapeShip.LaunchedShip |


### «Tín hiệu cơ học» — ĐANG DIỄN RA

| Thuộc tính | Giá trị |
|---|---|
| Loại (root) | `MechanoidSignal` |
| Xuất hiện | 12 Septober 5500 06:24 (tick 361000) |
| Đã nhận lúc | 12 Septober 5500 08:08 |
| Mô tả | Bạn đã phát hiện được tín hiệu từ một con tàu cơ khí trên quỹ đạo. Con tàu đã gặp trục trặc và đang dần mất độ cao. Bằng cách phản hồi sai tín hiệu, bạn có thể khiến con tàu rơi xuống gần đó, cho phép bạn trục vớt công nghệ trọng lực có giá trị. |
| Phần thưởng | Vật: GravEngine |
| Vật liên quan | `GravEngine` (230,13) |
| Thành công khi (tín hiệu) | gravEngine.Inspected |


### Nhiệm vụ đã kết thúc / hết hạn

| Nhiệm vụ | Loại | Kết cục | Xuất hiện | Ghi chú |
|---|---|---|---|---|
| «Chạy trốn phu nhân» | `Intro_Wimp` | đã hết hạn nhận | 14 Septober 5500 06:00 | thưởng lẽ ra: RoyalFavor +8 [Đế chế tan nát (Empire)] |
| «The Hard Prisoner» | `Hospitality_Prisoners` | đã hết hạn nhận | 11 Decembary 5500 06:24 | liên quan: Rebecca “Mercer” Mercer (đang ở ngoài map); thưởng lẽ ra: RoyalFavor +6 [Đế chế tan nát (Empire)] HOẶC Vật phẩm: null, null HOẶC Goodwill +20 [Đế chế tan nát (Empire)] |
| «RefugeePodCrash» | `RefugeePodCrash` | đã kết thúc: thành công | 12 Decembary 5500 16:00 | liên quan: Helena Arianites (đang ở ngoài map) |
| «Shoytt's Sad Survivors» | `Hospitality_Refugee` | đã hết hạn nhận | 14 Decembary 5500 06:24 | liên quan: Shoytt Barytt (đang ở ngoài map), Petronella ere pus kio (đang ở ngoài map); thưởng lẽ ra: VisitorsHelp; PossibleFutureReward |
| «The Deserter» | `Intro_Deserter` | đã hết hạn nhận | 2 Aprimay 5501 06:00 |  |
| «RefugeePodCrash» | `RefugeePodCrash` | đã kết thúc: thất bại | 4 Aprimay 5501 08:48 |  |
| «CreepJoinerArrival» | `CreepJoinerArrival` | đã kết thúc: thất bại | 6 Aprimay 5501 20:23 |  |


## 15. Phe phái

| ID | Tên | Loại | Quan hệ với bạn | Thiện chí | Số khu định cư | Thủ lĩnh | Ghi chú |
|---|---|---|---|---|---|---|---|
| Faction_7 | Đế chế tan nát | `Empire` | Neutral | 16 | 33 | Petronella ere pus kio |  |
| Faction_0 | Orussia | `OutlanderCivil` | Neutral | 0 | 36 | Elvira “Elvira” Arellano |  |
| Faction_2 | Camro dân tộc | `TribeCivil` | Neutral | 0 | 30 | Cự đà combo |  |
| Faction_11 | Người cổ đại | `Ancients` | Neutral | 0 | 0 | — |  |
| Faction_14 | Công ty thương gia | `TradersGuild` | Neutral | 0 | 0 | Ryoko “Onesan” Minese |  |
| Faction_1 | Moigleoo | `OutlanderRoughPig` | Hostile | -80 | 24 | Polag bopap |  |
| Faction_3 | Wen de bed | `TribeRoughNeanderthal` | Hostile | -80 | 38 | Meacabreixigo cómaro |  |
| Faction_4 | Fazechechz | `TribeSavageImpid` | Hostile | -100 | 33 | Zo kaznaz |  |
| Faction_5 | Kusytt | `PirateYttakin` | Hostile | -100 | 30 | Reece Clarke |  |
| Faction_6 | Khí độc đàn ông | `PirateWaster` | Hostile | -100 | 27 | Joshua “Marjot” Marjot |  |
| Faction_8 | bầy cỗ máy chiến đấu cơ | `Mechanoid` | Hostile | -100 | 0 | — |  |
| Faction_9 | trùng tộc | `Insect` | Hostile | -100 | 0 | — |  |
| Faction_10 | thực thể Bóng tối | `Entities` | Hostile | -100 | 0 | — |  |
| Faction_12 | Người cổ đại | `AncientsHostile` | Hostile | -100 | 0 | — |  |
| Faction_13 | Các Tôi Tớ Của Horax | `HoraxCult` | Hostile | -100 | 0 | — |  |
| Faction_15 | Các vũ trụ tội phạm | `Salvagers` | Hostile | -100 | 0 | Gage Buffington |  |

**Điểm đặc biệt trên bản đồ thế giới:** `Settlement` «nhung nguoi cung kho» tại ô thế giới 162296,0 [Quest11.map]; `EscapeShip` tại ô thế giới 286441,0 [Quest2.escapeShip]; `SpaceSettlement`×9 (phe: Công ty thương gia (TradersGuild)); `AsteroidBasic`×12 (tài nguyên quý: MineablePlasteel×4, MineableSteel×3, MineableSilver×2, MineableComponentsIndustrial×1, MineableJade×1, MineableGold×1).

**Tàu vận chuyển đang được game theo dõi:** `Shuttle` (—) [Quest11.pickupShipThing].


## 16. Dòng thời gian


### Diễn biến 3 ngày gần nhất (gộp chung mọi nguồn theo đúng thứ tự thời gian)

*Gộp thư, thông báo, trận đánh, sự kiện và xung đột xã hội trong 72 giờ qua thành một mạch duy nhất (cũ ở trên → mới nhất ở dưới).*

| Lúc | Cách đây | Nguồn | Diễn biến |
|---|---|---|---|
| 6 Aprimay 5501 20:23 | 2.7 ngày trước (2.7 ngày) | THƯ (`NeutralEvent`) | **Leathery stranger** — A ragged stranger with leathery skin is approaching your colony. He wants to talk. You can send a colonist to hear what he has to say. |
| 7 Aprimay 5501 08:53 | 2.2 ngày trước (2.2 ngày) | THƯ (`AcceptCreepJoiner`) | **Tangle wants to join** — The leathery stranger stares into space and speaks in a monotone, as though he hardly sees anyone or anything. He refuses to leave, insisting he is only interested in your colony.… |
| 7 Aprimay 5501 10:13–10:58 | 2.1 ngày trước (2.1 ngày) | chiến đấu | bac si ↔ WildBoar (thú hoang) — bac si → WildBoar: bắn 9 trúng 0 (`Gun_BoltActionRifle`) [4 phát vướng vật cản] |
| 7 Aprimay 5501 16:54 | 1.8 ngày trước (1.8 ngày) | xã hội | eistein → Protein: `Slight` (nói mỉa / coi thường) |
| 7 Aprimay 5501 18:01–8 Aprimay 5501 01:22 | 1.8 ngày trước (1.8 ngày) | chiến đấu | Protein, bac si, eistein ↔ Tangle (thực thể Bóng tối (Entities)) ↔ Boomrat (thú hoang) — bac si → Boomrat: bắn 12 trúng 0 (`Gun_BoltActionRifle`) [7 phát vướng vật cản]; Tangle → bac si: bắn 2 trúng 0 (`Gun_BoltActionRifle`) [1 phát vướng vật cản] + cận chiến 8 trúng 2 [1 lần là hất đất vào mắt]; bac si → Tangle: bắn 25 trúng 13 (`Gun_BoltActionRifle`) [5 phát vướng vật cản, huỷ 3 bộ phận] + cận chiến 17 trúng 12 (`Gun_BoltActionRifle`, tay không) [1 lần là hất đất vào mắt, huỷ 1 bộ phận]; Protein → Tangle: cận chiến 27 trúng 19 (tay không) [1 lần là hất đất vào mắt, huỷ 1 bộ phận]; Tangle → Protein: bắn 4 trúng 1 (`Gun_BoltActionRifle`) [1 phát vướng vật cản] + cận chiến 4 trúng 3 (`Gun_BoltActionRifle`) [1 lần là hất đất vào mắt]; eistein → Tangle: cận chiến 19 trúng 14 (`MeleeWeapon_Knife`, tay không) [1 lần là hất đất vào mắt, huỷ 5 bộ phận]; Tangle → eistein: cận chiến 1 trúng 1; **Tangle gục** (lúc 21:04, do eistein, `Cut`); **Tangle CHẾT** (lúc 22:26, do bac si, `Gunshot`); **Tangle gục** (lúc 23:09, do Protein, `Bruise`); **Tangle CHẾT** (lúc 23:36, do bac si, `Bruise`); **Tangle gục** (lúc 8 Aprimay 5501 00:00, do Protein, `Bruise`); **Tangle CHẾT** (lúc 8 Aprimay 5501 00:09, do eistein, `MissingBodyPart`); **Tangle gục** (lúc 8 Aprimay 5501 00:24, do bac si, `Bruise`); **Tangle CHẾT** (lúc 8 Aprimay 5501 00:31, do eistein, `Cut`); **Tangle gục** (lúc 8 Aprimay 5501 00:47, do bac si, `Gunshot`); **Tangle CHẾT** (lúc 8 Aprimay 5501 01:22, do Protein, `Bruise`) |
| 7 Aprimay 5501 20:23 | 1.7 ngày trước (1.7 ngày) | thông báo | Tangle has become hostile! |
| 7 Aprimay 5501 20:23 | 1.7 ngày trước (1.7 ngày) | THƯ (`ThreatBig`) | **Tangle hostile** — Upon being rejected, Tangle flew into a murderous rage and began to attack! |
| 7 Aprimay 5501 22:31 | 1.6 ngày trước (1.6 ngày) | thông báo | Tangle is using death refusal to self-resurrect. |
| 7 Aprimay 5501 23:43 | 1.5 ngày trước (1.5 ngày) | thông báo | Tangle is using death refusal to self-resurrect. |
| 8 Aprimay 5501 00:12 | 1.5 ngày trước (1.5 ngày) | thông báo | Tangle is using death refusal to self-resurrect. |
| 8 Aprimay 5501 00:36 | 1.5 ngày trước (1.5 ngày) | thông báo | Tangle is using death refusal to self-resurrect. |
| 8 Aprimay 5501 02:31 | 1.4 ngày trước (1.4 ngày) | THƯ (`NegativeEvent`) | **Sad wander: Protein** — Protein has broken down and is wandering around in sadness. This happened because of poor mood. The final straw was: Intense pain |
| 8 Aprimay 5501 04:22 | 1.4 ngày trước (1.4 ngày) | thông báo | Protein is no longer wandering in sadness. |
| 8 Aprimay 5501 08:00 | 1.2 ngày trước (1.2 ngày) | thông báo | A bookworm from Camro dân tộc is passing by. He is named Red Deer. |
| 8 Aprimay 5501 10:32 | 1.1 ngày trước (1.1 ngày) | thông báo | Pork x7 has rotted away in storage. |
| 8 Aprimay 5501 10:47 | 1.1 ngày trước (1.1 ngày) | thông báo | Eistein, Barkeep is fully healed. |
| 8 Aprimay 5501 10:48 | 1.1 ngày trước (1.1 ngày) | THƯ (`NewQuest`) | **Quest available: The Revered Artifact** — A new quest is available. The quest is called 'The Revered Artifact'. |
| 8 Aprimay 5501 11:20 | 1.1 ngày trước (1.1 ngày) | thông báo | Bac si, Bac si is fully healed. |
| 8 Aprimay 5501 18:48 | 18.0 giờ trước (0.8 ngày) | THƯ (`ThreatSmall`) | **Mad alpaca** — A local alpaca has gone mad. It will attack everyone it sees. |
| 8 Aprimay 5501 20:17–20:31 | 16.5 giờ trước (0.7 ngày) | chiến đấu | eistein, bac si ↔ Alpaca (thú hoang) — Alpaca → eistein: cận chiến 2 trúng 1; bac si → Alpaca: bắn 2 trúng 1 (`Gun_BoltActionRifle`) [1 phát vướng vật cản] + cận chiến 3 trúng 1 (`Gun_BoltActionRifle`); Alpaca → bac si: cận chiến 2 trúng 1; eistein → Alpaca: cận chiến 3 trúng 3 (`MeleeWeapon_Knife`); **Alpaca CHẾT** (do eistein) |
| 9 Aprimay 5501 03:32–05:33 | 9.3 giờ trước (0.4 ngày) | chiến đấu | bac si ↔ WildBoar (thú hoang) — bac si → WildBoar: bắn 20 trúng 2 (`Gun_BoltActionRifle`) [8 phát vướng vật cản, huỷ 2 bộ phận]; **WildBoar CHẾT** (lúc 05:33, do bac si, `MissingBodyPart`) |
| 9 Aprimay 5501 04:47 | 8.0 giờ trước (0.3 ngày) | thông báo | Eistein, Barkeep is fully healed. |
| 9 Aprimay 5501 09:37–12:26 | 3.2 giờ trước (0.1 ngày) | chiến đấu | bac si ↔ Boomrat (thú hoang) — bac si → Boomrat: bắn 26 trúng 2 (`Gun_BoltActionRifle`) [10 phát vướng vật cản, huỷ 4 bộ phận]; **Boomrat DiedExplosive** (lúc 12:26, do bac si) |
| 9 Aprimay 5501 10:00 | 2.8 giờ trước (0.1 ngày) | THƯ (`NewQuest`) | **Quest available: Temporary Workers** — A new quest is available. The quest is called 'Temporary Workers'. If you don't accept the quest within 8 days, it will expire. |
| 9 Aprimay 5501 11:10 | 1.6 giờ trước (0.1 ngày) | thông báo | Alpaca meat x71 has rotted away in storage. |
| 9 Aprimay 5501 11:35 | 1.2 giờ trước (0.1 ngày) | THƯ (`PositiveEvent`) | **Slaver from Camro dân tộc** — A caravan from Camro dân tộc is approaching. They are a slaver. They will hang around the colony for some time before leaving. You can attack them - but this will anger their fact… |
| 9 Aprimay 5501 12:03 | 0.7 giờ trước (0.0 ngày) | thông báo | Bac si, Bac si is fully healed. |
| 9 Aprimay 5501 12:26 | 0.4 giờ trước (0.0 ngày) | sự kiện (`Hunted`) | bac si săn được Boomrat |
| 9 Aprimay 5501 12:48 | 0.0 giờ trước (0.0 ngày) | THƯ (`ThreatBig`) | **Raid: Khí độc đàn ông** — A group of wasters from Khí độc đàn ông have arrived nearby. They will prepare for a while, then attack. Prepare a defense or attack them pre-emptively. |


### Thư (mọi thư từ đầu ván) và thông báo trong 5 ngày gần nhất

| Lúc | Cách đây (ngày) | Loại | Mức | Tiêu đề | Nội dung |
|---|---|---|---|---|---|
| 8 Septober 5500 18:00 | 30.8 | THƯ | NeutralEvent | Khách tham quan | Một Công chức từ Orussia đang tiến vào thuộc địa. Anh ta được đặt tên Kellan 'Kel' Cotter. Anh ta dường như có một vài mặt hàng để giao dịch. |
| 9 Septober 5500 15:35 | 29.9 | THƯ | ThreatSmall | Chồn bị điên | Một chồn gần đó đã phát điên. Nó sẽ tấn công tất cả mọi người mà nó nhìn thấy. |
| 11 Septober 5500 15:35 | 27.9 | THƯ | ThreatBig | Đột kích: Khí độc đàn ông | Một nhóm wasters từ Khí độc đàn ông đã đến gần đó. Họ đang tấn công ngay lập tức. |
| 11 Septober 5500 16:22 | 27.9 | THƯ | Death | Đã chết: Beelzebub (chuột cái) | Beelzebub bị chém chết. |
| 12 Septober 5500 06:24 | 27.3 | THƯ | NewQuest | Nhiệm vụ khả dụng: Tín hiệu cơ học | Có nhiệm vụ mới. Nhiệm vụ có tên 'Tín hiệu cơ học'. |
| 12 Septober 5500 08:15 | 27.2 | THƯ | PositiveEvent | Động cơ trọng lực | Con tàu cơ khí đã hạ cánh gần đó. Nó chứa một động cơ trọng lực đang hoạt động. Động cơ chống lại trọng lực và tạo ra một trường lực nâng xung quanh nó, cho phép nó nâng các con tàu hoặc bệ lớn. Mặc dù nó không hoạt động khi ở xa một hành… |
| 14 Septober 5500 06:00 | 25.3 | THƯ | NewQuest | Nhiệm vụ khả dụng: Chạy trốn phu nhân | Có nhiệm vụ mới. Nhiệm vụ có tên 'Chạy trốn phu nhân'. Nếu bạn không chấp nhận nhiệm vụ trong 2 ngày, nó sẽ hết thời hạn. |
| 14 Septober 5500 16:00 | 24.9 | THƯ | PositiveEvent | Thrumbos quý hiếm | Một đàn nhỏ của thrumbos đã lang thang vào khu vực. Hòa bình tự nhiên, những sinh vật quý hiếm này cực kỳ nguy hiểm khi đối đầu. Một số thương nhân sẵn sàng trả nhiều tiền cho da và sừng quý giá của họ. Thrumbos sẽ rời khỏi khu vực trong m… |
| 14 Septober 5500 16:54 | 24.8 | THƯ | PositiveEvent | Monolith bị sụp đổ | Bac si đã phát hiện một monolith cổ đại bị chôn vùi một phần gần đây. Nếu điều tra nó, bạn có thể tìm hiểu thêm. |
| 15 Septober 5500 04:00 | 24.4 | THƯ | PositiveEvent | Chuột đực tự thuần hóa | Một chuột đực đã trở nên thuần hóa. Nó hiện được chỉ định Chuột đực 1. |
| 2 Decembary 5500 12:24 | 22.0 | THƯ | NeutralEvent | Khách tham quan | Một Diễn viên từ Orussia đang tiến vào thuộc địa. Anh ta được đặt tên Masaru Maldonado. Anh ta dường như có một vài mặt hàng để giao dịch. |
| 3 Decembary 5500 04:24 | 21.4 | THƯ | ThreatBig | Đột kích: Khí độc đàn ông | Một nhóm wasters từ Khí độc đàn ông đã đến gần đó. Họ đang tấn công ngay lập tức. |
| 3 Decembary 5500 17:36 | 20.8 | THƯ | ThreatSmall | Chuột cái bị điên | Một chuột cái gần đó đã phát điên. Nó sẽ tấn công tất cả mọi người mà nó nhìn thấy. |
| 4 Decembary 5500 14:50 | 19.9 | THƯ | NeutralEvent | Ám ảnh kinh hoàng | Protein mộng thấy một cơn ác mộng kỳ lạ. Trong mơ, anh ta nhìn thấy một hình khối đen trải dài trong không gian và thời gian, phát triển và tiêu thụ. Hình khối bắt nguồn từ một monolith sụp đổ gần đó. Sau khi tỉnh giấc, Protein bị cuốn hút… |
| 4 Decembary 5500 14:58 | 19.9 | THƯ | ThreatBig | Phế tích nguy hiểm | Khi eistein tiến gần đến bức tường cổ đại, anh ấy bỗng cảm thấy nỗi sợ hãi chạy dọc khắp cơ thể mình. Anh ta không biết tại sao nhưng anh ta cảm thấy công trình cổ đại kia có thể ẩn chứa nhiều nguy hiểm trong đó. |
| 5 Decembary 5500 02:00 | 19.4 | THƯ | ThreatBig | Raid: Khí độc đàn ông | A group of wasters have arrived from nearby. They are attacking immediately. |
| 7 Decembary 5500 07:00 | 17.2 | THƯ | ThreatBig | Warg hunting eistein | A warg is hunting eistein for food! |
| 7 Decembary 5500 08:13 | 17.2 | THƯ | ThreatBig | Warg hunting bac si | A warg is hunting bac si for food! |
| 7 Decembary 5500 08:47 | 17.2 | THƯ | ThreatSmall | Warg revenge | A warg is attacking after being harmed! It will hunt any humanoid it can reach. It will calm down when it goes to sleep. |
| 9 Decembary 5500 20:48 | 14.7 | THƯ | PositiveEvent | Cargo pods | You have detected a cluster of cargo pods crashing nearby. Perhaps you'll find something useful in the wreckage. |
| 10 Decembary 5500 06:46 | 14.3 | THƯ | ThreatBig | Timber wolf hunting eistein | A timber wolf is hunting eistein for food! |
| 10 Decembary 5500 07:00 | 14.2 | THƯ | ThreatSmall | Timber wolf revenge | A timber wolf is attacking after being harmed! It will hunt any humanoid it can reach. It will calm down when it goes to sleep. |
| 11 Decembary 5500 00:15 | 13.5 | THƯ | NegativeEvent | Food binge: Eistein | Eistein is pigging out on food. This happened because of: Smokeleaf dependence (withdrawal 81%). |
| 11 Decembary 5500 06:00 | 13.3 | THƯ | NewQuest | Quest active: Ship to the Stars | A new quest is available. The quest is called 'Ship to the Stars'. |
| 11 Decembary 5500 06:24 | 13.3 | THƯ | NewQuest | Quest available: The Hard Prisoner | A new quest is available. The quest is called 'The Hard Prisoner'. If you don't accept the quest within 6 days, it will expire. |
| 12 Decembary 5500 00:00 | 12.5 | THƯ | NeutralEvent | Visitors | A group from Camro dân tộc are visiting the colony. They seem to have a few items to trade. |
| 12 Decembary 5500 16:00 | 11.9 | THƯ | NeutralEvent | Transport pod crash | A policewoman named Arianites is crashing in a transport pod nearby. If she survives the impact, she will be badly wounded. Arianites is from Đế chế tan nát. If she returns home safely, she will spread goodwill between your factions. You c… |
| 12 Decembary 5500 19:40 | 11.7 | THƯ | NegativeEvent | Disease: Lung rot | Eistein has gotten sick from lung rot due to long-term exposure to rot stink gas (which is given off by rotting corpses). Ensure you have a medical bed and a doctor. Make sure that eistein gets proper treatment. |
| 13 Decembary 5500 07:25 | 11.2 | THƯ | NegativeEvent | Food binge: Eistein | Eistein is pigging out on food. This happened because of: Smokeleaf dependence (withdrawal 89%). |
| 13 Decembary 5500 14:48 | 10.9 | THƯ | ThreatBig | Raid: Khí độc đàn ông | A group of wasters have arrived from nearby. They are attacking immediately. |
| 13 Decembary 5500 16:03 | 10.9 | THƯ | Death | Death: Rat 1 | Rat 1 has been cut to death. |
| 14 Decembary 5500 06:24 | 10.3 | THƯ | NewQuest | Quest available: Shoytt's Sad Survivors | A new quest is available. The quest is called 'Shoytt's Sad Survivors'. If you don't accept the quest within 6 days, it will expire. |
| 14 Decembary 5500 06:24 | 10.3 | THƯ | NegativeEvent | Solar flare | A solar flare has begun. The intense radiation will shut down all electrical devices. It should pass in about a day. |
| 14 Decembary 5500 20:26 | 9.7 | THƯ | ThreatSmall | Go-juice binge: Eistein | Eistein, Barkeep is binging on go-juice. This happened because of poor mood. The final straw was: Smokeleaf withdrawal |
| 15 Decembary 5500 12:24 | 9.0 | THƯ | ThreatBig | Manhunter pack | A pack of man-hunting raccoons have entered the area! Driven insane by the disease known as scaria, they will roam the region, hunting for humanoid flesh. They won't attack doors unless they see someone go through the door. Hide inside and… |
| 15 Decembary 5500 14:49 | 8.9 | THƯ | NegativeEvent | Food binge: Protein | Protein is pigging out on food. This happened because of poor mood. The final straw was: Observed rotting corpse |
| 15 Decembary 5500 16:23 | 8.8 | THƯ | NeutralEvent | Wild man wanders in | A person living among wild animals has wandered into the area. He's called Barark. You can attempt to tame him. |
| 1 Aprimay 5501 19:11 | 7.7 | THƯ | PositiveEvent | War merchant from Camro dân tộc | A caravan from Camro dân tộc is approaching. They are a war merchant. They will hang around the colony for some time before leaving. You can attack them - but this will anger their faction! |
| 2 Aprimay 5501 06:00 | 7.3 | THƯ | NewQuest | Quest available: The Deserter | A new quest is available. The quest is called 'The Deserter'. If you don't accept the quest within 7 days, it will expire. |
| 2 Aprimay 5501 11:50 | 7.0 | THƯ | PositiveEvent | Gift from Camro dân tộc | Tribespeople from Camro dân tộc have left a gift: -Silver x62 |
| 2 Aprimay 5501 13:22 | 7.0 | THƯ | PositiveEvent | Ancient mech | Passing near the remains of an ancient exostrider mechanoid, eistein noticed an intact transponder inside. If you could get the transponder, you could read valuable information from it. The massive mech is smashed and fused into a solid pi… |
| 4 Aprimay 5501 08:48 | 5.2 | THƯ | NeutralEvent | Transport pod crash | A bartender named Rasher is crashing in a transport pod nearby. If he survives the impact, he will be badly wounded. Rasher is from your enemy Moigleoo. You can capture him for recruitment or slavery purposes. |
| 4 Aprimay 5501 10:48 | 5.1 | THƯ | NewQuest | Quest available: Pollution Dump | A new quest is available. The quest is called 'Pollution Dump'. If you don't accept the quest within 6 days, it will expire. |
| 5 Aprimay 5501 09:38 | 4.1 | THƯ | NegativeEvent | Roof collapse | A roof has collapsed because it was too far from any support. These things were crushed: -Wood |
| 5 Aprimay 5501 09:40 | 4.1 | THƯ | NegativeEvent | Roof collapse | A roof has collapsed because it was too far from any support. These things were crushed: -Wood |
| 5 Aprimay 5501 09:42 | 4.1 | THƯ | NegativeEvent | Roof collapse | A roof has collapsed because it was too far from any support. These things were crushed: -Wood |
| 5 Aprimay 5501 09:44 | 4.1 | THƯ | NegativeEvent | Roof collapse | A roof has collapsed because it was too far from any support. These things were crushed: -Wood |
| 5 Aprimay 5501 09:47 | 4.1 | THƯ | NegativeEvent | Roof collapse | A roof has collapsed because it was too far from any support. These things were crushed: -Wood |
| 5 Aprimay 5501 09:49 | 4.1 | THƯ | NegativeEvent | Roof collapse | A roof has collapsed because it was too far from any support. These things were crushed: -Wood |
| 5 Aprimay 5501 09:51 | 4.1 | THƯ | NegativeEvent | Roof collapse | A roof has collapsed because it was too far from any support. These things were crushed: -Wood |
| 5 Aprimay 5501 09:53 | 4.1 | THƯ | NegativeEvent | Roof collapse | A roof has collapsed because it was too far from any support. These things were crushed: -Wood |
| 5 Aprimay 5501 09:56 | 4.1 | thông báo | SilentInput |  | A roof has collapsed because it was too far from any support. |
| 5 Aprimay 5501 22:23 | 3.6 | thông báo | NeutralEvent |  | Chunks of a spacecraft have impacted nearby. You can deconstruct them to yield resources. |
| 6 Aprimay 5501 02:00 | 3.5 | thông báo | NeutralEvent |  | Chunks of a spacecraft have impacted nearby. You can deconstruct them to yield resources. |
| 6 Aprimay 5501 20:23 | 2.7 | THƯ | NeutralEvent | Leathery stranger | A ragged stranger with leathery skin is approaching your colony. He wants to talk. You can send a colonist to hear what he has to say. |
| 7 Aprimay 5501 08:53 | 2.2 | THƯ | AcceptCreepJoiner | Tangle wants to join | The leathery stranger stares into space and speaks in a monotone, as though he hardly sees anyone or anything. He refuses to leave, insisting he is only interested in your colony. He says that he can help. As the former subject of a cultis… |
| 7 Aprimay 5501 20:23 | 1.7 | thông báo | NegativeEvent |  | Tangle has become hostile! |
| 7 Aprimay 5501 20:23 | 1.7 | THƯ | ThreatBig | Tangle hostile | Upon being rejected, Tangle flew into a murderous rage and began to attack! |
| 7 Aprimay 5501 22:31 | 1.6 | thông báo | NeutralEvent |  | Tangle is using death refusal to self-resurrect. |
| 7 Aprimay 5501 23:43 | 1.5 | thông báo | NeutralEvent |  | Tangle is using death refusal to self-resurrect. |
| 8 Aprimay 5501 00:12 | 1.5 | thông báo | NeutralEvent |  | Tangle is using death refusal to self-resurrect. |
| 8 Aprimay 5501 00:36 | 1.5 | thông báo | NeutralEvent |  | Tangle is using death refusal to self-resurrect. |
| 8 Aprimay 5501 02:31 | 1.4 | THƯ | NegativeEvent | Sad wander: Protein | Protein has broken down and is wandering around in sadness. This happened because of poor mood. The final straw was: Intense pain |
| 8 Aprimay 5501 04:22 | 1.4 | thông báo | SituationResolved |  | Protein is no longer wandering in sadness. |
| 8 Aprimay 5501 08:00 | 1.2 | thông báo | NeutralEvent |  | A bookworm from Camro dân tộc is passing by. He is named Red Deer. |
| 8 Aprimay 5501 10:32 | 1.1 | thông báo | NegativeEvent |  | Pork x7 has rotted away in storage. |
| 8 Aprimay 5501 10:47 | 1.1 | thông báo | PositiveEvent |  | Eistein, Barkeep is fully healed. |
| 8 Aprimay 5501 10:48 | 1.1 | THƯ (chưa đóng) | NewQuest | Quest available: The Revered Artifact | A new quest is available. The quest is called 'The Revered Artifact'. |
| 8 Aprimay 5501 11:20 | 1.1 | thông báo | PositiveEvent |  | Bac si, Bac si is fully healed. |
| 8 Aprimay 5501 18:48 | 0.8 | THƯ | ThreatSmall | Mad alpaca | A local alpaca has gone mad. It will attack everyone it sees. |
| 9 Aprimay 5501 04:47 | 0.3 | thông báo | PositiveEvent |  | Eistein, Barkeep is fully healed. |
| 9 Aprimay 5501 10:00 | 0.1 | THƯ (chưa đóng) | NewQuest | Quest available: Temporary Workers | A new quest is available. The quest is called 'Temporary Workers'. If you don't accept the quest within 8 days, it will expire. |
| 9 Aprimay 5501 11:10 | 0.1 | thông báo | NegativeEvent |  | Alpaca meat x71 has rotted away in storage. |
| 9 Aprimay 5501 11:35 | 0.1 | THƯ (chưa đóng) | PositiveEvent | Slaver from Camro dân tộc | A caravan from Camro dân tộc is approaching. They are a slaver. They will hang around the colony for some time before leaving. You can attack them - but this will anger their faction! |
| 9 Aprimay 5501 12:03 | 0.0 | thông báo | PositiveEvent |  | Bac si, Bac si is fully healed. |
| 9 Aprimay 5501 12:48 | 0.0 | THƯ | ThreatBig | Raid: Khí độc đàn ông | A group of wasters from Khí độc đàn ông have arrived nearby. They will prepare for a while, then attack. Prepare a defense or attack them pre-emptively. |

Thông báo cũ hơn 5 ngày (gộp theo nội dung): «Critical alert: Major break risk» ×11; «Cảnh báo khẩn: Nguy cơ suy sụp nghiêm trọng» ×5; «Eistein failed while constructing a wooden dining chair. So…» ×4; «Eistein, Barkeep is fully healed.» ×3; «Bac si, Bac si is fully healed.» ×3; «Protein thất bại trong lúc xây dựng bếp củi. Một ít tài ngu…» ×2; «Khách tham quan từ Orussia đang rời đi.» ×2; «Eistein is no longer pigging out on food.» ×2; «Critical alert: Extreme break risk» ×2; «Critical alert: Medical emergency» ×2; «Sổ tay thẩm mỹ (tệ hại N%) đã hao mòn hết trong kho chứa.» ×1; «Eistein, Nhân viên pha chế đã bình phục hoàn toàn.» ×1.


### Sự kiện đáng nhớ game ghi lại (tale)

Tổng: `Wounded`×202, `PlayedGame`×38, `Downed`×10, `Meditated`×8, `MajorThreat`×6, `KilledMelee`×6, `Prayed`×6, `KilledCapacity`×6, `Raid`×5, `ReadBook`×4, `Hunted`×4, `LandedInPod`×3, `HeatstrokeRevealed`×3, `KilledBy`×2, `TileSettled`×1, `Stripped`×1, `TrainedAnimal`×1, `ManhunterPack`×1, `TradedWith`×1, `KilledLongRange`×1.

| Lúc | Cách đây (ngày) | Loại | Diễn biến |
|---|---|---|---|
| 6 Septober 5500 06:00 | 33.3 | `TileSettled` | Khu định cư mới |
| 6 Septober 5500 06:06 | 33.3 | `LandedInPod` | Protein đáp xuống bằng pod |
| 6 Septober 5500 06:06 | 33.3 | `LandedInPod` | eistein đáp xuống bằng pod |
| 6 Septober 5500 06:06 | 33.3 | `LandedInPod` | bac si đáp xuống bằng pod |
| 11 Septober 5500 15:35 | 27.9 | `Raid` | Đột kích bắt đầu (người chứng kiến: bac si) |
| 11 Septober 5500 16:22 | 27.9 | `KilledBy` | Beelzebub bị Gray giết |
| 11 Septober 5500 16:22 | 27.9 | `KilledMelee` | Gray giết Beelzebub (bằng MeleeWeapon_Knife) |
| 11 Septober 5500 16:50 | 27.8 | `Downed` | Gray bị hạ gục bởi Protein (bằng Gun_Revolver) |
| 13 Septober 5500 01:56 | 26.5 | `HeatstrokeRevealed` | bac si phát bệnh Heatstroke |
| 13 Septober 5500 23:40 | 25.5 | `HeatstrokeRevealed` | bac si phát bệnh Heatstroke |
| 3 Decembary 5500 04:24 | 21.4 | `Raid` | Đột kích bắt đầu (người chứng kiến: bac si) |
| 3 Decembary 5500 16:03 | 20.9 | `Stripped` | eistein lột đồ Buxdun |
| 4 Decembary 5500 16:27 | 19.8 | `HeatstrokeRevealed` | eistein phát bệnh Heatstroke |
| 5 Decembary 5500 02:00 | 19.4 | `Raid` | Đột kích bắt đầu (người chứng kiến: eistein) |
| 5 Decembary 5500 05:48 | 19.3 | `Downed` | Squirrel bị hạ gục bởi Protein (bằng Gun_Revolver) |
| 6 Decembary 5500 03:20 | 18.4 | `KilledCapacity` | bac si giết Squirrel (nạn nhân mất chức năng BloodPumping) |
| 6 Decembary 5500 12:38 | 18.0 | `KilledCapacity` | Protein giết Rat (nạn nhân mất chức năng Consciousness) |
| 6 Decembary 5500 12:39 | 18.0 | `Hunted` | Protein săn được Rat |
| 7 Decembary 5500 09:34 | 17.1 | `Downed` | Warg bị hạ gục bởi eistein (bằng MeleeWeapon_Knife) |
| 7 Decembary 5500 17:10 | 16.8 | `Hunted` | Protein săn được Tortoise |
| 8 Decembary 5500 08:43 | 16.2 | `KilledCapacity` | Protein giết Hare (nạn nhân mất chức năng BloodFiltration) |
| 9 Decembary 5500 03:42 | 15.4 | `Hunted` | Protein săn được Horse |
| 9 Decembary 5500 10:52 | 15.1 | `TrainedAnimal` | Protein huấn luyện Rat 1 (Tameness) |
| 13 Decembary 5500 14:48 | 10.9 | `Raid` | Đột kích bắt đầu (người chứng kiến: eistein) |
| 13 Decembary 5500 16:03 | 10.9 | `KilledBy` | Rat 1 bị Elphy giết |
| 13 Decembary 5500 16:03 | 10.9 | `KilledMelee` | Elphy giết Rat 1 (bằng MeleeWeapon_Knife) |
| 13 Decembary 5500 16:03 | 10.9 | `KilledCapacity` | Elphy giết Rat 1 (nạn nhân mất chức năng BloodPumping) |
| 14 Decembary 5500 01:52 | 10.5 | `Downed` | Protein bị hạ gục (không do ai gây trực tiếp — kiệt sức/mất máu/đau) |
| 15 Decembary 5500 12:24 | 9.0 | `ManhunterPack` | Bầy thú điên (manhunter) kéo vào map (người chứng kiến: bac si) |
| 15 Decembary 5500 13:45 | 9.0 | `Downed` | Raccoon bị hạ gục bởi eistein (bằng MeleeWeapon_Knife) |
| 15 Decembary 5500 13:45 | 9.0 | `KilledMelee` | eistein giết Raccoon (bằng MeleeWeapon_Knife) |
| 2 Aprimay 5501 06:46 | 7.3 | `TradedWith` | Protein giao dịch với Colmea |
| 7 Aprimay 5501 21:04 | 1.7 | `Downed` | Tangle bị hạ gục bởi eistein (bằng MeleeWeapon_Knife) |
| 7 Aprimay 5501 23:09 | 1.6 | `Downed` | Tangle bị hạ gục bởi Protein (bằng Human) |
| 8 Aprimay 5501 00:00 | 1.5 | `Downed` | Tangle bị hạ gục bởi Protein (bằng Human) |
| 8 Aprimay 5501 00:09 | 1.5 | `KilledMelee` | eistein giết Tangle (bằng MeleeWeapon_Knife) |
| 8 Aprimay 5501 00:09 | 1.5 | `KilledCapacity` | eistein giết Tangle (nạn nhân mất chức năng Consciousness) |
| 8 Aprimay 5501 00:24 | 1.5 | `Downed` | Tangle bị hạ gục bởi bac si (bằng Gun_BoltActionRifle) |
| 8 Aprimay 5501 00:31 | 1.5 | `KilledMelee` | eistein giết Tangle (bằng MeleeWeapon_Knife) |
| 8 Aprimay 5501 00:47 | 1.5 | `Downed` | Tangle bị hạ gục bởi bac si (bằng Gun_BoltActionRifle) |
| 8 Aprimay 5501 20:31 | 0.7 | `KilledMelee` | eistein giết Alpaca (bằng MeleeWeapon_Knife) |
| 9 Aprimay 5501 05:33 | 0.3 | `KilledCapacity` | bac si giết WildBoar (nạn nhân mất chức năng BloodPumping) |
| 9 Aprimay 5501 12:26 | 0.0 | `Hunted` | bac si săn được Boomrat |
| 9 Aprimay 5501 12:48 | 0.0 | `Raid` | Đột kích bắt đầu (người chứng kiến: bac si) |


### Nhật ký chiến đấu (`battleLog`: 36 trận, 1,674 dòng gốc)

Game ghi lại từng phát bắn, từng đòn đánh (kể cả đi săn và thú hoang săn nhau) rồi gom thành «trận». Ở đây đã gộp theo cặp: «bắn 12 trúng 3» = bắn ra 12 phát, 3 phát trúng đúng mục tiêu; «cận chiến 5 trúng 2» = ra 5 đòn, trúng 2 (cận chiến kèm tên súng = dùng báng/nòng súng để đánh). «vướng vật cản» = viên đạn trượt mục tiêu và găm vào cây/tường/đá. Tên dạng `Loài#1`, `Loài#2` là mã cố định xuyên suốt toàn bộ bảng để theo dõi đúng cùng một con vật qua nhiều dòng. Các dòng xếp theo giờ bắt đầu của từng «trận»; với trận kéo dài nhiều giờ, giờ cụ thể của từng kết cục gục/chết được ghi ngay trong ngoặc. Dòng chỉ có kết cục (không có đòn đánh) là con vật/người gục hoặc chết sau trận vì mất máu, bệnh…

**Thành tích của phía thuộc địa trên toàn bộ log** (tính cả đi săn):
- **Protein**: bắn `Gun_Revolver` 312 phát, trúng mục tiêu 51 (16%), 58 phát vướng vật cản; cận chiến 47 đòn, trúng 29 (62%); bị đánh trúng 10 lần; bị gục 1 lần; đã giết (gồm 1 chết sau đó do mất máu): Ibex×3, Horse×3, Rat×2, Squirrel×2, Hare×2, Gray, Buxdun, Diana, Tortoise, CreepJoiner.
- **bac si**: bắn `Gun_BoltActionRifle` 367 phát, trúng mục tiêu 34 (9%), 138 phát vướng vật cản; cận chiến 31 đòn, trúng 16 (52%); bị đánh trúng 9 lần; đã giết (gồm 2 chết sau đó do mất máu): Horse×2, CreepJoiner×2, Squirrel, Ibex, Warg, Donkey, Elphy, Raccoon, WildBoar.
- **eistein**: cận chiến 45 đòn, trúng 33 (73%); bị đánh trúng 12 lần; đã giết: CreepJoiner×2, Mink, Raccoon, Alpaca.
- **Beelzebub** (thú của thuộc địa): bị đánh trúng 1 lần.
- **Rat 1** (thú của thuộc địa): cận chiến 3 đòn, trúng 1 (33%); bị đánh trúng 4 lần.
- Đạn trượt mục tiêu nhưng găm vào vật cản (198 viên): `Plant_TreeOak` ×118, `Wall` ×23, `ChunkMarble` ×17, `ChunkGranite` ×11, `Marble` ×7, `Plant_TreePoplar` ×7, `Granite` ×5, `Door` ×2, `AncientConcreteBarrier` ×1, `Sarcophagus` ×1, `AncientGenerator` ×1, `SmashedStump` ×1, `AncientPodCar` ×1, `Plant_Berry` ×1, `AncientRustedCarFrame` ×1, … và 1 loại khác.

| Lúc | Cách đây (ngày) | Các bên | Diễn biến → kết cục |
|---|---|---|---|
| 7 Septober 5500 09:12–10:09 | 32.1 | Tortoise#1, Warg (thú hoang) | Warg → Tortoise#1: cận chiến 24 trúng 8 [2 lần là hất đất vào mắt, 2 bị giáp chặn, huỷ 3 bộ phận]; Tortoise#1 → Warg: cận chiến 12 trúng 1; **Tortoise#1 CHẾT** (lúc 10:09, do Warg, `Crack`) |
| 9 Septober 5500 15:57–16:09 | 29.9 | eistein ↔ Mink (thú hoang) | eistein → Mink: cận chiến 5 trúng 2 (tay không) [huỷ 1 bộ phận]; Mink → eistein: cận chiến 4 trúng 2; **Mink CHẾT** (do eistein, `Bruise`) |
| 11 Septober 5500 16:18–16:59 | 27.9 | Protein, eistein, bac si, Beelzebub ↔ Gray (Khí độc đàn ông (PirateWaster)) | Gray → Beelzebub: cận chiến 3 trúng 1 (`MeleeWeapon_Knife`) [huỷ 2 bộ phận]; Gray → vật `Wall`: cận chiến 2 trúng 2 (`MeleeWeapon_Knife`); Protein → Gray: bắn 4 trúng 2 (`Gun_Revolver`) [huỷ 1 bộ phận]; bac si → Gray: cận chiến 2 trúng 0 (`Gun_BoltActionRifle`, tay không); Gray → bac si: cận chiến 1 trúng 0 (`MeleeWeapon_Knife`); eistein → Gray: cận chiến 4 trúng 4 (`MeleeWeapon_Knife`); Gray → eistein: cận chiến 2 trúng 1 (`MeleeWeapon_Knife`) [1 bị giáp chặn]; **Beelzebub CHẾT** (lúc 16:22, do Gray, `Cut`); **Gray gục** (lúc 16:50, do Protein, `Gunshot`); **Gray CHẾT** (lúc 16:59, do Protein, `Gunshot`) |
| 2 Decembary 5500 20:49 | 21.7 | Sparrow (thú hoang) | không rõ → Sparrow: nổ/lửa ×1 (`Flame`) [huỷ 2 bộ phận]; **Sparrow CHẾT** (`MissingBodyPart`) |
| 3 Decembary 5500 05:14–05:39 | 21.3 | Protein, bac si, eistein ↔ Buxdun (Khí độc đàn ông (PirateWaster)) | Protein → Buxdun: bắn 10 trúng 4 (`Gun_Revolver`) [3 phát vướng vật cản]; bac si → Buxdun: bắn 7 trúng 0 (`Gun_BoltActionRifle`) [2 phát vướng vật cản]; Buxdun → eistein: cận chiến 3 trúng 0 (`MeleeWeapon_Knife`); **Buxdun CHẾT** (lúc 05:39, do Protein) |
| 3 Decembary 5500 18:29–18:35 | 20.8 | Protein ↔ Rat#1 (thú hoang) | Protein → Rat#1: cận chiến 3 trúng 2 (`Gun_Revolver`) [huỷ 2 bộ phận]; Rat#1 → Protein: cận chiến 3 trúng 1; **Rat#1 CHẾT** (do Protein) |
| 5 Decembary 5500 03:08–09:36 | 19.4 | Protein, bac si, eistein ↔ Diana (Khí độc đàn ông (PirateWaster)) ↔ Ibex#1, Squirrel#1, Squirrel#2 (thú hoang) | Protein → Diana: bắn 9 trúng 4 (`Gun_Revolver`); Diana → eistein: cận chiến 2 trúng 1 (`MeleeWeapon_Club`); bac si → Diana: cận chiến 4 trúng 1 (`Gun_BoltActionRifle`); Diana → bac si: cận chiến 3 trúng 1 (`MeleeWeapon_Club`, tay không); Protein → Squirrel#1: bắn 17 trúng 1 (`Gun_Revolver`) [huỷ 2 bộ phận] + cận chiến 4 trúng 3 (`Gun_Revolver`) [1 lần là hất đất vào mắt, huỷ 1 bộ phận]; bac si → Squirrel#2: bắn 18 trúng 0 (`Gun_BoltActionRifle`) [9 phát vướng vật cản]; Squirrel#1 → Protein: cận chiến 3 trúng 0; Protein → Ibex#1: bắn 30 trúng 3 (`Gun_Revolver`) [10 phát vướng vật cản, huỷ 1 bộ phận]; **Diana CHẾT** (lúc 03:30, do Protein); **Squirrel#1 gục** (lúc 05:48, do Protein, `MissingBodyPart`); **Squirrel#1 CHẾT** (lúc 06:35, do Protein) |
| 5 Decembary 5500 07:40–14:24 | 19.2 | bac si ↔ Rat#2, Squirrel#2, Hare#1 (thú hoang) | bac si → Hare#1: bắn 16 trúng 0 (`Gun_BoltActionRifle`) [4 phát vướng vật cản]; bac si → Squirrel#2: bắn 16 trúng 0 (`Gun_BoltActionRifle`) [8 phát vướng vật cản]; bac si → Rat#2: bắn 18 trúng 0 (`Gun_BoltActionRifle`) [5 phát vướng vật cản] |
| 5 Decembary 5500 14:19–18:20 | 18.9 | Protein ↔ Ibex#2, Ibex#1 (thú hoang) | Protein → Ibex#2: bắn 15 trúng 3 (`Gun_Revolver`) [2 phát vướng vật cản, huỷ 1 bộ phận]; **Ibex#1 gục** (lúc 14:19, từ vết thương do Protein gây trước đó, `BloodLoss`); **Ibex#1 CHẾT** (lúc 16:03, do Protein); **Ibex#2 CHẾT** (lúc 18:20, do Protein, `Gunshot`) |
| 6 Decembary 5500 03:13–07:45 | 18.4 | bac si ↔ Ibex#3, Squirrel#3 (thú hoang) | bac si → Squirrel#3: bắn 3 trúng 1 (`Gun_BoltActionRifle`) [1 phát vướng vật cản, huỷ 2 bộ phận]; bac si → Ibex#3: bắn 17 trúng 0 (`Gun_BoltActionRifle`) [3 phát vướng vật cản]; **Squirrel#3 CHẾT** (lúc 03:20, do bac si, `MissingBodyPart`) |
| 6 Decembary 5500 07:34–15:32 | 18.2 | Protein ↔ Donkey, Rat#2, Squirrel#2, Ibex#4 (thú hoang) | Protein → Ibex#4: bắn 19 trúng 2 (`Gun_Revolver`) [4 phát vướng vật cản]; Protein → Squirrel#2: bắn 7 trúng 1 (`Gun_Revolver`) [3 phát vướng vật cản, huỷ 2 bộ phận]; Protein → Rat#2: bắn 23 trúng 1 (`Gun_Revolver`) [6 phát vướng vật cản, huỷ 2 bộ phận]; Protein → Donkey: bắn 11 trúng 3 (`Gun_Revolver`) [2 phát vướng vật cản]; **Squirrel#2 CHẾT** (lúc 09:36, do Protein, `Gunshot`); **Rat#2 CHẾT** (lúc 12:38, do Protein, `MissingBodyPart`) |
| 6 Decembary 5500 09:49–15:40 | 18.1 | bac si ↔ Ibex#3 (thú hoang) | bac si → Ibex#3: bắn 53 trúng 2 (`Gun_BoltActionRifle`) [26 phát vướng vật cản, huỷ 1 bộ phận]; **Ibex#3 gục** (lúc 15:40, từ vết thương do bac si gây trước đó, `BloodLoss`) |
| 6 Decembary 5500 12:14 | 18.0 | Ibex#4 (thú hoang) | **Ibex#4 gục** (từ vết thương do Protein gây trước đó, `BloodLoss`) |
| 6 Decembary 5500 14:41 | 17.9 | Ibex#4 (thú hoang) | **Ibex#4 CHẾT** (từ vết thương do Protein gây trước đó, `BloodLoss`) |
| 6 Decembary 5500 19:28–19:56 | 17.7 | Protein ↔ Hare#2 (thú hoang) | Protein → Hare#2: bắn 7 trúng 2 (`Gun_Revolver`) [huỷ 2 bộ phận]; **Hare#2 CHẾT** (lúc 19:56, do Protein) |
| 6 Decembary 5500 19:42 | 17.7 | Ibex#3 (thú hoang) | **Ibex#3 CHẾT** (từ vết thương do bac si gây trước đó, `BloodLoss`) |
| 6 Decembary 5500 19:48–23:27 | 17.7 | bac si ↔ Horse#1 (thú hoang) | bac si → Horse#1: bắn 20 trúng 3 (`Gun_BoltActionRifle`) [10 phát vướng vật cản]; **Horse#1 gục** (lúc 23:27, từ vết thương do bac si gây trước đó, `BloodLoss`) |
| 7 Decembary 5500 03:09 | 17.4 | Horse#1 (thú hoang) | **Horse#1 CHẾT** (từ vết thương do bac si gây trước đó, `BloodLoss`) |
| 7 Decembary 5500 08:46–19:32 | 17.2 | Protein, bac si, eistein ↔ Horse#2, Tortoise#2, Warg (thú hoang) | Protein → Warg: bắn 7 trúng 3 (`Gun_Revolver`) [3 phát vướng vật cản] + cận chiến 1 trúng 1 (`Gun_Revolver`); Warg → vật `Door`: cận chiến 5 trúng 5; bac si → Warg: bắn 3 trúng 2 (`Gun_BoltActionRifle`) [1 phát vướng vật cản, huỷ 1 bộ phận]; eistein → Warg: cận chiến 5 trúng 5 (`MeleeWeapon_Knife`); Warg → bac si: cận chiến 1 trúng 1; Protein → Tortoise#2: bắn 101 trúng 6 (`Gun_Revolver`) [15 phát vướng vật cản, 2 bị giáp chặn, huỷ 1 bộ phận]; Protein → Horse#2: bắn 17 trúng 8 (`Gun_Revolver`) [1 phát vướng vật cản]; **Warg gục** (lúc 09:34, do eistein, `Cut`); **Warg CHẾT** (lúc 09:50, do bac si, `Gunshot`); **Tortoise#2 CHẾT** (lúc 17:09, do Protein); **Horse#2 CHẾT** (lúc 19:32, do Protein) |
| 7 Decembary 5500 09:25 | 17.1 | Donkey (thú hoang) | **Donkey gục** (từ vết thương do Protein gây trước đó, `BloodLoss`) |
| 7 Decembary 5500 12:16 | 17.0 | bac si ↔ Donkey (thú hoang) | **Donkey CHẾT** (do bac si) |
| 7 Decembary 5500 15:30–16:57 | 16.9 | bac si ↔ Horse#3 (thú hoang) | bac si → Horse#3: bắn 12 trúng 1 (`Gun_BoltActionRifle`) [5 phát vướng vật cản]; **Horse#3 gục** (lúc 16:36, từ vết thương do bac si gây trước đó, `HeartAttack`); **Horse#3 CHẾT** (lúc 16:57, do bac si) |
| 8 Decembary 5500 05:55–07:00 | 16.3 | bac si ↔ Horse#4 (thú hoang) | bac si → Horse#4: bắn 10 trúng 1 (`Gun_BoltActionRifle`) [1 phát vướng vật cản] |
| 8 Decembary 5500 08:39–12:38 | 16.2 | Protein ↔ Horse#4, Hare#1 (thú hoang) | Protein → Hare#1: bắn 2 trúng 1 (`Gun_Revolver`) [1 phát vướng vật cản, huỷ 1 bộ phận]; Protein → Horse#4: bắn 20 trúng 5 (`Gun_Revolver`) [4 phát vướng vật cản]; **Hare#1 CHẾT** (lúc 08:43, do Protein, `MissingBodyPart`); **Horse#4 gục** (lúc 12:23, từ vết thương do Protein gây trước đó, `BloodLoss`); **Horse#4 CHẾT** (lúc 12:38, do Protein) |
| 8 Decembary 5500 13:25–20:23 | 16.0 | bac si ↔ Horse#5 (thú hoang) | bac si → Horse#5: bắn 67 trúng 2 (`Gun_BoltActionRifle`) [24 phát vướng vật cản] |
| 8 Decembary 5500 23:25–9 Decembary 5500 03:42 | 15.6 | Protein ↔ Horse#5 (thú hoang) | Protein → Horse#5: bắn 12 trúng 2 (`Gun_Revolver`) [3 phát vướng vật cản]; **Horse#5 gục** (lúc 9 Decembary 5500 01:55, từ vết thương do Protein gây trước đó, `BloodLoss`); **Horse#5 CHẾT** (lúc 9 Decembary 5500 03:42, do Protein) |
| 13 Decembary 5500 15:35–16:46 | 10.9 | bac si, Protein, eistein, Rat 1 ↔ Elphy (Khí độc đàn ông (PirateWaster)) | bac si → Elphy: bắn 12 trúng 3 (`Gun_BoltActionRifle`) [4 phát vướng vật cản] + cận chiến 5 trúng 2 (`Gun_BoltActionRifle`); Protein → Elphy: bắn 1 trúng 0 (`Gun_Revolver`) [1 phát vướng vật cản] + cận chiến 12 trúng 4 (`Gun_Revolver`, tay không); Elphy → Rat 1: cận chiến 5 trúng 4 (`MeleeWeapon_Knife`) [1 lần là hất đất vào mắt, huỷ 4 bộ phận]; Rat 1 → Elphy: cận chiến 3 trúng 1 [1 lần là hất đất vào mắt]; Elphy → bac si: cận chiến 5 trúng 4 (`MeleeWeapon_Knife`, tay không); Elphy → Protein: cận chiến 8 trúng 5 (`MeleeWeapon_Knife`) [1 lần là hất đất vào mắt]; eistein → Elphy: cận chiến 5 trúng 3 (`MeleeWeapon_Knife`) [1 lần là hất đất vào mắt]; Elphy → eistein: cận chiến 3 trúng 0 (`MeleeWeapon_Knife`, tay không); **Rat 1 CHẾT** (lúc 16:03, do Elphy, `MissingBodyPart`); **Elphy CHẾT** (lúc 16:46, do bac si, `Gunshot`) |
| 14 Decembary 5500 01:52 | 10.5 | Protein | **Protein gục** (từ vết thương do Elphy gây trước đó, `BloodLoss`) |
| 15 Decembary 5500 06:44–06:54 | 9.3 | Lynx, Bear_Grizzly (thú hoang) | Bear_Grizzly → Lynx: cận chiến 3 trúng 2 [huỷ 1 bộ phận]; **Lynx CHẾT** (do Bear_Grizzly, `Scratch`) |
| 15 Decembary 5500 13:43–14:15 | 9.0 | bac si, eistein ↔ Raccoon#2, Raccoon#1 (thú hoang) | Raccoon#2 → eistein: cận chiến 11 trúng 6; eistein → Raccoon#1: cận chiến 2 trúng 2 (`MeleeWeapon_Knife`) [huỷ 3 bộ phận]; Raccoon#1 → eistein: cận chiến 1 trúng 0; eistein → Raccoon#2: cận chiến 2 trúng 0 (`MeleeWeapon_Knife`); bac si → Raccoon#2: bắn 1 trúng 1 (`Gun_BoltActionRifle`) [huỷ 2 bộ phận]; **Raccoon#1 CHẾT** (lúc 13:45, do eistein, `Cut`); **Raccoon#1 gục** (lúc 13:45, do eistein, `Cut`); **Raccoon#2 CHẾT** (lúc 14:15, do bac si, `Gunshot`) |
| 4 Aprimay 5501 16:06 | 4.9 | Rasher (Moigleoo (OutlanderRoughPig)) | **Rasher CHẾT** (`BloodLoss`) |
| 7 Aprimay 5501 10:13–10:58 | 2.1 | bac si ↔ WildBoar (thú hoang) | bac si → WildBoar: bắn 9 trúng 0 (`Gun_BoltActionRifle`) [4 phát vướng vật cản] |
| 7 Aprimay 5501 18:01–8 Aprimay 5501 01:22 | 1.8 | Protein, bac si, eistein ↔ Tangle (thực thể Bóng tối (Entities)) ↔ Boomrat (thú hoang) | bac si → Boomrat: bắn 12 trúng 0 (`Gun_BoltActionRifle`) [7 phát vướng vật cản]; Tangle → bac si: bắn 2 trúng 0 (`Gun_BoltActionRifle`) [1 phát vướng vật cản] + cận chiến 8 trúng 2 [1 lần là hất đất vào mắt]; bac si → Tangle: bắn 25 trúng 13 (`Gun_BoltActionRifle`) [5 phát vướng vật cản, huỷ 3 bộ phận] + cận chiến 17 trúng 12 (`Gun_BoltActionRifle`, tay không) [1 lần là hất đất vào mắt, huỷ 1 bộ phận]; Protein → Tangle: cận chiến 27 trúng 19 (tay không) [1 lần là hất đất vào mắt, huỷ 1 bộ phận]; Tangle → Protein: bắn 4 trúng 1 (`Gun_BoltActionRifle`) [1 phát vướng vật cản] + cận chiến 4 trúng 3 (`Gun_BoltActionRifle`) [1 lần là hất đất vào mắt]; eistein → Tangle: cận chiến 19 trúng 14 (`MeleeWeapon_Knife`, tay không) [1 lần là hất đất vào mắt, huỷ 5 bộ phận]; Tangle → eistein: cận chiến 1 trúng 1; **Tangle gục** (lúc 21:04, do eistein, `Cut`); **Tangle CHẾT** (lúc 22:26, do bac si, `Gunshot`); **Tangle gục** (lúc 23:09, do Protein, `Bruise`); **Tangle CHẾT** (lúc 23:36, do bac si, `Bruise`); **Tangle gục** (lúc 8 Aprimay 5501 00:00, do Protein, `Bruise`); **Tangle CHẾT** (lúc 8 Aprimay 5501 00:09, do eistein, `MissingBodyPart`); **Tangle gục** (lúc 8 Aprimay 5501 00:24, do bac si, `Bruise`); **Tangle CHẾT** (lúc 8 Aprimay 5501 00:31, do eistein, `Cut`); **Tangle gục** (lúc 8 Aprimay 5501 00:47, do bac si, `Gunshot`); **Tangle CHẾT** (lúc 8 Aprimay 5501 01:22, do Protein, `Bruise`) |
| 8 Aprimay 5501 20:17–20:31 | 0.7 | eistein, bac si ↔ Alpaca (thú hoang) | Alpaca → eistein: cận chiến 2 trúng 1; bac si → Alpaca: bắn 2 trúng 1 (`Gun_BoltActionRifle`) [1 phát vướng vật cản] + cận chiến 3 trúng 1 (`Gun_BoltActionRifle`); Alpaca → bac si: cận chiến 2 trúng 1; eistein → Alpaca: cận chiến 3 trúng 3 (`MeleeWeapon_Knife`); **Alpaca CHẾT** (do eistein) |
| 9 Aprimay 5501 03:32–05:33 | 0.4 | bac si ↔ WildBoar (thú hoang) | bac si → WildBoar: bắn 20 trúng 2 (`Gun_BoltActionRifle`) [8 phát vướng vật cản, huỷ 2 bộ phận]; **WildBoar CHẾT** (lúc 05:33, do bac si, `MissingBodyPart`) |
| 9 Aprimay 5501 09:37–12:26 | 0.1 | bac si ↔ Boomrat (thú hoang) | bac si → Boomrat: bắn 26 trúng 2 (`Gun_BoltActionRifle`) [10 phát vướng vật cản, huỷ 4 bộ phận]; **Boomrat DiedExplosive** (lúc 12:26, do bac si) |


### Tương tác xã hội gần đây (`playLog`: 150 dòng)

Game chỉ giữ 150 tương tác mới nhất — ở đây là từ 13 Decembary 5500 16:28 đến 9 Aprimay 5501 12:32. Chiều mũi tên: người mở lời → người nghe.

| Ai → ai (đều đang ở trên map) | Số lần theo loại |
|---|---|
| bac si → eistein | `Chitchat` (chuyện phiếm) ×16, `Slight` (nói mỉa / coi thường) ×1 |
| eistein → Protein | `Chitchat` (chuyện phiếm) ×13, `Slight` (nói mỉa / coi thường) ×1 |
| Protein → eistein | `Chitchat` (chuyện phiếm) ×10, `Insult` (xúc phạm) ×2, `Slight` (nói mỉa / coi thường) ×1 |
| eistein → bac si | `Chitchat` (chuyện phiếm) ×13 |
| bac si → Protein | `Chitchat` (chuyện phiếm) ×11 |
| Protein → bac si | `Chitchat` (chuyện phiếm) ×7 |
| Rababarne → Snail | `Chitchat` (chuyện phiếm) ×1 |
| Daga → Hare | `Chitchat` (chuyện phiếm) ×1 |
| Grasshopper → Rababarne | `Chitchat` (chuyện phiếm) ×1 |
| Snail → Hedgehog | `Chitchat` (chuyện phiếm) ×1 |
| Dobreibo → Bat | `Chitchat` (chuyện phiếm) ×1 |

**Đáng chú ý (không phải chuyện phiếm, xếp từ cũ → mới):** 13 Decembary 5500 16:28 (10.8 ngày trước) — Protein → eistein: `Insult` (xúc phạm); 13 Decembary 5500 21:22 (10.6 ngày trước) — Protein → eistein: `Insult` (xúc phạm); 1 Aprimay 5501 20:08 (7.7 ngày trước) — Mole → Cailo: `Slight` (nói mỉa / coi thường); 1 Aprimay 5501 22:32 (7.6 ngày trước) — Jackal → Cailo: `DeepTalk` (tâm sự sâu); 1 Aprimay 5501 23:13 (7.6 ngày trước) — Caxigo → Skunk: `DeepTalk` (tâm sự sâu); 2 Aprimay 5501 00:35 (7.5 ngày trước) — Garaol → Black: `DeepTalk` (tâm sự sâu); 2 Aprimay 5501 01:24 (7.5 ngày trước) — Black → Garaol: `DeepTalk` (tâm sự sâu); 2 Aprimay 5501 01:55 (7.5 ngày trước) — Peza → Frog: `DeepTalk` (tâm sự sâu); 2 Aprimay 5501 10:28 (7.1 ngày trước) — Garaol → Skunk: `DeepTalk` (tâm sự sâu); 2 Aprimay 5501 12:28 (7.0 ngày trước) — Cailo → Peza: `DeepTalk` (tâm sự sâu); 3 Aprimay 5501 10:51 (6.1 ngày trước) — Protein → eistein: `Slight` (nói mỉa / coi thường); 6 Aprimay 5501 12:30 (3.0 ngày trước) — bac si → eistein: `Slight` (nói mỉa / coi thường); 7 Aprimay 5501 16:54 (1.8 ngày trước) — eistein → Protein: `Slight` (nói mỉa / coi thường).

**Có người/thú hiện không ở trên map** (khách đã rời đi, thú đã chết…): 70 dòng — `Chitchat` (chuyện phiếm) ×62, `DeepTalk` (tâm sự sâu) ×7, `Slight` (nói mỉa / coi thường) ×1; số dòng theo từng cá thể: Cailo [Camro dân tộc (TribeCivil)] ×15, Peza [Camro dân tộc (TribeCivil)] ×15, Garaol [Camro dân tộc (TribeCivil)] ×14, Mole [Camro dân tộc (TribeCivil)] ×13, Jackal [Camro dân tộc (TribeCivil)] ×13, Skunk [Camro dân tộc (TribeCivil)] ×13, Black [Camro dân tộc (TribeCivil)] ×12, Frog [Camro dân tộc (TribeCivil)] ×11, Colmea [Camro dân tộc (TribeCivil)] ×10, Buffalo [Camro dân tộc (TribeCivil)] ×9, Caxigo [Camro dân tộc (TribeCivil)] ×9, Martin [Orussia (OutlanderCivil)] ×3, … và 3 cá thể khác.


## 17. Chính sách đang dùng

**Chính sách thuốc «Chính sách thuốc»** (3 người dùng): Beer: giải trí; SmokeleafJoint: giải trí; Ambrosia: khi nghiện; Drug_Psilocap: khi nghiện; Yayo: khi nghiện; Flake: khi nghiện; PsychiteTea: khi nghiện; GoJuice: khi nghiện; WakeUp: khi nghiện; Penoxycyline: khi nghiện; Luciferium: khi nghiện; VoidsightSerum: khi nghiện; MetalbloodSerum: khi nghiện; JuggernautSerum: khi nghiện; MindNumbSerum: khi nghiện.

Chính sách có sẵn — thuốc: «Chính sách thuốc», «Không dùng», «Không giới hạn», «1 lần mỗi ngày» · trang phục: «Gì cũng mặc», «Lao động», «Vũ trang», «Trần trụi», «Nô lệ», «Du hành vũ trụ» · ăn uống: «Xa hoa», «Ngon», «Đơn giản», «Hỗn hợp», «Tươi sống», «Nhịn đói», «Đồ chay», «Ăn thịt», «Ăn thịt người», «Thịt côn trùng».


## 18. Giới hạn của dữ liệu

- File save **không lưu** các giá trị game tự tính lúc chạy: chỉ số phòng (ấn tượng/đẹp/sạch), tốc độ di chuyển, mức đau, năng lực cơ thể (Consciousness, Moving…), tốc độ chảy máu, HP tối đa, điện lưới, vùng phủ sáng, và các *thought tình huống* (đau, phòng xấu, thiếu giải trí, nghiện…). Mục «ký ức» ở trên chỉ gồm thought dạng ký ức.
- Các trường có giá trị bằng mặc định của C# (`gender=Male`, `healthState=Mobile`, `hostilityResponse=Flee`, `selfTend=False`, `medCare=NoCare`, `age=0` của ký ức vừa phát sinh) bị RimWorld bỏ qua khi ghi XML — công cụ tự điền lại đúng mặc định của game và ghi rõ `(mặc định)`.
- Ngày giờ: múi giờ suy từ tick bắt đầu ván và kiểm chứng bằng tick reset XP lúc nửa đêm của pawn.
- Bảng nghiên cứu, ngưỡng thối của thực phẩm/xác, dinh dưỡng, ngưỡng tâm trạng: dựa trên giá trị def **vanilla** (mod có thể thay đổi).
- Phòng, mạch quặng, khoảng cách, cảnh báo ở mục 2: do công cụ suy ra từ dữ liệu thô (không phải do game ghi).
- Tên def của địa hình/đá/mái được tra ngược từ mã băm; mã không nhận ra sẽ hiện dạng `Terrain#12345`.
