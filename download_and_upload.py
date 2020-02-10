from  download_res_from_ai_plat import download_train_res
from upload_file_to_azure_storage import upload_res
import os

def download_from_aiplat(project,version,path):
    download_train_res(project, version, path)

def upload_imgfolder_to_azure_storage(path):
    piclists = os.listdir(path)
    for pic in piclists:
        path_each = os.path.join(path, pic)
        with open(path_each, 'rb') as local_path:
            upload_res('labeltest/img/'+pic, local_path)

def upload_xmlfolder_to_azure_storage(path):
    xmllists = os.listdir(path)
    for xml in xmllists:
        path_each = os.path.join(path, xml)
        with open(path_each, 'rb') as local_path:
            upload_res('labeltest/xml/'+xml, local_path)

def main():
    project = '孙可标签测试'
    version = 'v1'
    path = r'./data'
    download_from_aiplat(project, version, path)
    upload_imgfolder_to_azure_storage(path + '/img')
    upload_xmlfolder_to_azure_storage(path + '/xml')

main()
