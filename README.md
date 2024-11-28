# **기후 분석 프로젝트**

## **파일 구조**

```bash
climate-analysis/
├── .git/                 # Git 버전 관리 시스템 관련 파일
├── data/                 # 기후 및 생산 데이터 폴더
│   ├── climate/          # 기후 데이터
│   │   ├── raw/          # 원본 기후 데이터
│   │   │   ├── australia/
│   │   │   ├── canada/
│   │   │   ├── usa/
│   │   ├── processed/    # 처리된 기후 데이터
│   │   │   ├── state/
│   │   │   ├── station/
│   ├── 밀생산량/          # 밀 생산량 데이터
├── image/                # 시각화 결과 이미지
├── plots/                # 분석 및 시각화 결과 파일
├── src/                  # 소스 코드 파일
├── .gitignore            # Git 무시 파일 설정
├── README.md             # 프로젝트 문서
```
---

## **상세 설명**

### **1. 데이터 폴더 (`data/`)**
기후 및 밀 생산량 데이터가 저장된 폴더입니다:
- **`climate/`:** 기후 관련 데이터, `raw`(원본)과 `processed`(처리된 데이터)로 나뉩니다.
  - **원본 데이터:**
    - `australia/`: Geraldton 지역의 강수량 및 온도 데이터 포함.
    - `canada/`: Saskatchewan 지역 데이터 포함.
    - `usa/`: North Dakota 지역 데이터 포함.
  - **처리된 데이터:**
    - `state/`: 주(State) 수준에서 집계된 기후 데이터.
    - `station/`: 특정 기후 관측소에서 수집된 데이터.
- **`밀생산량/`:** 미국, 캐나다, 호주의 밀 생산량 데이터가 포함된 폴더.

### **2. 이미지 폴더 (`image/`)**
분석 결과로 생성된 이미지 파일 저장:
- 예: `Australia_rainfall.png`

### **3. 시각화 결과 (`plots/`)**
분석 및 시각화 결과 파일이 저장된 폴더:
- `월_총_강수량_mm.png` (월별 총 강수량)
- `월평균_기온_°C.png` (월평균 기온)

### **4. 소스 코드 (`src/`)**
데이터 처리를 위한 Python 스크립트와 Jupyter Notebook:
- `data_processing.ipynb`: 데이터 전처리를 위한 노트북.
- `australia_get_csv.py`: 호주 데이터를 처리하는 스크립트.
- `test.py`: 기능 테스트를 위한 스크립트.

### **5. 버전 관리 (`.git/`)**
프로젝트 버전 관리를 위한 Git 파일 포함:
- **Git Hooks 및 설정 파일.**

---

## **프로젝트 개요**

`Climate Analysis` 프로젝트는 미국, 캐나다, 호주의 기후 데이터를 분석하여 강수량, 기온 변화 추이를 평가하고, 이를 밀 생산량에 미치는 영향과 연관지어 분석합니다. **데이터 시각화**, **처리 스크립트**, **통계 모델링**을 통합하여 통찰력을 제공합니다.

---

### **실행 방법**

1. 이 저장소를 클론합니다:
   ```bash
   git clone https://github.com/your-repo/climate-analysis.git
    ```