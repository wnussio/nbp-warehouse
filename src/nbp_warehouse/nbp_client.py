'''GET https://api.nbp.pl/api/exchangerates/tables/A/2024-01-02/2024-01-05/
Accept: application/json'''

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import date

base_url='https://api.nbp.pl/api/exchangerates/tables/A'

#url=f'{base_url}/{start}/{end}/'

def build_session() -> requests.Session:
    retry=Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=['GET']
    )

    session=requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.headers['Accept']='application/json'
    return session

def fetch_tables(session: requests.Session, start: date, end: date) -> tuple[str, list[dict]]:
    url=f'{base_url}/{start}/{end}/'
    response=session.get(url,timeout=10)

    if response.status_code==404: return url,[] 
    response.raise_for_status()
    return url,response.json()
    
   

