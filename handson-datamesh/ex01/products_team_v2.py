# products_team_v2.py
import pandas as pd
from sqlalchemy import create_engine
from contract_enforcer import DataContractEnforcer # Import class vừa viết

db_url = "postgresql://admin:password@localhost:5432/ecommerce_mesh"
engine = create_engine(db_url)

def build_product_data_product():
    print("\n👷 [Products Team] Đang xây dựng Data Product (Phiên bản Pro)...")
    
    # 1. Đọc dữ liệu thô
    df = pd.read_sql("SELECT * FROM products_domain.raw_items", engine)
    
    # Giả lập dữ liệu: Convert Decimal sang Float để khớp với YAML check
    df['price'] = df['price'].astype(float)
    
    # 2. Xử lý logic nghiệp vụ
    df['name_normalized'] = df['name'].str.upper()
    
    # --- TÌNH HUỐNG THỬ NGHIỆM ---
    # Hãy thử tạo ra một dữ liệu sai để xem Contract bắt lỗi:
    # Ví dụ: Một sản phẩm có Category lạ không nằm trong danh sách cho phép
    new_bad_row = pd.DataFrame([{
        'id': 999, 
        'name': 'Alien Artifact', 
        'name_normalized': 'ALIEN ARTIFACT',
        'category': 'SpaceTech',  # Lỗi! YAML chỉ cho phép: Electronics, Clothing...
        'price': 100.0
    }])
    df = pd.concat([df, new_bad_row], ignore_index=True)
    # -----------------------------

    # 3. GỌI CẢNH SÁT CONTRACT (Sử dụng thư viện Cerberus & YAML)
    enforcer = DataContractEnforcer('product_contract.yaml')
    clean_df = enforcer.validate(df)
    
    if clean_df.empty:
        print("💀 Không còn dữ liệu nào hợp lệ để publish!")
        return

    # 4. Công bố dữ liệu sạch
    clean_df[['id', 'name_normalized', 'category', 'price']].to_sql(
        'public_products', 
        engine, 
        schema='products_domain', 
        if_exists='replace', 
        index=False
    )
    print("🚀 [Products Team] Đã công bố dữ liệu sạch thành công!")

if __name__ == "__main__":
    build_product_data_product()
