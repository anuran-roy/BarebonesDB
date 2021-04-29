import json
from datetime import datetime
import time
import os


class DBNameUnavailable(Exception):
    pass


class BarebonesDB:

    def __init__(self, on="new", name=None, createTest=True, cacheSize=100):
        self.dct = {}
        self.queue = []
        self.cache = {}
        self.cacheSize = cacheSize
        self.f = 0
        self.name = name
        try:
            if on == "new":
                if self.name is None:
                    self.name = f'db-{datetime.now().strftime("%H-%M-%S-%d-%m-%Y")}'
                self.nm = f"{os.path.realpath('.')}\\{self.name}"
                os.mkdir(self.nm)
                if createTest:
                    self.DB = f"{self.nm}\\{self.name}_test.json"
                else:
                    self.DB = f"{self.nm}\\{self.name}.json"
                file = open(self.DB, "w")
                file.close()
            elif on.lower().strip() == "existing" and len(self.name.strip()) > 0:
                if createTest:
                    self.DB = f"{os.path.realpath('.')}\\{self.name}\\{self.name}_test.json"
                else:
                    self.DB = f"{os.path.realpath('.')}\\{self.name}\\{self.name}.json"
                if __name__ == "__main__":
                    print(f"DB instance is now pointing to {self.DB}")
            elif len(self.name.strip()) == 0:
                raise DBNameUnavailable
        except DBNameUnavailable:
            print("Please specify name of an existing DB. ")
        except Exception as e:
            print(f"FATAL ERROR during initialization! Error details: {e}")

    def about(self):
        abt = open("about.txt").readlines()
        for a in abt:
            print(a)

    def doCache(self, entry):
        if "".join(list(entry.keys())) not in list(self.cache.keys()):
            self.cache["".join(list(entry.keys()))
                       ] = entry["".join(list(entry.keys()))]
        if len(list(self.cache.keys())) > self.cacheSize:
            self.cache.pop(list(self.cache.keys())[0])

    def writest(self):
        try:
            file = open(self.DB, "a")
            for i in range(len(self.queue)):
                json.dump(self.queue[i], file)
                file.write("\n")
            if __name__ == "__main__":
                print("Writing Queued State Object... OK")
            self.queue = []
        except Exception as wt:
            print(
                f"Failed to write Queued State Object to DB. Details: {wt.message}")

    def threadqueue(self, t):
        '''Add the state to the thread queue'''
        try:
            for i in self.queue:
                if i['module'] == t['module']:
                    if i['timestamp'] == t['timestamp']:
                        self.f += 1
            if self.f > 0:
                print(f"{self.f} operation conflict(s) from same module ", end="")
                print("at same time. Waiting 0.25s for each.")
                time.sleep(0.25)
                self.queue.append(t)
            else:
                self.queue.append(t)
            if __name__ == "__main__":
                print("State Object queuing... OK ")
        except Exception as tq:
            print(f"Failed to queue State Object. Error details:{tq.message}")

    def makest(self, d):
        self.dct = d

        try:
            self.dct['timestamp'] = str(datetime.now())
            # self.dct.pop('dct')
            self.dct['fields'] = list(self.dct.keys())
            print("State Object Creation... OK")
            self.threadqueue(self.dct)
            if __name__ != "__main__":
                return self.dct
        except Exception as mke:
            print(
                f"Failed to create state object. Error details:{mke.message}")

    def readst(self, module=None, fromlast=1):
        file = open(self.DB, "r")
        if module == "*":
            print(f"Printing {fromlast} most recent entries to database:\n")
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

    def search(self, criteria, mode="get"):
        try:
            if f"{mode} {criteria}" in list(self.cache.keys()):
                return self.cache[criteria]
            else:
                q = open(self.DB, "r").readlines()
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
                    if mode == "get" and __name__ == "__main__":
                        for l in line2:
                            print(json.dumps(l, indent=4))
                        # elif mode == "delete":
                        #     print(l)
                    else:
                        self.doCache({str(criteria): line2})
                        return line2
                else:
                    if __name__ == "__main__":
                        print("Not found.")
                    self.doCache({f"{mode} {criteria}": line2})
                    return []
        except Exception as ex:
            print(
                f"An error occured while getting must fields. Details: {ex.message}")

    def remove(self, criteria):
        lef = open(self.DB, "r").readlines()
        entries_affected = [lef[i]
                            for i in self.search(criteria, mode="delete")]
        if __name__ == "__main__":
            print(
                f"Deleting {len(entries_affected)} entries. Proceed? [Y/N]", end=" ")
        resp = input() if __name__ == "__main__" else "Y"
        if resp == "Y" or resp == "y":
            e = list(set(lef) - set(entries_affected))
            ef = open(self.DB, "w")
            try:
                for i in e:
                    ef.writelines(i)

            except Exception as ex:
                print(f"\nAn error occured. Details: {ex.message}\n")
        else:
            print("\nDelete operation aborted.\n")

    def saveobj(self):
        try:
            self.__dict__.pop("dct")
            sdict = self.makest(self.__dict__)
            savepath = f"{os.path.realpath('.')}\\{self.name}\\state.json"
            file = open(savepath, "w")
            file.writelines(json.dumps(sdict))
        except Exception as serr:
            print(
                f"An error was encountered while saving the object. Details: {serr.message}")

    def switchdb(self, db_name, test=True, clearQueue=True, clearCache=True, cacheSize=100, writechanges=False):
        '''
        This method is not recommmended, since it bypasses a lot of methodical operations and is is intended to be a last-resort dirty fix
        to unavoidable problems, should such a dire need arise. Note that it may result in redundant data across databases. So please be 
        careful. Also using it regularly is against the principle of BarebonesDB, that is: One object for one DB.
        '''
        try:
            self.name = db_name
            self.cacheSize = cacheSize
            if writechanges:
                self.writest()
                self.cache = {}
            if clearCache:
                self.cache = {}
            if clearQueue:
                self.queue = []
            if test:
                self.DB = f"{os.path.realpath('.')}\\{self.name}\\{self.name}_test.json"
            else:
                self.DB = f"{os.path.realpath('.')}\\{self.name}\\{self.name}.json"
            if __name__ == "__main__":
                print(f"DB instance is now pointing to {self.DB}")
        except Exception as e:
            print(f"An error occured while changing DB pointer. Details: {e.message}")

    def resumeobj(self, state_file):
        try:
            file = json.loads(open(state_file, "r").readlines())
        except Exception as ex:
            print(f"An error occured while trying to load the state from the state file. Details: {ex.message}")


if __name__ == "__main__":
    from os import system, name
    cache = 100
    nm = None
    test = "True"
    o = "new"

    def makeobj():
        global o, cache, test, nm
        o = input("Make new DB instance or use existing? (default: new) > ").strip()
        if o == "":
            o = "new"
        nm = input("Enter DB name > ").strip()
        if nm == "":
            nm = None
        cache = input(
            "Enter cache size (number of elements). default: 100 > ").strip()
        if cache == "":
            cache = 100
        test = input(
            "Enable Test Database? (True/False) default: True > ").strip()
        if test.lower() == "true" or test == "":
            test = True
        else:
            test = False

    try:
        makeobj()
        global ob
        ob = BarebonesDB(on=o, createTest=test, name=nm, cacheSize=int(cache))

        # if name == "nt":
        #     _ = system('cls')
        # else:
        #     _ = system('clear')
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
                    ob.remove(cmd[1])
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
                            ob.readst(module=mod, fromlast=fl)
                        except KeyboardInterrupt:
                            print("\nExecution interrupted from Keyboard. Bye...")
                            break
                        except Exception as e:
                            print(
                                f"\nAn exception occured. Details: {e.message}")
                    else:
                        cmd = [cd[:cd.find(" ")], json.loads(
                            cd[cd.find(" ")+1:])]
                        ob.search(cmd[1], mode="get")
                elif cd[:cd.find(" ")].lower() == "add":
                    cmd = [cd[:cd.find(" ")], cd[cd.find(" ")+1:]]
                    if len(cmd) == 1:
                        s = input(
                            "[BarebonesDB] > Enter JSON String:  ").rstrip()
                    elif len(cmd) == 2:
                        s = cmd[1]
                    else:
                        print(len(cmd))
                        print(cmd)
                        print("Invalid Syntax. Please check and try again.")
                        continue
                    try:
                        jdict = json.loads(s)

                        ob.makest(jdict)
                        ob.writest()
                    except json.JSONDecodeError as j:
                        print("Error while parsing the JSON String.", end="")
                        print(f"Details: {j.msg}")
                        print(f"Error encountered at: {j.pos}", end="")
                        print(f" at line {j.lineno} column {j.colno}")
                    except AttributeError:
                        print(
                            "Attribute Error triggered from makest() or writest(). Cannot get attribute.")
                    except Exception as e:
                        print(
                            f"Error while parsing the JSON String. Details: {e.message}")
                elif cd == "":
                    continue
                elif cd.lower() == "about":
                    ob.about()
                else:
                    print(f"{cd} is not recognized by BarebonesDB. Try again.")

                print("\n")
            except KeyboardInterrupt:
                print("\nExecution interrupted from Keyboard. Exiting...")
                break
            except Exception as E:
                print(f"A Serious Error was encountered. Error details: {E}")
                continue
    except Exception as err:
        print(
            f"Fatal Error while initializing Database Instance. BarebonesDB can't start. Details: {err}")
