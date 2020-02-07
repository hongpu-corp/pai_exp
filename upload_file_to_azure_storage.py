##upload_file_to_azure_storage.py
import azure
from azure.storage.blob import BlockBlobService, PublicAccess

def upload_res(path, local_path):
    with open(local_path, 'rb') as f:
        BlockBlobService = connect_azure()
        Container_name = "hong-ai-plat"
        path = BlockBlobService.create_blob_from_stream(Container_name, path, f)
        print("Upload success!")
        return path

def connect_azure():
    BlockBlobService = azure.storage.blob.BlockBlobService(account_name='savepicture',
                                                           account_key='QMIt1aIFrnYyzCMp3ovu+RYDlmrmmOo650WeQgcaFwHUK95978WmDWD/e7otVTPieydLNbFsdxglNGfJ0FqE7g==',
                                                           endpoint_suffix='core.chinacloudapi.cn')
    return BlockBlobService

upload_res('/img/test.jpg', 'example.jpg')
