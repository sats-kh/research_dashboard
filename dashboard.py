import os
from datetime import datetime
import dash
from dash import dcc, html
import plotly.graph_objs as go
from utils import get_status_color, calculate_progress
from database import get_projects, get_milestones, DB_NAME
from graphs import create_progress_graph, create_budget_graph, create_research_graphs, create_milestone_graph

def init_dashboard(flask_app):
    external_stylesheets = [
        '/static/font/pretendard.css',
        '/static/font/pretendard-subset.css'
    ]

    dash_app = dash.Dash(
        __name__,
        server=flask_app,
        routes_pathname_prefix='/dashboard/',
        external_stylesheets=external_stylesheets
    )
    
    dash_app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
            <style>
                body {
                    background-color: #1E1E2E;
                }
            </style>
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''

    def serve_layout():
        # DB에서 최신 데이터를 불러오고 진행률 계산
        projects = get_projects()
        for project in projects:
            project["progress"] = calculate_progress(project["start_date"], project["end_date"])
        
        # 주요 통계 값 계산
        total_projects = len(projects)
        avg_progress = sum(p["progress"] for p in projects) / total_projects if total_projects > 0 else 0
        total_budget = sum(p["total_cost"] for p in projects)
        
        # 그래프 생성 (최신 데이터를 기반으로)
        progress_graph = create_progress_graph(projects)
        budget_graph = create_budget_graph(projects)
        research_graphs = create_research_graphs(projects)
        # DB에서 마일스톤 데이터 불러오기 및 그래프 생성
        milestones_data = get_milestones()
        milestone_graph = create_milestone_graph(milestones_data)
        
        # 데이터베이스 파일의 최종 수정 시간 가져오기
        db_last_update = datetime.fromtimestamp(os.path.getmtime(DB_NAME)).strftime("%Y-%m-%d")
        
        return html.Div(
            style={
                "backgroundColor": "#1E1E2E",
                "color": "white",
                "padding": "20px",
                "position": "relative",
                "fontFamily": "'Pretendard', sans-serif"
            },
            children=[
                # 우측 상단에 DB 최종 수정 날짜 표시
                html.Div(
                    f"마지막 업데이트: {db_last_update}",
                    style={
                        "position": "absolute",
                        "top": "10px",
                        "right": "20px",
                        "fontSize": "12px",
                        "color": "white",
                        "fontFamily": "'Pretendard', sans-serif"
                    }
                ),
                html.H1(
                    "재난안전융합연구센터 연구과제 대시보드",
                    style={
                        "textAlign": "center",
                        "fontSize": "60px",
                        "marginTop": "40px",
                        "fontFamily": "'Pretendard', sans-serif"
                    }
                ),
                # 주요 통계 카드 (grid 레이아웃)
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "repeat(4, 1fr)",
                        "gap": "15px",
                        "marginBottom": "20px",
                        "fontFamily": "'Pretendard', sans-serif"
                    },
                    children=[
                        html.Div(
                            style={
                                "backgroundColor": "#2E2E3E",
                                "borderRadius": "30px",
                                # "boxShadow": "2px 2px 8px rgba(0,0,0,0.5)",
                                "textAlign": "center",
                                "fontFamily": "'Pretendard', sans-serif"
                            },
                            children=[
                                html.P("총 연구과제", style={"fontFamily": "'Pretendard', sans-serif", "fontSize": "36px", "marginBottom": "0px", "color":"#ACACAC"}),
                                html.H2(f"{total_projects} 개", style={"fontFamily": "'Pretendard', sans-serif", "fontSize": "120px","marginTop": "4px", "marginBottom": "30px"})
                            ]
                        ),
                        html.Div(
                            style={
                                "backgroundColor": "#2E2E3E",
                                "borderRadius": "30px",
                                # "boxShadow": "2px 2px 8px rgba(0,0,0,0.5)",
                                "textAlign": "center",
                                "fontFamily": "'Pretendard', sans-serif"
                            },
                            children=[
                                html.P("평균 진행률", style={"fontFamily": "'Pretendard', sans-serif", "fontSize": "36px", "marginBottom": "0px", "color":"#ACACAC"}),
                                html.H2(f"{avg_progress:.1f}%", style={"fontFamily": "'Pretendard', sans-serif", "fontSize": "120px","marginTop": "4px", "marginBottom": "30px"})
                            ]
                        ),
                        html.Div(
                            style={
                                "backgroundColor": "#2E2E3E",
                                "borderRadius": "30px",
                                # "boxShadow": "2px 2px 8px rgba(0,0,0,0.5)",
                                "textAlign": "center",
                                "fontFamily": "'Pretendard', sans-serif"
                            },
                            children=[
                                html.P("총 예산", style={"fontFamily": "'Pretendard', sans-serif",  "fontSize": "36px", "marginBottom": "0px", "color":"#ACACAC"}),
                                html.H2(
                                        children=[
                                            html.Span(f"{total_budget}", style={"fontSize": "120px"}),
                                            html.Span(" 백만원", style={"fontSize": "48px",})
                                        ],
                                        style={
                                            "fontFamily": "'Pretendard', sans-serif",
                                            "marginTop": "4px",
                                            "marginBottom": "20px"
                                        }
                                    )
                                # html.H2(f"{total_budget} 백만원", style={"fontFamily": "'Pretendard', sans-serif", "fontSize": "120px","marginTop": "4px", "marginBottom": "30px"})
                            ]
                        ),
                        html.Div(
                            style={
                                "backgroundColor": "#2E2E3E",
                                "borderRadius": "30px",
                                # "boxShadow": "2px 2px 8px rgba(0,0,0,0.5)",
                                "textAlign": "center",
                                "fontFamily": "'Pretendard', sans-serif"
                            },
                            children=[
                                html.P("전체 참여 인원", style={"fontFamily": "'Pretendard', sans-serif",  "fontSize": "36px", "marginBottom": "0px", "color":"#ACACAC"}),
                                html.H2("15", style={"fontFamily": "'Pretendard', sans-serif", "fontSize": "120px","marginTop": "4px", "marginBottom": "30px"})
                            ]
                        )
                    ]
                ),
                # 연구과제 그래프 및 정량 성과지표
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "repeat(2, 1fr)",
                        "gap": "20px",
                        "fontFamily": "'Pretendard', sans-serif"
                    },
                    children=[
                        # 첫 번째 셀: "연구과제 진행률" 라벨과 progress_graph를 포함하는 카드
                        html.Div(
                            children=[
                                html.P(
                                    "연구과제 진행률",
                                    style={
                                        "textAlign": "left",
                                        "fontFamily": "'Pretendard', sans-serif",
                                        "fontSize": "40px",
                                        "color": "white",
                                        "marginBottom": "10px",
                                        "marginTop": "0px",
                                        "fontWeight": "bold",      # 볼드체 적용
                                        "paddingLeft": "25px"                                         
                                    }
                                ),
                                html.Div(
                                    children=dcc.Graph(figure=progress_graph, style={"width": "100%"}),
                                    style={
                                        "backgroundColor": "#2E2E3E",
                                        "padding": "15px",
                                        "borderRadius": "30px",
                                        # "boxShadow": "2px 2px 8px rgba(0,0,0,0.5)",
                                        "textAlign": "center",
                                        "fontFamily": "'Pretendard', sans-serif",
                                    }
                                )
                            ]
                        ),
                        # 두 번째 셀: "정량 성과지표" 라벨과 research_graphs를 포함하는 카드
                        html.Div(
                            children=[
                                html.P(
                                    "정량 성과지표",
                                    style={
                                        "textAlign": "left",
                                        "fontFamily": "'Pretendard', sans-serif",
                                        "fontSize": "40px",
                                        "color": "white",
                                        "marginBottom": "10px",
                                        "marginTop": "0px",
                                        "fontWeight": "bold",      # 볼드체 적용
                                        "paddingLeft": "25px"                                                                      
                                    }
                                ),
                                html.Div(
                                    children=html.Div(children=research_graphs, style={"width": "100%"}),
                                    style={
                                        "backgroundColor": "#2E2E3E",
                                        "padding": "15px",
                                        "borderRadius": "30px",                                        
                                        # "boxShadow": "2px 2px 8px rgba(0,0,0,0.5)",
                                        "textAlign": "center",
                                        "fontFamily": "'Pretendard', sans-serif",
                                    }
                                )
                            ]
                        )
                    ]
                ),
                # 마일스톤 그래프 영역 (단일 컬럼, 상단 여백 추가)
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr",
                        "marginTop": "25px",
                        "fontFamily": "'Pretendard', sans-serif",
                        "overflowX": "hidden"  # 부모 Div에 overflow 설정 추가
                    },
                    children=[
                        html.P(
                            "연구과제 마일스톤 진행률",
                            style={
                                "textAlign": "left",
                                "fontFamily": "'Pretendard', sans-serif",
                                "fontSize": "40px",
                                "color": "white",
                                "marginBottom": "10px",
                                "marginTop": "0px",
                                "fontWeight": "bold",      # 볼드체 적용
                                "paddingLeft": "25px"                                         
                            }
                        ),
                        html.Div(
                            children=create_milestone_graph(milestones_data),  # milestone_graph을 dcc.Graph로 반환한 함수 호출
                            style={
                                "backgroundColor": "#2E2E3E",
                                "padding": "15px",
                                "borderRadius": "30px",
                                # "boxShadow": "2px 2px 8px rgba(0,0,0,0.5)",
                                "textAlign": "center",
                                "fontFamily": "'Pretendard', sans-serif",
                                "width": "100%",
                                "height": "1080px",
                                "overflowX": "hidden"  # 여기에도 overflow 설정 추가
                            }
                        )
                    ]
                )
            ]
        )
    
    dash_app.layout = serve_layout
    return dash_app