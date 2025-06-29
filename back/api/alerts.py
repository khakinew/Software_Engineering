from flask import Blueprint, jsonify
from models.models import db, MonitorData
from datetime import datetime

alerts = Blueprint("alerts", __name__, url_prefix="/api/alerts")

# 合理范围（可配置）
ALERT_THRESHOLDS = {
    "temperature": (5, 35),           # ℃
    "ph": (6.5, 9.0),                 # 无量纲
    "dissolved_oxygen": (4, 14),      # mg/L
    "turbidity": (0, 100),            # NTU
    "ammonia_nitrogen": (0, 1.5),     # mg/L
}

@alerts.route("/latest", methods=["GET"])
def get_latest_alert():
    # --- 模拟报警开始 (临时测试代码) ---
    # mock_alert = {
    #     "field": "temperature",
    #     "value": 40,
    #     "message": "温度警告：当前值 40℃严重超出阈值 [5, 35]"
    # }
    # return jsonify(code=200, alerts=[mock_alert])
    # --- 模拟报警结束 ---

    # 获取最近一条监测数据
    latest = MonitorData.query.order_by(MonitorData.id.desc()).first()
    if not latest:
        return jsonify(code=404, message="暂无监测数据")

    alerts = []
    for field, (min_val, max_val) in ALERT_THRESHOLDS.items():
        value = getattr(latest, field, None)
        if value is not None and (value < min_val or value > max_val):
            alerts.append({
                "field": field,
                "value": value,
                "message": f"{field} 异常：当前值 {value} 超出范围 [{min_val}, {max_val}]"
            })

    if alerts:
        return jsonify(code=200, alerts=alerts)
    else:
        return jsonify(code=200, alerts=[])
