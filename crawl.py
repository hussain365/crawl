import shutil
import requests
import os
from mega import Mega
import json

# mega
mega = Mega()
m = mega.login('32nanne+college@gmail.com', 'WGkK-9UUGkmXC-_')

web_url = "http://localhost:8000"
web_headers = {
    'Content-Type': 'application/json'
}
codes = [438, 439, 447, 578, 608, 610, 683, 694]
for code in codes:
    for i in range(0, 999):
        student_id = f"r141{i:03}"
        url = f"http://s3-xplore.s3.ap-south-1.amazonaws.com/testlog/approvals/{code}/{student_id}.json"
        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        if (response.status_code == 200):
            try:
                # student_id = response.json().get("rollnumber")
                student_name = response.json().get("name")
                student_idcard = response.json().get("idcard")
                student_image = response.json().get("image")
                student_selfie = response.json().get("selfie")

                payload = json.dumps({
                    "endpoint": "insert_student",
                    "student_id": student_id,
                    "student_name": student_name
                })
                response = requests.request(
                    "POST", url, headers=web_headers, data=payload)
                print(response.text)

                # mega links
                mega_idcard = ""
                mega_image = ""
                mega_selfie = ""
                filename = f'{student_id}_{student_name}_{code}'

                try:
                    idcard_image = f'{filename}_idcard.jpg'
                    student_idcard_response = requests.get(
                        student_idcard, stream=True)
                    with open(idcard_image, 'wb') as out_file:
                        shutil.copyfileobj(
                            student_idcard_response.raw, out_file)
                        info = m.upload(idcard_image)
                        mega_idcard = m.get_upload_link(info)
                        if os.path.exists(idcard_image):
                            os.remove(idcard_image)
                except Exception as e:
                    print(e)

                try:
                    image_image = f'{filename}_image.jpg'
                    student_image_response = requests.get(
                        student_image, stream=True)
                    with open(image_image, 'wb') as out_file:
                        shutil.copyfileobj(
                            student_image_response.raw, out_file)
                        info = m.upload(image_image)
                        mega_image = m.get_upload_link(info)
                        if os.path.exists(image_image):
                            os.remove(image_image)
                except Exception as e:
                    print(e)

                try:
                    selfie_image = f'{filename}_selfie.jpg'
                    student_selfie_response = requests.get(
                        student_selfie, stream=True)
                    with open(selfie_image, 'wb') as out_file:
                        shutil.copyfileobj(
                            student_selfie_response.raw, out_file)
                        info = m.upload(selfie_image)
                        mega_selfie = m.get_upload_link(info)
                        if os.path.exists(selfie_image):
                            os.remove(selfie_image)
                except Exception as e:
                    print(e)
                web_payload = json.dumps({
                    "endpoint": "insert_image",
                    "student_id": student_id,
                    "student_idcard": student_idcard,
                    "student_image": student_image,
                    "student_selfie": student_selfie,
                    "mega_idcard": mega_idcard,
                    "mega_image": mega_image,
                    "mega_selfie": mega_selfie,
                    "json": json.dumps(response.json()),
                    "code": code,
                })
                response = requests.request(
                    "POST", web_url, headers=web_headers, data=web_payload)
                print(response.text)
            except Exception as e:
                print(e)
