# Real-time Vector Embedding Pipeline

This is a real-time data pipeline that creates vector embeddings in a vector database by consuming data from a Redpanda topic.

## Use case 

TBD

But, at a high-level, this solution ingests any textual data in real-time, creates embeddings for them, and allows users to perform semantic searching on them.

For example, marketing team analyzing product reviews made on an e-commerce store.

Let's refine the use case as we go.

## Architecture

![](./architecture.png)

The solution consists of:
- **Python script** - Simulates the product reviews customers made on an e-commerce website and produce them to a Redpanda topic.
- **Redpanda** - Ingests product review events into the `reviews` topic from the Python producer.
- **Quix** - Consumes the `reviews` topic, converts them into text embeddings, and writes them to the vector database.
- **Vector database** - Stores vector embeddings and allows client-facing applications to perform vector search on them.
- **Streamlit application** - User-facing application that allows users to type in queries in natural language and search the vector database.

## How to run?

The solution contains several components. Let's start them in proper order.

### Reviews generator
This Python script generates a stream of fake Amazon reviews and writes them into `reviews-raw` Redpanda topic.

To run the generator, navigate to the `reviews_generator` directory in a terminal and execute:

```bash
pip install -r requirements.txt
python main.py
```
You should see the `reviews-raw` topic is being populated with reviews.

### Reviews processor
This is a Quix application that transforms raw reviews into a format that is ready for vectorization.

To run the processor, navigate to the `reviews_processor` directory in a terminal and execute:

```bash
pip install -r requirements.txt
python main.py
```
You should see the `reviews-clean` topic is being populated with cleansed reviews.

### Weaviate sink
This is another Quix application that consumes the clean reviews from Redpanda and sinks them into Weaviate, a vector database.

To run the sink, navigate to the `weaviate_sink` directory in a terminal and execute:

```bash
pip install -r requirements.txt
python main.py
```
You should see the `reviews-vectorized` topic is being populated with vectorized reviews.

### Review search UI
This is a Streamlit application that enables the user to search for reviews stored in Weaviate.

To run the UI, navigate to the `search-ui` directory in a terminal and execute:

```bash
pip install -r requirements.txt
python app.py
```
You shoul see the search UI available on http://localhost:8501/.
