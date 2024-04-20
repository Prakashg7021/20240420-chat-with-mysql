# Chat With a MySQL Database Using Python and LangChain
**Introduction**
#
💡 Quick Links:

Chinook Database for MySQL: [Chinook_MySql.sql](https://github.com/lerocha/chinook-database/releases/download/v1.4.5/Chinook_MySql.sql)

A MySQL (or SQLite) database using Python and LangChain. We will use the LangChain wrapper of sqlalchemy to interact with the database. We will also use the langchain package to create a custom chain that will allow us to chat with the database using natural language.

![image](https://github.com/Prakashg7021/20240420-chat-with-mysql/assets/111484835/384d6fa9-adbe-458e-bca2-c9ce01cb0f0c)

As you can see in the diagram above, we will first create a SQL chain that will generate SQL queries based on the user’s input. We will then create a LangChain chain that will allow us to chat with the database using natural language. We will use the langchain package to create both chains.


# Prerequisites
Before we start, make sure you have the following installed:

**Python 3.9 or later**

**MySQL**

# Setting Up the Test Database

First of all, let’s download the [Chinook database](https://github.com/lerocha/chinook-database/releases/download/v1.4.5/Chinook_MySql.sql) . This is a sample database that represents a digital media store, including tables for artists, albums, media tracks, invoices, and customers. We will use this database to test our chatbot.

For easy access, you can download the latest SQL file from [this link](https://github.com/lerocha/chinook-database/releases/download/v1.4.5/Chinook_MySql.sql).

Now, let’s set up the database. We will use both SQLite and MySQL to demonstrate how to chat with a database using Python and LangChain. I am including both databases because SQLite is easy to set up and use, while MySQL is widely used in production.

Certainly! Below is a breakdown of each line of code with explanations for your README.md:

```python
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import sqlalchemy
import tiktoken
import math
```
- These lines import necessary modules and libraries. `os` is used for setting environment variables, and various modules from LangChain and other libraries are imported for specific functionalities like handling SQL databases, managing prompts, interacting with the OpenAI API, and token calculations.

```python
os.environ["OPENAI_API_KEY"] = "<YOUR_API_KEY>"
```
- Sets the OpenAI API key as an environment variable. Replace `<YOUR_API_KEY>` with your actual OpenAI API key.

```python
mysql_uri = "mysql+mysqlconnector://root:Crossworld@localhost:3306/chinook"
db = SQLDatabase.from_uri(mysql_uri)
```
- Establishes a connection to a MySQL database named "chinook" running locally on the default port (3306). Replace the credentials and URI with your database connection details.

```python
def get_schema(_):
    return db.get_table_info()
```
- Defines a function `get_schema` that retrieves information about the tables in the connected database.

```python
llm = ChatOpenAI()
```
- Instantiates a ChatOpenAI object, which allows interaction with the OpenAI API for language tasks.

```python
def calculate_tokens(text):
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(str(text)))
```
- Defines a function `calculate_tokens` that calculates the number of tokens in a given text using the TikToken library.

```python
sql_chain = (
    RunnablePassthrough.assign(schema=get_schema)
    | ChatPromptTemplate.from_template("""
        Based on the table schema below, write a SQL query that would answer the user's question:
        {schema}

        Question: {question}
        SQL Query:
    """)
    | llm.bind(stop=["\nSQL Result:"])
    | StrOutputParser()
)
```
- Constructs a processing chain for SQL queries. It sets up a prompt template with placeholders for schema and user question, sends the prompt to OpenAI's GPT model, and parses the output.

```python
def run_query(query):
    return db.run(query)
```
- Defines a function `run_query` to execute SQL queries on the connected database.

```python
full_chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
        response=lambda vars: run_query(vars["query"]),
    )
)
```
- Combines the SQL processing chain with the query execution function to create a complete processing pipeline.

```python
user_question = 'how many  are user there in album'

result = full_chain.invoke({"question": user_question})
```
- Sets up a user question and invokes the full processing pipeline to obtain the SQL query result.

```python
print("result:", result)
```
- Prints the result of the SQL query execution.

```python
input_string = str(user_question)
output_string = result
num_inp_tokens = calculate_tokens(input_string)
num_out_tokens = calculate_tokens(output_string)
```
- Converts the user question and query result into strings, then calculates the number of tokens in each using the `calculate_tokens` function.

```python
tok_inp_k = math.ceil(num_inp_tokens / 1000)
tok_out_k = math.ceil(num_out_tokens / 1000)
```
- Calculates the number of tokens per 1,000 tokens for both input and output strings, rounding up using `math.ceil`.

```python
price_inp_k = 0.0005
price_out_k = 0.0015
```
- Sets the prices per 1,000 tokens for input and output strings.

```python
prompt_price = (tok_inp_k * price_inp_k) + (tok_out_k * price_out_k)
```
- Calculates the total prompt price based on the number of tokens and their respective prices.

```python
print(f"Input tokens: {num_inp_tokens}")
print(f"Output tokens: {num_out_tokens}")
print(f"Prompt price: ${prompt_price:.5f}")
```
- Prints the number of tokens in the input and output strings, as well as the calculated prompt price with five decimal places.
