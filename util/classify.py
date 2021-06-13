from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import pandas as pd

def classify(X_train, y_train, X_test, y_test):
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X_train, y_train)

    prediction = knn.predict(X_test)
    print(prediction)

    confusion_matrix = pd.crosstab(y_test,prediction)
    #, rownames=['Real'], colnames=['Predicted'], margins=True
    print(confusion_matrix)

    metric = metrics.classification_report(y_test,prediction)
    print(metric)

    return prediction