from sklearn.naive_bayes import GaussianNB


train_data = [('statement1', 0.7), ('statement2', 0.3)]
gnb = GaussianNB()
gnb.fit([[1], [0]], [0.7, 0.3])

# 预测新的语句的概率
# 例如：'statement3'
predicted_probability = gnb.predict_proba([[1]])[0][0]
print(f"Predicted probability for 'statement3': {predicted_probability}")