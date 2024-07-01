import numpy as np
import pandas as pd
import streamlit as st
from loan import banking
from PIL import Image

model_path = './models/model.onnx'
my_model = banking(model_path)

# Đường dẫn tới hình ảnh
image_path = './images/banking.jpg'

# Mở và hiển thị hình ảnh
image = Image.open(image_path)
st.image(image, caption='WELCOME TO THE BANK', use_column_width=True)

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
# Tạo ba cột
col1, col2, col3 = st.columns([1, 7.2, 1])

# Đặt nội dung vào cột giữa (col2)
with col2:
    st.title("Dự đoán khả năng hoàn trả")
    st.write("Nhập thông tin vào các ô dưới đây để dự đoán.")

    in0 = st.radio('Chính sách thẻ: 1 nếu khách hàng đáp ứng đủ các tiêu chí đánh giá rủi ro tín dụng, 0 ngược lại', ['0', '1'])

    in1 = st.radio('Mục đích của khoản vay', ['Hợp nhất nợ', 'Thẻ tín dụng', 'Cải thiện nhà', 'Mua sắm chính',
        'Y tế', 'Nhà', 'Xe', 'Du lịch', 'Kinh doanh nhỏ', 'Di chuyển', 'Năng lượng tái tạo', 'Khác'
    ])
    tmp_in1 = cambred[in1].split(" ")
    in1 = ""
    in1 = "_".join([word.lower() for word in tmp_in1])
    # print(in1)
    
    in2 = st.number_input('Lãi suất của khoản vay')
    # print(in2)

    in3 = st.number_input('Số tiền trả góp hàng tháng mà người vay phải trả', 0)

    in4 = st.number_input('Thu nhập hàng năm', 0)

    in5 = st.number_input('Hệ số nợ trên thu nhập (DTI)')

    in6 = st.number_input('Điểm tín dụng của người vay (FICO)', 0)

    in7 = st.date_input('Ngày được cấp hạn mức tín dụng')

    in8 = st.number_input('Hạn mức tín dụng mà khách hàng trả một khoản phí cam kết cho một tổ chức tài chính để vay tiền và sau đó được phép sử dụng tiền khi cần thiết', 0)

    in9 = st.number_input('Tỉ lệ sử dụng nợ tín dụng (tỉ lệ phần trăm của tổng nợ tín dụng hiện có của người vay đang được sử dụng)')

    in10 = st.number_input('Số lượng các câu hỏi của người vay đối với tổ chức Tài Chính trong 6 tháng qua', 0)

    in11 = st.number_input('Số lần người vay đã quá 30 ngày đến hạn thanh toán trong 2 năm qua', 0)

    in12 = st.radio('Thông tin về lịch sử tín dụng của bên vay (VD: Phá sản, thanh toán trễ hạn)', ['0', '1', '2', '3', '4', '5'])

    if st.button('Submit'):
        # print(str(in7))
        in7_tmp = str(in7).split("-")
        day_in7 = ""
        in7_tmp.reverse()
        length = len(in7_tmp)-1
        for i in range(length):
            day_in7 += in7_tmp[i]
        day_in7 += in7_tmp[length][2:]
        # print(day_in7)
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

        # print(df)
        df_data = pd.DataFrame(df)
        df_test = df_data.iloc[[0]]
        # print(df_test.shape)
        # print(df_test.columns)
        st.write(df_test)
        text = my_model.predict(df_test)
        st.write(text)