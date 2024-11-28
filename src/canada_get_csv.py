import re
import requests
from bs4 import BeautifulSoup
import csv
from calendar import monthrange

# URL template
url_template = "https://climate.weather.gc.ca/climate_data/daily_data_e.html?hlyRange=2006-01-01%7C2024-11-26&dlyRange=2005-11-30%7C2024-11-26&mlyRange=2006-02-01%7C2007-11-01&StationID=44543&Prov=SK&urlExtension=_e.html&searchType=stnName&optLimit=yearRange&StartYear=2010&EndYear=2024&selRowPerPage=25&Line=0&searchMethod=contains&txtStationName=BRATT%27S+LAKE+CLIMATE&timeframe=2&Day=1&Year={y}&Month={m}"

# Data storage array
arr = [[[0.0, 0.0, 0.0] for _ in range(12)] for _ in range(15)]  # 2010~2024 (15 years) x 12 months

# Helper function to extract valid float value
def extract_numeric_value(text):
    # Match a floating-point number, including negative values
    match = re.search(r"-?\d+(\.\d+)?", text)
    if match:
        return float(match.group())
    return 0.0

# Start crawling
print("크롤링 시작...")
for y in range(2010, 2025):  # Year range: 2010 ~ 2024
    for m in range(1, 13):  # Month range: 1 ~ 12
        try:
            # Calculate the number of days in the month
            i = monthrange(y, m)[1]

            # Dynamically construct selectors for the given year and month
            selectors = {
                "월평균 일최고기온 (°C)": f"#dynamicDataTable > table > tbody > tr:nth-child({i + 2}) > td:nth-child(2)",
                "월평균 일최저기온 (°C)": f"#dynamicDataTable > table > tbody > tr:nth-child({i + 2}) > td:nth-child(3)",
                "월 총 강수량 (mm)": f"#dynamicDataTable > table > tbody > tr:nth-child({i + 1}) > td:nth-child(9)",
            }

            # Construct URL
            url = url_template.format(y=y, m=m)
            print(f"Processing Year={y}, Month={m}...", end=" ")

            # Send request
            session = requests.Session()
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            })

            response = session.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract data using updated selectors
            for idx, (key, selector) in enumerate(selectors.items()):
                element = soup.select_one(selector)
                value = element.text.strip() if element else "0"
                # Extract numeric value from text
                arr[y - 2010][m - 1][idx] = extract_numeric_value(value)
                print(value, arr[y - 2010][m - 1][idx], end = " | ")
            print()
        except Exception as e:
            print(f"Error at Year={y}, Month={m}: {e}")

print("크롤링 완료!")

# Save to CSV
output_file = "BRATT_Lake_Climate.csv"
print("CSV 파일 저장 중...")
with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["지점명", "시각 (YYYY-MM-DD)", "월평균 일최고기온 (°C)", "월평균 일최저기온 (°C)", "월 총 강수량 (mm)"])

    # Write data from arr
    for y in range(2010, 2025):
        for m in range(1, 13):
            date = f"{y:04d}-{m:02d}-01"
            writer.writerow([
                "BRATT'S Lake Climate",
                date,
                arr[y - 2010][m - 1][0],  # 월평균 일최고기온
                arr[y - 2010][m - 1][1],  # 월평균 일최저기온
                arr[y - 2010][m - 1][2],  # 월 총 강수량
            ])

print(f"CSV 파일이 저장되었습니다: {output_file}")
