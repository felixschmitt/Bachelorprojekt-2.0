#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
this module includes the BuildMatrix Class, which provides the operations to create an image

'''

import os
import random
import numpy as np
from PIL import Image


class BuildMatrix:
    '''
    provides all operations to create an image for a signal detection task

    '''
    

    def give_image_factory_var(self, store):
        '''
        where "store" has to be a VarStore-object

        this function attaches the given VarStore-Object to the BuildMatrix-Object

        this function has no output
        '''

        self.variables = store

    def init(self):
        '''
        this function has no input or output

        it initializes the "static" variables (which do not change over time)
        '''

        # directory the script is in, for loading the image below
        script_dir = os.path.dirname(__file__)
        
        if self.variables.signal_picture == "Haus":
            if self.variables.stimulus_size_pixels == "64x64":
                rel_path = "Haus64x64.jpg"
            if self.variables.stimulus_size_pixels == "128x128":
                rel_path = "Haus128x128.jpg"
            if self.variables.stimulus_size_pixels == "256x256":
                rel_path = "Haus256x256.jpg"
            
        # assign the chosen pixelsize from the gui to the variable "rel_path"
        if self.variables.signal_picture == "A":
            if self.variables.stimulus_size_pixels == '64x64':
                rel_path = "A64.jpg"
            if self.variables.stimulus_size_pixels == "128x128":
                rel_path = "A128.jpg"
            if self.variables.stimulus_size_pixels == "256x256":
                rel_path = "A256.jpg"
#        print(rel_path)
        # create the datapath and load the image in "img"
        # the image needs a white background (fill_value = 255) and a dark stimulus
        image_path = os.path.join(script_dir, rel_path)
        # img holds the loaded image
        img = Image.open(image_path)

        # get the pixelvalues of the image (img) and save it in "pixels"
        pixels = np.asarray(img)

        # needed to work with the pixelmatrix ("pixels")
        pixels.setflags(write=1)

        # save the pixel width (resolution of the picture)
        self.pixelwidth = len(pixels)

        # create a matrix as big as pixelwidth x pixelwidth full of fill_value = 255;
        # depth of the matrix is 3, so it can later be converted into an image-type
        white_matrix = np.full(
            (self.pixelwidth,
             self.pixelwidth,
             3),
            fill_value=255,
            dtype=np.uint8)

        # "inverse_stim_matrix" is calculated by "white_matrix" - "pixels";
        # where the stimulus was are now values >= 1, everywhere else (where the
        # background was) values of 0
        self.inverse_stim_matrix = white_matrix - pixels

        # "indices" save every index where the (color-)value is bigger or equal 1;
        # "indices" is built up as [[x-axis],[y-axis]]
        self.indices = np.where(self.inverse_stim_matrix[:, :, 0] >= 1)
        # indices of the x-axis
        self.indices_x = self.indices[0]
        # indices of the y-axis
        self.indices_y = self.indices[1]

    # if the signal intensity is changed, start this function to create a new
    # matrix with given intensity

    def refresh_signal_intensity(self):
        '''
        this is an "update" function with no input or output

        this function creates a new matrix where the pixels representing the stimulus

        get the value of the current "signal_intensity"
        '''

        # initialize the countervariable "i"
        i = 0

        # len(self.indices[0]) --> how much pixels represent the stimulus
        while i < len(self.indices[0]):
            # each pixel representing the stimulus, now gets a new signal_intensity;
            # "inverse_stim_matrix" needs to save the "signal_intensity" in all 3
            # levels (depth)
            self.inverse_stim_matrix[self.indices_x[i],
                                     self.indices_y[i],
                                     0] = self.variables.signal_intensity
            self.inverse_stim_matrix[self.indices_x[i],
                                     self.indices_y[i],
                                     1] = self.variables.signal_intensity
            self.inverse_stim_matrix[self.indices_x[i],
                                     self.indices_y[i],
                                     2] = self.variables.signal_intensity
            
            # if all 3 levels of a pixel got the new "signal_intensity",
            # increase the counter ("i")
            i = i + 1
      
        
    def build_matrix_with_signal(self):
        '''
        has no input

        this function creates an image of a gray noise + a stimulus

        this function returns an Image-type
        '''

        # add matrix with signal ("inverse_stim_matrix") to the matrix with the noise
        # (which is created by the function "build_matrix_without_signal")
        noise_signal_matrix = (
            self.build_matrix_without_signal()) + self.inverse_stim_matrix
        np.round_(noise_signal_matrix, decimals=0)
        
        return noise_signal_matrix

    def build_matrix_with_random_signal(self):
        '''
        has no input

        this function creates an image of a gray noise + a stimulus with random intensity

        this function returns an Image-type
        '''

        # pick a random value between 1 and 9
        random_signal_intensity = random.uniform(1, 9)

        # initialize countervariable "i"
        i = 0

        # each index which represents the stimulus, gets a new value
        # ("random_signal_intensity")
        while i < len(self.indices[0]):
            self.inverse_stim_matrix[self.indices_x[i],
                                     self.indices_y[i], 0] = random_signal_intensity
            self.inverse_stim_matrix[self.indices_x[i],
                                     self.indices_y[i], 1] = random_signal_intensity
            self.inverse_stim_matrix[self.indices_x[i],
                                     self.indices_y[i], 2] = random_signal_intensity
            i = i + 1

        # add Matrix with signal ("inverse_stim_matrix") to the Matrix with the noise
        # (wich is created by the function "build_matrix_without_signal()")
        noise_signal_matrix = (
            self.build_matrix_without_signal()) + self.inverse_stim_matrix

        return noise_signal_matrix

    def build_matrix_without_signal(self):
        '''
        this function has no input

        this function creates a random, gausian distributed, gray noise-image

        this function returns an Image-type
        '''




        # creates an empty noise_matrix with "depth" 3
        noise_matrix_3d = np.zeros(
            (self.pixelwidth, self.pixelwidth, 3), dtype=np.uint8)

        # put all the values from "noise_matrix" into each level of "noise_matrix_3d";
        # if each level is the same, you get a gray noise (from white over
        # gray to black)
        
        if self.variables.signal_colour == "Schwarz Weiss":        
            # initialize a random, gausian distributed noise_matrix
            noise_matrix = np.random.normal(
                self.variables.mean_noise, self.variables.standard_deviation_noise, [
                    self.pixelwidth, self.pixelwidth])
                
            noise_matrix_3d[:, :, 0] = noise_matrix[:, :]
            noise_matrix_3d[:, :, 1] = noise_matrix[:, :]
            noise_matrix_3d[:, :, 2] = noise_matrix[:, :]
            
        if self.variables.signal_colour == "Bunt": 
            
            noise_matrix = np.random.normal(
                self.variables.mean_noise, self.variables.standard_deviation_noise, [
                    self.pixelwidth, self.pixelwidth, 3])
                
            noise_matrix_3d[:, :, 0] = noise_matrix[:, :,0]
            noise_matrix_3d[:, :, 1] = noise_matrix[:, :,1]
            noise_matrix_3d[:, :, 2] = noise_matrix[:, :,2]
                

#
#        

        
        return noise_matrix_3d
