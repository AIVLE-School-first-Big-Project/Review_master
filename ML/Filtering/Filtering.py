import warnings , matplotlib, platform , shap, time,os
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc 
warnings.filterwarnings('ignore')

# 한글 적용하기
path = "C:/Windows/Fonts/malgun.ttf"
if platform.system() == "Darwin":
    rc("font", family="Arial Unicode MS")
elif platform.system() == "Windows":
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc("font", family=font_name)
else:
    print("Unknown system. sorry")
# 마이너스 부호 가능.
matplotlib.rcParams['axes.unicode_minus'] = False   

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# ['content_cnt', 'content_line', '내돈내산 키워드', 'img_cnt', 'ㅋㅋㅋㅋ 빈도 수', '... 빈도 수', '쿠팡키워드', 'coupan.ng 키워드', '단점 빈도 수', '광고키워드', '이미지광고키워드3', '솔직 빈도 수', '솔직키워드1', '비교 빈도 수', 'quote_cnt', 'ㅋ 빈도 수', 'ㅠㅠ 빈도 수', 'ㅋㅋㅋ 빈도 수', '이미지광고키워드1', '이미지쿠팡키워드1', '이미지순수키워드1', '이미지광고키워드2', '이미지없음', '이미지글없음']
# ['쿠팡키워드','광고키워드','이미지광고키워드3','솔직키워드1','이미지광고키워드1','이미지쿠팡키워드1', '이미지순수키워드1', '이미지광고키워드2', '이미지없음', '이미지글없음']
# ['last_img','content','content_cnt', 'content_line', '내돈내산 키워드', 'img_cnt', 'ㅋㅋㅋㅋ 빈도 수', '... 빈도 수', 'coupan.ng 키워드', '단점 빈도 수', '솔직 빈도 수',  '비교 빈도 수', 'quote_cnt', 'ㅋ 빈도 수', 'ㅠㅠ 빈도 수', 'ㅋㅋㅋ 빈도 수',]

feature_key = {
                  # 텍스트에 대해서
                  '쿠팡키워드' : '파트너스|수수료',
                  '광고키워드' : '원고료|체험단|제작비',
                  # '솔직키워드1' : '대가 없|없는|제외|빼고|양심',
                  # 이미지 OCR 결과에 대해서
                  '이미지광고키워드1' : '체험|대여|무상|지원|업체|원고료|소정|제작',
                  # '이미지광고키워드2' : '체험|대여|무상|지원|업체|원고료|소정|협찬|원고|서비스|제작|작성',
                  '이미지광고키워드3' : '제공|대여|무상|지원|업체|원고료|소정료|취재비|제품|서비스|체험단|제작비|제작|운고료|삭성|제험단|제삭|체삭|협찬|부터|밥아|받아|선정|선점|제금|반아|세작|협진|받이',
                  '이미지쿠팡키워드1' : '파트너스|쿠팡|일정액|수수료|수수|수익|쿠광|일원|일워|다트|너스',
                  # '이미지순수키워드1' : '내돈내산|사비|직접|구매|일정액',
                }

kk_list1 = ['부터|에서','반드시','제공', '대여' ,'무상','받을|밥아|받아|반아|바아|받이|반이','선정|선점' ,'지원' ,'업체' ,'원고료|운고료','협찬|협진|협잔','부터', '소정료' ,'취재비' ,'제품','서비스' ,'체험단|제험단|체험' ,'제작비|제작|삭성|제삭|체삭|세작|새작|재작']
kk_list2 = ['파트너스|피트너스|피트|너스','쿠팡|쿠광|구팡|구파|쿠파','일정액|수수료|이정액|수료','수익|수이|스이|스익','일원|일워|인워']
kk_list3 = ['내돈내산|내돈|내산','사비','직접|지접','구매|그매','일정액|일정','솔직','않은|않']

def make_Score(DataFrame,kk_list,col_name):
    col_list_ad = []
    for i in range(len(kk_list)):
        save_col = f"{col_name}_{i}"
        DataFrame[save_col] = 0
        DataFrame.loc[DataFrame["context_img"].str.contains(kk_list1[i]),save_col]=1
        col_list_ad.append(save_col)
    return DataFrame[col_list_ad].sum(axis=1)

def feature_create(DataFrame):

  for key, item in feature_key.items():
    if "이미지" not in key :
      DataFrame[key] = 0
      DataFrame.loc[DataFrame["content"].str.contains(item),key]=1
    else:
      DataFrame[key] = 0
      DataFrame.loc[DataFrame["context_img"].str.contains(item),key]=1
  
  DataFrame.loc[DataFrame['context_img'].isnull(),"context_img"] = ''

  DataFrame["AD_score"] = make_Score(DataFrame,kk_list=kk_list1, col_name='이미지광고')
  DataFrame["CP_score"] = make_Score(DataFrame,kk_list=kk_list2, col_name='이미지쿠팡')
  DataFrame["PU_score"] = make_Score(DataFrame,kk_list=kk_list3, col_name='이미지순수')

  DataFrame["이미지글없음"] = 0
  DataFrame.loc[DataFrame['context_img']=="", "이미지글없음"]= 1
  
  origin_col = ['content_cnt','content_line','img_cnt','... 빈도 수','내돈내산 키워드','쿠팡키워드','ㅠ 빈도 수',
                '광고키워드','단점 빈도 수','ㅠ 빈도 수','광고키워드','단점 빈도 수','이미지광고키워드3','비교 빈도 수',
                '솔직 빈도 수','coupan.ng 키워드','quote_cnt','ㅋㅋㅋㅋ 빈도 수','ㅋ 빈도 수','이미지글없음','이미지광고키워드1',
                '이미지쿠팡키워드1','ㅋㅋ 빈도 수','AD_score','CP_score','PU_score']
  DataFrame = DataFrame[origin_col] 
  return DataFrame


def Adblock_filter(loaded_model,data_frame,review_id,XAI_Model,threshold = 0.7):
  os.makedirs(os.path.join(BASE_DIR,"XAI_Folder/"),exist_ok=True)
  data_frame = feature_create(data_frame)
  yhat = loaded_model.predict_proba(data_frame.values)[:,1]
  y_pred = int(yhat>= 0.7)
  if y_pred == 0:
    shap_value_plot(explainer = XAI_Model, X_test = data_frame, review_id = review_id)

  return (y_pred, yhat[0])



def shap_value_plot(explainer, X_test, review_id):
    save_file_name = os.path.join(BASE_DIR,f"XAI_Folder/{review_id}.png")
    shap.initjs()
    shap_values = explainer.shap_values(X_test.values)
    shap.force_plot(explainer.expected_value,
                    shap_values,
                    X_test.iloc[[0]], show=False,matplotlib=True).savefig(save_file_name, bbox_inches = 'tight')


if __name__=="__main__":
    start = time.time()
    print(f"\n WorkingTime : {time.time() - start} sec")