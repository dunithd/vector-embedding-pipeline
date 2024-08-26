import logging
import os
import pandas as pd
import time

from quixstreams import Application


logging.basicConfig(filename='reviews_generator.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    app = Application(
        broker_address="localhost:9092",
        loglevel="DEBUG"
    )

    topic = app.topic(name="reviews-raw", value_serializer="json")

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Construct the path to the CSV file
    json_file_path = os.path.join(script_dir, "amazon-fashion-reviews.json")

    df = pd.read_json(json_file_path, lines=True)
    logger.debug("File loaded: {json_file_path}")

    # Get the column headers as a list
    headers = df.columns.tolist()
    print(headers)

    with app.get_producer() as producer:
        for _, row in df.iterrows():
            producer.produce(
                topic=topic.name,
                key=row["reviewerID"],
                value=row.to_json()
            )
            logging.info(f"Produced {row['reviewerID']}: {row.to_json}")
            time.sleep(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting")
