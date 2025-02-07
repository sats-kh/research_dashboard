import sqlite3

DB_NAME = "projects.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

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

def create_milestones_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Milestone TEXT NOT NULL,
            Start TEXT NOT NULL,
            Finish TEXT NOT NULL,
            Status TEXT NOT NULL,
            "세부 목표" TEXT,
            담당자 TEXT
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
            ("AI", "김연구", "2025-01-10", "2025-06-30", 100, 45, 3, 1, 2, 1, 1, 0, 1, 0),
            ("블록체인", "이연구", "2024-09-01", "2025-01-15", 50, 50, 2, 2, 1, 1, 0, 0, 1, 1),
            ("산불", "박연구", "2025-02-01", "2025-08-01", 200, 60, 1, 0, 2, 1, 1, 1, 2, 1),
            ("홍수", "김연구", "2025-01-10", "2025-06-30", 100, 45, 3, 1, 2, 1, 1, 0, 1, 0),
            ("산사태", "이연구", "2024-09-01", "2025-01-15", 50, 50, 2, 2, 1, 1, 0, 0, 1, 1),
            ("밀집", "박연구", "2025-02-01", "2025-08-01", 200, 60, 1, 0, 2, 1, 1, 1, 2, 1),
            ("블랙아이스", "김연구", "2025-01-10", "2025-06-30", 100, 45, 3, 1, 2, 1, 1, 0, 1, 0),
            ("위성", "이연구", "2024-09-01", "2025-01-15", 50, 50, 2, 2, 1, 1, 0, 0, 1, 1),
            ("로봇", "박연구", "2025-02-01", "2025-08-01", 200, 60, 1, 0, 2, 1, 1, 1, 2, 1),
            ("분산", "박연구", "2025-02-01", "2025-08-01", 200, 60, 1, 0, 2, 1, 1, 1, 2, 1),
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

def get_milestones():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM milestones")
    rows = cur.fetchall()
    conn.close()
    milestones = [dict(row) for row in rows]
    return milestones

def update_milestone(milestone_id, milestone_text, start, finish, status, detail, manager):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        UPDATE milestones
        SET Milestone = ?, Start = ?, Finish = ?, Status = ?, "세부 목표" = ?, 담당자 = ?
        WHERE id = ?
    """, (milestone_text, start, finish, status, detail, manager, milestone_id))
    conn.commit()
    conn.close()

def delete_milestone(milestone_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM milestones WHERE id = ?", (milestone_id,))
    conn.commit()
    conn.close()

def add_milestone(milestone_text, start, finish, status, detail, manager):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO milestones (Milestone, Start, Finish, Status, "세부 목표", 담당자)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (milestone_text, start, finish, status, detail, manager))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    insert_sample_data()
    create_milestones_table()

    print("Database initialized successfully!")