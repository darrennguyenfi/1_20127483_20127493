import requests
import json

def request(data):

    str ="https://tygia.com/json.php?ran=0&rate=0&gold=1&bank=VIETCOM&date=now"
    str.replace("now",data)
    print (str)
    req = requests.get(str)
    decoded_data=req.text.encode().decode('utf-8-sig') 
    data = json.loads(decoded_data)

    with open("data.json", "w") as f:
        f.write(json.dumps(data, indent=4))
    print("ok12")
    with open("data.json","r") as fi:
        data1=fi.read()
    data2=json.loads(data1)
    print(data2["golds"][0]["value"][0])
