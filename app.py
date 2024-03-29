from flask import Flask, render_template, request, send_from_directory, stream_with_context
import os
import re
import json
import pandas as pd
import string

from generator import generate_csv, yield_rows


FILE_FOLDER = os.path.join("static", "files")
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate_table", methods=['POST'])
def generate_table():
    columns = request.form['columns']
    # print(columns)
    nrows = int(request.form['nrows'])
    response, _ = generate_csv(columns, nrows=nrows, temperature=1)
    return stream_with_context(yield_rows(response))


@app.route("/save_table", methods=['POST'])
def save_table():
    table_str = request.form['table']
    filename = "table1.csv"
    df = pd.read_html(table_str)
    if len(df) != 1:
        return ""
    df = df[0]
    save_path = os.path.join(FILE_FOLDER, filename)
    df.to_csv(save_path, index=None, encoding='utf-8')
    return send_from_directory(directory=FILE_FOLDER, path=filename)


if __name__ == "__main__":
    app.run(debug=True)