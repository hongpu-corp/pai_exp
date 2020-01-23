##upload_file_to_azure_storage.py
import azure

class UploadFileToAzure:

    def azure_store_image_from_stream(self, img_name, file_stream):
        BlockBlobService = self.connect_azure()
        Container_name = "hong-ai-plat"
        path = BlockBlobService.create_blob_from_stream(Container_name, img_name, file_stream)
        print("Upload success！")
        return path

    def connect_azure(self):
        BlockBlobService = azure.storage.blob.BlockBlobService(account_name='savepicture',
                                                               account_key='QMIt1aIFrnYyzCMp3ovu+RYDlmrmmOo650WeQgcaFwHUK95978WmDWD/e7otVTPieydLNbFsdxglNGfJ0FqE7g==',
                                                               endpoint_suffix='core.chinacloudapi.cn')
        return BlockBlobService