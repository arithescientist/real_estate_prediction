import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set_style('darkgrid')

from statsmodels.formula.api import ols
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
import scipy.stats as scs
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PowerTransformer

from sklearn.utils import shuffle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import RFE

from sklearn.metrics import r2_score


def make_ols_sklearn(X, y, test_size=0.20, fit_intercept=False, standardize=False):
    """
    
    Makes an OLS in sklearn
    
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    if standardize:
        ss = StandardScaler()
        ss.fit(X_train)
        X_train = ss.transform(X_train)
        X_test = ss.transform(X_test)
    ols = LinearRegression(fit_intercept=fit_intercept, normalize=False)
    ols.fit(X_train, y_train)
    train_score = ols.score(X_train, y_train)
    test_score = ols.score(X_test, y_test)
   
    cvmae_5 = np.mean(cross_val_score(ols,X , y, cv=5, scoring='neg_mean_absolute_error'))
    cvmae_10 = np.mean(cross_val_score(ols,X, y, cv=10, scoring='neg_mean_absolute_error'))
    print(f"train R2 score = {train_score}")
    print(f"test R2 score = {test_score}\n")
   
    print(f"cv5 MSE score = {cvmae_5}")
    print(f"cv10  MSE score = {cvmae_10}")

    return ols

def build_ols(x_cols,target,df):
    """
    Build OLS in statsmodel
    """
    
    X = df[x_cols]
    y = df[target]
    model = sm.OLS(y,X).fit()
    print(model.summary())
    return model

def remove_outliers(df, col, threshold = 3):
    """
    Removes outliers at chosen threshold level
    """
    zscores = scs.zscore(df[col])
    indices = np.abs(np.where(zscores > threshold))
    return indices[0]

def check_p_values(model):
    
    """
    Removes p-values less than 0.05
    """
    summary = model.summary()
    p_table = summary.tables[1]
    p_table = pd.DataFrame(p_table.data)
    p_table.columns = p_table.iloc[0]
    p_table = p_table.drop(0)
    p_table = p_table.set_index(p_table.columns[0])
    p_table['P>|t|'] = p_table['P>|t|'].astype(float)
    x_cols = list(p_table[p_table['P>|t|'] < 0.05].index)
    print(len(p_table), len(x_cols))
    print(x_cols[:5])
    p_table.head()
    return x_cols

def plot_residuals(resids):
    plt.hist(resids)
    plt.title("Residuals")
    plt.show()
    
    xspace = np.linspace(0, 1, len(resids))
    plt.scatter(xspace, resids)
    plt.title("resids")
    plt.hlines(0, xmin=0, xmax=1)
    plt.show()

def VIFScore(x_cols):
    """
    Checks for multicollinearity in columns using VIF
    """
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    X = df[x_cols]
    vif = [variance_inflation_factor(X.values,i) for i in range(X.shape[1])]
    return list(zip(x_cols,vif))
