import os
import subprocess
import rocksdb
from flask import Flask, request, jsonify

UPLOAD_FOLDER = '/app/uploads/'
ALLOWED_EXTENSIONS = set(['py'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = rocksdb.DB("assignment1.db", rocksdb.Options(create_if_missing=True))

def execute(filepath):
    """
    Execute python file at the provided path and return output
    """
    proc = subprocess.Popen(['python3', filepath], stdout=subprocess.PIPE)
    outs, errs = proc.communicate()
    return outs

def store_file(filename, filepath):
    """
    store the file path in DB and return generated id for the script
    """
    id = 0
    for c in list(filename): #generate ID based upon ascii characters
        id+=ord(c)
    key = bytes(str(id),'ascii')
    value = bytes(filepath, 'ascii')
    db.put(key, value) #store key-value pair in rocksDB
    return str(id)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def hello_word():
    return 'Hello World!'

@app.route('/api/v1/scripts', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'data' not in request.files:
            return jsonify({'message': 'Error with uploaded file'})
        file = request.files['data']
        if file.filename == '':
            return jsonify({'message':'File Name Empty'})
        if file and allowed_file(file.filename):
            filepath=os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            id = store_file(file.filename, filepath)
            return jsonify({'script-id': id}), 201

@app.route('/api/v1/scripts/<int:script_id>', methods=['GET'])
def run_script(script_id):
    key = bytes(str(script_id),'ascii')
    value = db.get(key)
    if value is None:
        return "No such ID"
    filepath = value.decode('ascii')
    return execute(filepath)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
