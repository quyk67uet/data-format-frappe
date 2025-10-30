import json
import pandas as pd
import random 

def convert_json_to_csv_for_frappe(json_file_path, csv_file_path):
    """
    Chuyển đổi tệp JSON thành tệp CSV với định dạng "cha-con" cho Frappe.
    - Các thẻ "Sắp xếp các bước" sẽ có các bước được xáo trộn ngẫu nhiên.
    - Các thẻ khác sẽ được làm sạch và nằm trên một dòng duy nhất.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        column_names = [
            'flashcard_type', 'topic', 'learning_object', 'level', 'question', 'answer',
            'explanation', 'hint', 'ordering_steps_items.step_content',
            'ordering_steps_items.correct_order'
        ]
        all_rows = []

        for card in data:
            card_type = card.get('flashcard_type', '')

            if card_type in ['Sắp xếp các bước', 'Ordering Steps']:
                parent_row = {
                    'flashcard_type': card.get('flashcard_type', ''),
                    'topic': card.get('topic_id', card.get('topic', '')),
                    'learning_object': card.get('learning_object', ''),
                    'level': card.get('level', ''),
                    'question': card.get('question', ''),
                    'answer': card.get('answer', ''),
                    'explanation': card.get('explanation', ''),
                    'hint': card.get('hint', ''),
                    'ordering_steps_items.step_content': '',
                    'ordering_steps_items.correct_order': ''
                }
                all_rows.append(parent_row)

                steps = card.get('ordering_steps_items', [])
                if steps:
                    random.shuffle(steps)

                    for step in steps:
                        child_row = {
                            'flashcard_type': '', 'topic': '', 'learning_object': '', 'level': '', 'question': '',
                            'answer': '', 'explanation': '', 'hint': '',
                            'ordering_steps_items.step_content': step.get('step_content', ''),
                            'ordering_steps_items.correct_order': step.get('correct_order', '')
                        }
                        all_rows.append(child_row)
            else:
                single_row = {
                    'flashcard_type': card.get('flashcard_type', ''),
                    'topic': card.get('topic_id', card.get('topic', '')),
                    'learning_object': card.get('learning_object', ''),
                    'level': card.get('level', ''),
                    'question': card.get('question', ''),
                    'answer': card.get('answer', ''),
                    'explanation': card.get('explanation', ''),
                    'hint': card.get('hint', ''),
                    'ordering_steps_items.step_content': '',
                    'ordering_steps_items.correct_order': ''
                }
                for key, value in single_row.items():
                    if isinstance(value, str):
                        single_row[key] = ' '.join(value.replace('\r', ' ').split())
                all_rows.append(single_row)

        df_final = pd.DataFrame(all_rows, columns=column_names)
        df_final.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
        print(f"Đã chuyển đổi thành công tệp '{json_file_path}' thành '{csv_file_path}' với định dạng Frappe và các bước đã được xáo trộn.")

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy tệp '{json_file_path}'")
    except json.JSONDecodeError:
        print(f"Lỗi: Tệp '{json_file_path}' không phải là một tệp JSON hợp lệ.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

# --- Hướng dẫn sử dụng ---
json_input_path = '8_flashcards.json'
csv_output_path = 'flashcard_8.csv'
convert_json_to_csv_for_frappe(json_input_path, csv_output_path)