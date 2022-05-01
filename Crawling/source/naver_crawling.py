from datetime import datetime
from crawling_function import service_start, createFolder

now = datetime.now()
year, month, day = now.year, now.month, now.day

createFolder(f"./result/{year}{month}{day}")


if __name__ == "__main__":
    # company = input("제조 회사 이름을 작성해주세요 : ")
    # words = input("제품명을 입력해주세요 : ")
    # df = service_start(company, words)
    # df = df[df["content_cnt"] != 0].reset_index(drop=True)  # 스마트에디터 제거하는 코드

    # df.to_csv(f"./result/{year}{month}{day}/{company}_{words} 결과.csv",
    #           index=False, encoding="utf-8-sig")

    company = ["소니", "삼성", "엘지", "위닉스", "클럭", "클럭", "클럭", "클럭", "메이크맨", "이오시카", "오아", "아이뮤즈", "아이뮤즈", "삼성", "엘지",
               "SK매직", "코웨이", "보국", "쿠첸", "LG", "아이리버", "인스탁스 ", "인스탁스 ", "인스탁스 ", "캐논", "코닥", "에어맘", "유팡", "빈프레소", "쿠쿠"]
    words = ["wf-1000xm4", "더프리스타일", "코드제로a9", "타워QS", "마사지기s", "마사지기s Duo", "마사지기SE", "무릎마사지기", "무르비2", "제모기", "클린이소프트", "클링봇", "뮤패드L10", "큐커",
             "홈브루", "트리플케어", "에어카트리지", "카모플라쥬", "오토프레셔", "스타일러", "IXP-3000", "미니40", "미니11", "SQ1", "인스픽", "레트로3", "에어맘", "유팡플러스", "빈프레소", "쿠쿠 제빵기"]

    for i in range(len(company)):
        print(f"company = {company[i]}")
        print(f"words = {words[i]}")
        df = service_start(company[i], words[i])
        df = df[df["content_cnt"] != 0].reset_index(
            drop=True)  # 스마트에디터 제거하는 코드

        df.to_csv(f"./result/{year}{month}{day}/{company[i]}_{words[i]} 결과.csv",
                  index=False, encoding="utf-8-sig")
