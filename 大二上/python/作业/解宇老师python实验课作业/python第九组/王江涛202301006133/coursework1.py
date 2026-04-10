import tkinter as tk

root = tk.Tk()
root.title("简单计算器")
display = tk.Entry(root,width=20,font=("Arial",18),borderwidth=2,relief="solid",bg="#D0E0A0")
display.grid(row=0,column=0,columnspan=5)

def button_click(value):
    current_text = display.get()
    display.delete(0,tk.END)
    display.insert(0,current_text+value)

def calculate():
    try:
        result = eval(display.get())
        display.delete(0,tk.END)
        display.insert(0,str(result))
    except Exception as e:
        display.delete(0,tk.END)
        display.insert(0,"Error")

def clear():
    display.delete(0,tk.END)
buttons = [
('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),  
('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),    
('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),  
('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3)
]
for(text,row,col) in buttons:
    if text =='=':
        btn = tk.Button(root,text=text,padx=20,pady=20,command=calculate,bg="#D0E0A0")
    else:
        btn = tk.Button(root,text=text,padx=20,pady=20,command=lambda txt=text:button_click(txt),bg="#D0E0A0")
    btn.grid(row=row,column=col)

clear_button = tk.Button(root,text="C",padx=20,pady=20,command=clear,bg="#D0E0A0")
clear_button.grid(row=4,column=4,columnspan=2)
root.mainloop()




import turtle
t = turtle.Turtle()
t.speed(10)
for i in range(1000):
    t.forward(i*5)
    t.right(144)
turtle.done()







import sys 
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog
class Notepad(QMainWindow):    
    def __init__(self):        
        super().__init__()        
        self.initUI()    
    def initUI(self):             
             self.textEdit = QTextEdit()        
             self.setCentralWidget(self.textEdit)                      
             menubar = self.menuBar()        
             fileMenu = menubar.addMenu('文件')               
             openFile = QAction('Open', self)        
             openFile.setShortcut('Ctrl+O')        
             openFile.triggered.connect(self.openFile)        
             fileMenu.addAction(openFile)      
             saveFile = QAction('Save', self)        
             saveFile.setShortcut('Ctrl+S')        
             saveFile.triggered.connect(self.saveFile)        
             fileMenu.addAction(saveFile)               
             self.setGeometry(300, 300, 600, 400)     
             self.setWindowTitle('Simple Notepad(简单记事本)')       
             self.show()    
    def openFile(self):                
        options = QFileDialog.Options()        
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)        
        if fileName:            
            with open(fileName, 'r') as f:                
                self.textEdit.setText(f.read())

    def saveFile(self):        
        options = QFileDialog.Options()        
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options)        
        if fileName:            
            with open(fileName, 'w') as f:                
                f.write(self.textEdit.toPlainText())
if __name__ == '__main__':    
    app = QApplication(sys.argv)    
    notepad = Notepad()    
    sys.exit(app.exec_())
