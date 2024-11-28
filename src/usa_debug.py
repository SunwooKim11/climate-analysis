import requests

# URL and request data
base_url = "https://www.usclimatedata.com/ajax/load-history-content"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
form_data = {
    "token": "8196f2bbfdd735c7be16df655004cc39sqhyikf20BG3aSjd4b4EOtnLaq8cgonniiO1+/nEDP46f3BOAQ==",
    "page": "climate",
    "location": "usnd0037",
    "month_year": "August 2019",
    "tab": "#history",
    "unit": "american",
    "unit_required": "0",
    "unit_changed": "0"
}

# Make POST request for the specific case (2019-08)
response = requests.post(base_url, headers=headers, data=form_data)
if response.status_code == 200:
    # Save the HTML content to a file
    output_file = "debug_2019_08.html"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(response.text)
    print(f"HTML content saved to {output_file}")
else:
    print(f"Failed to fetch the data. Status code: {response.status_code}, Reason: {response.reason}")
