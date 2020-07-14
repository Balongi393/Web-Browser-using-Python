import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QTabBar,
                             QFrame, QStackedLayout)
from PyQt5.QtGui import QIcon, QWindow, QImage
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
class AdressB(QLineEdit):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, q):
        self.selectAll()

class Application(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("Logo.png"))
        self.setWindowTitle("Balongi")
        self.setBaseSize(1400, 720)
        self.setMinimumSize(1400, 720)
        self.CreateApplication()

    def CreateApplication(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        #Create Tabs
        self.tabbar = QTabBar(movable=True, tabsClosable=True)
        self.tabbar.tabCloseRequested.connect(self.CloseTab)
        self.tabbar.tabBarClicked.connect(self.SwitchTab)
        self.tabbar.setCurrentIndex(0)
        self.tabbar.setDrawBase(False)
        self.tabbar.setLayoutDirection(Qt.LeftToRight)
        self.tabbar.setElideMode(Qt.ElideLeft)
        # Keep Track at Tabs
        self.tabCount = 0
        self.tabs = []
        #Create AddressBar
        self.Toolbar = QWidget()
        self.Toolbar.setObjectName("Toolbar")
        self.Toolbarlayout = QHBoxLayout()
        self.addressb = AdressB()
        self.AddTabButton = QPushButton("🞢")
        #Connect addressbar + button signals
        self.addressb.returnPressed.connect(self.Browse)
        self.AddTabButton.clicked.connect(self.AddTab)
        #Set toolbar buttons
        self.BackButton = QPushButton("🠜")
        self.BackButton.clicked.connect(self.GoBack)
        self.ForwardButton = QPushButton("🠞")
        self.ForwardButton.clicked.connect(self.GoForward)
        self.ReloadButton = QPushButton("⭮")
        self.ReloadButton.clicked.connect(self.ReloadPage)
        #Build a toolbar
        self.Toolbar.setLayout(self.Toolbarlayout)
        self.Toolbarlayout.addWidget(self.BackButton)
        self.Toolbarlayout.addWidget(self.ForwardButton)
        self.Toolbarlayout.addWidget(self.ReloadButton)
        self.Toolbarlayout.addWidget(self.addressb)
        self.Toolbarlayout.addWidget(self.AddTabButton)
        # Set Main View
        self.container = QWidget()
        self.container.layout  = QStackedLayout()
        self.container.setLayout(self.container.layout)

        self.layout.addWidget(self.tabbar)
        self.layout.addWidget(self.Toolbar)
        self.layout.addWidget(self.container)
        self.setLayout(self.layout)
        self.AddTab()
        self.show()

    def CloseTab(self, i):
       self.tabbar.removeTab(i)

    def AddTab(self):
        i = self.tabCount
        self.tabs.append(QWidget())
        self.tabs[i].layout = QVBoxLayout()
        self.tabs[i].layout.setContentsMargins(0,0,0,0)
        #For tab switching
        self.tabs[i].setObjectName("tab" + str(i))
        #Open webview
        self.tabs[i].content = QWebEngineView()
        self.tabs[i].content.load(QUrl.fromUserInput("http://google.com"))
        self.tabs[i].content.titleChanged.connect(lambda: self.SetTabContent(i, "title"))
        self.tabs[i].content.iconChanged.connect(lambda: self.SetTabContent(i, "icon"))
        self.tabs[i].content.urlChanged.connect(lambda: self.SetTabContent(i, "url"))
        #Add web view to tabs layout
        self.tabs[i].layout.addWidget(self.tabs[i].content)
        # Set Top Level Tab from list to layout
        self.tabs[i].setLayout(self.tabs[i].layout)
        #Add tab to top level stackwidget
        self.container.layout.addWidget(self.tabs[i])
        self.container.layout.setCurrentWidget(self.tabs[i])
        #Set the tabs at the top of the screen
        self.tabbar.addTab("New Tab")
        self.tabbar.setTabData(i, {"object": "tab" + str(i), "initial": i})
        print("tabData: ", self.tabbar.tabData(i)["object"])
        self.tabbar.setCurrentIndex(i)
        self.tabCount += 1

    def SwitchTab(self, i):
        tab_data = self.tabbar.tabData(i)["object"]
        tab_content = self.findChild(QWidget, tab_data)
        self.container.layout.setCurrentWidget(tab_content)
        new_url = tab_content.content.url().toString()
        self.addressb.setText(new_url)

    def Browse(self):
        text = self.addressb.text()
        print(text)

        i = self.tabbar.currentIndex()
        tab = self.tabbar.tabData(i)["object"]
        web_view = self.findChild(QWidget, tab).content
        if "http" not in text:
            if "." not in text:
                url = "https://www.google.com/#q=" + text
            else:
                url = "http://" + text
        else:
            url = text
        web_view.load(QUrl.fromUserInput(url))

    def SetTabContent(self, i, type):
        '''
        self.tabs[i].objectName = tab1
        self.tabbar.tabDat[i]["object"] = tab1
        '''
        tab_name = self.tabs[i].objectName()
        # tab1
        count = 0
        running = True
        currentTab = self.tabbar.tabData(self.tabbar.currentIndex())["object"]
        if currentTab == tab_name and type == "url":
            new_url = self.findChild(QWidget, tab_name).content.url().toString()
            self.addressb.setText(new_url)
        else:
            while running:
                tab_data_name = self.tabbar.tabData(count)
                if count >= 99:
                    running = False
                if tab_name == tab_data_name["object"]:
                    if type == "title":
                        newTitle = self.findChild(QWidget, tab_name).content.title()
                        self.tabbar.setTabText(count, newTitle)
                    elif type == "icon":
                        newIcon = self.findChild(QWidget, tab_name).content.icon()
                        self.tabbar.setTabIcon(count, newIcon)
                    running = False
                else:
                    count += 1
    def GoBack(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content
        tab_content.back()

    def GoForward(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content
        tab_content.forward()

    def ReloadPage(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content
        tab_content.reload()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    with open("stylesheet.css", "r") as style:
        app.setStyleSheet(style.read())

    sys.exit(app.exec_())




