class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'




import sys
import requests
import pprint
from time import sleep
import json
from math import ceil

#TODO : DISPLAY PROMPT

print(f"{bcolors.HEADER}{bcolors.BOLD}                                              Welcome to Brevity")
print(f"{bcolors.UNDERLINE} {bcolors.OKGREEN}What it does")
print(f"{bcolors.ENDC}{bcolors.OKBLUE} Brevity takes in a lecture video and gives out the sumarised versiom of the lecture removing all unnneccessary fillers and keeping only the most important points")
print(f"{bcolors.UNDERLINE} {bcolors.OKGREEN}How to use")
print(f"{bcolors.ENDC}{bcolors.OKBLUE} Just enter the file path and it'll do the work for you")
print(f"{bcolors.UNDERLINE}{bcolors.OKGREEN} Enter lecture path {bcolors.ENDC}")
path = input()




# store global constants
auth_key = 'f35046714feb444c8fc2b54b7b4b6f8f'
headers = {
   "authorization": auth_key,
   "content-type": "application/json"
}
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
upload_endpoint = 'https://api.assemblyai.com/v2/upload'
 
# make a function to pass the mp3 to the upload endpoint
def read_file(filename):
   with open(filename, 'rb') as _file:
       while True:
           data = _file.read(5242880)
           if not data:
               break
           yield data
 
# upload our audio file
upload_response = requests.post(
   upload_endpoint,
   headers=headers, data=read_file(path)
    #    sys.argv[1]) #! THIS IS THE ARGUMENT
)
print('Audio file uploaded')
 
# send a request to transcribe the audio file
transcript_request = {'audio_url': upload_response.json()['upload_url']}
transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
print('Transcription Requested')
pprint.pprint(transcript_response.json())
# set up polling
polling_response = requests.get(transcript_endpoint+"/"+transcript_response.json()['id'], headers=headers)
filename = 'File_out/' + 'assmebly_out' + '.txt'
# if our status isn’t complete, sleep and then poll again
while polling_response.json()['status'] != 'completed':
   sleep(30)
   polling_response = requests.get(transcript_endpoint+"/"+transcript_response.json()['id'], headers=headers)
   print("File is", polling_response.json()['status'])
with open(filename, 'w') as f:
    f.write(polling_response.json()['text'])
print('Transcript saved to', filename)


'''
# Replace by your API key from Sassbook AI.
#! Replace API key
API_KEY="U2FsdGVkX1+mcE1hqAZafVJ2j19oyizEHiRTu4ulcJX5TonSZTjoMh/CTOLF3wXWPEwHyVINABS+l2uc1r3Q6skPymvwRhPL91kMe5kMJPqAE8nl9KbrQWU6FTzACPSlmwzuBDFmbIRojO8Iyek/bP21vlR883G2cz9kxDNUiSe3EYsJkAGWAoPtiPnUS/DaeX9w+QlWHatQnnRKYnCIng=="
authHeaderVal = f"Bearer {API_KEY}"
endPoint='https://sassbook.com/api/ext/summarize/v1'

# Text to summarize (UTF-8) loaded from file
# with open(sys.argv[1],'r') as file:
#     inText = file.read()

inText = polling_response.json()['text']

postHeaders = {'Content-type': 'application/json; charset=UTF-8',
    'Accept': 'application/json', 'Authorization': authHeaderVal }

# Target size
target = 'verbose' # See docs for other options
method = 'abstractive' # Or 'extractive'
payload = { 'sumSrc': inText, 'target': target, 'method': method }

try:
    # Make the API call
    response = requests.post(endPoint,
        data=json.dumps(payload),
        headers=postHeaders,
        timeout=250,
        allow_redirects=True)

    print("API call completed: ", response.ok)
    # Check the status code etc...
    respJson = response.json()
    if respJson.get('code'): # API returned error JSON
        print(f"API returned error code: {respJson['code']}")
        print(f"Error message: {respJson['message']}")
    else: # API returned result JSON
        with open("output.txt","w") as file:
            file.write(respJson['summary'] + "\n" + "Read time : " + str(ceil(len(respJson['summary'].split(" ")) / 250)) + " mins")
        # Print and inspect other properties here...
except Exception as e:
    print(f"An exception occurred while calling the API: {str(e)}")

sys.exit(0)
'''