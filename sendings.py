import requests
from pysendpulse.pysendpulse import PySendPulse
import pandas as pd

def to_mobile(mobile):
    nums = '0123456789'
    translated = ''
    for number in str(mobile):
        if number in nums: translated += number
    return translated

def check_track(track):
    if track == '-':
        return True
    if len(track) != 14 or track[0:6] != '295000':
        return False
    return True

def send_sms(track, phone_num):
    sms_aero_api = 'YOUR_API_KEY'
    my_email = 'YOUR_EMAIL'

    is_tracking = True
    if track == '-': is_tracking = False
    sms_text = ''
    if is_tracking: 
        sms_text = 'Заказ был отправлен! Ваш трек номер - '+ str(track) + '\n===\nBunny Kam'
    else:
        sms_text = 'Здравствуйте, ваш заказ был отправлен!\n===\nBunny Kam'
    r = requests.get('https://'+ my_email +':'+ sms_aero_api +'@gate.smsaero.ru/v2/sms/send?number='+ phone_num +'&text='+ sms_text +'&sign=SMS Aero')

def send_email(name, track, email):
    REST_API_ID = 'YOUR_REST_API_ID'
    REST_API_SECRET = 'YOUR_REST_API_SECRET'
    TOKEN_STORAGE = 'memcached'
    MEMCACHED_HOST = '127.0.0.1:11211'
    SPApiProxy = PySendPulse(REST_API_ID, REST_API_SECRET, TOKEN_STORAGE, memcached_host=MEMCACHED_HOST)
    
    # email templates
    email_track = {
        'subject': 'Уведомление с сайта Bunny Kam',
        'html': '<h1>Привет, ' + name + '</h1><p>Мы отправили твой заказ! Твой трек-номер - '+ str(track) +'</p><p>Отследить заказ можно на сайте Почты России - https://www.pochta.ru/tracking</p>',
        'text': 'Привет, ' + name + 'Мы отправили твой заказ! Твой трек-номер - '+ str(track) +'Отследить заказ можно на сайте Почты России - https://www.pochta.ru/tracking',
        'from': {'name': 'Bunny Kam', 'email': 'info@bunnykam.ru'},
        'to': [
            {'name': name, 'email': email}
        ]
    }

    email_non_track = {
        'subject': 'Уведомление с сайта Bunny Kam',
        'html': '<h1>Привет, ' + name + '</h1><p>Мы отправили твой заказ!</p>',
        'text': 'Привет, ' + name + 'Мы отправили твой заказ!',
        'from': {'name': 'Bunny Kam', 'email': 'info@bunnykam.ru'},
        'to': [
            {'name': name, 'email': email}
        ]
    }
    # choosing template for sending
    if track != '-':
        SPApiProxy.smtp_send_mail(email_track)
    else: 
        SPApiProxy.smtp_send_mail(email_non_track)

# main function
def send_notifications(filename):
    send_table = pd.read_csv(filename)

    names = send_table['Имя получателя']
    phones = send_table['Телефон']
    tracks = send_table['Трек-номер']
    emails = send_table['Email']

    track_error = open('track_error.txt', 'w')

    error_count = 0

    for i in tracks:
        if check_track(str(i)) == False:
            error_count += 1
            track_error.write(str(i))
            track_error.write('\n')

    track_error.close()

    if error_count == 0:
        for i in range(len(names)):
            send_sms(names[i], tracks[i], to_mobile(phones[i]))
            print("SMS на номер " + str(to_mobile(phones[i])) + " отправлено")
            send_email(names[i], tracks[i], emails[i])
            print("E-mail на почту " + str(emails[i]) + " отправлен")
            print("#"*20)
            print("Отправлено " + str(i+1) + " уведомлений из " + str(len(names)))
            