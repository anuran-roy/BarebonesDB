from barebonesdb import BarebonesDB as bbdb

d = "db1"  # Replace with the DB name you want to access

ob = bbdb(on="existing", name=None, createTest=True, cacheSize=50)  # Adjust the parameters as you wish

# Write your code below.
l = ob.search({"must": {"module": "Facebook"}})
print(l)
