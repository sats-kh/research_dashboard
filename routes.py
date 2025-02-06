# routes.py
import datetime
from flask import Blueprint, render_template, request, redirect
from database import get_projects, update_project, delete_project, add_project
from utils import calculate_progress

revise_blueprint = Blueprint('revise', __name__)

@revise_blueprint.route('/revise', methods=['GET', 'POST'])
def revise():
    if request.method == 'POST':
        action = request.form.get("action")
        if action:
            project_id = request.form.get("id")
            name = request.form.get("name", "")
            manager = request.form.get("manager", "")
            start_date = request.form.get("start_date", "")
            end_date = request.form.get("end_date", "")
            total_cost = int(request.form.get("total_cost", "0"))
            current_expenditure = int(request.form.get("current_expenditure", "0"))
            goal_papers = int(request.form.get("goal_papers", "0"))
            current_papers = int(request.form.get("current_papers", "0"))
            goal_patents_filed = int(request.form.get("goal_patents_filed", "0"))
            current_patents_filed = int(request.form.get("current_patents_filed", "0"))
            goal_patents_registered = int(request.form.get("goal_patents_registered", "0"))
            current_patents_registered = int(request.form.get("current_patents_registered", "0"))
            goal_software = int(request.form.get("goal_software", "0"))
            current_software = int(request.form.get("current_software", "0"))

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
        return redirect('/revise')

    projects = get_projects()
    # 진행률 업데이트
    for project in projects:
        project["progress"] = calculate_progress(project["start_date"], project["end_date"])
    return render_template('revise.html', projects=projects)