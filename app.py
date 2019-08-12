import requests
import speech_recognition as sr 
from os import path,chdir,getcwd
from pprint import pprint
import json
from pydub import AudioSegment 
from pydub.silence import split_on_silence
import os 
from flask import url_for


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

        
        audio = AudioSegment.from_wav(r"static/uploads/{}".format(fname))
        n=len(audio)
        counter=1
        print("function works")
        fh = open("recognized.txt", "w+")
        interval = 60*1000
        overlap = 1.5*1000
        start=0
        end=0
        # When audio reaches its end, flag is set to 1 and we break 
        flag = 0
        for i in range(0,2*n,interval):
            if i == 0:
                start=0
                end=interval
            else:
                start=end-overlap
                end=start+interval
            # When end becomes greater than the file length, 
    # end is set to the file length 
    # flag is set to 1 to indicate break. 
            if end>=n:
                end=n
                flag=1
            chunk =audio[start:end]
            filename = 'chunk'+str(counter)+'.wav'
            chunk.export(r'audio_chunks/{}'.format(filename), format ="wav") 
            print("Processing chunk "+str(counter)+". Start = "
                        +str(start)+" end = "+str(end)) 
            counter = counter + 1

            AUDIO_FILE = filename
  
        
            r=sr.Recognizer()
            with sr.AudioFile(r'audio_chunks/{}'.format(AUDIO_FILE)) as source: 
            # remove this if it is not working 
            # correctly. 
                r.adjust_for_ambient_noise(source) 
                audio_listened = r.listen(source) 

            try: 
            # try converting it to text 
                rec = r.recognize_google(audio_listened) 
            # write the output to the file. 
                fh.write(rec+" ") 
  
            # catch any errors. 
            except sr.UnknownValueError: 
                print("Could not understand audio") 
            
            except sr.RequestError as e: 
                print("Could not request results. check your internet connection") 
  
            if flag==1:
                fh.close()
                break






        
  

        

        try:
            output = open("recognized.txt", "r")
            #output=r.recognize_google(audio)#show all = true will show all possibilites of how google translates this audio to text
            #print("Over")
            #print("output received from google speech api ")

            #sending output to punctuator api using post request
            url_punctuator="http://bark.phon.ioc.ee/punctuator"
            data={'text':'{}'.format(output.read())}
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




