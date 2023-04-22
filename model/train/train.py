import os
import argparse
import pickle
from xgboost import XGBClassifier


def parse_args():
    """
    Use argparse to get the input parameters for preprocessing the data`.
    """
    parser = argparse.ArgumentParser(description="Train your model.")
    parser.add_argument(
        "preprocessed_train",
        type=str,
        help="Full path to the X_train_prep pickle file",
    )

    parser.add_argument(
        "y_train_path",
        type=str,
        help="Full path to the y_train pickle file",
    )

    args = parser.parse_args()

    return args

def main(preprocessed_train, y_train_path):
    '''
    This function train a machine learning model using XGBoost algorithm. Receives as arguments
     the path to our preprocessed train pickle file and the path to y_train pickle file.

    Parameters
    ----------
    preprocessed_train : pickle file
        Full path to X_train_prep pickle file.
    y_train_path : pickle file
        Full path to X_train pickle file.
    ----------
    Returns:
    pred_class: Binary class prediction of the target variable.
       
    '''

    with open(preprocessed_train, "rb") as f:
        X_train_prep = pickle.load(f)

    with open(y_train_path, "rb") as f:
        y_train = pickle.load(f)

    xgb_model = XGBClassifier()
    xgb_model_fit = xgb_model.fit(X_train_prep, y_train)

    # Save fitted XGBClassifier model
    with open(os.path.join("/src/pickles", "xgb_model_fit.pickle"), "wb") as f:
         pickle.dump(xgb_model_fit, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    print("----------------------------")
    print("Train done")


if __name__ == "__main__":
    args = parse_args()
    main(args.preprocessed_train, args.y_train_path)