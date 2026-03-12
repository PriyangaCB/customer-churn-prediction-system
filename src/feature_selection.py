from sklearn.feature_selection import SelectKBest, f_classif

# Feature selection using SelectKBest 
def select_features(X,y,k=10):
    # if dataset has fewer columns than k
    if X.shape[1] < k:
        k = "all"

    selector = SelectKBest(score_func=f_classif,k=k)

    X_new = selector.fit_transform(X,y)
    
    return X_new,selector