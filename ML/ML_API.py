from typing import List
from fastapi import FastAPI 
import uvicorn
from Text_summarization.Gensim import Gensim_summary
from Filtering.Filtering import Never0Classifier
import secret_key as sk
from Text_sentiment.koelectra import Text_sentiment_inferense

#-------------------------------------------------------------------------------------------------------#
# creating FastAPI APP
app = FastAPI() 

con = sk.config()

#-------------------------------------------------------------------------------------------------------#
# API
@app.post('/summary')
async def Text_Summary(artice_code:int): 
    cursor = con.connect_DB()

    print("상품 코드 : ",artice_code)
    summary = Gensim_summary(cursor,artice_code=artice_code)

    result = {
        'Decs' : summary
    }

    return result
    

@app.post('/sentiment')
async def Blog_filter(artice_code:int):
    cursor = con.connect_DB()
    print("상품 코드 : ",artice_code)
    pos_neg_result = Text_sentiment_inferense(cursor,artice_code=artice_code)
    
    postive = int(sum(pos_neg_result))
    negtive = int(len(pos_neg_result) - postive)
    result = {
        'postive' : postive,
        'negtive' : negtive,
    }
    return result

@app.post('/filtering')
async def Blog_filter(Blog_Name :List[int]):
    print("입력 후 받은 데이터 : ",Blog_Name)
    model = Never0Classifier()
    pred = model.predict(Blog_Name)
    result = {
        'pred' : [int(p[0]) for p in pred]
    }
    return result
#-------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    print("start API Service")
    uvicorn.run(app, host="0.0.0.0", port=1415)
