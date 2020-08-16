# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 17:14:48 2020

@author: zll
"""

import os
import numpy as np
from torch import tensor
from torch.utils import data
from patch_extracting import get_imarr, extract


class CHACEDB_dataset(data.Dataset):
    def __init__(self, train=True, online=True):
        '''
        when oline set True, it will extract patch from preprocessed images, \
        instead of read patch file.
        '''
        self.train = train
        self.online = online
        if train:  # load the training set
            img_path = '../data/CHASEDB/train/'
            label_path = '../data/CHASEDB/train/'
        else:      # load the test set
            img_path = '../data/CHASEDB/test/'
            label_path = '../dataCHASEDB/test/'

        if online:
            img_path += 'proc_imgs/'
            label_path += 'label/'
            # get file name from image path
            img_files = os.listdir(img_path)
            # get file name from truth path
            truth_files = os.listdir(label_path)

            # sort the file name list
            img_files.sort()
            truth_files.sort()

            # combine image path with file names
            img_files = [img_path + f for f in img_files]
            truth_files = [label_path + f for f in truth_files]

            # get array
            img_array = get_imarr(img_files)
            truth_array = get_imarr(truth_files)
            # extract patchs
            self.img = extract(img_array, (128, 128), 21, False)
            self.label = extract(truth_array, (128, 128), 21, True)
        else:
            # load
            self.img = np.load(img_path+'imgs.npy')
            self.label = np.load(label_path+'truth.npy')

        self.len = self.img.shape[0]  # length of the data set
        # transfer to 4-D
        new_shape = (self.img.shape[0], 1, self.img.shape[1],
                     self.img.shape[2])
        self.img = np.reshape(self.img, new_shape)
        self.label = np.reshape(self.label, new_shape)
        # transfer to tensor
        self.img = tensor(self.img)
        self.label = tensor(self.label)

    def __len__(self):
        return self.len

    def __getitem__(self, index):  # get one item
        img = self.img[index]
        label = self.label[index]
        return img, label

    def get_img(self):
        '''
        return all images
        '''
        return self.img

    def get_label(self):
        '''
        return all labels
        '''
        return self.label
