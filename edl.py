class reader(object):

    def __init__(self, edlfile):
        self.edlfile = edlfile

    def read(self):
        print self.edlfile.read()


class struct(object):

    def __init__(self, edlfile):
        self.edlfile = edlfile
        self.time1 = list()
        self.time2 = list()
        self.action = list()

        for line in self.edlfile:
             if len(line.split()) == 3:
                 self.time1.append(line.split()[0])
                 self.time2.append(line.split()[1])
                 self.action.append(line.split()[2].split('\n')[0])
             elif len(line.split()) == 2:
                 self.time1.append(line.split()[0])
                 self.time2.append(line.split()[1])
                 self.action.append("-")


class writer(object):

    def __init__(self, edlfile):
        self.edlfile = edlfile

    def writeline(self, time1, time2, action):
        self.time1 = time1
        self.time2 = time2
        self.action = action
        
        self.edlfile.write(str(time1)+"      "+str(time2)+"      "+str(action))
        
    def write_struct(self, estruct):
        self.time1 = estruct.time1
        self.time2 = estruct.time2
        self.action = estruct.action
            
        for x in range(0, len(self.time1)):
            if self.action[x] == "-":
                self.action[x] = ""
                
            self.edlfile.write(str(self.time1[x])+"      "+str(self.time2[x])+"      "+str(self.action[x])+"\n")
        
        
