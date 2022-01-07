# 28-1st-DRHEEWON-backend

> 본 repository는 웹개발 학습을 위하여 닥터마틴(https://www.drmartens.co.kr/) 사이트를 클론코딩하였습니다.

</br>
## 개발 인원 및 기간
- 개발기간: 2021.12.27. ~ 2022.01.07.
- Frontend: 김정현, 김용선, 강희원, 이석호 (repository: https://github.com/wecode-bootcamp-korea/28-1st-DRHEEWON-frontend)
- Backend: 김재엽

## 협업 도구
- slack
- Github
- Trello

## 사용기술
- Django Framework를 사용하여 웹서버 구축 및 API 개발
- MySQL을 사용하여 데이터베이스 구축
- Bcrypt 및 JWT를 사용하여 인증/인가 구현
- AWS(EC2, RDS)를 사용하여 배포

## 구현 기능
### User
-회원가입: 정규표현식을 사용한 email, password 정책 확인; 유저 아이디 중복 확인; bcrypt를 사용하여 유저 비밀번호 암호화;
-로그인: bcrpyt를 사용하여 비밀번호 복호화 및 JWT 발급

### Product
-상세페이지: 상세페이지에 필요한 데이터 제공
-목록 조회: 목록 페이지 및 메인 페이지에 필요한 데이터 목록 제공

### Review
- 리뷰 통계: 리뷰어들의 연령 별 비율 계산 및 데이터 제공
- 리뷰 조회: 상품에 맞는 리뷰를 조회하여 데이터 제공

### Cart
-장바구니 조회, 등록, 수정, 삭제 기능 구현

### Order
-Cart 관련 데이터베이스에 존재하는 값들을 order 데이터베이스로 transaction 수행
