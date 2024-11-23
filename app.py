from flask import Flask, jsonify, render_template
from database import get_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def data():
    data = get_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)