import requests
import json
# import related models here
from .models import CarDealer, DealerReview, CarModel
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:

        if 'api_key' in kwargs:
            params = kwargs['params']
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', kwargs['api_key']))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)

    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
# def post_request(url, json_payload, **kwargs):

#     requests.post(url, params=kwargs, json=json_payload)
#     print(kwargs)
#     print("POST from {} ".format(url))
#     try:

#         if 'api_key' in kwargs:
#             params = kwargs['params']
#             response = requests.post(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', kwargs['api_key']))
#         else:
#             # Call get method of requests library with URL and parameters
#             response = requests.get(url, headers={'Content-Type': 'application/json'},
#                                         params=kwargs)

#     except:
#         # If any error occurs
#         print("Network exception occurred")
#     status_code = response.status_code
#     print("With status {} ".format(status_code))
#     json_data = json.loads(response.text)
#     return json_data

def post_request(url, json_payload, **kwargs):
    try:
        # Call post method of requests library with URL, json_payload and parameters
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occured")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        #dealers = json_result["rows"]
        # For each dealer object
        #for dealer in dealers:
        for dealer in json_result:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# def get_dealer_by_id_from_cf(url, **kwargs):
#     dealer_id = kwargs['dealer_id']
#     results = []
#     # Call get_request with a URL parameter
#     json_result = get_request(url, id=dealer_id)
#     if json_result:
#         # Get the row list in JSON as dealers
#         #dealers = json_result["rows"]
#         # For each dealer object
#         #for dealer in dealers:
#         for dealer in json_result:
#             # Get its content in `doc` object
#             #dealer_doc = dealer["doc"]
#             dealer_doc = dealer
#             # Create a CarDealer object with values in `doc` object
#             dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
#                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
#                                    short_name=dealer_doc["short_name"],
#                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
#             results.append(dealer_obj)

#     return results

def get_dealer_by_id_from_cf(url, dealer_id):
    dealer = get_request(url, id=dealer_id)
    print("Dealer", dealer)
    if dealer:
        # Create a CarDealer object with values in `dealer` object
        return CarDealer(address=dealer[0]["address"], city=dealer[0]["city"], full_name=dealer[0]["full_name"],
                                    id=dealer[0]["id"], lat=dealer[0]["lat"], long=dealer[0]["long"],
                                    short_name=dealer[0]["short_name"],
                                    st=dealer[0]["st"], zip=dealer[0]["zip"])

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        #dealers = json_result["rows"]
        # For each dealer object
        #for dealer in dealers:
        #print(json_result)
        for review in json_result:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            #dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review['dealership'], name=review['name'], purchase=review['purchase'], 
                        review=review['review'], purchase_date=review['purchase_date'], car_make=review['car_make'],
                        car_model=review['car_model'], car_year=review['car_year'], sentiment=analyze_review_sentiments(review['review']), id=review['id'])
            results.append(review_obj)

    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
#def analyze_review_sentiments(text):
#    params = dict()
#    params["text"] = text
#    params["version"] = "2020-08-01"
#    params["features"] = "sentiment"
#    params["return_analyzed_text"] = True
#    url = 'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/43ef852b-bbd0-4c3f-8ff1-0fc689eaa388'
#    api_key = 'xzzU_UPew5D4SHlvh7NgeBDCChWPR2aiLGp8-7S10fRg'
#
#    result_json = get_request(url, api_key=api_key, params=params)
#    
#    return result_json

def analyze_review_sentiments(text): 
    url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/43ef852b-bbd0-4c3f-8ff1-0fc689eaa388" 
    api_key = "xzzU_UPew5D4SHlvh7NgeBDCChWPR2aiLGp8-7S10fRg" 
    authenticator = IAMAuthenticator(api_key) 
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 
    natural_language_understanding.set_service_url(url) 
    response = natural_language_understanding.analyze( text=text,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result() 
    label=json.dumps(response, indent=2) 
    label = response['sentiment']['document']['label'] 
    return(label) 


