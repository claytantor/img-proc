from flask import Flask, request, jsonify, send_file
import glob
import random
from facegen import pipeline

app = Flask(__name__)
app.config.from_envvar('APP_CONFIG')

# # load the deeporb yaml
# config = load_yaml(app.config['DEEPORB_CONFIG'])['imgpro']

@app.route('/')
def hello_world():
    return 'Hello, img proc!'

@app.route('/config', methods=['GET'])
def get_config():
    # print(app.config)
    response = {
        'vars':{
            'ENV':app.config['ENV'],
        },
        # 'appconfig': config
    }
    return jsonify(response), 200

@app.route('/facegen', methods=['GET'])
def facegen():

    gen_filename = pipeline()
    response_file = open(gen_filename, 'rb')
    return send_file(response_file, 
        mimetype='img/png', 
        as_attachment=True, 
        attachment_filename=gen_filename.split('/')[-1] )