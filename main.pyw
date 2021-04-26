import random
import time
import tkinter
import threading
import os
import os.path
import json
import hashlib


def main():
    mainWindow = MainWindow()
    mainWindow.mainloop()


class Database:
    def __init__(self, namelist, norepeat):
        self.norepeat = norepeat
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
        if self.norepeat.get() == 1:
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
        for _ in range(num):
            self.counter.append(False)

    def putin(self, data):
        self.counter.pop(0)
        self.counter.append(data)

    def getout(self):
        for i in self.counter:
            if not i:
                return False
        for _ in self.counter:
            try:
                int(i)  # 返回键盘按下的数字，其他情况全部返回False
            except:
                return False
        data = ''
        for _ in range(len(self.counter)):
            data += self.counter.pop(0)
            self.counter.append(False)
        return data


class SettingWindow:
    def __init__(self, parent):
        self.parent = parent
        self.setting_window = tkinter.Tk()
        self.sleep_time_label = tkinter.Label(
            self.setting_window, text='动画间隔时间（秒）：')
        self.sleep_time_label.grid(column=0, row=0)
        self.sleep_time_entry = tkinter.Entry(self.setting_window)
        self.sleep_time_entry.insert(0, str(self.parent.jsondata['sleep']))
        self.sleep_time_entry.grid(column=1, row=0)
        self.sleep_time_support_label = tkinter.Label(
            self.setting_window,
            text='按下抽签按钮后，屏幕上名字闪动间隔的时间',
            wraplength=390,
            justify='left'
        )
        self.sleep_time_support_label.grid(column=0, columnspan=2, row=1)
        self.range_label = tkinter.Label(self.setting_window, text='重复许可范围：')
        self.range_label.grid(column=0, row=2)
        self.range_entry = tkinter.Entry(self.setting_window)
        self.range_entry.insert(0, str(self.parent.jsondata['range']))
        self.range_entry.grid(column=1, row=2)
        self.range_support_label = tkinter.Label(
            self.setting_window,
            text='程序会统计名单中所有人被抽中的次数，次数最高和最低人不能超过这个范围，如果名单中有人统计次数过超出高出这个范围'
            '则下一轮系统不会抽取此人。例如名单中有张三、李四、王五，重复许可范围设置为0，第一轮抽签抽到李四，李四的统计次数为1，'
            '其他人为0，李四超出了重复许可范围，所以在下一轮抽签中李四不可能被抽中，直到张三、王五被抽到之后。',
            wraplength=390,
            justify='left'
        )
        self.range_support_label.grid(column=0, columnspan=2, row=3)
        self.save_buttom = tkinter.Button(
            self.setting_window, command=self.save_setting, text='保存')
        self.save_buttom.grid(column=0, columnspan=2, row=4)
        # 绑定自定义退出函数，确保只有一个setting_window打开
        self.setting_window.protocol('WM_DELETE_WINDOW', self.exit_setting)
        self.status_text = tkinter.StringVar(self.setting_window)
        self.status_label = tkinter.Label(
            self.setting_window, wraplength=390, textvariable=self.status_text)
        self.status_label.grid(column=0, columnspan=2, row=5)
        self.about_label = tkinter.Label(
            self.setting_window, text='项目开源地址：https://github.com/heimoshuiyu/lottery-assistant')
        self.about_label.grid(column=0, columnspan=2, row=6)
        self.setting_window.mainloop()

    def exit_setting(self):
        self.parent.is_setting_open = False
        self.setting_window.destroy()

    def save_setting(self):
        try:
            sleep_time = float(self.sleep_time_entry.get())
            range_value = int(self.range_entry.get())
        except:
            self.status_text.set('输入的数据不合法，请检查（不要输入多余的空格或其它字符）')
            return
        self.parent.jsondata['sleep'] = sleep_time
        self.parent.jsondata['range'] = range_value
        raw_jsondata = json.dumps(self.parent.jsondata)
        with open('config.json', 'w') as f:
            f.write(raw_jsondata)
        self.status_text.set('设置保存成功')


class MainWindow():
    def __init__(self):
        # 根据 now 判断抽签是否正在运行
        self.now = False

        self.jsondata = {}
        self.is_setting_open = False

        self.readnamelist()
        self.readjson()

        # 根窗口
        self.root = tkinter.Tk()
        self.root.title('抽签助手')
        # self.root.maxsize(600, 400)    #窗口大小
        #self.root.minsize(300, 240)

        # 容器
        # self.frame=tkinter.Frame(self.root,width=300,height=240,background='green')
        self.frame = tkinter.Frame(self.root, width=300, height=240)

        # name 用来储存当前显示在屏幕上的姓名
        self.name = tkinter.StringVar()
        self.nameLabel = tkinter.Label(
            self.frame, textvariable=self.name, width=10, height=4)
        #self.nameLabel.config(font = 'Helvetica -78 bold')
        self.nameLabel.config(font='微软雅黑 -78 bold')

        self.status = tkinter.StringVar()  # 按钮上的文字：开始/停止
        self.clickButton = tkinter.Button(
            self.frame, textvariable=self.status, command=self.startorstop)
        self.name.set('准备开始')
        self.status.set('开始抽取')

        # 绑定键盘记录器事件
        self.frame.bind("<Any-KeyPress>", self.callBack)

        # 布局
        self.nameLabel.grid(column=0, row=0, columnspan=3)
        self.clickButton.grid(column=0, row=1, columnspan=3)
        self.tipsString = tkinter.StringVar()
        self.tipsLabel = tkinter.Label(
            self.frame, textvariable=self.tipsString)
        self.tipsString.set('抽签助手V1.5，名单列表里共有%s个名字' % len(self.namelist))
        self.tipsLabel.grid(column=0, row=2)

        self.norepeat = tkinter.IntVar()  # 无重复模式判断变量
        self.check1 = tkinter.Checkbutton(
            self.frame, text='无重复模式', variable=self.norepeat)
        self.norepeat.set(1)
        self.setButton = tkinter.Button(
            self.frame, text='设置', command=self.show_setting)
        self.setButton.grid(column=2, row=2)
        self.check1.grid(column=1, row=2)
        self.frame.grid(column=0, row=0)
        self.frame.focus_set()

        self.database = Database(self.namelist, self.norepeat)
        self.counter = Counter(len(str(len(self.namelist))))

    def mainloop(self):
        self.root.mainloop()

    def show_setting(self):
        if self.is_setting_open:
            return
        self.is_setting_open = True
        self.settingWindow = SettingWindow(self)

    def readjson(self):  # 读取配置文件
        with open('config.json', 'rb') as f:
            data = f.read().decode('utf-8')
            self.jsondata = json.loads(data)

    def callBack(self, event):  # 键盘记录器关键函数
        self.counter.putin(event.keysym)

    def startorstop(self):  # 绑定按钮用的函数，执行一次开始，再执行一次停止，靠 now 判断当前是否再运行
        if not self.now:  # 开始
            self.now = True
            self.status.set('点击停止')
            threading.Thread(target=self.chouqian, args=()).start()
        else:
            self.now = False
            self.status.set('点击开始')

    def realchouqian(self):  # 真正的抽签函数，抽签动画停止后立即执行 realchouqian，
        if self.norepeat.get() == 1:  # 判断无重复模式勾选框是否勾选
            maxrange = self.jsondata['range']  # 从数据库中弄一个次数较少的名字出来
            resultname = self.database.get(maxrange)
            self.name.set(resultname)  # 把抽到的名字秒变数据库中抽到的名字
        num = self.counter.getout()  # 从键盘记录器调取输入的编号
        if num:
            self.name.set(self.namelist[int(num)-1])  # 从键盘记录器读取序号，设置名字，达到作弊效果

    def chouqian(self):  # 抽签主函数
        while self.now:
            randnum = random.randint(0, len(self.namelist)-1)
            self.name.set(self.namelist[randnum])
            time.sleep(self.jsondata['sleep'])
        self.realchouqian()  # 正常抽签后，执行一次真的抽签函数覆盖结果

    def readnamelist(self):  # 读取名单，按行分割，返回列表
        namelist = list()
        with open('名单.txt', 'rb') as f:
            raw_str = f.read()
        try:
            raw_str = raw_str.decode('utf-8')
        except:
            try:
                raw_str = raw_str.decode('gb2312')
            except:
                raise ValueError('名单.txt文件解码错误，请使用UTF-8或GB2312编码')
        raw_str = raw_str.replace('\r', '')
        _namelist = raw_str.split('\n')
        for name in _namelist:
            if name:
                namelist.append(name)
        self.namelist = namelist


if __name__ == '__main__':
    main()
