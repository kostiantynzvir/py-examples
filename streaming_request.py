import requests
from datetime import datetime
import time
import json
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk5NDIzMDYyLCJpYXQiOjE2OTkzMzY2NjIsImp0aSI6IjcwMTYwYWQyMzI4OTRhNGZiMjUwY2Q1YzNhNTE0MTUzIiwidXNlcl9pZCI6NDF9.HMlG6Zd7VQz3oLOYI-FjVP-vX1_IVSXrcrpTxBcDrGM" # replace 'your_token' with your actual token
}
session = requests.Session()
stream = session.get('http://localhost:8000/api/v1/compose/templates/', headers=headers, stream=True)

try:
    for line in stream.iter_lines():
        # filter out keep-alive new lines
        if line:
            # process each json object individually
            for json_obj in line.decode('utf-8').split('\n'):
                if not json_obj.strip():
                    # skip any empty lines
                    continue
                try:
                    data = json.loads(json_obj)
                    print(data)
                    print(datetime.now())
                except json.JSONDecodeError:
                    print('Unable to decode JSON for: ',json_obj)
      
        time.sleep(2)
finally:
    stream.close()