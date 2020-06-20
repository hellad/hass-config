import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import logging
logging.basicConfig(level=logging.DEBUG)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': "21673",
    'client_secret': '8ce343a2696f881c2faf9231660e979d91258247',
    'refresh_token': '4f3874cf4e030eeec20c4420c02a6a5596c491c3',
    'grant_type': "refresh_token",
    'f': 'json'
}

res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print(access_token)