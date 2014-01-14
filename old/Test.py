'''
Created on Dec 14, 2013

@author: Benjamin
'''

print(__doc__)

from sklearn import svm, datasets
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix

import pylab as pl

# import some data to play with
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Split the data into a training set and a test set
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# Run classifier
classifier = svm.SVC(kernel='linear')
y_pred = classifier.fit(X_train, y_train).predict(X_test)

# Compute confusion matrix
cm = confusion_matrix(y_test, y_pred)

print(cm)

# Show confusion matrix in a separate window
pl.matshow(cm)
pl.title('Confusion matrix')
pl.colorbar()
pl.ylabel('True label')
pl.xlabel('Predicted label')
pl.show()