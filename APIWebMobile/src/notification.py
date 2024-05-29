import boto3
from botocore.exceptions import ClientError

from src.dynamoDB_interaction import get_table

sns_client = boto3.client('sns', region_name='eu-north-1')

def notify_user(user_id: str, plate_number: str):
    user_table = get_table("User")
    user = user_table.get_item(Key={'user_id': user_id}).get('Item')

    if not user:
        print(f"User with ID {user_id} not found")
        return

    phone_number = user.get('phone')
    if not phone_number:
        print(f"Phone number not found for user ID {user_id}")
        return

    message = f"Mismatched plate detected: {plate_number} is parked in your reserved spot."
    subject = "Car Park Notification"

    try:
        response = sns_client.publish(
            PhoneNumber=phone_number,
            Message=message,
            Subject=subject
        )
        print(f"Notification sent: {response}")
    except ClientError as e:
        print(f"Error sending notification: {e}")
