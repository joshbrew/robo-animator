# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/crazy/Documents/TestUI/roboanimator.ui'
#
# Created by: PyQt5 UI code generator 5.10.1

"""
TODO

- More error catching
- More menu options
- Add undo/redo, other editing features to make system more robust.
- Style style style
- Fix file select for non .blend files so you don't have to manually import
- Detach the blender process correctly for concurrent running. 
- Add table templates/buttons

"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

import csv
import json
import sys
import subprocess
import os
import configparser
import requests
#from shutil import copyfile


class DragAndDrop(QtWidgets.QListWidget):
      dropped = QtCore.pyqtSignal(list)
      def __init__(self, type, parent=None):
            super(DragAndDrop, self).__init__(parent)
            self.setAcceptDrops(True)
            self.setIconSize(QtCore.QSize(72, 72))

      def dragEnterEvent(self, event):
            if event.mimeData().hasUrls():
                  event.accept()
            else:
                  event.ignore()

      def dragMoveEvent(self, event):
            if event.mimeData().hasUrls():
                  event.setDropAction(QtCore.Qt.CopyAction)
                  event.accept()
            else:
                  event.ignore()

      def dropEvent(self, event):

            if event.mimeData().hasUrls():
                  event.setDropAction(QtCore.Qt.CopyAction)
                  event.accept()

                  links = []

                  for url in event.mimeData().urls():
                        links.append(str(url.toLocalFile()))

                  self.dropped.emit(links)
            else:
                  event.ignore()

# Get ui template
Ui_MainWindow, QtBaseClass = uic.loadUiType('RoboAnimator.ui')

class MyApp(QtWidgets.QMainWindow):
    
    def defineStyleSheet(self):
        # Custom style sheet.
        stylesheet = ("""
        .QMenuBar { background: rgb(223, 223, 223) }
        .QMenu { background: rgb(223, 223, 223) }
        
        .QPushButton { background: white }
        .QTableView { background: rgb(220,220,220) }
        .QWidget { background: rgb(34,70,155) }
        .QTabWidget { background: rgb(223, 223, 223) }
        .QWidget#scrollAreaWidgetContents { background: rgb(223, 223, 223) }
        .QWidget#anims { background: black }
        .QWidget#motors { background: black }
        .QWidget#accs { background: black }
        .QWidget#out { background: black }
        .QLabel { color: white }
        """)
        
        return stylesheet
    
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) # Build ui objects
        
        self.appPath = os.path.abspath(os.path.dirname(__file__))
        
        self.Config = configparser.ConfigParser()
        self.Config.read('init.ini')
        
        self.bPath = self.Config['Init']['blender_path']
        self.piPath = self.Config['Init']['pi_path']
        
        # Begin script-side feature additions
        self.ui.actionImport_Animation.triggered.connect(self.on_pushButtonIA_clicked)
        self.ui.actionEdit_Animation.triggered.connect(self.on_pushButtonOB_clicked)
        self.ui.actionWriteData.triggered.connect(self.on_pushButtonWrite_clicked)
        self.ui.actionImportAnimationData.triggered.connect(self.on_pushButtonLoad_clicked)
        self.ui.actionsetBlenderPath.triggered.connect(self.on_setBlenderPath_clicked)
        self.ui.actionImport_Robot_Data.triggered.connect(self.on_pushButtonIM_clicked)
        self.ui.actionsetPiPath.triggered.connect(self.on_setPiPath_clicked)
        self.ui.actionTest_Run.triggered.connect(self.on_TestRun_clicked)
        
        # Toolbar
        #self.pushButtonLoad = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents)
        #self.pushButtonLoad.setGeometry(QtCore.QRect(0, 100, 335, 40)) # QRect(x position, y position, width, height)
        #self.pushButtonLoad.setObjectName("pushButtonLoad")
        #self.pushButtonLoad.setText("Import Animation CSV")
        #self.pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)
        
        #self.pushButtonSave = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents)
        #self.pushButtonSave.setGeometry(QtCore.QRect(0, 140, 335, 40))
        #self.pushButtonSave.setObjectName("pushButtonSave")
        #self.pushButtonSave.setText("Write Animation CSV")
        #self.pushButtonSave.clicked.connect(self.on_pushButtonWrite_clicked)
        
        self.pushButtonOB = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents)
        self.pushButtonOB.setGeometry(QtCore.QRect(0, 40, 335, 40))
        self.pushButtonOB.setObjectName("pushButtonOB")
        self.pushButtonOB.setText("Edit and Import Animation")
        self.pushButtonOB.clicked.connect(self.on_pushButtonOB_clicked)
        
        self.pushButtonIA = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents)
        self.pushButtonIA.setGeometry(QtCore.QRect(0, 80, 335, 40))
        self.pushButtonIA.setObjectName("pushButtonIA")
        self.pushButtonIA.setText("Import Animation")
        self.pushButtonIA.clicked.connect(self.on_pushButtonIA_clicked)
        
        self.pushButtonTestRun = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents)
        self.pushButtonTestRun.setGeometry(QtCore.QRect(0, 710, 335, 40))
        self.pushButtonTestRun.setObjectName("pushButtonTestRun")
        self.pushButtonTestRun.setText("Test Run")
        self.pushButtonTestRun.clicked.connect(self.on_TestRun_clicked)
        
        self.pushButtonIM = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents)
        self.pushButtonIM.setGeometry(QtCore.QRect(0, 260, 335, 40))
        self.pushButtonIM.setObjectName("pushButtonIM")
        self.pushButtonIM.setText("Import Port Config")
        self.pushButtonIM.clicked.connect(self.on_pushButtonIM_clicked)
        
        self.pushButtonSaveCfg = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents)
        self.pushButtonSaveCfg.setGeometry(QtCore.QRect(0, 200, 335, 40))
        self.pushButtonSaveCfg.setObjectName("pushButtonSaveCfg")
        self.pushButtonSaveCfg.setText("Write Animation Config")
        self.pushButtonSaveCfg.clicked.connect(self.on_writeSaveCfg_clicked)
        
        self.pushButtonSaveMCfg = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents)
        self.pushButtonSaveMCfg.setGeometry(QtCore.QRect(0, 300, 335, 40))
        self.pushButtonSaveMCfg.setObjectName("pushButtonSaveMCfg")
        self.pushButtonSaveMCfg.setText("Write Port Config")
        self.pushButtonSaveMCfg.clicked.connect(self.on_writeSaveMCfg_clicked)
        
        self.pushButtonSendFiles = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents)
        self.pushButtonSendFiles.setGeometry(QtCore.QRect(0, 660, 335, 40))
        self.pushButtonSendFiles.setObjectName("pushButtonSendFiles")
        self.pushButtonSendFiles.setText("Send Files")
        self.pushButtonSendFiles.clicked.connect(self.on_saveFiles_clicked)
        
        
        self.addAnimRowBtn = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents)
        self.addAnimRowBtn.setObjectName("addRowBtn")
        self.addAnimRowBtn.setGeometry(QtCore.QRect(0, 450, 170, 40))
        self.addAnimRowBtn.setText("Add Anim Row")
        self.addAnimRowBtn.clicked.connect(self.on_addAnimRowBtn_clicked)
       
        
        
        self.addSPIBtn = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents)
        self.addSPIBtn.setObjectName("addRowBtn")
        self.addSPIBtn.setGeometry(QtCore.QRect(0, 500, 170, 40))
        self.addSPIBtn.setText("Add SPI")
        self.addSPIBtn.clicked.connect(self.on_addSPIBtn_clicked)
       
        self.addGPIOBtn = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents)
        self.addGPIOBtn.setObjectName("addRowBtn")
        self.addGPIOBtn.setGeometry(QtCore.QRect(171, 500, 170, 40))
        self.addGPIOBtn.setText("Add GPIO")
        self.addGPIOBtn.clicked.connect(self.on_addGPIOBtn_clicked)
       
        
        # Anim Tab
        self.animLabel = QtWidgets.QLabel("Imported Data:",self)
        self.ui.animLayout.addWidget(self.animLabel)
        
        self.animModel = QtGui.QStandardItemModel() # Rewritable table data
        self.animModel.setColumnCount(10)
        self.animModel.setRowCount(1)
        arow = ['Flags','Frame','Time']
        self.animModel.insertRow(0,[
                    QtGui.QStandardItem(field) # set logic for table values here
                    for field in arow ])
    
        self.animTable = QtWidgets.QTableView()
        self.animTable.setModel(self.animModel)
        self.animTable.horizontalHeader().setStretchLastSection(True)
        self.animTable.setAlternatingRowColors(True)
        self.animTable.horizontalHeader().setVisible(False)
        self.animTable.verticalHeader().setVisible(False)
        self.ui.animLayout.addWidget(self.animTable)

        self.animTable.setSizeAdjustPolicy(
        QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.animTable.resizeColumnsToContents()


        
        
        
        # Motor Tab
        self.SPILabel = QtWidgets.QLabel("SPI Configurator:", self)
        self.ui.motorLayout.addWidget(self.SPILabel)
        
        
        self.SPIModel = QtGui.QStandardItemModel()
        self.SPIModel.setColumnCount(6)
        self.SPIModel.setRowCount(1)
        rowSPI = ['Port','Speed','CS','Mode','Bits','Drivers']
        self.SPIModel.insertRow(0,[
                    QtGui.QStandardItem(field) # set logic for table values here
                    for field in rowSPI ])
        
        self.SPITable = QtWidgets.QTableView()
        self.SPITable.setModel(self.SPIModel)
        self.SPITable.horizontalHeader().setStretchLastSection(True)
        self.SPITable.setAlternatingRowColors(True)
        self.SPITable.horizontalHeader().setVisible(False)
        self.SPITable.verticalHeader().setVisible(False)
        self.ui.motorLayout.addWidget(self.SPITable)
        
        self.SPITable.setSizeAdjustPolicy(
        QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.SPITable.resizeColumnsToContents()
        self.SPITable.resizeRowsToContents()
        
        self.GPIOLabel = QtWidgets.QLabel("GPIO Configurator:",self)
        self.ui.motorLayout.addWidget(self.GPIOLabel)

        self.motorModel = QtGui.QStandardItemModel()
        self.motorModel.setColumnCount(4)
        self.motorModel.setRowCount(1)
        rowM = ['Type','Name','GPIO','Comp']
        self.motorModel.insertRow(0,[
                    QtGui.QStandardItem(field) # set logic for table values here
                    for field in rowM ])
    
        self.motorTable = QtWidgets.QTableView()
        self.motorTable.setModel(self.motorModel)
        self.motorTable.horizontalHeader().setStretchLastSection(True)
        self.motorTable.setAlternatingRowColors(True)
        self.motorTable.horizontalHeader().setVisible(False)
        self.motorTable.verticalHeader().setVisible(False)
        self.ui.motorLayout.addWidget(self.motorTable)
        
        self.motorTable.setSizeAdjustPolicy(
        QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.motorTable.resizeColumnsToContents()
        self.motorTable.resizeRowsToContents()
        
        # Accessories Tab
        self.accLabel = QtWidgets.QLabel("Sound Configurator:", self)
        self.ui.accessoriesLayout.addWidget(self.accLabel)
        
        self.accessoryModel = QtGui.QStandardItemModel()
        self.accessoryModel.setColumnCount(1)
        self.accessoryModel.setRowCount(1)
        accheader = ['Name','File']
        self.accessoryModel.insertRow(0,[
                    QtGui.QStandardItem(field) # set logic for table values here
                    for field in accheader ])
    
        self.accessoriesTable = QtWidgets.QTableView()
        self.accessoriesTable.setModel(self.accessoryModel)
        self.accessoriesTable.horizontalHeader().setStretchLastSection(True)
        self.accessoriesTable.setAlternatingRowColors(True)
        self.accessoriesTable.horizontalHeader().setVisible(False)
        self.accessoriesTable.verticalHeader().setVisible(False)
        self.ui.accessoriesLayout.addWidget(self.accessoriesTable)
        
        self.accessoriesTable.setSizeAdjustPolicy(
        QtWidgets.QAbstractScrollArea.AdjustToContents)
        
        
        self.accLabel2 = QtWidgets.QLabel("Drop Sound Files:", self)
        self.ui.accessoriesLayout.addWidget(self.accLabel2)
        
        self.DragDrop = DragAndDrop("Drag Sound Here",self)
        self.DragDrop.dropped.connect(self.dropMethod)
        self.DragDrop.setIconSize(QtCore.QSize(50,50))
        self.ui.accessoriesLayout.addWidget(self.DragDrop)
        
        self.deleteButton = QtWidgets.QPushButton()
        self.deleteButton.setText("Delete Item")
        self.deleteButton.clicked.connect(self.deleteItem)
        self.ui.accessoriesLayout.addWidget(self.deleteButton)
        
        # Output Tab
        self.outputLabel = QtWidgets.QLabel("Configuration Output:", self)
        self.ui.outputLayout.addWidget(self.outputLabel)
        
        self.text = QtWidgets.QTextEdit(self)
        self.ui.outputLayout.addWidget(self.text)
        
        self.outputLabel2 = QtWidgets.QLabel("Animation Output:", self)
        self.ui.outputLayout.addWidget(self.outputLabel2)
        
        self.text2 = QtWidgets.QTextEdit(self)
        self.ui.outputLayout.addWidget(self.text2)
        # set custom style sheet
        self.setStyleSheet(self.defineStyleSheet())
        
    
    # Custom functions
    def ConfigSectionMap(self, Config, section):
        dict1 = {}
        options = Config.options(section)
        for option in options:
            try:
                dict1[option] = Config.get(section, option)
                #if dict1[option] == -1:
                #    configparser.DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1
    
    def dropMethod(self, fileList):
        for url in fileList:
            if os.path.exists(url):
                print(url)
                icon = QtGui.QIcon(self.appPath+'//icons//1000px-Speaker_Icon.svg')            
                icon.pixmap(72,72)
                item = QtWidgets.QListWidgetItem(url, self.DragDrop)
                item.setIcon(icon)        
                item.setStatusTip(url) 
                
                temp = url[::-1]
                file = ""
                for letter in temp:
                    if letter == '/':
                        break
                    file = file + letter
                file = file[::-1]
                name = ""
                for letter in file:
                    if letter == '.':
                        break
                    name = name + letter
                
                row = [name,file]
                
                self.accessoryModel.insertRow(1,[
                    QtGui.QStandardItem(field) # set logic for table values here
                    for field in row ])
    
    def returnListItems(self, listWidget):
        items = []
        for i in range(listWidget.count()):
            file = listWidget.item(i)
            items.append(file.text())
        return items
            
    def deleteListItem(self):
        if self.DragDrop.currentRow() != -1:
            self.accessoryModel.removeRows((self.DragDrop.count()-self.DragDrop.currentRow()),1)
        
        self.DragDrop.takeItem(self.DragDrop.currentRow())
        #item = None
    
    
    ## FIX ##
    #def deleteTableRow(self, model):
        #indices = model.selectedRows()
        #for index in sorted(indices):
         #   model.removeRow(index)
    
    #def deleteTableColumn(self, model):
        #indices = model.selectedColumns()
        #for index in sorted(indices):
        #    model.removeColumn(index)
    
    def addTableRow(self, model):
        count = model.rowCount()
        model.insertRow(count)
        
    
    def addTableColumn(self, model):
        count = model.columnCount()
        model.insertColumn(count)
    
    ## ##
    
    def loadCsv(self, model):
        fileName = QtWidgets.QFileDialog.getOpenFileUrl(self,'Open file',self.appPath,'Comma Separated Values (*.csv)')
        if fileName != ('',''):
            self.fileName = fileName[0].toLocalFile()
            print(fileName)
            with open(self.fileName, "r") as fileInput:
                model.clear()
                for row in csv.reader(fileInput):
                    items = [QtGui.QStandardItem(None)]
                    items.extend(
                        QtGui.QStandardItem(field)
                        for field in row
                        )
                    model.appendRow(items)
                    
                model.setItem(0,0,QtGui.QStandardItem("Flags"))
             
            self.animTable.resizeColumnsToContents()   
            self.animTable.resizeRowsToContents() 
        
    def writeCsv(self, model):
        fileName = QtWidgets.QFileDialog.getSaveFileUrl(self,'Save file',self.appPath,'Comma Separated Values (*.csv)')
        self.fileName = fileName[0].toLocalFile()
        with open(self.fileName, "w", newline='') as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(model.rowCount()):
                fields = [
                    model.data(
                        model.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    for columnNumber in range(model.columnCount())
                ]
                writer.writerow(fields)
    
    def loadCFG(self):
        self.SPIModel.clear()
        self.accessoryModel.clear()
        self.motorModel.clear()
        
        rowSPI = ['Port','Speed','CS','Mode','Bits','Drivers']
        self.SPIModel.insertRow(0,[
                    QtGui.QStandardItem(field) # set logic for table values here
                    for field in rowSPI ])
                    
        accheader = ['Name','File']
        self.accessoryModel.insertRow(0,[
                    QtGui.QStandardItem(field) # set logic for table values here
                    for field in accheader ])
                    
        rowM = ['Type','Name','GPIO','Comp']
        self.motorModel.insertRow(0,[
                    QtGui.QStandardItem(field) # set logic for table values here
                    for field in rowM ])
        
        filename = QtWidgets.QFileDialog.getOpenFileUrl(self, 'Open Config',self.appPath,'Config (*.cfg *.txt)')
        filedata = json.load(open(filename[0].toLocalFile()))
        temp1 = []
        temp2 = []
        temp3 = []
        for elements in filedata['SPI_cfg']:
            temp1.append([elements['port'],elements['speed'],elements['CS'],elements['bits'],elements['mode'],elements['drivers']])
            
        for row in temp1:
            self.SPIModel.insertRow(self.SPIModel.rowCount(),[
                    QtGui.QStandardItem(field) # set logic for table values here
                    for field in row ])
                
        self.SPITable.resizeColumnsToContents()
        self.SPITable.resizeRowsToContents()
        
        for elements in filedata['motor']:
            if elements['type'] != 'sound':
                temp2.append([elements['type'],elements['name'],elements['GPIO']])
            if elements['type'] == 'sound':
                temp3.append([elements['name'],elements['file']])
                
        for row in temp2:
            self.motorModel.insertRow(self.motorModel.rowCount(),[
                    QtGui.QStandardItem(field) # set logic for table values here
                    for field in row ])
                    
        for row in temp3:
            self.accessoryModel.insertRow(self.accessoryModel.rowCount(),[
                    QtGui.QStandardItem(field) # set logic for table values here
                    for field in row ])
            
        self.motorTable.resizeColumnsToContents()
        self.motorTable.resizeRowsToContents()
        self.accessoriesTable.resizeRowsToContents()
    
    def writeCFG(self):
        #self.SPIModel
        #self.accessoryModel
        #self.motorModel
        fileName = QtWidgets.QFileDialog.getSaveFileUrl(self,'Save file',self.appPath,'Config (*.cfg)')
        data = {'SPI_cfg':[],'motor':[]}
        with open(fileName[0].toLocalFile(), "w", newline='') as output:
            for rowNumber in range(1,self.SPIModel.rowCount()):
                if self.SPIModel.data(self.SPIModel.index(rowNumber,0)) != None: # catch blank rows
                    fields = [
                        self.SPIModel.data(
                            self.SPIModel.index(rowNumber, columnNumber),
                            QtCore.Qt.DisplayRole
                        )
                        for columnNumber in range(self.SPIModel.columnCount())
                    ]
                    SPI_Row = {'port':fields[0],
                               'speed':fields[1],
                               'CS':fields[2],
                               'mode':fields[3],
                               'bits':fields[4],
                               'drivers':fields[5]
                                   }
                    
                    data['SPI_cfg'].append(SPI_Row)
                    
            for rowNumber in range(1,self.motorModel.rowCount()):
                if self.motorModel.data(self.motorModel.index(rowNumber,0)) != None:
                    fields = [
                            self.motorModel.data(
                                self.motorModel.index(rowNumber, columnNumber),
                                QtCore.Qt.DisplayRole) 
                            for columnNumber in range(self.motorModel.columnCount())
                            ]
                       
                    motor_Row = {'type':fields[0],
                                 'name':fields[1],
                                 'GPIO':fields[2],
                                 'Comp':fields[3]}        
                        
                    data['motor'].append(motor_Row)
                    
            for rowNumber in range(1,self.accessoryModel.rowCount()):
                if self.accessoryModel.data(self.accessoryModel.index(rowNumber,0)) != None:
                    fields = [
                            self.accessoryModel.data(
                                self.accessoryModel.index(rowNumber, columnNumber),
                                QtCore.Qt.DisplayRole
                            )
                            for columnNumber in range(self.accessoryModel.columnCount())
                        ]
                    acc_Row = {'type':'sound',
                               'name':fields[0],
                               'file':fields[1]
                               }
                    
                    data['motor'].append(acc_Row)
                
                    #if self.DragDrop.count() > 0: 
                     #   for n in range(self.DragDrop.count()):
                      #      item = self.DragDrop.item(n)
                       #     path = str(item.data(0))
                        #    copyfile(path,self.appPath + '/sounds/'+ fields[1]) # copy file to sound folder
                
                        
            self.text.setText(str(data))
            json.dump(data, output)
            
    def writeAnimJson(self):
        
        # CURRENT JSON STRUCTURE
        # [{'Frame','Time','Flags','Data':[
        #        {'Bone1':'','distChanged','Angle X','Angle Y','Angle Z'}},{'Bone2:'',etc...}}]}}
        #  [{etc...}]]
        
        fileName = QtWidgets.QFileDialog.getSaveFileUrl(self,'Save file',self.appPath,'DAT (*.dat)')
        data = []
        header = []
        with open(fileName[0].toLocalFile(), "w", newline='') as output:
            for rowNumber in range(self.animModel.rowCount()):
                fields = [
                    self.animModel.data(
                        self.animModel.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    for columnNumber in range(self.animModel.columnCount())
                ]
                
                # Row Structure
                # 
                # Frame, Time, obj1 localX, obj1 localY, obj1 localZ, obj1 localDistChanged, obj1 localThetaX, obj1 localThetaY, obj1 localThetaZ, obj2 localX, ...
                # Data
                
                # F,T, then X,Y,Z,D,T_X,T_Y,T_Z
                #print(rowNumber, fields,'\n')
                
                if rowNumber == 0:
                    for colNumber in range(self.animModel.columnCount()):
                        if colNumber == 1 or colNumber == 2:
                            header.extend([fields[colNumber]])
                            if colNumber == 2:
                                header.extend([fields[0]])
                        
                        indexmaths = (colNumber-3)/7
                        if colNumber == 3 or int(indexmaths) == indexmaths: 
                            name = ''
                            for char in fields[colNumber]:
                                if char == '/':
                                    break
                                name = name + char
                            header.extend([name[:-1]])
                    #print(header)
                if rowNumber > 0:
                    jsonRow = {header[0]:fields[1][6:] , header[1]:fields[2], header[2]:fields[0], 'data':[]}
                    for colNumber in range(self.animModel.columnCount()):
                        indexmaths = (colNumber-3)/7
                        if colNumber == 3:
                            jsonRow['data'].append({
                                   'name': header[3],
                                   'distChanged':fields[colNumber+3],
                                   'Angle X':fields[colNumber+4],
                                   'Angle Y':fields[colNumber+5],
                                   'Angle Z':fields[colNumber+6]})
                        else: 
                            if int(indexmaths) == indexmaths:
                                jsonRow['data'].append({
                                       'name':header[int(indexmaths)+3],
                                       'distChanged':fields[colNumber+3],
                                       'Angle X':fields[colNumber+4],
                                       'Angle Y':fields[colNumber+5],
                                       'Angle Z':fields[colNumber+6]})
                    data.append(jsonRow)
                    
            self.text2.setText(str(data))
            json.dump(data, output)
                    

    def openBlender(self):
        anim_path = QtWidgets.QFileDialog.getOpenFileUrl(self,'Open animation', os.path.expanduser('~'), 'Blend (*.blend)') # ; Autodesk FBX or 3Ds; Collada; Alembic (*.fbx *.3ds *.dae *.abc)
        if anim_path != ('',''):
            script_path1 = self.appPath + 'openBlender.py'
            
            DETACHED_PROCESS = 0x00000008
            p1 = subprocess.Popen([self.bPath, '--python', script_path1, anim_path[0].toLocalFile()],shell=True, creationflags=DETACHED_PROCESS)
            p1.wait()
            
            script_path2 = self.appPath + '//getData.py'
            output_path = 'data//'
            
            p2 = subprocess.Popen([self.bPath, '-b', '--python', script_path2, output_path, anim_path[0].toLocalFile()], shell=True)
            p2.wait()
            fileName = output_path+'bone_data.csv'
            print(fileName)
            """ !!! """
            with open(fileName, "r") as fileInput:
                self.animModel.clear()
                for row in csv.reader(fileInput):  
                    items = [QtGui.QStandardItem(None)]
                    items.extend([
                        QtGui.QStandardItem(field) # set logic for table values here
                        for field in row ])
        
                    self.animModel.appendRow(items)
                self.animModel.setItem(0,0,QtGui.QStandardItem("Flags"))
            
            self.animTable.resizeColumnsToContents()
            self.animTable.resizeRowsToContents() 
        else:
            DETACHED_PROCESS = 0x00000008
            p1 = subprocess.Popen([self.bPath],shell=True, creationflags=DETACHED_PROCESS)
            p1.wait()
            self.importAnim()
        
    def importAnim(self):
        anim_path = QtWidgets.QFileDialog.getOpenFileUrl(self,'Open animation', os.path.expanduser('~'), 'Blend (*.blend )') # ; Autodesk FBX or 3Ds; Collada; Alembic (*.fbx *.3ds *.dae *.abc)
        if anim_path != ('',''):
            script_path = self.appPath + '//getData.py'
            output_path = 'data//'
            p2 = subprocess.Popen([self.bPath, '-b', '--python', script_path, output_path, anim_path[0].toLocalFile()],shell=True)
            p2.wait()
            fileName = output_path+'bone_data.csv'
            print(fileName)
            
            with open(fileName, "r") as fileInput:
                self.animModel.clear()
                for row in csv.reader(fileInput):
                    items = [QtGui.QStandardItem(None)]
                    items.extend([
                        QtGui.QStandardItem(field) # set logic for table values here
                        for field in row ])
                    self.animModel.appendRow(items)
                self.animModel.setItem(0,0,QtGui.QStandardItem("Flags"))
    
                
            self.animTable.resizeColumnsToContents()    
            self.animTable.resizeRowsToContents()     
                
    def setBlenderPath(self):
        blender_path = QtWidgets.QFileDialog.getOpenFileUrl(self, 'Select Blender Editor', os.path.expanduser('~'), 'blender.exe, bforartists.exe, etc. (*.exe)')
        if len(blender_path[0].toLocalFile()) > 1:
            self.bPath = blender_path[0].toLocalFile()
            self.Config['Init']['blender_path'] = self.bPath
            with open(self.appPath+'//init.ini', 'w') as configfile:
                self.Config.write(configfile)
                
    def setPiPath(self):
        pi_path, ok = QtWidgets.QInputDialog.getText(self, 'Input','Enter Host Address (e.g. http://localhost:9000):')
        if ok:
            self.piPath = pi_path
            self.Config['Init']['pi_path'] = self.piPath
            with open(self.appPath+'//init.ini','w') as configfile:
                self.Config.write(configfile)
            print('Success')
            
        
    # Saves memory, provides C++ signatures.
    @QtCore.pyqtSlot()
    def on_pushButtonWrite_clicked(self):
        self.writeCsv(self.animModel)

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.loadCsv(self.animModel)
        
    @QtCore.pyqtSlot()
    def on_pushButtonIM_clicked(self):
        self.loadCFG()
        
    @QtCore.pyqtSlot()
    def on_pushButtonOB_clicked(self):
        self.openBlender()
      
    @QtCore.pyqtSlot()
    def on_pushButtonIA_clicked(self):
        self.importAnim()
   
    @QtCore.pyqtSlot()
    def on_addAnimRowBtn_clicked(self):
        self.addTableRow(self.animModel)

     
    @QtCore.pyqtSlot()
    def on_addSPIBtn_clicked(self):
        self.addTableRow(self.SPIModel)

    @QtCore.pyqtSlot()
    def on_addGPIOBtn_clicked(self):
        self.addTableRow(self.motorModel)
        
    @QtCore.pyqtSlot()
    def on_setBlenderPath_clicked(self):
        self.setBlenderPath()
        
    @QtCore.pyqtSlot()
    def on_setPiPath_clicked(self):
        self.setPiPath()
        
    @QtCore.pyqtSlot()
    def deleteItem(self):
        self.deleteListItem()
        
    @QtCore.pyqtSlot()
    def on_writeSaveCfg_clicked(self):
        self.writeAnimJson()
      
    @QtCore.pyqtSlot()
    def on_writeSaveMCfg_clicked(self):
        self.writeCFG()
    
    @QtCore.pyqtSlot()
    def on_saveFiles_clicked(self):
        items = self.returnListItems(self.DragDrop)
        url = self.piPath+'/copy_files'
        files = []
        for item in items:
            files.append(tuple(['file',item]))

        r = requests.post(url,files=files)
        print(r.text)
    
    # Copies necessary data to piPath to be executed on the Pi Server
    @QtCore.pyqtSlot()
    def on_TestRun_clicked(self):
        motorCFGPath = QtWidgets.QFileDialog.getOpenFileUrl(self, 'Open Config',self.appPath,'Config (*.cfg *.txt)')
        animCFGPath = QtWidgets.QFileDialog.getOpenFileUrl(self,'Save file',self.appPath,'DAT (*.dat)')

        url = self.piPath+'/animate'
    
        json1 = json.load(open(motorCFGPath[0].toLocalFile()))
        json2 = json.load(open(animCFGPath[0].toLocalFile()))
        jsondat = [json1,json2]
        
        r = requests.post(url, json=jsondat)
        print(r.text)
        
        #Temporarily copies files to the piPath location where it can be run on the Pi's shell.
        #Ex: os.system('python TestRun.py motor.cfg anim.dat')
        #copyfile(motorCFGPath[0].toLocalFile(),self.piPath+'//'+motorCFGPath[0].fileName())
        #copyfile(animCFGPath[0].toLocalFile(),self.piPath+'//'+animCFGPath[0].fileName())
        #copyfile(self.appPath+'//TestRun.py',self.piPath+'//TestRun.py')
        #copyfile(self.appPath+'//run_TestRun.py',self.piPath+'//run_TestRun.py')
        #script_path = self.appPath + 'TestRun.py'
        #subprocess.call(['python', script_path, motorCFGPath[0], animCFGPath[0]])

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()