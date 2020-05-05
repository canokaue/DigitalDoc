from twilio.rest import Client

def send_sms(data):
    account_sid = 'AC11e4235ca56d17fbff7e15eda642dd5d'
    auth_token = '19c06ac9950a7515c798bb30dc67d8'
    client = Client(account_sid, auth_token)

    message = str("DigitalDoc succesful! \n\
Check you document on the blockchain by using the following link: \n\n%s" % data)
    
    message = client.messages \
        .create(
            body= message,
            messaging_service_sid='MG13349c5cd5c143f605bfffafb9b80210',
            to='+5566996655998'
        )

    print('Message succesfuly sent with pid: ' + message.sid)

# if __name__ == '__main__':
#     send_sms(dict(flick='mywrist'))