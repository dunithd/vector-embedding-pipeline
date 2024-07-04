import datetime
import json
import logging

from quixstreams import Application


logging.basicConfig(
    filename="reviews_processor.log", encoding="utf-8", level=logging.DEBUG
)
logger = logging.getLogger(__name__)


def cleanup_data(row):
    dt = datetime.datetime.fromtimestamp(row["unixReviewTime"])
    dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")

    row["datetime"] = json.dumps(dt_str)

    return row


def main():
    app = Application(
        broker_address="localhost:9092",
        loglevel="DEBUG",
        consumer_group="vectorsv1",
        auto_offset_reset="earliest",
        auto_create_topics=True,
    )

    input_topic = app.topic("reviews-raw", value_deserializer="json")
    output_topic = app.topic("reviews-clean", value_serializer="json")

    sdf = app.dataframe(topic=input_topic)

    sdf = (
        sdf.apply(cleanup_data)
        .update(lambda val: logger.info(f"Cleaned: {val}"))
        .to_topic(output_topic)
    )

    app.run(sdf)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting")
