import random, time, tkinter, threading
now = False
sleep = 0.01

def main():
    global name
    global status
    root = tkinter.Tk()
    name = tkinter.StringVar()
    nameLabel = tkinter.Label(root, textvariable = name)
    status = tkinter.StringVar()
    clickButton = tkinter.Button(root, textvariable = status, command = startorstop)
    name.set('准备开始')
    status.set('开始抽取')
    nameLabel.pack()
    clickButton.pack()
    root.mainloop()

def startorstop():
    global now
    if not now:
        now = True
        threading.Thread(target = chouqian, args = ()).start()
    else:
        now = False

def chouqian():
    global now
    while now:
        name.set(namelist[random.randint(0,len(namelist)-1)])
        time.sleep(sleep)
    

def readnamelist():
    namelist = list()
    with open('名单.txt', 'r') as f:
        for line in f:
            line = line.replace('\n','')
            namelist.append(line)
    return namelist

namelist = readnamelist()
main()
