import json

def map_lesson_titles(input_filepath, output_filepath):
    """
    Đọc tệp learning_object.json, ánh xạ lại các giá trị của 'lesson_title'
    dựa trên một bộ quy tắc định sẵn và lưu kết quả vào một tệp mới.
    """
    mapping_rules = {
        "Căn bậc hai và căn bậc ba của số thực": "LESSON-00006",
        "Một số phép tính về căn thức bậc hai của số thực": "LESSON-00007",
        "Căn thức bậc hai và căn thức bậc ba của biểu thức đại số": "LESSON-00008",
        "Một số phép biến đổi căn thức bậc hai của biểu thức đại số": "LESSON-00009"
    }

    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            learning_objects = json.load(f)

        updated_count = 0
        for lo in learning_objects:
            current_title = lo.get("lesson_title", "")
            
            for keyword, new_title in mapping_rules.items():
                if keyword in current_title:
                    lo["lesson_title"] = new_title
                    updated_count += 1
                    break 

        # Ghi dữ liệu đã cập nhật vào tệp mới
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(learning_objects, f, ensure_ascii=False, indent=2)

        print(f"Hoàn thành! Đã xử lý {len(learning_objects)} đối tượng và cập nhật {updated_count} mục.")
        print(f"Dữ liệu đã được cập nhật và lưu vào tệp: '{output_filepath}'")

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy tệp '{input_filepath}'.")
        print("Vui lòng đảm bảo tệp này tồn tại trong cùng thư mục với script.")
    except json.JSONDecodeError:
        print(f"Lỗi: Tệp '{input_filepath}' không phải là một tệp JSON hợp lệ.")
    except Exception as e:
        print(f"Đã xảy ra một lỗi không mong muốn: {e}")


input_json_file = '3-learning_object.json'


output_json_file = '3-learning_object_updated.json'

# Gọi hàm để thực hiện việc ánh xạ
map_lesson_titles(input_json_file, output_json_file)