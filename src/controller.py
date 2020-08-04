import requests
from Queue import Queue
from Pocast import Podcast
import time
import os

original_media_name = 'original.mp4'
intro_music_name = 'intro.mp3'
end_music_name = 'end.mp3'
process_queue = None


def start_process(config):
    print('>> start process')
    queue = get_queue()
    position = queue.enqueue(process, config)
    return position


def get_queue():
    global process_queue
    if not process_queue:
        print('>> create queue')
        process_queue = Queue()
    return process_queue


def process(config):
    if 'upload' in config:
        return process_upload(config)
    else:
        return process_download(config)

def process_upload(config):
    print('>> Process Start - UPLOAD')
    podcast = Podcast(
        config['name'], make_edit=config['make_edit'])
    podcast.process(config['original_media'], config['intro_music'], config['end_music'])
    clear_file(config['original_media'])
    clear_file(f'{config["original_media"].rsplit(".", 1)[0]}.mp3')
    clear_file(config['intro_music'])
    clear_file(config['end_music'])
    print('>> Process End')

def process_download(config):
    print('>> Process Start - DOWNLOAD')
    download(original_media_name, config['original_media'])
    download(intro_music_name, config['intro_music'])
    download(end_music_name, config['end_music'])
    podcast = Podcast(
        config['name'], make_edit=True if 'make_edit' in config and config['make_edit'] else False)
    podcast.process(original_media_name, intro_music_name, end_music_name)
    clear_file(original_media_name)
    clear_file(f'{original_media_name.rsplit(".", 1)[0]}.mp3')
    clear_file(intro_music_name)
    clear_file(end_music_name)
    print('>> Process End')

def download(file_name, url):
    print(f'>> download - {url}')
    r = requests.get(url, allow_redirects=True)
    open(f'temp/{file_name}', 'wb').write(r.content)


def clear_file(file_name):
    print(f'>> clear_file - {file_name}')
    os.remove(f'temp/{file_name}')


def get_result_file(file_name):
    if not os.path.isfile(f'storage/{file_name}.mp3'):
        return None
    return f'storage/{file_name}.mp3'
