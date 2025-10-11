import json
import csv
import os

# --- CẤU HÌNH TÊN FILE ---
LEARNING_OBJECTS_JSON_PATH = 'input.json'
QUESTIONS_CSV_PATH = 'questions.csv'
OUTPUT_CSV_PATH = 'questions_mapped.csv' # File đầu ra sẽ có tên này

def create_id_mapping(json_file_path):
    """
    Đọc file JSON của Learning Objects và tạo một dictionary để "dịch"
    từ custom_lo_id (ví dụ: 'LO-C1-01') sang name của Frappe (ví dụ: 'LO-00001').
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            learning_objects = json.load(f)
        
        id_map = {}
        for lo in learning_objects:
            # Key là ID tùy chỉnh, Value là ID (name) của Frappe
            if 'custom_lo_id' in lo and 'name' in lo:
                id_map[lo['custom_lo_id']] = lo['name']
        
        print(f"✅ Đã tạo bản đồ chuyển đổi cho {len(id_map)} Learning Objects.")
        return id_map
    except FileNotFoundError:
        print(f"❌ LỖI: Không tìm thấy file '{json_file_path}'. Hãy đảm bảo bạn đã export và đặt file đúng chỗ.")
        return None
    except Exception as e:
        print(f"❌ LỖI: Có lỗi khi đọc file JSON: {e}")
        return None

def map_csv_data(id_map, input_csv_path, output_csv_path):
    """
    Đọc file questions.csv, thay thế cột learning_object bằng ID đúng,
    và ghi ra một file CSV mới.
    """
    try:
        with open(input_csv_path, 'r', encoding='utf-8') as infile, \
             open(output_csv_path, 'w', encoding='utf-8', newline='') as outfile:
            
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            # Đọc và ghi lại dòng tiêu đề (header)
            header = next(reader)
            writer.writerow(header)
            
            processed_count = 0
            error_count = 0
            
            # Lặp qua từng dòng trong file câu hỏi
            for row in reader:
                if not row: continue # Bỏ qua dòng trống

                custom_id = row[0] # Lấy ID tùy chỉnh từ cột đầu tiên
                
                # "Dịch" ID tùy chỉnh sang ID của Frappe
                frappe_id = id_map.get(custom_id)
                
                if frappe_id:
                    # Nếu tìm thấy, thay thế giá trị trong cột đầu tiên
                    row[0] = frappe_id
                    writer.writerow(row)
                    processed_count += 1
                else:
                    # Nếu không tìm thấy, báo lỗi và bỏ qua dòng này
                    print(f"⚠️ CẢNH BÁO: Không tìm thấy ID của Frappe cho '{custom_id}'. Bỏ qua dòng này.")
                    error_count += 1
            
            print(f"\n✅ Hoàn thành! Đã xử lý {processed_count} câu hỏi.")
            if error_count > 0:
                print(f"⚠️ Có {error_count} dòng bị bỏ qua do không tìm thấy ID tương ứng.")
            print(f"👍 File mới đã được tạo tại: '{output_csv_path}'")

    except FileNotFoundError:
        print(f"❌ LỖI: Không tìm thấy file '{input_csv_path}'.")
    except Exception as e:
        print(f"❌ LỖI: Có lỗi khi xử lý file CSV: {e}")

# --- HÀM CHÍNH ĐỂ CHẠY SCRIPT ---
if __name__ == "__main__":
    print("--- Bắt đầu quá trình chuyển đổi ID cho file câu hỏi ---")
    
    # Kiểm tra xem các file cần thiết có tồn tại không
    if not os.path.exists(LEARNING_OBJECTS_JSON_PATH) or not os.path.exists(QUESTIONS_CSV_PATH):
        print("\n**Vui lòng đảm bảo 2 file sau có trong cùng thư mục với script:**")
        print(f"1. {LEARNING_OBJECTS_JSON_PATH} (Export từ Learning Object List)")
        print(f"2. {QUESTIONS_CSV_PATH} (File chứa ngân hàng câu hỏi của bạn)")
    else:
        # Bước 1: Tạo bản đồ ID
        mapping_dict = create_id_mapping(LEARNING_OBJECTS_JSON_PATH)
        
        # Bước 2: Nếu tạo bản đồ thành công, xử lý file CSV
        if mapping_dict:
            map_csv_data(mapping_dict, QUESTIONS_CSV_PATH, OUTPUT_CSV_PATH)