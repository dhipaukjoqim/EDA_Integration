from pprint import pprint

from requests import auth
from requests.utils import requote_uri
import requests
from requests_toolbelt.multipart import decoder

from typing import Union, Tuple, List, Dict, Any, Sequence
import json
import datetime
import os
import sys
import traceback
from collections import Counter


class MarkLogicAPI:

    with open("C:/Users/Dhipauk.Joqim/OneDrive - Sumitovant Biopharma/Documents/Projects/Curation_efforts/api/marklogic_queries/marklogic_cody_pw.txt", 'r') as myfile:
        marklogic_pw = myfile.read().rstrip()

    USER: str = 'cody'
    PASSWORD: str = str(marklogic_pw)
    
    AUTH: auth = (USER, PASSWORD)
    #AUTH: auth = auth.HTTPDigestAuth(USER, PASSWORD)
    HEADERS: dict = {'Accept': 'application/json'}

    API_URL: str = 'https://internal-ml.sumitovant.com:8011'
    #API_URL: str = 'https://jylpa5xed.7kwet5mnhat.a.marklogicsvc.com:8011'
    #API_URL: str = 'http://10.115.1.52:8092'
    API_STRUCTUREDQ_ENDP = '/v1/search?structuredQuery='
    API_DOCUMENT_ENDP = '/v1/documents?uri='
    API_EVAL_ENDP = '/v1/eval'
    PAGE_LENGTH = 500

    def __init__(self, collection: List = ['nifi_oss']):
        """
        @param collection:
        """

        self.collection = '&'.join([f'collection={i}' for i in collection])
        self.session = requests.Session()

    def request(
        self,
        url: str,
        method: str = 'get',
        to_json: bool = True,
        payload: Dict = {},
        headers: Dict = {},
    ) -> Union[requests.models.Response, Dict[str, Any], None]:
        """
        @param url:
        @param method:
        @param to_json:
        @param payload:
        @param headers:
        """

        try:
            req = {
                'get': self.session.get(
                    url, auth=self.AUTH, headers=self.HEADERS.update(headers)
                ),
                'delete': self.session.delete(
                    url, auth=self.AUTH, headers=self.HEADERS.update(headers)
                ),
                'post': self.session.post(
                    url,
                    auth=self.AUTH,
                    data=payload,
                    headers=self.HEADERS.update(headers),
                ),
            }
            resp = req[method]
            if to_json:
                return resp.json()
            return resp
        except Exception:
            print(traceback.format_exc())
            return None

def decode_response(resp) -> List:
        try:
            data = []
            _data = decoder.MultipartDecoder.from_response(resp)
            for part in _data.parts:
                _type = part.headers[b'Content-Type'].decode()
                if _type == 'application/json':
                    content = json.loads(part.content.decode())
                    if isinstance(content, list):
                        for cont in content:
                            if 'Title' in cont:
                                data.append(cont['Title'])
                    # else:
                    #     if 'Title' in content:  # document will always have an id
                    #         data = content['Title']
                    else: 
                        if 'id' in content:  # document will always have an id
                            data.append(content)
                elif _type =='text/plain':
                    content = part.content.decode()
                    content = str(content)
                    data = content
                    return data

            return data
        except Exception:
            #print(traceback.format_exc())
            print('no data found from marklogic')
            return []

def fetch_meta_prev(removedPieDate, oneWeekAgoRemovedPieDate, userGroupArray):
    print("Inside fetch META prev", flush=True)
    api = MarkLogicAPI()
    print (os.path.abspath("retrieve_doc_titles.js"))
    file_path = "C:/Users/Dhipauk.Joqim/OneDrive - Sumitovant Biopharma/Documents/Projects/Curation_efforts/api/marklogic_queries/retrieve_doc_titles.js"
    
    meta_prev_resp = []

    #TO-DO for loop by dynamically replacing INSERT_USER_GROUP
    for userGroup in userGroupArray:
        with open(file_path) as f:
            print("Fetching for userGroup", userGroup, flush=True)
            retrieve_doc_title = f.read()
            retrieve_doc_title = retrieve_doc_title.replace('REPLACE_TO_DATE', oneWeekAgoRemovedPieDate)
            retrieve_doc_title = retrieve_doc_title.replace('REPLACE_FROM_DATE', removedPieDate)
            retrieve_doc_title = retrieve_doc_title.replace('INSERT_USER_GROUP', userGroup)

            print("retrieve_doc_title", retrieve_doc_title)
            payload = {'javascript': retrieve_doc_title}
            
            url = f'{api.API_URL}{api.API_EVAL_ENDP}'
            resp = api.request(url, method='post', to_json=False, payload=payload)
            data = decode_response(resp)
            meta_obj = {}
            meta_obj['x'] = userGroup
            meta_obj['y'] = len(data)

            if (len(data)!=0):
                meta_prev_resp.append(meta_obj)
            print("meta_obj", meta_obj)

    return meta_prev_resp


def find_document_title(test_doc_id):
    
    api = MarkLogicAPI()
    print (os.path.abspath("find_doc_title.js"))
    file_path = "/root/Documents/joqim/UserEngagement_FE/api/marklogic_queries/find_doc_title.js"
    with open(file_path) as f:
        find_document_title = f.read()
        find_document_title = find_document_title.replace('REPLACE_DOC_ID',test_doc_id)

    payload = {'javascript': find_document_title}
    
    url = f'{api.API_URL}{api.API_EVAL_ENDP}'
    resp = api.request(url, method='post', to_json=False, payload=payload)
    data = decode_response(resp)
    return data

def fetch_prev(removedPieDate, oneWeekAgoRemovedPieDate, userGroup):
    
    print("Inside fetch_prev", flush=True)
    api = MarkLogicAPI()
    print (os.path.abspath("retrieve_doc_titles.js"))
    file_path = "C:/Users/Dhipauk.Joqim/OneDrive - Sumitovant Biopharma/Documents/Projects/Curation_efforts/api/marklogic_queries/retrieve_doc_titles.js"
    with open(file_path) as f:
        retrieve_doc_title = f.read()
        retrieve_doc_title = retrieve_doc_title.replace('REPLACE_TO_DATE', oneWeekAgoRemovedPieDate)
        retrieve_doc_title = retrieve_doc_title.replace('REPLACE_FROM_DATE', removedPieDate)
        retrieve_doc_title = retrieve_doc_title.replace('INSERT_USER_GROUP', userGroup)

    print("retrieve_doc_title", retrieve_doc_title)
    payload = {'javascript': retrieve_doc_title}
    
    url = f'{api.API_URL}{api.API_EVAL_ENDP}'
    resp = api.request(url, method='post', to_json=False, payload=payload)
    data = decode_response(resp)
    prev_list = []

    for i in data:
        prev = i['previous_curations'][0]
        prev_list = prev_list + prev.split("|||")
        d = {x:prev_list.count(x) for x in prev_list}

    print(d)
    return d

##Debug
# test_doc_id = '/OSS_source_documents/Press releases/html/27-01-2022_11_30_RSS_batch_1/PRNWs-Clinical_Trials_Medical_Discoveries_PR0_27-01-2022_11_30.html'
# m_api = MarkLogicAPI()
# doc_title = find_document_title(test_doc_id=test_doc_id)
#keep_documents('removedPieDate', 'oneWeekAgoRemovedPieDate')
#fetch_prev('2022-08-16T23:59:59Z', '2022-08-01T00:00:00Z', 'MYRTLE')
#fetch_meta_prev('2022-08-16T23:59:59Z', '2022-08-01T00:00:00Z', ['MYRTLE', 'NWSLTR'])
# print('complete')