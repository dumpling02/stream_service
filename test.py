import requests
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/ai_server_metrics')
def ai_server_metrics():
    try:
        # 请求接口数据
        response = requests.get('http://192.168.137.128:1985/api/v1/clients/')
        data = response.json()

        # 初始化统计变量
        camera_count = 0
        pull_clients_count = 0
        total_alive_time = 0
        active_camera_count = 0
        alive_cameras_info = []

        # 遍历客户端数据
        for client in data['clients']:
            # 正在推流 说明该客户端是摄像头
            if client['publish']:
                camera_count += 1
                total_alive_time += client['alive']
                # 统计摄像头的连接时间
                alive_cameras_info.append({
                    "id": client['id'],
                    "alive": client['alive']
                })

                # 检查最近30秒的发送码率来确定活跃状态
                if client['kbps']['send_30s'] != 0:
                    active_camera_count += 1
            # 统计拉流客户端
            else:
                pull_clients_count += 1

        # 构建结果
        result = {
            "ai_server_camera_count": camera_count,
            "ai_server_pull_client_count": pull_clients_count,
            "total_alive_time": total_alive_time,
            "alive_cameras_info": alive_cameras_info,
            "active_camera_count": active_camera_count
        }

        return jsonify({"code": 200, "msg": "success", "data": result})
    except Exception as e:
        return jsonify({"msg": "Internal server error", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
