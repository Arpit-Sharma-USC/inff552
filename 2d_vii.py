import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
import pandas as pd
import numpy as np
from sklearn.feature_selection import RFE
from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest
from sklearn.cross_validation import train_test_split

from sklearn.feature_selection import chi2
from imblearn.under_sampling import RandomUnderSampler

import seaborn as sns
from sklearn.metrics import confusion_matrix

from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from scipy import stats
import metrics
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold # import KFold
from sklearn.cross_validation import cross_val_score, cross_val_predict
from sklearn.utils import shuffle
import statsmodels.formula.api as smf
from sklearn.feature_selection import f_classif
from sklearn import model_selection
import statsmodels.api as sm

counter=0
chunks=1
i=1
value=69/chunks
print(value)
for l in range(1,2):
    counter = 0
    mean_chunk_arr = []
    my_score_arr = []
    # print('#####################################################IN L=', l,'######################################')

    for inner in range(1,l+1):

        # print('In chunk:',inner)



        dataframe=pd.read_csv('C:/Users/Shanu/PycharmProjects/Arem/AReM/my_dataset_v_test.csv')
        df=pd.read_csv('C:/Users/Shanu/PycharmProjects/Arem/AReM/my_dataset_v_train.csv')

        dataset=dataframe.values
        dfset=df.values

        x_shuf=dataset[:,0:6]
        y_shuf=dataset[:,6:]
        value = int(len(dataframe) / l)

        counter+=1
        start=int((value*counter)-value)
        end=int((value*counter))

        x_shuf_train = dfset[:, 0:6]
        y_shuf_train = dfset[:, 6:]
        value_train = int(len(df) / l)

        start_train = int((value_train * counter) - value_train)
        end_train = int((value_train * counter))

        # x_train_prime, y_train_prime = shuffle(x_shuf,y_shuf ,random_state=0)
        x_train_prime, y_train_prime = x_shuf_train, y_shuf_train
        x_test_prime,y_test_prime=x_shuf,y_shuf

        # print('starting:',start)
        # print('ending',end)
        x_train=x_train_prime[start_train:end_train,0:6]
        y_train=y_train_prime[start_train:end_train,0:6]


        X_test=x_test_prime[start:end,0:6]
        y_test=y_test_prime[start:end,0:6]



        rus = RandomUnderSampler(return_indices=True)
        X_resampled, y_resampled, idx_resampled = rus.fit_sample(X_test, y_test)

        X_resampled = pd.DataFrame(X_resampled)
        y_resampled = pd.DataFrame(y_resampled)
        y_resampled.columns = ['Class']
        undersampled_data = pd.concat([X_resampled, y_resampled], axis=1)

        X = undersampled_data.values
        y = undersampled_data.Class.values
        X=X[:,:6]
        print(X.shape)
        print(X_test.shape)
        # X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

        # kfold = model_selection.KFold(n_splits=5, random_state=7,shuffle=True)
        modelCV = LogisticRegression()
        scoring = 'accuracy'
        # X_new = SelectKBest(chi2, k=6).fit_transform(x_train, y_train)
        results = modelCV.fit(x_train,y_train)
        preds=modelCV.predict(X)
        score=modelCV.score(X,y)
        error=mean_squared_error(y,preds)

        # print('Score:',score)
        # print('Error:',error)

        # outcome_acc=results.()
        # print("5-fold cross validation average accuracy: %.3f" % (outcome_acc))
        # my_score_arr.append(score)
        my_score_arr.append(error)

        conf_matrix = confusion_matrix(y, preds)
        print(type(conf_matrix))
        plt.figure()
        sns.set()
        ax = sns.heatmap(conf_matrix, annot=True, cmap="YlGnBu",
                         cbar_kws={'label': 'No. of Classified/Missclassified Datapoints'})
        heading_conf = 'Confusion matrix for L=' + str(l) + ' Chunk: ' + str(inner)
        ax.set_title(heading_conf)
        fig = 'C:/Users/Shanu/PycharmProjects/Arem/AReM/' +'Case Control sampling'+ str(l) + 'chunk'+ str(inner)
        plt.savefig(fig)
        plt.show()

        logit_roc_auc = roc_auc_score(y, preds)
        fpr, tpr, thresholds = roc_curve(y, preds)
        plt.figure()
        plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
        plt.plot([0, 1], [0, 1], 'r--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        title_str = 'Receiver operating characteristic with case control sampling for L=' + str(l) + ' in chunk :' + str(inner)
        plt.title(title_str)
        plt.legend(loc="lower right")
        str_save_title = 'C:/Users/Shanu/PycharmProjects/Arem/AReM/' +'Case Control sampling'+ ' ROC' + str(l)
        plt.savefig(str_save_title)
        plt.show()

    mean_chunk = np.mean(my_score_arr)
    mean_chunk_arr.append(mean_chunk)
    print('Net Error for L=',l,'is',mean_chunk_arr)




















