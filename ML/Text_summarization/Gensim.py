from gensim.summarization.summarizer import summarize
import pandas as pd

from konlpy.tag import Kkma
from hanspell import spell_checker
import re, time, os

def preprocessing(review):
    # 한국어 형태소 분석 라이브러리    
    kkma = Kkma()
    
    total_review = ''
    #하나의 리뷰에서 문장 단위로 자르기
    for sentence in kkma.sentences(review):
        sentence = re.sub('([a-zA-Z])','',sentence)
        sentence = re.sub('[ㄱ-ㅎㅏ-ㅣ]+','',sentence)
        sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]','',sentence)
        if len(sentence) == 0:
            continue
        if len(sentence) < 198:
            spelled_sent = spell_checker.check(sentence)
            sentence = spelled_sent.checked
        sentence += '. '
        total_review += sentence
    return total_review

def Gensim_summary(Product_Name, custom_weight_value = 300):
    """
        params : 
            * Product_Name : 검색할 상품명
            * custom_weight_value : 화면에 요약할 단어 수
        return :
            * summary : 검색한 상품에 대한 전체 네이버 블로그 리뷰 요약글
    """
    base_path = os.getcwd()
    data_path = f'소닉_{Product_Name} (1).csv'
    data_path = os.path.join(base_path,data_path)
    
    # 데이터 로드
    df = pd.read_csv(data_path)
    # content에 널값이 없는 것에 대해서 추출
    df = df[df['content'].notnull()]
    # content 데이터 추출
    all_text = list(df['content'].iloc[0:].values)
    
    # 여러 블로그 글에 대해서 모두 한개의 문서로 변환
    review = "\n".join(all_text)

    pp = preprocessing(review)  # 기본적인 텍스트 전처리(띄어쓰기 교정)

    if custom_weight_value <150:
        custom_weight_value = 150
    summary = summarize(pp, word_count = custom_weight_value)
    summary = re.sub('\n', ' ',summary)
    
    return summary



if __name__=="__main__":
    start = time.time()

    Product_Name= 'wh-1000xm4'
    custom_weight_value = 500

    summary_review = Gensim_summary(Product_Name=Product_Name)
    print("요약글 : ")
    print("----"*10)
    print(summary_review)

    print(f"\n WorkingTime : {time.time() - start} sec")
