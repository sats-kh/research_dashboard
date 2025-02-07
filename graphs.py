# graphs.py
import math
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta
from dash import dcc, html
import pandas as pd
def create_progress_graph(projects):
    import plotly.express as px  # 이미 import 되어 있다면 생략 가능
    # Plotly 기본 색상 팔레트 사용
    color_palette = px.colors.qualitative.Plotly
    
    # 각 프로젝트 이름을 기준으로 색상을 할당 (일관된 색상 매핑)
    project_names = [p["name"] for p in projects]
    colors = [color_palette[hash(name) % len(color_palette)] for name in project_names]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=project_names,
        y=[p["progress"] for p in projects],
        marker=dict(color=colors, opacity=0.8),
        text=[f"{p['progress']}%" for p in projects],
        textposition="outside"
    ))
    fig.update_layout(
        title=dict(
            text="연구과제 진행률(기간)",
            x=0.5,
            xanchor="center",
            font=dict(family="Arial Bold", size=20, color="white")
        ),
        template="plotly_dark",
        height=300,
        margin=dict(l=40, r=20, t=40, b=40),
        paper_bgcolor="#2E2E3E",
        plot_bgcolor="#2E2E3E"
    )
    return fig  # Figure 객체 반환
    
def create_budget_graph(projects):
    fig = go.Figure()
    for idx, p in enumerate(projects):
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=p["current_expenditure"],
            title={"text": f"{p['name']}"},
            gauge={
                "axis": {
                    "range": [0, p["total_cost"]],
                    "ticks": "",       # 틱 마크 제거
                    "ticklen": 0       # 틱 길이 0으로 설정
                },
                "bar": {"color": "#FFD700"}
            },
            domain={"row": 0, "column": idx}
        ))
    fig.update_layout(
        title=dict(
            text="과제비 집행률(단위: 백만원)",
            x=0.5,
            xanchor="center",
            font=dict(family="Arial Bold", size=20, color="white")
        ),
        template="plotly_dark",
        grid={"rows": 1, "columns": len(projects)},
        height=300,
        margin=dict(l=40, r=20, t=40, b=40),
        paper_bgcolor="#2E2E3E",
        plot_bgcolor="#2E2E3E"
    )
    return fig  # Figure 객체 반환

def create_research_graphs(projects):
    research_graphs = []
    category_colors = {
        "논문": "#FF6347",
        "특허": "#4682B4",
        "SW": "#FFD700"
    }
    
    for project in projects:
        project_name = project["name"]
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
                marker=dict(color="#CCCCCC")
            )
        ])
        fig.update_layout(
            title=dict(
                text=f"{project_name}",
                x=0.5,
                xanchor="center",
                font=dict(family="Arial Bold", size=20, color="white")
            ),
            template="plotly_dark",
            barmode="stack",
            height=300,
            margin=dict(l=40, r=20, t=40, b=40),
            showlegend=False,
            paper_bgcolor="#2E2E3E",
            plot_bgcolor="#2E2E3E"
        )
        research_graphs.append(fig)
    
    # 각 Figure 객체들을 dcc.Graph로 감싸고 좌우 배치
    graph_components = [
        dcc.Graph(
            figure=f,
            style={
                "height": "300px",
                "flex": "1",
                "width": "100%",
                "borderRadius": "8px",
                "boxShadow": "2px 2px 8px rgba(0,0,0,0.5)"
            }
        )
        for f in research_graphs
    ]
    
    return html.Div(
        children=graph_components,
        style={
            "display": "flex",
            "flexDirection": "row",
            "gap": "20px",
            "overflowX": "auto"
        }
    )

def create_milestone_graph(milestones_data):
    """
    milestones_data: DB에서 불러온 마일스톤 데이터 리스트 
      (각 항목은 딕셔너리이며, 키는 "Milestone", "Start", "Finish", "Status", "세부 목표", "담당자" 등을 포함)
    """
    # DB 데이터를 DataFrame으로 변환
    df = pd.DataFrame(milestones_data)
    
    # 만약 DB에 데이터가 없으면, 샘플 데이터를 사용 (샘플 데이터에 담당자도 포함)
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
                "Finish": (now + timedelta(days=8)).strftime("%Y-%m-%d"), 
                "Status": "달성", 
                "세부 목표": "특허 등록"
            },
            {
                "Milestone": "밀집", 
                "담당자": "김연구", 
                "Start": (now + timedelta(days=6)).strftime("%Y-%m-%d"), 
                "Finish": (now + timedelta(days=36)).strftime("%Y-%m-%d"), 
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
                "Finish": (now + timedelta(days=38)).strftime("%Y-%m-%d"), 
                "Status": "달성", 
                "세부 목표": "특허 등록"
            },
            {
                "Milestone": "로봇", 
                "담당자": "이관훈", 
                "Start": (now + timedelta(days=9)).strftime("%Y-%m-%d"), 
                "Finish": (now + timedelta(days=19)).strftime("%Y-%m-%d"), 
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
    
    # 만약 DB 데이터에 "담당자" 컬럼이 없는 경우, 빈 문자열로 채움 (예방 코드)
    if "담당자" not in df.columns:
        df["담당자"] = ""
    
    # "세부 목표"와 "담당자"를 결합한 텍스트 라벨 생성 (예: "논문 작성 (김연구)")
    df["label"] = df["세부 목표"].astype(str) + " (" + df["담당자"].astype(str) + ")"
    
    # 각 마일스톤을 기준으로 색상을 자동 지정 (y축: Milestone)
    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Milestone",
        color="Milestone",
        text="label",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    
    fig.update_yaxes(autorange="reversed")
    
    # 개별 trace에 대해 textfont 속성 업데이트 (모든 trace에 대해 적용)
    for trace in fig.data:
        trace.update(textposition='inside', textfont=dict(color='white', size=80))
    
    now = datetime.now()
    two_weeks_later = now + timedelta(days=7)
    fig.update_layout(xaxis_range=[now, two_weeks_later])
    
    fig.update_layout(
        title=dict(
            text="프로젝트별 마일스톤 진행률",
            x=0.5,
            font=dict(family="Arial Bold", size=20, color="white")
        ),
        template="plotly_dark",
        paper_bgcolor="#2E2E3E",
        plot_bgcolor="#2E2E3E",
        height=700,
        margin=dict(l=40, r=20, t=40, b=40),
        showlegend=False
    )
    
    return dcc.Graph(figure=fig)