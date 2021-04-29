from barebonesdb import BarebonesDB as bbdb
import barebonesdb
d = "db1"  # Replace with the DB name you want to access

ob = bbdb(on="existing", name=d, createTest=True, cacheSize=50)  # Adjust the parameters as you wish

# Write your code below.
print([str(l) for l in ob.__dir__() if (not callable(getattr(ob, l)) and str(l)[0]!="_")])
l = ob.search({"must": {"module": "Facebook"}})
_ = print(l) if len(l) > 0 else print("Not found")