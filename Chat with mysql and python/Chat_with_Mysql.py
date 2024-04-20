# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 10:31:52 2024

@author: PrakashGupta
"""

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import sqlalchemy
import tiktoken
import math


os.environ["OPENAI_API_KEY"] = "<YOUR_API_KEY>"


mysql_uri = "mysql+mysqlconnector://root:Crossworld@localhost:3306/chinook"
db = SQLDatabase.from_uri(mysql_uri)

def get_schema(_):
    return db.get_table_info()

llm = ChatOpenAI()

def calculate_tokens(text):
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(str(text)))

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

def run_query(query):
    return db.run(query)

full_chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
        response=lambda vars: run_query(vars["query"]),
    )
)

user_question = 'how many  are user there in album'

result = full_chain.invoke({"question": user_question})

print("result:", result)

input_string = str(user_question)
output_string = result
num_inp_tokens = calculate_tokens(input_string)
num_out_tokens = calculate_tokens(output_string)

# Calculate tokens per 1k tokens
tok_inp_k = math.ceil(num_inp_tokens / 1000)
tok_out_k = math.ceil(num_out_tokens / 1000)

price_inp_k = 0.0005
price_out_k = 0.0015

# Calculate prompt price
prompt_price = (tok_inp_k * price_inp_k) + (tok_out_k * price_out_k)

print(f"Input tokens: {num_inp_tokens}")
print(f"Output tokens: {num_out_tokens}")
print(f"Prompt price: ${prompt_price:.5f}")


