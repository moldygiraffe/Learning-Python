import wx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from numpy import random


class MainFrame(wx.Frame):

    def __init__(self, parent):

        self.save_path = r"C:\Users\Michael\Downloads"

        wx.Frame.__init__(self, parent, title="Varactor Test Board", size=(1200, 580))

        # Add SplitterWindow panels
        self.split_win = wx.SplitterWindow(self)
        self.graph_panel = MatplotPanel(self.split_win)
        self.ctrl_menu = wx.Panel(self.split_win)
        self.split_win.SplitVertically(self.ctrl_menu, self.graph_panel, 200)

        # Define menu fields for voltage control.
        self.lvText = wx.StaticText(self.ctrl_menu, -1, 'Min Voltage (V)', size=(100 , 20), pos=(10 , 50))
        self.lvText = wx.StaticText(self.ctrl_menu, -1, 'Max Voltage (V)', size=(100, 20), pos=(10, 90))
        self.lvText = wx.StaticText(self.ctrl_menu, -1, 'Step Voltage (V)', size=(100, 20), pos=(10,130))
        self.min_voltage = wx.TextCtrl(self.ctrl_menu, -1, 'Vmin', size=(80 , 20), pos=(10 , 30))
        self.max_voltage = wx.TextCtrl(self.ctrl_menu, -1, 'Vmax', size=(80, 20), pos=(10, 70))
        self.step_voltage = wx.TextCtrl(self.ctrl_menu, -1, 'Vstep', size=(80, 20), pos=(10, 110))
        # There need to be 3 of these: Vmin, Vmax, Vstep

        # Select channel to tune.
        self.chText = wx.StaticText(self.ctrl_menu, -1, 'Tune Channel:', size=(100 , 20), pos=(10 , 200))
        self.chBox = wx.ComboBox(self.ctrl_menu,  choices =['1', '2', '3', '4', '5', '6', '7', '8', 'Common'], size = (100,20), pos=(10,220))

        #Where do I save my data?
        self.flText=wx.StaticText(self.ctrl_menu, -1, 'Save File:', size=(100,20), pos=(10,250))
        self.file_path = wx.TextCtrl(self.ctrl_menu, -1, self.save_path, size=(180,20), pos=(10,270))

        #Add buttons. There should be a Start Sweep, Measure Single, and Save File
        self.measBut = wx.Button(self.ctrl_menu, -1, "Measure", size=(80, 40), pos=(10, 410))
        self.measBut.Bind(wx.EVT_BUTTON, self.measure)

        self.fileBut = wx.Button(self.ctrl_menu, -1, 'Save Location', size=(80,40), pos=(10,450))
        self.fileBut.Bind(wx.EVT_BUTTON, self.set_path)

    def measure(self, event):
        try:
            minVolt = float(self.min_voltage.GetValue())
        except:
            print('Min volt not a number.')
            return
        print(f'Min volt is {minVolt}')
        if minVolt > 5 or minVolt < 0:
            print('Min volt is out of range [0,5]')
            return
        try:
            stepVolt = float(self.step_voltage.GetValue())
        except:
            print('Step volt not a number.')
            return
        print(f'Step volt is {stepVolt}')
        if stepVolt > 5 or stepVolt < 0:
            print('Step volt is out of range [0,5]')
            return
        try:
            maxVolt = float(self.max_voltage.GetValue())
        except:
            print('Max volt not a number.')
            return
        print(f'Max volt is {maxVolt}')
        if maxVolt > 5 or maxVolt < 0:
            print('Max volt is out of range [0,5]')
            return



        self.fig = Figure()

        self.ax1 = self.fig.add_subplot(111)
        self.ax1.scatter(random.rand(20), random.rand(20), 30)

        self.ax1.set_title("Data")
        self.ax1.set_xlim([0,1])
        self.ax1.set_ylim([0,1])
        self.ax1.set_xlabel('Frequency (Hz)')
        self.ax1.set_ylabel('S11 (dB)')
        self.canvas = FigureCanvas(self.graph_panel, -1, self.fig)

        print(f'Currently selected options are: \n'
              f'Minimum Voltage: {self.min_voltage.GetValue()}\n'
              f'Maximum Voltage: {self.max_voltage.GetValue()}\n'
              f'Step Voltage: {self.step_voltage.GetValue()}\n'
              f'Channel: {self.chBox.GetStringSelection()}')

    def set_path(self, event):

        fdlg = wx.FileDialog(self.ctrl_menu, "Select location to save data.", "", "", "CSV files(*.csv)|*.*", wx.FD_SAVE)

        if fdlg.ShowModal() == wx.ID_OK:
            self.save_path = fdlg.GetPath() + ".csv"
            self.file_path.SetValue(self.save_path)





class MatplotPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, size=(50, 50))

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)

        t = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        s = [0.0, 1.0, 0.0, 1.0, 0.0, 2.0, 1.0, 2.0, 1.0, 0.0]

        self.axes.plot(t, s)
        self.canvas = FigureCanvas(self, -1, self.figure)


app = wx.App()
frame = MainFrame(None).Show()
app.MainLoop()
