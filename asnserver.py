from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    with open('merged_results.json', 'r') as file:
        merged_results = json.load(file)
    query = request.args.get('q')
    json_output = request.args.get('json') == 'true'

    if not query:
        return render_template('search.html')

    results = []
    for obj in merged_results:
        for value in obj.values():
            if isinstance(value, str) and query in value:
                results.append(obj)

    if json_output:
        return jsonify(results)
    else:
        return render_template('results.html', query=query, results=results)


if __name__ == '__main__':
    app.run(host="0.0.0.0")

