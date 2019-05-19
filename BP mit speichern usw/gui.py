# -*- coding: utf-8 -*-
"""
provides the functions to create a gui

"""
import os
import sys
import ctypes
from psychopy import gui,core


class StateCheckIn:
    """
    provides the functions to create a gui
    
    """

    # if this class is started, it opens the gui
    def check_in_name_and_type(self):
        """
        creates a gui for testperson data and experiment type
       
        """
        user32 = ctypes.windll.user32
    
    # works with 1 monitor; 2 monitors could potentially lead to problems
        self.guiscreensize_x = user32.GetSystemMetrics(0)
        self.guiscreensize_y = user32.GetSystemMetrics(1)
        
        # ensure that the path starts from the same directery this script is in
        self.this_dir = os.path.dirname(
            os.path.abspath(__file__)).decode(
                sys.getfilesystemencoding())
        os.chdir(self.this_dir)

        # input window for the data of this testperson
        self.gui_input = gui.Dlg(title="Signalentdeckung.py",pos = ((self.guiscreensize_x / 2 - 200),10))
        self.gui_input.addField("Versuchsperson:")  # 0
        self.gui_input.addField("Durchgang:")  # 1
        self.gui_input.addField(
            "Experimenttyp:",
            choices=[
                "Yes-No Task",
                "2IFC",
                "2IFCnew",
                "4IFC",
                "Constant Stimuli"])  # 2
        self.gui_input.show()

    def set_variables(self, experiment_type):
        """
        creates a gui to configure the experiment
        
        """

        self.gui_input_var = gui.Dlg(title="Signalentdeckung.py", pos = ((self.guiscreensize_x / 2 - 200),10))
        
        self.gui_input_var.addText("Einstellungen:")

        self.gui_input_var.addField("Trialanzahl", 100)  # 0
        self.gui_input_var.addField("Anzahl der Trialblocks", 3)  # 1
        self.gui_input_var.addField("Anzahl der Testtrials", 5)  # 2
        self.gui_input_var.addField("Dauer Fixationskreuz", 0.4)  # 3
        self.gui_input_var.addField("Dauer Maske:", 0.5)  # 4
        self.gui_input_var.addField("Dauer Stimulus", 0.1)  # 5
        self.gui_input_var.addField("Dauer Antwortperiode", 2)  # 6
        self.gui_input_var.addField("Dauer Feedback", 0.1)  # 7
        self.gui_input_var.addField("Dauer Pause", 0.5)  # 8
        self.gui_input_var.addField("Stimulusgröße in Pixeln",
                                    choices=["64x64", "128x128", "256x256"])  # 9
        
        self.gui_input_var.addText("Signaleinstellungen:")
        
        self.gui_input_var.addField("Signal auswählen", choices=["A","Haus"])# 10
        self.gui_input_var.addField("Signal auswählen", choices=["Schwarz Weiss","Bunt"])# 11
        self.gui_input_var.addField("Stärke des Signals:", 11.0)  # 10
        self.gui_input_var.addField("Mittelwert", 128.0)  # 11
        self.gui_input_var.addField("Standartabweichung", 35.0)  # 12
        
        # dont show the last 3 options for the constant stimuli task 
        if experiment_type == "Constant Stimuli":
            self.gui_input_var.show()
        self.gui_input_var.addField("Kontrast - X je Trialblock", False)  # 13
        self.gui_input_var.addField("Schrittweite", 0.5)  # 14
        self.gui_input_var.addField("Zufällig", False)  #15
        if experiment_type != "Constant Stimuli":
            self.gui_input_var.show()
