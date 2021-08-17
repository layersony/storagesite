from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class MpesaCalls(BaseModel):
    '''
      store for mpesa calls for later analysis for confirmation purposes
    '''
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()
    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'

class MpesaCallBacks(BaseModel):
    '''
    store accepted Mpesa transactions without accessing each field in the body.
    '''
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()
    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'

class MpesaPayment(BaseModel):
    '''
    store successful transactions.
    '''
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'
        
    def __str__(self):
        return self.first_name

class Payment(BaseModel):
    '''
        store mpesa calls from callback
    '''
    checkoutRequestID = models.CharField(max_length=100, blank=True, null=True)
    merchantRequestID = models.CharField(max_length=50, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    mpesaReceiptNumber = models.CharField(max_length=20, blank=True, null=True)
    # transactionDate = models.CharField(max_length=100, blank=True, null=True)
    phoneNumber = models.CharField(max_length=13, blank=True, null=True)

    class Meta:
        verbose_name = 'CallBack Payment'
        verbose_name_plural = 'CallBack Payments'
