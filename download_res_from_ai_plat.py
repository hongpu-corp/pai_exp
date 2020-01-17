# download_res_from_ai_plat.py


import requests
import base64
import threading
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree
import codecs
from constants import DEFAULT_ENCODING
from ustr import ustr

import json
import os

XML_EXT = '.xml'
ENCODE_METHOD = DEFAULT_ENCODING

class PascalVocWriter:

    def __init__(self, foldername, filename, imgSize, databaseSrc='Unknown', localImgPath=None):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = localImgPath
        self.verified = False

    def prettify(self, elem):
        """
            Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf8')
        root = etree.fromstring(rough_string)
        return etree.tostring(root, pretty_print=True, encoding=ENCODE_METHOD).replace("  ".encode(), "\t".encode())
        # minidom does not support UTF-8
        '''reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t", encoding=ENCODE_METHOD)'''

    def genXML(self):
        """
            Return XML root
        """
        # Check conditions
        if self.filename is None or \
                self.foldername is None or \
                self.imgSize is None:
            return None

        top = Element('annotation')
        if self.verified:
            top.set('verified', 'yes')

        folder = SubElement(top, 'folder')
        folder.text = self.foldername

        filename = SubElement(top, 'filename')
        filename.text = self.filename

        if self.localImgPath is not None:
            localImgPath = SubElement(top, 'path')
            localImgPath.text = self.localImgPath

        source = SubElement(top, 'source')
        database = SubElement(source, 'database')
        database.text = self.databaseSrc

        size_part = SubElement(top, 'size')
        width = SubElement(size_part, 'width')
        height = SubElement(size_part, 'height')
        depth = SubElement(size_part, 'depth')
        width.text = str(self.imgSize[1])
        height.text = str(self.imgSize[0])
        if len(self.imgSize) == 3:
            depth.text = str(self.imgSize[2])
        else:
            depth.text = '1'

        segmented = SubElement(top, 'segmented')
        segmented.text = '0'
        return top

    def addBndBox(self, xmin, ymin, xmax, ymax, name, difficult):
        bndbox = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        bndbox['name'] = name
        bndbox['difficult'] = difficult
        self.boxlist.append(bndbox)

    def appendObjects(self, top):
        for each_object in self.boxlist:
            object_item = SubElement(top, 'object')
            name = SubElement(object_item, 'name')
            name.text = ustr(each_object['name'])
            pose = SubElement(object_item, 'pose')
            pose.text = "Unspecified"
            truncated = SubElement(object_item, 'truncated')
            if int(float(each_object['ymax'])) == int(float(self.imgSize[0])) or (int(float(each_object['ymin'])) == 1):
                truncated.text = "1"  # max == height or min
            elif (int(float(each_object['xmax'])) == int(float(self.imgSize[1]))) or (int(float(each_object['xmin'])) == 1):
                truncated.text = "1"  # max == width or min
            else:
                truncated.text = "0"
            difficult = SubElement(object_item, 'difficult')
            difficult.text = str(bool(each_object['difficult']) & 1)
            bndbox = SubElement(object_item, 'bndbox')
            xmin = SubElement(bndbox, 'xmin')
            xmin.text = str(each_object['xmin'])
            ymin = SubElement(bndbox, 'ymin')
            ymin.text = str(each_object['ymin'])
            xmax = SubElement(bndbox, 'xmax')
            xmax.text = str(each_object['xmax'])
            ymax = SubElement(bndbox, 'ymax')
            ymax.text = str(each_object['ymax'])

    def save(self, targetFile=None):
        root = self.genXML()
        self.appendObjects(root)
        out_file = None
        if targetFile is None:
            out_file = codecs.open(
                self.filename + XML_EXT, 'w', encoding=ENCODE_METHOD)
        else:
            out_file = codecs.open(targetFile, 'w', encoding=ENCODE_METHOD)

        prettifyResult = self.prettify(root)
        out_file.write(prettifyResult.decode('utf8'))
        out_file.close()


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