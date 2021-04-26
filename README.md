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
