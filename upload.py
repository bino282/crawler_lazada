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
tmp = []
with open('tmp.txt','r') as lines:
    for line in lines:
        tmp.append(line.strip())
fw = open('tmp.txt','w')
for file_name in list_file:
    if file_name not in tmp:
        print(upload_to_bucket('all_imgs_products/{}'.format(file_name),'./images/{}'.format(file_name),'storage_ai2019'))
        fw.write(file_name)
        fw.write('\n')
fw.close()
