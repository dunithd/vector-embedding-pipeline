import weaviate
import weaviate.classes.config as wc
import weaviate.classes.query as wq

from weaviate.classes.query import MetadataQuery


client = weaviate.connect_to_local(host="localhost", port=8888)

collection_name = "reviews"

reviews = client.collections.get(collection_name)

response = reviews.query.near_text(
    query="sport",
    limit=3,
    filters=(wq.Filter.by_property("rating").greater_or_equal(3) & wq.Filter.by_property("rating").less_or_equal(5)),
    return_metadata=MetadataQuery(distance=True)
)

for o in response.objects:
    print(o.properties)
    print(o.metadata.distance)

client.close()
