class Menu:
    def __init__(self, title, parent):
        self.title = title
        self.choices = []
        self.parent = parent
        self.pos = 0
        self.top = 0

    def getParent(self):
        return self.parent        

    def addEntry(self, desc, action):
        self.choices.append(Choice(desc, action))
        
    def getSize(self):
        return len(self.choices)
        
    def checkPos(self, pos):
        return (pos >= 0) and (pos < self.getSize())
        
    def choose(self, pos):
        return self.choices[pos].getAction()
            
    def printmenu(self):
        print(self.title)
        for x in range(self.getSize()):
            print("{}: {}" .format(x+1, self.choices[x].getDesc()))

    def getLines(self):
        lines = []
        for x in range(self.getSize()):
            lines.append(self.choices[x].getDesc())
        return lines

    def getVisibleLines(self):
        lines = []
        x = self.top
        while x < self.top + 5 and x < self.getSize():
            lines.append(self.choices[x].getDesc())
            x += 1
        return lines

    def getVisiblePos(self):
        return self.pos - self.top
        
    def getTitle(self):
        return self.title

    def getPos(self):
        return self.pos
    
    def up(self):
        if self.pos > 0:
            self.pos -= 1
            if self.pos < self.top:
                self.top -= 1
            
    def down(self):
        if self.pos < self.getSize() - 1:
            self.pos += 1
            if self.pos > self.top + 4:
                self.top += 1

    def select(self):
        return self.choices[self.pos].getAction()

class Choice:
    def __init__(self, desc, action):
        self.desc = desc
        self.action = action
       
    def getDesc(self):
        return self.desc
        
    def getAction(self):
        return(self.action)
        
    def printDesc(self):
        print(self.desc)
