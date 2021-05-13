import math, random
from twilio.rest import Client

TRIAL_VERSION = True
MY_PH_NUM = "+918617227062"  # default To Phone Number

FROM_PH_NUM = "+15108496863"

ACCCOUNT_SID = "AC92e93a8272f450acb66c359d003d6cc4"
AUTH_TOKEN = "668f6f36a779da7d790731634599c6a0"




def get_otp(length, options="1234567890QWERTYUIOPASDFGHJKLZXCVBNM", rand_val=1000):

    options = str(options)
    rand_val = int(rand_val)

    OTP=""
    options_len = len(options)
    #print(options_len)

    for i in range(length):
        #print(random.randint(0, 100))
        OTP += options[random.randint(0,rand_val) % options_len]

    return OTP




def send_sms(message="Hello, This is a test message", number=MY_PH_NUM):

	client = Client(ACCCOUNT_SID, AUTH_TOKEN)

	if TRIAL_VERSION:
		number = MY_PH_NUM

	number = number.strip()
	if (number[0] != '+'):
		number = '+91' + number

	sms = client.messages.create(
				
				from_ = FROM_PH_NUM,
				body = message,
				to = number,
	)

	return sms.sid

