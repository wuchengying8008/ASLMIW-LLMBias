import numpy as np
from keras_preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import LSTM, Dense, Embedding
from keras.models import Sequential
from keras.utils import to_categorical
from NLPExtract import text_array_find_order
from keras.models import load_model
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, './Utils'))
from DataBase import getMysqlDataCursor,execute_query
import NLPConstant

def LSTM_Prediction(inputData):
 # 加载标签文本数据
 with open(NLPConstant.LSTM_DEV_PATH, 'r',encoding='utf-8') as file:
    lines  = file.readlines()
 texts=[]
 labels=[]
 for line in lines:
    parts = line.strip().split('\t')
    texts.append(text_array_find_order(parts[0]))
    labels.append(parts[1])
 #texts = ["I love natural language processing", "Deep learning is amazing"]
 #texts = ["市场 经济 不 景气","我 喜欢 自然 语言", "深度 学习 非常 有 意思"]
 #labels = [0, 1, 2]  # 0 表示负面，1 表示正面
 #texts = ["持有 仓位 情况 说明","投资 金额 比例 情况", "股票 最新 行情 信息","最新 行情 数据 信息","行情 数据 查询 信息"]
 #labels = [0, 0, 1, 1,1]  # 0 表示负面，1 表示正面
 tokenizer = Tokenizer(num_words=1000)
 tokenizer.fit_on_texts(texts)
 sequences = tokenizer.texts_to_sequences(texts)
 max_sequence_length = 100
 data = pad_sequences(sequences, maxlen=max_sequence_length)
 #label_binarizer = np.array([[0, 1] if label == 1 else [1, 0] for label in labels])
 label_binarizer = to_categorical(np.array(labels))

 if os.path.exists(NLPConstant.OUT_FILE_PATH+'lstm_model.h5'):
     model=load_model(NLPConstant.OUT_FILE_PATH+'lstm_model.h5')
 else:
   #模型训练
    # 文本特征提取和序列标记
   model = Sequential()
   model.add(Embedding(1000, 8, input_length=max_sequence_length))
   model.add(LSTM(100))
   print("============个数===========")
   print(NLPConstant.LSTM_LABELS_NUM)
   model.add(Dense(NLPConstant.LSTM_LABELS_NUM, activation='softmax'))#标签个数
   model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
   model.fit(data, label_binarizer, epochs=10, verbose=1)
   model.save(NLPConstant.OUT_FILE_PATH + 'lstm_model.h5')
 #模型预测
 #model.evaluate(data, label_binarizer)

 # 使用模型
 #new_text = "language learning is very interest"
 #new_text = "最近 深度 学习 不好"
 #new_text = "最新 股票 600570 恒生 电子 行情 怎么样"
 arr_predict=[]
 for new_text in inputData:
   new_sequence = tokenizer.texts_to_sequences([new_text])[0]
   #new_sequence = pad_sequences(new_sequence, maxlen=max_sequence_length)#np.array(
   new_sequence = pad_sequences([new_sequence])
   prediction = model.predict(new_sequence)
   prediction = np.argmax(model.predict(new_sequence),axis=1)
   print('Predicted class:', prediction[0])
   arr_predict.append(prediction[0])
 return arr_predict;


#listAr=['持有 仓位 情况 说明']#["请 帮 我 分析 下 金融市场"]
#arr=LSTM_Prediction(listAr)
#print(arr)