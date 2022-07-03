import requests
import os


name = ""
def unload_photo(object):
    global name
    with open(os.path.dirname(os.path.abspath(__file__))+ '/photos'+'/'+object+'.jpg', "rb") as f:
        print(f"{os.path.dirname(os.path.abspath(__file__))}")
        multiple_files = [('file', (object+'.jpg', f, 'image/jpg'))]
        r = requests.post('https://imaginarysoundscape2.qosmo.jp:8000/process?save=1', files=multiple_files)
        json_response = r.json()
        sound_id = json_response.get('sound_id')
        name = sound_id
        print(f'mp3 url is https://storage.imaginarysoundscape.net/sounds/{sound_id}.mp3')


def download_mp3():
    url = f'https://storage.imaginarysoundscape.net/sounds/{name}.mp3'
    save = requests.get(url)
    with open(os.path.dirname(os.path.abspath(__file__)) + f'/sounds/{name}.mp3', 'wb') as f:
        f.write(save.content)
        return name