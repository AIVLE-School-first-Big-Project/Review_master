# 💰 Review_Master (잘샀구매)

<img width="800" alt="">

- 관심있는 전자제품 우리가 AI로 분석할게 넌 결정만 해!
- 제조사와 전자제품명을 검색창에 입력하여 검색하면 네이버 블로그를 크롤링하여 분석해 AI를 기반으로 순수리뷰목록과 긍정어와 부정어, 리뷰요약, 연관어, 구매 링크를 확인 할 수 있어요. 
  <br>

## 🚗 How to run

*우분투 & AWS or * 우분투 개인서버 -> 도커를 이용한 배포

1. 도커 허브(https://hub.docker.com/)에서 아나콘다 최신 이미지를 다운받아주세요.

```
  docker pull continuumio/anaconda3:latest
```


2. 로컬 환경에서 /home/review/ 폴더를 만들고, Review_Master repository를 clone해주세요.
```
  mkdir /home/review/
  cd /home/review/
  git clone https://github.com/AIVLE-School-first-Big-Project/Review_master.git
```

3. 시크릿키를 발급 받아서 깃허브 홈디렉토리에 secrets.json 파일을 생성 후 기입해주세요.
```
  cd Review_master/WEB2
  https://www.miniwebtool.com/django-secret-key-generator/
  vi secrets.json
  {
    "SECRET_KEY": "..."
  }
```

4. 격리된 컨테이너 공간을 생성합니다.
```
  docker run -it --name Lab -v /home/review/:/working_docker_folder -p 8000:8000 continuumio/anaconda3:latest

  ## 도커 환경에 진입했다면, 파이썬 3.6.4 버전으로 가상환경 생성.
  conda create -n lab python=3.6.4
  conda activate lab

  ## 도커 환경에 진입하지 못했다면
  docker start Lab
  docker exec -it Lab bash
  ## 파이썬 3.6.4 버전으로 가상환경 생성.
  conda create -n lab python=3.6.4
  conda activate lab
```

5. 생성된 가상환경 내에서 필요한 패키지 설치해주세요.
```
  cd /working_docker_folder/Review_master/WEB2
  # mysqlclient를 설치하기 위해 아래 코드를 진행.
  apt-get update
  # 만약 아래 코드가 에러가 난다면 - > apt-get install default-libmysqlclient-dev build-essential 
  apt-get install python3.6-dev default-libmysqlclient-dev build-essential
  # mysqlclient가 반드시 설치가 되어야한다.
  pip install mysqlclient

  # 남은 설치 파일은 requirements를 이용하여 설치한다.
  pip install -r requirements.txt

```
6. 프로젝트 실행에 필요한 테이블을 생성해주세요.
```
  python manage.py migrate
```

7. 웹 어플리케이션(WAS)을 실행시켜주세요.
```
  python manage.py runserver 0.0.0.0:8000
```

8. 웹 사이트에 아래 링크를 입력해주세요.
```
  http://127.0.0.1:8000/app or http://외부IP:8000/app or http://도메인:8000/app 
```

9. 만약 AWS를 사용해 실행시키는 경우. 보안 그룹을 다음과 같이 설정해야 접속이 가능하다.
![aws 보안규칙](https://user-images.githubusercontent.com/46054315/152639107-711432db-85b5-4cd5-9746-0eaf73646740.PNG)

---
<br>
<br>


## ⚙ Environment

Frontend

```
- bootstrap : 4.0
```

Backend

```
- django version : 3.2.11
```

Database

```
- MariaDB
```

<br>

## ⚡ tech-stack

### front-end

- bootstrap
- css

### backend

- django
- MariaDB

<br>

## 🌞 Contributors

- 김종원 👉 [JONWON2](https://github.com/JONWON2)
- 김상희 👉 [corgiccori97](https://github.com/corgiccori97)
- 오수현 👉 [soohyun97](https://github.com/soohyun97)
- 이윤지 👉 [dbswl2324](https://github.com/dbswl2324)
- 장성우 👉 [CastleRain](https://github.com/CastleRain)

<br>

## 📅 Development period

2022.04.15 ~ 2022.05.11