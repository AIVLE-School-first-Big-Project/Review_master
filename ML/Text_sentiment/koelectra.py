import secret_key as sk
import pandas as pd
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm
import time, re, time, os, sys
from Text_sentiment.custom_dataset import NSMCDataset
from konlpy.tag import Kkma
from pathlib import Path
from hanspell import spell_checker

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def rm_emoji1(Data):
  return Data.encode('euc-kr','ignore').decode('euc-kr')

def Text_sentiment_inferense_review(cursor, artice_code, review_id, model):
    kkma = Kkma()
    sql = f'''
                select review_id,content from ReviewData 
                where article_id ={artice_code} and review_id = {review_id} ;
            '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=['review_id', 'content'])
    total_blog = pd.DataFrame()

    model.eval()
    row = df.loc[0].values
    review_id = row[0]
    review = row[1]
    contents = []
    result_pred = []

    review= rm_emoji1(review)
    # 하나의 리뷰에서 문장 단위로 자르기
    for sentence in kkma.sentences(review):
        sentence = re.sub('\s[a-zA-Z]\s', '', sentence)
        sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', sentence)
        if len(sentence) <= 5:
            continue
        if len(sentence) < 140:
            spelled_sent = spell_checker.check(sentence)
            sentence = spelled_sent.checked
            contents.append(sentence)
        else:
            for sentence1 in kkma.sentences(sentence):
                if len(sentence1) < 140:
                    sentence1 = spell_checker.check(sentence1)
                    sentence1 = sentence1.checked
                sentence1 += '. '
            sentence = sentence1
    contents = pd.DataFrame(contents, columns=['context'])
    inferense_dataset = NSMCDataset(contents)
    inferense_loader = DataLoader(
        inferense_dataset, batch_size=16, shuffle=False)

    input_ids_batch, attention_masks_batch = inferense_dataset[0]
    for input_ids_batch, attention_masks_batch in tqdm(inferense_loader):
        y_pred = model(input_ids_batch,
                       attention_mask=attention_masks_batch)[0]
        _, predicted = torch.max(y_pred, 1)
        result_pred += predicted.tolist()
    contents["pred"] = result_pred
    contents['review_id'] = review_id
    total_blog = pd.concat([total_blog, contents])
    total_blog['artice_code'] = artice_code

    return total_blog['context'].values, total_blog['pred'].values


if __name__ == '__main__':
    start = time.time()

    con = sk.config()
    cursor = con.connect_DB()
    artice_code = 44
    text = "반갑습니다. 재미없고 너무 하다. 별로야."
    print(f"\n WorkingTime : {time.time() - start} sec")
