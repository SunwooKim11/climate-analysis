import requests
from bs4 import BeautifulSoup
import csv

# 크롤링할 URL과 기본 설정
base_url = "http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=38&p_display_type=dataFile&p_startYear=&p_c=&p_stn_num=008315"
output_file = "C:/kmu/CBA/output/Australia_Geraldton_Airport_low_temperature.csv"

# 결과를 저장할 배열
arr = [[0 for _ in range(12)] for _ in range(14)]  # 2<=y<=15, 2<=m<=13에 맞는 배열 크기


# 크롤링
print("크롤링 시작...")
for y in range(2, 16):  # y 범위: 2 ~ 15
    for m in range(2, 14):  # m 범위: 2 ~ 13
        try:
            # 진행 상황 출력
            print(f"Processing: Year={2011 + y - 2}, Month={m - 1:02d}...", end=' ')

            # 웹 페이지 요청
            session = requests.Session()
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            })

            response = session.get(base_url)
            soup = BeautifulSoup(response.text, "html.parser")
                        
            # Selector를 생성
            #dataTable > tbody > tr:nth-child(2) > td:nth-child(12)
            selector = f"#dataTable > tbody > tr:nth-child({y}) > td:nth-child({m})"
            td = soup.select_one(selector)
            print(td, end = ' ')
            if td:  # 값이 존재하면 해당 값을 저장
                value = td.text.strip()
            else:  # 해당 태그가 없으면 -99.9 저장
                value = "-99.9"

            # 값을 실수로 변환하고 배열에 저장
            arr[y - 2][m - 2] = float(value) if value else 0.0
            print(" Done")  # 진행 상황 완료 표시
        except Exception as e:
            print(f"Error at Year={2011 + y - 2}, Month={m - 1:02d}: {e}")
            arr[y - 2][m - 2] = -99.9  # 에러 발생 시 기본값 0 저장

print("크롤링 완료!")

# CSV로 저장
print("CSV 파일 저장 중...")
with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["지점명", "시각 (YYYY-MM-DD)", "월평균 일최저기온 (°C)"])
    
    # Geraldton 데이터 작성
    for y in range(2, 16):
        for m in range(2, 14):
            year = 2011 + y - 2  # y값을 실제 연도로 변환
            month = m - 1  # m값을 월로 변환 (2<=m<=13에서 실제 월은 1부터 시작)
            date = f"{year:04d}-{month:02d}-01"
            writer.writerow(["Geraldton Airport", date, arr[y - 2][m - 2]])

print(f"CSV 파일이 저장되었습니다: {output_file}")


