import requests
from bs4 import BeautifulSoup
import re

# URL과 요청 데이터 설정
url = "https://www.usclimatedata.com/ajax/load-history-content"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
form_data_template = {
    "token": "8196f2bbfdd735c7be16df655004cc39sqhyikf20BG3aSjd4b4EOtnLaq8cgonniiO1+/nEDP46f3BOAQ==",
    "page": "climate",
    "location": "usnd0037",
    "tab": "#history",
    "unit": "american",
    "unit_required": "0",
    "unit_changed": "0"
}

# Selector 설정
selectors = {
    "월평균 일최고기온 (°F)": "table.history_summary_table tbody tr:nth-of-type(1) td.text-right.high",
    "월평균 일최저기온 (°F)": "table.history_summary_table tbody tr:nth-of-type(2) td.text-right.low",
    "월 총 강수량 (inch)": "table.history_summary_table tbody tr:nth-of-type(3) td.text-right"
}

# 단위 변환 함수
def fahrenheit_to_celsius(f):
    return round((f - 32) * 5.0 / 9.0, 1)

def inches_to_mm(inches):
    return round(inches * 25.4, 1)

# 데이터 크롤링 함수
def fetch_data(year, month):
    form_data = form_data_template.copy()
    form_data["month_year"] = f"{month:02d} {year}"

    response = requests.post(url, headers=headers, data=form_data)
    if response.status_code != 200:
        print(f"Failed to fetch data for {year}-{month}. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    data = {}

    for key, selector in selectors.items():
        element = soup.select_one(selector)
        if element:
            match = re.search(r"[-+]?\d*\.?\d+", element.text)
            if match:
                value = float(match.group())
                if "°F" in key:
                    data[key] = fahrenheit_to_celsius(value)
                elif "inch" in key:
                    data[key] = inches_to_mm(value)
                else:
                    data[key] = value
            else:
                data[key] = None
        else:
            print(f"Missing data for {key} at {year}-{month}")
            data[key] = None

    return data

# 테스트 실행
print(fetch_data(2019, 8))
