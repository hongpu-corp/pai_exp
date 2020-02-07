import azure
import os
from azure.storage.blob import BlockBlobService, PublicAccess
class UploadFileToAzure:

    def azure_store_image_from_stream(self, img_name, file_stream):
        BlockBlobService = self.connect_azure()
        Container_name = "open-pai"
        path = BlockBlobService.create_blob_from_bytes(Container_name, 'img/'+img_name, file_stream)
        print("Upload success！")
        return path

    def connect_azure(self):
        BlockBlobService = azure.storage.blob.BlockBlobService(account_name='savepicture',
                                                               account_key='QMIt1aIFrnYyzCMp3ovu+RYDlmrmmOo650WeQgcaFwHUK95978WmDWD/e7otVTPieydLNbFsdxglNGfJ0FqE7g==',
                                                               endpoint_suffix='core.chinacloudapi.cn')
        return BlockBlobService

uploadFile = UploadFileToAzure()

path = r'./test/img'

piclists = os.listdir(path)
for pic in piclists:
    path_each = os.path.join(path, pic)
    with open(path_each, 'rb') as f:
        img = f.read()
    uploadFile.azure_store_image_from_stream(pic, img)
