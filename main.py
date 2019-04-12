import sys
from os import path

sys.path.append(path.dirname(__file__))

from freedom.httpserver import app


@app.route("/", methods=["GET"])
def home():
    return """
        <!html>
        <head>
            <title>Home</title>
        </head>
        <body>
            <h2>Hello world!!!</h2>`
        </body>
        </html>  
    """


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
