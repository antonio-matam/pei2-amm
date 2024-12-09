import json
import os
from google.cloud import pubsub_v1 as pubsub
import cloudstorage


def new_message_callback(message):
    print("==== New message received ====")
    print("data:", message.data)
    print("attributes:", message.attributes)
    print("message_id:", message.message_id)
    print("publish_time:", message.publish_time)

    try:
        event_data = json.loads(message.data)
        event_type = message.attributes["eventType"]
        assert event_type == "OBJECT_FINALIZE", \
            f"Expected event type OBJECT_FINALIZE, got {event_type}"
        bucket_name = event_data["bucket"]
        assert bucket_name == os.environ["RISK_BUCKET_NAME"], \
            f"Expected bucket {os.environ['RISK_BUCKET_NAME']}, " \
            f"got {bucket_name}"
        blob_name = event_data["name"]
    except Exception as e:
        print(f"Error parsing message: {e}")
        message.ack()
        return

    print("==== Valid risk message received ===")
    print(f"Bucket: {bucket_name} - Blob: {blob_name}")

    # Read the blob and extract the alert level
    risk_message = json.loads(cloudstorage.download_blob(blob_name))

    if risk_message["level"] > threshold:
        print(f"===== Alert: Risk level is above threshold ({threshold}) ===")
        # TODO: Completar para nivel 7
    else:
        print("===== Discarting message: Risk level is below "
              "threshold ({threshold}) ===")

    # Acknowledge the message
    message.ack()


def listen_for_alerts(threshold: int):
    """
    Main function to listen for alerts.

    This function will listen in a pub/sub subscription for blobs created in a
    bucket, then read the blob and send an alert if the alert level is higher
    than the threshold.

    Returns:
        None

    Raises:
        Exception: If the alert level is higher than the threshold.

    """
    print("Listening for notifications. Triggering alerts if the alert level"
          f"is higher than {threshold}")

    # Create a pub/sub client and subscribe to the subscription

    with pubsub.SubscriberClient() as subscriber:
        future = subscriber.subscribe(
            os.environ["PUBSUB_SUBSCRIPTION"],
            callback=new_message_callback)
        try:
            future.result()
        except KeyboardInterrupt:
            future.cancel()


if __name__ == '__main__':
    threshold = int(os.environ["ALERT_THRESHOLD"])
    listen_for_alerts(threshold)
