# TRẠNG THÁI THUỘC ĐỊA «nhung nguoi cung kho» — RimWorld 1.7.5000 rev1275

*Ảnh chụp tại **ngày 15 Decembary năm 5500, 13:27** (tick 1,458,646, ngày chơi thứ 24.311). Sinh tự động từ file save `Autosave-4.rws` (14,441,082 byte, SHA-1 `1fe0eddac0ff64417109e70204fbf22b8326f27c`) bằng script phân tích; không có nội dung nào do người viết tay. File chỉ đúng tại thời điểm lưu nói trên — nếu ván chơi đã đi tiếp (file save được lưu lại) thì bản này đã cũ.*


## 0. Cách đọc file này

- Đây là **ảnh chụp trạng thái** một ván RimWorld tại đúng thời điểm lưu. Mọi con số lấy trực tiếp từ file save; chỗ nào ghi *(suy luận)* / *(ước tính)* là do công cụ tính thêm, kèm giả định.
- **Toạ độ** `(x,z)`: gốc (0,0) ở góc Tây-Nam map; x tăng về **Đông**, z tăng về **Bắc**. Khoảng cách tính bằng ô.
- **Thời gian**: 1 giờ game = 2.500 tick, 1 ngày = 60.000 tick, 1 quý = 15 ngày, 1 năm = 4 quý (Aprimay, Jugust, Septober, Decembary).
- Tên trong dấu `` ` `` là **defName** gốc của game (tiếng Anh) — dùng để tra wiki chính xác.
- Mức nhu cầu/tâm trạng là 0–100%. Ưu tiên việc: 1 = cao nhất … 4 = thấp nhất, 0 = tắt.
- Mục 2 là danh sách **việc cần chú ý** do công cụ tự rà theo quy tắc; các mục sau là dữ liệu đầy đủ để kiểm chứng.
- File save chứa cả những thứ **người chơi chưa nhìn thấy** (vùng còn sương mù, bên trong kén/hòm cổ). Các chỗ đó đều được ghi rõ «trong sương mù» — hãy coi là thông tin biết trước, người chơi trong game chưa có.
- File này **tự chứa đủ**, không kèm file phụ nào. Thứ duy nhất chi tiết hơn (từng ô đất, từng cây, mọi trường XML) là chính file save `Autosave-4.rws`.
- **Mục lục:** 1. Ảnh chụp nhanh · 2. Việc cần chú ý ngay · 3. Con người trên map · 4. Ma trận công việc (ai bật việc gì) · 5. Căn cứ · 6. Kho & tài nguyên · 7. Trồng trọt · 8. Việc đã đánh dấu (designations) · 9. Mối đe doạ & địa điểm đáng chú ý trên map · 10. Động vật · 11. Bản đồ · 12. Xác chết trên map · 13. Nghiên cứu · 14. Nhiệm vụ · 15. Phe phái · 16. Dòng thời gian · 17. Chính sách đang dùng · 18. Giới hạn của dữ liệu


## 1. Ảnh chụp nhanh

| Thuộc tính | Giá trị |
|---|---|
| Ngày giờ trong game | **ngày 15 Decembary năm 5500, 13:27** — mùa Hè (ngày 60/60 của năm; múi giờ UTC-3) |
| Sắp tới | sang ngày mới sau 10.5 giờ; sang quý Aprimay sau 10.5 giờ (mùa Thu — suy luận, bán cầu Nam) |
| Đã chơi | 24.311 ngày game (tick 1,458,646); bắt đầu ngày 6 Septober 5500 06:00 |
| Thuộc địa | «nhung nguoi cung kho» — phe «AnkerGames's faction» — ô thế giới 162296,0 — biome `TemperateForest` — hành tinh EC-666 Secondary |
| Kịch bản / người kể chuyện | Hạ cánh khẩn cấp · `Cassandra` · độ khó `Medium` |
| Dân số trên map | 3 thuộc địa viên, 1 khách |
| Đột kích / đe doạ lớn | 4 lần đột kích (gần nhất: Khí độc đàn ông (PirateWaster), lúc 13 Decembary 5500 14:48); mối đe doạ lớn gần nhất: `ManhunterPack` lúc 15 Decembary 5500 12:24 (1.1 giờ trước) |
| Thời tiết / nhiệt độ | `Clear` · ngoài trời 26.9°C (đang là 13:27) · điều kiện đặc biệt: không · 5 ngày qua game ghi kèm sự kiện: ngoài trời 19.8–33.8°C (cao nhất lúc 10 Decembary 5500 18:33), trong phòng tới 32.2°C (lúc 10 Decembary 5500 22:01) |
| Tài sản thuộc địa | 22,701 (mẫu gần nhất 7.5 giờ trước); vật phẩm 13,268; 1 ngày trước 22,015 |
| Tâm trạng TB thuộc địa (game ghi) | 48% → 43% → 52% → 45% → 32% → 16% → 21% → 33% (mỗi mẫu cách 12.0 giờ) |
| Mods | Harmony, Core, Royalty, Ideology, Biotech, Anomaly, Odyssey, (1.7)Multiplayer-temp, RimHUD, SimpleCameraSetting |


## 2. Việc cần chú ý ngay

*Tự rà từ dữ liệu, xếp theo mức độ. Ngưỡng tâm trạng 35/20/5% là ngưỡng gốc vanilla (trait có thể làm lệch).*

- **[KHẨN] Tinh thần** — eistein đang trong cơn khủng hoảng `Binging_DrugExtreme`, chất: GoJuice (đã 17.0 giờ, do tâm trạng thấp) — không điều khiển/giao việc được.
- **[KHẨN] Tinh thần** — eistein: tâm trạng 19% — dưới ngưỡng khủng hoảng NẶNG 20% (ngưỡng gốc vanilla; đã dưới ngưỡng nhẹ 1.9 ngày).
- **[KHẨN] Đe doạ** — `Raccoon` ×2 đang ở trạng thái `ManhunterPermanent` (thú điên — tấn công mọi người nó thấy): (118,136) (cách tâm căn cứ 13 ô Tây Nam; người gần nhất: eistein, cách 5 ô; job `Goto`); (130,166) (cách tâm căn cứ 23 ô Bắc; người gần nhất: Helena, cách 14 ô; job `Goto`).
- **[QUAN TRỌNG] Nghiện** — eistein: nhu cầu `Chemical_Smokeleaf` = 0% → đang VẬT (cai) thuốc.
- **[QUAN TRỌNG] Y tế** — eistein: cần chăm sóc lại (lần chăm trước đã hết hiệu lực): LungRot phổi trái (Lung) (mức 0.149), LungRot phổi phải (Lung) (mức 0.145).
- **[QUAN TRỌNG] Nghiện** — eistein: `SmokeleafAddiction` mức 0.039 — tự hết sau ~1.18 ngày nếu không dùng lại.
- **[QUAN TRỌNG] Tinh thần** — Protein: tâm trạng 21% — dưới ngưỡng khủng hoảng nhẹ 35% (ngưỡng gốc vanilla; đã dưới ngưỡng nhẹ 5.5 giờ).
- **[QUAN TRỌNG] Nhu cầu** — Protein: Thức ăn (`Food`) chỉ còn 15%.
- **[QUAN TRỌNG] Nhu cầu** — Protein: Giải trí (`Joy`) chỉ còn 1%.
- **[QUAN TRỌNG] Vũ trang** — Protein đang KHÔNG cầm vũ khí nào (lần giao tranh gần nhất dùng `Gun_Revolver`, lúc 13 Decembary 5500 16:44). Vũ khí đang nằm trên map: `Gun_Autopistol` [Normal] tại (97,142) trong «Vùng kho chứa 1»; `Gun_Revolver` [Normal] tại (103,131) trong «Vùng kho chứa 1» — đang bị CẤM (forbidden), phải bỏ cấm mới nhặt được; `MeleeWeapon_Knife` [Poor] tại (96,141) trong «Vùng kho chứa 1»; trên map đang có thú điên/kẻ địch.
- **[QUAN TRỌNG] Đe doạ** — Nhóm thù địch `LordJob_SleepThenAssaultColony` (bầy cỗ máy chiến đấu cơ (Mechanoid)): Mech_Militor×2, Mech_Scorcher×1 quanh (201,69), cách căn cứ 103 ô Đông Nam — đang NGỦ ĐÔNG, sẽ thức và tấn công khi bị đánh động / khi có pawn làm lộ vùng sương mù ở đó.
- **[QUAN TRỌNG] Đe doạ** — Thú săn mồi hoang `Wolf_Timber` tại (124,107), cách tâm căn cứ 36 ô Nam; mức thức ăn 0.82, job Wait_Wander.
- **[QUAN TRỌNG] Lương thực** — `MealSimple` ×7: lô sớm nhất sẽ hỏng sau ~1.17 ngày (ở ≥10°C, không bảo quản lạnh).
- **[QUAN TRỌNG] Trồng trọt** — Ruộng «Vùng trồng trọt 1» (98 ô, x 108–121, z 135–141) đặt trồng `Plant_Rice` nhưng hiện có 0 cây trồng (có 19 cây dại mọc lẫn).
- **[QUAN TRỌNG] Trồng trọt** — Ruộng «Vùng trồng trọt 2» (11 ô, x 114–117, z 148–151) đặt trồng `Plant_Rice` nhưng hiện có 0 cây trồng (có 2 cây dại mọc lẫn).
- **[QUAN TRỌNG] Trồng trọt** — Ruộng «Growing zone 2» (15 ô, x 131–138, z 172–176) đặt trồng `Plant_Healroot` nhưng hiện có 0 cây trồng (có 5 cây dại mọc lẫn).
- **[QUAN TRỌNG] Công việc** — Có Hunt×26 đang chờ nhưng KHÔNG thuộc địa viên nào bật việc `Hunting`.
- **[QUAN TRỌNG] Nhân lực** — Chỉ 2/3 thuộc địa viên đang làm việc bình thường được (số còn lại đang khủng hoảng tinh thần hoặc gục).
- **[QUAN TRỌNG] Nhiệm vụ** — «The Hard Prisoner» (`Hospitality_Prisoners`) chưa nhận — hết hạn nhận sau 1.7 ngày.
- **[lưu ý] Nhu cầu** — eistein: Thoải mái (`Comfort`) chỉ còn 0%.
- **[lưu ý] Khách** — Helena (Đế chế tan nát (Empire)) là KHÁCH đang ở căn cứ, đang nằm giường tại (139,155); quest tag: Quest4.pawn.
- **[lưu ý] Chỗ ở** — Protein chưa được gán giường riêng (ownedBed = null).
- **[lưu ý] Lương thực** — 7 suất ăn sẵn + 304 đơn vị nguyên liệu thô cho 4 người: ≈ 3.4 ngày nếu ăn nguyên trạng, ≈ 5.2 ngày nếu nấu hết thành suất đơn giản (ước tính theo dinh dưỡng vanilla, 1.6/người/ngày).
- **[lưu ý] Vệ sinh** — Xác tươi `Corpse_Rat` «Rat 1» tại (133,134) (cách tâm căn cứ 10 ô) sẽ bắt đầu thối sau ~14.6 giờ (ở ≥10°C).
- **[lưu ý] Công việc** — Công trình chưa xây: Cooler×3, WoodFiredGenerator×5 (bản vẽ cũ nhất đặt 2.0 ngày trước).
- **[lưu ý] Hạ tầng** — Đã nghiên cứu Electricity nhưng chưa có máy phát/pin nào được xây xong.
- **[lưu ý] Nhiệt độ** — bac si có ký ức `SleptInHeat` (ngủ nơi nóng). Ngoài trời hiện 26.9°C, phòng có giường: R1 24.3°C, R3 24.9°C, R6 24.1°C, R7 24.6°C; nhưng 5 ngày qua ban ngày lên tới 33.8°C ngoài trời (10 Decembary 5500 18:33) và 32.2°C trong phòng (10 Decembary 5500 22:01).
- **[lưu ý] Kho** — Vật phẩm nằm ngoài mọi vùng kho (chưa bị cấm, không trong sương mù): GravlitePanel×348, Steel×152, WoodLog×31, Silver×1.
- **[lưu ý] Nhiệm vụ** — «Tín hiệu cơ học» đang diễn ra — thành công khi có tín hiệu: gravEngine.Inspected.
- **[lưu ý] Nhiệm vụ** — «Ship to the Stars» đang diễn ra — thành công khi có tín hiệu: escapeShip.LaunchedShip.
- **[lưu ý] Nhiệm vụ** — «Shoytt's Sad Survivors» (`Hospitality_Refugee`) chưa nhận — hết hạn nhận sau 4.7 ngày — có người quen: Shoytt Barytt là `Spouse` của Helena (khách đang ở trên map).
- **[lưu ý] Lịch** — Còn 10.5 giờ nữa sang quý Aprimay (mùa Thu — suy luận theo bán cầu Nam).


## 3. Con người trên map

| # | Tên | Vai trò | Giới, tuổi | Ô | Đang làm gì | Tâm trạng | Ăn / Ngủ / Giải trí | Sức khỏe (tóm tắt) | Vũ khí |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **bac si** | thuộc địa viên | M, 16t | (147,151) | `FeedPatient` → Suất ăn đơn giản `MealSimple` (đang được bê/giữ, không nằm rời trên map) (đối tượng: Protein) | 63% | 84% / 64% / 89% | 9 vết thương | Gun_BoltActionRifle (Normal) |
| 2 | **eistein** | thuộc địa viên | M, 47t | (115,132) | KHỦNG HOẢNG `Binging_DrugExtreme` (job `Wait_Wander`) | 19% | 64% / 19% / 99% | LungRot, LungRotExposure, MissingBodyPart, SmokeleafAddiction, SmokeleafTolerance | MeleeWeapon_Knife (Plasteel, Normal) |
| 3 | **Helena** | khách | F, 41t | (139,155) | `LayDown` — nằm trên giường (thức) → Giường `Bed` @(139, 155) | 46% | 22% / 80% / — | 4 vết thương | — |
| 4 | **Protein** | thuộc địa viên | M, 31t | (151,155) | `LayDown` — đang ngủ → Giường `Bed` @(151, 155) | 21% | 15% / 90% / 1% | 7 vết thương, BloodLoss, LungRotExposure | — |


### bac si — `Human665` (thuộc địa viên)

- **Danh tính:** Nikolay “bac si” Bishop · Male · 15.9 tuổi (niên đại 872) · phe AnkerGames's faction (PlayerColony) · kind `Colonist` · xenotype Baseliner · tôn giáo Astropolitan (86%)
- **Xuất thân / tính cách:** MedicalAssistant12 / — · trait: ShootingAccuracy(-1), FastLearner, BodyPurist
- **Hiện tại:** ô (147,151) · `FeedPatient` → Suất ăn đơn giản `MealSimple` (đang được bê/giữ, không nằm rời trên map) (đối tượng: Protein) · lịch giờ này: Anything
- **Tâm trạng:** 62.9%
- **Nhu cầu:** Food 84% · Rest 64% · Joy 89% · Beauty 40% · Comfort 28% · Outdoors 100% · DrugDesire 50% · RoomSize 84%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (10; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** `Chitchat`→Protein (thiện cảm +24, 0.3 ngày trước) · `Chitchat`→eistein (thiện cảm +35, 0.3 ngày trước) · `DeepTalk`→Protein (thiện cảm +14, 17.2 ngày trước) · `DeepTalk`→Protein (thiện cảm +14, 14.9 ngày trước) · `Insulted`→eistein (thiện cảm -14, 7.1 ngày trước) · `SleepDisturbed` (0.8 ngày trước) · `SleptInHeat` (0.8 ngày trước) · `SleepDisturbed` (0.3 ngày trước) · `AteRawHumanlikeMeat`→Crow (thú hoang) (thiện cảm -5, 0.3 ngày trước) · `AteFineMeal` (0.1 ngày trước)
- **Tổng thiện cảm từ ký ức:** Protein +52, eistein +22, Crow (thú hoang) -5
- **Sức khỏe** (trạng thái `Mobile`; 9 hediff):

| Hediff | Bộ phận | Mức | Chăm sóc | Tuổi (ngày) | Ghi chú |
|---|---|---|---|---|---|
| `Cut` | thận trái (Kidney) | 4.17 | đã băng/chăm (21%) | 1.9 | do knife/blade |
| `Cut` | thân (Torso) | 3.55 | đã băng/chăm (27%) | 1.9 | do knife/blade |
| `Cut` | vai trái (Shoulder) | 4.96 | đã băng/chăm (5%) | 1.9 | do knife/blade |
| `Cut` | tay trái (Arm) | 4.15 | đã băng/chăm (27%) | 1.9 | do knife/blade |
| `Cut` | ngón thứ hai chân trái (Toe) | 1.24 | đã băng/chăm (41%) | 1.9 | do knife/blade |
| `Crack` | xương chày trái (Tibia) | 1.13 | đã băng/chăm (34%) | 1.9 | do knife/blade |
| `Cut` | chân trái (Leg) | 1.09 | đã băng/chăm (40%) | 1.9 | do knife/blade |
| `Cut` | bàn chân trái (Foot) | 1.31 | đã băng/chăm (10%) | 1.9 | do knife/blade |
| `Bruise` | thân (Torso) | 5.31 | đã băng/chăm (21%) | 1.9 | do human/fist |

- **Kỹ năng:** Shooting 7★ · Melee 4★ · Construction 4 · Mining 1 · Cooking 1 · Plants 4 · Animals 2 · Crafting 0 · Artistic 3★★ · Medicine 7★★ · Social 2 · Intellectual 2
- **Ưu tiên việc:** **1**: Patient, Doctor, Construction · **2**: PlantCutting, Cleaning · **3**: PatientBedRest, BasicWorker, Art, Hauling · tắt (0): Firefighter, Warden, Handling, Cooking, Hunting, Growing, Mining, Smithing, Tailoring, Crafting, Research, Childcare, DarkStudy, Fishing
- **Mặc:** Apparel_CollarShirt (Synthread, Normal), Apparel_Pants (Synthread, Normal) · **Cầm:** Gun_BoltActionRifle (Normal) · **Túi:** MedicineIndustrial ×3 · **Đang bê:** MealSimple
- **Thiết lập:** giường riêng: Thing_Bed36903 @(134,147) · y tế: Best · tự băng: True · phản ứng địch: Attack · trang phục «Gì cũng mặc» · thuốc «Chính sách thuốc» · ăn «Xa hoa»
- **Lịch 24h:** 00–05 Sleep · 06 Meditate · 07 Joy · 08–19 Anything · 20 Joy · 21 Meditate · 22–23 Sleep
- **Lần dùng chất gần nhất:** Beer (21.0 ngày trước)


### eistein — `Human668` (thuộc địa viên)

- **Danh tính:** Anthony “eistein” Hayes · Male · 46.7 tuổi (niên đại 542) · phe AnkerGames's faction (PlayerColony) · kind `Colonist` · xenotype Baseliner · tôn giáo Astropolitan (93%)
- **Xuất thân / tính cách:** StoryWriter67 / Bartender62 · trait: FastLearner, DrugDesire(+2)
- **Hiện tại:** ô (115,132) · KHỦNG HOẢNG `Binging_DrugExtreme` (job `Wait_Wander`) · lịch giờ này: Anything
- **Tâm trạng:** 18.6% · thời gian liên tục dưới ngưỡng nhẹ/nặng/cực đoan: 1.9 ngày / 1.0 ngày / 0.8 giờ *(bộ đếm đứng yên trong lúc đang khủng hoảng)* · **đang khủng hoảng:** `Binging_DrugExtreme`, chất `GoJuice` (nhóm Hard), đã kéo dài 17.0 giờ, do tâm trạng thấp gây ra, không có hạn tự hết cưỡng bức (forceRecoverAfterTicks = -1)
- **Nhu cầu:** Food 64% · Rest 19% · Joy 99% · Beauty 40% · Comfort 0% · Outdoors 100% · DrugDesire 24% · RoomSize 100% · Chemical_Smokeleaf 0%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (9; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** `Chitchat`→bac si (thiện cảm +30, 0.3 ngày trước) · `Chitchat`→Protein (thiện cảm +33, 0.1 ngày trước) · `Insulted`→Protein (thiện cảm -13, 1.9 ngày trước) · `InsultedMood`→Protein (1.9 ngày trước) · `ObservedLayingCorpse` (0.3 ngày trước) · `Insulted`→Protein (thiện cảm -9, 1.7 ngày trước) · `InsultedMood`→Protein (1.7 ngày trước) · `AteRawHumanlikeMeat`→Crow (thú hoang) (thiện cảm -5, 0.3 ngày trước) · `AteFineMeal` (0.2 ngày trước)
- **Tổng thiện cảm từ ký ức:** bac si +30, Protein +12, Crow (thú hoang) -5
- **Sức khỏe** (trạng thái `Mobile`; 6 hediff):

| Hediff | Bộ phận | Mức | Chăm sóc | Tuổi (ngày) | Ghi chú |
|---|---|---|---|---|---|
| `SmokeleafAddiction` | toàn thân | 0.04 | — | 24.3 | giảm 0.033/ngày → hết sau ~1.18 ngày |
| `SmokeleafTolerance` | toàn thân | 0.51 | — | 20.5 | giảm 0.015/ngày → hết sau ~34.19 ngày |
| `MissingBodyPart` | ngón áp út chân phải (Toe) | 0.50 | đã băng/chăm (71%) | 5.3 | vì Bite |
| `LungRotExposure` | toàn thân | 0.45 | — | 3.4 |  |
| `LungRot` | phổi trái (Lung) | 0.15 | HẾT HẠN chăm — cần chăm lại (100%) | 2.7 | +0.300/ngày; tự hết sau 2.5 ngày |
| `LungRot` | phổi phải (Lung) | 0.15 | HẾT HẠN chăm — cần chăm lại (78%) | 2.7 | +0.300/ngày; tự hết sau 2.9 ngày |

- **Kỹ năng:** Shooting 1 · Melee 8★ · Construction 4 · Mining 3 · Cooking 7 · Plants 3 · Animals 4 · Crafting 2 · Artistic 7 · Medicine 4 · Social 9★ · Intellectual 9★
- **Ưu tiên việc:** **1**: Firefighter, Patient, Cleaning · **2**: Mining, PlantCutting, Hauling, Research · **3**: PatientBedRest, BasicWorker, Warden, Construction, Art, DarkStudy · tắt (0): Doctor, Handling, Cooking, Hunting, Growing, Smithing, Tailoring, Crafting, Childcare, Fishing
- **Mặc:** Apparel_FlakPants (Normal), Apparel_Parka (Synthread, Normal), Apparel_AdvancedHelmet (Plasteel, Normal) · **Cầm:** MeleeWeapon_Knife (Plasteel, Normal) · **Túi:** —
- **Thiết lập:** giường riêng: Thing_Bed53128 @(145,155) · y tế: Best · tự băng: True · phản ứng địch: — · trang phục «Gì cũng mặc» · thuốc «Chính sách thuốc» · ăn «Xa hoa»
- **Lịch 24h:** 00–05 Sleep · 06 Meditate · 07 Joy · 08–19 Anything · 20 Joy · 21 Meditate · 22–23 Sleep
- **Lần dùng chất gần nhất:** Beer (24.0 ngày trước), SmokeleafJoint (20.5 ngày trước), GoJuice (16.2 giờ trước)


### Helena — `Human90055` (khách)

- **Danh tính:** Helena Arianites · Female · 40.5 tuổi (niên đại 126) · phe Đế chế tan nát (Empire) · kind `SpaceRefugee` · xenotype Baseliner · tôn giáo Astropolitan (92%)
- **Xuất thân / tính cách:** MusicalKid86 / Policeman45 · trait: ShootingAccuracy(+1)
- **Hiện tại:** ô (139,155) · `LayDown` — nằm trên giường (thức) → Giường `Bed` @(139, 155) · lịch giờ này: —
- **Thân phận:** hostFaction=AnkerGames's faction (PlayerColony) · guestStatus=Guest · đã được chữa 4 lần · questTags: Quest4.pawn · vào map lúc 12 Decembary 5500 18:59
- **Tâm trạng:** 45.6%
- **Nhu cầu:** Food 22% · Rest 80% · Beauty 40% · Comfort 75% · Outdoors 88% · DrugDesire 50% · RoomSize 53%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (4; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** `RescuedMe`→bac si (thiện cảm +15, 2.8 ngày trước) · `SleptInHeat` (0.8 ngày trước) · `AteFineMeal` (0.5 ngày trước) · `AteRawHumanlikeMeat`→Crow (thú hoang) (thiện cảm -5, 0.3 ngày trước)
- **Tổng thiện cảm từ ký ức:** bac si +15, Crow (thú hoang) -5
- **Sức khỏe** (trạng thái `Mobile`; 4 hediff):

| Hediff | Bộ phận | Mức | Chăm sóc | Tuổi (ngày) | Ghi chú |
|---|---|---|---|---|---|
| `Cut` | chân phải (Leg) | 9.53 | đã băng/chăm (66%) | 2.9 |  |
| `Crack` | xương đòn phải (Clavicle) | 2.01 | đã băng/chăm (40%) | 2.9 |  |
| `Stab` | tay phải (Arm) | 7.65 | đã băng/chăm (21%) | 2.9 |  |
| `Crack` | cột sống (Spine) | 2.97 | đã băng/chăm (47%) | 2.9 |  |

- **Kỹ năng:** Shooting 5★★ · Melee 8★★ · Construction 3 · Mining 3 · Cooking 2 · Plants 3 · Animals 3 · Crafting 1 · Artistic 9★★ · Medicine 2 · Social 4 · Intellectual 4
- **Ưu tiên việc:** — (không có bảng ưu tiên: không phải thuộc địa viên)
- **Mặc:** Apparel_BasicShirt (WoolSheep, Normal), Apparel_Pants (WoolBison, Normal), Apparel_Parka (Cloth, Normal) · **Cầm:** — · **Túi:** —
- **Thiết lập:** giường riêng: chưa có · y tế: HerbalOrWorse · tự băng: — · phản ứng địch: — · trang phục «—» · thuốc «—» · ăn «Xa hoa»
- **Quan hệ:** Parent: Ali, Spouse: Shoytt


### Protein — `Human672` (thuộc địa viên)

- **Danh tính:** Ichabod “Protein” Andrade · Male · 31.3 tuổi (niên đại 86) · phe AnkerGames's faction (PlayerColony) · kind `Colonist` · xenotype Baseliner · tôn giáo Astropolitan (95%)
- **Xuất thân / tính cách:** WreckageExplorer93 / LowWageWorker7 · trait: Transhumanist
- **Hiện tại:** ô (151,155) · `LayDown` — đang ngủ → Giường `Bed` @(151, 155) · lịch giờ này: Anything
- **Tâm trạng:** 21.0% · thời gian liên tục dưới ngưỡng nhẹ/nặng/cực đoan: 5.5 giờ / 0.0 giờ / 0.0 giờ
- **Nhu cầu:** Food 15% · Rest 90% · Joy 1% · Beauty 40% · Comfort 57% · Outdoors 99% · DrugDesire 50% · RoomSize 57%
- **Ký ức ảnh hưởng tâm trạng/thiện cảm (12; `A`→X nghĩa là ký ức VỀ việc X đã làm/nói, kéo theo thiện cảm với X):** `Chitchat`→bac si (thiện cảm +22, 0.3 ngày trước) · `Chitchat`→eistein (thiện cảm +34, 0.1 ngày trước) · `DeepTalk`→bac si (thiện cảm +13, 17.2 ngày trước) · `DeepTalk`→bac si (thiện cảm +13, 14.8 ngày trước) · `Slighted`→eistein (thiện cảm -5, 14.7 ngày trước) · `Slighted`→eistein (thiện cảm -4, 5.3 ngày trước) · `Slighted`→eistein (thiện cảm -5, 2.8 ngày trước) · `RescuedMe`→bac si (thiện cảm +15, 1.4 ngày trước) · `AteFineMeal` (0.6 ngày trước) · `AteRawHumanlikeMeat`→Crow (thú hoang) (thiện cảm -5, 0.3 ngày trước) · `ObservedLayingRottingCorpse` (0.2 ngày trước) · `SleepDisturbed`
- **Tổng thiện cảm từ ký ức:** bac si +63, eistein +21, Crow (thú hoang) -5
- **Sức khỏe** (trạng thái `Mobile`; 9 hediff):

| Hediff | Bộ phận | Mức | Chăm sóc | Tuổi (ngày) | Ghi chú |
|---|---|---|---|---|---|
| `LungRotExposure` | toàn thân | 0.48 | — | 3.7 |  |
| `Cut` | chân trái (Leg) | 6.45 | đã băng/chăm (24%) | 1.9 | do knife/blade |
| `BloodLoss` | toàn thân | 0.25 | — | 1.9 |  |
| `Cut` | thân (Torso) | 4.12 | đã băng/chăm (0%) | 1.9 | do knife/blade |
| `Cut` | chân trái (Leg) | 4.00 | đã băng/chăm (0%) | 1.9 | do knife/blade |
| `Stab` | chân phải (Leg) | 8.85 | đã băng/chăm (9%) | 1.9 | do knife/point |
| `Cut` | bàn tay trái (Hand) | 3.67 | đã băng/chăm (0%) | 1.9 | do knife/blade |
| `Cut` | tay trái (Arm) | 2.84 | đã băng/chăm (44%) | 1.9 | do knife/blade |
| `Bruise` | thân (Torso) | 1.35 | đã băng/chăm (18%) | 1.9 | do knife/blade |

- **Kỹ năng:** Shooting 3 · Melee 2 · Construction 2 · Mining 3 · Cooking 8★★ · Plants 10★★ · Animals 6★ · Crafting 4 · Artistic 2 · Medicine 4 · Social 4 · Intellectual 6★
- **Ưu tiên việc:** **1**: Firefighter, Patient, Handling, Cooking, Growing · **2**: Cleaning, Research, Fishing · **3**: PatientBedRest, BasicWorker, Mining, PlantCutting, Smithing, Tailoring, Crafting, Hauling, DarkStudy · tắt (0): Doctor, Warden, Hunting, Construction, Art, Childcare
- **Mặc:** Apparel_Pants (Synthread, Normal), Apparel_BasicShirt (Synthread, Normal), Apparel_FlakVest (Normal) · **Cầm:** — · **Túi:** —
- **Thiết lập:** giường riêng: chưa có · y tế: Best · tự băng: True · phản ứng địch: Attack · trang phục «Gì cũng mặc» · thuốc «Chính sách thuốc» · ăn «Xa hoa»
- **Lịch 24h:** 00–05 Sleep · 06 Meditate · 07 Joy · 08–19 Anything · 20 Joy · 21 Meditate · 22–23 Sleep
- **Lần dùng chất gần nhất:** Beer (19.9 ngày trước)
- **Quan hệ:** Parent: Eva, Parent: Isaias


## 4. Ma trận công việc (ai bật việc gì)

Số = mức ưu tiên (1 cao nhất), `·` = tắt; `kn` = cấp kỹ năng liên quan. Thứ tự hàng = thứ tự game xét khi cùng mức ưu tiên (trên trước). Chế độ ưu tiên thủ công: True.

| Việc | Tên | bac si | eistein | Protein | Ghi chú |
|---|---|---|---|---|---|
| `Firefighter` | Chữa cháy | · | 1 | 1 |  |
| `Patient` | Bệnh nhân | 1 | 1 | 1 |  |
| `Doctor` | Bác sĩ | 1 (kn 7) | · (kn 4) | · (kn 4) |  |
| `PatientBedRest` | Nằm nghỉ dưỡng | 3 | 3 | 3 |  |
| `BasicWorker` | Việc cơ bản | 3 | 3 | 3 |  |
| `Warden` | Cai ngục | · (kn 2) | 3 (kn 9) | · (kn 4) |  |
| `Handling` | Thuần hóa | · (kn 2) | · (kn 4) | 1 (kn 6) |  |
| `Cooking` | Nấu ăn | · (kn 1) | · (kn 7) | 1 (kn 8) |  |
| `Hunting` | Săn bắn | · (kn 7) | · (kn 1) | · (kn 3) | **KHÔNG AI LÀM** |
| `Construction` | Xây dựng | 1 (kn 4) | 3 (kn 4) | · (kn 2) |  |
| `Growing` | Trồng trọt | · (kn 4) | · (kn 3) | 1 (kn 10) |  |
| `Mining` | Khai thác | · (kn 1) | 2 (kn 3) | 3 (kn 3) |  |
| `PlantCutting` | Chặt cây | 2 (kn 4) | 2 (kn 3) | 3 (kn 10) |  |
| `Smithing` | Rèn | · (kn 0) | · (kn 2) | 3 (kn 4) |  |
| `Tailoring` | May mặc | · (kn 0) | · (kn 2) | 3 (kn 4) |  |
| `Art` | Nghệ thuật | 3 (kn 3) | 3 (kn 7) | · (kn 2) |  |
| `Crafting` | Chế tạo | · (kn 0) | · (kn 2) | 3 (kn 4) |  |
| `Hauling` | Khiêng vác | 3 | 2 | 3 |  |
| `Cleaning` | Dọn dẹp | 2 | 1 | 2 |  |
| `Research` | Nghiên cứu | · (kn 2) | 2 (kn 9) | 2 (kn 6) |  |
| `Childcare` | Chăm trẻ | · | · | · | **KHÔNG AI LÀM** |
| `DarkStudy` | Nghiên cứu hắc ám | · (kn 2) | 3 (kn 9) | 3 (kn 6) |  |
| `Fishing` | Câu cá | · (kn 2) | · (kn 4) | 2 (kn 6) |  |


## 5. Căn cứ

Tâm căn cứ (trung bình toạ độ tường/cửa của bạn): (129,143); bao tường: x 93–152, z 129–156. Tổng 276 công trình của bạn.


### 5.1 Sơ đồ căn cứ

```
 162 .............................................................................^
 161 .............................................................................^
 160 .............................................................................^
 159 .............................................................................^
 158 ..............................................................................
 157 ..............................................................................
 156 ..................................................###################.........
 155 ..................................................##___3#____B#____4#.........
 154 ..................................................##____#__o__#__o__#.........
 153 ..................................................##____#_____#_____#.........
 152 ..................................................#+____#__*__#_____#.........
 151 ..............................,,.............V....##____#_____#1____#.........
 150 ..............................,,,.................#####+#+#####+#####.........
 149 ..............................,,,,.................#________________#.........
 148 ...............................,,.....######+###############+########.........
 147 ......................................#___________B#________________#.........
 146 ......................................#_________o__#___R____________#.........
 145 :::::::::###############..............#____________#___c____*_______#.........
 144 :::::::::#ii::::iii::ii#..............#______*_____+________________#.........
 143 :::::::::#:ii:::ii::::i#..............#____________#________________#x........
 142 :::::::::#ii:ii:iii::::#..............#____________#________________#.........
 141 :::&:::::#iiiiii::i::::#,,,,,,,,,,,,,,######+########################x........
 140 :::&:::::#ii::iiiii::::#,,,,,,,,,,,,,,#____________#:::&:::::::::::&#.........
 139 .........#iiiiiiiiii:::#,,,,,,,,,,,,,,#__S___c_____#:&:&::::&::::&::#x........
 138 .........#iiiiii:ii:::i#,,,,,,,,,,,,,,#_cc___J_____#::::::::::::::::#.........
 137 .........#i:iiiiiii:::i#,,,,,,,,,,,,,,#Tc__*_c__c__#:::::::::::&::::#x........
 136 .........#i:iiiiii:::::#,,,,,,,,,,a,,,#_________K__+:::&:::::::&::::#.........
 135 .........#iii:i:ii::::i#,,,,,,,,,,,,,,######+####################xxx#x........
 134 .........#iiii:ii:::i::#.........................&............................
 133 .........#ii:ii::i:::::+......................................................
 132 .........#i:::i:i:ii:::#.......2..............................................
 131 .........#:i::i::i:i:::#......................................................
 130 .........#:::i::i::::i:#......................................................
 129 .........###############.........................%............................
 128 ....................................F............%............................
 127 ..........................i........J........%.................................
 126 ...................................................J.........V................
 125 ..............................................................................
 124 ..............................................................................
 123 ......................................................%.......................
     000000000000000011111111111111111111111111111111111111111111111111111111111111
     888888999999999900000000001111111111222222222233333333334444444444555555555566
     456789012345678901234567890123456789012345678901234567890123456789012345678901
```

Khung vẽ: x 84–161, z 123–162. BẮC ở trên (z lớn), ĐÔNG bên phải (x lớn). Số bên trái = z của hàng; 3 hàng số dưới cùng = x của cột (trăm/chục/đơn vị). Mỗi công trình chỉ vẽ tại ô gốc (pos); công trình nhiều ô (giường 1×2, bếp 3×1, bàn…) chiếm thêm ô bên cạnh. Ký tự trên cùng che ký tự dưới (người > động vật > bản vẽ > công trình > xác > vật phẩm > zone > nền).
Chú thích: `#` tường · `+` cửa · `B` giường · `*` đuốc/đèn · `F` lửa trại · `T` bàn ăn · `c` ghế · `S` bếp · `K` bàn mổ thịt · `R` bàn nghiên cứu · `J` đồ giải trí (cọc móng ngựa/bàn cờ) · `o` điểm thiền · `V` mạch nước nóng · `x` bản vẽ/khung chưa xây · `&` xác chết · `i` vật phẩm · `a` động vật · `%` phế tích/đồ cổ không phải của bạn · `,` ô ruộng trống · `:` ô kho trống · `^` vách đá tự nhiên · `_` sàn đã lát · `.` nền tự nhiên
Người: 1 = bac si (147,151) · 2 = eistein (115,132) · 3 = Helena (139,155) · 4 = Protein (151,155)


### 5.2 Phòng / vùng kín thuộc căn cứ

*Game không lưu danh sách phòng; công cụ tự loang tìm vùng bị tường/đá/cửa bao kín. Nhiệt độ lấy từ lưới nhiệt lưu trong save.*

| Phòng | Bao | Số ô | Có mái | Nhiệt độ | Sàn | Cửa tại | Bên trong |
|---|---|---|---|---|---|---|---|
| R1 | x 123–134, z 142–147 | 72 | 72/72 | 24.3°C | WoodPlankFloor×72 | (128,141), (128,148), (135,144) | TorchLamp×1; Bed×1; MeditationSpot×1; [giường (134,147): bac si]; bẩn ×6 |
| R2 | x 123–134, z 136–140 | 60 | 60/60 | 24.8°C | WoodPlankFloor×60 | (128,135), (128,141), (135,136) | Table1x2c×1; FueledStove×1; DiningChair×4; TorchLamp×1; ChessTable×1; TableButcher×1; Stool×2; bẩn ×6 |
| R3 | x 136–139, z 151–155 | 20 | 20/20 | 24.9°C | WoodPlankFloor×20 | (135,152), (139,150) | Bed×1; [giường bệnh (139,155): chưa gán]; đang ở trong: Helena |
| R4 | x 136–151, z 142–147 | 96 | 96/96 | 24.1°C | WoodPlankFloor×96 | (135,144), (144,148) | TorchLamp×1; DiningChair×1; SimpleResearchBench×1; bẩn ×2 |
| R5 | x 136–151, z 149–149 | 16 | 16/16 | 24.2°C | WoodPlankFloor×16 | (139,150), (141,150), (144,148), (147,150) | trống |
| R6 | x 141–145, z 151–155 | 25 | 25/25 | 24.1°C | WoodPlankFloor×25 | (141,150) | MeditationSpot×1; TorchLamp×1; Bed×1; [giường (145,155): eistein] |
| R7 | x 147–151, z 151–155 | 25 | 25/25 | 24.6°C | WoodPlankFloor×25 | (147,150) | MeditationSpot×1; Bed×1; [giường bệnh (151,155): chưa gán]; đang ở trong: bac si, Protein |
| R8 | x 94–106, z 130–144 | 195 | 192/195 | 23.0°C | WoodPlankFloor×195 | (107,133) | vật phẩm: Steel×781, RawRice×304, WoodLog×3131, MealSimple×7, MeleeWeapon_Knife×1, ComponentIndustrial×30, Silver×929, Apparel_Pants×1, Leather_Camel×23, Apparel_BasicShirt×1, Leather_Wolf×26, Gun_Revolver×1, MedicineIndustrial×15, Gun_Autopistol×1; zone: Vùng kho chứa 1 (195 ô); bẩn ×5 |

**Chỉ số phòng do chính game tính** (lấy từ sự kiện gần nhất có ghi kèm bối cảnh; ấn tượng/đẹp/sạch càng âm càng tệ): `Bedroom`: ấn tượng 40.7, đẹp -0.2, sạch -0.1 (lúc 12 Decembary 5500 09:13); `Room`: ấn tượng 11.4, đẹp -2.5, sạch -0.4 (lúc 14 Decembary 5500 01:52); `Kitchen`: ấn tượng -5.3, đẹp -1.6, sạch -2.7 (lúc 14 Decembary 5500 13:14)


### 5.3 Công trình của bạn

| Def | Vật liệu | SL | Vị trí | HP | Chi tiết |
|---|---|---|---|---|---|
| `Wall` | WoodLog | 239 | 239 cái trong x 93–152, z 129–156 | 147–195 |  |
| `Door` | WoodLog | 11 | 11 cái trong x 107–147, z 133–152 | 104 |  |
| `DiningChair` | WoodLog | 5 | (125,138), (132,137), (139,145), (129,139), (129,137) | 65 |  |
| `TorchLamp` | — | 4 | (127,137), (144,145), (129,144), (143,152) | 75 | (127,137): nhiên liệu 10.0 · (144,145): nhiên liệu 10.2 · (129,144): nhiên liệu 10.1 · (143,152): nhiên liệu 10.2 |
| `Bed` | WoodLog | 4 | (134,147), (151,155), (139,155), (145,155) | 91 | (134,147): gán cho: bac si · (151,155): gán cho: chưa ai, giường bệnh · (139,155): gán cho: chưa ai, giường bệnh · (145,155): gán cho: eistein |
| `MeditationSpot` | — | 3 | (132,146), (143,154), (149,154) | — | (132,146): gán cho: bac si · (143,154): gán cho: eistein · (149,154): gán cho: Protein |
| `HorseshoesPin` | WoodLog | 2 | (119,127), (135,126) | 25–49 |  |
| `Stool` | WoodLog | 2 | (124,137), (124,138) | 49 |  |
| `Campfire` | — | 1 | (120,128) | 80 | (120,128): nhiên liệu 0 |
| `ChessTable` | WoodLog | 1 | (129,138) | 65 |  |
| `Table1x2c` | WoodLog | 1 | (123,137) | 49 |  |
| `TableButcher` | WoodLog | 1 | (132,136) | 117 | (132,136): bill: ButcherCorpseFlesh (lặp mãi) |
| `FueledStove` | — | 1 | (125,139) | 180 | (125,139): bill: CookMealFineBulk (lặp mãi); CookMealSimpleBulk (làm đến khi có 10); CookMealSimpleBulk ×1, nhiên liệu 30.6 |
| `SimpleResearchBench` | WoodLog | 1 | (139,146) | 162 |  |


### 5.4 Công trình CHƯA xây (bản vẽ / khung)

| Loại | Sẽ xây | Ô | Vật liệu | Đặt lúc | Đã có trong khung |
|---|---|---|---|---|---|
| bản vẽ | `Cooler` | (149,135) | — | 13 Decembary 5500 14:48 (1.9 ngày trước) | — |
| bản vẽ | `Cooler` | (150,135) | — | 13 Decembary 5500 14:48 (1.9 ngày trước) | — |
| bản vẽ | `Cooler` | (151,135) | — | 13 Decembary 5500 14:48 (1.9 ngày trước) | — |
| bản vẽ | `WoodFiredGenerator` | (153,135) | — | 13 Decembary 5500 12:43 (2.0 ngày trước) | — |
| bản vẽ | `WoodFiredGenerator` | (153,137) | — | 13 Decembary 5500 12:46 (2.0 ngày trước) | — |
| bản vẽ | `WoodFiredGenerator` | (153,139) | — | 13 Decembary 5500 12:49 (2.0 ngày trước) | — |
| bản vẽ | `WoodFiredGenerator` | (153,141) | — | 13 Decembary 5500 12:53 (2.0 ngày trước) | — |
| khung (đang xây) | `WoodFiredGenerator` | (153,143) | — | 15 Decembary 5500 10:30 (2.9 giờ trước) | Steel×75, Steel×11 |


## 6. Kho & tài nguyên

| Def | Tên | Tổng | Nằm ở đâu | Ghi chú |
|---|---|---|---|---|
| `WoodLog` | Gỗ | 3329 | Vùng kho chứa 1: 3131, Growing zone 1: 167, ngoài zone: 31 |  |
| `Steel` | Thép | 933 | Vùng kho chứa 1: 781, ngoài zone: 152 |  |
| `Silver` | Bạc | 930 | Vùng kho chứa 1: 929, ngoài zone: 1 |  |
| `GravlitePanel` | Tấm Gravlite | 348 | ngoài zone: 348 |  |
| `RawRice` | Gạo sống | 304 | Vùng kho chứa 1: 304 |  |
| `ComponentIndustrial` | Linh kiện công nghiệp | 30 | Vùng kho chứa 1: 30 |  |
| `Leather_Wolf` | Leather Wolf | 26 | Vùng kho chứa 1: 26 |  |
| `Leather_Camel` | Leather Camel | 23 | Vùng kho chứa 1: 23 |  |
| `Luciferium` | Luciferium | 15 | trong sương mù: 15 | bị cấm ×15 tại (201,74) |
| `MedicineIndustrial` | Thuốc công nghiệp | 15 | Vùng kho chứa 1: 15 |  |
| `MealSimple` | Suất ăn đơn giản | 7 | Vùng kho chứa 1: 7 | ×7 hỏng sau ~1.17 ngày |
| `BiomutationPulser` | Máy tạo đột biến | 1 | trong sương mù: 1 | bị cấm ×1 tại (198,77) |
| `Apparel_BasicShirt` | Áo sơ mi cơ bản | 1 | Vùng kho chứa 1: 1 | Normal/Cloth |
| `Gun_Autopistol` | Súng ngắn tự động | 1 | Vùng kho chứa 1: 1 | Normal |
| `Apparel_Pants` | Quần | 1 | Vùng kho chứa 1: 1 | Normal/Synthread |
| `Gun_Revolver` | Súng lục ổ xoay | 1 | Vùng kho chứa 1: 1 | bị cấm ×1 tại (103,131); Normal |
| `MeleeWeapon_Knife` | Dao | 1 | Vùng kho chứa 1: 1 | Poor/Steel |

Trong túi thuộc địa viên (chưa tính ở bảng trên): `MedicineIndustrial`×3.

**Lương thực cho người** *(ước tính theo dinh dưỡng vanilla; đã gồm cả đồ ăn trong túi thuộc địa viên)*: `RawRice`×304 (=15.2), `MealSimple`×7 (=6.3) → tổng 21.5 dinh dưỡng nguyên trạng, 33.5 nếu nấu hết thành suất đơn giản; 4 người ăn cần 6.4/ngày → **≈ 3.4–5.2 ngày**.


### Vùng kho

| Zone | Bao | Ô đã dùng | Ô có mái | Ưu tiên | Cho phép | Cách tâm căn cứ | Đang chứa |
|---|---|---|---|---|---|---|---|
| Vùng kho chứa 1 | x 94–106, z 130–144 | 99/195 | 192/195 | Normal | 834 def | 30 ô Tây | WoodLog×3131, Silver×929, Steel×781, RawRice×304, ComponentIndustrial×30, Leather_Wolf×26, Leather_Camel×23, MedicineIndustrial×15, MealSimple×7, Apparel_BasicShirt×1 |
| Vùng kho chứa 2 | x 234–244, z 143–151 | 20/99 | 0/99 | Normal | 39 def (38 loại xác) | 110 ô Đông | Corpse_Human (đã khô)×5, Corpse_Mech_Pikeman (không phân hủy)×3, Corpse_Mech_Scyther (không phân hủy)×2, Corpse_Ibex (đã khô)×2, Corpse_Squirrel (đã khô)×2, Corpse_Rat (đã khô)×2, Corpse_Sparrow (đã khô)×1, Corpse_Mink (đã khô)×1, Corpse_Tortoise (đã khô)×1, Corpse_Human (tươi)×1 |
| Stockpile zone 1 | x 136–151, z 136–140 | 9/80 | 80/80 | Normal | 115 def (115 loại xác); cấm: AllowRotten | 15 ô Đông | Corpse_Horse (đã khô)×2, Corpse_Hare (đã khô)×2, Corpse_Warg (đã khô)×1, Corpse_Tortoise (đã khô)×1, Corpse_Squirrel (đã khô)×1, Corpse_Rat (đã khô)×1, Corpse_Donkey (đã khô)×1 |
| Dumping stockpile zone 1 | x 84–92, z 140–145 | 2/54 | 0/54 | Normal | 153 def (152 loại xác); cấm: AllowCorpsesColonist, AllowCorpsesStranger, AllowCorpsesSlave, AllowCorpsesUnnatural | 41 ô Tây | Corpse_Horse (đã khô)×2 |


## 7. Trồng trọt

| Ruộng | Cây đặt trồng | Số ô | Bao | Số cây trồng hiện có | Độ lớn | Cây dại mọc lẫn | Đất | Cho phép | Cách tâm căn cứ |
|---|---|---|---|---|---|---|---|---|---|
| Vùng trồng trọt 1 | `Plant_Rice` | 98 | x 108–121, z 135–141 | **0** | — | Plant_Grass×11, Plant_TreeOak×5, Plant_TallGrass×2, Plant_Brambles×1 | Soil×98 | gieo: có, cắt: có | 16 ô Tây |
| Vùng trồng trọt 2 | `Plant_Rice` | 11 | x 114–117, z 148–151 | **0** | — | Plant_Grass×2 | SoilRich×11 | gieo: có, cắt: có | 15 ô Tây Bắc |
| Growing zone 1 | `Plant_Healroot` | 83 | x 131–145, z 174–188 | **15** | 36%–37% (TB 36%), chín: 0 | Plant_Grass×11, Plant_TreeOak×6, Plant_TallGrass×3, Plant_Brambles×2 | SoilRich×83 | gieo: có, cắt: có | 39 ô Bắc |
| Growing zone 2 | `Plant_Healroot` | 15 | x 131–138, z 172–176 | **0** | — | Plant_Grass×3, Plant_Dandelion×1, Plant_TallGrass×1 | SoilRich×15 | gieo: có, cắt: có | 31 ô Bắc |

Thực vật hoang trên map: 21,800 cây, trong đó 9,931 cây gỗ, `Plant_Berry`×75, `Plant_TreeAnima`×1, `Plant_HealrootWild`×80.


## 8. Việc đã đánh dấu (designations)

| Lệnh | Mục tiêu | SL | Phạm vi | Gần căn cứ nhất | Thuộc việc |
|---|---|---|---|---|---|
| CutPlant | `Plant_TreeOak` | 36 | x 94–152, z 123–150 | (131,132) (11 ô Nam) | PlantCutting |
| CutPlant | `Plant_Grass` | 35 | x 96–152, z 123–154 | (134,134) (10 ô Đông Nam) | PlantCutting |
| CutPlant | `Plant_TallGrass` | 15 | x 92–139, z 125–150 | (129,134) (9 ô Nam) | PlantCutting |
| CutPlant | `Plant_Dandelion` | 5 | x 130–151, z 126–134 | (130,134) (9 ô Nam) | PlantCutting |
| CutPlant | `Plant_Bush` | 5 | x 123–142, z 123–131 | (127,131) (12 ô Nam) | PlantCutting |
| CutPlant | `Plant_Brambles` | 4 | x 98–144, z 123–154 | (138,126) (19 ô Đông Nam) | PlantCutting |
| CutPlant | `Plant_TreePoplar` | 3 | x 131–149, z 123–125 | (131,125) (18 ô Nam) | PlantCutting |
| CutPlant | `Plant_Berry` | 1 | x 131–131, z 130–130 | (131,130) (13 ô Nam) | PlantCutting |
| Deconstruct | `Wall` | 6 | x 135–135, z 150–156 | (135,150) (9 ô Đông Bắc) | Construction |
| Deconstruct | `Door` | 1 | x 135–135, z 152–152 | (135,152) (11 ô Đông Bắc) | Construction |
| HarvestPlant | `Plant_TreeOak` | 99 | x 83–162, z 126–162 | (126,134) (9 ô Nam) | PlantCutting |
| HarvestPlant | `Plant_TreePoplar` | 23 | x 105–162, z 127–159 | (120,148) (10 ô Tây Bắc) | PlantCutting |
| HarvestPlant | `SmashedStump` | 1 | x 141–141, z 128–128 | (141,128) (19 ô Đông Nam) | PlantCutting |
| Hunt | `Quail` | 6 | x 79–249, z 21–32 | (79,24) (129 ô Tây Nam) | Hunting |
| Hunt | `WildBoar` | 5 | x 108–117, z 75–79 | (111,79) (66 ô Nam) | Hunting |
| Hunt | `Alpaca` | 3 | x 212–217, z 231–237 | (212,231) (121 ô Đông Bắc) | Hunting |
| Hunt | `Boomrat` | 3 | x 49–229, z 46–107 | (209,107) (88 ô Đông Nam) | Hunting |
| Hunt | `Ibex` | 2 | x 189–189, z 232–235 | (189,232) (107 ô Đông Bắc) | Hunting |
| Hunt | `Hare` | 2 | x 58–179, z 151–235 | (179,151) (51 ô Đông) | Hunting |
| Hunt | `Squirrel` | 2 | x 151–159, z 190–236 | (159,190) (56 ô Đông Bắc) | Hunting |
| Hunt | `Turkey` | 1 | x 194–194, z 117–117 | (194,117) (70 ô Đông) | Hunting |
| Hunt | `Raccoon` | 1 | x 241–241, z 14–14 | (241,14) (171 ô Đông Nam) | Hunting |
| Hunt | `Bluebird` | 1 | x 149–149, z 27–27 | (149,27) (118 ô Nam) | Hunting |
| MineVein | `MineableSteel` | 9 | x 168–171, z 191–194 | (169,191) (62 ô Đông Bắc) | Mining |


## 9. Mối đe doạ & địa điểm đáng chú ý trên map


### Nhóm pawn do AI điều khiển (lord)

| Lord | Phe | Quan hệ | Kiểu hành vi | Tham số | Thành viên | Cách căn cứ |
|---|---|---|---|---|---|---|
| Lord_0 | bầy cỗ máy chiến đấu cơ (Mechanoid) | Hostile | `LordJob_SleepThenAssaultColony` | faction=Faction_8, wakeOnPawnUnfogged=True | Mech_Militor (205,67); Mech_Scorcher (198,66); Mech_Militor (201,74) | 107 ô Đông Nam |

| Mech | Ô | Phe | Trạng thái | Trong sương mù | Cách căn cứ |
|---|---|---|---|---|---|
| `Mech_Militor` | (205,67) | bầy cỗ máy chiến đấu cơ (Mechanoid) | ngủ đông (dormant), job `LayDown`, duty `SleepForever` | có | 107 ô Đông Nam |
| `Mech_Scorcher` | (198,66) | bầy cỗ máy chiến đấu cơ (Mechanoid) | ngủ đông (dormant), job `LayDown`, duty `SleepForever` | có | 103 ô Đông Nam |
| `Mech_Militor` | (201,74) | bầy cỗ máy chiến đấu cơ (Mechanoid) | ngủ đông (dormant), job `LayDown`, duty `SleepForever` | có | 100 ô Đông Nam |


### Vùng kín khác trên map (phế tích, hầm cổ…)

| Phòng | Bao | Số ô | Có mái | Nhiệt độ | Sàn | Cửa tại | Bên trong | Cách căn cứ |
|---|---|---|---|---|---|---|---|---|
| R9 | x 191–205, z 63–80 | 204 | 204/204 | 22.3°C | TileMarble×142, AncientTile×50, AncientConcrete×12 | — | **TOÀN BỘ TRONG SƯƠNG MÙ — người chơi chưa nhìn thấy bên trong**; AncientBarrel×1 (không phải của bạn); SteleLarge×3 (không phải của bạn); AncientCryptosleepCasket×6 (không phải của bạn); Sarcophagus×1 (không phải của bạn); Table2x2c×1 (không phải của bạn); AncientHermeticCrate×1 (không phải của bạn); AncientCryptosleepCasket@(202,71) chứa Human «Sarah “Four Eyes” Renault» [AncientSoldier, 21.5 tuổi, phe Người cổ đại (Ancients), quan hệ Neutral, vũ khí Gun_Incinerator]; AncientCryptosleepCasket@(196,67) chứa Human «Beryl “Zamora” Zamora» [AncientSoldier, 45.1 tuổi, phe Người cổ đại (AncientsHostile), quan hệ Hostile, vũ khí Gun_EmpLauncher]; AncientCryptosleepCasket@(196,73) chứa Human «Amaya “Lover” Farrell» [AncientSoldier, 88.6 tuổi, phe Người cổ đại (Ancients), quan hệ Neutral, vũ khí Gun_HeavySMG]; AncientCryptosleepCasket@(193,67) chứa xác Manuel “Lutz” Lutz; AncientCryptosleepCasket@(199,71) chứa Human «Rachel “Melton” Melton» [AncientSoldier, 41.2 tuổi, phe Người cổ đại (Ancients), quan hệ Neutral, vũ khí Gun_MachinePistol]; AncientCryptosleepCasket@(199,67) chứa Human «Andreas “Lauv” Lauvhjell» [AncientSoldier, 53.8 tuổi, phe Người cổ đại (Ancients), quan hệ Neutral, vũ khí Gun_HellcatRifle]; Megascarab [không phe] ×3; AncientHermeticCrate@(203,69) chứa Techprint_SkinHardening; vật phẩm: BiomutationPulser×1, Luciferium×15; đang ở trong: Mech_Scorcher, Mech_Militor, Mech_Militor | 100 ô Đông Nam |


### Công trình không phải của bạn

| Def | SL | Vị trí | Gần căn cứ nhất | Trong sương mù | Chi tiết |
|---|---|---|---|---|---|
| `Wall` | 186 | x 101–232, z 24–199 | (105,119) (34 ô Tây Nam) | 23/186 |  |
| `Door` | 10 | x 103–232, z 26–194 | (103,119) (35 ô Tây Nam) |  |  |
| `Column` | 9 | x 157–227, z 25–197 | (157,197) (61 ô Đông Bắc) |  |  |
| `AncientCryptosleepCasket` | 6 | (199,67), (196,67), (199,71), (196,73), (202,71), (193,67) | (196,73) (97 ô Đông Nam) | 6/6 | (199,67) chứa Human «Andreas “Lauv” Lauvhjell» [AncientSoldier, 53.8 tuổi, phe Người cổ đại (Ancients), quan hệ Neutral, vũ khí Gun_HellcatRifle]; Megascarab [không phe] ×3; (196,67) chứa Human «Beryl “Zamora” Zamora» [AncientSoldier, 45.1 tuổi, phe Người cổ đại (AncientsHostile), quan hệ Hostile, vũ khí Gun_EmpLauncher]; (199,71) chứa Human «Rachel “Melton” Melton» [AncientSoldier, 41.2 tuổi, phe Người cổ đại (Ancients), quan hệ Neutral, vũ khí Gun_MachinePistol]; (196,73) chứa Human «Amaya “Lover” Farrell» [AncientSoldier, 88.6 tuổi, phe Người cổ đại (Ancients), quan hệ Neutral, vũ khí Gun_HeavySMG]; (202,71) chứa Human «Sarah “Four Eyes” Renault» [AncientSoldier, 21.5 tuổi, phe Người cổ đại (Ancients), quan hệ Neutral, vũ khí Gun_Incinerator]; (193,67) chứa xác Manuel “Lutz” Lutz |
| `ShipChunk_Mech` | 6 | (232,2), (212,3), (221,16), (231,10), (214,8), (225,17) | (221,16) (157 ô Đông Nam) |  |  |
| `SteamGeyser` | 5 | (129,151), (132,78), (102,48), (145,126), (62,128) | (129,151) (8 ô Bắc) |  |  |
| `Sarcophagus` | 3 | (196,76), (231,47), (231,44) | (196,76) (95 ô Đông Nam) | 1/3 |  |
| `SteleLarge` | 3 | (202,75), (202,67), (198,75) | (198,75) (97 ô Đông Nam) | 3/3 |  |
| `ShipChunk` | 3 | (129,213), (135,165), (47,208) | (135,165) (23 ô Bắc) |  |  |
| `AncientShipBeacon` | 2 | (56,31), (65,31) | (65,31) (129 ô Tây Nam) |  |  |
| `GravEngine` | 1 | (230,13) | (230,13) (165 ô Đông Nam) |  | gravshipName=tàu hấp dẫn |
| `VoidMonolith` | 1 | (43,114) | (43,114) (91 ô Tây) |  | progress=0; studyEnabled=False |
| `AncientMechDropBeacon` | 1 | (80,76) | (80,76) (83 ô Tây Nam) |  |  |
| `AncientHermeticCrate` | 1 | (203,69) | (203,69) (105 ô Đông Nam) | 1/1 | (203,69) chứa Techprint_SkinHardening |
| `Table2x2c` | 1 | (203,72) | (203,72) (103 ô Đông Nam) | 1/1 |  |

Đồ cổ/phế tích khác (trang trí, không chứa gì): `AncientConcreteBarrier`×41 (gần nhất (138,113)), `AncientFence`×23 (gần nhất (120,73)), `AncientWheel`×12 (gần nhất (133,129)), `AncientRazorWire`×12 (gần nhất (61,201)), `AncientGiantWheel`×11 (gần nhất (65,63)), `AncientLamppost`×9 (gần nhất (147,111)), `AncientRustedCar`×3 (gần nhất (128,119)), `AncientExostriderLeg`×3 (gần nhất (195,197)), `AncientRustedEngineBlock`×2 (gần nhất (131,112)), `AncientSmallCrate`×2 (gần nhất (212,34)), `AncientPipelineSection`×2 (gần nhất (31,103)), `AncientOperatingTable`×2 (gần nhất (214,29)), `AncientRustedCarFrame`×2 (gần nhất (138,123)), `AncientPodCar`×2 (gần nhất (128,127)), `AncientMiniWarwalkerRemains`×1 (gần nhất (85,38)), `AncientBarrel`×1 (gần nhất (202,77)), `AncientRefrigerator`×1 (gần nhất (211,32)), `AncientExostriderHead`×1 (gần nhất (201,197)), `AncientGenerator`×1 (gần nhất (164,35)), `AncientExostriderCannon`×1 (gần nhất (198,199)), `AncientExostriderRemains`×1 (gần nhất (199,197)).

**Anomaly:** cấp `Inactive` · monolith `Thing_VoidMonolith36663` · kiến thức từ monolith 0.


## 10. Động vật

50 con trên map, trong đó 0 con đã thuần của bạn.

| Loài (hoang) | SL | Con gần căn cứ nhất | Trạng thái con đó | Ghi chú |
|---|---|---|---|---|
| `Alpaca` | 7 | (212,231) (121 ô Đông Bắc) | thức ăn 0.66, job Wait_Wander | đã đánh dấu săn ×3; 3 con có thương tật |
| `Quail` | 6 | (79,24) (129 ô Tây Nam) | thức ăn 0.19, job GotoWander | đã đánh dấu săn ×6 |
| `Raccoon` | 6 | (118,136) (13 ô Tây Nam) | thức ăn 0.30, job Goto | đã đánh dấu săn ×1; 2 con `ManhunterPermanent`; 2 con có thương tật |
| `Crow` | 6 | (107,164) (30 ô Tây Bắc) | thức ăn 0.05, job Wait_MaintainPosture | 1 con có thương tật |
| `WildBoar` | 5 | (111,79) (66 ô Nam) | thức ăn 0.71, job Wait_Wander | đã đánh dấu săn ×5; 1 con có thương tật |
| `Hare` | 3 | (179,151) (51 ô Đông) | thức ăn 0.19, job GotoWander | đã đánh dấu săn ×2 |
| `Boomrat` | 3 | (209,107) (88 ô Đông Nam) | thức ăn 0.14, job Wait_Wander | đã đánh dấu săn ×3 |
| `Turkey` | 2 | (194,117) (70 ô Đông) | thức ăn 0.47, job Wait_Wander | đã đánh dấu săn ×1; 1 con có thương tật |
| `Megasloth` | 2 | (112,242) (100 ô Bắc) | thức ăn 1.86, job GotoWander |  |
| `Rhinoceros` | 2 | (18,25) (162 ô Tây Nam) | thức ăn 1.55, job Wait_MaintainPosture |  |
| `Squirrel` | 2 | (159,190) (56 ô Đông Bắc) | thức ăn 0.15, job GotoWander | đã đánh dấu săn ×2 |
| `Ibex` | 2 | (189,232) (107 ô Đông Bắc) | thức ăn 0.68, job Wait_Wander | đã đánh dấu săn ×2 |
| `Wolf_Timber` | 1 | (124,107) (36 ô Nam) | thức ăn 0.82, job Wait_Wander | THÚ SĂN MỒI |
| `Porcupine` | 1 | (248,163) (121 ô Đông) | thức ăn 0.28, job Wait_Wander |  |
| `Bluebird` | 1 | (149,27) (118 ô Nam) | thức ăn 0.11, job GotoWander | đã đánh dấu săn ×1 |
| `Bear_Grizzly` | 1 | (48,83) (101 ô Tây Nam) | thức ăn 1.85, job GotoWander | THÚ SĂN MỒI |

*«thức ăn» = mức dinh dưỡng đang có trong bụng (đơn vị dinh dưỡng; mức tối đa tuỳ kích cỡ loài, người = 1.0).*


## 11. Bản đồ

| Thuộc tính | Giá trị |
|---|---|
| Kích thước | 250 × 250 ô |
| Địa hình (số ô) | `Soil` 40,906, `Gravel` 6,391, `Marble_Rough` 5,162, `Granite_Rough` 2,792, `SoilRich` 2,219, `WaterShallow` 1,757, `Mud` 1,458, `BrokenAsphalt` 634, `WoodPlankFloor` 615, `AncientConcrete` 208, `TileMarble` 150, `FlagstoneGranite` 76, `TileSandstone` 72, `AncientTile` 50, `TileLimestone` 10 |
| Mái | `RoofRockThin` 1,769 (mái đá mỏng), `RoofConstructed` 1,022 (mái xây), `RoofRockThick` 806 (mái núi dày (không phá được)) |
| Vách đá / quặng / đá vụn (lớp nén) | `Marble` 2,074, `Granite` 998, `ChunkGranite` 726, `ChunkMarble` 654, `MineableSteel` 334, `MineableComponentsIndustrial` 44, `MineableSilver` 17, `MineableJade` 16, `ChunkSlagSteel` 6 |
| Sương mù | 2,878 ô chưa khám phá (4.6%) |
| Ô nhiễm / tuyết | 0 ô ô nhiễm; tuyết: không |
| Khí đang lơ lửng | không có (lưới khí toàn 0) |
| Tài nguyên sâu đã dò ra (cho khoan sâu) | chưa có (chưa quét bằng máy quét sâu, hoặc không có gì) |
| Khu vực (area) | Area_Home 2641 ô [x 80–248, z 123–192], Area_BuildRoof 808 ô [x 93–152, z 129–156], Area_NoRoof 126 ô [x 122–135, z 148–156], Area_SnowOrSandClear 0 ô, Area_PollutionClear 0 ô, Khu vực 1 0 ô |
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
 185 .......,",".................z...^??????^......='??
 180 ...,,",~~,"...............zz,...'^???^^'"....=='$?
 175 .~~~~~,,~,,...............zz....'^???^'"""..==..^^
 170 .~~~~~~,"..................z...'^$??^."""".==.'.''
 165 .~~~~~~,"......................^^??^""""""==..'...
 160 .~~~~~~,.......................'??^'.""""==.......
 155 .~~~~~~,..................BBBBB.^^'.....==........
 150 .",~~~,.....^^........zz.SBBBBB..'.....==......z..
 145 ...~~~.....'^'^'.zBBBBzzBBBBBBB.......==.......zz.
 140 ...~~.".,...''^..zB_zB..BBBBBBB......==...........
 135 ...,..",,.........Bz_BzzBBBBBBB.....==............
 130 ..."..............Bz_B.............==.............
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
  70 ...............................^???????K!...~~~...
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
| `MineableSteel` * | 105 | x 168–185, z 189–199 | (177,193) | 69 ô Đông Bắc | một phần | 9 |
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
| Dumping stockpile zone 1 | đã khô | 2 | Corpse_Horse×2 | x 87–87, z 140–141 | 42 ô Tây |  |
| Stockpile zone 1 | đã khô | 9 | Corpse_Warg×1, Corpse_Horse×2, Corpse_Hare×2, Corpse_Tortoise×1, Corpse_Squirrel×1, Corpse_Rat×1, Corpse_Donkey×1 | x 137–151, z 136–140 | 12 ô Đông Nam |  |
| Vùng kho chứa 2 | đã khô | 14 | Corpse_Sparrow×1, Corpse_Ibex×2, Corpse_Human×5, Corpse_Squirrel×2, Corpse_Mink×1, Corpse_Rat×2, Corpse_Tortoise×1 | x 234–243, z 143–149 | 112 ô Đông | Diana “Diana” Stokes (Khí độc đàn ông (PirateWaster), chết 5 Decembary 5500); Azskar “Gray” akman (Khí độc đàn ông (PirateWaster), chết 11 Septober 5500); Nikolay “Reks” Reks (—, chết 5 Septober 5498); Oshul wttytt (—, chết 1 Decembary 5498); Buxdun aksmoke (Khí độc đàn ông (PirateWaster), chết 3 Decembary 5500) |
| Vùng kho chứa 2 | tươi | 1 | Corpse_Human×1 | x 238–238, z 147–147 | 109 ô Đông | Jarod “Elphy” Elphinstone (Khí độc đàn ông (PirateWaster), chết 13 Decembary 5500) |
| Vùng kho chứa 2 | không phân hủy | 5 | Corpse_Mech_Scyther×2, Corpse_Mech_Pikeman×3 | x 235–241, z 146–149 | 108 ô Đông |  |
| ngoài zone | đã khô | 3 | Corpse_Horse×1, Corpse_Ibex×2 | x 47–235, z 30–68 | 118 ô Nam |  |
| ngoài zone | tươi | 3 | Corpse_Rat×1, Corpse_Lynx×1, Corpse_WildBoar×1 | x 39–133, z 76–134 | 10 ô Đông Nam |  |
| ngoài zone | không phân hủy | 3 | Corpse_Mech_Pikeman×3 | x 213–232, z 1–2 | 174 ô Đông Nam |  |

*Xác tươi (<2,5 ngày ở ≥10°C) → thối rữa (toả khí gây LungRot, 2,5–5 ngày) → khô. Xác mech không phân hủy.*


## 13. Nghiên cứu

**Đang chọn:** `Batteries` — đã tích luỹ 0 điểm. **Đã xong (7):** `ComplexFurniture`, `PassiveCooler`, `Stonecutting`, `ComplexClothing`, `Electricity`, `NutrientPaste`, `AirConditioning`. Còn 116 dự án chưa đụng tới.

*Save chỉ lưu số điểm, không lưu chi phí hay cờ hoàn thành. Dự án có điểm là số nguyên tròn (game gán = chi phí khi xong) được coi là đã xong — suy luận, độ tin cậy cao.*


## 14. Nhiệm vụ


### «Shoytt's Sad Survivors» — CHƯA NHẬN (đang chờ quyết định)

| Thuộc tính | Giá trị |
|---|---|
| Loại (root) | `Hospitality_Refugee` · từ thiện |
| Xuất hiện | 14 Decembary 5500 06:24 (tick 1381000) |
| Hạn nhận | 5 Aprimay 5501 06:30 — còn **4.7 ngày** |
| Mô tả | A group of 3 desperate refugees are approaching consisting of Shoytt and 2 children he has taken under his wing. They say their caravan was ambushed and everything was taken. Shoytt begs you for permission to stay at nhung nguoi cung kho for 10 days so they can rest and regroup. In return, they offer to work and fight for free during that time. If you make them happy, some of them may offer to join you. They may also reward you later for helping them - but there is no way to know their true intentions. These refugees are not part of any faction. If you wish, you can choose to kill, arrest, sell, or harvest them, without diplomatic consequences. |
| Phần thưởng | VisitorsHelp; PossibleFutureReward |
| Mốc thời gian trong nhiệm vụ | BetrayalOffer (3.0 days): 3.0 ngày; Guests depart in …: 10.0 ngày |
| Nhân vật liên quan | Shoytt Barytt (Male, 49.1 tuổi, `Refugee`, Andeduay (OutlanderRefugee), đang ở ngoài map; quest tag: Quest5.lodgers; **là `Spouse` của Helena (khách đang ở trên map)**); Sadako “Sadako” Morris (Female, 7.0 tuổi, `Refugee`, Andeduay (OutlanderRefugee), đang ở ngoài map; quest tag: Quest5.lodgers); Pwuug Squag (Male, 5.0 tuổi, `Refugee`, Andeduay (OutlanderRefugee), đang ở ngoài map; quest tag: Quest5.lodgers); Petronella ere pus kio (Female, 41.5 tuổi, `Empire_Royal_Stellarch`, Đế chế tan nát (Empire), đang ở ngoài map) |
| Phe liên quan | Andeduay (OutlanderRefugee), Đế chế tan nát (Empire) |
| Thành công khi (tín hiệu) | LastLodger_Recruited, LastLodger_LeftMapAllNotHealthy |
| Thất bại khi (tín hiệu) | LodgerDestroyed, LastLodger_Destroyed, LodgerArrested, LastLodger_Arrested, LodgerLeftBehind, LastLodger_LeftBehind, LodgerSurgeryViolation, LodgerPsychicRitualTarget, LastLodger_Kidnapped, LastLodger_Banished |


### «The Hard Prisoner» — CHƯA NHẬN (đang chờ quyết định)

| Thuộc tính | Giá trị |
|---|---|
| Loại (root) | `Hospitality_Prisoners` |
| Xuất hiện | 11 Decembary 5500 06:24 (tick 1201000) |
| Hạn nhận | 2 Aprimay 5501 06:50 — còn **1.7 ngày** |
| Độ khó | 1 sao |
| Mô tả | Basilos Dalassos, a novice of Đế chế tan nát has been caught in bed with the wrong person. He imprisoned the inappropriate lover in a show of rejection. Now he wants you to keep the prisoner Rebecca Mercer caged until the scandal blows over in 24 days. |
| Phần thưởng (chọn 1) | RoyalFavor +6 [Đế chế tan nát (Empire)] **HOẶC** Vật phẩm: Novel (Legendary) «Force», Gold ×20 **HOẶC** Goodwill +20 [Đế chế tan nát (Empire)] |
| Mốc thời gian trong nhiệm vụ | Shuttle arrives in …: 24.0 ngày |
| Nhân vật liên quan | Rebecca “Mercer” Mercer (Female, 48.1 tuổi, `SpaceRefugee_Clothed`, —, đang ở ngoài map; quest tag: Quest3.lodgers) |
| Phe liên quan | Đế chế tan nát (Empire) |


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
| «RefugeePodCrash» | `RefugeePodCrash` | đã kết thúc: thành công | 12 Decembary 5500 16:00 | liên quan: Helena Arianites (đang ở trên map) |


## 15. Phe phái

| ID | Tên | Loại | Quan hệ với bạn | Thiện chí | Số khu định cư | Thủ lĩnh | Ghi chú |
|---|---|---|---|---|---|---|---|
| Faction_18 | Andeduay | `OutlanderRefugee` | Neutral | 100 | 0 | Shoytt Barytt | ẩn, tạm thời |
| Faction_0 | Orussia | `OutlanderCivil` | Neutral | 0 | 36 | Elvira “Elvira” Arellano |  |
| Faction_2 | Camro dân tộc | `TribeCivil` | Neutral | 0 | 30 | Cự đà combo |  |
| Faction_7 | Đế chế tan nát | `Empire` | Neutral | 0 | 33 | Petronella ere pus kio |  |
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

**Điểm đặc biệt trên bản đồ thế giới:** `Settlement` «nhung nguoi cung kho» tại ô thế giới 162296,0 (khu định cư của bạn); `EscapeShip` tại ô thế giới 286441,0 [Quest2.escapeShip]; `SpaceSettlement`×9 (phe: Công ty thương gia (TradersGuild)); `AsteroidBasic`×12 (tài nguyên quý: MineablePlasteel×4, MineableSteel×3, MineableSilver×2, MineableComponentsIndustrial×1, MineableJade×1, MineableGold×1).

**Tàu vận chuyển đang được game theo dõi:** `Shuttle` (Đế chế tan nát (Empire)) [Quest3.dropoffShipThing]; `Shuttle` (—) [Quest3.pickupShipThing].


## 16. Dòng thời gian


### Thư (mọi thư từ đầu ván) và thông báo trong 5 ngày gần nhất

| Lúc | Cách đây (ngày) | Loại | Mức | Tiêu đề | Nội dung |
|---|---|---|---|---|---|
| 8 Septober 5500 18:00 | 21.8 | THƯ | NeutralEvent | Khách tham quan | Một Công chức từ Orussia đang tiến vào thuộc địa. Anh ta được đặt tên Kellan 'Kel' Cotter. Anh ta dường như có một vài mặt hàng để giao dịch. |
| 9 Septober 5500 15:35 | 20.9 | THƯ | ThreatSmall | Chồn bị điên | Một chồn gần đó đã phát điên. Nó sẽ tấn công tất cả mọi người mà nó nhìn thấy. |
| 11 Septober 5500 15:35 | 18.9 | THƯ | ThreatBig | Đột kích: Khí độc đàn ông | Một nhóm wasters từ Khí độc đàn ông đã đến gần đó. Họ đang tấn công ngay lập tức. |
| 11 Septober 5500 16:22 | 18.9 | THƯ | Death | Đã chết: Beelzebub (chuột cái) | Beelzebub bị chém chết. |
| 12 Septober 5500 06:24 | 18.3 | THƯ | NewQuest | Nhiệm vụ khả dụng: Tín hiệu cơ học | Có nhiệm vụ mới. Nhiệm vụ có tên 'Tín hiệu cơ học'. |
| 12 Septober 5500 08:15 | 18.2 | THƯ | PositiveEvent | Động cơ trọng lực | Con tàu cơ khí đã hạ cánh gần đó. Nó chứa một động cơ trọng lực đang hoạt động. Động cơ chống lại trọng lực và tạo ra một trường lực nâng xung quanh nó, cho phép nó nâng các con tàu hoặc bệ lớn. Mặc dù nó không hoạt động khi ở xa một hành… |
| 14 Septober 5500 06:00 | 16.3 | THƯ | NewQuest | Nhiệm vụ khả dụng: Chạy trốn phu nhân | Có nhiệm vụ mới. Nhiệm vụ có tên 'Chạy trốn phu nhân'. Nếu bạn không chấp nhận nhiệm vụ trong 2 ngày, nó sẽ hết thời hạn. |
| 14 Septober 5500 16:00 | 15.9 | THƯ | PositiveEvent | Thrumbos quý hiếm | Một đàn nhỏ của thrumbos đã lang thang vào khu vực. Hòa bình tự nhiên, những sinh vật quý hiếm này cực kỳ nguy hiểm khi đối đầu. Một số thương nhân sẵn sàng trả nhiều tiền cho da và sừng quý giá của họ. Thrumbos sẽ rời khỏi khu vực trong m… |
| 14 Septober 5500 16:54 | 15.9 | THƯ | PositiveEvent | Monolith bị sụp đổ | Bac si đã phát hiện một monolith cổ đại bị chôn vùi một phần gần đây. Nếu điều tra nó, bạn có thể tìm hiểu thêm. |
| 15 Septober 5500 04:00 | 15.4 | THƯ | PositiveEvent | Chuột đực tự thuần hóa | Một chuột đực đã trở nên thuần hóa. Nó hiện được chỉ định Chuột đực 1. |
| 2 Decembary 5500 12:24 | 13.0 | THƯ | NeutralEvent | Khách tham quan | Một Diễn viên từ Orussia đang tiến vào thuộc địa. Anh ta được đặt tên Masaru Maldonado. Anh ta dường như có một vài mặt hàng để giao dịch. |
| 3 Decembary 5500 04:24 | 12.4 | THƯ | ThreatBig | Đột kích: Khí độc đàn ông | Một nhóm wasters từ Khí độc đàn ông đã đến gần đó. Họ đang tấn công ngay lập tức. |
| 3 Decembary 5500 17:36 | 11.8 | THƯ | ThreatSmall | Chuột cái bị điên | Một chuột cái gần đó đã phát điên. Nó sẽ tấn công tất cả mọi người mà nó nhìn thấy. |
| 4 Decembary 5500 14:50 | 10.9 | THƯ | NeutralEvent | Ám ảnh kinh hoàng | Protein mộng thấy một cơn ác mộng kỳ lạ. Trong mơ, anh ta nhìn thấy một hình khối đen trải dài trong không gian và thời gian, phát triển và tiêu thụ. Hình khối bắt nguồn từ một monolith sụp đổ gần đó. Sau khi tỉnh giấc, Protein bị cuốn hút… |
| 4 Decembary 5500 14:58 | 10.9 | THƯ | ThreatBig | Phế tích nguy hiểm | Khi eistein tiến gần đến bức tường cổ đại, anh ấy bỗng cảm thấy nỗi sợ hãi chạy dọc khắp cơ thể mình. Anh ta không biết tại sao nhưng anh ta cảm thấy công trình cổ đại kia có thể ẩn chứa nhiều nguy hiểm trong đó. |
| 5 Decembary 5500 02:00 | 10.5 | THƯ | ThreatBig | Raid: Khí độc đàn ông | A group of wasters have arrived from nearby. They are attacking immediately. |
| 7 Decembary 5500 07:00 | 8.3 | THƯ | ThreatBig | Warg hunting eistein | A warg is hunting eistein for food! |
| 7 Decembary 5500 08:13 | 8.2 | THƯ | ThreatBig | Warg hunting bac si | A warg is hunting bac si for food! |
| 7 Decembary 5500 08:47 | 8.2 | THƯ | ThreatSmall | Warg revenge | A warg is attacking after being harmed! It will hunt any humanoid it can reach. It will calm down when it goes to sleep. |
| 9 Decembary 5500 20:48 | 5.7 | THƯ | PositiveEvent | Cargo pods | You have detected a cluster of cargo pods crashing nearby. Perhaps you'll find something useful in the wreckage. |
| 10 Decembary 5500 06:46 | 5.3 | THƯ | ThreatBig | Timber wolf hunting eistein | A timber wolf is hunting eistein for food! |
| 10 Decembary 5500 07:00 | 5.3 | THƯ | ThreatSmall | Timber wolf revenge | A timber wolf is attacking after being harmed! It will hunt any humanoid it can reach. It will calm down when it goes to sleep. |
| 10 Decembary 5500 19:00 | 4.8 | thông báo | NegativeEvent |  | Eistein failed while constructing a wooden dining chair. Some resources have been wasted. |
| 11 Decembary 5500 00:15 | 4.6 | THƯ | NegativeEvent | Food binge: Eistein | Eistein is pigging out on food. This happened because of: Smokeleaf dependence (withdrawal 81%). |
| 11 Decembary 5500 04:32 | 4.4 | thông báo | PositiveEvent |  | Eistein, Barkeep is fully healed. |
| 11 Decembary 5500 06:00 | 4.3 | THƯ | NewQuest | Quest active: Ship to the Stars | A new quest is available. The quest is called 'Ship to the Stars'. |
| 11 Decembary 5500 06:24 | 4.3 | THƯ | NewQuest | Quest available: The Hard Prisoner | A new quest is available. The quest is called 'The Hard Prisoner'. If you don't accept the quest within 6 days, it will expire. |
| 11 Decembary 5500 11:39 | 4.1 | thông báo | NegativeEvent |  | Bac si failed while constructing a wooden dining chair. Some resources have been wasted. |
| 11 Decembary 5500 11:58 | 4.1 | thông báo | SituationResolved |  | Eistein is no longer pigging out on food. |
| 12 Decembary 5500 00:00 | 3.6 | THƯ | NeutralEvent | Visitors | A group from Camro dân tộc are visiting the colony. They seem to have a few items to trade. |
| 12 Decembary 5500 10:45 | 3.1 | thông báo | NeutralEvent |  | Visitors from Camro dân tộc are leaving. |
| 12 Decembary 5500 16:00 | 2.9 | THƯ | NeutralEvent | Transport pod crash | A policewoman named Arianites is crashing in a transport pod nearby. If she survives the impact, she will be badly wounded. Arianites is from Đế chế tan nát. If she returns home safely, she will spread goodwill between your factions. You c… |
| 12 Decembary 5500 19:40 | 2.7 | THƯ | NegativeEvent | Disease: Lung rot | Eistein has gotten sick from lung rot due to long-term exposure to rot stink gas (which is given off by rotting corpses). Ensure you have a medical bed and a doctor. Make sure that eistein gets proper treatment. |
| 13 Decembary 5500 07:25 | 2.3 | THƯ | NegativeEvent | Food binge: Eistein | Eistein is pigging out on food. This happened because of: Smokeleaf dependence (withdrawal 89%). |
| 13 Decembary 5500 14:48 | 1.9 | THƯ | ThreatBig | Raid: Khí độc đàn ông | A group of wasters have arrived from nearby. They are attacking immediately. |
| 13 Decembary 5500 16:03 | 1.9 | THƯ | Death | Death: Rat 1 | Rat 1 has been cut to death. |
| 13 Decembary 5500 16:37 | 1.9 | thông báo | PositiveEvent |  | Arianites, Policewoman is no longer incapable of walking. |
| 13 Decembary 5500 18:55 | 1.8 | thông báo | RejectInput |  | No reachable ritual spot. |
| 13 Decembary 5500 20:02 | 1.7 | thông báo | SituationResolved |  | Eistein is no longer pigging out on food. |
| 13 Decembary 5500 20:02 | 1.7 | thông báo | ThreatBig |  | Critical alert: Extreme break risk |
| 13 Decembary 5500 22:21 | 1.6 | thông báo | ThreatBig |  | Critical alert: Extreme break risk |
| 14 Decembary 5500 01:54 | 1.5 | thông báo | ThreatBig |  | Critical alert: Colonist needs rescue |
| 14 Decembary 5500 01:54 | 1.5 | thông báo | ThreatBig |  | Critical alert: Medical emergency |
| 14 Decembary 5500 05:02 | 1.4 | thông báo | ThreatBig |  | Critical alert: Medical emergency |
| 14 Decembary 5500 06:24 | 1.3 | THƯ | NewQuest | Quest available: Shoytt's Sad Survivors | A new quest is available. The quest is called 'Shoytt's Sad Survivors'. If you don't accept the quest within 6 days, it will expire. |
| 14 Decembary 5500 06:24 | 1.3 | THƯ | NegativeEvent | Solar flare | A solar flare has begun. The intense radiation will shut down all electrical devices. It should pass in about a day. |
| 14 Decembary 5500 12:13 | 1.1 | thông báo | PositiveEvent |  | Protein, Grunt is no longer incapable of walking. |
| 14 Decembary 5500 16:14 | 0.9 | thông báo | NeutralEvent |  | The solar flare is ending. |
| 14 Decembary 5500 20:26 | 0.7 | THƯ | ThreatSmall | Go-juice binge: Eistein | Eistein, Barkeep is binging on go-juice. This happened because of poor mood. The final straw was: Smokeleaf withdrawal |
| 14 Decembary 5500 23:02 | 0.6 | thông báo | NegativeEvent |  | Alpaca meat x13 has rotted away in storage. |
| 15 Decembary 5500 12:24 | 0.0 | THƯ | ThreatBig | Manhunter pack | A pack of man-hunting raccoons have entered the area! Driven insane by the disease known as scaria, they will roam the region, hunting for humanoid flesh. They won't attack doors unless they see someone go through the door. Hide inside and… |

Thông báo cũ hơn 5 ngày (gộp theo nội dung): «Critical alert: Major break risk» ×10; «Cảnh báo khẩn: Nguy cơ suy sụp nghiêm trọng» ×5; «Eistein failed while constructing a wooden dining chair. So…» ×3; «Protein thất bại trong lúc xây dựng bếp củi. Một ít tài ngu…» ×2; «Khách tham quan từ Orussia đang rời đi.» ×2; «Bac si, Bac si is fully healed.» ×2; «Sổ tay thẩm mỹ (tệ hại N%) đã hao mòn hết trong kho chứa.» ×1; «Eistein, Nhân viên pha chế đã bình phục hoàn toàn.» ×1; «Một nhóm du khách từ Camro dân tộc đang đi ngang qua.» ×1; «Một Người hái lượm từ Camro dân tộc đang đi qua. Anh ta đượ…» ×1; «Cảnh báo: Nghiên cứu sẽ không bắt đầu cho đến khi bạn xây d…» ×1; «Một nhóm du khách từ Orussia đang đi ngang qua.» ×1.


### Sự kiện đáng nhớ game ghi lại (tale)

Tổng: `Wounded`×121, `PlayedGame`×27, `Prayed`×6, `MajorThreat`×5, `ReadBook`×4, `Raid`×4, `Downed`×4, `KilledCapacity`×4, `LandedInPod`×3, `HeatstrokeRevealed`×3, `Hunted`×3, `KilledBy`×2, `KilledMelee`×2, `Meditated`×2, `TileSettled`×1, `Stripped`×1, `TrainedAnimal`×1, `TradedWith`×1, `ManhunterPack`×1.

| Lúc | Loại | Diễn biến |
|---|---|---|
| 6 Septober 5500 06:00 | `TileSettled` | Khu định cư mới |
| 6 Septober 5500 06:06 | `LandedInPod` | Protein đáp xuống bằng pod |
| 6 Septober 5500 06:06 | `LandedInPod` | eistein đáp xuống bằng pod |
| 6 Septober 5500 06:06 | `LandedInPod` | bac si đáp xuống bằng pod |
| 11 Septober 5500 15:35 | `Raid` | Đột kích bắt đầu (người chứng kiến: bac si) |
| 11 Septober 5500 16:22 | `KilledBy` | Beelzebub bị Gray giết |
| 11 Septober 5500 16:22 | `KilledMelee` | Gray giết Beelzebub (bằng MeleeWeapon_Knife) |
| 11 Septober 5500 16:50 | `Downed` | Gray bị hạ gục bởi Protein (bằng Gun_Revolver) |
| 13 Septober 5500 01:56 | `HeatstrokeRevealed` | bac si phát bệnh Heatstroke |
| 13 Septober 5500 23:40 | `HeatstrokeRevealed` | bac si phát bệnh Heatstroke |
| 3 Decembary 5500 04:24 | `Raid` | Đột kích bắt đầu (người chứng kiến: bac si) |
| 3 Decembary 5500 16:03 | `Stripped` | eistein lột đồ Buxdun |
| 4 Decembary 5500 16:27 | `HeatstrokeRevealed` | eistein phát bệnh Heatstroke |
| 5 Decembary 5500 02:00 | `Raid` | Đột kích bắt đầu (người chứng kiến: eistein) |
| 5 Decembary 5500 05:48 | `Downed` | Squirrel bị hạ gục bởi Protein (bằng Gun_Revolver) |
| 6 Decembary 5500 03:20 | `KilledCapacity` | bac si giết Squirrel (nạn nhân mất chức năng BloodPumping) |
| 6 Decembary 5500 12:38 | `KilledCapacity` | Protein giết Rat (nạn nhân mất chức năng Consciousness) |
| 6 Decembary 5500 12:39 | `Hunted` | Protein săn được Rat |
| 7 Decembary 5500 09:34 | `Downed` | Warg bị hạ gục bởi eistein (bằng MeleeWeapon_Knife) |
| 7 Decembary 5500 17:10 | `Hunted` | Protein săn được Tortoise |
| 8 Decembary 5500 08:43 | `KilledCapacity` | Protein giết Hare (nạn nhân mất chức năng BloodFiltration) |
| 9 Decembary 5500 03:42 | `Hunted` | Protein săn được Horse |
| 9 Decembary 5500 10:52 | `TrainedAnimal` | Protein huấn luyện Rat 1 (Tameness) |
| 12 Decembary 5500 06:52 | `TradedWith` | bac si giao dịch với Cervexa |
| 13 Decembary 5500 14:48 | `Raid` | Đột kích bắt đầu (người chứng kiến: eistein) |
| 13 Decembary 5500 16:03 | `KilledBy` | Rat 1 bị Elphy giết |
| 13 Decembary 5500 16:03 | `KilledMelee` | Elphy giết Rat 1 (bằng MeleeWeapon_Knife) |
| 13 Decembary 5500 16:03 | `KilledCapacity` | Elphy giết Rat 1 (nạn nhân mất chức năng BloodPumping) |
| 14 Decembary 5500 01:52 | `Downed` | Protein bị hạ gục (không do ai gây trực tiếp — kiệt sức/mất máu/đau) |
| 15 Decembary 5500 12:24 | `ManhunterPack` | Bầy thú điên (manhunter) kéo vào map (người chứng kiến: bac si) |


### Nhật ký chiến đấu (`battleLog`: 31 trận, 1,374 dòng gốc)

Game ghi lại từng phát bắn, từng đòn đánh (kể cả đi săn và thú hoang săn nhau) rồi gom thành «trận». Ở đây đã gộp theo cặp: «bắn 12 trúng 3» = bắn ra 12 phát, 3 phát trúng đúng mục tiêu; «cận chiến 5 trúng 2» = ra 5 đòn, trúng 2 (cận chiến kèm tên súng = dùng báng/nòng súng để đánh). «vướng vật cản» = viên đạn trượt mục tiêu và găm vào cây/tường/đá. Tên dạng `Loài` là thú không có tên riêng; `#1`, `#2` phân biệt các con cùng loài trong một trận. Dòng chỉ có kết cục (không có đòn đánh) là con vật/người gục hoặc chết sau trận vì mất máu, bệnh…

**Thành tích của phía thuộc địa trên toàn bộ log** (tính cả đi săn):
- **Protein**: bắn `Gun_Revolver` 312 phát, trúng mục tiêu 51 (16%), 58 phát vướng vật cản; cận chiến 20 đòn, trúng 10 (50%); bị đánh trúng 6 lần; bị gục 1 lần; đã giết: Horse×3, Rat×2, Squirrel×2, Ibex×2, Hare×2, Gray, Buxdun, Diana, Tortoise.
- **bac si**: bắn `Gun_BoltActionRifle` 275 phát, trúng mục tiêu 15 (5%), 103 phát vướng vật cản; cận chiến 11 đòn, trúng 3 (27%); bị đánh trúng 6 lần; đã giết: Squirrel, Warg, Donkey, Horse, Elphy.
- **eistein**: cận chiến 19 đòn, trúng 14 (74%); bị đánh trúng 4 lần; đã giết: Mink.
- **Beelzebub** (thú của thuộc địa): bị đánh trúng 1 lần.
- **Rat 1** (thú của thuộc địa): cận chiến 3 đòn, trúng 1 (33%); bị đánh trúng 4 lần.
- Đạn trượt mục tiêu nhưng găm vào vật cản (161 viên): `Plant_TreeOak` ×98, `Wall` ×16, `ChunkMarble` ×15, `ChunkGranite` ×8, `Marble` ×7, `Plant_TreePoplar` ×7, `Granite` ×5, `AncientConcreteBarrier` ×1, `Door` ×1, `Sarcophagus` ×1, `AncientGenerator` ×1, `SmashedStump` ×1.

| Lúc | Các bên | Diễn biến → kết cục |
|---|---|---|
| 7 Septober 5500 09:12–10:09 | Tortoise, Warg (thú hoang) | Warg → Tortoise: cận chiến 24 trúng 8 [2 lần là hất đất vào mắt, 2 bị giáp chặn, huỷ 3 bộ phận]; Tortoise → Warg: cận chiến 12 trúng 1; **Tortoise CHẾT** (do Warg, `Crack`) |
| 9 Septober 5500 15:57–16:09 | eistein ↔ Mink (thú hoang) | eistein → Mink: cận chiến 5 trúng 2 (tay không) [huỷ 1 bộ phận]; Mink → eistein: cận chiến 4 trúng 2; **Mink CHẾT** (do eistein, `Bruise`) |
| 11 Septober 5500 16:18–16:59 | Protein, eistein, bac si, Beelzebub ↔ Gray (Khí độc đàn ông (PirateWaster)) | Gray → Beelzebub: cận chiến 3 trúng 1 (`MeleeWeapon_Knife`) [huỷ 2 bộ phận]; Gray → vật `Wall`: cận chiến 2 trúng 2 (`MeleeWeapon_Knife`); Protein → Gray: bắn 4 trúng 2 (`Gun_Revolver`) [huỷ 1 bộ phận]; bac si → Gray: cận chiến 2 trúng 0 (`Gun_BoltActionRifle`, tay không); Gray → bac si: cận chiến 1 trúng 0 (`MeleeWeapon_Knife`); eistein → Gray: cận chiến 4 trúng 4 (`MeleeWeapon_Knife`); Gray → eistein: cận chiến 2 trúng 1 (`MeleeWeapon_Knife`) [1 bị giáp chặn]; **Beelzebub CHẾT** (do Gray, `Cut`); **Gray gục** (do Protein, `Gunshot`); **Gray CHẾT** (do Protein, `Gunshot`) |
| 2 Decembary 5500 20:49 | Sparrow (thú hoang) | không rõ → Sparrow: nổ/lửa ×1 (`Flame`) [huỷ 2 bộ phận]; **Sparrow CHẾT** (`MissingBodyPart`) |
| 3 Decembary 5500 05:14–05:39 | Protein, bac si, eistein ↔ Buxdun (Khí độc đàn ông (PirateWaster)) | Protein → Buxdun: bắn 10 trúng 4 (`Gun_Revolver`) [3 phát vướng vật cản]; bac si → Buxdun: bắn 7 trúng 0 (`Gun_BoltActionRifle`) [2 phát vướng vật cản]; Buxdun → eistein: cận chiến 3 trúng 0 (`MeleeWeapon_Knife`); **Buxdun CHẾT** (do Protein) |
| 3 Decembary 5500 18:29–18:35 | Protein ↔ Rat (thú hoang) | Protein → Rat: cận chiến 3 trúng 2 (`Gun_Revolver`) [huỷ 2 bộ phận]; Rat → Protein: cận chiến 3 trúng 1; **Rat CHẾT** (do Protein) |
| 5 Decembary 5500 03:08–09:36 | Protein, bac si, eistein ↔ Diana (Khí độc đàn ông (PirateWaster)) ↔ Ibex, Squirrel×2 (thú hoang) | Protein → Diana: bắn 9 trúng 4 (`Gun_Revolver`); Diana → eistein: cận chiến 2 trúng 1 (`MeleeWeapon_Club`); bac si → Diana: cận chiến 4 trúng 1 (`Gun_BoltActionRifle`); Diana → bac si: cận chiến 3 trúng 1 (`MeleeWeapon_Club`, tay không); Protein → Squirrel#1: bắn 17 trúng 1 (`Gun_Revolver`) [huỷ 2 bộ phận] + cận chiến 4 trúng 3 (`Gun_Revolver`) [1 lần là hất đất vào mắt, huỷ 1 bộ phận]; bac si → Squirrel#2: bắn 18 trúng 0 (`Gun_BoltActionRifle`) [9 phát vướng vật cản]; Squirrel#1 → Protein: cận chiến 3 trúng 0; Protein → Ibex: bắn 30 trúng 3 (`Gun_Revolver`) [10 phát vướng vật cản, huỷ 1 bộ phận]; **Diana CHẾT** (do Protein); **Squirrel#1 gục** (do Protein, `MissingBodyPart`); **Squirrel#1 CHẾT** (do Protein) |
| 5 Decembary 5500 07:40–14:24 | bac si ↔ Rat, Squirrel, Hare (thú hoang) | bac si → Hare: bắn 16 trúng 0 (`Gun_BoltActionRifle`) [4 phát vướng vật cản]; bac si → Squirrel: bắn 16 trúng 0 (`Gun_BoltActionRifle`) [8 phát vướng vật cản]; bac si → Rat: bắn 18 trúng 0 (`Gun_BoltActionRifle`) [5 phát vướng vật cản] |
| 5 Decembary 5500 14:19–18:20 | Protein ↔ Ibex×2 (thú hoang) | Protein → Ibex#1: bắn 15 trúng 3 (`Gun_Revolver`) [2 phát vướng vật cản, huỷ 1 bộ phận]; **Ibex#2 gục** (`BloodLoss`); **Ibex#2 CHẾT** (do Protein); **Ibex#1 CHẾT** (do Protein, `Gunshot`) |
| 6 Decembary 5500 03:13–07:45 | bac si ↔ Ibex, Squirrel (thú hoang) | bac si → Squirrel: bắn 3 trúng 1 (`Gun_BoltActionRifle`) [1 phát vướng vật cản, huỷ 2 bộ phận]; bac si → Ibex: bắn 17 trúng 0 (`Gun_BoltActionRifle`) [3 phát vướng vật cản]; **Squirrel CHẾT** (do bac si, `MissingBodyPart`) |
| 6 Decembary 5500 07:34–15:32 | Protein ↔ Donkey, Rat, Squirrel, Ibex (thú hoang) | Protein → Ibex: bắn 19 trúng 2 (`Gun_Revolver`) [4 phát vướng vật cản]; Protein → Squirrel: bắn 7 trúng 1 (`Gun_Revolver`) [3 phát vướng vật cản, huỷ 2 bộ phận]; Protein → Rat: bắn 23 trúng 1 (`Gun_Revolver`) [6 phát vướng vật cản, huỷ 2 bộ phận]; Protein → Donkey: bắn 11 trúng 3 (`Gun_Revolver`) [2 phát vướng vật cản]; **Squirrel CHẾT** (do Protein, `Gunshot`); **Rat CHẾT** (do Protein, `MissingBodyPart`) |
| 6 Decembary 5500 09:49–15:40 | bac si ↔ Ibex (thú hoang) | bac si → Ibex: bắn 53 trúng 2 (`Gun_BoltActionRifle`) [26 phát vướng vật cản, huỷ 1 bộ phận]; **Ibex gục** (`BloodLoss`) |
| 6 Decembary 5500 12:14 | Ibex (thú hoang) | **Ibex gục** (`BloodLoss`) |
| 6 Decembary 5500 14:41 | Ibex (thú hoang) | **Ibex CHẾT** (`BloodLoss`) |
| 6 Decembary 5500 19:28–19:56 | Protein ↔ Hare (thú hoang) | Protein → Hare: bắn 7 trúng 2 (`Gun_Revolver`) [huỷ 2 bộ phận]; **Hare CHẾT** (do Protein) |
| 6 Decembary 5500 19:42 | Ibex (thú hoang) | **Ibex CHẾT** (`BloodLoss`) |
| 6 Decembary 5500 19:48–23:27 | bac si ↔ Horse (thú hoang) | bac si → Horse: bắn 20 trúng 3 (`Gun_BoltActionRifle`) [10 phát vướng vật cản]; **Horse gục** (`BloodLoss`) |
| 7 Decembary 5500 03:09 | Horse (thú hoang) | **Horse CHẾT** (`BloodLoss`) |
| 7 Decembary 5500 08:46–19:32 | Protein, bac si, eistein ↔ Horse, Tortoise, Warg (thú hoang) | Protein → Warg: bắn 7 trúng 3 (`Gun_Revolver`) [3 phát vướng vật cản] + cận chiến 1 trúng 1 (`Gun_Revolver`); Warg → vật `Door`: cận chiến 5 trúng 5; bac si → Warg: bắn 3 trúng 2 (`Gun_BoltActionRifle`) [1 phát vướng vật cản, huỷ 1 bộ phận]; eistein → Warg: cận chiến 5 trúng 5 (`MeleeWeapon_Knife`); Warg → bac si: cận chiến 1 trúng 1; Protein → Tortoise: bắn 101 trúng 6 (`Gun_Revolver`) [15 phát vướng vật cản, 2 bị giáp chặn, huỷ 1 bộ phận]; Protein → Horse: bắn 17 trúng 8 (`Gun_Revolver`) [1 phát vướng vật cản]; **Warg gục** (do eistein, `Cut`); **Warg CHẾT** (do bac si, `Gunshot`); **Tortoise CHẾT** (do Protein); **Horse CHẾT** (do Protein) |
| 7 Decembary 5500 09:25 | Donkey (thú hoang) | **Donkey gục** (`BloodLoss`) |
| 7 Decembary 5500 12:16 | bac si ↔ Donkey (thú hoang) | **Donkey CHẾT** (do bac si) |
| 7 Decembary 5500 15:30–16:57 | bac si ↔ Horse (thú hoang) | bac si → Horse: bắn 12 trúng 1 (`Gun_BoltActionRifle`) [5 phát vướng vật cản]; **Horse gục** (`HeartAttack`); **Horse CHẾT** (do bac si) |
| 8 Decembary 5500 05:55–07:00 | bac si ↔ Horse (thú hoang) | bac si → Horse: bắn 10 trúng 1 (`Gun_BoltActionRifle`) [1 phát vướng vật cản] |
| 8 Decembary 5500 08:39–12:38 | Protein ↔ Horse, Hare (thú hoang) | Protein → Hare: bắn 2 trúng 1 (`Gun_Revolver`) [1 phát vướng vật cản, huỷ 1 bộ phận]; Protein → Horse: bắn 20 trúng 5 (`Gun_Revolver`) [4 phát vướng vật cản]; **Hare CHẾT** (do Protein, `MissingBodyPart`); **Horse gục** (`BloodLoss`); **Horse CHẾT** (do Protein) |
| 8 Decembary 5500 13:25–20:23 | bac si ↔ Horse (thú hoang) | bac si → Horse: bắn 67 trúng 2 (`Gun_BoltActionRifle`) [24 phát vướng vật cản] |
| 8 Decembary 5500 23:25–9 Decembary 5500 03:42 | Protein ↔ Horse (thú hoang) | Protein → Horse: bắn 12 trúng 2 (`Gun_Revolver`) [3 phát vướng vật cản]; **Horse gục** (`BloodLoss`); **Horse CHẾT** (do Protein) |
| 10 Decembary 5500 19:16–19:23 | bac si ↔ Squirrel (thú hoang) | bac si → Squirrel: bắn 3 trúng 0 (`Gun_BoltActionRifle`) |
| 13 Decembary 5500 15:35–16:46 | bac si, Protein, eistein, Rat 1 ↔ Elphy (Khí độc đàn ông (PirateWaster)) | bac si → Elphy: bắn 12 trúng 3 (`Gun_BoltActionRifle`) [4 phát vướng vật cản] + cận chiến 5 trúng 2 (`Gun_BoltActionRifle`); Protein → Elphy: bắn 1 trúng 0 (`Gun_Revolver`) [1 phát vướng vật cản] + cận chiến 12 trúng 4 (`Gun_Revolver`, tay không); Elphy → Rat 1: cận chiến 5 trúng 4 (`MeleeWeapon_Knife`) [1 lần là hất đất vào mắt, huỷ 4 bộ phận]; Rat 1 → Elphy: cận chiến 3 trúng 1 [1 lần là hất đất vào mắt]; Elphy → bac si: cận chiến 5 trúng 4 (`MeleeWeapon_Knife`, tay không); Elphy → Protein: cận chiến 8 trúng 5 (`MeleeWeapon_Knife`) [1 lần là hất đất vào mắt]; eistein → Elphy: cận chiến 5 trúng 3 (`MeleeWeapon_Knife`) [1 lần là hất đất vào mắt]; Elphy → eistein: cận chiến 3 trúng 0 (`MeleeWeapon_Knife`, tay không); **Rat 1 CHẾT** (do Elphy, `MissingBodyPart`); **Elphy CHẾT** (do bac si, `Gunshot`) |
| 14 Decembary 5500 01:52 | Protein | **Protein gục** (`BloodLoss`) |
| 15 Decembary 5500 06:44–06:54 | Lynx, Bear_Grizzly (thú hoang) | Bear_Grizzly → Lynx: cận chiến 3 trúng 2 [huỷ 1 bộ phận]; **Lynx CHẾT** (do Bear_Grizzly, `Scratch`) |
| 15 Decembary 5500 10:40–11:00 | WildBoar, Wolf_Timber (thú hoang) | Wolf_Timber → WildBoar: cận chiến 7 trúng 4 [huỷ 1 bộ phận]; WildBoar → Wolf_Timber: cận chiến 4 trúng 0; **WildBoar CHẾT** (do Wolf_Timber) |


### Tương tác xã hội gần đây (`playLog`: 150 dòng)

Game chỉ giữ 150 tương tác mới nhất — ở đây là từ 2 Decembary 5500 20:34 đến 15 Decembary 5500 13:05. Chiều mũi tên: người mở lời → người nghe.

| Ai → ai (đều đang ở trên map) | Số lần theo loại |
|---|---|
| Protein → bac si | `Chitchat` (chuyện phiếm) ×25 |
| eistein → Protein | `Chitchat` (chuyện phiếm) ×22, `Slight` (nói mỉa / coi thường) ×2 |
| bac si → eistein | `Chitchat` (chuyện phiếm) ×24 |
| Protein → eistein | `Chitchat` (chuyện phiếm) ×16, `Insult` (xúc phạm) ×2 |
| eistein → bac si | `Chitchat` (chuyện phiếm) ×16, `Insult` (xúc phạm) ×1 |
| bac si → Protein | `Chitchat` (chuyện phiếm) ×15 |

**Đáng chú ý (không phải chuyện phiếm):** 8 Decembary 5500 12:05 — eistein → bac si: `Insult` (xúc phạm); 9 Decembary 5500 10:52 — Protein → Rat 1: `TrainAttempt` (huấn luyện thú); 10 Decembary 5500 06:03 — eistein → Protein: `Slight` (nói mỉa / coi thường); 12 Decembary 5500 00:08 — Cervexa → Purple: `DeepTalk` (tâm sự sâu); 12 Decembary 5500 18:02 — eistein → Protein: `Slight` (nói mỉa / coi thường); 13 Decembary 5500 16:28 — Protein → eistein: `Insult` (xúc phạm); 13 Decembary 5500 21:22 — Protein → eistein: `Insult` (xúc phạm).

**Có người/thú hiện không ở trên map** (khách đã rời đi, thú đã chết…): 27 dòng — `Chitchat` (chuyện phiếm) ×22, `AnimalChat` (trò chuyện với thú) ×3, `TrainAttempt` (huấn luyện thú) ×1, `DeepTalk` (tâm sự sâu) ×1; số dòng theo từng cá thể: Cervexa [Camro dân tộc (TribeCivil)] ×12, Purple [Camro dân tộc (TribeCivil)] ×12, Penguin [Camro dân tộc (TribeCivil)] ×10, Porcupine [Camro dân tộc (TribeCivil)] ×8, Rat 1 [thú của thuộc địa, đã chết] ×4, Freya [Orussia (OutlanderCivil)] ×2, Kent [Orussia (OutlanderCivil)] ×2.


## 17. Chính sách đang dùng

**Chính sách thuốc «Chính sách thuốc»** (3 người dùng): Beer: giải trí; SmokeleafJoint: giải trí; Ambrosia: khi nghiện; Drug_Psilocap: khi nghiện; Yayo: khi nghiện; Flake: khi nghiện; PsychiteTea: khi nghiện; GoJuice: khi nghiện; WakeUp: khi nghiện; Penoxycyline: khi nghiện; Luciferium: khi nghiện; VoidsightSerum: khi nghiện; MetalbloodSerum: khi nghiện; JuggernautSerum: khi nghiện; MindNumbSerum: khi nghiện.

Chính sách có sẵn — thuốc: «Chính sách thuốc», «Không dùng», «Không giới hạn», «1 lần mỗi ngày» · trang phục: «Gì cũng mặc», «Lao động», «Vũ trang», «Trần trụi», «Nô lệ», «Du hành vũ trụ» · ăn uống: «Xa hoa», «Ngon», «Đơn giản», «Hỗn hợp», «Tươi sống», «Nhịn đói», «Đồ chay», «Ăn thịt», «Ăn thịt người», «Thịt côn trùng».


## 18. Giới hạn của dữ liệu

- File save **không lưu** các giá trị game tự tính lúc chạy: chỉ số phòng (ấn tượng/đẹp/sạch), tốc độ di chuyển, mức đau, năng lực cơ thể (Consciousness, Moving…), tốc độ chảy máu, HP tối đa, điện lưới, vùng phủ sáng, và các *thought tình huống* (đau, phòng xấu, thiếu giải trí, nghiện…). Mục «ký ức» ở trên chỉ gồm thought dạng ký ức.
- Giới tính: game chỉ ghi khi khác `Male`; không có thẻ nghĩa là Male.
- Ngày giờ: múi giờ suy từ tick bắt đầu ván và kiểm chứng bằng tick reset XP lúc nửa đêm của pawn.
- Bảng nghiên cứu, ngưỡng thối của thực phẩm/xác, dinh dưỡng, ngưỡng tâm trạng: dựa trên giá trị def **vanilla** (mod có thể thay đổi).
- Phòng, mạch quặng, khoảng cách, cảnh báo ở mục 2: do công cụ suy ra từ dữ liệu thô (không phải do game ghi).
- Tên def của địa hình/đá/mái được tra ngược từ mã băm; mã không nhận ra sẽ hiện dạng `Terrain#12345`.
