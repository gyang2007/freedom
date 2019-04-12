from flask import Flask

app = Flask(__name__)

import freedom.data.httpserver


@app.route("/test", methods=["GET"])
def data():
    return """
        <!html>
        <head>
            <title>Test</title>
        </head>
        <body>
            <h2>Test!!!</h2>
        </body>
        </html>  
    """
