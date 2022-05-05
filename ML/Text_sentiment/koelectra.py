import secret_key as sk
import pandas as pd
import torch
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset
from transformers import ElectraForSequenceClassification, AdamW
from tqdm import tqdm
import time
import re
import time
import os
import sys
from Text_sentiment.custom_dataset import NSMCDataset
from konlpy.tag import Kkma
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


# 한개의 블로그에서 다수의 문장이 존재할것이다.
# 다수의 문장을 한 문장씩 추론하는 것보다. 한번에 추론을 하는게 어떤지. 한문장씩?
# 한문장씩 추론하는 API 부터 만들자.
BASE_DIR = Path(__file__).resolve().parent
device = torch.device('cpu')
model = ElectraForSequenceClassification.from_pretrained(
        "monologg/koelectra-small-v3-discriminator", num_labels=2).to(device)
model.load_state_dict(torch.load(os.path.join(BASE_DIR, 'model/huggingFace_model_82.pt')))
model.to(device)

def Text_sentiment_inferense(cursor, artice_code):
    kkma = Kkma()
    sql = f'''
                select review_id,content from ReviewData 
                where article_id ={artice_code} and advertise = 0
                order by content_date DESC limit 5;
        
            '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=['review_id', 'content'])
    total_blog = pd.DataFrame()

    # print("경로 : ", BASE_DIR)
    # model.load_state_dict(torch.load(os.path.join(BASE_DIR, 'model/huggingFace_model_82.pt')))
    model.eval()
    for idx in range(5):
        row = df.loc[idx].values
        review_id = row[0]
        review = row[1]
        contents = []
        result_pred = []
        # 하나의 리뷰에서 문장 단위로 자르기
        for sentence in kkma.sentences(review):
            sentence = re.sub('([a-zA-Z])', '', sentence)
            sentence = re.sub(
                '[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', sentence)
            if len(sentence) <= 5:
                continue
            else:
                contents.append(sentence)
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
    file_name = f"./Data/{artice_code}_neg_pos.csv"
    # total_blog.to_csv( os.path.join(BASE_DIR, file_name), index=False,encoding='utf-8-sig')

    return total_blog['pred'].values


def Text_sentiment_inferense_review(cursor, artice_code, review_id):
    kkma = Kkma()
    sql = f'''
                select review_id,content from ReviewData 
                where article_id ={artice_code} and review_id = {review_id} ;
            '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=['review_id', 'content'])
    total_blog = pd.DataFrame()

    device = torch.device('cpu')
    model = ElectraForSequenceClassification.from_pretrained(
        "monologg/koelectra-small-v3-discriminator", num_labels=2).to(device)
    print("경로 : ", BASE_DIR)
    model.load_state_dict(torch.load(os.path.join(
        BASE_DIR, 'model/huggingFace_model_82.pt')))
    model.eval()
    model.to(device)

    row = df.loc[0].values
    review_id = row[0]
    review = row[1]
    contents = []
    result_pred = []
    # 하나의 리뷰에서 문장 단위로 자르기
    for sentence in kkma.sentences(review):
        sentence = re.sub('([a-zA-Z])', '', sentence)
        sentence = re.sub(
            '[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', sentence)
        if len(sentence) <= 5:
            continue
        else:
            contents.append(sentence)
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
    # file_name = f"./Data/{artice_code}_neg_pos.csv"
    # total_blog.to_csv( os.path.join(BASE_DIR, file_name), index=False,encoding='utf-8-sig')

    return total_blog['context'].values, total_blog['pred'].values


if __name__ == '__main__':
    start = time.time()

    con = sk.config()
    cursor = con.connect_DB()
    artice_code = 44
    text = "반갑습니다. 재미없고 너무 하다. 별로야."
    Text_sentiment_inferense(cursor, artice_code=artice_code)
    print(f"\n WorkingTime : {time.time() - start} sec")
