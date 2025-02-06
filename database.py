import sqlite3

DB_NAME = "projects.db"

# 데이터베이스 초기화
def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            manager TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            total_cost INTEGER NOT NULL,
            current_expenditure INTEGER NOT NULL,
            goal_papers INTEGER DEFAULT 0,
            current_papers INTEGER DEFAULT 0,
            goal_patents_filed INTEGER DEFAULT 0,
            current_patents_filed INTEGER DEFAULT 0,
            goal_patents_registered INTEGER DEFAULT 0,
            current_patents_registered INTEGER DEFAULT 0,
            goal_software INTEGER DEFAULT 0,
            current_software INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# 샘플 데이터 추가
def insert_sample_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM projects")
    count = cursor.fetchone()[0]
    if count == 0:
        projects = [
            ("AI 연구 프로젝트", "김연구", "2025-01-10", "2025-06-30", 100, 45, 3, 1, 2, 1, 1, 0, 1, 0),
            ("블록체인 분석", "이연구", "2024-09-01", "2025-01-15", 50, 50, 2, 2, 1, 1, 0, 0, 1, 1),
            ("로봇 자동화", "박연구", "2025-02-01", "2025-08-01", 200, 60, 1, 0, 2, 1, 1, 1, 2, 1)
        ]
        cursor.executemany('''
            INSERT INTO projects 
            (name, manager, start_date, end_date, total_cost, current_expenditure,
             goal_papers, current_papers, goal_patents_filed, current_patents_filed,
             goal_patents_registered, current_patents_registered, goal_software, current_software)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', projects)
        conn.commit()
    conn.close()

# 연구과제 불러오기
def get_projects():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    conn.close()
    project_list = []
    for project in projects:
        project_list.append({
            "id": project[0],
            "name": project[1],
            "manager": project[2],
            "start_date": project[3],
            "end_date": project[4],
            "total_cost": project[5],
            "current_expenditure": project[6],
            "goal_papers": project[7],
            "current_papers": project[8],
            "goal_patents_filed": project[9],
            "current_patents_filed": project[10],
            "goal_patents_registered": project[11],
            "current_patents_registered": project[12],
            "goal_software": project[13],
            "current_software": project[14],
        })
    return project_list

# 연구과제 업데이트
def update_project(project_id, name, manager, start_date, end_date, total_cost, current_expenditure,
                   goal_papers, current_papers, goal_patents_filed, current_patents_filed,
                   goal_patents_registered, current_patents_registered, goal_software, current_software):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE projects 
        SET name=?, manager=?, start_date=?, end_date=?, total_cost=?, current_expenditure=?,
            goal_papers=?, current_papers=?, goal_patents_filed=?, current_patents_filed=?,
            goal_patents_registered=?, current_patents_registered=?, goal_software=?, current_software=?
        WHERE id=?
    ''', (name, manager, start_date, end_date, total_cost, current_expenditure,
          goal_papers, current_papers, goal_patents_filed, current_patents_filed,
          goal_patents_registered, current_patents_registered, goal_software, current_software,
          project_id))
    conn.commit()
    conn.close()

# 연구과제 삭제
def delete_project(project_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id=?", (project_id,))
    conn.commit()
    conn.close()

# 연구과제 추가
def add_project(name, manager, start_date, end_date, total_cost, current_expenditure,
                goal_papers, current_papers, goal_patents_filed, current_patents_filed,
                goal_patents_registered, current_patents_registered, goal_software, current_software):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO projects 
        (name, manager, start_date, end_date, total_cost, current_expenditure,
         goal_papers, current_papers, goal_patents_filed, current_patents_filed,
         goal_patents_registered, current_patents_registered, goal_software, current_software)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, manager, start_date, end_date, total_cost, current_expenditure,
          goal_papers, current_papers, goal_patents_filed, current_patents_filed,
          goal_patents_registered, current_patents_registered, goal_software, current_software))
    conn.commit()
    conn.close()

# 실행 시 자동 초기화
if __name__ == "__main__":
    create_database()
    insert_sample_data()
    print("Database initialized successfully!")