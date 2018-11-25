from flask import Flask, request, jsonify
from basket import generate_basket_from_eans, get_basket, put_item_into_basket, get_total_price
from badges import save_receipt

headers = {
    "Content-Type": "application/json",
}

app = Flask(__name__)

@app.route("/add", methods=["POST"])
def search():
    response = request.get_json()
    result = generate_basket_from_eans(response['eans_list'], 'K171')
    return jsonify(result), 200, headers

@app.route("/items", methods=["GET", "POST"])
def items():
    if request.method == "GET":
        result = get_basket('39693627', '1c2429dc3069a743980419d3b2350905fada2702')
        return jsonify(result), 200, headers
    elif request.method == "POST":
        ean = request.form['ean']
        position = request.form['position']
        result = put_item_into_basket(
            '39693627', '1c2429dc3069a743980419d3b2350905fada2702', ean, position, 1)
        return jsonify(result), 200, headers
    else:
        return jsonify({}), 500, headers

@app.route('/person', methods=["POST"])
def person():
    response = request.get_json()
    result = save_receipt(response['eans_list'])
    # app.logger.info(result.__dict__.description)
    for badge in result.__dict__:
        app.logger.info(badge, result.__dict__[badge].__dict__)
    app.logger.info(vars(result))
    serialized = [vars(result[key]) for key in vars(result)]

    app.logger.info(serialized)
    return jsonify(serialized), 200, headers

if __name__ == '__main__':
    app.run(debug=True)
