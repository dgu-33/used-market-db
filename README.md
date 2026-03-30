# 동국 중고 마켓 

<p align="center">
  <img src="ui_views/other%20images/%EB%8D%B0%EB%B2%A0%EC%84%A4%20%EC%95%84%EC%BD%94.jpg" alt="mascot">
</p>

Python, Tkinter, MySQL로 개발한 중고물품 거래 데스크탑 애플리케이션입니다.



## 주요 기능

- 회원가입 및 로그인
- 상품 게시글 등록, 수정, 삭제
- 제목, 카테고리, 동네, 가격, 상태, 좋아요 기준으로 게시글 검색 및 필터링
- 게시글 좋아요 / 취소
- 구매자와 판매자 간 1:1 채팅
- 판매 완료 처리 시 거래 내역 기록
- 거래 후 리뷰 및 만족도 평가
- 거래 내역, 받은 리뷰, 채팅방을 포함한 마이페이지

## 실행 환경

- Python 3.12+
- MySQL server
- DB 접속 정보를 담은 `.env` 파일 (`.env.example` 참고)
- 의존성 패키지: `mysql-connector-python`, `Pillow`, `python-dotenv`, `bcrypt`

## 실행 방법

```bash
python main.py
```

## 프로젝트 구조

```
second_hand_marketplace/
├── db/
│   └── queries.py        # SQL 쿼리 함수 모음
├── ui_views/
│   ├── GUI.py            # 메인 창 및 홈 화면
│   ├── login.py          # 로그인 화면
│   ├── signup.py         # 회원가입 화면
│   ├── add_post.py       # 게시글 등록
│   ├── search_view_post.py  # 게시글 검색, 조회, 수정
│   ├── profile.py        # 마이페이지 및 거래 내역
│   ├── chat.py           # 1:1 채팅
│   └── review.py         # 거래 후 리뷰 작성
├── config.py             # .env에서 DB 설정 로드
├── database.py           # get_connection() 팩토리
├── main.py               # 진입점
└── .env                  # DB 접속 정보 (커밋 제외)
```


