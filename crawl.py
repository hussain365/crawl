import shutil
import requests
import sqlite3
import os
from mega import Mega
import json

# sqlite3
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# mega
mega = Mega()
m = mega.login('32nanne+college@gmail.com', 'WGkK-9UUGkmXC-_')

codes = [552,595,607,609,740,570,612,678,680,722,584,611,654,691,583,613,675,695]
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

                cursor.execute(
                    "SELECT * FROM student WHERE student_id = ?", (student_id,))
                existing_student = cursor.fetchone()

                if existing_student is None:
                    cursor.execute("insert into student values(?,?)",
                                   (student_id, student_name))

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

                cursor.execute("insert into images (student_id,student_idcard,student_image,student_selfie,mega_student_idcard,mega_student_image,mega_student_selfie,json,code) values(?,?,?,?,?,?,?,?,?)",
                               (student_id, student_idcard, student_image, student_selfie, mega_idcard, mega_image, mega_selfie, json.dumps(response.json()), code))
                conn.commit()
            except Exception as e:
                print(e)

