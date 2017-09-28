from tkinter import *
 
root=Tk()
 
#创建一个框架，在这个框架中响应事件
frame=Frame(root,
    width=200,height=200,
    background='green')
 
def callBack(event):
    print(event.keysym)
 
frame.bind("<Any-KeyPress>",callBack)
frame.pack()
#当前框架被选中，意思是键盘触发，只对这个框架有效
frame.focus_set()
 
mainloop()
