import json

def assign_sequential_lesson_ids(input_filepath, output_filepath):
    """
    Đọc một tệp JSON chứa danh sách các bài học, gán ID tuần tự cho mỗi bài,
    và lưu kết quả vào một tệp JSON mới.
    """
    try:
        # Đọc tệp JSON đầu vào chứa danh sách các bài học
        with open(input_filepath, 'r', encoding='utf-8') as f:
            lessons = json.load(f)

        # Danh sách mới để lưu các bài học đã được cập nhật
        updated_lessons = []
        
        # Sử dụng enumerate để có được chỉ số (bắt đầu từ 1) cho mỗi bài học
        for index, lesson in enumerate(lessons, 1):
            # Tạo lesson_id với định dạng 5 chữ số, có số 0 ở đầu
            # Ví dụ: 1 -> "00001", 10 -> "00010"
            lesson_id = f"LESSON-{index:05d}"
            
            # Tạo một dictionary mới với thứ tự key mong muốn
            updated_lesson = {
                "lesson_id": lesson_id,
                "lesson_title": lesson["lesson_title"],
                "topic": lesson["topic"]
            }
            updated_lessons.append(updated_lesson)

        # Ghi danh sách đã cập nhật vào tệp JSON đầu ra
        with open(output_filepath, 'w', encoding='utf-8') as f:
            # indent=2 để file JSON dễ đọc
            # ensure_ascii=False để hiển thị đúng tiếng Việt
            json.dump(updated_lessons, f, ensure_ascii=False, indent=2)

        print(f"Hoàn thành! Đã gán ID cho {len(updated_lessons)} bài học.")
        print(f"Kết quả đã được lưu vào tệp: '{output_filepath}'")

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy tệp '{input_filepath}'. Vui lòng kiểm tra lại đường dẫn.")
    except json.JSONDecodeError:
        print(f"Lỗi: Tệp '{input_filepath}' không phải là một tệp JSON hợp lệ.")
    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn: {e}")

# --- Hướng dẫn sử dụng ---

# 1. Tạo một tệp có tên `all_lessons.json` và dán nội dung JSON bạn đã cung cấp vào đó.
#    Nội dung tệp `all_lessons.json`

# 2. Lưu đoạn mã Python trên vào một tệp, ví dụ: `generate_lesson_ids.py`.
#    Hãy chắc chắn hai tệp này nằm trong cùng một thư mục.

# 3. Chạy script từ terminal: python generate_lesson_ids.py

# --- Cấu hình tên tệp ---
input_file = 'all_lessons.json'
output_file = 'lessons_with_ids.json'

# Gọi hàm để thực thi
assign_sequential_lesson_ids(input_file, output_file)