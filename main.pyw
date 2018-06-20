import random
import time
import tkinter
import threading
import json
import hashlib
import dbm
try:
    import playsound
except:
    pass
import winsound



now = False
sleep = 0.01

class Database():
    def __init__(self, namelist):
        md5 = hashlib.md5()
        md5data = json.dumps(namelist)
        md5.update(md5data.encode('utf-8'))
        self.namehash = md5.hexdigest()
        self.database = dbm.open('database-%s'%self.namehash, 'c')
        for name in namelist:
            if not self.database.get(name):
                self.database[name] = str(0)
    def get(self, maxrange):
        min = self.getminnum()
        max = min + maxrange
        resultnamelist = self.getrangedict(min, max)
        randomindex = random.randint(0, len(resultnamelist) - 1)
        if qianzhi.get() == 1:
            self.count(resultnamelist[randomindex])
        return resultnamelist[randomindex]
    def getminnum(self):
        first = True
        for name in self.database:
            index = self.database[name]
            index = int(index)
            if first:
                min = index
                first = False
                continue
            if index < min:
                min = index
        return min
    def getrangedict(self, min, max):
        resultnamelist = []
        for name in self.database:
            index = self.database[name]
            index = int(index)
            if index >= min and index <= max:
                resultnamelist.append(name.decode('utf-8'))
        print(resultnamelist)
        return resultnamelist
    def count(self, name):
        name = name.encode('utf-8')
        before = self.database[name]
        now = int(before) + 1
        now = str(now)
        self.database[name] = now



class Counter():
    def __init__(self, num):
        self.counter = list()
        for i in range(num):
            self.counter.append(False)
    def putin(self, data):
        tmp = self.counter.pop(0)
        self.counter.append(data)
    def getout(self):
        for i in self.counter:
            if not i:
                return False
        for i in self.counter:
            try:
                tmp = int(i)
            except:
                return False
        data = ''
        for i in range(len(self.counter)):
            data += self.counter.pop(0)
            self.counter.append(False)
        return data

def show_setting():
    setting_window = tkinter.Tk()
    sleep_time_label = tkinter.Label(setting_window, text='间隔时间（毫秒）')
    sleep_time_label.grid(column=0, row=0)
    sleep_time = tkinter.StringVar()
    sleep_time_entry = tkinter.Entry(setting_window, textvariable=sleep_time)
    setting_window.mainloop()


def main():
    global name, status, tipsString, jsondata, root, qianzhi, root
    root = tkinter.Tk()
    root.title('抽签助手')
    #root.maxsize(600, 400)    #窗口大小
    #root.minsize(300, 240)
    #frame=tkinter.Frame(root,width=300,height=240,background='green')  #容器
    frame = tkinter.Frame(root, width=300, height=240)
    name = tkinter.StringVar()
    nameLabel = tkinter.Label(frame,textvariable=name,width=10,height=4)
    #nameLabel.config(font = 'Helvetica -78 bold')
    nameLabel.config(font = '微软雅黑 -78 bold')
    status = tkinter.StringVar()
    clickButton = tkinter.Button(frame,textvariable=status,command=startorstop)
    name.set('准备开始')
    status.set('开始抽取')
    frame.bind("<Any-KeyPress>",callBack)
    nameLabel.grid(column = 0, row = 0, columnspan = 3)
    clickButton.grid(column = 0, row = 1, columnspan=3)
    tipsString = tkinter.StringVar()
    tipsLabel = tkinter.Label(frame, textvariable = tipsString)
    tipsString.set('名单列表里共有%s个名字，没有重复'%len(namelist))
    tipsLabel.grid(column = 0, row = 2)
    qianzhi = tkinter.IntVar()
    check1 = tkinter.Checkbutton(frame, text = '无重复模式', variable=qianzhi)
    qianzhi.set(1)
    setButton = tkinter.Button(frame, text = '设置', command=show_setting)
    setButton.grid(column = 2, row = 2)
    check1.grid(column = 1, row = 2)
    frame.grid(column = 0, row = 0)
    frame.focus_set()
    root.mainloop()

def readjson():
    with open('config.json', 'rb') as f:
        data = f.read().decode('utf-8')
        jsondata = json.loads(data)
        return jsondata

def writejson(jsondata):
    jsondata = str(jsondata)
    with open('config.json', 'w') as f:
        f.write(jsondata)

def check_forever():
    while True:
        time.sleep(0.01)
        print(qianzhi.get())

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
    global counter, database, qianzhi
    if qianzhi.get() == 1:
        maxrange = jsondata['range'] - 1
        resultname = database.get(maxrange)
        name.set(resultname)
    num = counter.getout()
    if num:
        name.set(namelist[int(num)-1])

sum = 1
y = 0
def chouqian():
    global now, tipsString, namelist, sum, y, jsondata
    while now:
        randnum = random.randint(0,len(namelist)-1)
        sum += 1
        if randnum == 0:
            y += 1
        name.set(namelist[randnum])
        #tipsString.set('每人被抽到的理论概率为%s，实际概率为%s'%(round(1/len(namelist)*100,5), round((y/sum)*100,4)))
        tipsString.set('抽签助手Ver1.4 内置数据库记录 打死都不会重复的版本')
        time.sleep(jsondata['sleep'])
    realchouqian()
    

def readnamelist():
    namelist = list()
    with open('名单.txt', 'r') as f:
        for line in f:
            line = line.replace('\n','')
            if line:
                namelist.append(line)
    return namelist

namelist = readnamelist()
database = Database(namelist)
jsondata = readjson()
def playmp3():
    print(jsondata['mp3file'])
    playsound.playsound(jsondata['mp3file'])
threading.Thread(target = playmp3, args = (),daemon = True).start()
counter = Counter(len(str(len(namelist))))
main()
