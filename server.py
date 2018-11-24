from flask import Flask, request, jsonify
from basket import get_product_metadata

headers = {
    "Content-Type": "application/json",
}

app = Flask(__name__)

@app.route("/groceries")
def groceries():
    q = request.args.get('q')
    result = get_product_metadata(q)
    return jsonify(result), 200, headers


if __name__ == '__main__':
    app.run()