import requests
import json
from urllib.parse import urlparse
import pandas as pd
import sys
import xml.etree.ElementTree as ET


api_key="Pwaw88cME6mmha8yCLXWdATbPTssDMyJYfBJ"
country_codes = ['de', 'at', 'ch', 'it', 'es', 'fr', 'pl', 'nl', 'uk', 'us', 'se', 'br', 'tr', 'be', 'ie', 'pt', 'dk', 'no', 'fi', 'gr', 'hu', 'sk', 'cz', 'au', 'jp', 'ca', 'ro', 'hr', 'bg', 'si']

category = 'economic' #or 'social'
data = pd.read_csv("domains_"+category+".csv",sep=";")
domains = data.loc[:,'domain']


with open('domains_visibility_index_'+category+'.csv', 'a') as f:
    sys.stdout = f
    print("domain;visibility_index")
    for domain in domains:
        for country_code in country_codes:
            request="https://api.sistrix.com/domain.sichtbarkeitsindex?api_key="+api_key+"&host="+domain+"&country="+country_code
            response = requests.get(request)
            root= ET.fromstring(response.content)
            for child in root.iter('*'):
                if child.tag == 'answer': 
                    for tag in child:
                        h_value = tag.get('value')
                        if h_value is not None:
                            print(domain+";"+country_code+";"+h_value)