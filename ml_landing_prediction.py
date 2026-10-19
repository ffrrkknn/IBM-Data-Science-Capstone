import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


# Karmaşıklık Matrisi (Confusion Matrix) Çizim Fonksiyonu
def plot_confusion_matrix(y, y_predict, title='Confusion Matrix'):
  cm = confusion_matrix(y, y_predict)
  ax = plt.subplot()
  sns.heatmap(cm, annot=True, ax=ax, cmap='Blues')
  ax.set_xlabel('Predicted labels')
  ax.set_ylabel('True labels')
  ax.set_title(title)
  ax.xaxis.set_ticklabels(['did not land', 'land'])
  ax.yaxis.set_ticklabels(['did not land', 'landed'])
  plt.show()


# Veri Setlerinin Yüklenmesi
URL1 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv'
data = pd.read_csv(URL1)

URL2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv'
X = pd.read_csv(URL2)

# ==========================================
# TASK 1: Target Variable (Y) Creation
# ==========================================
Y = data['Class'].to_numpy()

# ==========================================
# TASK 2: Standardize the Data (X)
# ==========================================
transform = preprocessing.StandardScaler()
X = transform.fit_transform(X)

# ==========================================
# TASK 3: Train / Test Split
# ==========================================
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=2
)
print(f'Test örneklem sayısı: {Y_test.shape[0]}')

# ==========================================
# TASK 4 & 5: Logistic Regression
# ==========================================
parameters_lr = {'C': [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}
lr = LogisticRegression()
logreg_cv = GridSearchCV(lr, parameters_lr, cv=10)
logreg_cv.fit(X_train, Y_train)

print(
    '\n[Logistic Regression] Best Parameters:', logreg_cv.best_params_
)  # cite: 14
print(f'[Logistic Regression] Train Accuracy (CV): {logreg_