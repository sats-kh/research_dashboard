# dashboard.py
import dash
from dash import dcc, html
import plotly.graph_objs as go
from utils import get_status_color, calculate_progress
from database import get_projects
from graphs import create_progress_graph, create_budget_graph, create_research_graphs

def init_dashboard(flask_app):
    dash_app = dash.Dash(
        __name__,
        server=flask_app,
        routes_pathname_prefix='/dashboard/'
    )
    
    # 연구과제 데이터 불러오기 및 진행률 업데이트
    projects = get_projects()
    for project in projects:
        project["progress"] = calculate_progress(project["start_date"], project["end_date"])
    
    # 통계 값 계산
    total_projects = len(projects)
    avg_progress = sum(p["progress"] for p in projects) / total_projects if total_projects > 0 else 0
    total_budget = sum(p["total_cost"] for p in projects)

    # 그래프 생성
    progress_graph = create_progress_graph(projects)
    budget_graph = create_budget_graph(projects)
    research_graphs = create_research_graphs(projects)

    # Dash 대시보드 레이아웃 구성
    dash_app.layout = html.Div(style={"backgroundColor": "#1E1E2E", "color": "white", "padding": "20px"}, children=[
        html.H1("재난안전융합연구센터 연구과제 대시보드", style={"textAlign": "center"}),
        
        # 주요 통계 카드 (grid 레이아웃)
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(4, 1fr)",  # 4개의 카드가 한 줄에 표시됨
                "gap": "15px",
                "marginBottom": "20px"
            },
            children=[
                html.Div(
                    style={
                        "backgroundColor": "#2E2E3E",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "boxShadow": "2px 2px 8px rgba(0,0,0,0.5)",
                        "textAlign": "center"
                    },
                    children=[
                        html.H3("총 연구과제"),
                        html.H2(f"{total_projects} 개")
                    ]
                ),
                html.Div(
                    style={
                        "backgroundColor": "#2E2E3E",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "boxShadow": "2px 2px 8px rgba(0,0,0,0.5)",
                        "textAlign": "center"
                    },
                    children=[
                        html.H3("평균 진행률"),
                        html.H2(f"{avg_progress:.1f}%")
                    ]
                ),
                html.Div(
                    style={
                        "backgroundColor": "#2E2E3E",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "boxShadow": "2px 2px 8px rgba(0,0,0,0.5)",
                        "textAlign": "center"
                    },
                    children=[
                        html.H3("총 예산"),
                        html.H2(f"{total_budget} 백만원")
                    ]
                ),
                html.Div(
                    style={
                        "backgroundColor": "#2E2E3E",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "boxShadow": "2px 2px 8px rgba(0,0,0,0.5)",
                        "textAlign": "center"
                    },
                    children=[
                        html.H3("참여 인원"),
                        html.H2("X 명")
                    ]
                )
            ]
        ),
        # 연구과제 개별 진행 상태 카드
        html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr", "gap": "15px", "marginBottom": "20px"}, children=[
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
        # 그래프 배치
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(3, 1fr)",  # 3개의 동일한 컬럼 생성
                "gap": "20px"
            },
            children=[
                dcc.Graph(figure=progress_graph),
                dcc.Graph(figure=budget_graph),
                html.Div(children=research_graphs)
            ]
        )
    ])