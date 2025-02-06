# app.py
from flask import Flask
from routes import update_blueprint, milestone_blueprint  # Flask 라우트 모듈
from dashboard import init_dashboard   # Dash 대시보드 초기화 함수

app = Flask(__name__)

# Flask 라우트 등록
app.register_blueprint(update_blueprint)
app.register_blueprint(milestone_blueprint)

# Dash 대시보드 초기화 (Flask 서버와 통합)
init_dashboard(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)