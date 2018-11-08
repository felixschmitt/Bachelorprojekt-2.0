#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
this is the main module of the program, it creates the window running the experiment

to start the experiment run this file

'''

# import modules
from __future__ import unicode_literals, division, print_function
import sys
import random
from psychopy import core, event, visual
from PIL import Image
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

#reload(sys)
#sys.setdefaultencoding('utf8')

# only if the gui button ok is pressed, the rest of the code will be executed
#if not variables.gui.gui_input_var.OK:
#    variables.gui.core.quit()

###### STOP #######

# if the input of the second gui-page is done,
# initialize the variables with the parameters of the second gui-page
variables.set_variables()



# Array for the correct answers per Trialblock
data = []


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
    core.wait(1)
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

# if "variables.testtrials" == 0 (no test-trials activated),
# "max_trial" holds the amount of "variables.number_of_trials"
else:
    max_trial = variables.number_of_trials
    testtrial_condition = False

    ### START OF THE EXPERIMENT ###

#################### scheme of execution##################
#
# while (trial_blocks < variables.trial_blocks):
#    if trial== max_trial:
#       trial_blocks ++
#       trial = 0
#    while (trial < max_trial):
#       if len(variables.trial_composition) == i:
#          trial ++
#          i = 0
#       while (len(variables.trial_composition) > i)
#           if trial_composition[i] = x:
#               execute component-x
#               i++
#
##########################################################

while trial_blocks < variables.trial_blocks:

    ### BETWEEN TWO TRIALBLOCKS ROUTINE ###

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
            countdown_clock = core.CountdownTimer(5)
            testtrial_over_inst = True

            ### NO TESTTRIAL CONDITION (SAVE DATA OF TRIALBLOCK) ###

        # else (no testtrials (left))
        else:
            # save the results of the last trialblock
            D = np.array(data)
            # create a new array to save the results of the next trialblock
            data = []

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
            trial_blocks = trial_blocks + 1
            # countdown in between trialblocks
            countdown_clock = core.CountdownTimer(3.5)
            # dont draw testtrial_over_inst between 2 regular trialblocks
            testtrial_over_inst = False

            ### INTENSITY DOWN CONDITION ###

        # if "decrease_intensity" == True, refresh the newSignalIntesity
        if variables.decrease_intensity:
            print(new_signal_intensity)
            print(variables.intensity_steps)
            new_signal_intensity = new_signal_intensity - variables.intensity_steps
            print(new_signal_intensity)
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

        ### TRIAL ROUTINE ###

    # as long as counter-variable "trial" < "max_trial" and
    # "trial_blocks" < "variables.trial_blocks", continue the loop
    while trial < max_trial and trial_blocks < variables.trial_blocks:

        trial_clock = core.Clock()

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
            if testtrial_condition is False:
                data.append([response_test_person])
                response_test_person = 0
                np.savetxt(
                    variables.data_path,
                    data,
                    delimiter="\t"
                )

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
                    draw_component = create_image(has_stim)
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

                # Event No
                if event.getKeys(keyList=["n"]):
                    # "response_evaluation.get_answer_yes_no()" evaluates the answer of the
                    # tested person and gives back 1-4 (hit, miss, correct rejection, 
                    # false alarm), which is saved in "response_test_person"
                    response_test_person = response_evaluation.get_answer_yes_no(
                        False, has_stim)
                    i = i + 1
                    # unlock blocked(False) for next component
                    blocked = False

                # Event Yes
                if event.getKeys(keyList=["y"]):
                    # "response_evaluation.get_answer_yes_no() evaluates the answer
                    # of the tested person and gives back 1-4 (hit, miss, correct rejection,
                    # false alarm), which is saved in "response_test_person"
                    response_test_person = response_evaluation.get_answer_yes_no(
                        True, has_stim)
                    i = i + 1
                    blocked = False

                # Event no answer
                if trial_clock.getTime() > frame_remains:
                    # response_test_person = 0 for no answer
                    response_test_person = 0
                    i = i + 1
                    blocked = False

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
                    event.clearEvents()

                # Event 1
                if event.getKeys(keyList=["1"]):
                    # if "1" is pressed, "response_evaluation.get_answer_2ifc() evaluates
                    # the answer of the tested person and gives back 1 or 2
                    # (1 for correct and 2 for wrong), which is saved in "response_test_person"
                    response_test_person = response_evaluation.get_answer_2ifc(has_stim)
                    i = i + 1
                    blocked = False

                # Event 2
                if event.getKeys(keyList=["2"]):
                    # if "2" is pressed, "response_evaluation.get_answer_2ifc() evaluates
                    # the answer of the tested person and gives back 1 or 2
                    # (1 for correct and 2 for wrong), which is saved in "response_test_person"
                    response_test_person = response_evaluation.get_answer_2ifc(has_stim_2)
                    i = i + 1
                    blocked = False

                # if answering time is over, assign 0 to "response_test_person"
                if trial_clock.getTime() > frame_remains:
                    response_test_person = 0
                    i = i + 1
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
                    event.clearEvents()

                # Event 1
                if event.getKeys(keyList=["1"]):
                    # if "1" is pressed, "response_evaluation.get_answer_constant_stimuli()" 
                    # evaluates the answer of the tested person and give back 1 or 2 (1 for correct 
                    # and 2 for wrong), which is saved in "response_test_person"
                    response_test_person = response_evaluation.get_answer_constant_stimuli(
                        1, difference, pos_of_constant)
                    i = i + 1
                    blocked = False

                # Event 2
                if event.getKeys(keyList=["2"]):
                    # if "2" is pressed, "response_evaluation.get_answer_constant_stimuli()" 
                    # evaluates the answer of the tested person and give back 1 or 2 (1 for correct 
                    # and 2 for wrong), which is saved in "response_test_person"
                    response_test_person = response_evaluation.get_answer_constant_stimuli(
                        2, difference, pos_of_constant)
                    i = i + 1
                    blocked = False

                # if answering time is over, assign 0 to "responseTestPerson"
                if trial_clock.getTime() > frame_remains:
                    response_test_person = 0
                    i = i + 1
                    blocked = False

            # flip updates the screen continuously
            window.flip()


# put out the number of correct answers per trial in the console
print(save)

# show the results with a graph in the console
plt.plot(save)
plt.ylim(0, variables.number_of_trials)
plt.xlim(0, variables.trial_blocks - 1)
plt.show()

# terminates the program
quit_exp(window)
