import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, roc_auc_score
from sklearn.linear_model import LogisticRegression

def TrainingResults(model):
    print("Best estimator:\n{}".format(model.best_estimator_))
    print("\nBest cross-validation score: {:.2f}".format(model.best_score_))
    print("\nBest parameters:\n{}".format(model.best_params_))
    
    model_df = pd.DataFrame(model.cv_results_)
    display(model_df.head())

def TestResults(model, x, y):
    prediction = model.predict(x)
    print("Test set predictions: \n{}".format(model.predict(x)))
    print("\n\nTest set accuracy: {:.2f}".format(model.score(x, y)))
    print("\n\nConfusion matrix: \n{}".format(confusion_matrix(y, prediction)))
    print("\n\nClassification report: \n{}".format(classification_report(y, prediction)))
    
def ROCPlot(model, X_test, y_test):
    y_test_plot = y_test
    y_test_plot = y_test_plot.cat.rename_categories({'Below':0, 'Above':1})
    y_test_plot = y_test_plot.astype('int')
    
    chance_probs = [0 for _ in range(len(y_test_plot))]
    lr_probs = model.predict_proba(X_test)
    lr_probs = lr_probs[:, 0]
    ns_auc = roc_auc_score(y_test_plot, chance_probs)
    lr_auc = roc_auc_score(y_test_plot, lr_probs)
    
    print('Chance: ROC AUC=%.3f' % (ns_auc))
    print('Model: ROC AUC=%.3f' % (lr_auc))

    ns_fpr, ns_tpr, _ = roc_curve(y_test_plot, chance_probs)
    lr_fpr, lr_tpr, _ = roc_curve(y_test_plot, lr_probs)
    plt.plot(ns_fpr, ns_tpr, linestyle='--', label='Chance')
    plt.plot(lr_fpr, lr_tpr, marker='.', label='Model')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend()
    plt.show()
    