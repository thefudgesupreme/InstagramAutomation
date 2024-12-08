CLIENT_ID = '4fd64d36c4a6b7e'
CLIENT_SECRET='b3e1314cee8dd48e76a9344fee3e55ac2b4acf66'

import requests, os, json

def post_image(title, description, path):
    image_name=os.path.basename(path)
    url = "https://api.imgur.com/3/image"

    payload={'type': 'image',
    'title': f'{title}',
    'description': f'{description}'}
    files=[
    ('image',(f'{image_name}',open(path,'rb'),'image/jpeg'))
    ]
    headers = {
    'Authorization': f'Client-ID {CLIENT_ID}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files).json()
    print(response['data']['link'])
    if response['status'] == 200:
        return True,response['data']['link']
    else:
        return False, ""

if __name__ == '__main__':
    post_image('test', 'test', 'F:\\Instagram\\PictoSynth\\Images\\Raw\\All\\9034730247_SocamergeAniMixXL.safetensors_006.jpeg')