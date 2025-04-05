import numpy as np

def mwmote(X, y, n_neighbors=5, n_synthetic=1):
    """
    MWMOTE。
    """
    n_classes = np.unique(y).size
    if n_classes != 2:
        raise ValueError("MWMOTE is designed for binary classification problems.")
    
   
    majority, minority = np.where(y == 1), np.where(y == 0)
    X_majority, X_minority = X[majority], X[minority]
    n_minority = X_minority.shape
    
   
    X_new = np.zeros((n_synthetic * n_minority, X.shape‌:ml-citation{ref="1" data="citationList"}))
    for i in range(n_minority):
       
        distances = np.sqrt(np.sum((X_minority[i] - X_minority) ** 2, axis=1))
        k_indices = np.argsort(distances)[:n_neighbors]
        k_neighbors = X_minority[k_indices]
        weights = np.random.dirichlet(‌:ml-citation{ref="1" data="citationList"} * n_neighbors) * (1 / n_neighbors)  
        weights /= weights.sum()  #
       
        for j in range(n_synthetic):
            synthetic = X_minority[i] + np.dot(weights, k_neighbors - X_minority[i]) + np.random.randn(1, X.shape‌:ml-citation{ref="1" data="citationList"}) * 0.1  # 添加噪声
            X_new[i * n_synthetic + j] = synthetic.ravel()  
    return X_new
