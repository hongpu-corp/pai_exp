from  download_res_from_ai_plat import download_train_res
from upload_file_to_azure_storage import upload_res
import os

def download_from_aiplat(project,version,path):
    '''
    Download from ai-plat and save in the form of folders containing img and xml.
    :param project: the name of project
    :param version: the version of the project
    :param path: the path to save the folders
    '''
    download_train_res(project, version, path)

def upload_imgfolder_to_azure_storage(path):
    '''
    Upload the img files of the downloaded folders to azure storage.
    :param path: the path of the img files
    '''
    piclists = os.listdir(path)
    for pic in piclists:
        path_each = os.path.join(path, pic)
        with open(path_each, 'rb') as local_path:
            upload_res('test/img/'+pic, local_path)

def upload_xmlfolder_to_azure_storage(path):
    '''
    Upload the xml files of the downloaded folders to azure storage.
    :param path: the path of the xml files
    '''
    xmllists = os.listdir(path)
    for xml in xmllists:
        path_each = os.path.join(path, xml)
        with open(path_each, 'rb') as local_path:
            upload_res('test/xml/'+xml, local_path)

def main():
    project = '孙可标签测试'
    version = 'v1'
    path = r'./data'
    download_from_aiplat(project, version, path)
    upload_imgfolder_to_azure_storage(path + '/img')
    upload_xmlfolder_to_azure_storage(path + '/xml')

main()
