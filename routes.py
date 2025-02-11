# routes.py
import datetime
from flask import Blueprint, render_template, request, redirect
from database import get_projects, update_project, delete_project, add_project, get_milestones, update_milestone, delete_milestone, add_milestone
from utils import calculate_progress

update_blueprint = Blueprint('update', __name__)
milestone_blueprint = Blueprint('milestone', __name__)


@update_blueprint.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        action = request.form.get("action")
        if action:
            project_id = request.form.get("id")
            name = request.form.get("name", "")
            manager = request.form.get("manager", "")
            start_date = request.form.get("start_date", "")
            end_date = request.form.get("end_date", "")
            total_cost = float(request.form.get("total_cost", "0") or 0)
            current_expenditure = float(request.form.get("current_expenditure", "0") or 0)
            goal_papers = int(request.form.get("goal_papers", "0") or 0)
            current_papers = int(request.form.get("current_papers", "0") or 0)
            goal_patents_filed = int(request.form.get("goal_patents_filed", "0") or 0)
            current_patents_filed = int(request.form.get("current_patents_filed", "0") or 0)
            goal_patents_registered = int(request.form.get("goal_patents_registered", "0") or 0)
            current_patents_registered = int(request.form.get("current_patents_registered", "0") or 0)
            goal_software = int(request.form.get("goal_software", "0") or 0)
            current_software = int(request.form.get("current_software", "0") or 0)


            if action == "update" and project_id:
                update_project(project_id, name, manager, start_date, end_date,
                               total_cost, current_expenditure,
                               goal_papers, current_papers,
                               goal_patents_filed, current_patents_filed,
                               goal_patents_registered, current_patents_registered,
                               goal_software, current_software)
            elif action == "delete" and project_id:
                delete_project(project_id)
            elif action == "add":
                add_project(name, manager, start_date, end_date,
                            total_cost, current_expenditure,
                            goal_papers, current_papers,
                            goal_patents_filed, current_patents_filed,
                            goal_patents_registered, current_patents_registered,
                            goal_software, current_software)
        return redirect('/update')

    projects = get_projects()
    # 진행률 업데이트
    for project in projects:
        project["progress"] = calculate_progress(project["start_date"], project["end_date"])
    return render_template('update.html', projects=projects)
    
@milestone_blueprint.route('/milestone', methods=['GET', 'POST'])
def milestone():
    if request.method == 'POST':
        action = request.form.get("action")
        if action:
            milestone_id = request.form.get("id")
            # 마일스톤 제목은 드롭다운으로 선택하므로, 선택된 연구과제명을 받아옴.
            milestone_text = request.form.get("Milestone", "")
            start = request.form.get("Start", "")
            finish = request.form.get("Finish", "")
            status = request.form.get("Status", "")
            detail = request.form.get("세부 목표", "")
            # 새로 추가된 담당자 필드
            manager = request.form.get("담당자", "")
            
            if action == "update" and milestone_id:
                update_milestone(milestone_id, milestone_text, start, finish, status, detail, manager)
            elif action == "delete" and milestone_id:
                delete_milestone(milestone_id)
            elif action == "add":
                add_milestone(milestone_text, start, finish, status, detail, manager)
        return redirect('/milestone')
    
    milestones = get_milestones()
    projects = get_projects()  # 연구과제 목록을 함께 가져와서 드롭다운 옵션으로 사용
    return render_template('milestone.html', milestones=milestones, projects=projects)