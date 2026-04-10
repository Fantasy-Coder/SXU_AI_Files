from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

data = load_breast_cancer()
X = data.data
y = data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler() 
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)


y_pred = knn.predict(X_test)

print("分类报告:\n", classification_report(y_test, y_pred))
print("混淆矩阵:\n", confusion_matrix(y_test, y_pred))
print("准确率: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))



from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


X, y = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)
kmeans = KMeans(n_clusters=4)
y_kmeans = kmeans.fit_predict(X)


plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

centers = kmeans.cluster_centers_ 
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.75) 
plt.title('K-means Clustering')
plt.xlabel('characteristic 1')
plt.ylabel('characteristic 2')
plt.show()



from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE 
X, y = make_classification(n_samples=1000, n_features=20, n_informative=2, n_redundant=10, n_clusters_per_class=1, weights=[0.95], flip_y=0, random_state=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)


classifier = RandomForestClassifier(random_state=42)
classifier.fit(X_train_res, y_train_res)


y_pred = classifier.predict(X_test)
print("处理不平衡数据后的分类报告:\n", classification_report(y_test, y_pred))


from sklearn.decomposition import PCA
import numpy as np


np.random.seed(42) 
X = np.random.randn(300, 10)


pca = PCA(n_components=2)  
X_pca = pca.fit_transform(X) 

print("原始数据的形状:", X.shape)
print("降维后的数据形状:", X_pca.shape)


import pandas as pd

data = {'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 32, 37, 45],
        'Gender': ['F', 'M', 'M', 'M'],
        'Medical_History': ['None', 'Diabetes', 'Hypertension', 'None']}

df = pd.DataFrame(data)
print("原始数据集:\n", df)

df_anonymous = df.drop(columns=['Name'])
print("\n匿名化后的数据集:\n", df_anonymous)
