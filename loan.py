import onnxruntime, pickle, time
import numpy as np
import pandas as pd

encode = pickle.load(open('./models/OneHotEncoder.pkl', 'rb'))
stand = pickle.load(open('./models/MinMaxScaler.pkl', 'rb'))

class banking(object):
    def __init__(self, model_path = f'./models/model.onnx'):
        self.classes = ["Not Fully Paid", "Fully Paid"]
        self.input_name, self.output_name = self.initialize_model(model_path)

    def initialize_model(self, path):
        so = onnxruntime.SessionOptions()
        so.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.session = onnxruntime.InferenceSession(path, sess_options=so,
                                                    providers=onnxruntime.get_available_providers())
        input_name = self.session.get_inputs()[0].name
        output_name = self.session.get_outputs()[0].name
        return input_name, output_name

    def encoder(self, data_in):
        #data_in.shape[1] = 13
        data = data_in.copy()
        # print(data.shape)
        data.drop('credit_policy', axis=1, inplace=True)
        # Mã hóa object
        data = encode.transform(data)
        
        # Chuẩn hóa
        data = pd.DataFrame(stand.transform(data), columns=data.columns.to_list())
        # print(data.columns)
        
        return data
        
    def predict(self, data):
        input_model = np.array(self.encoder(data)).astype(np.float32)
        # print(input_model.shape)
        result = self.session.run([self.output_name], {self.input_name: input_model})
        # print("result: ", result)
        predicted_value = int(result[0][0])
        label = self.classes[predicted_value]
        return label
    
# if __name__ == '__main__':
#     df = pd.read_csv("loan_data.csv")
#     model_path = "./models/model.onnx"
#     df_test = df.iloc[[0]]
#     print((df_test))
#     print("Label True: ", df_test['not_fully_paid'].values[0])
#     df_test.drop('not_fully_paid', axis=1, inplace=True)
#     df_test = df_test.drop(columns=df_test.columns[0])
#     print((df_test.columns))
#     start = time.time()
#     my_model = banking(model_path)
#     class_num = my_model.predict(df_test)
#     end = time.time()
#     print(class_num)
#     print(end - start)