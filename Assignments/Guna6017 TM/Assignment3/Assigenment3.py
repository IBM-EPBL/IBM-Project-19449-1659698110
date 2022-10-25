from crypt import methods
from flask import Flask, render_template,request
import ibm_boto3
from ibm_botocore.client import Config,ClientError

# Constants for IBM COS values
COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud" # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "syr5pFU8tPtGnxhATWBSaPoT_fqJoj9DRPAPpBsgrggx"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/b359fa7d4ff443c49820e679571dbcb8:40535214-f3ba-4fe4-a470-6407283ae80d::"

# Create client 
cos = ibm_boto3.client("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("Assignment3.html")

def multi_part_upload(bucket_name,item_name,file_path):
    try:
        print("Starting file Transfer for [0] to bucket [1]\n".format(item_name,bucket_name))
        
        #set 5mb file size limit 
        part_size = 1024 * 1024 * 5
        
        #set max file size limit 15mb
        file_threshold = 1024 * 1024 *15

        #set the transfer threshold and chunk size
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(multipart_threshold = file_threshold,
                                                              multipart_chunksize = part_size)
        
        #The upload file obj is method will be automatically execute a multipart upload in 5mb chunk size upto 15mb
        
        with open(file_path,"rb") as file_data:
            cos.Object(bucket_name,item_name).upload_fileobj(
                Fileobj = file_data,
                Config = transfer_config
            )
        print("Transfer for[0] Completed\n".format(item_name))
    except ClientError as be:
        print("Client Error : [0]\n".format(be))
    except Exception as e:
        print("Unable to Complete multi part upload :[0]\n".format(e))

# def multi_part_upload(bucket_name, item_name, file_path):
#     try:
#         print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
#         # set 5 MB chunks
#         part_size = 1024 * 1024 * 5

#         # set threadhold to 15 MB
#         file_threshold = 1024 * 1024 * 15

#         # set the transfer threshold and chunk size
#         transfer_config = ibm_boto3.s3.transfer.TransferConfig(
#             multipart_threshold=file_threshold,
#             multipart_chunksize=part_size
#         )

#         # the upload_fileobj method will automatically execute a multi-part upload
#         # in 5 MB chunks for all files over 15 MB
#         with open(file_path, "rb") as file_data:
#             cos.Object(bucket_name, item_name).upload_fileobj(
#                 Fileobj=file_data,
#                 Config=transfer_config
#             )

#         print("Transfer for {0} Complete!\n".format(item_name))
#     except ClientError as be:
#         print("CLIENT ERROR: {0}\n".format(be))
#     except Exception as e:
#         print("Unable to complete multi-part upload: {0}".format(e))

@app.route("/delete",methods=['GET','POST'])
def delete():
    return render_template("deletefiles.html")


@app.route("/uploader",methods = ['GET','POST'])
def uploader():
    if request.method == 'POST':
        bucket = request.form['bucket']
        file_Name = request.form['filename']
        f = request.files['file']
        multi_part_upload(bucket,file_Name,f.filename)
        return "File Uploaded Sucessfully"

    if request.method == 'GET':
        return render_template("Assignment3.html")

def delete_item(bucket_name, object_name):
    try:
        cos.delete_object(Bucket=bucket_name, Key=object_name)
        print("Item: {0} deleted!\n".format(object_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to delete object: {0}".format(e))

@app.route('/deletefile', methods = ['GET', 'POST'])
def deletefile():
   if request.method == 'POST':
       bucket=request.form['bucket']
       name_file=request.form['filename']
       
       delete_item(bucket,name_file)
       return 'file deleted successfully'
    
   if request.method == 'GET':
       return render_template('delete.html')

if __name__ == "__main__":
    app.run(debug = True)