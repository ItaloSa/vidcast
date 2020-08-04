
from flask import Flask, jsonify, request, send_file
from controller import start_process, get_result_file
from werkzeug.utils import secure_filename
import os
import random
import string

if not os.path.isdir('temp'):
    os.mkdir('temp')
if not os.path.isdir('storage'):
    os.mkdir('storage')

APP_PORT = os.getenv('PORT') or 5000
UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = {'mp3', 'mp4'}

server = Flask(__name__)
server.config['DEBUG'] = True
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def random_file_name(file_name):
    return f'{get_random_string(12)}.{file_name.rsplit(".", 1)[1].lower()}'

@server.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'hello from vidcast'})


@server.route('/podcastfy', methods=['POST'])
def process():
    config = request.json
    result_name = f'{config["name"]}-{get_random_string(6)}'
    config['name'] = result_name
    position = start_process(config)
    return jsonify({'status': 'OK', 'queue_position': position, 'result_name': result_name})


@server.route('/podcastfy/upload', methods=['POST'])
def process_upload():
    if ('original_media' or 'intro_music' or 'end_music') not in request.files:
        return jsonify({'status': 'NOT_OK'}), 400

    original_media_file = request.files['original_media']
    intro_music_file = request.files['intro_music']
    end_music_file = request.files['end_music']

    file_list = [original_media_file, intro_music_file, end_music_file]
    allowed = [allowed_file(file.filename) for file in file_list]

    if False in allowed:
        return jsonify({'status': 'NOT_OK'}), 400

    original_media_name = random_file_name(original_media_file.filename)
    original_media_file.save(os.path.join(
        server.config['UPLOAD_FOLDER'], original_media_name))

    intro_music_name = random_file_name(intro_music_file.filename)
    intro_music_file.save(os.path.join(
        server.config['UPLOAD_FOLDER'], intro_music_name))

    end_music_name = random_file_name(end_music_file.filename)
    end_music_file.save(os.path.join(
        server.config['UPLOAD_FOLDER'], end_music_name))

    result_name = f'{request.form.get("name")}-{get_random_string(6)}'
    config = {
        'name': result_name,
        'make_edit': request.form.get('make_edit') == 'true',
        'original_media': original_media_name,
        'intro_music': intro_music_name,
        'end_music': end_music_name,
        'upload': True
    }
    position = start_process(config)
    return jsonify({'status': 'OK', 'queue_position': position, 'result_name': result_name})


@server.route('/result/<file_name>', methods=['GET'])
def get_result(file_name):
    result_file_path = get_result_file(file_name)
    if not result_file_path:
        return jsonify({'status': 'NOT_FOUND'}), 404
    else:
        return send_file(f'../{result_file_path}', attachment_filename=f'{file_name}.mp3', mimetype='audio/mpeg')


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=APP_PORT)
