import logging
import os
import weaviate
import weaviate.classes.config as wc

from dotenv import load_dotenv
from quixstreams import Application
from weaviate.classes.config import Configure


load_dotenv()

logging.basicConfig(filename="weaviate_sink.log", encoding="utf-8", level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = weaviate.connect_to_local(host="localhost", port=8888)
logger.info(f"Weaviate client: {client.is_ready()}")

collection_name = "reviews"

# Create a collection (similar to a SQL table)
if not client.collections.exists(collection_name):
    reviews = client.collections.create(
        name="Review",
        properties=[
            wc.Property(
                name="reviewer_id",
                data_type=wc.DataType.TEXT,
                skip_vectorization=True,
            ),
            wc.Property(name="review_text", data_type=wc.DataType.TEXT),
            wc.Property(name="summary", data_type=wc.DataType.TEXT),
            wc.Property(name="rating", data_type=wc.DataType.NUMBER),
            wc.Property(
                name="datetime", data_type=wc.DataType.TEXT, skip_vectorization=True
            ),
        ],
        vectorizer_config=wc.Configure.Vectorizer.text2vec_transformers(),
        generative_config=wc.Configure.Generative.openai(),
        inverted_index_config=wc.Configure.inverted_index(index_property_length=True),
    )


def sink(row):
    reviews = client.collections.get(collection_name)

    logger.info(f"Ingesting row: {row}")
    try:
        uuid = reviews.data.insert(
            properties={
                "reviewer_id": row["reviewerID"],
                "review_text": row["reviewText"],
                "summary": row["summary"],
                "rating": row["overall"],
                "datetime": row["datetime"],
            },
        )
        logger.info(f"Ingested vector: {uuid}")

    except Exception as e:
        logger.error(f"Error: {e}")


def main():
    app = Application(
        broker_address="localhost:9092",
        loglevel="DEBUG",
        consumer_group="vectorsv1",
        auto_offset_reset="earliest",
        auto_create_topics=True,
    )

    input_topic = app.topic("reviews-clean", value_deserializer="json")
    output_topic = app.topic("reviews-vectorized", value_serializer="json")

    sdf = app.dataframe(topic=input_topic)

    sdf = sdf.update(sink)
    sdf = sdf.to_topic(output_topic)

    app.run(sdf)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting.")
    finally:
        client.close()
        logger.info("Weaviate connection closed. Existing")
