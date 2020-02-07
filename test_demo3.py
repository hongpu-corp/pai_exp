import azure
import os
from azure.storage.blob import BlockBlobService

class UploadFileToAzure:

    def azure_store_image_from_stream(self, xml_name, file_stream):
        BlockBlobService = self.connect_azure()
        Container_name = "open-pai"
        BlockBlobService.create_blob_from_path(Container_name,'xml/'+xml_name, file_stream)
        print("Upload success！")
        return path

    def connect_azure(self):
        BlockBlobService = azure.storage.blob.BlockBlobService(account_name='savepicture',
                                                               account_key='QMIt1aIFrnYyzCMp3ovu+RYDlmrmmOo650WeQgcaFwHUK95978WmDWD/e7otVTPieydLNbFsdxglNGfJ0FqE7g==',
                                                               endpoint_suffix='core.chinacloudapi.cn')
        return BlockBlobService


uploadFile = UploadFileToAzure()
path = r'./test/xml'
xmlLists = os.listdir(path)
for xml in xmlLists:
    pathxml = os.path.join(path, xml)
    uploadFile.azure_store_image_from_stream(xml, pathxml)
