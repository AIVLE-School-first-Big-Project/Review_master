from typing import List
from fastapi import FastAPI, Form, Body
import uvicorn
from Text_summarization.Gensim import Gensim_summary
from Filtering.Filtering import Adblock_filter
import secret_key as sk
from Text_sentiment.koelectra import Text_sentiment_inferense_review
import urllib.request
import time
import requests
import json
import os
import pandas as pd
from pydantic import BaseModel
from pathlib import Path
from Word_Association.association import Text_association_inferense
from fastapi.responses import FileResponse
from io import BytesIO, StringIO
import zipfile

BASE_DIR = Path(__file__).resolve().parent

#-------------------------------------------------------------------------------------------------------#
# creating FastAPI APP
app = FastAPI()
con = sk.config()

os.makedirs(os.path.join(BASE_DIR, 'Filtering/dummy/'), exist_ok=True)

#-------------------------------------------------------------------------------------------------------#
# create function


def dowload_last_img(url):
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        save_img_path = os.path.join(BASE_DIR, 'Filtering/dummy/test_img.png')
        print(save_img_path)
        print(url)
        # 이미지 저장.
        urllib.request.urlretrieve(url, save_img_path)
        time.sleep(1)
        files = {"file": open(save_img_path, "rb").read()}
        response = requests.post(
            'http://27.255.77.102:5000/evaluation', files=files)
        if response.status_code == 200:
            feature_text = response.json()
            if len(feature_text) == 0:
                print("내용이 없다고? !!")
                print(feature_text)
                result = ""
            else:
                # json_files = {"file": open(save_img_path, "rb").read()}
                # with open(save_json_path,'w',  encoding='utf-8') as f:
                #     json.dump(feature_text, f, ensure_ascii=False, indent='\t')
                result = " ".join(list(feature_text.keys()))
    except:
        result = ""
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
    print("상품 코드 : ", artice_code)
    context_result, pos_neg_result = Text_sentiment_inferense_review(
        cursor, artice_code=artice_code, review_id=review_id)

    postive = int(sum(pos_neg_result))
    negtive = int(len(pos_neg_result) - postive)

    pos_neg_result = [int(val) for val in (pos_neg_result)]
    context_result = [str(text) for text in (context_result)]
    blog_result = list(zip(context_result, pos_neg_result))
    result = {
        'postive': postive,
        'negtive': negtive,
        'blog_result': blog_result
    }
    return result


@app.post('/filtering/')
# async def Blog_filter(Blog_Name :List[str]):
async def Blog_filter(data: dict = Body(...)):
    # print("키 정보 : ",data.keys())
    data = pd.DataFrame(data)
    data["context_img"] = dowload_last_img(data['last_img'].values[0])
    # print(data.columns)
    y_pred, y_prod = Adblock_filter(data_frame=data)
    print("예측 결과 : ", int(y_pred))
    result = {
        'pred': str(int(y_pred)),
        'pro':  str(round(float(y_prod[0][0]), 2))
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

#-------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    print("start API Service")
    uvicorn.run(app, host="0.0.0.0", port=1415)
