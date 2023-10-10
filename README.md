# **SaaS Specification**


+ Build an API to feed a json object to a python script and get a json object back
+ The API must be able to check credentials either with an API key or registered users
+ Build functionality to generate and share API keys, and register users from a landing page (http://paraknowledge.ai)
+ Build capability to monitor usage:
  - how mnay API calls
  - determine the pricing tier based on api-key or user-registration
  - detrmine the number of samples used per call
+ Build capability to charge account based on pricing tier and usage
+ Have option for generating invoices

# We next describe the IO specification




## **Data IO Specification**

The input/output operations will be handled by the python script. An example, called `run_dummy_model.py`,
will be provided for reference.

Example usage with provided data:

```
python3 run_dummy_model.py -p SAMPLE_MODEL.pickle -i sample_data.json -o sample_predictions.json -v True
python3 run_dummy_model.py -p SAMPLE_MODEL.pickle -i sample_data.json -v True
```

If -o if not specified, the script will print the json object into the STDOUT.

The output should be saved to the database.

### **Input/Output Format**

We expect the json input for the patient data in the following .json format:

```json
[
    { 
        'patient_id': 'P00101606306',
        'sex': 'F',
        'location': 'Chicago, IL, 60601',
        'age': 0,
        'birth_date': '01-01-2006',
        'race': 'More than one race',
        'ethnicity': 'Hispanic or Latino',
        'income': '80000',
        'occupation': 'School Teacher',
        'family_relation': 'Mother',
        'DX_record': [
            {'date': '07-31-2006', 'code': 'Z38.00'},
            {'date': '07-31-2006', 'code': 'P59.9'},
            {'date': '08-07-2006', 'code': 'Z00.129'},
            {'date': '08-07-2006', 'code': 'P59.9'},
            {'date': '08-07-2006', 'code': 'P59.9'},
            {'date': '08-29-2016', 'code': 'J01.90'}
        ],
        'RX_record': [
            {'date': '10-29-2011', 'code': 'rxLDA017'},
            {'date': '05-16-2015', 'code': 'rxIDG004'},
            {'date': '08-08-2015', 'code': 'rxIDG004'},
            {'date': '06-04-2016', 'code': 'rxIDD013'},
        ],
        'PROC_record': [
            {'date': '02-05-2007', 'code': '90723'},
            {'date': '11-05-2007', 'code': 'J1100'},
            {'date': '11-05-2007', 'code': '99214'},
        ]
    }
]
```


The output will be of the following .json format:
```json
[
    {'patient_id': 'P00101606306', 'predicted_risk': 0.0042816491258671, 'decision': 0, 'confidence': 0.0},
    {'patient_id': 'P00101606307', 'predicted_risk': 0.02346271, 'decision': 1, 'confidence': 0.8},
    {'patient_id': 'P00101606308', 'predicted_risk': 0.01765892, 'decision': 0, 'confidence': 0.5},
    {'patient_id': 'P00101606309', 'predicted_risk': 0.00239817, 'decision': 1, 'confidence': 0.9}
]
```

# Frontend Design and Optimization

We have a preliminary example here: (http://paraknowledge.ai)
This needs to be augmented or modified to provide the user registration,
and potentially show usage and invoice to users after they register and login


