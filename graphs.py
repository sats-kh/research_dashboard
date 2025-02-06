# graphs.py
import math
import plotly.graph_objs as go
from dash import dcc, html

def create_progress_graph(projects):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[p["name"] for p in projects],
        y=[p["progress"] for p in projects],
        marker=dict(color=["#6A5ACD", "#FF4500", "#32CD32"], opacity=0.8),
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