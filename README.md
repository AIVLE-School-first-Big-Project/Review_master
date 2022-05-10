# 관심있는 전자제품 우리가 AI로 분석할게! 넌 결정만 해 :speak_no_evil:
> __안녕하세요 :wink: 저희는 부산아이(Ai)가의 `REVIEW_MASTER`팀 입니다.__
> 
> KT AIVLE SCHOOL 1기 BigProject 14조 (AI부산경남1반 2조)
> 
> :one: __개발기간__ : 2022/04/11 ~ 2022/05/11
>
> :two: __개발자__ : 에이블러 김종원, 김상희, 오수현, 이윤지, 장성우
>
> :three: __담당튜터__ : 정호용멘토님, __담당매니저__ : 김하나매니저님


<br/><br/>

## 1. :microphone: 주제
> :speaker: 생활가전과 전자기기에 대해 네이버 블로그에 업로드된 후기(리뷰)글을 크롤링 하여 광고성(대가성)후기 글을 걸러내고 순수리뷰만을 소비자에게 제공하여 소비자의 의사결정에 도움을 준다.
> 의사결정을 위해 조작되지 않은 순수리뷰목록과 리뷰요약을 제공하고 연관어분석, 감성어분석을 시각화 하여 한눈에 볼 수 있도록 하며 구매로 바로 이어질 수 있도록 구매처와 가격에 대한 정보도 안내한다.
> 전반적으로 구매고민수준이 높은 전자기기에 대해 __소비자는 다각도로 분석된 정보를 경험할 수 있어 의사결정에 도움을 받을 수 있다.__
<br/>
<br/>

## 2. :art: UIUX
전체 UIUX 보기 링크 : https://xd.adobe.com/view/23bccd5f-6fb5-4c42-b151-57b4ca045661-76ef/
![1234](https://user-images.githubusercontent.com/98193218/165659368-8eab21d0-2c4a-4913-bebc-e97f3b6d70e7.png)

<br/>
<br/>

## 3. :pencil: 문제 정의
### 3.1 추진 배경
:point_right: 대가성 홍보들의 경우, 제품의 실제 사용 리뷰보다 상품을 홍보하기 위한 목적의 내용이 많고 리뷰 수가 방대하므로 구매 의사결정에 어려움을 겪고 원하는 리뷰를 찾기 힘들다.
![123456789](https://user-images.githubusercontent.com/98193218/165668007-03ca4287-609e-40ac-b3d6-2ac694f3febc.png)
[출처] 소비자정책교육연구 제11권 1호, 2015.03, 고대균 외 1명
 
 :mag_right: 위의 도표의 출처인 소비자정책연구 제11권 1호 '소비자의사결정에서의 구매고민'에 따르면 다른 상품군에 비해 __생활가전 및 전자기기에 대해 소비자들은 전반적으로 구매고민수준이 3.36으로 가장 높게 나타났으며__ 식품과는 반대로 정보를 찾고 알아보는데 시간이 더 필요했다는 데에 관한 응답이 3.64점으로 높게 나타나 소비자가 경험하고 싶은 구매고민의 수준 자체가 다른것을 알 수 있었다. 소비자에게 제품이 중요할수록, 다른사람에게 조언 및 동의를 얻고자 할수록 구매고민의 수준이 더 높은것을 알 수 있었다. 따라서 __가전의 경우 소비자의 의사결정을 위해 다각도에서 분석한 상품의 정보가 필요하다고 판단하였다.__
<br/>
<br/>

### 3.2  서비스 기획 세분화
- `메인페이지`     : 관심상품을 검색할 수 있으며, 오늘의 추천검색어와 20~50대까지의 인기검색어를 볼 수 있다. 
- `상품분석페이지` : 검색된 관심상품에 대해 광고성(대가성)후기글을 제외한 네이버블로그 리뷰글을 볼 수 있으며 리뷰요약과 연관어분석, 감성어분석을 제공하여 사용자의 구매결정의사를 도울 수 있는 다양한 정보를 제공한다. 또한 사용자에게 상품에 대한 가격정보와 구매처에 대한 정보, 구매링크를 제공하여 구매의사결정부터 구매까지 원스톱으로 이어질 수 있는 상품분석페이지를 제공한다.
- `마이페이지`     : 회원정보수정과 검색기록보기, 나의질문, 회원탈퇴 기능을 제공하여 서비스 사용에 있어 전반적인 기능을 제공한다. 
- `질문게시판`     : 문의글과 상황을 이미지로 전찰할 수 있는 질문게시판을 제공한다. 
- `요금제`         : 구독회원(월 990원)과 일반회원(무료)으로 구분하여 구독회원에게는 상품검색기록과 아직 기록되지 않은 상품분석정보를 훨씬 더 빠르게 제공한다.
<br/>

## 4. :newspaper: 기대효과
 :pushpin: __소비자의 구매의사결정에 도움을 준다.__
-	__제품군의 트랜드 확인__ 광고가 아닌 실제 리뷰를 판단하여 조작되지 않은 트렌드를 살펴볼 수 있다. 
-	__신뢰성있는 정보제공__ 고객에게 광고성 리뷰를 배제하고 신뢰성 있는 진솔한 리뷰를 기반으로 구매 의사 결정을 도와준다. 
- __다각도의 상품분석정보 제공__ 다각도로 분석된 상품정보를 제공하여 소비자의 정보경험을 높이고 의사결정에 도움을 줄 수 있다.

 :pushpin:	__기업은 제품의 모니터링이 가능하다.__
 - __유지보수에 기여__ 리뷰와 상품분석정보 제공으로 솔직한 후기에 기반하여 고쳐야할 점을 도출하고 제품개발 및 유지 보수에 기여할 수 있다.
 - __제품 모니터링을 제공__ 객관적이고 냉철한 리뷰를 제공하여 시장분석을 가능하게 한다.
<br/>

## 5. :open_file_folder: 프로젝트 폴더 설명
- `ML`       : 상품리뷰분석 ML모델링, 요약, 연관어분석, 감성어분석등의 머신러닝 개발 폴더
- `WEB`      : 서비스를 GUI로 나타내기 위해 반응형 웹을 제작하는 프론트 폴더
- `Crawling` : 네이버블로그로 부터 상품리뷰 데이터를 수집하는 크롤링 코드 개발 폴더
<br/>

## 6. :wrench: 아키텍처
### 6.1 ERD설계
링크 : https://www.erdcloud.com/d/PST66TPBzP6ChRBC9
![12141](https://user-images.githubusercontent.com/98193218/167568634-322bbd42-86a9-47a4-bf42-ac9525b67a49.png)
<br/>
<br/>
### 6.2 아키텍쳐 설계
![123456798](https://user-images.githubusercontent.com/98193218/165856169-b35f5ea4-7520-467b-bc5f-538338551b09.png)

<br/>
<br/>

## 7. :soon: Service Flow
![1234](https://user-images.githubusercontent.com/98193218/167683766-1a22d96f-5def-4381-8fe0-7de01041bbab.png)

## 8. 환경설정
![11](https://user-images.githubusercontent.com/67889714/167681065-f38c9b99-6f1f-416a-a567-dbd2e738384a.png)

## 9. :couple: 팀 소개
![123456](https://user-images.githubusercontent.com/98193218/165661266-0a87fa96-0652-44cc-8774-44c0b2b23598.png)

## 10. :movie_camera: 시연 영상

## 11. :bell: 라이센스
