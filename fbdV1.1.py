# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 14:06:20 2021

@author: maxan
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 23:00:26 2021

@author: maxan
"""
from tkinter import *  
from tkinter import ttk
import os
from tkinter import messagebox
from vpython import *
import random
from pandastable import Table, TableModel
from pandastable import Table
from pandastable import images
from pandastable.dialogs import addButton
import pandas as pd
import re
import numpy as np
import sympy as sp
from sympy.vector import CoordSys3D

scene = canvas()
scene.width = 600
scene.height = 600
scene.range = 30
scene.userspin = True
y = arrow(pos=vector(0,0,0), axis=vector(0,10,0), shaftwidth=0.5, color=color.red)
x = arrow(pos=vector(0,0,0), axis=vector(10,0,0), shaftwidth=1/2, color=color.green)
z = arrow(pos=vector(0,0,0), axis=vector(0,0,10), shaftwidth=1/2, color=color.blue)
#box(pos= vec(0,0,0), size = vec(8,4,4))
xt = text(text='x', axis=x.axis, pos=x.axis, height = 1)
yt = text(text='y', axis=y.axis, pos=y.axis, height = 1)
zt = text(text='z', axis=z.axis, pos=z.axis, height = 1)

temp_point = []
temp_sphere = []
temp_pointstr = ''

spin = scene.userspin
fwd = scene.forward

a = CoordSys3D('a')
clicks = False
def getevent(evt):
    global lasthit, lastpick, lastcolor,temp_point, clicks
    hit = scene.mouse.pick
    
    if hit != None:
        lasthit = hit
        lastpick = None
        if isinstance(hit, box) and clicks == False:  # pick individual point of curve
            #lastpick = hit.segment
            lastcolor = vector(hit.color) # make a copy
            hit.color = color.red
            clicks = True
        elif isinstance(hit, box) and clicks == True:  # pick individual point of curve
            #lastpick = hit.segment
            lastcolor = vector(hit.color) # make a copy
            hit.color = color.white
            clicks = False
        return clicks
    elif hit == None:
        loc = evt.pos
        temp_point.append(loc)
        temp_sphere.append(sphere(pos=loc, radius= 2, color=color.cyan))
        if len(temp_point) > 1:
            for spheres in range(0,len(temp_point)-1):
                s = temp_sphere[spheres] 
                s.visible = False
                del s
        print(str(loc))
        temp_pointstr = vec2str(loc)
        #print(temp_pointstr)
        return temp_point,loc,temp_sphere, temp_pointstr
  
def clearShapes(scene,shape):
    global x,y,z
    if shape == "arrows":
        for obj in scene.objects:
            print("object", obj)
            if isinstance(obj,arrow) and obj!= x and obj!= y and obj!=z and isinstance(obj,text) and obj!=xt and obj!= yt and obj!= zt:
                print("arrow", obj)
                obj.visible = False
                del obj
            if isinstance(obj,text) and obj!=xt and obj!= yt and obj!= zt:
                obj.visible = False
                del obj
    elif shape == 'beams':
        for obj in scene.objects:
            print("object", obj)
            if isinstance(obj,box) and isinstance(obj,text) and obj!=xt and obj!= yt and obj!= zt:
                print("box", obj)
                obj.visible = False
                del obj
            if isinstance(obj,text) and obj!=xt and obj!= yt and obj!= zt:
                obj.visible = False
                del obj
    return scene

def findSumOfForces(force):
    directionVector = force['Force Direction'].split(',')
    return [str(direction)+'*'+force['Force Name'] for direction in directionVector]

def findSumOfForcesunknowns(force):
    directionVector = force['Force Direction'].split(',')
    return [str(direction)+'*'+force['Force Value'] for direction in directionVector]

def combine(columns):
    return sp.sympify('+'.join(columns.to_list()))


    
def str2array(a):
    a = a.replace(" ", '')
    a = a.split(',')
    a = [float(n) for n in a]
    return a

def array2str(a):
    s = ''
    s = str(a[0]) + ','+ str(a[1]) + ','+ str(a[2]) 
    return s
    
def roun(n):
    a = ((n // 10) *10) + 10
    return a

def scale(n,m):
    if abs(n) > 10:
        if n != m:
            b = roun(m)
        elif n==m:
            b = roun(n)
        x = (n/b) * 10
    else:
        x = n
    return x

def round_new(n,v):
    a = ((n // v) * v) + v
    return a


def scale_new(n, m,v):
    if n != m:
        b = round_new(m,v)
    elif n == m:
        b = round_new(n,v)
    x = (n / b) * v
    
    return x

def vec2str(v):
    a = []
    a.append(round(v.x,3))
    a.append(round(v.y,3))
    a.append(round(v.z,3))
    s = array2str(a)
    return s

def dataframe_difference(df1, df2, which=None):
    """Find rows which are different between two DataFrames."""
    comparison_df = df1.merge(df2,indicator=True,how='outer')
    if which is None:
        diff_df = comparison_df[comparison_df['_merge'] != 'both']
    else:
        diff_df = comparison_df[comparison_df['_merge'] == which]
    #diff_df.to_csv('data/diff.csv')
    return diff_df

def findSumOfMoments(force, point):
    print('dir',force['Force Direction'])
    directionVector = str2array(force['Force Direction'])
    F = np.array(directionVector)
    print(F)
    print('point',point)
    r = np.array(str2array(force['Force Position'])) - point
    print(r)
    Moment = np.cross(r,F)
    print('moment', Moment)
    return [str(eachMoment)+'*'+force['Force Name'] for eachMoment in Moment]

def findSumOfMomentsunknowns(force, point):
    print('dir',force['Force Direction'])
    directionVector = str2array(force['Force Direction'])
    F = np.array(directionVector)
    print(F)
    print('point',point)
    r = np.array(str2array(force['Force Position'])) - point
    print(r)
    Moment = np.cross(r,F)
    print('moment', Moment)
    return [str(eachMoment)+'*'+force['Force Value'] for eachMoment in Moment]


def drawShapes(a,shape,c = color.magenta):
    print(a)
    if shape == 'arrows':
        pos_force= str2array(a["Force Position"])
        dir_force= str2array(a["Force Direction"])
        n_force= a['Force Name_y']
        arrow(pos = vec(pos_force[0],pos_force[1],pos_force[2]),
          axis = 5*vec(dir_force[0],dir_force[1],dir_force[2]), color = c)
        text(pos = vec(pos_force[0],pos_force[1]+3,pos_force[2]), text = n_force)
    elif shape == 'beams':
        start_node = str2array(a["Start Node Pos"])
        end_node = str2array(a["End Node Pos"])
        start_node_name = a["Start Node"]
        end_node_name = a["End Node"]
        vector_length = np.array(end_node) - np.array(start_node)
        vector_length= np.array([scale(n,np.max(vector_length)) for n in vector_length])
        print(vector_length)
        centerpos = np.array(start_node) +  vector_length/2
        print(centerpos , "centerpos")
        length = np.linalg.norm(vector_length)
        h = 1
        print("length", length)
        
        box(pos = vec(centerpos[0],centerpos[1],centerpos[2]),axis = vec(vector_length[0],vector_length[1],vector_length[2]),
                        size = vec(length,h,h))
        text(text = start_node_name,pos = vec(start_node[0],start_node[1]+2,start_node[2]),height = 1)
        text(text = end_node_name,pos = vec(end_node[0],end_node[1]+2,end_node[2]),height = 1)

scene.bind("mousedown", getevent)

class ComboboxSelectionWindow():
    def __init__(self, master):
        self.master = master
        #self.winfo_toplevel().title("Free Body Diagram Solver V1.1")
        self.bg = PhotoImage(file = "stock.png", master = app)
        self.label1 = Label(master,image = self.bg, bg = 'grey')
        self.label1.place(x=0,y=0, relwidth=1, relheight=1)
        # self.canvas1 = Canvas(master, height = 600, width = 600)
        # self.canvas1.pack()
        # self.canvas1.create_image((0,0), image=self.bg, anchor=SW)
        self.entry_contents=None
        self.path = 'Test_FBD'
        self.comboBox_example = Label(master, text = "Enter a Chapter" )
        self.comboBox_example.place(x=280, y = 100)
        #self.labelTop.place(x = 250, y = 100, width=140, height=25)
        self.comboBox_example = ttk.Combobox(master,values= os.listdir(self.path))
        #self.comboBox_example.current(0)
        self.comboBox_example.place(x = 250, y = 130, width=140, height=25)

        self.okButton = Button(master, text='Ok',command = self.callback)
        self.okButton.place(x = 250, y = 160, width=140, height=25)

    def callback(self):
        """ get the contents of the Entry and exit
        """
        self.comboBox_example_contents=self.comboBox_example.get()
        self.folder1 = self.comboBox_example_contents 
        print(self.folder1)
        self.pick()
        
    def pick(self):
        master = self.master
        self.entry = None
        self.label = Label(master,text = "Pick Problem")
        self.label.place(x = 250, y = 200, width=140, height=25)
        self.comboBox = ttk.Combobox(master,values= os.listdir(self.path + '/' + self.folder1) )
        self.comboBox.place(x = 250, y = 220, width=140, height=25)

        self.ok = Button(master, text='Start',command = self.callback2)
        self.ok.place(x = 250, y = 250, width=140, height=25)
    
    def callback2(self):
        self.combo2_contents = self.comboBox.get()
        self.folder2 = self.combo2_contents
        self.start_problem()

    def start_problem(self):
        global temp_pointstr,scene
        self.start_problem = Toplevel(self.master)
        frame = self.start_problem
        menu = Menu(frame)
        self.start_problem.config(menu = menu)
        self.temp_point = temp_pointstr
        fileMenu = Menu(menu,tearoff =0)
        pickUser = Menu(menu,tearoff = 0)
        menu.add_cascade(label = 'View', menu = fileMenu)
        menu.add_cascade(label = 'User', menu = pickUser)
        fileMenu.add_command(label = '2D', command = self.switch2D)
        fileMenu.add_command(label = 'XY', command = self.switchXY)
        fileMenu.add_command(label = 'YZ', command = self.switchYZ)
        #fileMenu.add_command(label = 'ZX', command = self.switchZX)
        fileMenu.add_command(label="Exit", command=frame.quit)
        pickUser.add_command(label = 'Instructor', command = self.switch2instructor)
        pickUser.add_command(label = "Student", command = self.switch2User)
        
        #menu.add_cascade(label = 'User', menu = fileMenu)
        #usermenu = Menu(menu, tearoff = 0)
        #usermenu.add_command(label = 'Student', command = self.switch2student)
        #usermenu.add_command(label = 'Instructor', command = self.switch2instructor)
        
        for f in os.listdir(self.path + '/' + self.folder1+'/' + self.folder2 ):
            name, ext = os.path.splitext(f)
            if ext == '.xlsx':
                xlsx_path = self.path + '/' + self.folder1+'/' + self.folder2 + '/' + name + ext
            elif ext == '.PNG':
                self.pic_path = self.path + '/' + self.folder1+'/' + self.folder2 + '/' + name + ext
                print(self.pic_path)
        xl_file = pd.ExcelFile(xlsx_path)

        self.dfs = {sheet_name: xl_file.parse(sheet_name).astype(str)
               for sheet_name in xl_file.sheet_names}
        title = Label(frame,text="Free Body Diagram of a Cantilever beam", bg='white', font=("Arial bold", 20))
        title.grid(row = 0, column = 0)
        self.bg2 = PhotoImage(file = self.pic_path, master = frame)
        # self.label1 = tk.Label(master,image = self.bg, bg = 'grey')
        # self.label1.place(x=0,y=0, relwidth=1, relheight=1)
        self.canvas2 = Canvas(frame, height = 300, width = 500)
        self.canvas2.grid(row = 5, column = 0)
        self.canvas2.create_image((0,0), image=self.bg2, anchor=NW)

        # userbutton = Button(frame, text="User", command = self.inputUser)
        # userbutton.pack(side = LEFT)
        # inpButton = Button(frame, text="Input Coordinates for beam", command = self.inputNode)
        # inpButton.pack(side = LEFT)
        # beam_structure_table = Button(frame,text = "Show Beam Table", command = self.showBeamTable)
        # beam_structure_table.pack(side = LEFT)
        # check_beams = Button(frame,text = "Check Beams", command = self.checkBeams)
        # check_beams.pack(side = LEFT)
        # forces = Button(frame,text = "Add forces", command = self.addForceinfo)
        # forces.pack(side = LEFT)
        # loads = Button(frame,text = "Add distributed loading", command = self.forceDistribution)
        # loads.pack(side = LEFT)
        # force_structure_table = Button(frame,text = "Show Force Table", command = self.showForceTable)
        # force_structure_table.pack(side = LEFT)
        # check_forces = Button(frame,text = "Check Forces", command = self.checkForces)
        # check_forces.pack(side = LEFT)
        # eqns = Button(frame,text = "Enter Equations", command = self.enterEquations)
        # eqns.pack(side = LEFT)
        # unknowns = Button(frame, text = 'Enter unknown forces', command = self.inputunknowns)
        # unknowns.pack(side = LEFT)
        
        self.canvas3 = Canvas(frame)
        self.canvas3.grid(row =1, column =0)
        strucButton = Button(self.canvas3, text = "Structure", command = self.structureInfo)
        strucButton.grid(row = 1, column = 0, padx = 20, pady = 20)
        self.canvas3.update()
        
        forceButton = Button(self.canvas3, text = "Forces", command = self.forceInfo)
        forceButton.grid(row = 1, column = 2, padx = 20, pady = 20)
        self.canvas3.update()
        # self.canvas3.create_line(forceButton.winfo_x()+80,forceButton.winfo_y(),
        #                         forceButton.winfo_x() +140,forceButton.winfo_y() ,arrow = LAST)
        
        eqns = Button(self.canvas3,text = "Enter Equations", command = self.enterEquations)
        eqns.grid(row = 1, column = 4, padx= 20,  pady = 20)
        self.canvas3.update()
        #self.canvas3.create_line(eqns.winfo_width()+120,eqns.winfo_height(),
                                 #eqns.winfo_width() +160,eqns.winfo_height() ,arrow = LAST)
        
        unknowns = Button(self.canvas3,text = "Enter unknown forces", command = self.inputunknowns)
        unknowns.grid(row = 1, column = 6, padx= 20,  pady = 20)
        self.canvas3.update()
        
        self.step1 = self.canvas3.create_line(strucButton.winfo_x()+strucButton.winfo_width(),strucButton.winfo_y()+0.5*strucButton.winfo_y(),
                                 forceButton.winfo_x(),strucButton.winfo_y()+0.5*strucButton.winfo_y(),arrow = LAST, width = 3)
        
        self.step2 = self.canvas3.create_line(forceButton.winfo_x()+forceButton.winfo_width(),forceButton.winfo_y()+0.5*forceButton.winfo_y(),
                                 eqns.winfo_x(),forceButton.winfo_y()+0.5*forceButton.winfo_y(),arrow = LAST, width = 3)
        
        self.step3 = self.canvas3.create_line(eqns.winfo_x()+eqns.winfo_width(),eqns.winfo_y()+0.5*eqns.winfo_y(),
                                 unknowns.winfo_x(),eqns.winfo_y()+0.5*eqns.winfo_y(),arrow = LAST, width = 3)
        
        self.checkstep1 = False
        self.checkstep2 = False
        
        self.val = StringVar(temp_pointstr)
        print(self.val.get())
        self.unknown_forces_mag = []
        self.unknown_forces_vars = []
        self.known_forces_vars = []
        self.known_forces_mag = []
        self.beam_names = ['0']
        self.start_nodes_names = ['0']
        self.start_nodes_pos = ['0']
        self.end_nodes_names = ['0']
        self.end_nodes_pos = ['0']
        self.beam_positions = ['0']
        self.beam_dimensions = ['0']
        self.force_name_array = ['0']
        self.force_mag_array = ['0']
        self.force_pos_array = ['0']
        self.force_dir_array = ['0']
            
        self.d = {"Force Name": self.force_name_array, "Force Value": self.force_mag_array,
                  "Force Position": self.force_pos_array, "Force Direction": self.force_dir_array}
        self.force_data = pd.DataFrame(self.d)
        
        self.beam_diction = {"Start Node" : self.start_nodes_names, "Start Node Pos":self.start_nodes_pos,  
                          "End Node" : self.end_nodes_names, "End Node Pos":self.end_nodes_pos,}
        self.beam_data = pd.DataFrame(self.beam_diction)
        self.check = False
        self.userCheck = False
        if self.check == False:
            eqns.state = DISABLED
        #draw_button.grid(row=i+1, column=3,columnspan=3, pady=2, sticky='WE')
        #forceButton = Button(frame, text="Save Solution", command = self.forces)
        #forceButton.pack()
        #self.buttons = [inpButton, forceButton]
    
    def structureInfo(self):
        self.strucInfo = Toplevel(self.start_problem)
        self.strucInfo.geometry('300x300+600+300')
        inpNode = Button(self.strucInfo, text="Input Coordinates for beam", command = self.inputNode)
        inpNode.pack(side = TOP, pady = 20)
        inpTable = Button(self.strucInfo,text = "Show Beam Table", command = self.showBeamTable)
        inpTable.pack(side = TOP, pady = 20)
        check_beams = Button(self.strucInfo,text = "Check Beams", command = self.checkBeams)
        check_beams.pack(side = TOP, pady = 20)
    
    def forceInfo(self):
        self.forcInfo = Toplevel(self.start_problem)
        self.forcInfo.geometry('300x300+600+300')
        frame = self.forcInfo
        forces = Button(frame,text = "Add forces", command = self.addForceinfo)
        forces.pack(pady = 20)
        loads = Button(frame,text = "Add distributed loading", command = self.forceDistribution)
        loads.pack(pady = 20)
        force_structure_table = Button(frame,text = "Show Force Table", command = self.showForceTable)
        force_structure_table.pack(pady = 20)
        check_forces = Button(frame,text = "Check Forces", command = self.checkForces)
        check_forces.pack(pady = 20)
    
    
        
    def selectUser(self):
        self.user.destroy()
        selection = self.var.get()
        if selection == 1:
            self.userCheck = False
        else:
            self.userCheck = True
    def inputNode(self):
        self.inputNode = Toplevel(self.start_problem)
        inputNode = self.inputNode
        Label(inputNode, text = 'Name of start node').grid(row = 1, column = 1)
        self.start_node_name = Entry(inputNode)
        self.start_node_name.grid(row = 1, column = 2)
        
        Label(inputNode, text = 'Position of start node').grid(row = 2, column = 1)
        self.start_node_pos = Entry(inputNode)
        self.start_node_pos.grid(row = 2, column = 2)
        
        Label(inputNode, text = 'Name of end node').grid(row = 3, column = 1)
        self.end_node_name = Entry(inputNode)
        self.end_node_name.grid(row = 3, column = 2)
        
        Label(inputNode, text = 'Position of end node').grid(row = 4, column = 1)
        self.end_node_pos = Entry(inputNode)
        self.end_node_pos.grid(row = 4, column = 2)
        
        submit_button=Button(inputNode,text="Submit",command=self.drawbeamnodes)
        submit_button.grid(row=5, column=2,columnspan=3, pady=2, sticky='WE')   
    
    def addBeamtoTable(self):
        self.beam_diction = {"Start Node" : self.start_nodes_names, "Start Node Pos":self.start_nodes_pos,  
                          "End Node" : self.end_nodes_names, "End Node Pos":self.end_nodes_pos,}
        self.beam_data = pd.DataFrame(self.beam_diction)
    
    def drawbeamnodes(self):
        start_node = str2array(self.start_node_pos.get())
        end_node = str2array(self.end_node_pos.get())
        start_node_name = self.start_node_name.get()
        end_node_name = self.end_node_name.get()
        self.start_nodes_name.append(start_node_name)
        self.end_nodes_name.append(end_node_name)
        self.start_nodes_pos.append(start_node)
        self.end_nodes_pos.append(end_node)
        vector_length = np.array(end_node) - np.array(start_node)
        vector_length= np.array([scale(a,np.max(vector_length)) for a in vector_length])
        centerpos = vector_length/2
        print(centerpos , "centerpos")
        length = np.linalg.norm(vector_length)
        h = 2
        if length<=5:
            h = 1
        print("length", length)
        box(pos = vec(centerpos[0],centerpos[1],centerpos[2]), size = vec(length,h,h))
        text(text = start_node_name,pos = vec(start_node[0],start_node[1]+3,start_node[2]),height = 1)
        text(text = end_node_name,pos = vec(end_node[0],end_node[1]+3,end_node[2]),height = 1)
        self.addBeamtoTable
        self.inputNode.destroy()
    
    def switch2User(self):
        self.userCheck = False
    
    def switch2instructor(self):
        self.userCheck = True
    
    def switch2D(self):
        global spin,fwd
        #spin = False
        scene.userspin = False
        scene.forward = vec(0,0,-1)
        return scene.userspin,scene.forward
    
    def switchXY(self):
        global spin,fwd
        spin = True
        scene.userspin = True
        scene.forward = vec(0,0,-1)
        return scene.userspin
    
    def switchYZ(self):
        global spin,fwd
        spin = True
        scene.userspin = True
        scene.forward = vec(1,0,0)
        return scene.userspin
        
    def addForceinfo(self):
        global temp_pointstr
        self.addForceInfo = Toplevel(self.forcInfo)
        addforceinfo = self.addForceInfo
        
        Label(addforceinfo, text = 'Name of force').grid(row = 1, column = 1)
        self.name_force = Entry(addforceinfo)
        self.name_force.grid(row = 1, column = 2)
        
        Label(addforceinfo, text = 'Magnitude of Force').grid(row = 2, column = 1)
        self.mag_force = Entry(addforceinfo)
        self.mag_force.grid(row = 2, column = 2)
        #self.force_mag_array.append(self.mag_force.get())
        
        
        Label(addforceinfo, text = 'Position of force').grid(row = 3, column = 1)
        self.pos_force = Entry(addforceinfo, textvariable = self.val)
        #self.pos_force.bind('<Return>', array2str(temp_point))
        self.pos_force.grid(row = 3, column = 2)
        
        
        Label(addforceinfo, text = 'Direction of force').grid(row = 4, column = 1)
        self.dir_force = Entry(addforceinfo)
        self.dir_force.grid(row = 4, column = 2)
        
        
        draw_button = Button(addforceinfo, text = "Draw force",command = self.drawforces).grid(row = 5, column = 2)
    
    def inputUser(self):
        self.user = Toplevel(self.start_problem)
        self.var = IntVar()
        R1 = Radiobutton(self.user, text="Student", variable=self.var, value=1)
        R1.pack( anchor = W )
        R2 = Radiobutton(self.user, text="Instructor", variable=self.var, value=2)
        R2.pack( anchor = W )
        submit = Button(self.user, text = "Submit", command = self.selectUser)
        submit.pack()
    
    def forceDistribution(self):
        self.forcedistribution = Toplevel(self.forcInfo)
        self.var = IntVar()
        
        uni_dist_button = Radiobutton(self.forcedistribution, text = "Uniform forced Loading", variable = self.var, value = 1)
        uni_dist_button.grid(row = 1, column=1)
        var_dist_button = Radiobutton(self.forcedistribution, text = "Varying forced Loading", variable = self.var, value = 2)
        var_dist_button.grid(row = 1,column = 3)
        
        submit = Button(self.forcedistribution, text = "Submit", command =  self.inputDistribution)
        submit.grid(row = 3, column = 2)
        
    def inputDistribution(self):
        print("open,", self.var)
        #self.forcedistribution = Toplevel(self.forcedistribution)
        if int(self.var.get()) == 1:
        
            Label(self.forcedistribution, text = 'Name of force Loading').grid(row = 5, column = 1)
            self.name_uni_load = Entry(self.forcedistribution)
            self.name_uni_load.grid(row = 5, column = 2)
            
            Label(self.forcedistribution, text = 'initial magnitude of Force loading').grid(row = 6, column = 1)
            self.in_mag_var_load = Entry(self.forcedistribution)
            self.in_mag_var_load.grid(row = 6, column = 2)
            #self.force_mag_array.append(self.mag_force.get())
            
            Label(self.forcedistribution, text = 'final magnitude of Force loading').grid(row = 7, column = 1)
            self.fin_mag_var_load = Entry(self.forcedistribution)
            self.fin_mag_var_load.grid(row = 7, column = 2)
            #self.force_mag_array.append(self.mag_force.get())
            
            Label(self.forcedistribution, text = 'start position of Force loading').grid(row = 8, column = 1)
            self.startpos_var_load = Entry(self.forcedistribution)
            self.startpos_var_load.grid(row = 8, column = 2)
            #self.force_mag_array.append(self.mag_force.get())
            
            Label(self.forcedistribution, text = 'end position of Force loading').grid(row = 9, column = 1)
            self.endpos_var_load = Entry(self.forcedistribution)
            self.endpos_var_load.grid(row = 9, column = 2)
            #self.force_mag_array.append(self.mag_force.get())
            
            Label(self.forcedistribution, text = 'Direction of Force loading').grid(row = 10, column = 1)
            self.dir_var_load = Entry(self.forcedistribution)
            self.dir_var_load.grid(row = 10, column = 2)
            #self.force_mag_array.append(self.mag_force.get())
            draw_loading = Button(self.forcedistribution, text = "Draw Loading", command = self.varloadDraw).grid(row = 11, column = 2)
        
        elif int(self.var.get()) == 2:
        
            #self.forcedistribution = Toplevel(self.forcedistribution)
            
            Label(self.forcedistribution, text = 'Name of force Loading').grid(row = 5, column = 1)
            self.name_uni_load = Entry(self.forcedistribution)
            self.name_uni_load.grid(row = 5, column = 2)
            
            Label(self.forcedistribution, text = 'Magnitude of Force loading').grid(row = 6, column = 1)
            self.mag_uni_load = Entry(self.forcedistribution)
            self.mag_uni_load.grid(row = 6, column = 2)
            #self.force_mag_array.append(self.mag_force.get())
            
            
            Label(self.forcedistribution, text = 'start position of force').grid(row = 7, column = 1)
            self.startpos_uni_load = Entry(self.forcedistribution, textvariable = self.val)
            #self.pos_force.bind('<Return>', array2str(temp_point))
            self.startpos_uni_load.grid(row = 7, column = 2)
            
            
            Label(self.forcedistribution, text = 'end position of force').grid(row = 8, column = 1)
            self.endpos_uni_load = Entry(self.forcedistribution)
            self.endpos_uni_load.grid(row = 8, column = 2)
            
            Label(self.forcedistribution, text = 'direction of force').grid(row = 9, column = 1)
            self.dir_uni_load = Entry(self.forcedistribution)
            self.dir_uni_load.grid(row = 9, column = 2)
            
            draw_loading = Button(self.forcedistribution, text = "Draw Loading", command = self.uniloadDraw).grid(row = 10, column = 2)    
        
    def varloadDraw(self):
        startpos = str(self.startpos_var_load.get())
        endpos = str(self.endpos_var_load.get())
        dirload = str2array(str(self.dir_var_load.get()))
        in_mag = float(self.in_mag_var_load.get())
        fin_mag = float(self.fin_mag_var_load.get())
        
        
        diff = (np.array(str2array(endpos)) - np.array(str2array(startpos)))/10
        initial = np.array(str2array(startpos))
        
        if in_mag < fin_mag:
            for i in range(10):
                v = scale_new(in_mag, fin_mag,3)
                arrow(pos = vec(initial[0],initial[1],initial[2]),
                      axis = v*vec(dirload[0],dirload[1],dirload[2]), color=color.orange)
                initial = initial + diff
                #v = scale_new(in_mag, fin_mag,3)
                in_mag += fin_mag/10
                print(initial, v)
        elif in_mag > fin_mag:
            for i in range(10):
                v = scale_new(in_mag, fin_mag,3)
                arrow(pos = vec(initial[0],initial[1],initial[2]),
                      axis = v*vec(dirload[0],dirload[1],dirload[2]), color=color.orange)
                initial = initial + diff
                in_mag -= fin_mag/10
                print(initial, v)
        self.forcedistribution.destroy()
        #self.forcedistribution.destroy()
        
    
        
    def uniloadDraw(self):
        startpos = str(self.startpos_uni_load.get())
        endpos = str(self.endpos_uni_load.get())
        dirload = str2array(str(self.dir_uni_load.get()))
        magload = int(self.mag_uni_load.get())
        
        diff = (np.array(str2array(endpos)) - np.array(str2array(startpos)))/10
        initial = np.array(str2array(startpos))
        for i in range(10):
            arrow(pos = vec(initial[0],initial[1],initial[2]),
                  axis = 3*vec(dirload[0],dirload[1],dirload[2]), color=color.orange)
            initial = initial + diff
            print(initial)
        self.force_mag_array.append(int(magload)*diff*10)
        self.force_name_array.append(self.name_uni_load.get())
        self.force_pos_array.append(diff*5)
        self.force_dir_array.append(str(self.dir_uni_load.get()))
        self.addForcetoTable()
        self.forcedistribution.destroy()
        #self.forcedistribution.destroy()
    
    def drawforces(self):
        #print(self.name_force,self.mag_force)
        pos_force = self.pos_force.get()
        dir_force = self.dir_force.get()
        n_force = self.name_force.get()
        self.force_name_array.append(str(n_force))
        self.force_mag_array.append(str(self.mag_force.get()))
        self.force_pos_array.append(str(pos_force))
        self.force_dir_array.append(str(dir_force))
        
        pos_force= str2array(pos_force)
        dir_force= str2array(dir_force)
        
        print('drawn')
        arrow(pos = vec(pos_force[0],pos_force[1],pos_force[2]),
              axis = 5*vec(dir_force[0],dir_force[1],dir_force[2]), color = color.magenta)
        text(pos = vec(pos_force[0],pos_force[1],pos_force[2]), text = n_force )
        print(self.force_name_array,self.force_mag_array, self.force_pos_array,self.force_dir_array)
        self.addForcetoTable()
        self.addForceInfo.destroy()
    
    def addForcetoTable(self):
        self.forcediction = {"Force Name": self.force_name_array, "Force Value": self.force_mag_array,
                  "Force Position": self.force_pos_array, "Force Direction": self.force_dir_array}
        self.force_data = pd.DataFrame(self.d)
        print(self.force_data)

        
    def showForceTable(self):
        self.showforceTable = Toplevel(self.forcInfo)
        self.f = Frame(self.showforceTable)
        self.f.pack( fill=BOTH, expand=1)
        self.force_table = Table(self.f, dataframe = self.force_data,showtoolbar=True, showstatusbar=True)
        #self.force_name_array.append()
        self.force_table.show()
        self.force_table.update_rowcolors()
        self.force_table.rowcolors[:] = '#fcfafa'
        #img3 = images.accept()
        updateButton = Button(self.showforceTable,text = 'Update' ,command = self.updateCanvas)
        updateButton.pack()
        clearButton = Button(self.showforceTable,text = 'Clear', command= self.clearCanvas)
        clearButton.pack()
        if self.userCheck == True:
            AutoButton = Button(self.showforceTable,text = 'Auto', command = self.autofillForces)
            AutoButton.pack()
    
    def autofillForces(self):
        self.force_table.model.df = self.dfs['Force_Info']
        self.force_table.redraw()
        return self.force_table
    
    def updateCanvas(self):
        clearShapes(scene, 'arrows')
        self.force_data = self.force_table.model.df
        #print(df)
        if len(self.force_data) == 0:
            print("array empty please fill")
        else:    
            for index,row in self.force_data.iterrows():
                pos_force= row["Force Position"]
                mag_force = str(row['Force Value'])
                #self.force_pos_array.append(pos_force)
                pos_force = str2array(pos_force)
                dir_force= row["Force Direction"]
                #self.force_dir_array.append(dir_force)
                dir_force = str2array(dir_force)
                n_force= row['Force Name']
                print(self.force_name_array)
                if mag_force == str('?'):
                    self.unknown_forces_vars.append(n_force)
                    print(self.unknown_forces_vars)
                else:
                    self.known_forces_vars.append(n_force)
                    self.known_forces_mag.append(mag_force)
                arrow(pos = vec(pos_force[0],pos_force[1],pos_force[2]),
                      axis = 5*vec(dir_force[0],dir_force[1],dir_force[2]), color = color.magenta)
                text(pos = vec(pos_force[0],pos_force[1],pos_force[2])+5*vec(dir_force[0],dir_force[1],dir_force[2]), text = n_force )
        print(self.force_data)
        
        
    def clearCanvas(self):
        clearShapes(scene, 'beams')
        self.force_name_array=['0']
        self.force_dir_array=['0']
        self.force_mag_array=['0']
        self.force_pos_array = ['0']
        self.d = {"Force Name": self.force_name_array, "Force Value": self.force_mag_array,
                  "Force Position": self.force_pos_array, "Force Direction": self.force_dir_array}
        self.force_data =  pd.DataFrame(self.d)
        self.force_table.model.df = self.force_data
        print(self.force_data)
        self.force_table.redraw()
        return self.force_data,self.force_table
    
    
    def showBeamTable(self):
        self.BeamTable = Toplevel(self.start_problem)
        f = Frame(self.BeamTable)
        f.pack( fill=BOTH, expand=1)
        self.beam_showTable = Table(f, dataframe = self.beam_data,showtoolbar=True, showstatusbar=True)
        self.beam_showTable.show()
        self.beam_showTable.update_rowcolors()
        self.beam_showTable.rowcolors[:] = '#fcfafa'
        img3 = images.accept()
        updateButton = Button(self.BeamTable, text = 'Update', command = self.updateBeams)
        updateButton.pack()
        clearButton = Button(self.BeamTable,text = 'Clear', command = self.clearBeams)
        clearButton.pack()
        AutoButton = Button(self.BeamTable,text = 'Auto', command = self.autofillBeams)
        AutoButton.pack()
        
    def autofillBeams(self):
        self.beam_showTable.model.df = self.dfs['Beam_Info']
        self.beam_showTable.redraw()
        return self.beam_showTable
        
    def updateBeams(self):
        clearShapes(scene, 'beam')
        self.beam_data = self.beam_showTable.model.df
        #print(df)
        if len(self.beam_data) == 0:
            print("array empty please fill")
        else:    
            for index,row in self.beam_data.iterrows():
                drawShapes(row,'beams',c = color.white)
        print(self.beam_data)
        
    def clearBeams(self):
        clearShapes(scene, 'beam')
        self.beam_names = ['0']
        self.start_nodes_names = ['0']
        self.start_nodes_pos = ['0']
        self.end_nodes_names = ['0']
        self.end_nodes_pos = ['0']
        self.beam_diction = {"Start Node" : self.start_nodes_names, "Start Node Pos":self.start_nodes_pos,  
                          "End Node" : self.end_nodes_names, "End Node Pos":self.end_nodes_pos,}
        self.beam_data = pd.DataFrame(self.beam_diction)
        self.beam_showTable.model.df = self.beam_data
        self.beam_showTable.redraw()

    def checkForces(self):
        x = self.force_data.loc[:0,'Force Name']
        if x.item() == '0':
            messagebox.showerror(title='Forces', message="Nice try to get answers, go back and input forces")
        else:
            solution_forces = self.dfs['Force_Info']
            print(solution_forces)
            print(self.force_data)
            mergedResult =  pd.merge(solution_forces,self.force_data,how='outer', 
                                     on = ['Force Value','Force Position','Force Direction'],indicator=True)
            print(mergedResult)
            correctAnswers = mergedResult[mergedResult['_merge']=='both']
            print(correctAnswers)
            wrongAnswers = mergedResult[mergedResult['_merge']=='right_only']
            wrongForcePos = np.array(wrongAnswers['Force Position'])
            wrongForcePos = wrongForcePos.tolist()
            missingAnswers = mergedResult[mergedResult['_merge']=='left_only']
            missingForces = np.array(missingAnswers['Force Position'])
            missingForces = missingForces.tolist()
            print(wrongForcePos)
            clearShapes(scene,'arrows')
            if len(wrongAnswers) != 0:
                messagebox.showerror(title='Forces', message="You have made a mistake! Recheck your forces at the following locations. " + wrongForcePos[0])
                wrongAnswers.apply(lambda row: drawShapes(row,'arrows',color.red),axis =1)
            
            if len(missingAnswers) != 0:
                messagebox.showwarning(title='Forces', message="You are missing a force, Hint: Check the following locations " + missingForces[0])
                
            
            if len(correctAnswers) != 0:
                correctAnswers.apply(lambda row: drawShapes(row,'arrows',color.blue), axis =1)
            if len(wrongAnswers) == 0 and len(missingAnswers) == 0:
                self.canvas3.itemconfig(self.step2, fill = 'green')
            else:
                self.canvas3.itemconfig(self.step2, fill = 'red')
            correctAnswers = correctAnswers.drop(['Force Name_y', '_merge'], axis = 1)
            correctAnswers = correctAnswers.rename(columns = {'Force Name_x': "Force Name"})
            
            wrongAnswers = wrongAnswers.drop(['Force Name_x', '_merge'], axis = 1)
            wrongAnswers = wrongAnswers.rename(columns = {'Force Name_y': "Force Name"})
            
            print('correct', correctAnswers)
            print('wrong', wrongAnswers)
            
            f = correctAnswers.append(wrongAnswers)
            print(f)
            
            # self.force_table.rowcolors[:len(correctAnswers)] = '#AAFC74'
            # self.force_table.rowcolors[len(correctAnswers):len(wrongAnswers)] = '#fc7474'
            #
            # self.force_table.rowcolors[:len(correctAnswers)] = '#AAFC74'
            # self.force_table.rowcolors[len(correctAnswers):len(wrongAnswers)] = '#fc7474'
            # self.force_table.redraw()
            # self.force_table.show()
            
    def checkBeams(self):
        x = self.beam_data.loc[:0,"Start Node"]
        if x.item() == '0':
            messagebox.showerror(title='Beams', message="Nice try to get answers, go back and input Beams")
        else:
            solution_beams = self.dfs['Beam_Info']
            mergedResult = pd.merge(solution_beams, self.beam_data, how ='outer',
                                    indicator = True)
            correctAnswers = mergedResult[mergedResult['_merge']=='both']
            print(correctAnswers)
            wrongAnswers = mergedResult[mergedResult['_merge']=='right_only']
            wrongNodePos = np.array(wrongAnswers['Start Node'])
            wrongNodePos = wrongNodePos.tolist()
            missingAnswers = mergedResult[mergedResult['_merge']=='left_only']
            missingNode = np.array(missingAnswers['Start Node'])
            missingNode = missingNode.tolist()
            clearShapes(scene,'beams')
            if len(wrongAnswers) != 0:
                messagebox.showerror(title='Beams', message="You have made a mistake! Recheck your beams at the following locations. " + wrongNodePos[0])
                wrongAnswers.apply(lambda row: drawShapes(row,'beams',color.red),axis =1)
                self.check = False
                self.canvas3.itemconfig(self.step1, fill = 'red')

            if len(missingAnswers) != 0:
                messagebox.showwarning(title='Forces', message="You are missing a beam, Hint: Check the following locations " + missingNode[0])
                self.check = False
                self.canvas3.itemconfig(self.step1, fill = 'red')

            if len(correctAnswers) != 0:
                correctAnswers.apply(lambda row: drawShapes(row,'beams',color.blue), axis =1)
            if len(wrongAnswers) == 0 and len(missingAnswers) == 0:
                self.check = True
                self.canvas3.itemconfig(self.step1, fill = 'green')
    def enterEquations(self):
        if self.check == False:
            messagebox.showwarning(title='Equations', message="You haven't input correct forces and/or beams, Go back and recheck your work" )
        else:
            self.inputEquations = {'∑Fx':None,'∑Fy':None,'∑Fz':None}
            self.poi = self.beam_data['Start Node'].append(self.beam_data["End Node"])
            self.poi = np.array(self.poi).tolist()
            self.poi = list(dict.fromkeys(self.poi))
            #self.print(self.poi)
            listOfExp = ['∑Fx', '∑Fy','∑Fz' ]
            listOfExp=listOfExp + ['∑M'+item for item in self.poi]
            self.equations = Toplevel(self.start_problem)
            self.equations.title('Sum of Forces')
            self.option = StringVar(self.equations)
            self.option.set("∑Fx") # default value
            self.equationOption = OptionMenu(self.equations, self.option, *listOfExp)
            self.equationOption.grid(row=0,column=0,padx=5, sticky='WE')
            self.equationEntry=Entry(self.equations)
            self.equationEntry.grid(row=0,column=1,padx=5, sticky='WE')
            self.equationFeedback = Text(self.equations, width = 50, height = 3)
            self.equationFeedback.grid(row=1, column=0, columnspan = 2, sticky='WE')
            
            eq_add_button=Button( self.equations,text="Add",command=self.addEquationtoTable)
            eq_add_button.grid(row=3,column=0, sticky='WE')
            
            submission_button=Button( self.equations,text="Check",command=self.checking_Entered_Equations)
            submission_button.grid(row=3,column=1, sticky='WE') 
        
    def addEquationtoTable(self):
        
        if self.option.get()=='∑Fx':
            self.inputEquations['∑Fx'] = sp.sympify(self.equationEntry.get())
            
        elif self.option.get()=='∑Fy': 
            self.inputEquations['∑Fy'] = sp.sympify(self.equationEntry.get())
            
        elif self.option.get()=='∑Fz': 
            self.inputEquations['∑Fz'] = sp.sympify(self.equationEntry.get())
            
        #self.inpEqnsTables = pd.DataFrame(self.inputEquations)
            
    def checking_Entered_Equations(self):
        self.auto_equations()
        self.equation_entered = self.equationEntry.get()
        print(self.equation_entered)
        self.equation_entered=sp.sympify(self.equation_entered)
        print(self.equation_entered)
        force_Names=self.equation_entered.free_symbols
        #self.equation_entered = self.round_expr(self.equation_entered,2)
        print('Equation entered is : ', self.equation_entered)
        print('Forces are : ', force_Names)
        
        self.inputEquationsTable = pd.DataFrame.from_dict(data = self.inputEquations, orient= 'index', columns = ["Expression"])
        
        correct_eqn = self.solEquationsTable.loc[self.option.get()]['Expression']
        print(correct_eqn)
        answer_Equation=correct_eqn
        answer_Symbols=answer_Equation.free_symbols
        print(answer_Equation)
        remainder_Equation= answer_Equation-self.equation_entered
        error_Equation=remainder_Equation.free_symbols
        print(remainder_Equation)
        
        notfound=list(error_Equation)
        for force in answer_Symbols:
            if force in notfound : 
                notfound.remove(force)
        print(' The following entered forces are invalid ', notfound)
        
        missing=list(answer_Symbols)
        for force in force_Names : 
            if force in answer_Symbols: 
                missing.remove(force)
                
        print('The following forces are missing:', missing)        
        
        wrong_Coefficient=[]
        for force in answer_Symbols: 
            if force in error_Equation: 
                wrong_Coefficient.append(force)
        for force in missing: 
            wrong_Coefficient.remove(force)
        print ('The following entered forces have wrong coefficients : ', wrong_Coefficient)
        self.equationVariables = {'not found':notfound, 'wrong coefficient':wrong_Coefficient, 'missing':missing}
        self.symbolsToStrings()
        self.giveFeedBackonEquations()
    
    def symbolsToStrings(self):
        for key in self.equationVariables:
                self.equationVariables[key] = list(map(str, self.equationVariables[key]))
    
    def findVariables(self, text, variable):
        ind = text.find(variable)
        return [ind, ind+len(variable)]
    
    def giveFeedBackonEquations(self):
        color = {'not found':'red', 'wrong coefficient':'blue', 'missing':'maroon'}
        text = str(self.equation_entered)
        if self.equationVariables['missing']:
            missingText = '|\tMissing:'+','.join(self.equationVariables['missing'])
            text = text+missingText
        self.equationFeedback.delete('1.0', END)
        self.equationFeedback.insert(INSERT, text)
        for key in self.equationVariables:
            for variable in self.equationVariables[key]:
                ind = self.findVariables(text, variable)
                self.equationFeedback.tag_add(key, "1."+str(ind[0]), "1."+str(ind[1]))
            self.equationFeedback.tag_config(key, foreground=color[key])
    
    def auto_equations(self):
        data = self.force_data
        self.text = ''
      
        result = data.apply(findSumOfForces, axis=1)
        print(result)
        newData = pd.DataFrame(tuple(result), columns=['i','j','k'])
        
        newData.apply(combine)
        
        print(newData)
       
        self.finalEquations = {'∑Fx': sum(sp.sympify(newData['i'])*a.i),'∑Fy': sum(sp.sympify(newData['j'])*a.j),
                          '∑Fz': sum(sp.sympify(newData['k'])*a.k)}
        print(self.finalEquations)
        
        d = np.array([i,j,k]).transpose()
        
        finalMoms = {}
        poi_coord = self.beam_data['Start Node Pos'].append(self.beam_data["End Node Pos"])
        poi_coord = np.array(poi_coord).tolist()
        poi_coord = list(dict.fromkeys(poi_coord))
        
        for n in range(len(self.poi)):
            point = np.array(str2array(poi_coord[n]))
            result = self.force_data.apply(lambda force_data: findSumOfMoments(force_data, point), axis=1)
            Data = pd.DataFrame(tuple(sp.sympify(result)), columns=['i','j','k'])
            print(Data)
            x = Data.sum(level = 0)
            print(x)
            x = sum(np.dot(x.to_numpy(),d))
            print(x)
            finalMoms['∑M'+self.poi[n]]  = x
        print(finalMoms)
        m = self.finalEquations.update(finalMoms)
        print(self.finalEquations)
        self.solEquationsTable = pd.DataFrame.from_dict(data = self.finalEquations, orient = 'index', columns = ['Expression'])
        print(self.solEquationsTable)
        print(self.solEquationsTable.loc['∑Fx'])
        
        for key, value in self.finalEquations.items():
            self.text += str(key) + ' = ' + str(value) + '\n'
        print(self.text)
            
        #self.equationFeedback.delete('1.0', END)
        #self.equationFeedback.insert(INSERT, self.text) 
        
    def inputunknowns(self):
        self.inputUnknownForces = Toplevel(self.start_problem)
        
        self.unknownforce = StringVar(self.inputUnknownForces)
        listOfExp = self.unknown_forces_vars
        self.forceVar = OptionMenu(self.inputUnknownForces, self.unknownforce, *listOfExp)
        self.forceVar.grid(row=0,column=0,padx=5, sticky='WE')
        self.forceEntry=Entry(self.inputUnknownForces)
        self.forceEntry.grid(row=0,column=1,padx=5, sticky='WE')
        self.forceFeedback = Text(self.inputUnknownForces, width = 50, height = 3)
        self.forceFeedback.grid(row=1, column=0, columnspan = 2, sticky='WE')
        
        eq_add_button=Button( self.inputUnknownForces,text="Add",command=self.addUnknowntoTable)
        eq_add_button.grid(row=3,column=0, sticky='WE')
        
        submission_button=Button( self.inputUnknownForces,text="Check",command=self.checking_unknown)
        submission_button.grid(row=3,column=1, sticky='WE') 
        # if self.userCheck == True:
        #     AutoButton = Button(self.inputUnknownForces,text = 'Auto', command = self.autofillForces)
        #     AutoButton.grid(row=3,column=2, sticky='WE')
        #     self.forceFeedback.insert(INSERT, self.soln)
        
    def addUnknowntoTable(self):
        var = self.unknownforce.get()
        self.force_data = self.force_table.model.df
        for index,row in self.force_data.iterrows():
            n_force= row["Force Name"]
            if n_force == var:
                print(row['Force Value'])
                row['Force Value'] = self.forceEntry.get()
                self.unknown_forces_mag.append(float(self.forceEntry.get()))
                print(row['Force Value'])
        print(self.force_data)
    
    def autounknowns(self):
        data = self.dfs['Force_Info']
        self.text = ''
      
        result = data.apply(findSumOfForces, axis=1)
        print(result)
        newData = pd.DataFrame(tuple(result), columns=['i','j','k'])
        
        newData.apply(combine)
        
        print(newData)
        i,j,k = sp.symbols('i,j,k')
        self.finalunknowns = {'∑Fx': sum(sp.sympify(newData['i'])),'∑Fy': sum(sp.sympify(newData['j'])),
                          '∑Fz': sum(sp.sympify(newData['k']))}
        print(self.finalunknowns)
        
        i,j,k = sp.symbols('i,j,k')
        d = np.array([i,j,k]).transpose()
        
        finalMoms = {}
        self.poi = self.beam_data['Start Node'].append(self.beam_data["End Node"])
        self.poi = np.array(self.poi).tolist()
        self.poi = list(dict.fromkeys(self.poi))
        poi_coord = self.beam_data['Start Node Pos'].append(self.beam_data["End Node Pos"])
        poi_coord = np.array(poi_coord).tolist()
        poi_coord = list(dict.fromkeys(poi_coord))
        
        for n in range(len(self.poi)):
            point = np.array(str2array(poi_coord[n]))
            result = self.force_data.apply(lambda force_data: findSumOfMoments(force_data, point), axis=1)
            Data = pd.DataFrame(tuple(sp.sympify(result)), columns=['i','j','k'])
            x = Data.sum(level = 0)
            x = sum(np.dot(x.to_numpy(),d))
            finalMoms['∑M'+self.poi[n]]  = x
        print(finalMoms)
        m = self.finalunknowns.update(finalMoms)
        print(self.finalunknowns)
        self.solunknownsTable = pd.DataFrame.from_dict(data = self.finalunknowns, orient = 'index', columns = ['Expression'])
        print(self.solunknownsTable)
        print(self.solunknownsTable.loc['∑Fx'])
        
        for key, value in self.finalunknowns.items():
            self.text += str(key) + ' = ' + str(value) + '\n'
        print(self.text)
        
        self.variables = [sp.Symbol(v) for v in self.unknown_forces_vars]
        variables = self.variables
        known_variables = [sp.Symbol(n) for n in self.known_forces_vars]
        equations = self.finalunknowns
        eqn_solution = [equations['∑Fx']]
        eqn_solution.append(equations['∑Fy'])
        eqn_solution.append(equations['∑Fz'])
        i,j,k = sp.symbols('i,j,k')
        eqn_needed = len(variables) - len(eqn_solution)
        MA = equations['∑MA']
        temp, M_x = MA.as_independent(i, as_Mul=True,as_Add = True)
        eqn_solution.append(M_x)
        temp, M_y = MA.as_independent(j, as_Mul=True,as_Add = True)
        eqn_solution.append(M_y)
        temp, M_z = MA.as_independent(k, as_Mul=True,as_Add = True)
        eqn_solution.append(M_z)
        
        print('variables', variables)
        print('equations', eqn_solution)   
        A, b = sp.linear_eq_to_matrix(list(eqn_solution), variables)
        print(A)
        print(b)
        known_b = sp.Matrix([0,0,0,0,0,0])
        
        print(known_b)
        soln = sp.linsolve((A,b),variables)
        soln = list(soln)
        soln = list(soln[0])
        
        print(soln)
        
        for var in range(len(known_variables)):
            print('values for sub',known_variables[var],self.known_forces_mag[var])
            soln = [s.subs(known_variables[var],self.known_forces_mag[var]) for s in soln]
            print('sol',soln)
        
        self.soln = soln
        print('soln', self.soln)
            
    
    def checking_unknown(self):
        self.autounknowns()
        #self.auto_equations()
        print('.............................................')
        self.createMatrix()
        self.giveFeedBackonUnknowns()
        
    def createMatrix(self):
        force_mag = self.unknown_forces_mag
        print(np.array(self.soln))
        print(np.array(force_mag))
        remainder = np.array(self.soln) - force_mag
        self.correct = []
        self.incorrect = []
        self.check = {'correct':self.correct,'incorrect':self.incorrect}
        for i in range(len(remainder)):
            if remainder[i] != 0:
                self.incorrect.append([remainder[i],self.variables[i]])
            else:
                self.correct.append([remainder[i],self.variables[i]])
                
    def giveFeedBackonUnknowns(self):
        color = {'incorrect':'red', 'correct':'green'}
        Text = ''
        if len(self.check['incorrect']) == 0:
            Text += 'Good Job! all forces are correct'
        elif len(self.check['incorrect']) != 0:
            Text += 'The following forces are incorrect, please recheck them '
            for i in range(len(self.incorrect)):
                Text += str(self.incorrect[i][1]) + ' '
        print(Text)
        self.forceFeedback.delete('1.0', END)
        self.forceFeedback.insert(INSERT, Text)

app = Tk()
app.title("Free Body Diagram Solver V1.1")
app.geometry('600x400')
app.wm_attributes("-transparentcolor", 'grey')
Selection=ComboboxSelectionWindow(app)
app.mainloop()





