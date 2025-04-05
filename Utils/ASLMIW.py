import numpy as np
'''
1) different investor groups are classified;
2) templates are designed for different investment scenarios; 
3) the initial values of LLM bias probabilities are determined, 
and weights are assigned to samples that generate bias probabilities; 
4) static characteristic factors of the selected groups are identified,
 and the data sampling probabilities of imbalanced datasets are adjusted 
 through the weight assignment process to promote self-balancing of the training sample data; 
5) dynamic characteristic factors of the groups are identified, 
and new samples are randomly generated for severely sparse data by 
introducing perturbation signals; the amplitude control is used to manage sample deviation; 
6) special adjustments are made for financially vulnerable groups, such as novice investors, 
elderly investors, and information-disadvantaged groups, and specific labeled data are added 
to the existing dataset for individuals with certain special attributes; 
7) the LLM bias is controlled using the loss function to constrain the execution
behavior of the LLMs and improve model accuracy.
'''

def ASLMIWLLMBias(X, y, n_neighbors=5, n_synthetic=1,file,senario):
    """
    ASLMIWLLMBias
    """
    n_classes = np.unique(y).size
    if n_classes != 2:
        raise ValueError("ASLMIWLLMBias is designed for binary classification problems.")
    majority, minority = np.where(y == 1), np.where(y == 0)
    X_majority, X_minority = getDatafromSQLUtile('majority','minority')
    importtanceSize,biasWeigeht=getBiasandImporantSizefromTemplate(file,senario)
    X_minority_static=getMinorityStaticFactor(X_minority)#get static factors
    n_minority_s = X_minority_static.shape
    n_minority_dynamic=getMinorityDynamicFactor(X_minority)
    n_minority_dynamic=PerturbationLearning(n_minority_dynamic)
    n_minority_d = n_minority_dynamic.shape
    n_minority_new=combineFactors(n_minority_s,n_minority_d)
    X_new = np.zeros((n_synthetic * n_minority_new, X.shape‌:ml-citation{ref="1" data="citationList"}))
    for i in range(n_minority_new):
        distances = np.sqrt(np.sum((X_minority[i] - X_minority) ** 2, axis=1))
        k_indices = np.argsort(distances)[:n_neighbors]
        k_neighbors = X_minority[k_indices]
        weights = np.random.dirichlet(‌:ml-citation{ref="1" data="citationList"} * n_neighbors) * (1 / n_neighbors)  
        weights /= weights.sum()  #
       
        for j in range(n_synthetic):
            synthetic = X_minority[i] + np.dot(weights, k_neighbors - X_minority[i]) + np.random.randn(1, X.shape‌:ml-citation{ref="1" data="citationList"}) * 0.1  # 添加噪声
            X_new[i * n_synthetic + j] = synthetic.ravel()  
    return X_new
