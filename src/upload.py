import requests
import json
import time

tokens = []
tokens.append(
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

board = "na_kamura_1263/捃拾帖"

url = "https://raw.githubusercontent.com/utda/dataset/master/docs/collections/tanaka/image/collection.json"

headers = {"content-type": "application/json"}
r = requests.get(url, headers=headers)
data = r.json()

manifests = data["manifests"]

for j in range(len(manifests)):

    manifest = manifests[j]

    url = manifest["@id"]

    headers = {"content-type": "application/json"}
    r = requests.get(url, headers=headers)
    data = r.json()

    canvases = data["sequences"][0]["canvases"]

    count = 0

    for i in range(len(canvases)):

        if j <= 1 or (j <= 2 and i < 2):
            continue
            # 22もれ

        canvas = canvases[i]
        image_url = canvas["thumbnail"]["service"]["@id"] + \
            "/full/600,/0/default.jpg"
        link = "http://demo.tify.rocks/demo?manifest="+url + \
            "&tify={%22pages%22:["+str(i+1)+"],%22view%22:%22info%22}"

        note = data["label"]+" p." + \
            str(i+1) + " from 『田中芳男・博物学コレクション』(東京大学総合図書館所蔵)"

        flg = True

        while(flg):

            k = count % len(tokens)
            access_token = tokens[k]

            print(str(j)+"/"+str(len(manifests)) +
                  " - "+str(i)+"/"+str(len(canvases)))

            # print(access_token)

            response = requests.post(
                "https://api.pinterest.com/v1/pins/",
                params={
                    "access_token": access_token,
                    "board": board,
                    "note": note,
                    "link": link,
                    "image_url": image_url
                },
            )

            count += 1

            if response.status_code == 201:
                flg = False
            else:
                print(response.json()["message"])

            print("UTDA "+str(k)+": Remaining: " +
                  str(response.headers["X-RateLimit-Remaining"]))

            # print(response.status_code)

            print("-------")

            time.sleep(2 * 60)  # 2分 * 60秒
