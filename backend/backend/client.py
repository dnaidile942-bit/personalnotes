import requests
URL = "http://127.0.0.1:8000"
user_details = {"username": "sanghavi", "email": "sanghavi@gmail.com", "password": "sanghavi@123"}


# response = requests.post(url = URL+"/register",json=user_details)
# print(response.status_code)
# print(response.json())
# print("line 9")

response = requests.post(url=URL+"/login",json={"email": "sanghavi@gmail.com", "password": "sanghavi@123"})
print("line 11")
response_json = response.json()
print("line 13")
print(response_json)

access_token=response_json["access_token"]
refresh_token=response_json["refresh_token"]

header={"refresh-token":refresh_token}
response=requests.post(url=URL+"/refresh",headers=header)
print(response.json())

access_token=response.json()["access_token"]

header={"token":access_token}
response=requests.get(url=URL+"/notes",headers=header)
print(response.json())

header={"token":access_token}
note={"title":"My First Note","content":"This is my first personal note"}
response=requests.post(url=URL+"/notes",headers=header,json=note)
print(response.json())
