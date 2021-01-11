# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 20:26:02 2021

@author: User
"""
import glob, pylab, pandas as pd
import pydicom, numpy as np
from os import listdir
from os.path import isfile, join
import cv2 as cv

import matplotlib.pylab as plt
import os
import seaborn as sns
from medpy.io import save,load
#import SimpleITK as sitk

from itk import itkElastixRegistrationMethodPython
import itk
#from itkwidgets import compare, checkerboard
import numpy as np
import pyelastix


base_path = 'C:/Users/User/Desktop/SNUH PETCT Registration/snuh'


images_path = base_path + '/origin/'
folder_name = listdir(images_path)


for i in range(0, len(folder_name)):
    study_num = listdir(images_path + folder_name[i]) #folder_name loop

    #CT_images_list = [s for s in listdir(images_path + folder_name[i] + '/' + study_num[0]) if isfile(join(images_path + folder_name[i] + '/' + study_num[0], s))]
    PET_images_list = [s for s in listdir(images_path + folder_name[i] + '/' + study_num[1]) if isfile(join(images_path + folder_name[i] + '/' + study_num[1], s))]


    #print('The Number of Registration CT images', len(CT_images_list))
    print('The Number of Registration PET images', len(PET_images_list))


    #vol_CT = []

    #img, CT_header = load(images_path + folder_name[i] + '/' + study_num[0] + '/' + CT_images_list[0])
    #for idx_c in range(0, len(CT_images_list)):
     #   print(idx_c)
      #  CT_dcm = pydicom.dcmread(images_path + folder_name[i] + '/' + study_num[0] + '/' + CT_images_list[idx_c])
      #  vol_CT.append(CT_dcm.pixel_array)

      #  np_vol_CT = np.array(vol_CT, dtype=np.float32)

    

    dcm_p = pydicom.dcmread(images_path + folder_name[i] + '/' + study_num[1] + '/' + PET_images_list[50])
    
    
    reg_images_path = base_path + '/regist/'
    reg_folder = listdir(reg_images_path)
    reg_num = listdir(reg_images_path + reg_folder[i]) 
    reg_images_list = [s for s in listdir(reg_images_path + reg_folder[i] + '/' + reg_num[0]) if isfile(join(reg_images_path + reg_folder[i] + '/' + reg_num[0], s))]
    
    for idx in range(0, len(reg_images_list)):
        dcm_reg = pydicom.dcmread(reg_images_path + reg_folder[i] + '/' + reg_num[0] + '/' + reg_images_list[idx])
        
        dcm_reg.Modality = 'PT'                    #modality
        dcm_reg[0x0010, 0x0020] = dcm_p[0x0010, 0x0020]    #Patient ID
        dcm_reg[0x0010, 0x1030] = dcm_p[0x0010, 0x1030]    #Patient's weight
        
  
        pet_dose = dcm_p[0x0054, 0x0016]
        
        pet_dose[0][0x0018, 0x1074]
        
        dcm_reg.add_new([0x0018, 0x1074],'DS', pet_dose[0].RadionuclideTotalDose) #Radiomuclide total dose
        dcm_reg[0x0054, 0x1322] = dcm_p[0x0054, 0x1322]                           # Dose calibration factor
        dcm_reg.add_new([0x0018, 0x1075],'DS', pet_dose[0].RadionuclideHalfLife)  # Radionuclide half life
        dcm_reg[0x0008, 0x0030] = dcm_p[0x0008, 0x0030]    # Study Time 
        dcm_reg[0x0008, 0x0031] = dcm_p[0x0008, 0x0031]    # Series Time
        dcm_reg[0x0008, 0x0032] = dcm_p[0x0008, 0x0032]    # Acquisition Time
        dcm_reg[0x0008, 0x0033] = dcm_p[0x0008, 0x0033]    # Content Time
        dcm_reg.add_new([0x0018, 0x1072],'DS', pet_dose[0].RadiopharmaceuticalStartTime) # Radiopharmaceutical Start time 
        
        #https://github.com/ivoflipse/pydicom/blob/master/source/generate_dict/dict_2011.csv
        
        savedir = os.path.join(base_path + '/regist_header')
        if not(os.path.exists(savedir)):
            os.mkdir(savedir)
        savedir2 = os.path.join(savedir + '/' + str(reg_folder[i]))
        if not(os.path.exists(savedir2)):
            os.mkdir(savedir2)
        
        dcm_reg.save_as(savedir2 + '/' + str(idx + 1) + '_header.dcm')
        print(idx)
        
        


'''
(0054,0016) SQ                                                   # 0, 0 egg
      (0018,0031) LO Fluorodeoxyglucose                                # 1, 18 Radiopharmaceutical
      (0018,1072) TM 143500.000000                                     # 1, 14 Radiopharmaceutical Start Time
      (0018,1074) DS 340400000                                         # 1, 10 Radionuclide Total Dose
      (0018,1075) DS 6586.2                                            # 1, 6 Radionuclide Half Life
      (0018,1076) DS 0.9673                                            # 1, 6 Radionuclide Positron Fraction
      (0054,0300) SQ                                                   # 0, 0 Radionuclide Code Sequence
      (0054,0304) SQ                                                   # 0, 0 Radiopharmaceutical Code Sequence






(0010,1030) DS 70                                                # 1, 2 Patient's Weight
  (0018,1074) DS 358900000                                         # 1, 10 Radionuclide Total Dose
(0054,1322) DS 30050300                                          # 1, 8 Dose Calibration Factor
      (0018,1075) DS 6586.2                                            # 1, 6 Radionuclide Half Life
      
(0008,0030) TM 110343.682000                                     # 1, 14 Study Time
(0008,0031) TM 110911.000000                                     # 1, 14 Series Time
(0008,0032) TM 110911.000000                                     # 1, 14 Acquisition Time
(0008,0033) TM 111819.768000                                     # 1, 14 Content Time
      (0018,1072) TM 095146.000000                                     # 1, 14 Radiopharmaceutical Start Time
(0008, 0060) Modality는 PT 로 변경 필요








from PIL import Image
import numpy as np
import pydicom

ds = pydicom.dcmread('C:\\Users\\User\\Desktop\\test\\1.dcm') # pre-existing dicom file
#im_frame = Image.open('0015_result.png') # the PNG file to be replace

    # RGBA (4x8-bit pixels, true colour with transparency mask)
#np_frame = np.array(moving_img_deformed.getdata(), dtype=np.uint8)[200,:,:]
ds.Rows = CT_dcm.Rows
ds.Columns = CT_dcm.Columns
ds.PhotometricInterpretation = dcm_p.PhotometricInterpretation
ds.SamplesPerPixel = dcm_p.SamplesPerPixel
ds.BitsStored = dcm_p.BitsStored
ds.BitsAllocated = dcm_p.BitsAllocated
ds.HighBit = dcm_p.HighBit
ds.PixelRepresentation = dcm_p.PixelRepresentation
ds.PixelData = moving_img_deformed.tobytes()
ds.save_as('C:\\Users\\User\\Desktop\\test\\1_reg.dcm')


'''