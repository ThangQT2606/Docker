import onnx
import pickle
import skl2onnx
from skl2onnx.common.data_types import FloatTensorType
model = pickle.load(open('model.pkl', 'rb'))
# Xác định kiểu dữ liệu đầu vào cho mô hình ONNX
initial_type = [('float_input', FloatTensorType([None, 23]))]
onnx_model = skl2onnx.convert_sklearn(model, initial_types=initial_type)
output_model_path = "model.onnx"
onnx.save(onnx_model, output_model_path)