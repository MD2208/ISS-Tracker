import requests
import datetime as dt
import smtplib
import time
MY_LAT = 50.064651 # Your current location should be entered
MY_LONG = 19.944981 # Mine is Krakow
MY_MAIL = "sender@gmail.com"
MY_PASSWORD = "sender_app_pass"

## ---- Find ISS pos ---- ##
iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
iss_response.raise_for_status()
iss_data = iss_response.json()
iss_long = float(iss_data['iss_position']['longitude'])
iss_lat = float(iss_data['iss_position']['latitude'])

## ---- Use sunrise/sunset API --- ###
parameters ={
    'lat': MY_LAT,
    'lng' : MY_LONG,
    'formatted' : 0
}
sun_response = requests.get(url='https://api.sunrise-sunset.org/json',params=parameters)
sun_response.raise_for_status()

sun_data = sun_response.json()
sunrise = int(sun_data['results']['sunrise'].split("T")[1].split(":")[0])
sunset = int(sun_data['results']['sunset'].split("T")[1].split(":")[0])
## --- Get current Time as hour -- ##
now = dt.datetime.now()
time_now = now.hour
## --- Compare location of ISS to my loc and Check the sky dark enough ---##
## --- Run the program and check in 60 sec to send mail --- ##
while True:
    time.sleep(60)
    if (iss_lat <= MY_LAT + 0.5 and iss_lat >= MY_LAT - 0.5) and (iss_long <= MY_LONG + 0.5 and iss_long >= MY_LONG - 0.5):
        if time_now > sunset or time_now < sunrise:
            ## -- Send an Email by smtlip -- ##
            with smtplib.SMTP("smtp.gmail.com") as connection:
                ## -- Correct sender and reciever email before run it! ---#
                connection.starttls()
                connection.login(user=MY_MAIL,password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_MAIL,
                    to_addrs='reciever@gmail.com',
                    msg=f"Subject:ISS-TRACKER\n\nThe current location of ISS is {iss_lat} and {iss_long}. Look up and try to find it!"
                )
    #     else:
    #         print('Sky is not dark enough')
    # else:
    #     print('ISS is not Close enough')