import pandas
import matplotlib.pyplot as mpt
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

filename = "iris.data"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = pandas.read_csv(filename, names = names)

# Split-out validation dataset
array = dataset.values
X = array[:, 0: 4]
Y = array[:, 4]
validation_size = 0.2
seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size = validation_size, random_state = seed)

# Check algorithms
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))

# Evaluate each model
results = []
names = []
for name, model in models:
    kfold = model_selection.KFold(n_splits = 10, random_state = seed)
    res = model_selection.cross_val_score(model, X_train, Y_train, cv = kfold, scoring = 'accuracy')
    results.append(res)
    names.append(name)
    msg = "%s: %f (%f)" % (name, res.mean(), res.std())
    print msg

# Compare algorithms
fig = mpt.figure()
ax = fig.add_subplot(111)
mpt.boxplot(results)
ax.set_xticklabels(names)
fig.suptitle('Algorithm Comparison')
mpt.show()

# Make predictions on validation dataset
kNN = KNeighborsClassifier()
kNN.fit(X_train, Y_train)
predictions = kNN.predict(X_validation)
print accuracy_score(Y_validation, predictions)
print confusion_matrix(Y_validation, predictions)
print classification_report(Y_validation, predictions)












