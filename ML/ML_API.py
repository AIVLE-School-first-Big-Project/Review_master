from typing import List
from fastapi import FastAPI 
import uvicorn
from Text_summarization.Gensim import Gensim_summary
from Filtering.Filtering import Never0Classifier
    
#-------------------------------------------------------------------------------------------------------#
# creating FastAPI APP
app = FastAPI()    
    
#-------------------------------------------------------------------------------------------------------#
# API
@app.post('/summary')
async def Text_Summary(Product_Name:str, custom_weight_value:int): 
    summary = Gensim_summary(Product_Name=Product_Name,custom_weight_value=custom_weight_value)

    result = {
        'Decs' : summary
    }
    return result
    
@app.post('/filtering')
async def Blog_filter(Blog_Name :List[int]): 

    print(Blog_Name)
    model = Never0Classifier()
    pred = model.predict(Blog_Name)
    result = {
        'pred' : [int(p[0]) for p in pred]
    }
    return result

#-------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    print("start API Service")
    uvicorn.run(app, host="0.0.0.0", port=1414)
    
