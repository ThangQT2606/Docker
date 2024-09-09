import pandas as pd
import streamlit as st
from loan import banking
import base64

# Gọi model dự đoán
my_model = banking()

# Đường dẫn tới hình ảnh
image_path = './images/bank.png'

# Mở và hiển thị hình ảnh
def load_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
image_base64 = load_image(image_path)
cambred = {
    'Hợp nhất nợ' : 'Debt consolidation',
    'Thẻ tín dụng' : 'Credit card',
    'Cải thiện nhà' : 'Home improvement',
    'Mua sắm chính' : 'Major purchase',
    'Y tế': 'Medical',
    'Nhà' : 'House',
    'Xe' : 'Car',
    'Du lịch' : 'Vacation',
    'Kinh doanh nhỏ' : 'Small business',
    'Di chuyển' : 'Moving',
    'Năng lượng tái tạo' : 'Renewable energy',
    'Khác' : 'Other'
}

def main():
    st.set_page_config(page_title="https://banking.vn", layout="wide")
    col1, col2, col3 = st.columns([1, 7, 0.5])

    # Đặt nội dung vào cột giữa (col2)
    with col2:
        st.markdown(
            f"""
            <style>
            .main {{
                background-image: url('data:image/png;base64,{image_base64}');
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-position: center;
            }}
            .stButton>button {{
                background-color: #4CAF50;
                color: white;
                border-radius: 12px;
            }}
            .stTextInput>div>div>input, .stNumberInput>div>div>input, .stDateInput>div>div>input {{
                border: 2px solid #4169E1;
                border-radius: 4px;
                color: #FFFFFF;
                padding: 5px 10px;
            }}
            .stTextInput>label, .stRadio>label, .stRadio>div>div>label, .stNumberInput>label, 
            .stDateInput>label, .stSelectbox>label {{
                color: #FFFFFF;
            }}
            .stCheckbox>label {{
                color: #FFFFFF;
            }}
            .stRadio>div>div>label, .stSelectbox>div>div>div>span {{
                color: #FFFFFF !important;
            }}
            .st-selectbox__menu-option:hover, .stRadio>div>div>div:hover {{
                background-color: #4169E1;
                color: #FFFFFF;
            }}
            .stRadio>div>div>label>span {{ /*  Style cho label của radio */
                color: #FFFFFF !important;
            }}
            .st-rw {{ /* Thêm style cho class st-rw */
                color: #FFFFFF !important;
            }}
            .st-mq {{ /* Thêm style cho class st-mq */
                color: #FFFFFF !important;
            }}
            .st-mq>div>div>label>span {{  /*  Style cho lựa chọn của multiselect */
                color: #FFFFFF !important;
            }}
            .custom-label {{ /* Style cho label */
                color: #FFFFFF;
                font-size: 14px; /* Điều chỉnh font size */
                display: inline-block; /* Thay đổi thành inline-block */
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown("""
        <div style="text-align: center;">
            <h1 style="color: #00FF00;">Dự đoán khả năng hoàn trả</h1>
        </div>
        <ul style="color: #FFD700;">
            <li>Nhập thông tin vào các ô dưới đây để dự đoán.</li>
        </ul>
        """, unsafe_allow_html=True)

        in0 = st.selectbox(
            'Chính sách thẻ: 1 nếu khách hàng đáp ứng đủ các tiêu chí đánh giá rủi ro tín dụng, 0 ngược lại', 
            ['0', '1'], 
            format_func=lambda x: x
        )

        st.markdown(
            """
            <span class="custom-label">
                Mục đích của khoản vay:
                (Lưu ý chọn 1 mục mà khoản vay có thể được dùng làm mục đích chính)
            </span>
            """, unsafe_allow_html=True) 
        in1 = st.multiselect(  
            'Dưới đây là các lựa chọn', ['Hợp nhất nợ', 'Thẻ tín dụng', 'Cải thiện nhà', 'Mua sắm chính',
            'Y tế', 'Nhà', 'Xe', 'Du lịch', 'Kinh doanh nhỏ', 'Di chuyển', 'Năng lượng tái tạo', 'Khác'],
            default='Khác'
        )
        tmp_in1 = cambred[in1[0]].split(" ") 
        in1 = "_".join([word.lower() for word in tmp_in1])
        
        in2 = st.number_input('Lãi suất của khoản vay')

        in3 = st.number_input('Số tiền trả góp hàng tháng mà người vay phải trả', 0)

        in4 = st.number_input('Thu nhập hàng năm', 0)

        in5 = st.number_input('Hệ số nợ trên thu nhập (DTI)')

        in6 = st.number_input('Điểm tín dụng của người vay (FICO)', 0)

        in7 = st.date_input('Ngày được cấp hạn mức tín dụng')

        in8 = st.number_input('Hạn mức tín dụng mà khách hàng trả một khoản phí cam kết cho một tổ chức tài chính để vay tiền và sau đó được phép sử dụng tiền khi cần thiết', 0)

        in9 = st.number_input('Tỉ lệ sử dụng nợ tín dụng (tỉ lệ phần trăm của tổng nợ tín dụng hiện có của người vay đang được sử dụng)')

        in10 = st.number_input('Số lượng các câu hỏi của người vay đối với tổ chức Tài Chính trong 6 tháng qua', 0)

        in11 = st.number_input('Số lần người vay đã quá 30 ngày đến hạn thanh toán trong 2 năm qua', 0)

        st.markdown(
            """
            <span class="custom-label" style="display:inline-block;">
                Thông tin về lịch sử tín dụng của bên vay (VD: Phá sản, thanh toán trễ hạn):
            </span>
            """, unsafe_allow_html=True) 
        in12 = st.multiselect(  
            """
            Hãy kiểm tra thật kỹ thông tin dưới đây:
            0: Bên vay không có vấn đề gì về lịch sử tín dụng
            1: Bên vay đã phá sản
            2: Bên vay đã quá hạn thanh toán trong 30 ngày
            3: Bên vay đã quá hạn thanh toán trong 60 ngày
            4: Bên vay đã quá hạn thanh toán trong 90 ngày
            5: Bên vay đã quá hạn thanh toán nhiều hơn 90 ngày
            """, ['0', '1', '2', '3', '4', '5'],
            default=['0']
        )
        in12 = int(in12[0])

        if st.button('Submit'):
            in7_tmp = str(in7).split("-")
            day_in7 = "".join(in7_tmp[::-1])

            df = {
                'credit_policy' : [int(in0)],
                'purpose': [in1],
                'int_rate': [in2],
                'installment': [in3],
                'log_annual_inc': [in4],
                'dti': [in5],
                'fico': [in6],
                'days_with_cr_line': [day_in7],
                'revol_bal': [in8],
                'revol_util': [in9],
                'inq_last_6mths': [in10],
                'delinq_2yrs': [in11],
                'pub_rec': [int(in12)]
            }

            df_data = pd.DataFrame(df)
            df_test = df_data.iloc[[0]]
            st.write(df_test)
            text = my_model.predict(df_test)
            if text == "Not Fully Paid":
                st.error("Xin lỗi, bạn không đủ điều kiện vay tiền.")
            else:
                st.success("Chúc mừng, bạn đã được chấp nhận vay tiền.")

if __name__ == '__main__':
    main()