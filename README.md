# AI04-Project-3

# AI04 - Flask Project

## 구매자 및 관리자를 위한 Sales Order 관리 App

기간: 21.07.29~21.08.02

<br>
<br>

**`배포 URL`**

[https://sdcosmetics2021.herokuapp.com/](https://sdcosmetics2021.herokuapp.com/)

<br>
<br>


**`엔티티 관계도 Schema`**

#스키마 사진 

<img src = "https://drive.google.com/file/d/1ZdRy6MikgtPBHSfPGPDyfQBLwy54yhpP/view?usp=sharing">

<br>
<br>

**`What User Can do`**

<img src = "https://drive.google.com/file/d/12c4R-FVO8LKXkHkmAKCKXOhQiZcNVRNM/view?usp=sharing">

1. 판매 제품 리스트 확인
2. 신규 오더 접수 
3. 최종소비자 선호 제품 예측 서비스 이용
4. 기존 및 신규 오더 My Page 확인 

<br>
<br>

**`What Admin Can do`**

<img src ="https://drive.google.com/file/d/1QhvCQ5p3MnL466kcUJ7DxSRm_k3ToXMM/view?usp=sharing" >

1. 판매 제품 리스트 확인
2. 신제품 등록
3. 신규 접수 오더 확인

<br>
<br>

**`Directory Tree`**
<br>
<img src ="https://drive.google.com/file/d/1NS2ETd3RrYNWaDWXfdY2iOy4_SdMzm5v/view?usp=sharing">

**flask_app**

├── __init__.py

├── models

│	├── customer.py

│  	└── sales.py

├── routes

│	├── admin_routes.py

│  	└── main_routes.py

├── service

│	├── recommend.py

├── static

│	├── css

│  	└── image

├── templates

│	├── admin_kanban.html

│  	└── admin.html

│  	└── form_.html

│  	└── index.html

│  	└── recommend.html

migrations

Procfile

requirements.txt

runtime.txt

SD_Cosmetics.db

<br>
<br>


**`Reference`**

Templates : [https://getbootstrap.com/docs/4.0/components](https://getbootstrap.com/docs/4.0/components/forms/)
