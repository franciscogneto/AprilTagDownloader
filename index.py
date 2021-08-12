# ======================================= IMPORTS ====================================#
import requests
from dotenv import dotenv_values
from PyInquirer import prompt


# ======================================= VARIABLES ====================================#
arrayOfChoices = []

config = dotenv_values(".env")
token = config['TOKEN']
url = config['URL']
username = 'francisco-neto-fit'
header = {'Authorization': 'token %s' % token}
index = 0
# ======================================= GETTING DATA ====================================#
# Request to get the tag familys in respository

response = requests.get(url=url,headers=header).json();
for data in response:
    name = str(data['name'])
    if(not(name.__eq__("README.md"))):
        index += 1
        option = str(index)+'-)'+ data['name']
        arrayOfChoices.append({'name':option,'url':data['url']})

questions = [
    {
        'type': 'list',
        'name': 'choice',
        'message': 'Qual familia de tag você quer?',
        'choices':arrayOfChoices
    }
]
choice = prompt(questions)
choice = str(choice['choice'])
index = int(choice.split(sep='-)')[0])

option = arrayOfChoices[index - 1]
index = 0

response = requests.get(option['url'],headers=header).json()
arrayOfChoices = []

for data in  response:
    index += 1
    option = str(index)+'-)'+ data['name']
    arrayOfChoices.append({'name':option,'download_url':data['download_url'], 'fileName':data['name']})

questions = [
        {
            'type': 'list',
            'name': 'choice',
            'message': 'Qual AprilTag você quer?',
            'choices':arrayOfChoices
        }
    ]    
choice = prompt(questions)['choice']

index = int(choice.split(sep='-)')[0])

option = arrayOfChoices[index - 1]

img = requests.get(option['download_url'], headers=header)
path = "aprilTags/"+option['fileName']
file = open(path, "wb")
file.write(img.content)
file.close()

print('Script executado com sucesso!')



