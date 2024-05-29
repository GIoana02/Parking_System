import boto3
import hashlib

session = boto3.Session(
    aws_access_key_id='AKIA6ODUZE2GJB5SJPPS',
    aws_secret_access_key='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',
)

dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')

# Helper function to get DynamoDB table
def get_table(table_name):
    return dynamodb.Table(table_name)

# Secure way to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()