from pathlib import Path
import json
import os


class config():
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parent
        secret_file = os.path.join(BASE_DIR, 'secrets.json')

        with open(secret_file) as f:
            self.secrets = json.loads(f.read())

    def get_secret(self, setting):
        try:
            return self.secrets[setting]
        except KeyError:
            pass
