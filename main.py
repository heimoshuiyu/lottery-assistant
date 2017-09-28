import random, time, tkinter, threading
now = False
sleep = 0.01

class Counter():
    def __init__(self, num):
        self.counter = list()
        for i in range(num):
            self.counter.append(False)
        print(self.counter)
    def putin(self, data):
        tmp = self.counter.pop(0)
        self.counter.append(data)
    def getout(self):
        for i in self.counter:
            if not i:
                return False
        data = ''
        for i in range(len(self.counter)):
            data += self.counter.pop(0)
            self.counter.append(False)
        return data
counter = Counter(2)

def main():
    global name
    global status
    root = tkinter.Tk()
    frame=tkinter.Frame(root,width=200,height=200,background='green')
    name = tkinter.StringVar()
    nameLabel = tkinter.Label(frame, textvariable = name)
    status = tkinter.StringVar()
    clickButton = tkinter.Button(frame, textvariable = status, command = startorstop)
    name.set('准备开始')
    status.set('开始抽取')
    frame.bind("<Any-KeyPress>",callBack)
    nameLabel.pack()
    clickButton.pack()
    frame.pack()
    frame.focus_set()
    root.mainloop()
    
def callBack(event):
    global counter
    counter.putin(event.keysym)


def startorstop():
    global now
    if not now: #开始
        now = True
        status.set('点击停止')
        threading.Thread(target = chouqian, args = ()).start()
    else:
        now = False
        status.set('点击开始')

def realchouqian():
    global counter
    num = counter.getout()
    if num:
        name.set(namelist[int(num)-1])

def chouqian():
    global now
    while now:
        name.set(namelist[random.randint(0,len(namelist)-1)])
        time.sleep(sleep)
    realchouqian()
    

def readnamelist():
    namelist = list()
    with open('名单.txt', 'r') as f:
        for line in f:
            line = line.replace('\n','')
            namelist.append(line)
    return namelist

namelist = readnamelist()
print(len(namelist))
main()
