import os
import settings
from flask import Blueprint, render_template, request, jsonify
from middleware import model_predict
import csv

router = Blueprint("app_router", __name__, template_folder="templates")


@router.route("/", methods=["GET", "POST"])
def index():
    """
    GET: Index endpoint, renders our HTML code.

    POST: Sends a request with data attached in the body of the request; 
    this is the way most web forms are submitted.

    It calls our ML model to get and display the predictions.
    """
    # Opens the web page
    if request.method == "GET":
        return render_template("form.html")

    if request.method == "POST":
        form_dict = request.form.to_dict()

        print(form_dict)

        path = os.path.join(settings.UPLOAD_FOLDER, "forms.csv") 
        if os.path.exists(path): 
            with open(path,"a") as f:
                w = csv.DictWriter(f, form_dict.keys())
                w.writerow(form_dict)
        else:
            with open(path,"a") as f:
                w = csv.DictWriter(f, form_dict.keys())
                w.writeheader()
                w.writerow(form_dict)

        # Calls this function to predict from middleware
        prediction, probability = model_predict(form_dict)
                
        context = {
            "prediction": prediction,
            "probability": probability
                  }

        # Define the treshold as 0.27
        if float(context["probability"]) >= 0.27:
            context["prediction"] = 1
        else:
            context["prediction"] = 0

        return render_template("results.html", context=context)
        

@router.route("/predict", methods=["POST"])
def predict():
    rpse = {"prediction": None, "probability": None}

    # If user sends an invalid request return `rpse` dict with 
    # default values HTTP 400 Bad Request code
    if request.method != "POST":
        return jsonify(rpse), 400
    
    form_dict = request.form.to_dict()
    prediction, probability = model_predict(form_dict)
   
    rpse = {"prediction": prediction, 
            "probability": probability
            }
    return jsonify(rpse)