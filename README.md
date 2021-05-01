# BarebonesDB

![BarebonesDB logo](https://i.imgur.com/fdOrgps.png)

A simple, extremely lightweight, portable NoSQL style barebone DBMS purely made in Python 3.8 with no additional dependencies (atleast for now). 
Suitable for simple use cases where you need NoSQL style I/O. 

P.S: It's more like a module than a standalone DBMS.

## Install 

To be honest, there's not much to install. It's more of a plug-and-play type thing. 

1. First create a database (or index - that's what men of culture call a NoSQL database). You can do it by creating a DB with .json format.
2. Open barebonesdb.py and edit the value of DB with the location of your DB file. 
3. Enjoy!

## Importing to your script (or project)

Just do `from <LOCATION> import barebonesdb`, where `<LOCATION>` is the location of the barebonesdb.py (either absolute, or relative to your working directory.)

## Some FAQs

What is it?
> BarebonesDB is a NoSQL style DBMS. Err... barebones of a NoSQL DBMS actually. 

What do I need to make it work?
> Only Python 3.x is needed. Just FYI, this has been made on Python 3.8

How do I work with it?
> Here's how:
1. To add data to your DB: `add <YOUR DICTIONARY>`. Example: `add {"name": "Anuran", "Github": "@anuran-roy"}`
2. To get data from yout DB: `get {"must": {<The dictionary of fields that you MUST want>}, "not": {{<The dictionary of fields that you DON'T want>}}}`. 
Example: `{"must": {"name": "Anuran"}, "not": {"Github": "@anuran-roy"}}` will give output "Not found" because there is no entry where name is Anuran and username is not "@anuran-roy" (until you specify it.)
	
A few tips:
> Don't make your dictionary too "deep", i.e, don't nest objects too much. It will slow down the lookup speed.

P.S: You can access the FAQ section from the BarebonesDB CLI when executing barebonesdb.py manually. Type `about` and you'll get it.

## **UPDATE** 

### Date: 29-4-2021

1. I have made a lot of changes to the architecture of BarebonesDB. Now you need to create an object (say, ob) and initialize the BarebonesDB class. 

Example Syntax:

`ob = BarebonesDB(on= "existing", name="db1", createTest=True)`

The above line initializes an instance of BarebonesDB class, with the flag to open an "existing" database of name "db1" on testing mode. In testing mode, a separate DB is created, so that you can carry out your testing there. The name of the test database is of the format `<database_name>_test.json`

2. Added a caching function of custom size. 

Example syntax: 

 `ob = BarebonesDB(on= "existing", name="db1", createTest=True, cacheSize=50)`

  The above line initializes an instance of BarebonesDB class, with the flag to open an "existing" database of name "db1" on testing mode, and cache size of 50 elements.

  YES, that's the fun part! You can now have variable cache sizes for different purposes!

  **For a simple test run, you can run execute test.py**
