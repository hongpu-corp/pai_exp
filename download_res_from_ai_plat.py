# download_res_from_ai_plat.py


import requests
import json
import base64
from get_xml import PascalVocWriter
import os
import threading


def login(email, password, url):  # 登陆模块
    # url = 'http://vi-plat.chinaeast2.cloudapp.chinacloudapi.cn:8000/api/v1/auth/'
    data = json.dumps({'email': email, 'password': password})
    response = requests.post(url, data)  # 发出请求
    res = json.loads(response.text)
    if res != -1 and res != 0:
        token = res['token']
    else:
        return {'error': '账号或密码错误'}
    header = {
        'Content-Type': 'application/json',
        'Authorization': 'jwt' + ' ' + token
    }

class Job(threading.Thread):

    def __init__(self, version_id, resource_id_list, header, img_dir, path):

        self.version_id = version_id
        self.resource_id_list = resource_id_list
        self.header = header
        self.img_dir = img_dir
        self.path = path
        self.start()

    def run(self):
        for self.resource_id in self.resource_id_list:
            self.thread_work(self.version_id, self.resource_id, self.header, self.img_dir, self.path)

    def thread_work(self, version_id, resource_id, headers, img_dir, path):
        url_download_res_label = 'http://vi-plat.chinaeast2.cloudapp.chinacloudapi.cn:8000/api/v1/download_res_label/?label_version_id=' + str(
            version_id[0]) + '&' + 'res_id=' + str(resource_id)
        response = requests.get(url_download_res_label, headers=headers)
        res_data_and_label = json.loads(response.text)
        res_data = res_data_and_label['res_data']
        res_name = res_data_and_label['res_name']
        res_label = res_data_and_label['res_label']
        label = json.loads(res_label)
        if len(label) == 1:
            res_data = res_data[0]
            img = base64.b64decode(res_data)
            file = open(img_dir + '/' + res_name, 'wb')
            file.write(img)
            file.close()
        else:  # res_name 需要改变一下
            counter = 0
            for sub_img in res_data:
                img = base64.b64decode(sub_img)
                res_name_list = res_name.split('.')
                file = open(img_dir + '/' + res_name_list[0] + '_' + str(counter) + '.jpg', 'wb')
                counter += 1
                file.write(img)
                file.close()

        # get xml
        xml_dir = path + '/' + 'xml'
        if '.jpg' in res_name:
            res_name = res_name.split('.jpg')[0]
        elif '.png' in res_name:
            res_name = res_name.split('.png')[0]
        else:
            res_name = res_name.split('.')[0]
        if not os.path.isdir(xml_dir):
            os.makedirs(xml_dir)

        counter = 0
        for name in label:
            if name == '':
                vocwriter = PascalVocWriter(foldername=xml_dir, filename=res_name, imgSize=(
                    0, 0), databaseSrc='Unknown', localImgPath=xml_dir)
                for i in label[name]:
                    minx = int(i['vertexs'][0][0])
                    miny = int(i['vertexs'][0][1])
                    maxx = int(i['vertexs'][1][0])
                    maxy = int(i['vertexs'][1][1])
                    name = i['name']
                    vocwriter.addBndBox(minx, miny, maxx, maxy, name, False)
                xml_name = res_name + ".xml"
                xml_path = os.path.join(xml_dir, xml_name)
                vocwriter.save(targetFile=xml_path)
            else:
                vocwriter = PascalVocWriter(foldername=xml_dir, filename=res_name, imgSize=(
                    0, 0), databaseSrc='Unknown', localImgPath=xml_dir)
                for i in label[name]:
                    minx = int(i['vertexs'][0][0])
                    miny = int(i['vertexs'][0][1])
                    maxx = int(i['vertexs'][1][0])
                    maxy = int(i['vertexs'][1][1])
                    name = i['name']
                    vocwriter.addBndBox(minx, miny, maxx, maxy, name, False)
                xml_name = res_name + '_' + str(counter) + ".xml"
                counter += 1
                xml_path = os.path.join(xml_dir, xml_name)
                vocwriter.save(targetFile=xml_path)