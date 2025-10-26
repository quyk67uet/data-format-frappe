import json
import csv

# Đọc file JSON
with open('3-learning_object_updated.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Tạo file CSV
with open('3-learning_object.csv', 'w', newline='', encoding='utf-8') as csv_file:
    # Lấy các khóa (keys) từ phần tử đầu tiên làm tiêu đề cột
    fieldnames = data[0].keys()
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Ghi tiêu đề và nội dung
    writer.writeheader()
    writer.writerows(data)

print("✅ Đã chuyển đổi thành công sang 3-learning_object.csv")
