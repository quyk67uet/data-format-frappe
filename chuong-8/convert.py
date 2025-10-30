import json
import csv

# File đầu vào và đầu ra
input_file = "8-lessons.json"
output_file = "8-lessons.csv"

# Đọc dữ liệu từ JSON
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Lấy các trường từ phần tử đầu tiên
fieldnames = data[0].keys()

# Ghi ra file CSV
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"Đã chuyển {input_file} thành {output_file} thành công!")
