# ======================================= IMPORTS ====================================#
import requests, os
from dotenv import dotenv_values
from PyInquirer import prompt


# ======================================= VARIABLES ====================================#
arrayOfChoices = []
config = dotenv_values(".env")

if config.__len__() != 0:
    token = config['TOKEN']
    url = config['URL']
    username = config['USERNAME']
    header = {'Authorization': 'token %s' % token} 
else:
    token = '' 
    username = ''
    header = {}
    url = 'https://api.github.com/repos/francisco-neto-fit/apriltag-imgs/contents/'

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
familyName = choice.split(sep='-)')[1]

option = arrayOfChoices[index - 1]
index = 0

questions = [
    {
        'type': 'list',
        'name': 'choice',
        'message': 'Quantas aprilTAgs deseja baixar?',
        'choices':['1-)Uma','2-)Todas']
    }
]

quantityOption = prompt(questions)['choice']

if quantityOption.find('2') != -1:
    response = requests.get(option['url'],headers=header).json()
    arrayOfChoices = []
    os.mkdir(path=familyName)
    for data in  response:
        index += 1
        
        img = requests.get(data['download_url'], headers=header)
        path = familyName+'/'+data['name']
        if data['name'].find('tag') != -1:
            file = open(path, "wb")
            file.write(img.content)
            file.close()  
            print('✅Arquivo: '+ path + 'criado')  
else:
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
    path = familyName+'/'+option['fileName']
    os.mkdir(path=familyName)
    file = open(path, "wb")
    file.write(img.content)
    file.close()

print('Script executado com sucesso!✅')
print('¯\_(ツ)_/¯')

