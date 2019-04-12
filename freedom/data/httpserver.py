import json

import freedom.data.gather_data
from freedom.httpserver import app


@app.route("/data/collect", methods=["GET"])
def gather_data():
    freedom.data.gather_data.__process_gather_stock_trade_data()
    return json.dumps({
        "ret": True, "msg": "任务已启动"
    })
