from typing import List
from fastapi import FastAPI, Form, Body
import uvicorn
from Text_summarization.Gensim import Gensim_summary
from Filtering.Filtering import Adblock_filter
import secret_key as sk
from Text_sentiment.koelectra import Text_sentiment_inferense_review
import urllib.request
import time  
import requests, pymysql
import json
import os
import pandas as pd
from pydantic import BaseModel
from pathlib import Path
from Word_Association.association import Text_association_inferense
from fastapi.responses import FileResponse
from io import BytesIO,StringIO
import zipfile, torch
from urllib import parse
from urllib.parse import urlsplit, quote
from transformers import ElectraForSequenceClassification
import joblib
import shap
from config import config

BASE_DIR = Path(__file__).resolve().parent


#-------------------------------------------------------------------------------------------------------#
# ML/DL model loaded

device = torch.device('cpu')
sentiment_backbone_model = ElectraForSequenceClassification.from_pretrained(
        "monologg/koelectra-small-v3-discriminator", num_labels=2).to(device)

sentiment_backbone_model.load_state_dict(torch.load(os.path.join(BASE_DIR, 'Text_sentiment/model/huggingFace_model_82.pt')))

loaded_XGB_model = joblib.load(os.path.join(BASE_DIR,'Filtering/model/xgb_model_binary_v3.0.pkl')) 
loaded_XAI_BASE_DD = joblib.load(os.path.join(BASE_DIR,'Filtering/model/XAI_SHAP_v3.0.pkl')) 
explainer_XAI = shap.TreeExplainer(loaded_XGB_model,data=loaded_XAI_BASE_DD, model_output="probability",feature_names=config().origin_cols)

#-------------------------------------------------------------------------------------------------------#
# creating FastAPI APP
app = FastAPI()
con = sk.config()

os.makedirs(os.path.join(BASE_DIR, 'Filtering/dummy/'), exist_ok=True)

#-------------------------------------------------------------------------------------------------------#
# create function


def dowload_last_img(url):
    save_img_path = os.path.join(BASE_DIR, 'Filtering/dummy/test_img.png')
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    try:
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, save_img_path)
    except:
        print("한글 에러1")
        try:
            url_info = urlsplit(url)
            encoded_url = f'{url_info.scheme}://{url_info.netloc}{quote(url_info.path)}?{url_info.query}'
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(encoded_url, save_img_path)
        except:
            print("한글 에러2")
            url = ""
    if len(url) != 0:
        files = {"file": open(save_img_path, "rb").read()}
        response = requests.post(
            'http://27.255.77.102:5000/evaluation', files=files)
        if response.status_code == 200:
            feature_text = response.json()
            if len(feature_text) == 0:
                print("내용이 없다고? !!")
                result = ""
            else:
                result = " ".join(list(feature_text.keys()))
        else:
            result = ""
    else:
        result = ""

    print("OCR 결과 : ", result)
    return result

#-------------------------------------------------------------------------------------------------------#
# API


@app.post('/summary/')
async def Text_Summary(artice_code: int):
    cursor = con.connect_DB()

    print("상품 코드 : ", artice_code)
    summary = Gensim_summary(cursor, artice_code=artice_code)

    result = {
        'Decs': summary
    }

    return result


@app.post('/sentiment/')
async def Blog_filter(artice_code: int, review_id: int):
    cursor = con.connect_DB()
    print("상품 코드 : ",artice_code, 'review : ',review_id)
    context_result , pos_neg_result = Text_sentiment_inferense_review(cursor, artice_code = artice_code, review_id= review_id, model = sentiment_backbone_model)
    
    positive = int(sum(pos_neg_result))
    negative = int(len(pos_neg_result) - positive)

    pos_neg_result = [int(val) for val in (pos_neg_result)]
    context_result = [str(text) for text in (context_result)]
    blog_result = list(zip(context_result, pos_neg_result))
    result = {
        'positive': positive,
        'negative': negative,
        'blog_result': blog_result
    }
    return result


@app.post('/filtering/')
async def Blog_filter(data: dict = Body(...)):
    data = pd.DataFrame(data)
    review_id = data["review_id"].values[0]
    data["context_img"] = dowload_last_img(data['last_img'].values[0])
    y_pred, y_prod = Adblock_filter(loaded_model= loaded_XGB_model, data_frame=data, review_id=review_id, XAI_Model = explainer_XAI)
    print("예측 결과 : ", int(y_pred)," {",y_prod,"}")
    result = {
        'pred': str(int(y_pred)),
        'pro':  str(round(float(y_prod), 2))
    }
    return result


@app.post('/association/')
async def association(artice_code: int):
    cursor = con.connect_DB()

    image_pathes = Text_association_inferense(cursor, artice_code)
    save_zip_file = os.path.join(BASE_DIR, 'figImage.zip')
    suvey_zip = zipfile.ZipFile(save_zip_file, "w")
    for j in range(3):
        suvey_zip.write(os.path.relpath(image_pathes[j]))
    suvey_zip.close()
    return FileResponse(save_zip_file, media_type='application/x-zip-compressed', filename="result.zip")


@app.get('/explain/')
async def explainable_AI(review_id:int):
    load_file_name = os.path.join(BASE_DIR,f'Filtering/XAI_Folder/{review_id}.png')
    return FileResponse(load_file_name)

#-------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    print("start API Service")
    uvicorn.run(app, host="0.0.0.0", port=1415)
