# -*- coding: utf-8 -*-
"""
stores all the input variables from the gui so other classes can acces it

"""
from __future__ import unicode_literals, division, print_function
import os
import sys
from psychopy import core
from gui import StateCheckIn


class VarStore:
    """
    stores all the input variables from the gui so other classes can acces it

    """


    # initialize the VarStore Object (just needed once)
    def init(self):
        # create a StateCheckIn object (gui)
        self.gui = StateCheckIn()
        self.gui.check_in_name_and_type()
        self.screensize_x = self.gui.guiscreensize_x
        self.screensize_y = self.gui.guiscreensize_y
        ###name of the object###

        if not self.gui.gui_input.OK:
            core.quit()

    # initialize variables with the parameters of the gui class
        # no check needed
        self.name_testperson = self.gui.gui_input.data[0]
        self.session_number = self.gui.gui_input.data[1]
        self.experiment_type = self.gui.gui_input.data[2]
        # set trial composition depending on given task
        if self.experiment_type == "Yes-No Task":
            self.trial_composition = [1, 2, 3, 4, 5, 6]
        if self.experiment_type == "2IFC":
            self.trial_composition = [1, 2, 3, 2, 7, 8, 5, 6]
        if self.experiment_type == "4IFC":
            self.trial_composition = [1, 2, 9, 2, 9, 2, 9, 2, 9, 10, 5, 6]
        if self.experiment_type == "Constant Stimuli":
            self.trial_composition = [1, 2, 11, 2, 11, 12, 5, 6]

        self.gui.set_variables(self.experiment_type)

    def within_range(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def set_variables(self):
        self.initialize_failed = False
        # 1-100
        self.number_of_trials = self.within_range(
            self.gui.gui_input_var.data[0], 1, 100)
        # 1-100
        self.trial_blocks = self.within_range(
            self.gui.gui_input_var.data[1], 1, 100)
        # 0-50
        self.testtrials = self.within_range(
            self.gui.gui_input_var.data[2], 0, 50)
        #0.0 - 10
        self.time_fixation_cross = self.within_range(
            self.gui.gui_input_var.data[3], 0, 10)
        self.time_blank_screen = self.within_range(
            self.gui.gui_input_var.data[4], 0, 10)
        self.time_stimulus = self.within_range(
            self.gui.gui_input_var.data[5], 0.0001, 10)
        self.time_answer = self.within_range(
            self.gui.gui_input_var.data[6], 0.0001, 10)
        self.time_feedback = self.within_range(
            self.gui.gui_input_var.data[7], 0, 10)
        self.time_pause = self.within_range(
            self.gui.gui_input_var.data[8], 0, 10)
        # no check
        self.stimulus_size_pixels = self.gui.gui_input_var.data[9]
        
        self.signal_picture = self.gui.gui_input_var.data[10]
        
        self.signal_colour = self.gui.gui_input_var.data[11]
        
        # 0-15
        self.signal_intensity = self.within_range(
            self.gui.gui_input_var.data[12], 1, 15)
        # 50-200
        self.mean_noise = self.within_range(
            self.gui.gui_input_var.data[13], 50, 200)
        # 0-40
        self.standard_deviation_noise = self.within_range(
            self.gui.gui_input_var.data[14], 0, 40)

        self.decrease_intensity = self.gui.gui_input_var.data[15]
        # steps * trialblock have to be less than signal_intensity
        self.intensity_steps = self.within_range(
            self.gui.gui_input_var.data[16], 0.1, 10)
        if (self.intensity_steps * self.trial_blocks >
                self.signal_intensity and self.decrease_intensity):
            self.initialize_failed = True
        self.random_intensity = self.gui.gui_input_var.data[17]

        self.data_path = self.gui.this_dir + os.sep + u'data/' + \
            self.name_testperson + "_Durchgang" + self.session_number + ".tsv"
        
        # checks if savefile already exist to prevent overwriting
#        if os.path.exists(self.data_path):
#            sys.exit("Datei " + self.data_path + " existiert bereits!")

        self.instruction = """
Guten Tag,
\ndas Experiment beginnt in Kürze.
\nBitte lesen Sie sich die folgenden Instruktionen gut durch.
\nFalls Sie Fragen haben sollten, stellen Sie diese bitte vor Start des Experiments dem Versuchsleiter. Falls Sie alles Verstanden haben drücken Sie auf "w" für "weiter".
\n[Weiter]"""


# choose the text for the instruction depeding on the given task
        if self.experiment_type == "Yes-No Task":
            self.instruction2 = u"""
Es werden Ihnen nun verschiedene Stimuli präsentiert.
\nEinige Stimuli bestehen nur aus dem Störrauschen, andere bestehen aus dem Rauschen und dem zu entdeckenden Signal.
\nIn der Mitte des Bildschirms wird Ihnen nun ein Stimulus mit Signal als Beispiel gezeigt.
\nWenn Sie das Signal während des Experiments entdecken, drücken Sie bitte "y".
\nAls nächstes wird Ihnen nur das Störrauschen allein als Beispiel angezeigt.
\n[Weiter]"""
            self.instruction3 = u"""
In der Mitte des Bildschirms wird Ihnen nun nur das Störrauschen angezeigt.
\nFalls Sie gleich nur das Rauschen wahrnehmen sollten, drücken Sie bitte "n".
\n[Weiter]"""
            self.instruction4 = u"""
Gleich startet das Experiment.
\nZunächst wird Ihnen in der Mitte des Bildschirms ein Fixationskreuz angezeigt. Genau dort erscheint wenig später für kurze Zeit der Stimulus.
\nNachdem der Stimulus wieder ausgeblendet wurde, startet die Antwortperiode.
\nZur Erinnerung:
\nFalls Sie in dem Stimulus das Signal erkennen, drücken Sie bitte "y".
\nFalls Sie das Signal NICHT entdecken können, drücken Sie "n".
\nNach Ihrer Entscheidung erhalten Sie ein kurzes Feedback, ob ihre Wahl korrekt war: Ein grünes Kreuz bei richtiger Antwort und ein rotes bei einer falschen.
\nDanach erscheint wieder das Fixationskreuz und ein neuer Durchgang startet.
\nWenn Sie nun auf "w" drücken startet das Experiment. Wir empfehlen, Ihre Finger schon auf die entsprechenden Tasten zu legen.
\n[Weiter]"""

        if self.experiment_type == "2IFC":
            self.instruction2 = u"""
Im Experiment werden Ihnen immer zwei Stimuli in kurzer Folge präsentiert.
\nEiner der beiden Stimuli besteht nur aus dem Störrauschen, der andere besteht immer aus dem Rauschen und dem zu entdeckenden Signal.
\nIn der Mitte des Bildschirms wird Ihnen nun ein Stimulus mit Signal als Beispiel gezeigt.
\nAls nächstes wird Ihnen nur das Störrauschen allein als Beispiel angezeigt.
\n[Weiter]"""
            self.instruction3 = u"""
In der Mitte des Bildschirms wird Ihnen nun nur das Störrauschen angezeigt.
\nSie haben im Folgenden die Aufgabe, anzugeben, ob das Signal im ersten oder im zweiten Stimulus angezeigt wurde.
\nDazu drücken Sie, nachdem Sie beide Stimuli gesehen haben, "1" falls Sie das Signal im ersten vermuten, oder "2" falls Sie denken, es wäre im zweiten.
\n[Weiter]"""
            self.instruction4 = u"""
Gleich startet das Experiment.
\nZunächst wird Ihnen in der Mitte des Bildschirms ein Fixationskreuz angezeigt. Genau dort erscheint wenig später für kurze Zeit der erste Stimulus, gefolgt vom zweiten.
\nNachdem der zweite Stimulus ausgeblendet wurde, startet die Antwortperiode.
\nZur Erinnerung:
\nFalls Sie das Signal in dem ersten Stimulus erkennen, drücken Sie bitte "1".
\nFalls Sie das Signal in dem zweiten Stimulus erkennen, drücken Sie bitte "2".
\nNach Ihrer Entscheidung erhalten Sie ein kurzes Feedback, ob ihre Wahl korrekt war: Ein grünes Kreuz bei richtiger Antwort und ein rotes bei einer falschen.
\nDanach erscheint wieder das Fixationskreuz und ein neuer Durchgang startet.
\nWenn Sie nun auf "w" drücken startet das Experiment. Wir empfehlen, Ihre Finger schon auf die entsprechenden Tasten zu legen.
\n[Weiter]"""

        if self.experiment_type == "4IFC":
            self.instruction2 = u"""
Im Experiment werden Ihnen immer vier Stimuli in kurzer Folge präsentiert.
\nDrei der Stimuli bestehen nur aus dem Störrauschen, einer besteht immer aus dem Rauschen und dem zu entdeckenden Signal.
\nIn der Mitte des Bildschirms wird Ihnen nun ein Stimulus mit Signal als Beispiel gezeigt.
\nAls nächstes wird Ihnen nur das Störrauschen allein als Beispiel angezeigt.
\n[Weiter]"""
            self.instruction3 = u"""
In der Mitte des Bildschirms wird Ihnen nun nur das Störrauschen angezeigt.
\nSie haben im Folgenden die Aufgabe, anzugeben in welchem der vier Stimuli das Signal angezeigt wurde.
\nDazu drücken Sie, nachdem Sie die Stimuli gesehen haben, die entsprechende Zahl auf Ihrer Tastatur, also beispielsweise "3" falls Sie das Signal im dritten Stimulus vermuten.
\n[Weiter]"""
            self.instruction4 = u"""
Gleich startet das Experiment.
\nZunächst wird Ihnen in der Mitte des Bildschirms ein Fixationskreuz angezeigt. Genau dort erscheint wenig später für kurze Zeit der erste Stimulus, gefolgt von drei weiteren.
\nNachdem der vierte und letzte Stimulus ausgeblendet wurde, startet die Antwortperiode.
\nZur Erinnerung:
\nDas Signal ist immer in genau einem der vier Stimuli enthalten, für diesen Stimulus drücken Sie bitte die entsprechende Zahlentaste.
\nNach Ihrer Entscheidung erhalten Sie ein kurzes Feedback, ob ihre Wahl korrekt war: Ein grünes Kreuz bei richtiger Antwort und ein rotes bei einer falschen.
\nDanach erscheint wieder das Fixationskreuz und ein neuer Durchgang startet.
\nWenn Sie nun auf "w" drücken startet das Experiment. Wir empfehlen, Ihre Finger schon auf die entsprechenden Tasten zu legen.
\n[Weiter]"""

        if self.experiment_type == "Constant Stimuli":
            self.instruction2 = u"""
Im Experiment werden Ihnen immer zwei Stimuli in kurzer Folge präsentiert.
\nDie Stimuli bestehen immer aus einem Störrauschen und einem Signal.
\nIn der Mitte des Bildschirms wird Ihnen nun ein solcher Stimulus mit Signal als Beispiel gezeigt.
\nAls nächstes ein Stimulus mit einem stärkeren Signal als Beispiel angezeigt.
\n[Weiter]"""
            self.instruction3 = u"""
In der Mitte des Bildschirms wird Ihnen nun ein Stimulus mit einem stärkeren Signal angezeigt.
\nSie haben im Folgenden die Aufgabe, anzugeben ob das Signal im ersten oder im zweiten Stimulus stärker war.
\nDazu drücken Sie, nachdem Sie beide Stimuli gesehen haben, "1" falls Sie das erste Signal stärker empfanden, oder "2" falls Sie denken, das zweite war stärker.
\n[Weiter]"""
            self.instruction4 = u"""
Gleich startet das Experiment.
\nZunächst wird Ihnen in der Mitte des Bildschirms ein Fixationskreuz angezeigt. Genau dort erscheint wenig später für kurze Zeit der erste Stimulus, gefolgt vom zweiten.
\nNachdem der zweite Stimulus ausgeblendet wurde, startet die Antwortperiode.
\nZur Erinnerung:
\nFalls Sie das Signal in dem ersten Stimulus für stärker halten, drücken Sie bitte "1".
\nFalls Sie das Signal in dem zweiten Stimulus für stärker halten, drücken Sie bitte "2".
\nNach Ihrer Entscheidung erhalten Sie ein kurzes Feedback, ob ihre Wahl korrekt war: Ein grünes Kreuz bei richtiger Antwort und ein rotes bei einer falschen.
\nDanach erscheint wieder das Fixationskreuz und ein neuer Durchgang startet.
\nWenn Sie nun auf "w" drücken startet das Experiment. Wir empfehlen, Ihre Finger schon auf die entsprechenden Tasten zu legen.
\n[Weiter]"""
        
# only if the gui button ok is pressed, the rest of the code will be executed
        if not self.gui.gui_input_var.OK:
            core.quit()

#
#        if self.experiment_type == "Yes/No Task":
#            self.instruction2 = 'Es werden Ihnen nun verschiedene Stimuli präsentiert. \n\nEinige Stimuli bestehen nur aus dem Störrauschen, andere bestehen aus dem Rauschen und dem zu entdeckenden Signal. \n\nIn der Mitte des Bildschirms wird Ihnen nun ein Stimulus mit Signal als Beispiel gezeigt. \n\nWenn Sie das Signal während des Experiments entdecken, drücken Sie bitte "y". \n\nAls nächstes wird Ihnen nur das Störrauschen allein als Beispiel angezeigt. \n \n[Weiter]'
#            self.instruction3 ='In der Mitte des Bildschirms wird Ihnen nun nur das Störrauschen angezeigt.\n\nFalls Sie gleich nur das Rauschen wahrnehmen sollten, drücken Sie bitte "n". \n\n[Weiter]'
#            self.instruction4 = 'Gleich startet das Experiment. \n\nZunächst wird Ihnen in der Mitte des Bildschirms ein Fixationskreuz angezeigt. Genau dort erscheint wenig später für kurze Zeit der Stimulus. \n\nNachdem der Stimulus wieder ausgeblendet wurde, startet die Antwortperiode. \n\nZur Erinnerung: \n\nFalls Sie in dem Stimulus das Signal erkennen, drücken Sie bitte "y". \n\nFalls Sie das Signal NICHT entdecken können, drücken Sie "n". \n\nNach Ihrer Entscheidung erhalten Sie ein kurzes Feedback, ob ihre Wahl korrekt war: Ein grünes Kreuz bei richtiger Antwort und ein rotes bei einer falschen. \n\nDanach erscheint wieder das Fixationskreuz und ein neuer Durchgang startet. \n\nWenn Sie nun auf "w" drücken startet das Experiment. Wir empfehlen, Ihre Finger schon auf die entsprechenden Tasten zu legen. \n\n[Weiter]'
#
#
#        if self.experiment_type == "2IFC":
#            self.instruction2 = "Im Experiment werden Ihnen immer zwei Stimuli in kurzer Folge präsentiert. \n\nEiner der beiden Stimuli besteht nur aus dem Störrauschen, der andere besteht immer aus dem Rauschen und dem zu entdeckenden Signal. \n\nIn der Mitte des Bildschirms wird Ihnen nun ein Stimulus mit Signal als Beispiel gezeigt. \n\nAls nächstes wird Ihnen nur das Störrauschen allein als Beispiel angezeigt. \n \n[Weiter]"
#            self.instruction3 = 'In der Mitte des Bildschirms wird Ihnen nun nur das Störrauschen angezeigt. \n\nSie haben im Folgenden die Aufgabe, anzugeben, ob das Signal im ersten oder im zweiten Stimulus angezeigt wurde. Dazu drücken Sie, nachdem Sie beide Stimuli gesehen haben, "1" falls Sie das Signal im ersten vermuten, oder "2" falls Sie denken, es wäre im zweiten.\n\n[Weiter]'
#            self.instruction4 = 'Gleich startet das Experiment. \n\nZunächst wird Ihnen in der Mitte des Bildschirms ein Fixationskreuz angezeigt. Genau dort erscheint wenig später für kurze Zeit der erste Stimulus, gefolgt vom zweiten. \n\nNachdem der zweite Stimulus ausgeblendet wurde, startet die Antwortperiode. \n\nZur Erinnerung: \n\nFalls Sie das Signal in dem ersten Stimulus erkennen, drücken Sie bitte "1". \n\nFalls Sie das Signal in dem zweiten Stimulus erkennen, drücken Sie bitte "2". \n\nNach Ihrer Entscheidung erhalten Sie ein kurzes Feedback, ob ihre Wahl korrekt war: Ein grünes Kreuz bei richtiger Antwort und ein rotes bei einer falschen. \n\nDanach erscheint wieder das Fixationskreuz und ein neuer Durchgang startet. \n\nWenn Sie nun auf "w" drücken startet das Experiment. Wir empfehlen, Ihre Finger schon auf die entsprechenden Tasten zu legen. \n\n[Weiter]'
#
#        if self.experiment_type == "4IFC":
#            self.instruction2 = 'Im Experiment werden Ihnen immer vier Stimuli in kurzer Folge präsentiert. \n\nDrei der Stimuli bestehen nur aus dem Störrauschen, einer besteht immer aus dem Rauschen und dem zu entdeckenden Signal. \n\nIn der Mitte des Bildschirms wird Ihnen nun ein Stimulus mit Signal als Beispiel gezeigt. \n\nAls nächstes wird Ihnen nur das Störrauschen allein als Beispiel angezeigt. \n \n[Weiter]'
#            self.instruction3 = 'In der Mitte des Bildschirms wird Ihnen nun nur das Störrauschen angezeigt. \n\nSie haben im Folgenden die Aufgabe, anzugeben in welchem der vier Stimuli das Signal angezeigt wurde. Dazu drücken Sie, nachdem Sie die Stimuli gesehen haben, die entsprechende Zahl auf Ihrer Tastatur, also beispielsweise "3" falls Sie das Signal im dritten Stimulus vermuten. \n\n[Weiter]'
#            self.instruction4 = 'Gleich startet das Experiment. \n\nZunächst wird Ihnen in der Mitte des Bildschirms ein Fixationskreuz angezeigt. Genau dort erscheint wenig später für kurze Zeit der erste Stimulus, gefolgt von drei weiteren. \n\nNachdem der vierte und letzte Stimulus ausgeblendet wurde, startet die Antwortperiode. \n\nZur Erinnerung: \n\nDas Signal ist immer in genau einem der vier Stimuli enthalten, für diesen Stimulus drücken Sie bitte die entsprechende Zahlentaste. \n\nNach Ihrer Entscheidung erhalten Sie ein kurzes Feedback, ob ihre Wahl korrekt war: Ein grünes Kreuz bei richtiger Antwort und ein rotes bei einer falschen. \n\nDanach erscheint wieder das Fixationskreuz und ein neuer Durchgang startet. \n\nWenn Sie nun auf "w" drücken startet das Experiment. Wir empfehlen, Ihre Finger schon auf die entsprechenden Tasten zu legen. \n\n[Weiter]'
#
#        if self.experiment_type == "Constant Stimuli":
#            self.instruction2 = 'Im Experiment werden Ihnen immer zwei Stimuli in kurzer Folge präsentiert. \n\nDie Stimuli bestehen immer aus einem Störrauschen und einem Signal. \n\nIn der Mitte des Bildschirms wird Ihnen nun ein solcher Stimulus mit Signal als Beispiel gezeigt. \n\nAls nächstes ein Stimulus mit einem stärkeren Signal als Beispiel angezeigt. \n\n[Weiter]'
#            self.instruction3 = 'In der Mitte des Bildschirms wird Ihnen nun ein Stimulus mit einem stärkeren Signal angezeigt. \n\nSie haben im Folgenden die Aufgabe, anzugeben ob das Signal im ersten oder im zweiten Stimulus stärker. Dazu drücken Sie, nachdem Sie beide Stimuli gesehen haben, "1" falls Sie das erste Signal stärker empfanden, oder "2" falls Sie denken, das zweite war stärker. \n\n[Weiter]'
#            self.instruction4 = 'Gleich startet das Experiment. \n\nZunächst wird Ihnen in der Mitte des Bildschirms ein Fixationskreuz angezeigt. Genau dort erscheint wenig später für kurze Zeit der erste Stimulus, gefolgt vom zweiten. \n\nNachdem der zweite Stimulus ausgeblendet wurde, startet die Antwortperiode. \n\nZur Erinnerung: \n\nFalls Sie das Signal in dem ersten Stimulus für stärker halten, drücken Sie bitte "1". \n\nFalls Sie das Signal in dem zweiten Stimulus für stärker halten, drücken Sie bitte "2". \n\nNach Ihrer Entscheidung erhalten Sie ein kurzes Feedback, ob ihre Wahl korrekt war: Ein grünes Kreuz bei richtiger Antwort und ein rotes bei einer falschen. \n\nDanach erscheint wieder das Fixationskreuz und ein neuer Durchgang startet. \n\nWenn Sie nun auf "w" drücken startet das Experiment. Wir empfehlen, Ihre Finger schon auf die entsprechenden Tasten zu legen. \n\n[Weiter]'
