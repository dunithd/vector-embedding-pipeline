```mermaid
%%{ init: { 'flowchart': { 'curve': 'monotoneX' } } }%%
graph LR;
reviews_generator[reviews_generator] -->|reviews-raw|reviews_processor[reviews_processor];
reviews_processor[reviews_processor] -->|reviews-clean|weaviate_sink[weaviate_sink];

```