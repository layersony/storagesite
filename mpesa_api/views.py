from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from decouple import config
from django.contrib import messages

#mpesa_cred
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPassword
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaPayment, Payment

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
        "CallBackURL": "https://storagesite.herokuapp.com/api/v1/c2b/callback",
        "AccountReference": "Storagesite",
        "TransactionDesc": "Testing stk push StorageSite"
    }
    response = requests.post(api_url, json=request, headers=headers)
    print('lipa na mpesa online')
    print(response)
    return HttpResponse('success')

@csrf_exempt
def register_urls(request):
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
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    print(body)
    print('from call back')

    if body['Body']['stkCallback']['ResultCode'] == 0:
        payment = Payment(
            checkoutRequestID = body['Body']['stkCallback']['CheckoutRequestID'],
            merchantRequestID = body['Body']['stkCallback']['MerchantRequestID'],
            amount = body['Body']['stkCallback']['CallbackMetadata']['Item'][0]["Value"],
            mpesaReceiptNumber = body['Body']['stkCallback']['CallbackMetadata']['Item'][1]["Value"],
            transactionDate = body['Body']['stkCallback']['CallbackMetadata']['Item'][-2]["Value"],
            phoneNumber = body['Body']['stkCallback']['CallbackMetadata']['Item'][-1]["Value"],
        )
        payment.save()
        print('saved response')
        messages.success('Payment Successfully')    
    else:
        payment = Payment(
            checkoutRequestID = body['Body']['stkCallback']['CheckoutRequestID'],
            merchantRequestID = body['Body']['stkCallback']['MerchantRequestID'],
            amount = 'Cancelled',
            mpesaReceiptNumber = 'Cancelled',
            transaction_date = 'Cancelled',
            phoneNumber = 'Cancelled',
        )
        payment.save()
        messages.error('Transcation Declined By User')

    resp = {
        "ResultCode": 0,
        "ResultDesc": "Success"
    }

    return JsonResponse(dict(resp))

@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    with open('paymnt.txt', 'a+') as f:
        f.write(request.body.decode('utf-8'))
        f.close

    return JsonResponse(dict(context))

@csrf_exempt
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    
    print('from confirmation')
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    if mpesa_payment['Body']['stkCallback']['ResultCode'] == 0:
        payment = Payment(
            checkoutRequestID = mpesa_payment['Body']['stkCallback']['CheckoutRequestID'],
            merchantRequestID = mpesa_payment['Body']['stkCallback']['MerchantRequestID'],
            amount = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][0]["Value"],
            mpesaReceiptNumber = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][1]["Value"],
            transaction_date = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][3]["Value"],
            phoneNumber = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][4]["Value"],
        )
        payment.save()
        print('saved response')
        messages.success('Payment Successfully')
        
    else:
        payment = Payment(
            checkoutRequestID = mpesa_payment['Body']['stkCallback']['CheckoutRequestID'],
            merchantRequestID = mpesa_payment['Body']['stkCallback']['MerchantRequestID'],
            amount = 'Cancelled',
            mpesaReceiptNumber = 'Cancelled',
            transaction_date = 'Cancelled',
            phoneNumber = 'Cancelled',
        )
        payment.save()
        messages.error('Transcation Declined By User')
    return JsonResponse(dict(context))