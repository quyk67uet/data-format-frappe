import csv
import json
import re

def roman_to_int(s):
    """Hàm phụ để chuyển số La Mã thành số nguyên."""
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    for i in range(len(s)):
        if i > 0 and roman_map[s[i]] > roman_map[s[i-1]]:
            result += roman_map[s[i]] - 2 * roman_map[s[i-1]]
        else:
            result += roman_map[s[i]]
    return result

def process_chapter_data(csv_file_path, master_lessons_filepath):
    """
    Đọc tệp CSV của một chương và tệp JSON master.
    1. Tạo tệp lessons.json cho riêng chương đó.
    2. Tạo tệp learning_object.json với lesson_title được ánh xạ sang lesson_id.
    """
    try:
        with open(master_lessons_filepath, 'r', encoding='utf-8') as f:
            master_lessons = json.load(f)

        def clean_content(cell_text):
            cleaned_text = cell_text.strip(' .') 
            return " ".join(cleaned_text.split())

        lesson_title_to_id_map = {
            clean_content(lesson['lesson_title']): lesson['lesson_id']
            for lesson in master_lessons
        }

        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)

            first_line = next(reader)[0]
            topic_id = 1
            match = re.search(r'CHƯƠNG\s+([IVXLCDM]+)', first_line, re.IGNORECASE)
            if match:
                roman_numeral = match.group(1).upper()
                topic_id = roman_to_int(roman_numeral)

            next(reader)
            
            lessons_for_this_chapter = []
            learning_objects = []
            seen_lesson_titles = set()
            current_lesson_title = ""
            lesson_counter = 0

            for row in reader:
                if not any(row):
                    continue

                raw_lesson_title = row[0].strip()
                if raw_lesson_title:
                    current_lesson_title = clean_content(raw_lesson_title)
                    
                    if current_lesson_title not in seen_lesson_titles:
                        seen_lesson_titles.add(current_lesson_title)
                        lesson_counter += 1
                        lessons_for_this_chapter.append({
                            "lesson_title": current_lesson_title,
                            "topic": topic_id,
                            "lesson_number": lesson_counter
                        })
            
                lesson_id = lesson_title_to_id_map.get(current_lesson_title)
                
                if not lesson_id:
                    print(f"Cảnh báo: Không tìm thấy ID cho bài học '{current_lesson_title}' trong tệp master.")

                lo = {
                    "custom_lo_id": clean_content(row[1]),
                    "learning_object_title": clean_content(row[2]),
                    "cognitive_level": clean_content(row[3]),
                    "description": clean_content(row[4]),
                    "objective": clean_content(row[5]),
                    "lesson_title": lesson_id
                }
                learning_objects.append(lo)

        chapter_num_match = re.search(r'chuong-(\d+)', csv_file_path)
        chapter_prefix = chapter_num_match.group(1) if chapter_num_match else "output"

        # Ghi tệp lessons cho chương hiện tại
        lessons_output_filename = f"/content/drive/MyDrive/isy_data/{chapter_prefix}-lessons.json"
        with open(lessons_output_filename, 'w', encoding='utf-8') as f:
            json.dump(lessons_for_this_chapter, f, ensure_ascii=False, indent=2)
        print(f"Tạo thành công tệp '{lessons_output_filename}'")

        # Ghi tệp learning objects đã được ánh xạ
        lo_output_filename = f"/content/drive/MyDrive/isy_data/{chapter_prefix}-learning_object.json"
        with open(lo_output_filename, 'w', encoding='utf-8') as f:
            json.dump(learning_objects, f, ensure_ascii=False, indent=2)
        print(f"Tạo thành công tệp '{lo_output_filename}' với lesson_id đã được ánh xạ.")

    except FileNotFoundError as e:
        print(f"Lỗi: Không tìm thấy tệp. Vui lòng kiểm tra lại đường dẫn: {e.filename}")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

# --- Sử dụng ---

# Đường dẫn đến tệp CSV của chương bạn muốn xử lý
csv_input_path = '/content/drive/MyDrive/isy_data/chuong-1.csv' 

# Đường dẫn đến tệp JSON "tổng" chứa tất cả ID của các bài học
master_lessons_file = '/content/drive/MyDrive/isy_data/lessons_with_ids.json'

# Gọi hàm để xử lý tệp
process_chapter_data(csv_input_path, master_lessons_file)
