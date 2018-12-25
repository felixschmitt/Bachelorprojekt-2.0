# -*- coding: utf-8 -*-
"""
provides the functions to evaluate the specific tasks

"""


class TrialEvaluation:
    """
    provides the functions to evaluate the specific tasks
    
    """
    
    # evaluate yes/no task
    def get_answer_yes_no(self, key_yes, stimulus):
        '''
        where "key_yes" and "stimulus" have to be a boolean

        this function evaluates the given answer of the tested person

        it returns a number from 1-4

        1 = Hit, 2 = False alarm, 3 = Correct rejection, 4 = Miss
        '''
        # Hit --> if "stimulus" was there (True) and answer was yes
        # ("key_yes" == True)
        if (stimulus and key_yes):
            self.answer = 1
        # False Alarm  --> if "stimulus" was not there (False) and answer was
        # yes ("key_yes" == True)
        if not stimulus and key_yes:
            self.answer = 2
        # Correct Rejection  --> if "stimulus" was not there (False) and
        # answer was no ("key_yes" == False)
        if not stimulus and not key_yes:
            self.answer = 3
        # Miss --> if "stimulus" was there (True) and answer was no
        # ("key_yes" == False)
        if stimulus and not key_yes:
            self.answer = 4

        return self.answer

    # evaluate 2 IFC task
    def get_answer_2ifc(self, stimulus):
        '''
        where "stimulus" has to be a boolean

        this function checks whether the chosen image contained a stimulus or not

        it returns 1 if the answer was correct, 2 if the answer was wrong
        '''
        # if there was a stimulus --> 1 (correct)
        if stimulus:
            self.answer = 1
        # else the chosen image had no stimulus --> 2 (wrong)
        else:
            self.answer = 2

        return self.answer

    # evaluate 4 IFC Task

    def get_answer_4ifc(self, key_answer, signal_with_stim):
        '''
        where "key_answer" and "signal" have to be an intiger

        this function checks whether the chosen "key_answer" and "signal_with_stim" are the same

        it returns 1 if the answer was correct, 2 if the answer was wrong
        '''
        # if the tested person chose the image in which the stimulus was -->
        # 1
        if signal_with_stim == key_answer:
            self.answer = 1
        # else signal_with_stim != key_answer (person picked the wrong image)
        # --> 2
        else:
            self.answer = 2

        return self.answer

    def get_answer_constant_stimuli(
            self,
            key_1_or_2,
            difference,
            constant_pos):
        '''
        where "key_1_or_2", "difference" and "constant_pos" have to be a intiger

        this function evaluate wich stimulus has the higher intensity

        and checks whether the person has given the right answer

        it returns 1 if the answer was correct, 2 if the answer was wrong
        '''

        # if the "difference" is greater than zero --> constant stimulus
        # intensity is greater
        if difference > 0:
            # "key_1_or_2" and "constant_pos" could be 1 or 2
            # if the chosen image is the constant image
            if key_1_or_2 == constant_pos:
                self.answer = 1
            # else the chosen image is the inconstant image
            else:
                self.answer = 2

        # if the "difference" is less than zero --> inconstant stimulus
        # intensity is greater
        if difference < 0:
            # if the chosen image is the inconstant image
            if key_1_or_2 != constant_pos:
                self.answer = 1
            # else if the chosen image is the constant image
            else:
                self.answer = 2

        return self.answer
    
        
    def response_name(self, argument):
        if argument == 0:
            answer = 'No Answer'
        if argument == 1:  
            answer = "Hit";
        if argument == 2: 
            answer = "False Alarm";
        if argument == 3: 
            answer = "Correct Rejection";
        if argument == 4:
            answer = "Miss"
               
        return (answer)