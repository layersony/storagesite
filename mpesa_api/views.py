from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from decouple import config

#mpesa_cred
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPassword
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaPayment

def getAccessToken(request):
    consumer_key = config('CONSUMER_KEY')
    consumer_secret = config('CONSUMER_SECRET')
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)


def lipa_na_mpesa_online(request, namber):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
        "Password": LipanaMpesaPassword.decode_password,
        "Timestamp": LipanaMpesaPassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": int(namber),  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPassword.Business_short_code,
        "PhoneNumber": int(namber),  # replace with your phone number to get stk push
        "CallBackURL": "https://storagesite.herokuapp.com/",
        "AccountReference": "Storagesite",
        "TransactionDesc": "Testing stk push StorageSite"
    }
    response = requests.post(api_url, json=request, headers=headers)
    print(response)
    return HttpResponse('success')

@csrf_exempt
def register_urls(request):
    print(request)
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPassword.Test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://storagesite.herokuapp.com/api/v1/c2b/confirmation",
               "ValidationURL": "https://storagesite.herokuapp.com/api/v1/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)

@csrf_exempt
def call_back(request):
    #you can capture the mpesa calls.
    # pass
    print(request)

@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    print(request)
    with open('paymnt.txt', 'a+') as f:
        f.write(request.body.decode('utf-8'))
        f.close

    return JsonResponse(dict(context))

@csrf_exempt
def confirmation(request):
    print(request)
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)

    with open('confirm.txt', 'a+') as f:
        f.write(request.body.decode('utf-8'))
        f.close
    
    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],
    )
    payment.save()
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))