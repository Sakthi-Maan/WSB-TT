from playsound import playsound
import time


data = ['YAVVATHUURAIVATHU ULAGAM.mp3',
        'NALLINATHIN OONGUM THUNAI ILLAI.mp3', 'YANAITHU NINAIPPINUM KAAYAAR.mp3']
for i in range(len(data)):
    playsound('/var/www/html/calendar/thirukkural_audio/'+data[i])
    time.sleep(3)
