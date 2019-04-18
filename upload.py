from google.cloud import storage
import os
def upload_to_bucket(blob_name, path_to_file, bucket_name):

    storage_client = storage.Client.from_service_account_json(
        'creds.json')

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)
    return blob.public_url

list_file = os.listdir('./images')
for file_name in list_file:
    print(upload_to_bucket('all_imgs_products/{}'.format(file_name),'./images/{}'.format(file_name),'storage_ai2019'))