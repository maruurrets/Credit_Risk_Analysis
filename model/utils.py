import settings
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class my_transformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.upper_lim = []
        self.lower_lim = []
        self.columns = ["MONTHS_IN_RESIDENCE", "ALL_INCOMES", "PERSONAL_ASSETS_VALUE"]

    def fit(self,X ,y= None):
        X.drop(columns = settings.columns_drop, inplace=True)
        for column in self.columns:
            q1=np.quantile(X[column], 0.25)
            q3=np.quantile(X[column], 0.75)
            iqr=q3-q1
            self.upper_lim.append(q3+1.5*iqr)
            self.lower_lim.append(q1-1.5*iqr)
        return self

    def transform(self,X, y=None):
        
        for i, column in enumerate(self.columns):            
           X[column]=np.where(X[column]>self.upper_lim[i], self.upper_lim[i], np.where(X[column]<self.lower_lim[i], self.lower_lim[i],X[column]))

        for col in X.columns:
            for value in X[col]:
                if col=="MARITAL_STATUS" and value==0:
                    X.loc[X["MARITAL_STATUS"]==0, "MARITAL_STATUS"]= np.nan
                else:
                    continue
                if col=="QUANT_DEPENDANTS" and value>=7:
                    X.loc[X["QUANT_DEPENDANTS"]>=7, "QUANT_DEPENDANTS"]= 7
                else:
                    continue
                if col=="STATE_OF_BIRTH" and value == "XX" or value == " ":
                    X.loc[X["STATE_OF_BIRTH"] == "XX" , "STATE_OF_BIRTH"]= np.nan
                    X.loc[X["STATE_OF_BIRTH"] == " " , "STATE_OF_BIRTH"]= np.nan
                else:
                    continue
                if col=="NACIONALITY" and value == 2:
                    X.loc[X["NATIONALITY"] == 2 , "NATIONALITY"]= 0
                else:
                    continue
                if col=="AGE" and value < 17:
                    X.loc[X["AGE"] < 17, "AGE"]=17
                else:
                    continue
                if col=="RESIDENCIAL_ZIP_3" and value == "#DIV/0!":
                    X.loc[X["RESIDENCIAL_ZIP_3"] == "#DIV/0!", "RESIDENCIAL_ZIP_3"]= np.nan
                else:
                    continue
             
        return X