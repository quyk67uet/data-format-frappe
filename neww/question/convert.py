import json
import pandas as pd

def convert_questions_json_to_csv(json_file_path, csv_file_path):
    """
    Chuyển đổi tệp JSON chứa danh sách các câu hỏi thành tệp CSV
    phù hợp để import vào Frappe Desk.

    Hàm này sẽ làm sạch các ký tự xuống dòng trong các trường văn bản
    để đảm bảo mỗi câu hỏi nằm trên một dòng duy nhất.
    """
    try:
        # Đọc và tải dữ liệu từ tệp JSON
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        df = pd.DataFrame(data)

        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.replace(r'\r|\n', ' ', regex=True)

        column_order = ['learning_object', 'question_text', 'suggested_solution', 'difficulty']
        existing_columns = [col for col in column_order if col in df.columns]
        df = df[existing_columns]

        # Xuất DataFrame ra tệp CSV
        df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
        print(f"Đã chuyển đổi thành công tệp '{json_file_path}' thành '{csv_file_path}'")

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy tệp '{json_file_path}'")
    except json.JSONDecodeError:
        print(f"Lỗi: Tệp '{json_file_path}' không phải là một tệp JSON hợp lệ.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")


# Ví dụ về cách gọi hàm
json_input_path = '8_questions.json'
csv_output_path = 'questions_8.csv'
convert_questions_json_to_csv(json_input_path, csv_output_path)