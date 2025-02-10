import os
import shutil
from datetime import datetime
import schedule
import time

def backup_db():
    source = "projects.db"  # 백업할 데이터베이스 파일 경로
    backup_dir = "db_backup"  # 백업 파일이 저장될 디렉토리
    
    # backup_dir 디렉토리가 없으면 생성
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # 오늘 날짜를 YYYYMMDD 형식으로 생성
    today = datetime.now().strftime("%Y%m%d")
    backup_filename = f"project_{today}.db"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # project.db 파일을 backup_path 로 복사
    shutil.copy(source, backup_path)
    print(f"Backup created: {backup_path}")

# 매일 자정(00:00)에 백업 작업 예약
schedule.every().day.at("09:34").do(backup_db)

# 스케줄러 루프 (무한 반복하여 예약된 작업 실행)
while True:
    schedule.run_pending()
    time.sleep(60)  # 60초마다 확인
