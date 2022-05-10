# 프로그램 소개
저희는 AI기반으로 소비자들에게 똑똑한 소비 문화를 이끌 __잘샀구매__ 입니다.

![mainPage](https://user-images.githubusercontent.com/46054315/167645891-5ab5ead0-b601-4a15-9796-7192a6e06d2c.PNG)
- 관심있는 전자제품 우리가 AI로 분석할게 넌 결정만 해!
- 제조사와 전자제품명을 검색창에 입력하여 검색하면 네이버 블로그를 크롤링하여 분석해 AI를 기반으로 순수리뷰목록과 긍정어와 부정어, 리뷰요약, 연관어, 구매 링크를 확인 할 수 있어요. 
  <br>

## 🚗 How to run Ubuntu

*우분투 & AWS or * 우분투 개인서버 -> 도커를 이용한 배포
1. 도커 관련 설치
```
  sudo apt-get update
  sudo apt install docker.io 
  sudo systemctl start docker
  sudo systemctl enable docker
```
2. 도커 허브(https://hub.docker.com/)에서 아나콘다 최신 이미지를 다운받아주세요.

```
  docker pull continuumio/anaconda3:latest
```


3. 로컬 환경에서 /home/review/ 폴더를 만들고, Review_Master repository를 clone해주세요.
```
  mkdir /home/review/
  cd /home/review/
  git clone https://github.com/AIVLE-School-first-Big-Project/Review_master.git
```

4. 시크릿키를 발급 받아서 깃허브 WEB2 폴더에 secrets.json 파일을 다운 받을 수 있게 wget으로 다운 받아주세요.
```
  cd Review_master/WEB2
  wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1f-9k4u6sqlQH0Jz75uCWiKVQAPRDUDd5' -O secrets.json
```

5. 격리된 컨테이너 공간을 생성합니다.
```
  docker run -it --name aivle -v /home/ubuntu/review/:/wf -p 8000:8000 continuumio/anaconda3:latest

  ## 도커 환경에 진입했다면, 파이썬 3.6.4 버전으로 가상환경 생성.
  conda create -n django python=3.6.4
  conda activate django

  ## 도커 환경에 진입하지 못했다면
  docker start aivle
  docker exec -it aivle bash
  ## 파이썬 3.6.4 버전으로 가상환경 생성.
  conda create -n django python=3.6.4
  conda activate django
```

6. 생성된 가상환경 내에서 필요한 패키지 설치해주세요.
```
  cd /wf/Review_master/WEB2
  # mysqlclient를 설치하기 위해 아래 코드를 진행.
  apt-get update
  apt-get install default-libmysqlclient-dev build-essential 
  # 만약 위 코드가 에러가 난다면
  apt-get install python3.6-dev default-libmysqlclient-dev build-essential
  # mysqlclient가 반드시 설치가 되어야한다.
  pip install mysqlclient

  # 남은 설치 파일은 requirements를 이용하여 설치한다.
  pip install -r requirements.txt
  pip install pandas

```
7. 프로젝트 실행에 필요한 테이블을 생성해주세요.
```
  python manage.py migrate
```

8. 웹 어플리케이션(WAS)을 실행시켜주세요.
```
  python manage.py runserver 0.0.0.0:8000
```

9. 웹 사이트에 아래 링크를 입력해주세요.
```
  http://127.0.0.1:8000/app or http://외부IP:8000/app or http://도메인:8000/app 
```

10. 만약 AWS를 사용해 실행시키는 경우. 보안 그룹을 다음과 같이 설정해야 접속이 가능하다.
![aws 보안규칙](https://user-images.githubusercontent.com/46054315/152639107-711432db-85b5-4cd5-9746-0eaf73646740.PNG)

---
<br>
<br>

## 🚗 How to run Window

* 윈도우 -> 아나콘다
1. 아나콘다 프롬프트를 실행시켜 python 3.6.4의 가상환경을 만든다.
```
  conda create -n django python=3.6.4
```
2. vscode를 실행 시켜서 git clone을 진행한다.
```
  git clone https://github.com/AIVLE-School-first-Big-Project/Review_master.git
```
3. 아까 설치한 django 가상환경으로 설정 후, 필요한 패키지를 설치한다.
```
  # vs code 창에서 command Propt를 클릭하여 아래 명령어를 입력해 패키지를 설치한다.
  pip install -r requirements.txt
  pip install mysqlclient-1.4.6-cp36-cp36m-win_amd64.whl
  pip install pandas
```
4. 시크릿키 secrets.json 파일을 다운 받아서 사용해주세요.
```
  https://drive.google.com/file/d/1f-9k4u6sqlQH0Jz75uCWiKVQAPRDUDd5/view?usp=sharing
  
  # 다운 받은 secrets.json 파일을 WEB2 에 넣어주세요.
```
5. 프로젝트 실행에 필요한 테이블을 생성해주세요.
```
  python manage.py migrate
```

6. 웹 어플리케이션(WAS)을 실행시켜주세요.
```
  python manage.py runserver
```

7. 웹 사이트에 아래 링크를 입력해주세요.
```
  http://127.0.0.1:8000/app/main 
```

---

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

2022.04.15 ~ 2022.05.11 (5Week)
