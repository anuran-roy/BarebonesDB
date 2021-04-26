# BarebonesDB

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
1. To add data to your DB: 
`add <YOUR DICTIONARY>`. 

Example: `add {"name": "Anuran", "Github": "@anuran-roy"}`

2. To get data from yout DB: 
`get {"must": {<The dictionary of fields that you MUST want>}, "not": {{<The dictionary of fields that you DON'T want>}}}`. 

Example: `{"must": {"name": "Anuran"}, "not": {"Github": "@anuran-roy"}}` will give output "Not found" because there is no entry where name is Anuran and username is not "@anuran-roy" (until you specify it.)
	
A few tips:
> Don't make your dictionary too "deep", i.e, don't nest objects too much. It will slow down the lookup speed.

P.S: You can access the FAQ section from the BarebonesDB CLI when executing barebonesdb.py manually. Type `about` and you'll get it.
