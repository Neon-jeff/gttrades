import random

def CreateOtp():
    # creates the otp digits
    # set otp expiry------> Jesus what was i thinking lol
    # maybe i should return a dict with 
    # the new otp and required timestamp
    # am i overcomplicating things :/
    otp=''
    for i in range(0,6):
        otp+=str(random.randint(0,9))
    return otp



def SendOTP():
    # call email service and send the otp
    pass

def VerifyOTP():
    # verify the otp
    pass

