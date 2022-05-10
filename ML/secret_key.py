from pathlib import Path
import json,os
import pymysql


class config():
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parent
        secret_file = os.path.join(BASE_DIR, 'ML_secrets.json')

        with open(secret_file) as f:
            self.secrets = json.loads(f.read())

    def get_secret(self, setting):
        try:
            return self.secrets[setting]
        except KeyError:
            error_msg = "Set the {} environment variable".format(setting)
    
    def connect_DB(self,):
        db = pymysql.connect(host = self.get_secret('HOST'), port=1412, user='review_master', password=self.get_secret("PASSWORD"),db='Busan1412',charset='utf8')
        cursor = db.cursor()
        return cursor