import json

# Đường dẫn đến file JSON mà bạn đã lưu
file_path = "questions.json"

# Mở và đọc file JSON
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Trường hợp file là một danh sách các object
if isinstance(data, list):
    count = len(data)
    print(f"Số lượng object trong file JSON là: {count}")

# Trường hợp file là object lớn chứa nhiều object con
elif isinstance(data, dict):
    count = len(data)
    print(f"Số lượng object trong file JSON (cấp 1) là: {count}")
else:
    print("Cấu trúc JSON không hợp lệ.")
