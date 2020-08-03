
from flask import Flask, jsonify, request, send_file
from controller import start_process, get_result_file
import os

app_port = os.getenv('PORT') or 5000

server = Flask(__name__, port=)
server.config['DEBUG'] = True

if not os.path.isdir('temp'):
    os.mkdir('temp')
if not os.path.isdir('storage'):
    os.mkdir('storage')


@server.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'hello from vidcast'})


@server.route('/podcastfy', methods=['POST'])
def process():
    config = request.json
    position = start_process(config)
    return jsonify({'status': 'OK', 'queue_position': position})


@server.route('/result/<file_name>', methods=['GET'])
def get_result(file_name):
    result_file_path = get_result_file(file_name)
    if not result_file_path:
        return jsonify({'status': 'NOT_FOUND'}), 404
    else:
        return send_file(f'../{result_file_path}', attachment_filename=f'{file_name}.mp3', mimetype='audio/mpeg')


if __name__ == '__main__':
    server.run()
