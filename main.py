
import os
#use

#python .\spotify_rec.py --artist "xxxx" --track "yyyy"
CLIENT_ID = "8a848c86e3954fc09810ebc56eeeb246"
CLIENT_SECRET = "dcb6ddef7bcd4afaa2244ef18b76ea51"
REDIRECT_URI = "http://localhost:8888/callback"

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

def acquire_token():
    """Fetches a Spotify web API token"""
    token_cache_dir = os.path.join(ROOT_PATH, "cache")
    token_cache_file = os.path.join(token_cache_dir, "token.p")
    if os.path.exists(token_cache_file):
        current_time = time.time()
        if current_time - os.path.getmtime(token_cache_file) < 3600:
            with open(token_cache_file, "rb") as fid:
                token = pickle.load(fid)
            return token
        else:
            grant_type = 'client_credentials'
            body_params = {'grant_type' : grant_type}
            url = 'https://accounts.spotify.com/api/token'
            response = requests.post(url, data=body_params, auth=(CLIENT_ID, CLIENT_SECRET))
            token_raw = json.loads(response.text)
            token = token_raw["access_token"]
            with open(token_cache_file, "wb") as fid:
                pickle.dump(token, fid)
            return token
    else:
        grant_type = 'client_credentials'
        body_params = {'grant_type' : grant_type}
        url = 'https://accounts.spotify.com/api/token'
        response = requests.post(url, data=body_params, auth=(CLIENT_ID, CLIENT_SECRET))
        token_raw = json.loads(response.text)
        token = token_raw["access_token"]
        with open(token_cache_file, "wb") as fid:
            pickle.dump(token, fid)
        return token

def define_settings():
    """
    Sets the endpoint as well as defines the token.
    """
    endpoint_url = "https://api.spotify.com/v1/recommendations?"
    token = acquire_token()
    settings = [endpoint_url, token]
    return settings
