# Mô phỏng thiết bị IoT ThingsBoard

Dự án này mô phỏng một thiết bị IoT giao tiếp với Nền tảng Đám mây ThingsBoard IoT, thực hiện cung cấp thiết bị (device provisioning) và truyền dữ liệu telemetry sử dụng cả hai giao thức MQTT và HTTP.

## Kết quả

Dự án đã thể hiện thành công khả năng giao tiếp của thiết bị IoT với ThingsBoard sử dụng cả hai giao thức MQTT và HTTP. Dưới đây là các ảnh chụp màn hình hiển thị toàn bộ quy trình:

### Cung cấp thiết bị (Device Provisioning)

![Cung cấp thiết bị](check_connect_thingsboard.png)

Đã cung cấp thành công thiết bị "MyIoTDevice" qua MQTT. Kịch bản kết nối với MQTT broker của ThingsBoard, gửi thông tin xác thực cung cấp và nhận về ACCESS_TOKEN (mã truy cập) để truyền dữ liệu telemetry sau đó.

### Gửi Telemetry qua MQTT

![Truyền Telemetry qua MQTT](datasend_MQTT.png)

Dữ liệu telemetry được truyền qua giao thức MQTT hiển thị các chỉ số cảm biến có đóng dấu thời gian (nhiệt độ, độ ẩm, áp suất, ánh sáng) được gửi đến ThingsBoard với khoảng thời gian 2 giây.

### Trực quan hóa dữ liệu - Dữ liệu MQTT

![Bảng điều khiển ThingsBoard - MQTT](datareceived_Thingsboard_MQTT.png)

Biểu đồ chuỗi thời gian thực hiển thị dữ liệu telemetry nhận được qua MQTT. Biểu đồ hiển thị các giá trị nhiệt độ (xanh dương), áp suất (xanh lá), ánh sáng (đỏ) và độ ẩm (vàng) theo thời gian, xác nhận việc nhập dữ liệu thành công.

### Gửi Telemetry qua HTTP

![Truyền Telemetry qua HTTP](datasend_Thingsboard_HTTP_API.png)

Dữ liệu telemetry được truyền qua HTTP REST API hiển thị các chỉ số cảm biến có đóng dấu thời gian được gửi thành công đến ThingsBoard sử dụng HTTPS trên cổng 443.

### Trực quan hóa dữ liệu - Dữ liệu HTTP

![Bảng điều khiển ThingsBoard - HTTP](Datareceived_Thingsboard_HTT_PAPI.png)

Biểu đồ chuỗi thời gian thực hiển thị dữ liệu telemetry nhận được qua HTTP API. Sự trực quan hóa xác nhận rằng dữ liệu gửi qua HTTP REST API được nhận và hiển thị đúng cách trong ThingsBoard.

## Cấu trúc dự án

```
DevIOT-ThingsBoard/
├── config.py                    # Trình tải cấu hình
├── provision_device.py          # Cung cấp thiết bị qua MQTT
├── send_telemetry_mqtt.py       # Gửi telemetry qua MQTT
├── send_telemetry_http.py       # Gửi telemetry qua HTTP
├── requirements.txt             # Các thư viện phụ thuộc Python
├── .env.example                 # Mẫu biến môi trường
├── .env                         # Biến môi trường của bạn (không được git theo dõi)
├── access_token.txt             # ACCESS_TOKEN đã tạo (được tạo sau khi cung cấp)
└── README.md                    # Tệp này
```

## Tính năng

### 1. Cung cấp thiết bị (MQTT)
- Tự động đăng ký thiết bị mới với ThingsBoard
- Nhận ACCESS_TOKEN để xác thực
- Lưu token để sử dụng trong tương lai

### 2. Gửi Telemetry qua MQTT
- Kết nối với ThingsBoard sử dụng ACCESS_TOKEN
- Gửi dữ liệu cảm biến mô phỏng (nhiệt độ, độ ẩm, áp suất, ánh sáng)
- Truyền dữ liệu thời gian thực

### 3. Gửi Telemetry qua HTTP
- Sử dụng HTTP REST API để gửi dữ liệu telemetry
- Các yêu cầu POST đơn giản với xác thực bằng ACCESS_TOKEN
- Tần suất tin nhắn có thể cấu hình

## Hướng dẫn cài đặt

### Yêu cầu tiên quyết
- Python 3.7 hoặc cao hơn
- Tài khoản ThingsBoard (sử dụng demo.thingsboard.io hoặc instance của riêng bạn)
- Thông tin xác thực cung cấp thiết bị từ ThingsBoard

### Cài đặt

1. Cài đặt các thư viện phụ thuộc Python:
```bash
pip install -r requirements.txt
```

2. Tạo tệp `.env` từ tệp mẫu:
```bash
cp .env.example .env
```

3. Chỉnh sửa `.env` với thông tin xác thực ThingsBoard thực tế của bạn:
```bash
THINGSBOARD_HOST=demo.thingsboard.io
PROVISION_DEVICE_KEY=your_provision_key
PROVISION_DEVICE_SECRET=your_provision_secret
DEVICE_NAME=MyIoTDevice
```

**Lưu ý:** Không bao giờ commit `.env` vào version control (nó đã có trong `.gitignore`).

### Lấy thông tin xác thực cung cấp (Provisioning Credentials)

1. Đăng nhập vào ThingsBoard
2. Đi đến **Device profiles** → Chọn profile của bạn → **Device provisioning**
3. Bật provisioning và ghi lại:
   - Provision device key
   - Provision device secret

## Sử dụng

### Bước 1: Cung cấp thiết bị

Chạy kịch bản cung cấp để đăng ký thiết bị của bạn:

```bash
python provision_device.py
```

Việc này sẽ:
- Kết nối đến ThingsBoard MQTT broker
- Gửi yêu cầu cung cấp
- Nhận và lưu ACCESS_TOKEN vào `access_token.txt`

### Bước 2: Gửi Telemetry qua MQTT

```bash
python send_telemetry_mqtt.py
```

Bạn sẽ được nhắc nhập:
- Số lượng tin nhắn muốn gửi
- Khoảng thời gian giữa các tin nhắn

Kịch bản sẽ gửi dữ liệu cảm biến mô phỏng đến ThingsBoard.

### Bước 3: Gửi Telemetry qua HTTP

```bash
python send_telemetry_http.py
```

Tương tự như MQTT, nhưng sử dụng yêu cầu HTTP POST để thay thế.

## Định dạng dữ liệu Telemetry

Các chương trình gửi dữ liệu cảm biến mô phỏng:

```json
{
  "temperature": 25.34,
  "humidity": 65.21,
  "pressure": 1013.45,
  "light": 75
}
```

## Xác minh

Sau khi chạy các chương trình:

1. Đăng nhập vào ThingsBoard
2. Điều hướng đến **Devices**
3. Tìm thiết bị của bạn (ví dụ: "MyIoTDevice")
4. Kiểm tra **Latest telemetry** để xem dữ liệu đã nhận
5. Xem dữ liệu trên dashboard hoặc tạo các trực quan hóa

## Khắc phục sự cố

### Vấn đề kết nối
- Xác minh `THINGSBOARD_HOST` trong tệp `.env`
- Kiểm tra cài đặt tường lửa cho cổng 1883 (MQTT) và 443 (HTTPS)
- Đảm bảo có kết nối internet

### Cung cấp thất bại
- Xác minh thông tin xác thực cung cấp là chính xác
- Kiểm tra xem cung cấp thiết bị đã được bật trong ThingsBoard chưa
- Đảm bảo tên thiết bị chưa tồn tại

### Không nhận được dữ liệu
- Xác minh ACCESS_TOKEN là chính xác
- Kiểm tra trạng thái thiết bị trên ThingsBoard
- Xem nhật ký ThingsBoard để tìm lỗi

## Thư viện phụ thuộc

- `paho-mqtt`: Thư viện client MQTT
- `requests`: Thư viện client HTTP

## Giấy phép

Dự án này dành cho mục đích giáo dục như một phần của khóa học IoT.

## Tác giả

Được tạo cho Khóa học Lập trình IoT - Bài tập 9
