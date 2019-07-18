import requests
import speech_recognition as sr 
from os import path,chdir,getcwd
from pprint import pprint
import json

with open("config.json","r") as c:
    params=json.load(c)["params"]
class MomGenerator:
    '''def recognizerWithMicrophone():

        r=sr.Recognizer()#creating instance of recognizer class

        #using microphone for source input
        with sr.Microphone() as source:
            print("Speak!")
            audio = r.listen(source) #collecting the audio for recognizer
            print("Over")

        #translate..

        try:
            text = r.recognize_google(audio) #the text stores whatever google api returns 
            print("you said,",text) #printing what google api returned

        except:
            print("Could not recognize")
            #exception if google api doesn't understand what you said'''


    def recognizerWithAudioFile(fname):
        
        '''chdir(r"static/uploads")
        audio_file=path.join(path.dirname(path.realpath(__file__)),"{}".format(fname))'''
        
  

        r=sr.Recognizer()
        with sr.AudioFile(r"C:\Users\admin\Desktop\MinutesOfMeeting\static\uploads\{}".format(fname)) as source:
            audio=r.record(source)

        try:
            output=r.recognize_google(audio)#show all = true will show all possibilites of how google translates this audio to text
            #print("Over")
            print("output received from google speech api ")

            #sending output to punctuator api using post request
            url_punctuator="http://bark.phon.ioc.ee/punctuator"
            data={'text':'{}'.format(output)}
            response_from_punctuator=requests.request("POST",url_punctuator,data=data)
            #print("text returned from punctuator api:",response_from_punctuator.text)

            punctuated_text=response_from_punctuator.text
            print("output received from punctuator api ")
            response = requests.post("https://api.aylien.com/api/v1/summarize?title='text'&text={}&sentences_number=10".format(punctuated_text),
            headers={
                "X-AYLIEN-TextAPI-Application-Key":"{}".format(params["aylien-api-key"]),
                "X-AYLIEN-TextAPI-Application-ID":"{}".format(params["aylien-app-id"])
            }
            )
            

            #don't uncomment this meaning cloud 
            #sending the punctuated text to meaningcloud api using the api key
            '''    url = "https://api.meaningcloud.com/summarization-1.0"

                payload = "key=440a3e9fde785d6b5aa4bd1595052891&txt={}&url=&doc=&sentences=10".format(punctuated_text)
                headers = {'content-type': 'application/x-www-form-urlencoded'}
                #application/x-www-form-urlencoded

                response = requests.request("POST", url, data=payload,headers=headers)'''
                
            #headers=headers
            #dont uncomment :D

    
            #printing json object
           # print("text returned from meaning cloud api:",response.json()['summary'])
            text=response.json()['sentences']
            print("output received from aylien")

            
            
        # pprint("original output:",output)

            #output also shows the accuracy of its conversion...check key confidence and transcript in output means the difference conversions of the audio file
            
        except:
            return "Could not recognize" #exception if google api doesn't understand 

        return text


    #choice=int(input("Enter a choice 1)Microphone 2)Audio File"))
    '''if choice==1:
        recognizerWithMicrophone()'''
    #else:
    #commenting out other stuffs

    #recognizerWithAudioFile()




