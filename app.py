# app.py
from flask import Flask
from routes import update_blueprint, milestone_blueprint  # Flask 라우트 모듈
from dashboard import init_dashboard   # Dash 대시보드 초기화 함수
from expense import expense_dashboard

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, public, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Flask 라우트 등록
app.register_blueprint(update_blueprint)
app.register_blueprint(milestone_blueprint)

# Dash 대시보드 초기화 (Flask 서버와 통합)
init_dashboard(app)
expense_dashboard(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
