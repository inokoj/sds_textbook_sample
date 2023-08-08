import requests

url = "https://api-mebo.dev/api"
headers = {'content-type': 'application/json'}
item_data = {
  "api_key": "3c9e94d1-9dce-4115-aed0-762784c35b2c185b9c87457365",
  "agent_id": "b5d659fb-4d33-4bde-be4f-78735ea691051859f7bc1b5131",
  "utterance": "今日の天気は",
  "uid": "ユーザ識別子(被らなければなんでもOK)"
}

r = requests.post(url,json=item_data,headers=headers)

print(r)
print(r.json()["utterance"])
print(r.json()["bestResponse"]["utterance"])