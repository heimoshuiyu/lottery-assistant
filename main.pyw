### 代码不规范
### 没事就不要瞎看
### 背景BGM功能还没完善
### 也不打算完善
### qwq



import random
import time
import tkinter
import threading
import os
import os.path
import json
import hashlib


now = False
sleep = 0.01 # 抽签动画闪动时间间隔


class Database:
    def __init__(self, namelist):
        md5 = hashlib.md5()  # 根据名单生成md5，打开对应的数据库
        md5data = json.dumps(namelist)
        md5.update(md5data.encode('utf-8'))
        self.namehash = md5.hexdigest()
        self.database = {}
        self.filename = 'database-%s.json' % self.namehash
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                json_raw_data = f.read()
            self.database = json.loads(json_raw_data)
        for name in namelist:
            if not self.database.get(name):
                self.database[name] = str(0)

    def get(self, maxrange):  # 返回被抽中次数较少的名单列表
        min = self.getminnum()
        max = min + maxrange
        resultnamelist = self.getrangedict(min, max)
        randomindex = random.randint(0, len(resultnamelist) - 1)
        if qianzhi.get() == 1:
            self.count(resultnamelist[randomindex])
        return resultnamelist[randomindex]

    def getminnum(self):  # 返回数据库中的最小数字
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

    def getrangedict(self, min, max):  # 返回指定范围的名单列表
        resultnamelist = []
        for name in self.database:
            index = self.database[name]
            index = int(index)
            if index >= min and index < max:
                resultnamelist.append(name)
        print(resultnamelist)
        return resultnamelist

    def count(self, name):  # 使数据库中指定名字的次数+1
        before = self.database[name]
        now = int(before) + 1
        now = str(now)
        self.database[name] = now
        self.write_database()

    def write_database(self):  # 保存数据
        json_raw_data = json.dumps(self.database)
        with open(self.filename, 'w') as f:
            f.write(json_raw_data)


class Counter:  # 键盘记录器类，先进先出方式记录键盘按键
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
                tmp = int(i)  # 返回键盘按下的数字，其他情况全部返回False
            except:
                return False
        data = ''
        for i in range(len(self.counter)):
            data += self.counter.pop(0)
            self.counter.append(False)
        return data

is_setting_open = False
def show_setting():  # 想弄个设置窗口，太麻烦算了 ###又不是不能用.jpg###
    global setting_window, is_setting_open, sleep_time_entry, range_entry, status_text
    if is_setting_open:
        return
    else:
        is_setting_open = True
    setting_window = tkinter.Tk()
    sleep_time_label = tkinter.Label(setting_window, text='动画间隔时间（秒）：')
    sleep_time_label.grid(column=0, row=0)
    sleep_time_entry = tkinter.Entry(setting_window)
    sleep_time_entry.insert(0, str(jsondata['sleep']))
    sleep_time_entry.grid(column=1, row=0)
    sleep_time_support_label = tkinter.Label(
        setting_window,
        text = '按下抽签按钮后，屏幕上名字闪动间隔的时间',
        wraplength = 390,
        justify = 'left'
    )
    sleep_time_support_label.grid(column=0, columnspan=2, row=1)
    range_label = tkinter.Label(setting_window, text='重复许可范围：')
    range_label.grid(column=0, row=2)
    range_entry = tkinter.Entry(setting_window)
    range_entry.insert(0, str(jsondata['range']))
    range_entry.grid(column=1, row=2)
    range_support_label = tkinter.Label(
        setting_window,
        text = '程序会统计名单中所有人被抽中的次数，次数最高和最低人不能超过这个范围，如果名单中有人统计次数过超出高出这个范围'
        '则下一轮系统不会抽取此人。例如名单中有张三、李四、王五，重复许可范围设置为0，第一轮抽签抽到李四，李四的统计次数为1，'
        '其他人为0，李四超出了重复许可范围，所以在下一轮抽签中李四不可能被抽中，直到张三、王五被抽到之后。',
        wraplength = 390,
        justify = 'left'
    )
    range_support_label.grid(column=0, columnspan=2, row=3)
    save_buttom = tkinter.Button(setting_window, command=save_setting, text='保存')
    save_buttom.grid(column=0, columnspan=2, row=4)
    setting_window.protocol('WM_DELETE_WINDOW', exit_setting)  # 绑定自定义退出函数，确保只有一个setting_windows打开
    status_text = tkinter.StringVar(setting_window)
    status_label = tkinter.Label(setting_window, wraplength=390, textvariable=status_text)
    status_label.grid(column=0, columnspan=2, row=5)
    about_label = tkinter.Label(setting_window, text='项目开源地址：https://github.com/heimoshuiyu/lottery-assistant')
    about_label.grid(column=0, columnspan=2, row=6)
    setting_window.mainloop()
    is_setting_open = False

def exit_setting():
    global is_setting_open, setting_window
    is_setting_open = False
    setting_window.destroy()

def save_setting():
    global status_text
    try:
        sleep_time = float(sleep_time_entry.get())
        range_value = int(range_entry.get())
    except:
        status_text.set('输入的数据不合法，请检查（不要输入多余的空格或其它字符）')
        return
    jsondata['sleep'] = sleep_time
    jsondata['range'] = range_value
    raw_jsondata = json.dumps(jsondata)
    with open('config.json', 'w') as f:
        f.write(raw_jsondata)
    status_text.set('设置保存成功')

def main():  # 就是主函数和窗口排版，不想加注释了，好乱QAQ
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
    tipsString.set('抽签助手V1.5，名单列表里共有%s个名字'%len(namelist))
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

def readjson(): # 读取配置文件返回字典, jsondata是全局用的哦（逃
    with open('config.json', 'rb') as f:
        data = f.read().decode('utf-8')
        jsondata = json.loads(data)
        return jsondata

def writejson(jsondata):  # 写配置文件
    jsondata = str(jsondata)
    with open('config.json', 'w') as f:
        f.write(jsondata)

def check_forever():
    while True:
        time.sleep(0.01)
        print(qianzhi.get())

def callBack(event):  # 键盘记录器关键函数
    global counter
    counter.putin(event.keysym)

def startorstop():  # 绑定按钮用的函数，执行一次开始，再执行一次停止，靠now判断当前是否再运行
    global now
    if not now:  # 开始
        now = True
        status.set('点击停止')
        threading.Thread(target = chouqian, args = ()).start()
    else:
        now = False
        status.set('点击开始')

def realchouqian():  # 真正的抽签函数，抽签动画停止后立即执行realchouqian，
    global counter, database, qianzhi
    if qianzhi.get() == 1:  # 判断无重复模式勾选框是否勾选
        maxrange = jsondata['range']  # 从数据库中弄一个次数较少的名字粗来
        resultname = database.get(maxrange)
        name.set(resultname)  # 把抽到的名字秒变数据库中抽到的名字
    num = counter.getout() # 从键盘记录器调取输入的编号
    if num:
        name.set(namelist[int(num)-1])  # 从键盘记录器读取序号，设置名字，达到作弊效果

sum = 1
y = 0
def chouqian(): # 抽签主函数
    global now, tipsString, namelist, sum, y, jsondata
    while now:
        randnum = random.randint(0,len(namelist)-1)
        sum += 1
        if randnum == 0:
            y += 1
        name.set(namelist[randnum])
        #tipsString.set('每人被抽到的理论概率为%s，实际概率为%s'%(round(1/len(namelist)*100,5), round((y/sum)*100,4)))
        time.sleep(jsondata['sleep'])
    realchouqian() # 正常抽签后，执行一次真的抽签函数覆盖结果
    

def readnamelist(): # 读取名单，按行分割，返回列表
    namelist = list()
    with open('名单.txt', 'rb') as f:
        raw_str = f.read()
    try:
        raw_str = raw_str.decode('utf-8')
    except:
        try:
            raw_str = raw_str.decode('gb2312')
        except:
            return ['名单.txt文件解码错误，请使用UTF-8或GB2312编码']
    raw_str = raw_str.replace('\r','')
    _namelist = raw_str.split('\n')
    for name in _namelist:
        if name:
            namelist.append(name)
    return namelist

namelist = readnamelist()
database = Database(namelist)
jsondata = readjson()
counter = Counter(len(str(len(namelist))))
main()  # 执行主函数
