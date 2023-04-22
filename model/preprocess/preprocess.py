import numpy as np
import pandas as pd
import os
import settings
import argparse
import pickle
from utils import my_transformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer


def parse_args():
    """
    Use argparse to get the input parameters for preprocessing the data.
    """
    parser = argparse.ArgumentParser(description="Preprocess data.")
    parser.add_argument(
        "data_csv",
        type=str,
        help="Full path to the file with the input data . E.g. "
             "data/PAKDD2010_Modeling_Data.txt.",
    )

    args = parser.parse_args()
    return args


def main(data_csv):
    """
    This script will be used for preprocessing our raw data. The only input argument it
    should receive is the path to our data_csv. We will store the resulting train/test
    splits and preprossed in pickles directory using pickle.

    Parameters
    ----------
    data_csv : csv or txt file
        Full path to csv or txt file.
    
    """
    #Pipeline for my transformations
    tranformation_pipeline = Pipeline(steps=[
        ("my_trans", my_transformer())
    ])

    # Pipeline for numeric features
    ##imput all and scale
    numeric_pipeline = Pipeline(steps=[
        ('impute', SimpleImputer(strategy='mean')),
        ("standarization", StandardScaler())
    ])

    # Pipeline for categorical features
    string_pipeline_catnum = Pipeline( steps=[
        ('impute', SimpleImputer(strategy='most_frequent')),
        ('encode', OneHotEncoder(handle_unknown='ignore', sparse=False, drop='if_binary')),
    ])


    string_pipeline_cat = Pipeline( steps=[
        ('impute', SimpleImputer(strategy='most_frequent')),
        ('encode2', OneHotEncoder(handle_unknown='ignore', sparse=False, drop='if_binary')),
    ])

    # Merge both pipelines into one single pre-processing object
    full_processor = ColumnTransformer(transformers=[
        ('number', numeric_pipeline,  settings.numerical_features),
        ('string1', string_pipeline_catnum, settings.categorical_features),
        ('string2', string_pipeline_cat, settings.numeric_categ_features),
    ])

    # The final pipeline with all the transformations
    final_pipeline = make_pipeline(tranformation_pipeline, full_processor)

    data = pd.read_csv(data_csv, encoding = 'ISO-8859-1', delimiter='\t', low_memory=False, names = settings.list_columns)
    data["ALL_INCOMES"] = data["PERSONAL_MONTHLY_INCOME"]+data["OTHER_INCOMES"]
    target = data["TARGET_LABEL_BAD=1"]
    features = data.drop("TARGET_LABEL_BAD=1", axis = 1)
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=100, stratify=target)
    final_pipeline_fit = final_pipeline.fit(X_train.copy())

    # Save final preprocessing pipeline in a pickle, after fitting it
    with open(os.path.join("/src/pickles", "final_pipeline_fit.pickle"), "wb") as f:
        pickle.dump(final_pipeline , f, protocol=pickle.HIGHEST_PROTOCOL)
    
    X_train_prep = final_pipeline_fit.transform(X_train)
    X_train_prepr = pd.DataFrame(X_train_prep)
        
    with open(os.path.join("/src/pickles", "X_train_prep.pickle"), "wb") as f:
        pickle.dump(X_train_prepr, f, protocol=pickle.HIGHEST_PROTOCOL)
    with open(os.path.join("/src/pickles", "y_train.pickle"), "wb") as f:
        pickle.dump(y_train, f, protocol=pickle.HIGHEST_PROTOCOL)
    with open(os.path.join("/src/pickles", "y_test.pickle"), "wb") as f:
        pickle.dump(y_test, f, protocol=pickle.HIGHEST_PROTOCOL)

    print("----------------------------")
    print("Preprocessing done")

if __name__ == "__main__":
    args = parse_args()
    main(args.data_csv)




