import json
import time
from uuid import uuid4
import redis
import settings

# Connect to Redis
db = redis.Redis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID
    )


def model_predict(form_dict):
    """
    Receives the form_dict, and queues the job into Redis.
    Will loop until getting the answer from our ML service.

    Parameters
    ----------
    form_dict : dict
        All data uploaded by the user in the form, as a dictionary.

    Returns
    -------
    prediction, probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        probability as a number.
    """
    prediction = None
    probability = None

    # Assign an unique ID for this job and add it to the queue.
    job_id = str(uuid4())

    # Create a dict with the job data and the id to send through Redis.
    # Form_dict is a dict (comes from completing the form)
    job_data = {"id": job_id, "form": form_dict} 

    # Json to string
    job_data_str = json.dumps(job_data)

    # Send the job to the model service using Redis
    db.lpush(settings.REDIS_QUEUE, job_data_str)

    # Loop until we received the response from our ML model
    while True:
        
        #Recieve prediction from hash table saved in ml_service
        pred_dict = db.get(job_id)  
        if pred_dict is None:
            time.sleep(settings.API_SLEEP)
            continue
        else:
            pred_dict = json.loads(pred_dict)  
            prediction = pred_dict["prediction"]
            probability = pred_dict["probability"]
            db.delete(job_id)
            break

    return prediction, probability
