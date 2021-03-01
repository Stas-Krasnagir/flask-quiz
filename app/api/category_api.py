from app import app
from flask import jsonify, wrappers, request
from app.models import Categories


@app.route('/', methods=['GET'])
def index():
    return "Home page"


@app.route('/categories/', methods=['GET'])
def categories() -> wrappers.Response:
    return jsonify(dict(Categories.get_categories()))


@app.route('/category/<int:id>', methods=['GET'])
def get_category(id: int) -> wrappers.Response:
    category = Categories.query.get_or_404(id)
    return jsonify(category.to_json())


@app.route('/category/', methods=['POST'])
def add_category() -> wrappers.Response:
    category = request.form['data']
    try:
        Categories.check_exist_category(category)
        Categories.add(category)
        return jsonify({"201 Created": "HTTP/1.1"})
    except:
        return jsonify({"403 Forbidden": "HTTP/1.1"})

    # category = request.form['data']
    # if Categories.check_exist_category(category):
    #    return jsonify({"403 Forbidden": "HTTP/1.1"})
    # Categories.add(category)
    # return jsonify({"201 Created": "HTTP/1.1"})


@app.route('/category/<int:id>', methods=['DELETE'])
def delete_category(id: int) -> wrappers.Response:
    Categories.query.get_or_404(id)
    Categories.delete_note(id)
    return jsonify({"200 OK": "HTTP/1.1"})


@app.route('/category/<int:id>', methods=['PUT'])
def edit_category(id: int) -> wrappers.Response:
    Categories.query.get_or_404(id)
    try:
        Categories.edit(request.form['data'], id)
        return jsonify({"200 OK": "HTTP/1.1"})
    except:
        return jsonify({"403 Forbidden": "HTTP/1.1"})
