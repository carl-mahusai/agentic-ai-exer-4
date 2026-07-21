# agentic-ai-exer-4

pip install -r requirements.txt

python app.py


## Core Specifications

* Create **at least three** PDF documents about coding best practices (e.g. Python coding best practices, SOLID design principles, etc.).
  * You may use any AI platform like ChatGPT to generate the contents of these documents.
  * This is to simulate different knowledge bases for the exercise. By now, you should have at least 3 policy documents created using the policy generator from the previous exercise and at least 3 coding best practices documents that you have created just a while ago.
* Set up vector databases that store document embeddings.
  * Employ a **simple** vector database implementation (i.e. SQLite-based DB like ChromaDB)
  * **Devise your own** document chunking strategy and top-k similar chunks retrieval strategy.
  * Feel free to use any **text embedding models** to convert your document chunks to embeddings:
    * Sample free models: Sentence Transformers from Hugging Face.
    * Sample paid models: `text-embedding-3-small` and other versions from OpenAI.
  * Create two vector databases. One for the policy documents and another for the coding best practices documents.
* Develop a **RAG agent** that is responsible for managing all RAG tasks.
  * The agent should be able to rewrite user queries before passing them to the RAG system whenever the input is vague or context dependent.
    * For example:
      * A user first asks: “What is the AI usage policy?”.
      * Later, the user follows up with: “What are its strengths and points for improvement?”.
      * Since the second query is ambiguous, the agent should transform it into a standalone query such as “What are the strengths and points of improvement of the AI usage policy?”.
      * This ensures that RAG system receives clear, self-contained queries and can retrieve the most relevant information effectively.
  * The RAG agent must be capable of **routing user queries** to the appropriate knowledge base.
    * Queries related to policy briefs should be directed to the policy knowledge base.
    * Queries concerning coding best practices should be routed to the coding best practices knowledge base.
* Let the main agent **decide if it needs to extract additional context from the RAG system** when handling user inputs.