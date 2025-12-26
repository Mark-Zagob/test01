# contract_enforcer.py
import yaml
from cerberus import Validator
import pandas as pd

class DataContractEnforcer:
    def __init__(self, contract_path):
        # 1. Đọc file cấu hình YAML
        with open(contract_path, 'r') as f:
            self.contract_config = yaml.safe_load(f)
        
        # 2. Khởi tạo Validator của Cerberus với schema đã định nghĩa
        self.validator = Validator(self.contract_config['schema'])
        # Cho phép các cột lạ (extra fields) nếu cần, hoặc cấm tiệt bằng allow_unknown=False
        self.validator.allow_unknown = True 

    def validate(self, df):
        print(f"👮 [Contract] Bắt đầu kiểm tra {len(df)} dòng dữ liệu...")
        
        # Chuyển DataFrame thành list of dicts để Cerberus kiểm tra từng dòng
        records = df.to_dict(orient='records')
        
        valid_records = []
        error_count = 0
        
        for record in records:
            # Kiểm tra từng dòng
            if self.validator.validate(record):
                valid_records.append(record)
            else:
                error_count += 1
                # In ra lỗi chi tiết (chỉ in 3 lỗi đầu tiên cho đỡ rối)
                if error_count <= 3:
                    print(f"   ❌ Lỗi tại dòng ID {record.get('id', 'Unknown')}: {self.validator.errors}")

        if error_count > 0:
            print(f"⚠️ CẢNH BÁO: Phát hiện {error_count} dòng vi phạm hợp đồng!")
            
            # --- QUYẾT ĐỊNH CỦA DOANH NGHIỆP ---
            # Cách 1: Strict Mode (Chặt chẽ) -> Dừng luôn nếu có bất kỳ lỗi nào
            # raise Exception("Data Contract Violation: Pipeline Stopped!")
            
            # Cách 2: Filter Mode (Lọc bỏ) -> Chỉ giữ lại dòng đúng (Ta dùng cách này cho bài Lab)
            print(f"   -> Đã loại bỏ {error_count} dòng lỗi. Tiếp tục với {len(valid_records)} dòng sạch.")
            
        else:
            print("✅ TUYỆT VỜI: 100% dữ liệu tuân thủ hợp đồng.")

        # Trả về DataFrame sạch
        return pd.DataFrame(valid_records)
