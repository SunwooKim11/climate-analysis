import requests
from bs4 import BeautifulSoup
import csv

# - [new south wales - mungindi](https://en.wikipedia.org/wiki/Mungindi)
# - [victoria - mallee] (https://agriculture.vic.gov.au/__data/assets/pdf_file/0019/1042606/Grains-Industry-Fast-Facts_June-2024.pdf)
# - [southern australia - cleve](https://en.wikipedia.org/wiki/Cleve,_South_Australia)
# - [westhern australia - Geraldton Airport](https://en.wikipedia.org/wiki/Geraldton)

climate =["월평균 일 최고기온 (°C)",           # 0
          "월평균 일 최저기온 (°C)",           # 1
          "월별 일 최고기온(°C)",              # 2
          "월별 일 최저기온(°C)",              # 3
          "월 총 강수량 (mm)",                # 4
          "월평균 일 태양복사량 (MJ/m^2)"]      # 5
station = ["NSW_Moree_Aero", "VIC_Mallee_Snowtown", "SA_Cleve_SA", "WA_Geraldton_Airport"] 

# 크롤링할 URL과 기본 설정
stationIdx = 2

climateIdx = 5

startYearIdx = 23
endYearIdx = startYearIdx+14 +2

#dataTable > tbody > tr:nth-child(23) > td:nth-child(2)
# # 
# # # # 
base_url = "http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=203&p_display_type=dataFile&p_startYear=&p_c=&p_stn_num=018014" 

output_file = f"C:\kmu\climate-analysis\data\climate\processed\Australia_{station[stationIdx]}_{climateIdx}.csv"

# 결과를 저장할 배열
arr = [[0 for _ in range(12)] for _ in range(endYearIdx-startYearIdx)]  # startYearIdx<=y<=endYearIdx, 2<=m<=13에 맞는 배열 크기


# # 크롤링
print("크롤링 시작...")
for y in range(startYearIdx, endYearIdx):  # y 범위: 2 ~ 15
    for m in range(2, 14):  # m 범위: 2 ~ 13
        try:
            # 진행 상황 출력
            print(f"Processing: Year={2011 + y - startYearIdx}, Month={m - 1:02d}...", end=' ')

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
                
            value = value[:value.find('.')+2] # '43.59th' -> '43.5'
            
            # 값을 실수로 변환하고 배열에 저장
            arr[y - startYearIdx][m - 2] = float(value) if value!="-99.9" else -99.9
            print(" Done")  # 진행 상황 완료 표시
        except Exception as e:
            print(f"Error at Year={2011 + y - 2}, Month={m - 1:02d}: {e}")
            arr[y - startYearIdx][m - 2] = -99.9 # 에러 발생 시 기본값 0 저장

print("크롤링 완료!")

# CSV로 저장
print("CSV 파일 저장 중...")
with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["지점명", "시각 (YYYY-MM-DD)", climate[climateIdx]])
    
    # Geraldton 데이터 작성
    for y in range(startYearIdx, endYearIdx):
        for m in range(2, 14):
            year = 2011 + y - startYearIdx  # y값을 실제 연도로 변환
            month = m - 1  # m값을 월로 변환 (2<=m<=13에서 실제 월은 1부터 시작)
            date = f"{year:04d}-{month:02d}-01"
            writer.writerow([station[stationIdx], date, arr[y - startYearIdx][m - 2]])

print(f"CSV 파일이 저장되었습니다: {output_file}")


