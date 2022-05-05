import secret_key as sk
from gensim.summarization.summarizer import summarize
import pandas as pd

from konlpy.tag import Kkma
from hanspell import spell_checker
import re
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def preprocessing(review):
    # 한국어 형태소 분석 라이브러리
    kkma = Kkma()
    total_review = ''

    # 하나의 리뷰에서 문장 단위로 자르기
    for sentence in kkma.sentences(review):
        sentence = re.sub('([a-zA-Z])', '', sentence)
        sentence = re.sub('[ㄱ-ㅎㅏ-ㅣ]+', '', sentence)
        # sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]','',sentence)
        if len(sentence) == 0:
            continue
        # if len(sentence) < 198:
        #     spelled_sent = spell_checker.check(sentence)
        #     sentence = spelled_sent.checked
        # sentence += '. '
        total_review += sentence
    return total_review


def Gensim_summary(cursor, artice_code):
    """
        params : 
            * cursor : DB 정보
            * artice_code : 상품 코드
        return :
            * summary : 검색한 상품에 대한 전체 네이버 블로그 리뷰 요약글
    """

    sql = f'''
                select writer, content_date, content from ReviewData 
                where article_id ={artice_code} and advertise = 0
                order by content_date DESC limit 10;
        
            '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=['writer', 'content_date', 'content'])
    print("DB 행의 갯수 : ", df.shape[0], "개 입니다.")
    if df.shape[0] != 0:
        # content에 널값이 없는 것에 대해서 추출
        df = df[df['content'].notnull()]
        # content 데이터 추출
        all_text = list(df['content'].iloc[0:].values)

        # 여러 블로그 글에 대해서 모두 한개의 문서로 변환
        review = "\n".join(all_text)
        pp = preprocessing(review)  # 기본적인 텍스트 전처리(띄어쓰기 교정)
        summary = summarize(pp, word_count=200)
        summary = re.sub('\n', ' ', summary)
        if len(summary) == 0:
            return "광고성 블로그 리뷰로 작성된 글이 대부분이라 요약이 불가능한 상태입니다. 추후 모니터닝을 실시하여 업데이트 하도록 하겠습니다."
        else:
            return summary
    else:
        return "광고성 블로그 리뷰로 작성된 글이 대부분이라 요약이 불가능한 상태입니다. 추후 모니터닝을 실시하여 업데이트 하도록 하겠습니다."


if __name__ == "__main__":
    start = time.time()
    # DB 연결
    con = sk.config()
    cursor = con.connect_DB()

    # 요약 기능.
    summary_review = Gensim_summary(cursor, artice_code=22)
    print("요약글 : ")
    print("----"*10)
    print(summary_review)

    print(f"\n WorkingTime : {time.time() - start} sec")
