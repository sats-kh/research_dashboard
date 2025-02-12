import math
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.express as px
from dash import dcc, html

from utils import get_status_color, calculate_progress
from database import get_projects, get_milestones, DB_NAME

# 미리 지정한 색상 리스트 (15개 이상)
my_colors = [
    "#2DB9FF", "#686DFA", "#FFC300",
    "#FF00C3", "#FF0000", "#AE00FF",
    "#ECFF81", "#FFB5B5", "#2FFFAC",
    "#65FFF0", "#D4FF00", "#E7FF5D",
    "#FF8000", "#0048FF", "#00FF2F",
]

def get_color_mapping_from_projects(projects):
    """
    projects: 연구과제 목록 (각 항목은 dict, "name" 키 포함)
    각 프로젝트 이름에서 앞뒤 공백만 제거한 원본 문자열을 기준으로,
    고유한 이름을 정렬하여 my_colors 리스트 순서대로 색상을 할당하는 사전을 반환.
    """
    cleaned_names = [p["name"].strip() for p in projects]
    unique_names = sorted(set(cleaned_names))
    mapping = {name: my_colors[i % len(my_colors)] for i, name in enumerate(unique_names)}
    return mapping

# 전역 변수: COLOR_MAPPING (애플리케이션 초기 실행 시 업데이트)
COLOR_MAPPING = {}

def create_progress_graph(projects):
    global COLOR_MAPPING
    # 프로젝트 목록을 순회하면서, COLOR_MAPPING에 누락된 이름이 있으면 추가
    for p in projects:
        key = p["name"].strip()
        if key not in COLOR_MAPPING:
            # 기존 매핑 개수를 기준으로 새로운 색상 할당 (색상 리스트를 순환)
            COLOR_MAPPING[key] = my_colors[len(COLOR_MAPPING) % len(my_colors)]
    # print("Progress COLOR_MAPPING:", COLOR_MAPPING)
    
    # 프로젝트 이름은 앞뒤 공백만 제거하여 사용
    project_names = [p["name"].strip() for p in projects]
    colors = [COLOR_MAPPING[p["name"].strip()] for p in projects]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=project_names,
        y=[p["progress"] for p in projects],
        marker=dict(color=colors, opacity=0.8),
        text=[f"{p['progress']}%" for p in projects],
        textposition="outside",
        textfont=dict(family="Pretendard", size=30, color="white"),
        cliponaxis=False
    ))
        
    fig.update_layout(
        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(family="Pretendard", size=20, color="white")
        ),
        template="plotly_dark",
        height=400,
        margin=dict(l=40, r=20, t=40, b=40),
        paper_bgcolor="#2E2E3E",
        plot_bgcolor="#2E2E3E"
    )
    
    fig.update_xaxes(
        side="bottom",
        linecolor="white",
        linewidth=2,
        tickfont=dict(family="Pretendard", size=36, color="white")
    )
    fig.update_yaxes(
        tickfont=dict(family="Pretendard", size=20, color="white")
    )
    
    return fig  # Figure 객체 반환

def create_research_graphs(projects):
    research_graphs = []
    # 연구성과 지표용 색상은 카테고리별로 고정
    category_colors = {
        "논문": "#ECECEC",
        "특허": "#8A8A8A",
        "SW": "#5E5E5E"
    }
    
    for project in projects:
        project_name = project["name"].strip()
        final_results = {
            "논문": project.get("goal_papers", 0),
            "특허": project.get("goal_patents_filed", 0) + project.get("goal_patents_registered", 0),
            "SW": project.get("goal_software", 0)
        }
        current_results = {
            "논문": project.get("current_papers", 0),
            "특허": project.get("current_patents_filed", 0) + project.get("current_patents_registered", 0),
            "SW": project.get("current_software", 0)
        }
        categories = list(final_results.keys())
        current_values = [min(current_results[cat], final_results[cat]) for cat in categories]
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
                marker=dict(color="#3C3C49")
            )
        ])
        
        fig.update_layout(
            template="plotly_dark",
            barmode="stack",
            height=400,
            margin=dict(l=40, r=20, t=40, b=70),
            showlegend=False,
            paper_bgcolor="#2E2E3E",
            plot_bgcolor="#2E2E3E"
        )
        
        fig.update_xaxes(
            showticklabels=False,
            linecolor="white",
            linewidth=2,
            side="bottom"
        )
        
        fig.update_yaxes(
            tickmode="linear",
            dtick=1,
            showgrid=True,
            gridcolor="#545464",
            gridwidth=1,
            tickson="boundaries",
            tickfont=dict(family="Pretendard", size=20, color="white")
        )
        
        fig.update_layout(
            annotations=[
                dict(
                    text=project_name,
                    x=0.5,
                    y=-0.20,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(family="Pretendard", size=36, color="white")
                )
            ]
        )
        
        research_graphs.append(fig)
    
    graph_components = [
        html.Div(
            children=dcc.Graph(figure=f, style={"width": "100%"}),
            style={
                "width": "100%",
                "borderRadius": "30px",
                "overflow": "hidden",
                "height": "auto"
            }
        )
        for f in research_graphs
    ]
    
    return html.Div(
        children=graph_components,
        style={
            "display": "flex",
            "flexDirection": "row",
            "gap": "30px",
            "overflowX": "auto"
        }
    )

def create_milestone_graph(milestones_data):
    """
    milestones_data: DB에서 불러온 마일스톤 데이터 리스트 
      (각 항목은 딕셔너리이며, 키는 "Milestone", "Start", "Finish", "Status", "세부 목표", "담당자" 등을 포함)
    """
    df = pd.DataFrame(milestones_data)
    
    if df.empty:
        now = datetime.now()
        data = [
            {
                "Milestone": "AI", 
                "담당자": "김연구", 
                "Start": (now + timedelta(days=1)).strftime("%Y-%m-%d"), 
                "Finish": (now + timedelta(days=31)).strftime("%Y-%m-%d"), 
                "Status": "달성", 
                "세부 목표": "논문 작성"
            },
            {
                "Milestone": "블록체인", 
                "담당자": "박연구", 
                "Start": (now + timedelta(days=2)).strftime("%Y-%m-%d"), 
                "Finish": (now + timedelta(days=11)).strftime("%Y-%m-%d"), 
                "Status": "달성", 
                "세부 목표": "특허 출원"
            },
            {
                "Milestone": "산불", 
                "담당자": "이연구", 
                "Start": (now + timedelta(days=3)).strftime("%Y-%m-%d"), 
                "Finish": (now + timedelta(days=33)).strftime("%Y-%m-%d"), 
                "Status": "달성", 
                "세부 목표": "특허 등록"
            },
            {
                "Milestone": "홍수", 
                "담당자": "이관훈", 
                "Start": (now + timedelta(days=4)).strftime("%Y-%m-%d"), 
                "Finish": (now + timedelta(days=14)).strftime("%Y-%m-%d"), 
                "Status": "달성", 
                "세부 목표": "특허 등록"
            },
            {
                "Milestone": "산사태", 
                "담당자": "홍길동", 
                "Start": (now + timedelta(days=5)).strftime("%Y-%m-%d"), 
                "Finish": (now + timedelta(days=12)).strftime("%Y-%m-%d"), 
                "Status": "달성", 
                "세부 목표": "특허 등록"
            },
            {
                "Milestone": "밀집", 
                "담당자": "김연구", 
                "Start": (now + timedelta(days=6)).strftime("%Y-%m-%d"), 
                "Finish": (now + timedelta(days=16)).strftime("%Y-%m-%d"), 
                "Status": "달성", 
                "세부 목표": "논문 작성"
            },
            {
                "Milestone": "블랙아이스", 
                "담당자": "박연구", 
                "Start": (now + timedelta(days=7)).strftime("%Y-%m-%d"), 
                "Finish": (now + timedelta(days=16)).strftime("%Y-%m-%d"), 
                "Status": "달성", 
                "세부 목표": "특허 출원"
            },
            {
                "Milestone": "위성", 
                "담당자": "이연구", 
                "Start": (now + timedelta(days=8)).strftime("%Y-%m-%d"), 
                "Finish": (now + timedelta(days=13)).strftime("%Y-%m-%d"), 
                "Status": "달성", 
                "세부 목표": "특허 등록"
            },
            {
                "Milestone": "로봇", 
                "담당자": "이관훈", 
                "Start": (now + timedelta(days=2)).strftime("%Y-%m-%d"), 
                "Finish": (now + timedelta(days=9)).strftime("%Y-%m-%d"), 
                "Status": "달성", 
                "세부 목표": "특허 등록"
            },
            {
                "Milestone": "분산", 
                "담당자": "홍길동", 
                "Start": (now + timedelta(days=10)).strftime("%Y-%m-%d"), 
                "Finish": (now + timedelta(days=13)).strftime("%Y-%m-%d"), 
                "Status": "달성", 
                "세부 목표": "특허 등록"
            },
        ]
        df = pd.DataFrame(data)
    
    if "담당자" not in df.columns:
        df["담당자"] = ""
    
    # label: 세부 목표만 사용 (추가 공백 포함)
    df["label"] = df["세부 목표"].astype(str) + "    "
    
    # Milestone 값은 strip()만 적용 (원본 그대로 사용)
    df["Milestone"] = df["Milestone"].str.strip()
    unique_milestones = sorted(set(df["Milestone"]))
    
    global COLOR_MAPPING
    # 전역 COLOR_MAPPING에 누락된 Milestone 이름이 있으면 추가
    for name in unique_milestones:
        if name not in COLOR_MAPPING:
            COLOR_MAPPING[name] = my_colors[len(COLOR_MAPPING) % len(my_colors)]
    # print("COLOR_MAPPING:", COLOR_MAPPING)
    
    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Milestone",
        color="Milestone",
        text="label",
        color_discrete_map=COLOR_MAPPING
    )
    
    fig.update_yaxes(autorange="reversed")
    
    for trace in fig.data:
        trace.update(
            textposition='inside',
            textfont=dict(family="Pretendard", size=36, color="white"),
            width=0.95,
        )
    
    now = datetime.now()
    two_weeks_later = now + timedelta(days=21)
    fig.update_layout(xaxis_range=[now, two_weeks_later])
    
    fig.update_layout(
        title=dict(
            x=0.5,
            font=dict(family="Pretendard", size=20, color="white")
        ),
        template="plotly_dark",
        paper_bgcolor="#2E2E3E",
        plot_bgcolor="#2E2E3E",
        margin=dict(l=40, r=20, t=40, b=40),
        showlegend=False
    )
    
    fig.update_yaxes(
        tickmode="linear",
        dtick=1,
        showgrid=True,
        gridcolor="#545464",
        gridwidth=1,
        tickson="boundaries"
    )
    fig.update_yaxes(title_text="")
    
    fig.update_xaxes(
        tickfont=dict(family="Pretendard", size=20, color="white"),
        title_text="",
        side="bottom",
        linecolor="white",
        linewidth=2
    )
    fig.update_yaxes(tickfont=dict(family="Pretendard", size=36, color="white"))
    
    return dcc.Graph(
        figure=fig,
        style={
            "width": "100%",
            "maxWidth": "100%",
            "height": "100%",
            "overflowX": "hidden"
        }
    )

def create_budget_graph(projects):
    fig = go.Figure()

    # 각 프로젝트의 제목에 따른 색상 할당 (COLOR_MAPPING에 없는 경우 기본값 "#FFD700")
    # (COLOR_MAPPING은 미리 정의되어 있다고 가정)
    for p in projects:
        bar_color = COLOR_MAPPING.get(p["name"].strip(), "#FFD700")
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=p["current_expenditure"],
            # 기존 title 속성을 제거하여, 제목은 annotation으로 처리합니다.
            gauge={
                "axis": {
                    "range": [0, p["total_cost"]],
                    "tickfont": {"family": "Pretendard", "size": 18, "color": "white"},
                    "showticklabels": True
                },
                "bar": {"color": bar_color},
                "bordercolor": "#ECECEC",
                "steps": [
                    {"range": [0, p["total_cost"] * 0.5], "color": "#3C3C49"},
                    {"range": [p["total_cost"] * 0.5, p["total_cost"]], "color": "#8A8A8A"}
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": p["total_cost"] * 0.9
                }
            },
            domain={"row": 0, "column": projects.index(p)}
        ))
    
    # grid 설정: 1행, n열
    fig.update_layout(
        template="plotly_dark",
        grid={"rows": 1, "columns": len(projects)},
        height=350,
        margin=dict(l=40, r=20, t=50, b=80),  # 하단 여백을 늘려서 annotation 공간 확보
        paper_bgcolor="#2E2E3E",
        plot_bgcolor="#2E2E3E"
    )
    
    # 각 게이지 아래에 연구과제 제목(annotation) 추가
    num_projects = len(projects)
    for i, p in enumerate(projects):
        # grid의 각 셀는 전체 width에서 (i/n ~ (i+1)/n)에 해당하므로 중앙은 (i+0.5)/n
        fig.add_annotation(
            x=(i + 0.48) / num_projects,
            y=-0.05,  # y축 paper 좌표: 0보다 낮게 설정하여 게이지 아래에 위치
            xref="paper",
            yref="paper",
            text=f"<b>{p['name']}</b>",
            showarrow=False,
            font={"family": "Pretendard", "size": 20, "color": "white"},
            xanchor="center",
            yanchor="top"
        )
    
    return fig