from sklearn.base import BaseEstimator
import numpy as np
import time
import joblib


# 임시 제로 모델
class Never0Classifier(BaseEstimator):
  def fit(self,X,y=None):
    pass
  def predict(self,X):
    return np.zeros((len(X),1),dtype=bool)

def Adblock_filter(cursor,artice_code):
  pass



if __name__=="__main__":
    start = time.time()

    model = Never0Classifier()
    pred = model.predict([1,2])

    print(pred)
    print(f"\n WorkingTime : {time.time() - start} sec")