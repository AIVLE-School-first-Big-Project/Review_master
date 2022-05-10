# 잘샀구매 서비스 API

## HOW to RUN CODE

```
conda create -n ML_API python=3.6.4

conda activate ML_API

cd ML
pip install -r requirements.txt
git clone https://github.com/ssut/py-hanspell.git

cd py-hanspell
pip install ipython
python setup.py install

cd ..

```

```
만약 cuda가 10.x를 사용하고 있다면 tensorflow를 2.3.0을 설치하면 됩니다.
pip install tensorflow==2.3.0

```


## API 실행하는 명령어
python ML_API.py
<!-- uvicorn ML_API:app --reload -->