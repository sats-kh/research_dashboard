# app.py
from flask import Flask
from routes import revise_blueprint  # Flask 라우트 모듈
from dashboard import init_dashboard   # Dash 대시보드 초기화 함수

app = Flask(__name__)

# Flask 라우트 등록
app.register_blueprint(revise_blueprint)

# Dash 대시보드 초기화 (Flask 서버와 통합)
init_dashboard(app)

if __name__ == '__main__':
    app.run(debug=True)