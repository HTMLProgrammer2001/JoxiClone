from flask import send_file, request, abort, jsonify, make_response
import os, random, string

from server import app, db
from models.File import File


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@app.route('/')
def test():
    return make_response('Test')


@app.route('/save', methods=['POST'])
def save_file():
    image = request.files.get('image')
    print(image)

    if not image:
        return abort(422)

    secureName = get_random_string(16)
    extension = image.filename.rsplit('.', 1)[1]
    fullName = secureName + '.' + extension
    uploads_dir = './Server/files'
    file = File(name=secureName, extension=extension)

    db.session.add(file)
    db.session.commit()

    image.save(os.path.join(uploads_dir, fullName))

    return jsonify({
        'message': 'Photo successfully saved',
        'path': f'http://localhost:5000/image/{secureName}'
    })


@app.route('/image/<imageName>')
def get_image(imageName: str):
    file = File.query.filter_by(name=imageName).first()

    if not file:
        return abort(404)

    return send_file(f"files/{file.name}.{file.extension}")
