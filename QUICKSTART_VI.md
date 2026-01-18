# Hướng dẫn bắt đầu nhanh

## Trước khi bắt đầu

Bạn cần lấy thông tin xác thực cung cấp (provisioning credentials) từ ThingsBoard trước.

### Lấy thông tin xác thực từ ThingsBoard:

1. Truy cập https://demo.thingsboard.io (hoặc instance ThingsBoard của bạn)
2. Đăng nhập vào tài khoản của bạn
3. Điều hướng đến: **Device profiles** → **default** (hoặc profile của bạn)
4. Nhấn vào tab **Device provisioning**
5. Bật "Allow device creation" nếu chưa được bật
6. Sao chép các giá trị sau:
   - **Provision device key**
   - **Provision device secret**

## Các bước cấu hình

1. Mở tệp `.env` và cập nhật:
```bash
THINGSBOARD_HOST=demo.thingsboard.io
PROVISION_DEVICE_KEY=dán_key_của_bạn_vào_đây
PROVISION_DEVICE_SECRET=dán_secret_của_bạn_vào_đây
DEVICE_NAME=MyTestDevice
```

**Quan trọng:** Không bao giờ chia sẻ hoặc commit tệp `.env` của bạn!

## Chạy chương trình

### 1. Cung cấp thiết bị (Lấy ACCESS_TOKEN)
```bash
python provision_device.py
```

Kết quả mong đợi:
```
✓ Connected to ThingsBoard MQTT Broker
✓ Device provisioned successfully!
✓ ACCESS_TOKEN: xxxxxxxxxx
✓ Token saved to access_token.txt
```

### 2. Gửi dữ liệu qua MQTT
```bash
python send_telemetry_mqtt.py
```

Bạn sẽ được hỏi:
- How many messages? (số lượng tin nhắn, mặc định: 5)
- Interval? (khoảng thời gian, mặc định: 2 giây)

### 3. Gửi dữ liệu qua HTTP
```bash
python send_telemetry_http.py
```

Các câu hỏi nhắc tương tự như phiên bản MQTT.

## Xác minh trên ThingsBoard

1. Vào trang **Devices**
2. Tìm thiết bị của bạn (ví dụ: "MyTestDevice")
3. Nhấn vào nó
4. Vào tab **Latest telemetry**
5. Bạn sẽ thấy: temperature (nhiệt độ), humidity (độ ẩm), pressure (áp suất), light (ánh sáng)

## Các vấn đề thường gặp

**"Connection refused" (Từ chối kết nối)**
- Kiểm tra xem `THINGSBOARD_HOST` có đúng không
- Xác minh kết nối internet
- Thử `demo.thingsboard.io` nếu đang dùng máy chủ demo

**"Provisioning failed" (Cung cấp thất bại)**
- Kiểm tra kỹ provision key và secret
- Đảm bảo device provisioning đã được bật
- Tên thiết bị có thể đã tồn tại (hãy thử tên khác)

**"No ACCESS_TOKEN" (Không có ACCESS_TOKEN)**
- Chạy `provision_device.py` trước
- Kiểm tra xem `access_token.txt` đã được tạo chưa

## Các tệp trong dự án

- `.env` - Cấu hình (SỬA CÁI NÀY ĐẦU TIÊN)
- `.env.example` - Mẫu cho tệp .env
- `config.py` - Tải cấu hình từ .env
- `provision_device.py` - Lấy ACCESS_TOKEN
- `send_telemetry_mqtt.py` - Gửi qua MQTT
- `send_telemetry_http.py` - Gửi qua HTTP
- `access_token.txt` - Token tự động tạo (đừng sửa)
