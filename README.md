# Sort Lab

Python과 Flask로 만든 정렬 알고리즘 시각화 웹 애플리케이션입니다.

## 제공 기능

- Bubble, Selection, Insertion, Merge, Quick, Heap Sort
- 정렬 과정 애니메이션 및 속도/데이터 개수 조절
- 비교 횟수와 교환(또는 배열 쓰기) 횟수 표시
- 시간·공간 복잡도 비교표
- 데이터 개수별 실제 실행 시간 그래프

## VS Code에서 실행

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

브라우저에서 `http://127.0.0.1:5000`을 여세요.

> 성능 그래프는 Chart.js CDN을 사용하므로 인터넷 연결이 필요합니다.
