from openai import OpenAI, OpenAIError
import datetime
import pyttsx3
import speech_recognition as sr
import time
import sys
import base64
import playsound

messages = [
	{'role' : 'system', 'content' : 'Your name is Kioku, which means memory in Japanese. Your job is to have friendly \
	  conversation with xxxx who is having onset of dementia. Start conversation by asking her about her family details \
	  Doctor has advised to keep her memory active by engaging her in a conversation which will make her recall names of \
	  people, places, events, dates etc. \
	  These are her personal and family details. Her name is xxxx. Her age is 82. She has two children, daughter Aaaa and son Rrrrr \
	  She lives in Mmmm, Oooo with her son. Her daughter in laws name is Pppp and the son in law is Aaaa \
	  Aaaa has two children, daughter Nnnn and son Ssss. Rrrr also has two kids, son Rrrr and daughter Rkkk \
	  Aaaa lives in Pppp. Aaaa used to live in zzz for 10 years and she moved to Pppp in 200x \
	  Nnnn got married in 2023 december with Kii. They live in Sssss, USA. All other grandkids are unmarried \
	  Rrrr and Rkkk are in Aaaa pursuing further education \
	  Ssss has completed graduation and is working in USA \
	  Rrr is yyy at company name \
	  Nnnn has degree in biotech and has completed hhhh and is working as a llll in a startup \
	  She has three brothers and two sisters. Out of three, two brothers - Dddd and Hhhh are deceased and one brother Yyyy is living in Ppp \
	  Both her sisters are alive and one sister Mmm lives in Ppp while other sister Nnn lives in Mmmm \
	  She was born in pob which is in state of country \
	  Ppp has bachelors degree in eeeee and she worked in a vvv before getting married \
	  Ppp got married to Vvvv and moved to Ppp after marriage \
	  Open the conversation by greeting Pppp and then start asking her about her personal details. \
	  Also give her simple math or logical problems to solve. Some sample problems are as below \
	  {if you have 10 dollars then how many apples can you buy if they cost 2.5 dollar each} \
	  {if ram is older than sita and sita is older than bharat then who is oldest between them} \
	  {if you have a 3 litre and 2 litre measuring cups how can you measure 4 litres of milk using them} \
	  if her answer to logical problems or about her personal details is incorrect then inform that to her politely \
	  and also provide correct answer. Ignore the case in names of people and places.\
	 '}
]

keep_going = True
    
def sayIt(text: str):
	engine = pyttsx3.init()
	engine.say(text)
	engine.runAndWait()
	del(engine)

def textIt():
	recognizer = sr.Recognizer()

	with sr.Microphone() as source:
		print("Please say something...")
		audio = recognizer.listen(source)

	try:
        # Recognize speech using Google Web Speech API
		text = recognizer.recognize_google(audio)
		print(text)
		return text
	except sr.UnknownValueError:
		print("Sorry, I could not understand the audio.")
		return 'Sorry Pushpa, I could not get what you said, please repeat'
	except sr.RequestError:
		print("Could not request results; check your network connection.")
		return 'Sorry Pushpa, I could not get what you said, please repeat'


def gptResponse():

	prompt = textIt()

	if prompt.find('bye') > 0 or prompt.find('enough') > 0:
		keep_going = False
		sayIt('It was nice talking to you Pushpa. Take care of yourself, drink pleanty of water and do not worry excessively. \
			   we will talk again, bye for now.')
		sys.exit('Have a good day Pushpa !!!')

	messages.append({'role' : 'user', 'content' : prompt})

	resp = get_completion(messages)

	messages.append({'role' : 'assistant', 'content' : resp})

	sayIt(resp)
#	time.sleep(2)

def main():
	
	OpenAI.api_key  = 'your api key unless set in environment'   

	now = datetime.datetime.now()
	day = now.strftime("%A")
	date = now.strftime("%d")
	month = now.strftime("%B")
	th = 'th'
	if day == 1:
		th = 'st'
	elif day == 2:
		th = 'nd'
	elif day == 3:
		th = 'rd'



#	greeting = '<center>!!! Hello Pushpa, how are you today ? Let us have a little conversation to activate your memory !!!<br>'
#	greeting += 'Today is '+day+' the '+str(date)+th+' of '+month+' and its a lovely day outside.</center>'
#	print(greeting)

	sayIt('Hello Pushpa, how are you today? My name is Kioku, which means memory in Japanese. \
				Today is '+day+' the '+str(date)+th+' of '+month+' and its a lovely day outside. \
	   			I will ask you about your family and also give you some easy math or logic problems to solve.\
				With this you willl keep your memory sharp. So, lets go.')

#	return 'Kioku is running'
	while keep_going:
		gptResponse()
#		time.sleep(2)

	sys.exit('Have a good day Pushpa !!!')


def get_completion(messages, model="gpt-4o-audio-preview", temperature=0):
    
    client = OpenAI()

    try:
        response = client.chat.completions.create(
            model=model,
			modalities=["text", "audio"],
    		audio={"voice": "alloy", "format": "mp3"},
            messages=messages,
            temperature=temperature
			)
#        print(base64.b64decode(response.choices[0].message.audio.data))
        wav_bytes = base64.b64decode(response.choices[0].message.audio.data)
        with open("pushpa.wav", "wb") as f:
           f.write(wav_bytes)
#        return response.choices[0].message.content
        return response.choices[0].message.audio.transcript
	
    except OpenAIError as e:
        return f"Error: {e}"

if __name__== "__main__":
	main()

