import numpy as np
'''
Special groups were dispersed across various populations, with a relatively small number and 
a low distribution density. The characteristics of investors in the special groups did not 
exhibit significant anomalies compared to the other groups. For the special groups, special 
adjustments were performed by adding specific factors.
This method is the main framework of special learning.
'''
'''
return the new combineSyntheticSpecialgroup
'''
def SpecialLearn(X, y, n_neighbors=5, n_synthetic=1,file,senario):
    """
    SpecailLearning
    """
    samples =ASLMIWLLMBias(file,senario)
    specialTags,specialInvestors=getSpectialGroup(senario)
    for i in range(len(specialInvestors)):
     specialOne=convertTagInvestor(specialInvestors[i].shape)
       for j in range(len(specialTags)):
         converTagsList(specialOne,specialTags)
    X_new = combineSyntheticSpecial((samples,specialInvestors)
    for i in range(X_new):
       if check(X_new[i]) not in specialInvestors:
          reCombine(X_new[i]);
    return X_new
