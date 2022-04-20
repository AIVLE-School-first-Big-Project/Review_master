from fastapi import FastAPI 
import uvicorn
from Gensim import Gensim_summary

    
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
    

#-------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    print("start API Service")
    uvicorn.run(app, host="0.0.0.0", port=8001)
    
