from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt

"""
函数说明:根据feature_words将文本向量化

Parameters:
    train_data_list - 训练集
    test_data_list - 测试集
    feature_words - 特征集
Returns:
    train_feature_list - 训练集向量化列表
    test_feature_list - 测试集向量化列表
"""


def text_features(text, feature_words):
    text_words = set(text)
    features = [1 if word in text_words else 0 for word in feature_words]
    return features
def TextFeatures(train_data_list, test_data_list, feature_words):
 train_feature_list = [text_features(text, feature_words) for text in train_data_list]
 test_feature_list = [text_features(text, feature_words) for text in test_data_list]
 return train_feature_list, test_feature_list
"""
函数说明:新闻分类器

Parameters:
    train_feature_list - 训练集向量化的特征文本
    test_feature_list - 测试集向量化的特征文本
    train_class_list - 训练集分类标签
    test_class_list - 测试集分类标签
Returns:
    test_accuracy - 分类器精度
"""


def TextClassifier(train_feature_list, test_feature_list, train_class_list, test_class_list):
    classifier = MultinomialNB().fit(train_feature_list, train_class_list)
    test_accuracy = classifier.score(test_feature_list, test_class_list)
    return test_accuracy
if __name__ == '__main__':
# 文本预处理
  folder_path = 'Sample'  # 训练集存放地址
  all_words_list, train_data_list, test_data_list, train_class_list, test_class_list = TextProcessing(folder_path,
                                                                                                    test_size=0.2)

# 生成stopwords_set，断开词汇
stopwords_file = 'stopwords_cn.txt'
stopwords_set = MakeWordsSet(stopwords_file)

test_accuracy_list = []
deleteNs = range(0, 1000, 20)  # 0 20 40 60 ... 980
for deleteN in deleteNs:
    feature_words = words_dict(all_words_list, deleteN, stopwords_set)
train_feature_list, test_feature_list = TextFeatures(train_data_list, test_data_list, feature_words)
test_accuracy = TextClassifier(train_feature_list, test_feature_list, train_class_list, test_class_list)
test_accuracy_list.append(test_accuracy)

plt.figure()
plt.plot(deleteNs, test_accuracy_list)
plt.title('Relationship of deleteNs and test_accuracy')
plt.xlabel('deleteNs')
plt.ylabel('test_accuracy')
plt.show()