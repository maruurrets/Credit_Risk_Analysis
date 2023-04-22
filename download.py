import boto3
import os

# fetch credentials from env variables
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

# setup a AWS S3 client/resource
s3 = boto3.resource(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    )

# point the resource at the existing bucket
bucket = s3.Bucket('anyoneai-datasets')

files_download = ['LeaderBoard_Data.zip', 'Leaderboard_Submission_Example.zip',
         'PAKDD-2010 training data.zip', 'PAKDD2010_Leaderboard_Submission_Example.txt',
         'PAKDD2010_Modeling_Data.txt', 'PAKDD2010_Prediction_Data.txt',
         'PAKDD2010_VariablesList.XLS', 'Prediction_Data.zip']

        
dest_directory = 'data'
source_directory = 'credit-data-2010'


def download_files(list_of_files):
    for file in list_of_files:
        dest_path = os.path.join(dest_directory, file)
        source_path = os.path.join(source_directory, file)
        with open(dest_path, 'wb') as data:
            bucket.download_fileobj(source_path, data)
          
download_files(files_download)