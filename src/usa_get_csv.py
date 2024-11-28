import requests
import re
from bs4 import BeautifulSoup

# Constants for conversions
def fahrenheit_to_celsius(f):
    return round((f - 32) * 5.0 / 9.0, 1)

def inches_to_mm(inches):
    return round(inches * 25.4, 1)

# URL and request data
base_url = "https://www.usclimatedata.com/ajax/load-history-content"
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

# Updated selectors
selectors = {
    "월평균 일최고기온 (°F)": ".history_summary_table tbody tr:nth-child(1) td.text-right",
    "월평균 일최저기온 (°F)": ".history_summary_table tbody tr:nth-child(2) td.text-right",
    "월 총 강수량 (inch)": ".history_summary_table tbody tr:nth-child(3) td.text-right"
}

print("크롤링 시작...")
for y in range(2010, 2012):  # 예제 디버깅 범위로 축소
    for m in range(1, 3):  # 월 범위 축소
        try:
            # Prepare form data
            month_name = ["January", "February", "March", "April", "May", "June",
                          "July", "August", "September", "October", "November", "December"]
            form_data = form_data_template.copy()
            form_data["month_year"] = f"{month_name[m - 1]} {y}"

            # Send POST request
            response = requests.post(base_url, headers=headers, data=form_data)
            response.raise_for_status()

            # Save HTML response for debugging
            debug_file = f"debug_{y}_{m:02d}.html"
            with open(debug_file, "w", encoding="utf-8") as file:
                file.write(response.text)
            print(f"Saved debug file: {debug_file}")

            # Parse response
            soup = BeautifulSoup(response.text, "html.parser")
            if not soup.select(".history_summary_table"):
                print(f"No summary table found for Year={y}, Month={m}")
                continue

            # Extract data
            for key, selector in selectors.items():
                element = soup.select_one(selector)
                if not element:
                    print(f"Missing data for {key} at Year={y}, Month={m}")
                    continue
                print(f"Found {key}: {element.text.strip()}")  # Print extracted value for debugging

        except Exception as e:
            print(f"Error at Year={y}, Month={m}: {e}")
