#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
this is the main module of the program, it creates the window running the experiment

to start the experiment run this file

'''

# import modules
from __future__ import unicode_literals, division, print_function
import sys
import os
import random
from psychopy import locale_setup, gui, visual, core, data, event, logging, clock
from PIL import Image
from psychopy.misc import fromFile
import numpy as np
import matplotlib.pyplot as plt
from matrix import BuildMatrix
from trial_evaluation import TrialEvaluation
from variable_store import VarStore

# creates an object that opens the gui, stores the parameters of the gui-input
# and checks if the input is correct 
variables = VarStore()
# initializes the VarStore-Object with the parameters of the first page
# of the gui


variables.init()


###### STOP #######

# if the input of the second gui-page is done,
# initialize the variables with the parameters of the second gui-page
variables.set_variables()

######
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
exp_name = variables.experiment_type  # from the Builder filename that created this script
expInfo = {'session': variables.session_number, 'participant': variables.name_testperson}
#dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
#if dlg.OK == False:
#    core.quit() # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = exp_name

print(expInfo['date'])

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s_%s' % (expInfo['participant'], expInfo['session'], exp_name, expInfo['date'])
filename_trial = _thisDir + os.sep + u'data/%s/trialdata' % (expInfo['participant'])
#u'data/%s_%s_%s'

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=exp_name, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=_thisDir,
   savePickle=True, saveWideText=True,
    dataFileName=filename)

# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file
######



##
conditions=[{'Task': expInfo['expName']}]




conditions2=[
##L Array in array 
{'label':'Signal Stärke'},

]
    
trials = data.TrialHandler(nReps= variables.number_of_trials,
#    method='sequential', 
    extraInfo=expInfo, 
    originPath= None,
#    trialList=data.importConditions(u'Data\\_Yes-No Task_2018_Nov_13_1440.xlsx'),
    trialList=conditions,
    seed=None, name='trials')


test_trials = data.TrialHandler(nReps=variables.testtrials, method='sequential', 
    extraInfo=expInfo, originPath= None,
#    trialList=data.importConditions(u'Data\\_Yes-No Task_2018_Nov_13_1440.xlsx'),
    trialList=conditions2,
    seed=None, name='trials')

save_pic = []
time_response = 0
o = 0

thisExp.addLoop(test_trials)


thisTrial = trials.trialList[0]
thisTrial = test_trials.trialList[0]
a=0
current_trialblock = 0

# Array for the correct answers per Trialblock
dataOld = []


def quit_exp(win):
    '''
    where "win" has to be a visual.Window-type

    this function has no output

    this function draws "Beenden" on the screen and closes the window after 1 second
    '''
    draw_component.setAutoDraw(False)
    win.flip()
    quit_inst.draw()
    win.flip()
    ##### NEW TRY
    # these shouldn't be strictly necessary (should auto-save)
    
    thisExp.saveAsWideText(filename+'.csv')
#    thisExp.saveAsPickle(filename)
#    logging.flush()
    
    # make sure everything is closed down
    thisExp.abort()  # or data files will save again on exit
    ##### BETWEEN
#    core.wait(1)
    win.close()
    core.quit()


# creates the window for the experiment
window = visual.Window(
    color=[0, 0, 0],
    fullscr=True,
    size=[variables.screensize_x, variables.screensize_y],
    units='pix')

# create a mouse object and set it's visibility to false
m = event.Mouse(win = window)
m.setVisible(False)

# ensures that no globalKeys exist to prevent problems with binding
event.globalKeys.remove(key='all')

# if "q" or "escape" are pressed at any point of the experiment,
# cancel it and draw "Beenden..."
event.globalKeys.add(
    key='q',
    func=quit_exp,
    func_args=[window],
    name='quit through q')
event.globalKeys.add(
    key='escape',
    func=quit_exp,
    func_args=[window],
    name='quit through esc')

quit_inst = visual.TextStim(window,
                            'Beenden...',
                            pos=[0, 0])

# initialize_failed == True if parameters which lead to problems are chosen
# then close the "window"
if variables.initialize_failed:
    window.close()

# creates an object of the class "BuildMatrix"
# with this object you can request new "noise" or "noise paired with
# stimulus"-images
image_factory = BuildMatrix()

# hands the object "init", with the initialized variables, to the object
# "image_factory"
image_factory.give_image_factory_var(variables)

# initializes the parameters which are only needed once
image_factory.init()

# loads the given signal intensity for the image (noise paired with stimulus)
image_factory.refresh_signal_intensity()


# for blocking in Trial (4IFC)
# neuer Name --> macht dass erster durch geht (zufallszahl) danach kommt
# nicht mehr durch
single_pass = True

# intern variable to count trialblocks
trial_blocks = 0

# intern variable to count the trial
trial = 0

# initialize value
inconstant_value = 0

# new_signal_intensity is an intern variable which will be in- and decreased
# thoughout the experiment, if "decrease_intensity" is activated;
# initialized with the signal intensity from the gui
new_signal_intensity = 0.0
new_signal_intensity = variables.signal_intensity

# saves the count of correct answers in one try
save = []


# response of the testperson, initialized with 0 for "not answered"
response_test_person = 0


# initialize an object of the TrialEvaluation class, which has functions
# to evaluate the testpersons answer
response_evaluation = TrialEvaluation()


# first instruction which is the same for every task
trial_inst_1 = visual.TextStim(window, variables.instruction, pos=[0, 100])
# instruction2 which is assigned in the variable_store
trial_inst_2 = visual.TextStim(window, variables.instruction2, pos=[400, 0])
# instruction3 which is assigned in the variable_store
trial_inst_3 = visual.TextStim(window, variables.instruction3, pos=[400, 0])
# instruction4 which is assigned in the variable_store
trial_inst_4 = visual.TextStim(window, variables.instruction4, pos=[0, 0])
blockinstruction  = u"""
Trialblock abgeschlossen!
\nSie können nun eine Pause machen. 
\nZum Fortfahren drücken Sie "w".
"""
block_inst = visual.TextStim(window, blockinstruction, pos=[0, 0])


# textstimulus telling the user the test trials are over
test_trial_over = visual.TextStim(
    window, "Testtrial abgeschlossen", pos=[0, 100])


# function that creates a fixation cross in diffrent colors
def build_cross(cross_color):
    '''
    where "cross_color" has to be a color recognized by PsychoPy

    this function returns a fixationcross in given ("cross_color") color

    the cross has the size of 5 pixels in each direction
    '''
      
#    fixationskreuz = visual.Rect(
#        win=window,
#        vertices=((0, -5), (0, 5), (0, 0), (-5, 0), (5, 0)),
#        lineWidth=10,
#        closeShape=False,
#        lineColor=cross_color
#    )
    if cross_color == "black":
        fixationskreuz = visual.Rect(
            win=window,            
            width=5, 
            height=5,
            vertices=((0, -50), (0, 50), (0, 0), (-50, 0), (50, 0)),
            lineWidth=30,
            closeShape=True,
            lineColor=cross_color)
    else:
        fixationskreuz = visual.Rect(
            win=window,
            vertices=((0, -5), (0, 5), (0, 0), (-5, 0), (5, 0)),
            lineWidth=10,
            closeShape=False,
            lineColor=cross_color
        )
    return fixationskreuz


# to initialize a fixation cross in red, green or black
positive_feedback = build_cross("lime")
negative_feedback = build_cross("red")
fixation_cross = build_cross("black")

# in case for leaving the instruction draw quit needs 
draw_component = fixation_cross

variables.picture_save = False
picture_number = 1
#_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
picture_location = _thisDir + os.sep + u'data/Fotos/%s_%s_%s' % (expInfo['participant'], exp_name, expInfo['date'])
#
def create_image(stim):
    '''
    where "stim" has to be a boolean

    this function creates an image out of a matrix with help of the "image_factory"

    if "stim" == False --> Image (noise)

    if "stim" == True --> Image (stimulus + noise)

    if "stim" == True and "variables.random_intensity == True
    --> Image (stimulus with random intensity + noise)

    returns an "image" type visual.ImageStim
    '''
        
    if (stim and variables.random_intensity):
        new_matrix = image_factory.build_matrix_with_random_signal()
    elif stim:
        new_matrix = image_factory.build_matrix_with_signal()
    else:
        new_matrix = np.round_(image_factory.build_matrix_without_signal(), decimals=0)
    if (variables.picture_save == True):
        img = Image.fromarray(new_matrix)
        img.save(picture_location + '_%s' % (variables.picture_number) + ".jpg", "JPEG", quality=80, optimize=True, progressive=True)
        variables.picture_number = variables.picture_number + 1 
        variables.picture_save = False
    image = visual.ImageStim(
        win=window,
        name='Matrix',
        image= Image.fromarray(new_matrix),
        mask=None,
        ori=0,
        pos=(0, 0),
        color=[1, 1, 1],
        colorSpace='rgb',
        opacity=1,
        flipHoriz=False,
        flipVert=False,
        texRes=256,
        interpolate=False,
        depth=0.0)

    return image


# random boolean which determines if a stimulus will be drawn or not
has_stim = bool(random.getrandbits(1))

# opposite of the random boolean has_stim
has_stim_2 = not has_stim
# creates an image consisting of noise or a stimulus + noise
# NOCH GENUTZT?!
#current_image = create_image(has_stim)

first_has_stim = True

answer_given = False

# to save the starting signal_intensity, initialized once at the start of the experiment
# because variables.signal_intensity changes over time
constant_value = variables.signal_intensity

# for blocking in trial
single_pass = True

# counter-variable for the index of the "trial_composition[i]"
i = 0

# "blocked" indicates wether a component is running (blocked = True) or
# not (blocked = False)
blocked = False

### INSTRUCTION ###

# if this is the first trial, draw the instructions
if trial == 0:

    # draw "instruction1" (instruction page 1)
    trial_inst_1.draw()
    window.flip()
    # press "w" to continue code (instruction page 2)
    event.waitKeys(keyList=["w"])
    example_image = create_image(True)
    example_image.draw()
    trial_inst_2.draw()
    window.flip()
    # press "w" to continue code (instruction page 3)
    event.waitKeys(keyList=["w"])
    # if the experiment_type is constant stimuli, draw a stronger stimulus, else
    # draw only noise so the user can compare
    if variables.experiment_type == "Constant Stimuli":
        image_factory.variables.signal_intensity = constant_value + 5
        image_factory.refresh_signal_intensity()
        example_image = create_image(True)
    else:
        example_image = create_image(False)
    example_image.draw()
    trial_inst_3.draw()
    window.flip()
    # press "w" to continue code (instruction page 4)
    event.waitKeys(keyList=["w"])
    trial_inst_4.draw()
    window.flip()
    # press "w" to continue code (countdowntimer)
    event.waitKeys(keyList=["w"])
    countdown_clock = core.CountdownTimer(3.5)

    # draw the countdown for 3,5 seconds till the experiment starts
    while countdown_clock.getTime() > 0:

        countdown_text = visual.TextStim(window,
                                         int(round(countdown_clock.getTime())),
                                         pos=[0, 0])
        countdown_text.draw()
        window.flip()

    ### INSTRUCTION DONE ###

    ### INITIALIZE TESTTRIALS IF NEEDED ###

# max_trial holds the number of trials executed per trialblock;
# if testTrialCondidition is True, it blocks the testrials from being saved

# if "variables.testtrials" != 0, "max_trial" holds the amount of testtrials
# until they are finished
if variables.testtrials != 0:
    max_trial = variables.testtrials
    testtrial_condition = True
    trials_loop = test_trials
    variables.trial_blocks = variables.trial_blocks + 1 

# if "variables.testtrials" == 0 (no test-trials activated),
# "max_trial" holds the amount of "variables.number_of_trials"
else:
    max_trial = variables.number_of_trials
    testtrial_condition = False
    trials_loop = trials

thisTrial = trials_loop.trialList[0]
thisExp.addLoop(trials_loop)
    ### START OF THE EXPERIMENT ###

#################### scheme of execution##################
#
# while (trial_blocks < variables.trial_blocks):
#    if trial== max_trial:
#       trial_blocks ++
#       trial = 0
#    while (trial < ):
#       if len(variables.trial_composition) == i:
#          trial ++
#          i = 0
#       while (len(variables.trial_composition) > i)
#           if trial_composition[i] = x:
#               execute component-x
#               i++
#
##########################################################


for trial_blocks in range (variables.trial_blocks):
#while trial_blocks < variables.trial_blocks:
    ### BETWEEN TWO TRIALBLOCKS ROUTINE ###

####
    #NEXT Condition
####
    
        ### TRIAL ROUTINE ###
    for thisTrial in trials_loop:
        
 ################################## 
      

                    
        ######################
        
        
#        if trial > max_trial or trial_blocks > variables.trial_blocks:
#            break
        
        continueRoutine = True
        trialComponents = [image_factory.variables.signal_intensity,response_test_person]
        
        # as long as counter-variable "trial" < "max_trial" and
        # "trial_blocks" < "variables.trial_blocks", continue the loop
        
#        while trial < max_trial and trial_blocks < variables.trial_blocks:
            
        while(continueRoutine):
            trial_clock = core.Clock()
            answer_clock = core.Clock()
            ### BETWEEN TRIAL ROUTINE ###
    
            # if len(variables.trial_composition) == i, the trial is over
            if len(variables.trial_composition) == i:
                # activate a trial_clock
                trial_clock = core.Clock()
                # go to next trial
                trial = trial + 1
                # start next trial again at variables.trial_composition[0]
                i = 0
                # "single_pass" is a variable, that is set on True between two trials
                # to create just one random number per trial (at 4IFC task)
                single_pass = True
                

                
                
                ### SAVE DATA OF TRIAL ###
    
                # only if it's not a testtrial
                if testtrial_condition  == False:
                    dataOld.append([response_test_person])
                    
                    np.savetxt(
                        variables.data_path,
                        dataOld,
                        delimiter="\t"
                    )
                        ##NEW### end Trial routine
                    
        #            for thisTrial in trials:
        #            for thisTrial in trials:
                    trialComponents = [image_factory.variables.signal_intensity]
                    #response_test_person
                    respone = response_test_person
                    if (exp_name == "Yes-No Task"or exp_name == "2IFCnew"):
                        response = response_evaluation.response_name(response_test_person)
                    else:
                        if response_test_person == 1:
                            response = "correct answer"
                        if response_test_person == 2:
                            response  = "wrong answer"
                    
                    if exp_name == "Constant Stimuli":
                        trials_loop.addData('signal_intensity', inconstant_value)
                    else:
                        trials_loop.addData('signal_intensity', image_factory.variables.signal_intensity)
                        
                    if (exp_name == "Constant Stimuli"):
                        trials_loop.addData('constant Value', constant_value)
                    else:
                        trials_loop.addData('constant Value', -1)
                
#                    trials_loop.addData('signal_picture', save_pic)
                    trials_loop.addData('response', response)
                    trials_loop.addData('time_response', time_response)
                    trials_loop.addData('signal_on_stimuluspos1', first_has_stim)
                    if exp_name == "2IFC":
                        trials_loop.addData('signal_on_stimuluspos2', not first_has_stim)
                    if exp_name == "2IFC":
                        trials_loop.addData('signal_on_stimuluspos2', not first_has_stim)
                    else:
                        trials_loop.addData('signal_on_stimuluspos2', - 1)
                    if (exp_name == "2IFC"):
                        trials_loop.addData('stimulus_name_pos1', 'stimulus%s_%s_%s' % (expInfo['participant'], exp_name, expInfo['date']) + '_%s' % (variables.picture_number - 2))
                        trials_loop.addData('stimulus_name_pos2', 'stimulus%s_%s_%s' % (expInfo['participant'], exp_name, expInfo['date']) + '_%s' % (variables.picture_number -1))
                    else:
                        trials_loop.addData('stimulus_name_pos1', 'stimulus_%s_%s_%s' % (expInfo['participant'], exp_name, expInfo['date']) + '_%s' % (variables.picture_number -1 ))
                        trials_loop.addData('stimulus_name_pos2', -1)
                        
                    thisExp.nextEntry()

                    
                    ####
                    
                    ##Get redy for next trial
                    response_test_person = 0
                
                continueRoutine = False
                
                
                ### TRIAL-COMPONENTS ###
                
                
                
            # each trial is put together out of diffrent trial-components
            # in "variables.trial_composition[i]";
            # if len(variables.trial_composition) == i, the trial is over
            while (len(variables.trial_composition) > i and max_trial > trial):
    
                ##FIXATIONCROSS##
    
                # if trial_composition[i] == 1, draw the fixation cross
                if i < len(
                        variables.trial_composition) and variables.trial_composition[i] == 1:
                    
                    draw_component = fixation_cross
                    draw_component.setAutoDraw(True)
                    
                    # blocked indicates wether a component is running (blocked = True)
                    # or not (blocked = False); it also guarantees that "frame_remains"
                    # is only initialized once at the start of the component
                    if not blocked:
                        # initialize remaining frames (time); stop component
                        # if remaining time - 3/4 of the monitorFramePeriod is over
                        # because of the latency of the monitor
                        frame_remains = trial_clock.getTime() + variables.time_fixation_cross - \
                            window.monitorFramePeriod * 0.75
                        blocked = True
    
                    # if time for component is over, increase i (next component);
                    # set blocked to False (component is done)
                    # and stop drawing component (setAutodraw(false))
                    if trial_clock.getTime() > frame_remains:
                        draw_component.setAutoDraw(False)
                        i = i + 1
                        blocked = False
    
                ##MASK##
    
                # if trial_composition[i] == 2, show the mask
                # this component shows the plain background for given time
                if i < len(
                        variables.trial_composition) and variables.trial_composition[i] == 2:
    
                    # initialize routine for trial-component
                    if not blocked:
                        frame_remains = trial_clock.getTime() + variables.time_blank_screen - \
                            window.monitorFramePeriod * 0.75
                        blocked = True
    
                    if trial_clock.getTime() > frame_remains:
                        #component is done
                        i = i + 1
                        blocked = False
    
                ##STIMULUS YES/NO TASK AND FIRST STIMULUS FOR 2IFC##
    
                # if trial_composition[i] == 3, draw the Stimulus for yes/no task
                # this component shows image of (noise) or (noise + stimulus)
                if i < len(
                        variables.trial_composition) and variables.trial_composition[i] == 3:
    
                    # initialize routine for trial-component
                    if not blocked:
                        frame_remains = trial_clock.getTime() + variables.time_stimulus - \
                            window.monitorFramePeriod * 0.75
                        blocked = True
                        # has_stim decides wether we have an image with noise
                        # or with noise + stimulus
                        has_stim = bool(random.getrandbits(1))
                        variables.picture_save = True
                        draw_component = create_image(has_stim)
                        # variable for saving
                        first_has_stim = has_stim
                        
                        
                        # draw that image
                        draw_component.setAutoDraw(True)
    
                    if trial_clock.getTime() > frame_remains:
                        #component is done
                        draw_component.setAutoDraw(False)
                        i = i + 1
                        blocked = False
    
                ##ANSWERPERIOD YES/NO TASK ##
    
                # if trial_composition[i] == 4, start answerperiod of the yes/no task
                # this component gets an input of "y" for yes or "n" for no
                # it evaluates the answer and saves it in "response_test_person"
                if i < len(
                        variables.trial_composition) and variables.trial_composition[i] == 4:
    
                    # initialize routine for trial-component
                    if not blocked:
                        frame_remains = trial_clock.getTime() + variables.time_answer - \
                            window.monitorFramePeriod * 0.75
                        blocked = True
                        # clear the key input list
                        event.clearEvents()
                        answer_clock.reset()
                    
                    if answer_given == False:
                        # Event No
                        if event.getKeys(keyList=["n"]):
                            # "response_evaluation.get_answer_yes_no()" evaluates the answer of the
                            # tested person and gives back 1-4 (hit, miss, correct rejection, 
                            # false alarm), which is saved in "response_test_person"
                            response_test_person = response_evaluation.get_answer_yes_no(
                                False, has_stim)
                            answer_given = True 
                            time_response= answer_clock.getTime()
                            # unlock blocked(False) for next component
                            if exp_name != "2IFCnew":
                                blocked = False
                                i = i + 1
        
                        # Event Yes
                        if event.getKeys(keyList=["y"]):
                            # "response_evaluation.get_answer_yes_no() evaluates the answer
                            # of the tested person and gives back 1-4 (hit, miss, correct rejection,
                            # false alarm), which is saved in "response_test_person"
                            response_test_person = response_evaluation.get_answer_yes_no(
                                True, has_stim)
                            answer_given = True 
                            time_response= answer_clock.getTime()
                            if exp_name != "2IFCnew":
                                blocked = False
                                i = i + 1
    
                    # Event no answer
                    if trial_clock.getTime() > frame_remains:
                        # response_test_person = 0 for no answer
                        if exp_name != "2IFCnew":
                            response_test_person = 0
                            time_response= - 1
                            
                        i = i + 1
                        blocked = False
                        answer_given = False
                        ## -1 = no answer
                        
                        
#                    print (time_response)
                    ##FEEDBACK##
    
                # if trial_composition[i] == 5, draw the feedback;
                # this component is used for assigning the "response_test_person"
                # with a green (for correct), a red (for false) or a
                # black cross (for no answer)
                if i < len(
                        variables.trial_composition) and variables.trial_composition[i] == 5:
    
                    # initialize routine for trial-component
                    if not blocked:
                        frame_remains = trial_clock.getTime() + variables.time_feedback - \
                            window.monitorFramePeriod * 0.75
                        blocked = True
    
                    # assign response_test_person to a cross in the right color
                    if response_test_person == 0:
                        # no answer --> "specific_feedback" = black cross
                        draw_component = fixation_cross
    
                    if response_test_person == 1 or response_test_person == 3:
                        # hit or correct rejection --> "specific_feedback" = green
                        # cross
                        draw_component = positive_feedback
    
                    if response_test_person == 2 or response_test_person == 4:
                        # miss or false alarm --> "specific_feedback" = red cross
                        draw_component = negative_feedback
    
                    # draw the cross in evaluated color
                    draw_component.setAutoDraw(True)
    
                    # component is over, reset everything to be ready for the
                    # next trialcomponent
                    if trial_clock.getTime() > frame_remains:
                        draw_component.setAutoDraw(False)
                        i = i + 1
                        blocked = False
    
                    ## BREAK ##
    
                # if trial_composition[i] == 6, do a pause
                # this component shows the plain background of the window
                # for "variables.time_pause" seconds
                if i < len(
                        variables.trial_composition) and variables.trial_composition[i] == 6:
    
                    # initialize routine for trial-component
                    if not blocked:
                        frame_remains = trial_clock.getTime() + variables.time_pause - \
                            window.monitorFramePeriod * 0.75
                        blocked = True
    
                    if trial_clock.getTime() > frame_remains:
                        #component is done
                        i = i + 1
                        blocked = False
    
                    ##SECOND STIMULUS OF 2IFC##
    
                # if trial_composition[i] == 7, show the second stimulus of the 2IFC-task
                # this component shows stimulus + noise if the first image was just noise
                # and shows just noise without stimulus, if the first image was
                # (stimulus + noise)
                if i < len(
                        variables.trial_composition) and variables.trial_composition[i] == 7:
    
                    # initialize routine for trial-component
                    if not blocked:
                        # the second stimulus is the negation of the first
                        # stimulus
                        has_stim_2 = not has_stim
                        # create a new matrix with the opposite of the first one
                        variables.picture_save = True
                        draw_component = create_image(has_stim_2)
                        draw_component.setAutoDraw(True)
                        # calculate the remaining time
                        frame_remains = trial_clock.getTime() + variables.time_stimulus - \
                            window.monitorFramePeriod * 0.75
                        
                        blocked = True
                        
    
                    if trial_clock.getTime() > frame_remains:
                        #component is done
                        draw_component.setAutoDraw(False)
                        i = i + 1
                        blocked = False
    
                    ## EVALUATION 2IFC- TASK ##
    
                # if trial_composition[i] == 8, start the evaluation component
                # this component listens to the button and if "1" or "2" is pressed,
                # the input gets evaluated
                if i < len(
                        variables.trial_composition) and variables.trial_composition[i] == 8:
    
                    # initialize routine for trial-component
                    if not blocked:
                        frame_remains = trial_clock.getTime() + variables.time_answer - \
                            window.monitorFramePeriod * 0.75
                        blocked = True
                        answer_clock.reset()
                        event.clearEvents()
    
                    # Event 1
                    if event.getKeys(keyList=["1"]):
                        # if "1" is pressed, "response_evaluation.get_answer_2ifc() evaluates
                        # the answer of the tested person and gives back 1 or 2
                        # (1 for correct and 2 for wrong), which is saved in "response_test_person"
                        response_test_person = response_evaluation.get_answer_2ifc(has_stim)
                        i = i + 1
                        time_response= answer_clock.getTime()
                        blocked = False
    
                    # Event 2
                    if event.getKeys(keyList=["2"]):
                        # if "2" is pressed, "response_evaluation.get_answer_2ifc() evaluates
                        # the answer of the tested person and gives back 1 or 2
                        # (1 for correct and 2 for wrong), which is saved in "response_test_person"
                        response_test_person = response_evaluation.get_answer_2ifc(has_stim_2)
                        i = i + 1
                        time_response= answer_clock.getTime()
                        blocked = False
    
                    # if answering time is over, assign 0 to "response_test_person"
                    if trial_clock.getTime() > frame_remains:
                        response_test_person = 0
                        i = i + 1
                        time_response= - 1
                        blocked = False
    
                    ## STIMULUS 4IFC ##
    
                # if trial_composition[i] == 9, show a stimulus of the 4IFC task
                # this component is executed 4 times each trial, 1 time it shows (stimulus + noise)
                # and 3 times it shows just noise without the stimulus
                if i < len(
                        variables.trial_composition) and variables.trial_composition[i] == 9:
    
                    # initialize routine for trial-component
                    if not blocked:
    
                        # this condition is only true once in a trial
                        # single_pass is set on True again in the "BETWEEN TRIAL
                        # ROUTINE"
                        if single_pass:
                            # image_with_stim is a random number between 1 and 4,
                            # which presents the stimulus
                            image_with_stim = random.randint(1, 4)
                            # image_number is used to compare if the current image
                            # is the one where the stimulus needs to be drawn;
                            # increased with each image
                            image_number = 1
                            # block this codesegment till next trial
                            single_pass = False
    
                        # if the counter-variable "image_number" is equal to
                        # "image_with_stim", draw an image with noise + stimulus
                        if image_with_stim == image_number:
                            draw_component = create_image(True)
    
                        # if image_with_stim != image_number --> draw an image
                        # (just noise)
                        else:
                            draw_component = create_image(False)
    
                        # setAutoDraw(True) for the "current_image" initialized
                        # above
                        draw_component.setAutoDraw(True)
                        # increase the counter-variable "image_number"
                        image_number = image_number + 1
                        frame_remains = trial_clock.getTime() + variables.time_stimulus - \
                            window.monitorFramePeriod * 0.75
                        blocked = True
    
                    if trial_clock.getTime() > frame_remains:
                        #component is done
                        draw_component.setAutoDraw(False)
                        i = i + 1
                        blocked = False
    
                    ## EVALUATION 4IFC ##
    
                # if trial_composition[i] == 10, start the evaluation component
                # this component listens to the button and evaluate the inputs
                # "1","2","3","4"
                if i < len(
                        variables.trial_composition) and variables.trial_composition[i] == 10:
    
                    # initialize routine for trial-component
                    if not blocked:
                        frame_remains = trial_clock.getTime() + variables.time_answer - \
                            window.monitorFramePeriod * 0.75
                        blocked = True
                        event.clearEvents()
    
                    # Event 1
                    if event.getKeys(keyList=["1"]):
                        # if "1" is pressed, "response_evaluation.get_answer_4ifc() evaluates
                        # the answer of the tested person and gives back 1 or 2 (1 for correct
                        # and 2 for wrong answer) which is saved in "response_test_person"
                        response_test_person = response_evaluation.get_answer_4ifc(
                            1, image_with_stim)
                        i = i + 1
                        blocked = False
    
                    # Event 2
                    if event.getKeys(keyList=["2"]):
                        # evaluates response with help of
                        # "response_evaluation.get_answer_4ifc()" and handed parameters
                        response_test_person = response_evaluation.get_answer_4ifc(
                            2, image_with_stim)
                        i = i + 1
                        blocked = False
    
                    # Event 3
                    if event.getKeys(keyList=["3"]):
                        # evaluates response with help of
                        # "response_evaluation.get_answer_4ifc()" and handed parameters
                        response_test_person = response_evaluation.get_answer_4ifc(
                            3, image_with_stim)
                        i = i + 1
                        blocked = False
    
                    # Event 4
                    if event.getKeys(keyList=["4"]):
                        # evaluates response with help of
                        # "response_evaluation.get_answer_4ifc()" and handed parameters
                        response_test_person = response_evaluation.get_answer_4ifc(
                            4, image_with_stim)
                        i = i + 1
                        blocked = False
    
                    # if answering time is over, assign 0 to "response_test_person"
                    if trial_clock.getTime() > frame_remains:
                        response_test_person = 0
                        i = i + 1
                        blocked = False
    
                    ##CONSTANT STIMULI ##
    
                # if trial_composition[i] == 11, start the constant stimuli component
                # this component is executed 2 times each trial; the first image
                # shows either a constant or an inconstant stimulus (which is picked
                # out of a gausian distribution around the constant). A random boolean
                # decides which one is presented first, the other one is presented
                # second
                if i < len(
                        variables.trial_composition) and variables.trial_composition[i] == 11:
    
                    # initialize routine for trial-component
                    if not blocked:
    
                        # single_pass is True only once every trial, so the
                        # codesegment below will be executed just 1 time, while this
                        # component is executed 2 times
                        # unverständlich!!!!!!!!!!!!!!!!!!!!
                        if single_pass:
                            # second_is_constant decides whether the constant or
                            # inconstant stimulus is presented first
                            second_is_constant = bool(random.getrandbits(1))
                            # set single_pass on False till next trial
                            single_pass = False
    
                            if second_is_constant:
                                # pos_of_constant saves the position of the constant
                                # stimulus
                                pos_of_constant = 2
                            else:
                                pos_of_constant = 1
    
                            # initialize the inconstant_value which is picked out of a
                            # gausian distribution, with mean "constant_value" and
                            # derivation = 1)
                            inconstant_value = round(
                                np.random.normal(constant_value, 1), 0)
                            # if the constant stimulus has the same intensity as the inconstant
                            # stimulus, a random boolean decides whether the inconstant
                            # intensity gets +1 or -1
                            if constant_value == inconstant_value:
                                add_1 = bool(random.getrandbits(1))
                                if add_1:
                                    inconstant_value = inconstant_value + 1
                                if not add_1:
                                    inconstant_value = inconstant_value - 1
                            ##single_pass over##
    
                        # if second_is_constant == True --> draw the
                        # inconstant stimulus
                        if second_is_constant:
                            # update the image_factory with the intensity of the
                            # inconstant stimulus
                            image_factory.variables.signal_intensity = inconstant_value
                            image_factory.refresh_signal_intensity()
                            # create an image (noise + stimulus) with updated
                            # intensity
                            draw_component = create_image(True)
    
                        # if second_is_constant != True --> draw the constant
                        # stimulus
                        else:
                            # update the image_factory with the intensity of the
                            # constant stimulus
                            image_factory.variables.signal_intensity = constant_value
                            image_factory.refresh_signal_intensity()
                            # create an image (noise + stimulus) with updated
                            # intensity
                            draw_component = create_image(True)
    
                        blocked = True
                        frame_remains = trial_clock.getTime() + variables.time_stimulus - \
                            window.monitorFramePeriod * 0.75
                        draw_component.setAutoDraw(True)
                        # negate the variable "second_is_constant" so it executes
                        # the opposite stimulus the next time
                        second_is_constant = not second_is_constant
    
                    if trial_clock.getTime() > frame_remains:
                        draw_component.setAutoDraw(False)
                        i = i + 1
                        blocked = False
                
                
                 ### EVALUATION CONSTANT STIMULI ##
    
                # if trialComposition[i] == 12, start the evaluation for constant stimuli;
                # this component evaluates whether the tested person has given a right answer
                # --> "response_test_person" = 1 or a wrong answer --> "response_test_person" = 2
                if i < len(
                        variables.trial_composition) and variables.trial_composition[i] == 12:
                    
                    # initialize routine for trial-component
                    if not blocked:
                        frame_remains = trial_clock.getTime() + variables.time_answer - \
                            window.monitorFramePeriod * 0.75
                        blocked = True
                        # difference is used to decide wether constant or inconstant intensity is bigger;
                        # difference > 0 if constant stimulus intensity is bigger;
                        # difference < 0 if inconstant stimulus intensity is bigger
                        difference = constant_value - inconstant_value
                        answer_clock.reset()
                        event.clearEvents()
    
                    # Event 1
                    if event.getKeys(keyList=["1"]):
                        # if "1" is pressed, "response_evaluation.get_answer_constant_stimuli()" 
                        # evaluates the answer of the tested person and give back 1 or 2 (1 for correct 
                        # and 2 for wrong), which is saved in "response_test_person"
                        response_test_person = response_evaluation.get_answer_constant_stimuli(
                            1, difference, pos_of_constant)
                        i = i + 1
                        time_response= answer_clock.getTime()
                        blocked = False
    
                    # Event 2
                    if event.getKeys(keyList=["2"]):
                        # if "2" is pressed, "response_evaluation.get_answer_constant_stimuli()" 
                        # evaluates the answer of the tested person and give back 1 or 2 (1 for correct 
                        # and 2 for wrong), which is saved in "response_test_person"
                        response_test_person = response_evaluation.get_answer_constant_stimuli(
                            2, difference, pos_of_constant)
                        i = i + 1
                        time_response= answer_clock.getTime()
                        blocked = False
    
                    # if answering time is over, assign 0 to "responseTestPerson"
                    if trial_clock.getTime() > frame_remains:
                        response_test_person = 0
                        i = i + 1
                        time_response= - 1
                        blocked = False
                
                # if trial_composition[i] == 13, start answerperiod of the yes/no task
                # this component gets an input of "y" for yes or "n" for no
                # it evaluates the answer and saves it in "response_test_person"
                if i < len(
                        variables.trial_composition) and variables.trial_composition[i] == 13:
    
                    # initialize routine for trial-component
                    if not blocked:
                        frame_remains = trial_clock.getTime() + variables.time_answer - \
                            window.monitorFramePeriod * 0.75
                        blocked = True
                        # clear the key input list
                        event.clearEvents()
                        answer_clock.reset()

                    
                    # Event No
                    
                        
                    if answer_given == False:     
                        if event.getKeys(keyList=["n"]):
                            answer_given = True 
                            if response_test_person == 2 or response_test_person == 3:
                                # "response_evaluation.get_answer_yes_no()" evaluates the answer of the
                                # tested person and gives back 1-4 (hit, miss, correct rejection, 
                                # false alarm), which is saved in "response_test_person"
                                response_test_person_second = response_evaluation.get_answer_yes_no(
                                    False, has_stim)
                                
    #                            i = i + 1
                                response_test_person = 2
                                time_response= answer_clock.getTime()
                            else:        
                                response_test_person = 1
                                time_response= answer_clock.getTime()
                                # unlock blocked(False) for next component
    #                            blocked = False
                            
        
                        # Event Yes
                        
                        if event.getKeys(keyList=["y"]):
                            # "response_evaluation.get_answer_yes_no() evaluates the answer
                            # of the tested person and gives back 1-4 (hit, miss, correct rejection,
                            # false alarm), which is saved in "response_test_person"
                            answer_given = True 
                            if response_test_person == 1 or response_test_person == 4:
                                response_test_person_second = response_evaluation.get_answer_yes_no(
                                    True, has_stim)
    #                            i = i + 1
                                
                                response_test_person = 2
                                time_response_second = answer_clock.getTime()
    #                            blocked = False
                            else:
                                response_test_person = 1
                                time_response_second = answer_clock.getTime()
                    # Event no answer
                    if trial_clock.getTime() > frame_remains:
                        # response_test_person = 0 for no answer
#                        response_test_person_second = 0
                        i = i + 1
                        blocked = False
#                        if response_test_person == 1 or response_test_person == 3:
                            
                        ## -1 = no answer
                        if answer_given == False :
                            time_response_second = - 1     
                            
                        answer_given = False
                # flip updates the screen continuously
                window.flip()
    
                # if maximum trials are reached, start the between-trialblock-routine
    if trial == max_trial:
        
        # trial needs to be reseted ("trial" = 0)
        trial = 0

        ### TESTTRIAL CONDITION ###

        # if there are testtrials (only executed once at the start of the
        # experiment, if "testtrial_condition" == True)
        if testtrial_condition:
            # set countdown_clock on 5s and draw the testtrial_over_inst;
            # from now on "max_trial" has the amount of
            # "variables.number_of_trials"
            max_trial = variables.number_of_trials
            testtrial_condition = False
            countdown_clock = core.CountdownTimer(3.5)
            testtrial_over_inst = True
            trials_loop = trials
            thisTrial = trials.trialList[0]
#            thisExp.nextEntry()
            ### NO TESTTRIAL CONDITION (SAVE DATA OF TRIALBLOCK) ###

        # else (no testtrials (left))
        else:
            ############ pause zwischen blocks ###################
            ######################################################
            if trial_blocks + 1 < variables.trial_blocks:
                block_inst.draw()
                window.flip()
                event.waitKeys(keyList=["w"])
            ######################################################
            ######################################################
            
            # save the results of the last trialblock
            D = np.array(dataOld)
            # create a new array to save the results of the next trialblock
            dataOld = []

            # 0 no answer
            # 1 HIT (yesTrue)
            # 2 FALSE ALARM (yesFalse)
            # 3 CORRECT REJECTION (noTrue)
            # 4 MISS (noFalse)
            # correct = HIT + CORRECT REJECTION
            correct = np.sum(np.logical_or(D[:, 0] == 1, D[:, 0] == 3))
            print(
                "%i/%i, %g%%" %
                (correct,
                 variables.number_of_trials,
                 correct /
                 variables.number_of_trials *
                 100))
            # save the amount of correct answers in the array save
            save.insert(trial_blocks, correct)
            # "trial_blocks" ++ to go to next trialround
            
#            print(trial_blocks)
            # countdown in between trialblocks
            countdown_clock = core.CountdownTimer(3.5)
            # dont draw testtrial_over_inst between 2 regular trialblocks
            testtrial_over_inst = False

            
            
            ### INTENSITY DOWN CONDITION ###

            # if "decrease_intensity" == True, refresh the newSignalIntesity
            if variables.decrease_intensity:
#                print(new_signal_intensity)
#                print(variables.intensity_steps)
                new_signal_intensity = new_signal_intensity - variables.intensity_steps
#                print(new_signal_intensity)
                # update the "signal_intensity" of the variables object,
                # which belongs to the image_factory-object
                image_factory.variables.signal_intensity = new_signal_intensity
                # refresh the signal_intensity of the image_factory, for the next
                # matrix
                image_factory.refresh_signal_intensity()

            ### BETWEEN TRIALBLOCK COUNTER ###
        # countdown to show the trialblock is over and the next trialblock has
        # possibly new conditions or settings;
        # "trial_blocks" < "variables.trial_blocks" ensures the countdown isn't
        # drawn after the last trialblock
        trial_blocks = trial_blocks + 1
        if trial_blocks < variables.trial_blocks:

            # shows a countdown between 2 trialblocks
            while countdown_clock.getTime() > 0:
                countdown_text = visual.TextStim(window, int(
                    round(countdown_clock.getTime())), pos=[0, 0])
                countdown_text.draw()
                # if the last trialblock was testtrials, also draw the
                # "test_trial_over"-text
                if testtrial_over_inst:
                    test_trial_over.draw()
                window.flip()
        

    
    conditions = [{'Task': expInfo['expName']}]  
    
    trials_loop = data.TrialHandler(nReps= variables.number_of_trials,
#    method='sequential', 
        extraInfo=expInfo, 
        originPath= None,
#    trialList=data.importConditions(u'Data\\_Yes-No Task_2018_Nov_13_1440.xlsx'),
        trialList=conditions,
        seed=None, name='trials') 
    

    thisExp.addLoop(trials_loop)
    thisTrial = trials_loop.trialList[0]       
    


# terminates the program
quit_exp(window)
