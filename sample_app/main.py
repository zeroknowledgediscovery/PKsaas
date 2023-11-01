from zcor_utils.common import current_time
from zcor.classifier import predict_json
from flask import Flask, request, jsonify
from functools import wraps
import random
import string
import uuid


app = Flask(__name__)

# In-memory data storage for simplicity; use a database in production
api_keys = {} # Stores api_key: user_id mappings
usage_records = {} # Stores user_id: number_of_uses mappings
user_billing = {} # Stores user_id: amount_due mappings
RATE_PER_USAGE = 33.34 # Example rate per usage


def generate_api_key():
    return str(uuid.uuid4())


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('zcor-api-key')
        if api_key not in api_keys:
            return jsonify({"error": "API key is invalid or missing"}), 403
        return f(*args, **kwargs)
    return decorated_function


@app.route('/generate_api_key', methods=['GET'])
def new_api_key():
    new_key = generate_api_key()
    user_id = str(uuid.uuid4())
    api_keys[new_key] = user_id
    usage_records[user_id] = 0
    user_billing[user_id] = 0.0
    return jsonify({"api_key": new_key})


@app.route('/process', methods=['POST'])
@require_api_key
def process_json():
    #input_json_object = request.json
    input_json_object = request.get_json(silent=True)
    if not isinstance(input_json_object, list):
        return jsonify({"error": "JSON input should be a list of dictionaries."}), 400

    api_key = request.headers.get('zcor-api-key')
    user_id = api_keys[api_key] # TODO :: RAISE ERROR IF API KEY NOT RECOGNIZED

    # Check for 'fpr_setting' as a float    
    fpr_setting = request.args.get('fpr_setting', default=0.05, type=float)

    # Billing calculations
    number_of_patients = len(input_json_object)
    usage_records[user_id] += number_of_patients
    user_billing[user_id] += number_of_patients * RATE_PER_USAGE

    # Process and return some random values in a JSON object
    processed_data = [{"result": random.random()} for _ in data]
    
    interpreted_predictions = predict_json(
        "ASD_pure.pkl.gz",
        input_json_object,
        FPR_SETTING = fpr_setting
    )    
    return jsonify(interpreted_predictions)


@app.route('/usage', methods=['GET'])
@require_api_key
def get_usage():
    api_key = request.headers.get('zcor-api-key')
    user_id = api_keys[api_key]
    return jsonify({
        "number_of_patients_processed": usage_records[user_id],
        "amount_due": user_billing[user_id]
    })


if __name__ == '__main__':
    app.run(debug=True)

