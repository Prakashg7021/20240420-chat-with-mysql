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


