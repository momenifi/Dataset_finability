import requests
from urllib.parse import urlparse
import pandas as pd
import sys
  
category = 'economic' #or 'social'
data = pd.read_csv("dois_"+category+".csv",sep=";")
dois = data.loc[:,'doi']
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
h='1'
with open('dois_domains'+category+'.csv', 'a') as f:
    sys.stdout = f
    for doi in dois:
        URL = "https://doi.org/" + doi # Specify the DOI here
        try:
            r = requests.head(URL,allow_redirects=True,headers = headers) # Redirects help follow to the actual domain
            h='1'
            parsed_uri = urlparse(r.url) #url parse to get the scheme and domain name 
            result = doi + ";" + '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri) + ";" + h
            print(result)
        except:
            try:
                r = requests.head(URL,allow_redirects=True) # Redirects help follow to the actual domain
                h='2'
                parsed_uri = urlparse(r.url) #url parse to get the scheme and domain name 
                result = doi + ";" + '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri) + ";" + h
                print(result)
            except:
                h='3'
                result = doi + ";" + "NG" + ";" + h
                print(result)