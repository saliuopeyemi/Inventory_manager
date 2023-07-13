from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QMovie,QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QDialog,QStackedWidget,QSplashScreen,QMainWindow,QLineEdit,QInputDialog,QFormLayout,QLabel,QPushButton,QFileDialog,QMessageBox,QTextEdit,QVBoxLayout
import json
from prettytable import PrettyTable as pt
from datetime import date
from time import sleep
from openpyxl import Workbook

dashboard_name=" "
screen_value=" "

class homepage(QMainWindow):
    def __init__(self):
        super(homepage,self).__init__()
        loadUi("app.ui",self)
        self.loginbtn.clicked.connect(logIn)
        self.createbtn.clicked.connect(create)

class search(QDialog):
    def __init__(self):
        super(search, self).__init__()
        self.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(170, 255, 127, 255), stop:1 rgba(255, 255, 255, 255))")
        self.frame=QFormLayout()
        self.setWindowTitle("Find Item ID")
        self.word = QLineEdit()
        self.screen=QTextEdit()
        self.screen.setStyleSheet('font: 75 7.5pt "DejaVu Sans Mono";')
        self.screen.setReadOnly(True)
        self.search_btn=QPushButton("Search")
        self.cancel=QPushButton("Cancel")
        self.frame.addRow(QLabel("Result:"), self.screen)
        self.frame.addRow(QLabel("Search text:"),self.word)
        self.frame.addRow(self.cancel,self.search_btn)
        self.setLayout(self.frame)
        self.cancel.clicked.connect(self.exit)
        self.search_btn.clicked.connect(self.search)

    def exit(self):
        self.close()

    def search(self):
        with open("tempfile.json","r") as file:
            data=json.load(file)
        with open("main.json","r") as file1:
            user = json.load(file1)
        self.searched= self.word.text()
        search_list=[]
        for i in data[user]:
            if self.searched in i[1]:
                result_item=[i[0],i[1]]
                search_list.append(result_item)
        result_table=pt()
        result_table.field_names=["ITEM ID","ITEM"]
        for j in search_list:
            result_table.add_row(j,divider=True)
        final_result=result_table.get_string()
        self.screen.setText(final_result)







class login(QMainWindow):
    def __init__(self):
        super(login,self).__init__()
        loadUi("login.ui", self)
        self.login_trial = 3
        self.password.setEchoMode(QLineEdit.Password)
        self.back.clicked.connect(back)
        self.login.clicked.connect(self.auth)
        #LOG IN POINT
    def auth(self):
        global dashboard_name
        self.error.setText("")
        if len(self.username.text())== 0:
            self.error.setText("Username field cannot be empty")
        elif len(self.password.text()) == 0:
            self.error.setText("Password field cannot be empty")
        else:
            with open("temp1.json","r") as file:
                accounts = json.load(file)
                for i in accounts:
                    if self.username.text() == i:
                        if self.password.text() == accounts[i]:
                            #MAIN DASHBOARD LOAD POINT..........
                            dashboard_name=self.username.text()
                            with open("main.json","r") as file:
                                active = json.load(file)
                            with open("main.json", "w") as file:
                                json.dump(dashboard_name,file)
                            goto_dashboard()
                            self.login_trial = 3
                        else:
                            if self.login_trial != 0:
                                self.login_trial -=1
                                self.error.setText(f"Incorrect Password. {self.login_trial} attempts left")
                            else:
                                #ENFORCE DATABASE LOGIN SECURITY POINT
                                pass
                    else:
                        #pass
                        self.error.setText("Incorrect username/password")

class delete_dialog(QDialog):
    def __init__(self):
        super(delete_dialog,self).__init__()
        self.setStyleSheet(
            "background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(170, 255, 127, 255), stop:1 rgba(255, 255, 255, 255))")
        self.frame = QFormLayout()
        self.setWindowTitle("Delete Item")
        self.setFixedWidth(320)
        self.setFixedHeight(80)
        self.label=QLabel("Item ID:")
        self.id_entry=QLineEdit()
        self.cancel=QPushButton("Cancel")
        self.delet=QPushButton("Delete")
        self.frame.addRow(self.label,self.id_entry)
        self.frame.addRow(self.cancel,self.delet)
        self.setLayout(self.frame)
        self.cancel.clicked.connect(self.kill)
        self.delet.clicked.connect(self.delete_item)
    def kill(self):
        self.close()
    def delete_item(self):
        self.id=self.id_entry.text()
        with open("tempfile.json","r") as file:
            database=json.load(file)
        with open("main.json","r") as file2:
            user=json.load(file2)
        for i in database:
            if i == user:
                for j in database[i]:
                    if j[0] == int(self.id):
                        row_index= database[i].index(j)
                        del database[i][row_index]
        with open("tempfile.json","w") as file:
            json.dump(database,file)
            self.kill()


class item_out(QDialog):
    def  __init__(self):
        super(item_out,self).__init__()
        self.setStyleSheet(
            "background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(170, 255, 127, 255), stop:1 rgba(255, 255, 255, 255))")
        self.setWindowTitle("Item Out")
        self.setFixedWidth(320)
        self.setFixedHeight(110)
        self.frame=QFormLayout()
        self.id=QLineEdit()
        self.amt=QLineEdit()
        self.ok=QPushButton("Ok")
        self.cancel=QPushButton("Cancel")
        self.frame.addRow(QLabel("Item ID:"),self.id)
        self.frame.addRow(QLabel("Item Amount:"),self.amt)
        self.frame.addRow(self.cancel,self.ok)
        self.setLayout(self.frame)
        self.cancel.clicked.connect(self.close_dialog)
        self.ok.clicked.connect(self.item_out)

    def item_out(self):
        try:
            item_id=int(self.id.text())
            item_amount=int(self.amt.text())
            with open("tempfile.json", "r") as file:
                database = json.load(file)
            with open("main.json", "r") as file2:
                user = json.load(file2)
            for i in database:
                if i == user:
                    count=0
                    for j in database[i]:
                        count+=1
                        if j[0] == item_id:
                            Index = database[i].index(j)
                            if j[2] < item_amount:
                                self.error = QMessageBox()
                                self.error.setWindowTitle("Stock Inadequacy")
                                self.error.setText("Not enough units to out for this item ")
                                self.error.setIcon(QMessageBox.Critical)
                                self.error.setStandardButtons(QMessageBox.Ok)
                                self.error.exec()
                            else:
                                database[i][Index][2] = database[i][Index][2] - item_amount
                                database[i][Index][5] = str(date.today())
                                database[i][Index][7] += item_amount
                                break
                        elif count < len(database[i]):
                            continue
                        else:
                            self.error = QMessageBox()
                            self.error.setWindowTitle("Id not captured")
                            self.error.setText("No item is recorded with id")
                            self.error.setIcon(QMessageBox.Critical)
                            self.error.setStandardButtons(QMessageBox.Ok)
                            self.error.exec()
            with open("tempfile.json", "w") as file:
                json.dump(database, file)
            self.close()
        except:
            self.error = QMessageBox()
            self.error.setWindowTitle("Inappropriate Value")
            self.error.setText("Unallowed character for item id/item amount")
            self.error.setIcon(QMessageBox.Critical)
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.exec()

    def close_dialog(self):
        self.close()

class item_in(QDialog):
    def __init__(self):
        super(item_in, self).__init__()
        self.setStyleSheet(
            "background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(170, 255, 127, 255), stop:1 rgba(255, 255, 255, 255))")
        self.setWindowTitle("Item In")
        self.setFixedWidth(320)
        self.setFixedHeight(110)
        self.frame = QFormLayout()
        self.id = QLineEdit()
        self.amt = QLineEdit()
        self.ok = QPushButton("Ok")
        self.cancel = QPushButton("Cancel")
        self.frame.addRow(QLabel("Item ID:"), self.id)
        self.frame.addRow(QLabel("Item Amount:"), self.amt)
        self.frame.addRow(self.cancel, self.ok)
        self.setLayout(self.frame)
        self.cancel.clicked.connect(self.close_dialog)
        self.ok.clicked.connect(self.item_in)
    def close_dialog(self):
        self.close()
    def item_in(self):
        try:
            item_id=int(self.id.text())
            item_amount=int(self.amt.text())
            with open("tempfile.json", "r") as file:
                database = json.load(file)
            with open("main.json", "r") as file2:
                user = json.load(file2)
            for i in database:
                if i == user:
                    count=0
                    for j in database[i]:
                        count+=1
                        if j[0] == item_id:
                            Index = database[i].index(j)
                            database[i][Index][2] = database[i][Index][2] + item_amount
                            database[i][Index][4] = str(date.today())
                            database[i][Index][6] += item_amount
                            break
                        elif count < len(database[i]):
                            continue
                        else:
                            self.error = QMessageBox()
                            self.error.setWindowTitle("Id not captured")
                            self.error.setText("No item is recorded with id")
                            self.error.setIcon(QMessageBox.Critical)
                            self.error.setStandardButtons(QMessageBox.Ok)
                            self.error.exec()
            with open("tempfile.json", "w") as file:
                json.dump(database, file)
            self.close()
        except:
            self.error = QMessageBox()
            self.error.setWindowTitle("Inappropriate Value")
            self.error.setText("Unallowed character for item id/item amount")
            self.error.setIcon(QMessageBox.Critical)
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.exec()


class add_dialog(QDialog):
    def __init__(self):
        super(add_dialog,self).__init__()
        self.setStyleSheet(
            "background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(170, 255, 127, 255), stop:1 rgba(255, 255, 255, 255))")
        self.frame=QFormLayout()
        self.setWindowTitle("New Item")
        self.setFixedWidth(320)
        self.setFixedHeight(240)
        self.id=QLineEdit()
        self.name=QLineEdit()
        self.qty=QLineEdit()
        self.container=QLineEdit()
        self.accept=QPushButton("Accept")
        self.cancel=QPushButton("Cancel")
        self.frame.addRow(QLabel("Item Id:"), self.id)
        self.frame.addRow(QLabel("Item Name:"), self.name)
        self.frame.addRow(QLabel("Quantity"),self.qty)
        self.frame.addRow(QLabel("Container"), self.container)
        self.frame.addRow(self.cancel,self.accept)
        self.setLayout(self.frame)
        self.cancel.clicked.connect(self.close_window)
        self.accept.clicked.connect(self.add_data)
    def close_window(self):
        self.close()
    def add_data(self):
        global active_user
        with open("tempfile.json","r") as file:
            data = json.load(file)
        with open("main.json","r") as file:
            active_user=json.load(file)
# ITEM LIST FOR DATABSE AND SCREEN TABLE........................
        try:
            item_id=int(self.id.text())
            item_name=self.name.text()
            item_qty=int(self.qty.text())
            item_container=self.container.text()
            added_date=str(date.today())
            modify_date=str(date.today())
            total_in = item_qty
            total_out=0
            item_list=[item_id,item_name,item_qty,item_container,added_date,modify_date,total_in,total_out]
    #ADD ITEM TO DATABASE
            for i in data:
                if i == active_user:
                    data[i].append(item_list)
            with open("tempfile.json", "w") as file:
                data = json.dump(data,file)
            self.close()
        except:
            self.error = QMessageBox()
            self.error.setWindowTitle("Inappropriate Value")
            self.error.setText("Unallowed character for integer entry.")
            self.error.setIcon(QMessageBox.Critical)
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.exec()

class change_password(QDialog):
    def __init__(self):
        super(change_password,self).__init__()
        self.setStyleSheet(
            "background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(170, 255, 127, 255), stop:1 rgba(255, 255, 255, 255))")
        self.frame=QFormLayout()
        self.setWindowTitle("Change Password")
        self.setFixedWidth(320)
        self.setFixedHeight(240)
        self.p_password=QLineEdit()
        self.p_password.setEchoMode(QLineEdit.Password)
        self.c_password1=QLineEdit()
        self.c_password1.setEchoMode(QLineEdit.Password)
        self.c_password2=QLineEdit()
        self.c_password2.setEchoMode(QLineEdit.Password)
        self.cancel=QPushButton("Cancel")
        self.ok=QPushButton("Commit")
        self.frame.addRow(QLabel("Previous Password:"),self.p_password)
        self.frame.addRow(QLabel("Enter New Password:"),self.c_password1)
        self.frame.addRow(QLabel("Confirm Password:"),self.c_password2)
        self.frame.addRow(self.cancel,self.ok)
        self.setLayout(self.frame)
        self.ok.clicked.connect(self.change_action)
        self.cancel.clicked.connect(self.Cancel)

    def Cancel(self):
        self.close()

    def change_action(self):
        former_password=self.p_password.text()
        password1=self.c_password1.text()
        password2=self.c_password2.text()
        with open("main.json","r") as file:
            user=json.load(file)
        with open("temp1.json","r") as file2:
            account=json.load(file2)
        for i in account:
            if i== user:
                if account[i] == former_password:
                    if password1==password2:
                        account[i] = password1
                        with open("temp1.json","w") as file:
                            json.dump(account,file)
                        self.error = QMessageBox()
                        self.error.setWindowTitle("Password Change")
                        self.error.setText("Your password was changed successfully")
                        self.error.setIcon(QMessageBox.Information)
                        self.error.setStandardButtons(QMessageBox.Ok)
                        output=self.error.exec()
                        if output == 1024:
                            self.close()

                    else:
                        self.error = QMessageBox()
                        self.error.setWindowTitle("Unmatched Passwords")
                        self.error.setText("Your password choice was not confirmed")
                        self.error.setIcon(QMessageBox.Critical)
                        self.error.setStandardButtons(QMessageBox.Ok)
                        self.error.exec()
                else:
                    self.error = QMessageBox()
                    self.error.setWindowTitle("Password change denied")
                    self.error.setText("Your password change request was declined")
                    self.error.setIcon(QMessageBox.Critical)
                    self.error.setStandardButtons(QMessageBox.Ok)
                    self.error.exec()







class dashboard(QMainWindow):
    global screen_value
    def __init__(self):
        super(dashboard,self).__init__()
        loadUi("dashboard.ui",self)
        self.anim=QMovie("anim.gif")
        self.dashboard_icon.setMovie(self.anim)
        self.anim.start()
        self.refresh_page()
        self.screen.setReadOnly(True)
        self.database_info.setText(f"Hello {dashboard_name}...")
        self.add.setStyleSheet("QPushButton::hover{background-color:yellow;}")
        self.add.clicked.connect(self.add_data)
        self.refresh.setStyleSheet("QPushButton::hover{background-color:yellow;}")
        self.refresh.clicked.connect(self.refresh_page)
        self.logout.setStyleSheet("QPushButton::hover{background-color:yellow;}")
        self.logout.clicked.connect(self.logOut)
        self.delet.setStyleSheet("QPushButton::hover{background-color:yellow;}")
        self.delet.clicked.connect(self.show_del_dialog)
        self.Iout.setStyleSheet("QPushButton::hover{background-color:yellow;}")
        self.Iout.clicked.connect(self.out)
        self.Iin.setStyleSheet("QPushButton::hover{background-color:yellow;}")
        self.Iin.clicked.connect(self.item_in)
        self.c_password.setStyleSheet("QPushButton::hover{background-color:yellow;}")
        self.c_password.clicked.connect(self.Change_password)
        self.find.setStyleSheet("QPushButton::hover{background-color:yellow;}")
        self.find.clicked.connect(self.search_text)
        self.report.setStyleSheet("QPushButton::hover{background-color:yellow;}")
        self.report.clicked.connect(self.create_report)


    def create_report(self):
        wb =Workbook()
        ws=wb.active
        with open("tempfile.json","r") as file:
            data=json.load(file)
        with open("main.json","r") as file1:
            user=json.load(file1)
        try:
            for i in data[user]:
                ws.append(i)
            self.directory=QFileDialog.getExistingDirectory()
            wb.save(f"{self.directory}/{user}'s report.xlsx")
            self.success=QMessageBox()
            self.success.setStyleSheet("background-color:green; border-radius:5px;font: 75 10pt 'Consolas'")
            self.success.setWindowTitle("Report Export Success")
            self.success.setText(f"{user}'s report was exported successfully")
            self.success.setIcon(QMessageBox.Information)
            self.success.setStandardButtons(QMessageBox.Ok)
            self.success.exec()
        except:
            self.error=QMessageBox()
            self.error.setWindowTitle("Report Creation Abort")
            self.error.setText("You canceled this operation")
            self.error.setIcon(QMessageBox.Critical)
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.exec()


    def search_text(self):
        self.Search= search()
        self.Search.show()

    def Change_password(self):
        self.c_pwrd=change_password()
        self.c_pwrd.show()


    def item_in(self):
        self.item = item_in()
        self.item.show()

    def out(self):
        self.Item_out =item_out()
        self.Item_out.show()

    def show_del_dialog(self):
        self.del_dialog= delete_dialog()
        self.del_dialog.show()
    def add_data(self):
        self.add = add_dialog()
        self.add.show()
    def refresh_page(self):
        with open("main.json", "r") as file:
            active=json.load(file)
        with open("tempfile.json","r") as file:
            data= json.load(file)
        for i in data:
            if i == active:
                data_unit= data[i]
                tb=pt()
                #.............................SPECIFYING COLUMNS FOR VIEW AND DATABASE..........................................
                tb.field_names=["ITEM ID","ITEM DESCRIPTION","QUANTITY","BUNDLE NAME","DATE ADDED","MODIFIED","ƩIN","ƩOUT"]
                for j in data_unit:
                    tb.add_row(j,divider=True)
                view=tb.get_string(sortby="ITEM ID")
                self.screen.setText(view)
    def logOut(self):
        logIn()






def goto_dashboard():
    global dboard
    dboard=dashboard()
    widget.addWidget(dboard)
    widget.setCurrentIndex(widget.currentIndex()+1)

class create_acc(QMainWindow):
    def __init__(self):
        super(create_acc,self).__init__()
        loadUi("c_acnt.ui", self)
        self.password.setEchoMode(QLineEdit.Password)
        self.c_password.setEchoMode(QLineEdit.Password)
        self.back.clicked.connect(back)
        self.create.clicked.connect(self.cre8)
    def cre8(self):
        global u_name
        with open("temp1.json", "r") as file:
            account_data = json.load(file)
        self.error.setText("")
        if len(self.username.text()) == 0:
            self.error.setText("Username field cannot be empty")
        elif len(self.password.text()) == 0:
            self.error.setText("Password field cannot be empty")
        elif self.password.text() != self.c_password.text():
            self.error.setText("Passwords do not match")
        else:
            self.check_list =[]
            with open("temp1.json","r") as file:
                account_data=json.load(file)
            for i in account_data:
                self.check_list.append(i)
            if self.username.text() in self.check_list:
                self.error.setText("Username already exists.")
            else:
                global u_name
                global u_pword
                u_name=str(self.username.text())
                u_pword = str(self.password.text())
                add_new_account()
                with open("tempfile.json","r") as file:
                    data = json.load(file)
                data[u_name]=[]
                with open("tempfile.json", "w") as file:
                    json.dump(data,file)
                self.error.setText("Account successfully created. Return to login")
                self.username.setText("")
                self.password.setText("")
                self.c_password.setText("")

def add_new_account():
    with open("temp1.json", "r") as file:
        account_data = json.load(file)
        account_data[u_name]=u_pword
    with open("temp1.json","w") as file:
        json.dump(account_data,file)



def back():
    hmpg = homepage()
    widget.addWidget(hmpg)
    widget.setCurrentIndex(widget.currentIndex()+1)

def logIn():
    lgin = login()
    widget.addWidget(lgin)
    widget.setCurrentIndex(widget.currentIndex()+1)

def create():
    cre8 = create_acc()
    widget.addWidget(cre8)
    widget.setCurrentIndex(widget.currentIndex()+1)

class intro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.messages=["Initializing content objects","Creating database container","Setting storage elements","Opening Inventory Manager"]
        self.logo = QPixmap("icon.png")
        self.Intro=QSplashScreen(self.logo)
        self.Intro.show()
        for i in self.messages:
            self.Intro.showMessage(f"<font color=Gold size=4><strong>{i}</strong></font>")
            sleep(3)
        self.Intro.close()

class container(QStackedWidget):
    def __init__(self):
        super().__init__()

    def closeEvent(self,event):
        Reply=QMessageBox.question(self,"Exit","You are about to close Inventory Manager",QMessageBox.Ok|QMessageBox.Cancel)
        if Reply == QMessageBox.Ok:
            event.accept()
        else:
            event.ignore()


app = QApplication([])
hmpg =  homepage()
enter=intro()
widget= container()
widget.setWindowIcon(QIcon("icon.png"))
widget.setFixedWidth(947)
widget.setFixedHeight(558)
widget.setWindowTitle("Inventory Manager")
widget.addWidget(hmpg)
widget.show()
app.exec()

