import re
import datetime
from flask import Flask, render_template, request, redirect
import dash
from dash import dcc, html
import plotly.graph_objs as go
from database import get_projects, update_project, delete_project, add_project

app = Flask(__name__)

# 연구과제 DB 정보 수정 웹페이지
@app.route('/revise', methods=['GET', 'POST'])
def revise():
    if request.method == 'POST':
        action = request.form.get("action")

        if action:
            project_id = request.form.get("id")
            name = request.form.get("name", "")
            manager = request.form.get("manager", "")
            start_date = request.form.get("start_date", "")
            end_date = request.form.get("end_date", "")
            total_cost = request.form.get("total_cost", "0")
            current_expenditure = request.form.get("current_expenditure", "0")
            final_goal = request.form.get("final_goal", "")
            current_deliverables = request.form.get("current_deliverables", "")

            # 연구과제 수정
            if action == "update" and project_id:
                update_project(project_id, name, manager, start_date, end_date, int(total_cost), int(current_expenditure), final_goal, current_deliverables)

            # 연구과제 삭제
            elif action == "delete" and project_id:
                delete_project(project_id)

            # 연구과제 추가
            elif action == "add":
                add_project(name, manager, start_date, end_date, int(total_cost), int(current_expenditure), final_goal, current_deliverables)

        return redirect('/revise')

    projects = get_projects()
    return render_template('revise.html', projects=projects)

# 현재 날짜 가져오기
today = datetime.date.today()

# 진행률 자동 계산 함수
def calculate_progress(start_date, end_date):
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    total_days = (end - start).days
    elapsed_days = (today - start).days

    if elapsed_days <= 0:
        return 0  # 시작 전
    if elapsed_days >= total_days:
        return 100  # 완료됨

    return round((elapsed_days / total_days) * 100, 1)  # 소수점 1자리 반올림

# 연구과제 데이터 불러오기 (SQLite)
projects = get_projects()

# 진행률 업데이트
for project in projects:
    project["progress"] = calculate_progress(project["start_date"], project["end_date"])

# 주요 통계 카드
total_projects = len(projects)
avg_progress = sum(p["progress"] for p in projects) / total_projects
total_budget = sum(p["total_cost"] for p in projects)

# ✅ 연구 성과 비교 그래프 (각 연구과제별 스택형 바 차트 생성)
# 각 연구과제마다, "논문", "특허출원", "특허등록", "SW"에 대해 목표 대비 현재 달성치와 남은 목표를 표시합니다.
stacked_graphs = []
# 각 카테고리별 색상 (현재 달성치)
category_colors = {
    "논문": "#FF6347",
    "특허출원": "#4682B4",
    "특허등록": "#6A5ACD",
    "SW": "#FFD700"
}

for project in projects:
    project_name = project["name"]

    # 각 연구과제에 대해 목표와 현재 성과를 딕셔너리로 정리 (키 존재하지 않을 경우 0으로 처리)
    final_results = {
        "논문": project.get("goal_papers", 0),
        "특허출원": project.get("goal_patents_filed", 0),
        "특허등록": project.get("goal_patents_registered", 0),
        "SW": project.get("goal_software", 0)
    }

    current_results = {
        "논문": project.get("current_papers", 0),
        "특허출원": project.get("current_patents_filed", 0),
        "특허등록": project.get("current_patents_registered", 0),
        "SW": project.get("current_software", 0)
    }

    categories = list(final_results.keys())

    # 현재 달성치는 목표치보다 클 수 없도록 min() 사용
    current_values = [min(current_results[cat], final_results[cat]) for cat in categories]
    # 남은 목표는 (목표 - 현재)이며 음수 방지를 위해 max(0, 목표-현재)
    remaining_values = [max(final_results[cat] - current_results[cat], 0) for cat in categories]

    fig = go.Figure(data=[
         go.Bar(
              name="현재 달성",
              x=categories,
              y=current_values,
              marker=dict(color=[category_colors[cat] for cat in categories])
         ),
         go.Bar(
              name="남은 목표",
              x=categories,
              y=remaining_values,
              marker=dict(color="#CCCCCC")
         )
    ])

    fig.update_layout(
         title=f"{project_name} - 연구 성과 비교",
         template="plotly_dark",
         barmode="stack",
         xaxis=dict(title="카테고리"),
         yaxis=dict(title="수량")
    )

    # 각 연구과제별 그래프를 dcc.Graph 객체로 생성 후 리스트에 추가
    stacked_graphs.append(dcc.Graph(figure=fig))

# 연구과제 진행률 그래프
progress_data = go.Figure()
progress_data.add_trace(go.Bar(
    x=[p["name"] for p in projects],
    y=[p["progress"] for p in projects],
    marker=dict(color=["#6A5ACD", "#FF4500", "#32CD32"], opacity=0.8),
    text=[f"{p['progress']}%" for p in projects],
    textposition="outside"
))
progress_data.update_layout(title="연구과제 진행률 (자동 계산)", template="plotly_dark")

# 예산 사용 현황 (게이지 차트)
budget_data = go.Figure()
for p in projects:
    budget_data.add_trace(go.Indicator(
        mode="gauge+number",
        value=p["current_expenditure"],
        title={"text": f"{p['name']} 예산 소진"},
        gauge={"axis": {"range": [0, p["total_cost"]]}, "bar": {"color": "#FFD700"}},
        domain={"row": 0, "column": projects.index(p)}
    ))
budget_data.update_layout(template="plotly_dark", grid={"rows": 1, "columns": len(projects)})

# Dash 앱 설정
dash_app = dash.Dash(
    __name__,
    server=app,
    routes_pathname_prefix='/dashboard/'
)

# 진행 상태 색상 반환 함수
def get_status_color(progress):
    if progress >= 80:
        return "#32CD32"  # Green (완료)
    elif progress >= 40:
        return "#FFA500"  # Orange (진행 중)
    else:
        return "#FF4500"  # Red (지연)

# 대시보드 레이아웃
dash_app.layout = html.Div(style={"backgroundColor": "#1E1E2E", "color": "white", "padding": "20px"}, children=[
    html.H1("연구과제 대시보드", style={"textAlign": "center"}),

    # ✅ 상단 주요 통계 카드
    html.Div(style={
        "display": "flex",
        "justifyContent": "space-around",
        "alignItems": "center",
        "marginBottom": "20px"
    }, children=[
        html.Div(style={"backgroundColor": "#2E2E3E", "padding": "20px", "borderRadius": "10px", "width": "30%", "textAlign": "center"}, children=[
            html.H3("총 연구과제"),
            html.H2(f"{total_projects} 개")
        ]),
        html.Div(style={"backgroundColor": "#2E2E3E", "padding": "20px", "borderRadius": "10px", "width": "30%", "textAlign": "center"}, children=[
            html.H3("평균 진행률"),
            html.H2(f"{avg_progress:.1f}%")
        ]),
        html.Div(style={"backgroundColor": "#2E2E3E", "padding": "20px", "borderRadius": "10px", "width": "30%", "textAlign": "center"}, children=[
            html.H3("총 예산"),
            html.H2(f"{total_budget} 백만원")
        ])
    ]),

    # ✅ 연구과제 개별 진행 상태 카드 추가
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "15px", "marginBottom": "20px"}, children=[
        html.Div(style={
            "backgroundColor": "#333",
            "padding": "15px",
            "borderRadius": "8px",
            "boxShadow": "2px 2px 8px rgba(0,0,0,0.5)",
            "textAlign": "center"
        }, children=[
            html.H3(project["name"]),
            html.P(f"담당자: {project['manager']}"),
            html.Div(style={
                "backgroundColor": get_status_color(project["progress"]),
                "color": "white",
                "padding": "5px",
                "borderRadius": "5px",
                "display": "inline-block"
            }, children=f"진행률: {project['progress']}%")
        ]) for project in projects
    ]),

    # ✅ 그래프 배치: 진행률, 예산, 그리고 연구 성과(연구과제별 스택형 바 차트)
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"}, children=[
        dcc.Graph(figure=progress_data),
        dcc.Graph(figure=budget_data),
        # stacked_graphs는 이미 dcc.Graph 객체들의 리스트이므로, html.Div의 children로 넣어줍니다.
        html.Div(children=stacked_graphs)
    ])
])

if __name__ == '__main__':
    app.run(debug=True)