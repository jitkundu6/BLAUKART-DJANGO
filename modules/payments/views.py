import os
import razorpay

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib import messages
from .models import Payment


# TEST KEY
#RAZORPAY_KEY = "rzp_test_pOdnmaU6ec5IWt"
#RAZORPAY_KEY_SECRET = "olR9dGd8I7l3XXZ4KERkDRq7" 

# Live Key
#RAZORPAY_KEY = "rzp_live_4DXpUVE0cjejpJ"
#RAZORPAY_KEY_SECRET = "oviSY94By1rYCsxFbhPX9Hzkd"



# LIVE KEY (working)
#RAZORPAY_KEY = "rzp_live_U1WZUzR2bDRJxl"
#RAZORPAY_KEY_SECRET = "6N2FrVW70ov6nEyQH7QJzVXf"

# TEST KEY (working)
RAZORPAY_KEY = "rzp_test_k9FYjaYUbjtrvz"
RAZORPAY_KEY_SECRET = "JMvGj6aiAsmMa80Ct14ngstJ"



# Payment Initiation:
def payment_initiate(request, id):

    #################### Checking User Log In: ##########################
    FAILED = False
    user = request.user
    try:
        if user.email is None:
            FAILED = True

    except Exception as err:
        print(f"ErrorType- {type(err)}")
        print(f"Error- {err}")

        FAILED = True
    

    if FAILED:
        messages.warning(request, f"Please Log In before making payment")
        print(f"Please Log In before making payment")

        # Returns None if user came from another website
        url = request.META.get('HTTP_REFERER')
        print(f"Redirecting to - {url}")

        if url is not None:
            return redirect(url)
        return redirect('shop:basic:home')

    else:
        print(f"Get user :{user}")




    #################### Getting Payment details by 'id' ##########################
    FAILED = False
    payment = None
    try:
        payment = Payment.objects.get(id=id)
        if payment is None:
            FAILED = True

    except Exception as err:
        print(f"ErrorType- {type(err)}")
        print(f"Error- {err}")

        FAILED = True
        

    if FAILED:
        messages.warning(request, f"Payment not initiated!")
        print( f'Payment not initiated!')

        # Returns None if user came from another website
        url = request.META.get('HTTP_REFERER')
        print(f"Redirecting to - {url}")

        if url is not None:
            return redirect(url)
        return redirect('shop:basic:home')

    else:
        print(f"Get Payment details by id: {id}")




    #################### Checking whether User is same as Payment User or not ##########################
    FAILED = False
    try:
        if user != payment.user:
            FAILED = True

    except Exception as err:
        print(f"ErrorType- {type(err)}")
        print(f"Error- {err}")

        FAILED = True
    

    if FAILED:
        messages.warning(request, f"Sorry! Present payment is not initiated by you")
        print(f"Sorry! Present payment is not initiated by you")

        # Returns None if user came from another website
        url = request.META.get('HTTP_REFERER')
        print(f"Redirecting to - {url}")

        if url is not None:
            return redirect(url)
        return redirect('shop:basic:home')

    else:
        print(f"Get user :{user}")




    #################### Getting Payment 'status' ##########################
    FAILED = False
    status = None
    try:
        status = payment.status
        if(status == 'done'):
            FAILED = True

    except Exception as err:
        print(f"ErrorType- {type(err)}")
        print(f"Error- {err}")

        FAILED = True


    if FAILED:
        messages.warning(request, f"This Payment is Previously done! - Try Again")
        print( f"This Payment is Previously done! - Try Again")

        # Returns None if user came from another website
        url = request.META.get('HTTP_REFERER')
        print(f"Redirecting to - {url}")
        
        if url is not None:
            return redirect(url)
        return redirect('shop:basic:home')

    else:
        print(f"Get Payment status: {status}")




    #################### Getting Payment 'amount' ##########################
    amount = payment.amount

    if(amount<1):
        amount = 1   #100 here means 1 dollar, 1 rupree if currency INR

    amount *= 100

    # client = razorpay.Client(auth=(os.getenv('razorpaykey'), os.getenv('razorpaysecret')))
    client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_KEY_SECRET) )
    response = client.order.create({'amount': amount,'currency':'INR','payment_capture':1})
    # respose {'id': 'order_H1GPQiRHlPiDQu', 'entity': 'order', 'amount': 100, 'amount_paid': 0, 'amount_due': 100,
    # 'currency': 'USD', 'receipt': None, 'offer_id': None, 'status': 'created', 'attempts':0, 'notes': [], 'created_at': 1618941001}
    print(response)

    payment.o_id = response['id']

    payment.amount_paid = response['amount_paid']
    payment.amount_due = response['amount_due']

    payment.offer_id = response['offer_id']
    payment.status = response['status']
    payment.attempts = response['attempts']
    payment.notes = response['notes']
    payment.created_at =  response['created_at']

    payment.save()

    request.session['payment'] = payment.id

    url = request.META.get('HTTP_REFERER')
    print(f"last_url - {url}")
    if url is None:
        request.session['url'] = '#'
    else:
        request.session['url'] = url

   
    param = {'response': response, 'api_key' : RAZORPAY_KEY, 'pay_amount':amount/100}
    return render(request,"payments/payment.html", param)






# Payment Success View:
@csrf_exempt
def payment_success(request):
    print("---success---")

    #################### Checking User Log In: ##########################
    FAILED = False
    user = request.user
    try:
        if user.email is None:
            FAILED = True

    except Exception as err:
        print(f"ErrorType- {type(err)}")
        print(f"Error- {err}")

        FAILED = True
    

    if FAILED:
        messages.warning(request, f"Please Log In before making payment")
        print(f"Please Log In before making payment")

        # Returns None if user came from another website
        url = request.META.get('HTTP_REFERER')
        print(f"Redirecting to - {url}")

        if url is not None:
            return redirect(url)
        return redirect('shop:basic:home')

    else:
        print(f"Get user :{user}")




    #################### Getting Payment details by 'id' ##########################
    FAILED = False
    payment = None
    try:
        id = request.session['payment']
        payment = Payment.objects.get(id=id)
        if payment is None:
            FAILED = True

    except Exception as err:
        print(f"ErrorType- {type(err)}")
        print(f"Error- {err}")

        FAILED = True
        

    if FAILED:
        messages.warning(request, f"Payment not initiated!")
        print( f'Payment not initiated!')

        # Returns None if user came from another website
        url = request.META.get('HTTP_REFERER')
        print(f"Redirecting to - {url}")
        
        if url is not None:
            return redirect(url)
        return redirect('shop:basic:home')

    else:
        print(f"Get Payment details by id: {id}")




    #################### Checking whether User is same as Payment User or not ##########################
    FAILED = False
    try:
        if user != payment.user:
            FAILED = True

    except Exception as err:
        print(f"ErrorType- {type(err)}")
        print(f"Error- {err}")

        FAILED = True
    

    if FAILED:
        messages.warning(request, f"Sorry! Present payment is not initiated by you")
        print(f"Sorry! Present payment is not initiated by you")

        # Returns None if user came from another website
        url = request.META.get('HTTP_REFERER')
        print(f"Redirecting to - {url}")

        if url is not None:
            return redirect(url)
        return redirect('shop:basic:home')

    else:
        print(f"Get user :{user}")


    if request.method =="POST":
        print('-----')
        print(request.POST)
        print(payment)

        payment.status = "done"
        payment.save()
        print("payment satus saved")

        url = request.session['url']
        request.session['url'] = ""
        print(f"Back url - {url}")

        #return HttpResponse("Done payment hurrey!")
        return render(request, 'payments/success.html', {'last_url':url})


    ##### if request.method == "GET":
    url = request.META.get('HTTP_REFERER')
    print(f"last_url - {url}")
    if url is None:
        return redirect('shop:basic:home')
    else:
        return redirect(url)




