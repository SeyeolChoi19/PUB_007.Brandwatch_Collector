import requests, os

import datetime as dt 

from bcr_api.bwproject   import BWProject, BWUser 
from bcr_api.bwresources import *

def get_access_token(username: str, password: str, grant_type: str, client_id: str, token_file_name: str):
    response = requests.post(
        "https://api.brandwatch.com/oauth/token", 
        data = {
            "username"   : username, 
            "password"   : password,
            "grant_type" : grant_type, 
            "client_id"  : client_id
        }
    )

    if (response.status_code == 200):
        with open(token_file_name, "w") as f:
            f.write(response.json().get("access_token"))