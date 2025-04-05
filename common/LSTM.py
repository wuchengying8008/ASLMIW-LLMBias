from keras_preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import LSTM, Dense, Embedding
from keras.models import Sequential
from keras.api.models import Model
from keras import layers, models, callbacks
from keras.utils import to_categorical
from keras import backend as K
import numpy as np

# 示例数据
texts = [
    "上课课很开心",
    "经济下滑",
    "今天踢足球",
    "社会经济不好","市场萎缩","GDP下滑","生活指数不景气","经济往下走"
]
labels = [0, 1, 0, 1,1,1,1,1]  # 0代表"体育"，1代表"经济"
texts2 = ["今天踢足球"]
# 文本向量化
tokenizer = Tokenizer(num_words=1000)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
print('sample_data:',sequences)
tokenizer2 = Tokenizer(num_words=1000)
#tokenizer2.fit_on_texts(texts2)
sequences2 = tokenizer.texts_to_sequences(texts2)

print('sample_data2:',sequences2)
#print('sample_data2:',sequences2)

word_index = tokenizer.word_index
print('Word index:', word_index)
data = pad_sequences(sequences)
labels = to_categorical(np.array(labels))

# 创建模型
model = Sequential()
model.add(Embedding(1000, 8, input_length=data.shape[1]))
model.add(LSTM(100))
model.add(Dense(2, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(data, labels, epochs=10, verbose=1)

#sample_data = sequences[0]
#max_sequence_length=100
#new_text = ["我国经济下滑"]
#new_sequence = tokenizer.texts_to_sequences([new_text])[0]
#new_sequence = pad_sequences(np.array(new_sequence), maxlen=max_sequence_length)
# prediction = model.predict(new_sequence)
sample_data = sequences2[0]
sample_data = pad_sequences([sample_data])
#y_pred = np.argmax(model.predict(sample_data),axis=1)
print("预测概率：",model.predict(sample_data))
y_pred = np.argmax(model.predict(sample_data),axis=1)
print('Predicted class:', y_pred[0])