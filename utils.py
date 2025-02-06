# utils.py
import datetime

# 현재 날짜 가져오기
today = datetime.date.today()

def calculate_progress(start_date, end_date):
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    total_days = (end - start).days
    elapsed_days = (today - start).days

    if elapsed_days <= 0:
        return 0  # 시작 전
    if elapsed_days >= total_days:
        return 100  # 완료됨
    return round((elapsed_days / total_days) * 100, 1)

def get_status_color(progress):
    if progress >= 80:
        return "#32CD32"  # Green (완료)
    elif progress >= 40:
        return "#FFA500"  # Orange (진행 중)
    else:
        return "#FF4500"  # Red (지연)