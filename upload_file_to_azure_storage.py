##upload_file_to_azure_storage.py
import azure
from azure.storage.blob import BlockBlobService, PublicAccess

# local_path为文件的句柄
def upload_res(path, local_path):
    BlockBlobService = connect_azure()
    Container_name = "open-pai"
    path = BlockBlobService.create_blob_from_stream(Container_name, path, local_path)
    print("Upload success!")
    return path

def connect_azure():
    BlockBlobService = azure.storage.blob.BlockBlobService(account_name='savepicture',
                                                           account_key='QMIt1aIFrnYyzCMp3ovu+RYDlmrmmOo650WeQgcaFwHUK95978WmDWD/e7otVTPieydLNbFsdxglNGfJ0FqE7g==',
                                                           endpoint_suffix='core.chinacloudapi.cn')
    return BlockBlobService

with open('example.jpg', 'rb') as local_path:
    upload_res('/img/test.jpg', local_path)
