import streamlit as st
import weaviate
import weaviate.classes.config as wc
import weaviate.classes.query as wq

from weaviate.classes.query import MetadataQuery


client = weaviate.connect_to_local(host="localhost", port=8888)

def search_weaviate(query):
    collection_name = "reviews"
    reviews = client.collections.get(collection_name)

    response = reviews.query.near_text(
        query=query,
        limit=3,
        filters=(wq.Filter.by_property("rating").greater_or_equal(3) & wq.Filter.by_property("rating").less_or_equal(5)),
        return_metadata=MetadataQuery(distance=True)
    )
    return response

def main():
    st.title("Product Review Search")

    # Text input field
    search_term = st.text_input('Search term')

    if st.button("Search"):
        results = search_weaviate(search_term)

        for o in results.objects:
            st.write(o.properties)
            st.write(o.metadata.distance)

        # st.dataframe(df)  # Display DataFrame

if __name__ == "__main__":
    main()

client.close()