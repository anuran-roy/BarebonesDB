import json
from datetime import datetime
import time

dct = {}
queue = []
# DB = "./state_db.bbdb"  # For deployment
DB = "./state_db_test.bbdb"  # For testing

f = 0


def about():
    abt = open("about.txt").readlines()
    for a in abt:
        print(a)


def writest():
    try:
        global DB
        file = open(DB, "a")
        global queue
        for i in range(len(queue)):
            json.dump(queue[i], file)
            file.write("\n")
        print("Writing Queued State Object... OK")
        queue = []
    except Exception as wt:
        print(f"Failed to write Queued State Object to DB. Details: {wt}")


def threadqueue(t):
    '''Add the state to the thread queue'''
    global queue
    global f
    try:
        for i in queue:
            if i['module'] == t['module']:
                if i['timestamp'] == t['timestamp']:
                    f += 1
        if f > 0:
            print(f"{f} conflicting operation(s) from same module ", end="")
            print("at same time. Waiting 0.25s for each")
            time.sleep(0.25)
            queue.append(t)
        else:
            queue.append(t)
        print("State Object queuing... OK ")
    except Exception as tq:
        print(f"Failed to queue State Object. Error details:{tq}")


def makest(d):
    global dct
    dct = d

    try:
        dct['timestamp'] = str(datetime.now())
        dct['fields'] = list(dct.keys())
        print("State Object Creation... OK")
        threadqueue(dct)
        if __name__ != "__main__":
            return dct
    except Exception as mke:
        print(f"Failed to create state object. Error details:{mke}")


def readst(module=None, fromlast=1):
    global DB
    file = open(DB, "r")
    if module == "*":
        print(f"Printing {fromlast} most recent entries to the database:\n")
        for i in file.readlines()[-1*fromlast:]:
            print(json.dumps(json.loads(i), indent=4))
            print()
        return None
    else:
        f = 0
        for i in file.readlines()[::-1]:
            dump = json.loads(i)
            if dump['module'] == module and f == fromlast-1:
                if __name__ == '__main__':
                    print(json.dumps(json.loads(i), indent=4))
                return dump
            elif dump['module'] == module and f < fromlast-1:
                f += 1
        if __name__ == '__main__':
            print("Not Found")
        return "Not Found."


def search(criteria, mode="get"):
    try:
        q = open(DB, "r").readlines()
        q2 = []
        cf = list(criteria.keys())

        must_keys = (criteria["must"].keys()) if "must" in cf else []
        # may_keys = (criteria["may"].keys()) if "may" in cf else []
        not_keys = (criteria["not"].keys()) if "not" in cf else []

        line2 = []
        c = 0
        c2 = 0
        for i in range(len(q)):
            qk = list(json.loads(q[i]).keys()) if q[i] != "\n" else []
            if set(not_keys).issubset(set(qk)):
                for nt in not_keys:
                    if criteria["not"][nt] == json.loads(q[i])[nt]:
                        c += 1
                if c == 0:
                    q2.append(q[i])
            c = 0

        i = 0
        for i in range(len(q2)):
            qk2 = list(json.loads(q2[i]).keys())

            if set(must_keys).issubset(set(qk2)):
                for mst in must_keys:
                    if criteria["must"][mst] == json.loads(q2[i])[mst]:
                        c2 += 1
                if c2 == len(must_keys):

                    if mode == "get":
                        line2.append(json.loads(q2[i]))
                    elif mode == "delete":
                        line2.append(i)
                c2 = 0
        if len(line2) > 0:
            for l in line2:
                if mode == "get":
                    print(json.dumps(l, indent=4))
                # elif mode == "delete":
                #     print(l)
            if mode == "delete":
                return line2
        else:
            print("Not found.")
            return []
    except Exception as ex:
        print(f"An error occured while getting must fields. Details: {ex}")


def remove(criteria):
    lef = open(DB, "r").readlines()
    entries_affected = [lef[i] for i in search(criteria, mode="delete")]
    if __name__ == "__main__":
        print(f"Deleting {len(entries_affected)} entries. Proceed? [Y/N]", end=" ")
    resp = input() if __name__ == "__main__" else "Y"
    if resp == "Y" or resp == "y":
        e = list(set(lef) - set(entries_affected))
        ef = open(DB, "w")
        try:
            for i in e:
                ef.writelines(i)

        except Exception as ex:
            print(f"\nAn error occured. Details: {ex}\n")
    else:
        print("\nDelete operation aborted.\n")


if __name__ == "__main__":
    from os import system, name
    if name == "nt":
        _ = system('cls')
    else:
        _ = system('clear')
    while True:
        try:
            cd = input("[BarebonesDB] > ").strip()
            if cd.lower() == "clear" or cd.lower() == "cls":
                if name == "nt":
                    _ = system('cls')
                else:
                    _ = system('clear')
            elif cd.lower() in ["exit", "quit", "close", "bye"]:
                print("Exiting...\n")
                break
            elif cd[:cd.find(" ")].lower() == "delete":
                cmd = ["delete", json.loads(cd[cd.find(" ")+1:])]
                remove(cmd[1])
            elif cd[:cd.find(" ")].lower() == "get":
                if cd[-1] != "}":
                    cmd = cd.split(" ")
                    if len(cmd) == 1:
                        mod = input(" > Enter module name: ")
                        fl = input(" > Enter the k-th last index: ")
                    elif len(cmd) == 2:
                        mod = cmd[1]
                        fl = "1"
                    elif len(cmd) == 3:
                        mod = cmd[1]
                        fl = cmd[2]
                    else:
                        print("[BarebonesDB] > Invalid command! Try again!")
                        continue
                    try:
                        if fl.isnumeric():
                            fl = int(fl)
                        else:
                            fl = 1
                        readst(module=mod, fromlast=fl)
                    except KeyboardInterrupt:
                        print("\nExecution interrupted from Keyboard. Bye...")
                        break
                    except Exception as e:
                        print(f"\nAn exception occured. Details: {e}")
                else:
                    cmd = [cd[:cd.find(" ")], json.loads(cd[cd.find(" ")+1:])]
                    search(cmd[1], mode="get")
            elif cd[:cd.find(" ")].lower() == "add":
                cmd = [cd[:cd.find(" ")], cd[cd.find(" ")+1:]]
                if len(cmd) == 1:
                    s = input("[BarebonesDB] > Enter JSON String:  ").rstrip()
                elif len(cmd) == 2:
                    s = cmd[1]
                else:
                    print(len(cmd))
                    print(cmd)
                    print("Invalid Syntax. Please check and try again.")
                    continue
                try:
                    jdict = json.loads(s)

                    makest(jdict)
                    writest()
                except json.JSONDecodeError as j:
                    print("Error while parsing the JSON String.", end="")
                    print(f"Details: {j.msg}")
                    print(f"Error encountered at: {j.pos}", end="")
                    print(f" at line {j.lineno} column {j.colno}")
                except Exception as e:
                    print(f"Error while parsing the JSON String. Details: {e}")
            elif cd == "":
                continue
            elif cd.lower() == "about":
                about()
            else:
                print(f"{cd} is not recognized by BarebonesDB. Try again.")

            print("\n")
        except KeyboardInterrupt:
            print("\nExecution interrupted from Keyboard. Exiting...")
            break
        except Exception as E:
            print(f"A Fatal Error was encountered. Error details: {E}")
            continue
