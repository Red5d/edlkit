import os

class Edit(object):
    def __init__(self, time1, time2, action):
        self.time1 = str(time1)
        self.time2 = str(time2)
        self.action = str(action)
        
class EDL(object):
    def __init__(self, edlfile):
        self.edits = []
        self.edlfile = edlfile

        if os.path.exists(self.edlfile) == False:
            open(self.edlfile, 'a').close()
        else:
            with open(self.edlfile) as f:
                for line in f.readlines():
                    if len(line.split()) == 3:
                        self.edits.append(Edit(line.split()[0], line.split()[1], line.split()[2].split('\n')[0]))
                    elif len(line.split()) == 2:
                        self.edits.append(Edit(line.split()[0], line.split()[1], "-"))
                
    def sort(self):
        self.edits.sort(key=lambda x: float(x.time1))
                
    def save(self):
        self.sort()
        with open(self.edlfile, 'w') as f:
            for edit in self.edits:
                f.writelines(str(edit.time1)+"      "+str(edit.time2)+"      "+edit.action+"\n")
                
    def add(self, time1, time2, action):
        self.edits.append(Edit(time1, time2, action))
        self.sort()

        
