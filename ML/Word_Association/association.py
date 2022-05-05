import os
import re
import seaborn as sns
from matplotlib import font_manager, rc
from collections import Counter
from konlpy.tag import Hannanum
from konlpy.tag import Okt
from pathlib import Path
import scipy.stats as spst
import platform
from tqdm import tqdm
import warnings
import operator
import matplotlib.font_manager as fm
from konlpy.tag import *
import konlpy
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rc('font', family='NanumBarunGothic')
warnings.filterwarnings('ignore')


warnings.filterwarnings('ignore')

path = "C:/Windows/Fonts/malgun.ttf"

if platform.system() == "Darwin":
    rc("font", family="Arial Unicode MS")
elif platform.system() == "Windows":
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc("font", family=font_name)
else:
    print("Unknown system. sorry")

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


# 한개의 블로그에서 다수의 문장이 존재할것이다.
# 다수의 문장을 한 문장씩 추론하는 것보다. 한번에 추론을 하는게 어떤지. 한문장씩?
# 한문장씩 추론하는 API 부터 만들자.
BASE_DIR = Path(__file__).resolve().parent
korean_stopwords_path = os.path.join(BASE_DIR, "korean_stopwords.txt")

with open(korean_stopwords_path, encoding='utf8') as f:
    stopwords = f.readlines()
stopwords = [x.strip() for x in stopwords]

#-------------------------------------------------------------------------------------------------------#
# sub function


def text_cleaning(text):
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')  # 한글의 정규표현식을 나타냅니다.
    result = hangul.sub('', text)
    return result


def get_nouns(x):
    nouns_tagger = Okt()
    nouns = nouns_tagger.nouns(x)
    # 한글자 키워드를 제거
    nouns = [noun for noun in nouns if len(noun) > 1]
    # 불용어를 제거
    nouns = [noun for noun in nouns if noun not in stopwords]
    return nouns


#-------------------------------------------------------------------------------------------------------#
# main function
def Text_association_inferense(cursor, artice_code):
    sql = f'''
                select review_id,content from ReviewData 
                where article_id ={artice_code} and advertise = 0
                order by content_date DESC limit 10;
            '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=['review_id', 'content'])
    df['content'] = df['content'].apply(lambda x: text_cleaning(x))
    df['nouns'] = df['content'].apply(lambda x: get_nouns(x))

    # 동시출현 단어쌍 (말뭉치) 도출
    count = {}  # 동시출현 빈도가 저장될 dict
    for line in df['nouns']:
        # 하나의 문서에서 동일한 단어가 두번 나와도 두번의 동시출현으로 고려X
        words = list(set(line))
        # 한줄씩 읽어와서 단어별로 분리(unique한 값으로 받아오기)
        # split은 띄어쓰기를 단어로 구분하라는 함수
        for i, a in enumerate(words):
            for b in words[i+1:]:
                if a > b:
                    count[b, a] = count.get((b, a), 0) + 1
                else:
                    count[a, b] = count.get((a, b), 0) + 1

    count.get(("a", "b"), 0)  # a, b라는 key가 없을 때는 디폴트를 0으로 해라
    df = pd.DataFrame.from_dict(count, orient='index')
    list1 = []
    for i in range(len(df)):
        # index를 중심으로 계속 중첩해서 list에 넣는다
        list1.append([df.index[i][0], df.index[i][1], df[0][i]])

    result_df = pd.DataFrame(list1, columns=['word1', 'word2', "freq"])
    result_df.sort_values(by=['freq'], ascending=False, inplace=True)

    name_values = result_df["word1"].value_counts().index[:3]

    options = {
        'node_color': '#A7E4E4',
        'edge_color': '#0B8B8B',
        'width': 1,
        'with_labels': True,
        'font_weight': 'regular',
        'font_size': 10,
        # 'node_shape':"o",
    }
    img_save_folder_path = os.path.join(BASE_DIR, f"figImage/{artice_code}")
    img_pathes = []
    os.makedirs(img_save_folder_path, exist_ok=True)
    for idx in tqdm(range(3)):
        result_df_1 = result_df[result_df['word1'] ==
                                name_values[idx]].reset_index(drop=True).head(10)
        G_centrality = nx.Graph()
        for ind in range(10):
            G_centrality.add_edge(result_df_1['word1'][ind], result_df_1['word2'][ind], weight=int(
                result_df_1['freq'][ind]))

        dgr = nx.degree_centrality(G_centrality)        # 연결 중심성
        btw = nx.betweenness_centrality(G_centrality)   # 매개 중심성
        cls = nx.closeness_centrality(G_centrality)     # 근접 중심성
        egv = nx.eigenvector_centrality(G_centrality)   # 고유벡터 중심성
        pgr = nx.pagerank(G_centrality)                 # 페이지 랭크

        # 중심성이 큰 순서대로 정렬한다.
        sorted_dgr = sorted(
            dgr.items(), key=operator.itemgetter(1), reverse=True)
        sorted_btw = sorted(
            btw.items(), key=operator.itemgetter(1), reverse=True)
        sorted_cls = sorted(
            cls.items(), key=operator.itemgetter(1), reverse=True)
        sorted_egv = sorted(
            egv.items(), key=operator.itemgetter(1), reverse=True)
        sorted_pgr = sorted(
            pgr.items(), key=operator.itemgetter(1), reverse=True)

        plt.figure(figsize=(7, 7))
        G = nx.Graph()
        # 페이지 랭크에 따라 두 노드 사이의 연관성을 결정한다. (단어쌍의 연관성)
        # 연결 중심성으로 계산한 척도에 따라 노드의 크기가 결정된다. (단어의 등장 빈도수)
        for i in range(len(sorted_pgr)):
            G.add_node(sorted_pgr[i][0], nodesize=sorted_dgr[i][1])

        for ind in range(10):
            G.add_weighted_edges_from(
                [(result_df_1['word1'][ind], result_df_1['word2'][ind], int(result_df_1['freq'][ind]))])

        # 노드 크기 조정
        sizes = [G.nodes[node]['nodesize'] * 3000 for node in G]
        nx.draw(G, node_size=sizes, pos=nx.spring_layout(
            G, k=30, iterations=1000), **options, font_family=font_name)  # font_family로 폰트 등록
        ax = plt.gca()
        ax.collections[0].set_edgecolor("#0B8B8B")
        save_img_name = f"figImage/{artice_code}/fig_{idx}.jpg"
        save_img_path = os.path.join(BASE_DIR, save_img_name)
        img_pathes.append(save_img_path)
        plt.savefig(save_img_path)

    return img_pathes
