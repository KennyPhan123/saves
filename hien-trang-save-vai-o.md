# HIỆN TRẠNG SAVE “vãi ò” — 5500, 14 Aprimay, 16:27

> Đọc trực tiếp từ `vãi ò.rws` (14.955.945 bytes) bằng `tools/rimworld_dump.py`.
> **Game 1.7.4990 rev1069** · Core + Royalty + Ideology + Biotech + Anomaly + Odyssey (không mod ngoài).
> Tick **821.158** = **13,686 ngày** đã chơi · thời gian chơi thật 6.331 giây (~1h45).
>
> File này là **snapshot mới**. `bao-cao-save-vai-o.md` ở gốc repo là snapshot **cũ hơn 12 giờ game**
> (tick 791.289) — xem mục 1 để biết đã thay đổi những gì.

Tái lập:

```bash
python3 tools/rimworld_dump.py "vãi ò.rws" -o dump   # → dump/report.md (181k ký tự), state.json, CSV
```

---

## 0. Bảng điều khiển — 30 giây

| Hạng mục | Trạng thái | Số liệu |
|---|:--:|---|
| **Tâm trạng eistein** | 🔴 **KHẨN** | **17 %** (12h trước: 34 %), 2 cảnh báo “Major break risk”, bộ đếm minor-break **24.450/30.000 tick** |
| Suất ăn dự phòng | 🔴 **0** | Không có một suất ăn nào; chỉ 332 gạo sống + 10 quả mọng. eistein đói 17 % |
| Nhiên liệu nấu | 🟢 | Bếp củi (125,139) còn **45,4** nhiên liệu, bill “Nấu 4 suất ăn” ×10 **vẫn hợp lệ** |
| Người làm việc | 🔴 | **eistein bị khoá lịch Joy 16h/ngày** → 1/3 dân số không làm gì |
| Nghiên cứu | 🔴 | **Batteries: 0 %** dù bàn nghiên cứu dựng từ tick 689.234 (~3,7 ngày trước) |
| Điện | 🟡 | Đã research Electricity, **chưa xây một nguồn điện nào** |
| Nhà ở | 🟢 | 211 công trình; 189 tường gỗ, 8 cửa, 3 giường — **toàn bộ khu nhà đều có mái** (giải nén `roofGrid`), chỉ hở 3 ô trong kho |
| Thức ăn thô | 🟢 | 109 ô lúa, độ lớn TB **73,6 %** (65–92 %) → thu hoạch trong ~1–2 ngày |
| Tài nguyên | 🟢 | Gỗ **4.848** · Thép **987** · Bạc **800** · Linh kiện **30** · Thuốc **24** |
| Phòng thủ | 🔴 | 0 túi cát/barricade; 3 người mà chỉ **1 súng trường + 1 súng lục + 1 dao**; **2 mối đe doạ đang xếp hàng** |
| Đột kích | 🟡 | 2 vụ đã xảy ra (gần nhất tick 716.000 = **1,75 ngày trước**) → vụ thứ 3 đang tới |
| Anomaly | 🟡 | Monolith **Inactive**, nhưng **đang “gọi” Protein** (giấc mơ lúc tick 802.090) |
| Tôn giáo | 🟢 | Astropolitan, 31 tín điều, cả 3 tin cậy 86–95 % |

---

## 1. 12 giờ game vừa qua đã thay đổi gì (so với `state.json` cũ)

| Mục | Cũ (tick 791.289) | Mới (tick 821.158) |
|---|---|---|
| Công trình của bạn | 211 | **211 (không xây thêm gì)** |
| Gỗ | 4.430 | **4.848** (+418 do chặt cây) |
| Lệnh được giao (designations) | 73 | **32** (đã dọn 41 việc) |
| Ô lúa | 98 | **109** (+11 ô ruộng mới ở 114–117 × 148–151) |
| Suất ăn sinh tồn | 2 | **0** (đã ăn hết) |
| Thư mới | — | **5**: “Ám ảnh kinh hoàng”, “Phế tích nguy hiểm”, 3 tin nhắn |
| Tâm trạng eistein | 34 % | **17 %** |

**Điều đáng chú ý nhất:** cả 3 pawn vừa ở **góc tây nam bản đồ (15–21, 231–234)** — mỏ thép tạm cách căn cứ **~200 ô**. Đó chính là lý do eistein có `SleptOnGround`, `SleptOutside`, `SleptInHeat` (0,62 ngày trước) và tụt 17 điểm tâm trạng trong nửa ngày. Giờ cả 3 đã về nhà.

---

## 2. Ba pawn — hiện trạng

| | **Protein** (Ichabod) | **bac si** (Nikolay) | **eistein** (Anthony) |
|---|:--:|:--:|:--:|
| Vị trí | (110,133) | (135,121) | (139,135) |
| Đang làm | **Tháo cửa (111,132)** | Chơi móng ngựa | **Cầu nguyện** (RelaxAlone) |
| Tâm trạng | 57 % 🟢 | 65 % 🟢 | **17 %** 🔴 |
| Thức ăn | 80 % | 93 % | **17 %** 🔴 |
| Nghỉ ngơi | **29 %** 🟡 | 37 % 🟡 | 41 % |
| Thoải mái | 35 % | 40 % | **16 %** |
| Sức khỏe | Khỏe | Khỏe | Nghiện cần sa 0,393 · Dung nạp 0,672 · **Heatstroke 0,07** |
| Vũ khí | Súng lục ổ xoay | **Súng trường bolt-action** | Dao plasteel + giáp Flak + mũ tiên tiến |
| Lịch | Ngủ 22–05, làm 06–19, Joy 20–21 | Giống Protein | **Joy 06–21 (16 tiếng!)** 🔴 |
| Kỹ năng chính | Trồng **10**★★ · Nấu **8**★★ · Trí tuệ 6★ | Y học **5**★★ · Bắn 3★ | **Trí tuệ 9★ · Xã hội 9★** · Cận chiến 7★ · Nghệ thuật 7 |

### eistein đang sắp nổ

- `ticksBelowMinor = 24.450` trên ngưỡng **30.000 tick** → còn **~5.500 tick ≈ 2,3 giờ game** nữa là chạm mốc *minor break*. Đã có 2 cảnh báo **“Critical alert: Major break risk”** (tick 807.684 và 817.619).
- Suy nghĩ tiêu cực đang găm: `SleptInHeat`, `SleptOutside`, `AteWithoutTable`, `Slighted` (−4,65), **2× `ObservedLayingRottingCorpse`**. Suy nghĩ tích cực chỉ còn `CrashedTogether` ×2 và `NewColonyHope`.
- **Đừng** cắt cần sa đột ngột lúc này — withdrawal sẽ trừ thêm tâm trạng. Chữa nguyên nhân, không chữa triệu chứng.

### Ưu tiên công việc (0 = tắt)

| Việc | Protein | bac si | eistein |
|---|:--:|:--:|:--:|
| Nấu ăn | **1** | 0 | 1 |
| Trồng trọt | **1** | 0 | 0 |
| Xây dựng | **1** | 1 | 1 |
| Khiêng vác | **1** | 1 | 1 |
| Chặt cây | 1 | 2 | 2 |
| Nghiên cứu | 2 | **0** | **2** |
| Bác sĩ | 0 | 1 | 0 |
| Chữa cháy | 1 | **0** | 1 |

> Không ai có Nghiên cứu ở mức 1. Cộng với lịch Joy của eistein ⇒ **Batteries đứng ở 0 % vĩnh viễn** dù bàn nghiên cứu đã có.

---

## 3. Căn cứ “damn bro”

**Công trình (211):** 189 Tường gỗ · 8 Cửa · 3 Giường · 4 Đuốc · 2 Ghế đẩu · 1 Bàn ăn 1×2 (123,137) · 1 Bếp củi (125,139) · 1 Bàn nghiên cứu (139,146) · 1 Cọc móng ngựa (135,126) · 1 Khung ghế ăn **dở dang** (139,145, đã 3 ngày).

**Chưa có:** điện, đèn điện, tủ lạnh, điều hoà, túi cát/barricade, tường đá, nhà kho riêng, nhà tù, phòng thờ.

**Vùng:** ruộng lúa 1 = 98 ô (108–121 × 135–141) · ruộng lúa 2 = **11 ô mới** (114–117 × 148–151) · kho 1 = 195 ô (94–106 × 130–144, nhận **834 loại** = gần như tất cả) · kho xác 2 = 99 ô (234–244 × 143–151, cách nhà ~120 ô).

**Trong kho:** Gỗ 4.540 · Thép 867 · Bạc 800 · Gạo 328 · Linh kiện 30 · Thuốc 24 · 1 súng ngắn tự động · 1 dao · 1 áo + 1 quần.

**Ngoài kho:** 120 thép ở mỏ tây nam · **348 tấm Gravlite** quanh xác tàu cơ khí (212–232 × 1–17) · 15 Luciferium ở di tích (201,74) · 308 gỗ vương vãi.

**Rác/bẩn:** 2.814 ô (2.587 mảnh đá vụn, 114 mảnh máy, 52 tro). Có sẵn nguyên liệu đá để chuyển sang tường đá nếu muốn.

**Mái nhà:** đã giải nén `roofGrid` (deflate + base64) — toàn bộ các phòng đều có mái xây dựng. Duy nhất **3 ô (100,136), (100,137), (100,138)** trong kho 1 bị hở: kho rộng 13 ô nên cột giữa vượt quá tầm đỡ của tường. Muốn bịt thì kê 1 cột gỗ giữa kho.

---

## 4. Nghiên cứu · Tôn giáo · Anomaly · Nhiệm vụ

**Nghiên cứu:** xong 7 (ComplexFurniture, PassiveCooler, Stonecutting, ComplexClothing, Electricity, NutrientPaste, AirConditioning) — **đang làm Batteries, tiến độ 0 %**.

**Tôn giáo Astropolitan** (deity, ẩn): ăn thịt người = chấp nhận · xác chết = xấu · **ăn bột dinh dưỡng = kinh tởm** ⚠ · khỏa thân = phản đối · nghi lễ: tang, khiêu vũ, đánh trống, liên kết cây anima, sinh nở, tử hình, diễn văn. **Chưa có ghế nghi lễ/ritual spot** ⇒ chưa chạy được nghi lễ nào. Có 1 **cây Anima** ở (67,170).

**Anomaly:** monolith **Inactive**, chưa kích hoạt. Nhưng tick 802.090 có thư “Ám ảnh kinh hoàng”: Protein mơ thấy monolith và **bị cuốn về phía nó**. `nextHarbingerTreeCheckTick` = 844.319 (còn ~23.000 tick).

**Nhiệm vụ:** *Tín hiệu cơ học* — tàu cơ khí đã hạ cánh, **động cơ trọng lực ở (230,13)** + 348 tấm gravlite → có thể đóng tàu rời hành tinh. *Chạy trốn phu nhân* — xuất hiện tick 480.000 với hạn 2 ngày, **đã quá hạn từ lâu**, bỏ qua.

**Phe:** Orussia (thân thiện, hay ghé buôn) · Camro dân tộc · Khí độc đàn ông (đã đột kích 2 lần) · Đế chế tan nát · bầy cỗ máy · thực thể Bóng tối.

---

## 5. Bản đồ & các điểm nóng

| Điểm | Toạ độ | Ghi chú |
|---|---|---|
| **Di tích nguy hiểm** | 193–203 × 67–77 | 6 quan tài ngủ đông, 3 sarcophagus, hòm kín, **15 Luciferium (201,74)**, **3 mech đang canh**: Militor (205,67) & (201,74), Scorcher (198,66) |
| Xác tàu cơ khí | 212–232 × 1–17 | 6 mảnh tàu, 348 tấm gravlite, 7 xác mech, động cơ trọng lực (230,13) |
| Mỏ thép tạm | 15–21 × 231–234 | 120 thép — **cách nhà ~200 ô, không đáng đi** |
| Kho xác | 234–244 × 143–151 | 17 xác: 4 người, 5 pikeman, 2 scyther, thú |
| Mạch nước nóng | **(145,126)** và **(129,151)** | Sát căn cứ → đặt Geothermal generator khi có công nghệ |
| Cây Anima | (67,170) | Cho nghi lễ “liên kết cây anima” |

Động vật: 35 con (6 ngựa, 3 tê giác, 3 ibex, warg, megasloth…) + **1 chuột đực đã thuần hoá** ở (140,137).

---

## 6. Chẩn đoán — 5 nguyên nhân gốc

1. **eistein bị khoá lịch Joy 16 giờ/ngày.** Anh ta là người giỏi nhất thuộc địa (Trí tuệ 9★, Xã hội 9★, Nấu 7, Nghệ thuật 7) nhưng **không được giao việc nào**. Đây là lý do trực tiếp của: nghiên cứu 0 %, không ai nấu ăn, và tâm trạng lao dốc (Joy đầy nhưng thức ăn/nghỉ/tiện nghi thì không).
2. **Không có suất ăn nào trong thuộc địa.** Bill nấu hợp lệ và còn nhiên liệu, nhưng Protein bị 4 việc ưu tiên 1 giành mất, eistein thì đang “nghỉ”. Kết quả: ăn gạo sống (−7 tâm trạng/`AteRawFood`) đúng lúc cần tăng tâm trạng.
3. **Đi khiêng thép ở mỏ cách 200 ô.** Ngủ đất + ngủ ngoài trời + ngủ nơi nóng trong 1 đêm = mất gần 20 điểm tâm trạng. Đổi 120 thép lấy một cú sụp tinh thần là lỗ.
4. **Không có nguồn điện và không có ai nghiên cứu.** Đã research Electricity/AirConditioning/Batteries-nearly nhưng 0% tiến độ và 0 công trình điện ⇒ đuốc là nguồn sáng duy nhất, không tủ lạnh, không điều hoà.
5. **Không có phòng thủ.** 2 mối đe doạ đang xếp hàng, đột kích cuối 1,75 ngày trước, 3 người / 3 vũ khí, không barricade.

---

## 7. Việc nên làm tiếp theo

### ⏱ Làm ngay (2–3 phút thao tác, trước khi bấm chạy tiếp)

1. **Sửa lịch eistein:** đổi 06 h–21 h từ `Joy` → `Anything` (hoặc `Work`). Giữ 20 h–21 h là `Joy`.
   → Đây là một cú click nhưng sửa được 3 vấn đề cùng lúc.
2. **Nấu ăn ngay:** chọn bếp (125,139) → bill “Nấu 4 suất ăn đơn giản ×10” đổi thành **“Cho đến khi có 20”** (Do until you have X). Hạ ưu tiên `Xây dựng`/`Khiêng vác` của Protein xuống **2** trong hôm nay để anh ta nấu.
3. **Cho eistein ăn trước khi làm gì khác** — Food 17 %, và tuyệt đối không để anh ta ăn gạo sống nếu đã có suất ăn.
4. **Xoá lệnh `Haul` ở (15,232) / (15,234) / (21,231)** — 120 thép không đáng 200 ô đi bộ.
5. **Bật Nghiên cứu = 1 cho eistein** (Trí tuệ 9★) sau khi anh ta ăn xong → Batteries sẽ chạy.

### 🕐 Trong 1–2 giờ game tới

6. **Xây Ritual spot (miễn phí, 1 ô) trong phòng ăn** rồi chạy **“Tiệc khiêu vũ”**. Đây là cách nhanh nhất kéo cả 3 khỏi vùng nguy hiểm mà không tốn tài nguyên.
7. **Chokepoint phòng thủ:** chọn 1 cửa duy nhất làm điểm chặn (gợi ý cửa (128,141) hoặc (128,148)), xây 3–4 **túi cát** hai bên, cho bac si (bắn 3★, súng trường) đứng sau, eistein (cận chiến 7 + giáp) đứng ô cửa. Khoá 7 cửa còn lại bằng cách xây tường.
8. **Đưa súng ngắn tự động trong kho (97,142) cho eistein** làm vũ khí phụ, hoặc cho Protein — hiện nó chỉ nằm trong thùng.
9. **Hoàn thành khung ghế ăn dở (139,145)** hoặc huỷ để lấy lại 45 gỗ — nó treo ở đó 3 ngày rồi.

### 📅 Hôm nay – ngày 15

10. **Điện:** xong Batteries → xây **Wood-fired generator** + 2–3 đèn trong phòng ăn/phòng ngủ (đèn = +mood, +tốc độ làm việc).
11. **Chuyển tường gỗ → tường đá** ở mặt ngoài (đã có Stonecutting, 2.587 mảnh đá vụn tại chỗ). Ưu tiên 4 bức tường bao ngoài cùng — gỗ cháy rất nhanh khi bị đốt.
12. **Ngừng phụ thuộc gạo sống:** thêm 1 ruộng **bông** hoặc **healroot** (đã có 87 healroot hoang nên chưa gấp), và cân nhắc 2–3 ô **bí ngô/bắp** để đa dạng.
13. **Dọn kho xác**: huỷ zone 2 (cách 120 ô, pawn đi qua sẽ ăn `ObservedLayingRottingCorpse` — eistein vừa dính 2 lần) hoặc đốt xác.

### 🗓 2–3 ngày tới

14. **Đừng mở di tích (193–203 × 67–77).** 3 mech canh + hòm kín + 15 luciferium (gây nghiện vĩnh viễn). Chỉ mở khi có 4+ súng, giáp cho cả 3, và một chokepoint. Nếu muốn luciferium mà không đánh: **để nguyên**, luciferium chỉ có giá trị khi bạn có pawn đã nghiện.
15. **Anomaly:** monolith đang gọi Protein. Càng để lâu càng nhiều “giấc mơ” (−mood). Quyết định có chủ đích: **chưa kích hoạt** cho tới khi có điện + phòng thủ + 4 người. (`nextHarbingerTreeCheckTick` = 844.319.)
16. **Odyssey / về đích:** có động cơ trọng lực + 348 tấm gravlite → đủ để đóng tàu rời đi. Nếu mục tiêu là “thắng nhẹ nhàng”, đây là đường ngắn nhất; nếu muốn xây thuộc địa lâu dài thì để dành.
17. **Địa nhiệt:** 2 mạch nước nóng ngay sát nhà (145,126) và (129,151) → **Geothermal generator** là nguồn điện tốt nhất bản đồ này, không cần nhiên liệu. Thêm vào lộ trình research sau Batteries.

### ⚠️ Kiểm tra thêm

- **Quần áo eistein:** đang mặc **parka** (đồ chống lạnh, giảm ngưỡng chịu nóng) mà vẫn bị `Heatstroke 0,07` → đổi sang áo sơ mi/vải thường, và đừng để pawn ngủ trong phòng bếp (bếp củi toả nhiệt).
- **Chính sách thuốc:** đang là “Chính sách thuốc 1”. Kiểm tra xem cần sa có được cấp theo lịch không — cắt đột ngột lúc tâm trạng 17 % sẽ phản tác dụng.
- **Kho 1 nhận 834 loại** = hố đen. Tách zone riêng cho gỗ/thép/thức ăn để pawn không tha rác vào giữa nhà.

---

## 8. Tóm một câu

> Thuộc địa **không thiếu tài nguyên** (4.848 gỗ, 987 thép, 109 ô lúa sắp chín, 800 bạc) — nó thiếu **người làm việc và một bữa ăn**. Sửa lịch của eistein, nấu 20 suất ăn, dựng 1 ritual spot và 1 chokepoint: 15 phút thao tác đó đổi lấy cả 3 pawn khoẻ mạnh trước vụ đột kích thứ ba.

---

*Số liệu trích từ `dump/state.json` + `dump/report.md` (sinh tự động, 25.464 object; mọi object đều được phân loại, 0 unclassified).*
