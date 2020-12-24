#importing libraries
import sys  
sys.path.insert(0, '/Users/emilyburns/Documents/Data_Science/projects/web_scraping_wiki/code/script/functions')
import funs_do_modeling as funs

import os
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, roc_auc_score, accuracy_score
from sklearn.ensemble import VotingClassifier
from mlxtend.classifier import StackingCVClassifier
import graphviz
from sklearn import tree

#setting the seed
random.seed(101)

#import cleaned csv file
df = pd.read_csv('/Users/emilyburns/Documents/Data_Science/projects/web_scraping_wiki/data/processed_data/all_project_data_clean.csv')

#taking a look at the data
df['Suicide_Classification'] = df['Suicide_Classification'].astype('category')
df.head()
df.info()

#scaling features
col_names = ['2016_Suicide_Rate', '2015_Disorder_Prevalence', '2015_Unemployment', 
             '2015_Healthcare_Expenditure', '2015_Gender_Ratio']
features = df[col_names]
scaler = StandardScaler().fit(features.values)
features = scaler.transform(features.values)

df[col_names] = features

#splitting into training and test sets
X = df.iloc[:, 1:5]
y = df['Suicide_Classification']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 101)

#looking at training set dimensions and classification distribution
print("Number of countries in training data: {}".format(len(X_train))) 
print("Number of countries in test data: {}".format(len(X_test))) 

#looking at class balance
df['Suicide_Classification'].value_counts()
y_train.value_counts()
y_train.value_counts().plot(kind='bar', title='Count (target)')

#using smote to account for class imbalance
smt = SMOTE(random_state=0)
X_train_SMOTE, y_train_SMOTE = smt.fit_sample(X_train, y_train)

y_train_SMOTE.value_counts().plot(kind='bar', title='Count (target)')


################################
        # KNN Modeling
################################

knn = KNeighborsClassifier()

knn_grid_params = {'n_neighbors': [3, 5, 7, 9, 11],
              'weights': ['uniform', 'distance']}

knn_gscv = GridSearchCV(knn, 
                        knn_grid_params,
                        verbose = 1,
                        cv=5, 
                        n_jobs = -1)

knn_results = knn_gscv.fit(X_train_SMOTE, y_train_SMOTE)

funs.TrainingResults(knn_results)
funs.TestResults(knn_gscv, X_test, y_test)
funs.ROCPlot(knn_gscv, X_test, y_test)


################################
 # Logistic Regression Modeling
################################

logreg = LogisticRegression(random_state=101)

logreg_grid_params = {'C': [0.001, 0.01, 0.1, 1, 10, 100], 
                      'penalty': ['l1', 'l2']}

logreg_gscv = GridSearchCV(logreg,
                           logreg_grid_params,
                           cv=5,
                           verbose =1,
                           n_jobs = -1)

logreg_results = logreg_gscv.fit(X_train_SMOTE, y_train_SMOTE)

funs.TrainingResults(logreg_results)
funs.TestResults(logreg_gscv, X_test, y_test)
funs.ROCPlot(logreg_gscv, X_test, y_test)


################################
 # Decision Tree Modeling
################################

tree = DecisionTreeClassifier()

tree_grid_params = {'criterion': ['gini', 'entropy'],
                    'max_depth': [2,4,6,8,10]}

tree_gscv = GridSearchCV(tree,
                           tree_grid_params,
                           cv=5,
                           verbose =1,
                           n_jobs = -1)

tree_results = tree_gscv.fit(X_train_SMOTE, y_train_SMOTE)

funs.TrainingResults(tree_gscv)

#visualizing tree results
feature_names = X_train.columns
dot_data = tree.export_graphviz(tree_gscv.best_estimator_, out_file=None, 
            filled=True, rounded=True, feature_names=feature_names, class_names=['0','1','2'])

graph = graphviz.Source(dot_data)  
graph   

funs.TestResults(tree_gscv, X_test, y_test)
funs.ROCPlot(tree_gscv, X_test, y_test)


############################################
         # Voting Ensemble Model
############################################
voting_clf = VotingClassifier(estimators=[('lr', logreg_gscv), 
                                          ('knn', knn_gscv), 
                                          ('tree', tree_gscv)], voting='hard') 

for clf in (logreg_gscv, tree_gscv, knn_gscv, voting_clf):
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(clf.__class__.__name__, accuracy_score(y_test, y_pred))

funs.TestResults(voting_clf, X_test, y_test)
    
############################################
         # Stacking Ensemble Model
############################################

#stacking model without gridsearch
stacking_clf = StackingCVClassifier(classifiers = [DecisionTreeClassifier(), LogisticRegression()],
                            shuffle = False,
                            use_probas = True,
                            cv = 5,
                            meta_classifier = KNeighborsClassifier())

classifiers = {"lr": KNeighborsClassifier(),
               "knn": LogisticRegression(),
               "stack": stacking_clf}

results = pd.DataFrame()

for key in classifiers:
    y_pred = classifiers[key].predict_proba(X_test)[:,1]
    results[f"{key}"] = y_pred
    
results["actual_value"] = y_test
results.head(10)

#adding gridsearch to stacking model
params = {'decisiontreeclassifier__criterion': ['gini', 'entropy'],
          'decisiontreeclassifier__max_depth': [2,4,6,8,10],
          'logisticregression__C': [0.001, 0.01, 0.1, 1, 10, 100],
          'meta_classifier__n_neighbors': [3, 5, 7, 9, 11],
          'meta_classifier__weights': ['uniform', 'distance']
          }

grid = GridSearchCV(estimator=stacking_clf, 
                    param_grid=params, 
                    cv=5,
                    refit=True)

grid.fit(X_train_SMOTE, y_train_SMOTE)

cv_keys = ('mean_test_score', 'std_test_score', 'params')

for r, _ in enumerate(grid.cv_results_['mean_test_score']):
    print("%0.3f +/- %0.2f %r"
          % (grid.cv_results_[cv_keys[0]][r],
             grid.cv_results_[cv_keys[1]][r] / 2.0,
             grid.cv_results_[cv_keys[2]][r]))
    
print('Best parameters: %s' % grid.best_params_)
print('\nAccuracy: %.2f' % grid.best_score_)

funs.TestResults(stacking_clf, X_test, y_test)
funs.ROCPlot(stacking_clf, X_test, y_test)