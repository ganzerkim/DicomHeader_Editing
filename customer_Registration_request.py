# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 10:50:20 2021

@author: Mingeon Kim (Siemens-healthineers)
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


base_path = 'C:/Users/User/Desktop/snuh'


images_path = base_path + '/origin/'
folder_name = listdir(images_path)

i=0
study_num = listdir(images_path + folder_name[i]) #folder_name loop

CT_images_list = [s for s in listdir(images_path + folder_name[i] + '/' + study_num[0]) if isfile(join(images_path + folder_name[i] + '/' + study_num[0], s))]
PET_images_list = [s for s in listdir(images_path + folder_name[i] + '/' + study_num[1]) if isfile(join(images_path + folder_name[i] + '/' + study_num[1], s))]


print('The Number of Registration CT images', len(CT_images_list))
print('The Number of Registration PET images', len(PET_images_list))


vol_CT = []

img, CT_header = load(images_path + folder_name[i] + '/' + study_num[0] + '/' + CT_images_list[0])
for idx_c in range(0, len(CT_images_list)):
    print(idx_c)
    CT_dcm = pydicom.dcmread(images_path + folder_name[i] + '/' + study_num[0] + '/' + CT_images_list[idx_c])
    vol_CT.append(CT_dcm.pixel_array)

np_vol_CT = np.array(vol_CT, dtype=np.float32)



vol_PET = []

img, PET_header = load(images_path + folder_name[i] + '/' + study_num[1] + '/' + PET_images_list[0])
for idx_p in range(0, len(PET_images_list)):
    print(idx_p)
    dcm_p = pydicom.dcmread(images_path + folder_name[i] + '/' + study_num[1] + '/' + PET_images_list[idx_p])
    vol_PET.append(dcm_p.pixel_array)

np_vol_PET = np.array(vol_PET, dtype=np.float32)







import skimage.transform
re_PET_img = skimage.transform.resize(np_vol_PET, (551,512,512), order=0)


fixed_img = np_vol_CT
moving_img = re_PET_img

params = pyelastix.get_default_params(type='RIGID')
#params.MaximumNumberOfIterations = 200
#params.FinalGridSpacingInVoxels = 10
params.AutomaticTransformInitialization = True
# Apply the registration (im1 and im2 can be 2D or 3D)
moving_img_deformed, field = pyelastix.register(moving_img, fixed_img, params, exact_params = False, verbose = 1)



from medpy.filter import otsu
threshold = otsu(moving_img_deformed)
output_data = moving_img_deformed > threshold
PET_header.get_voxel_spacing = [0.5, 0.5, 0.5]
PET_header.get_offset = [0.0, 0.0, 0.0]
save(moving_img_deformed,'C:\\Users\\User\\Desktop\\test\\regg.dcm', PET_header) 


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



scipy.ndimage.zoom(ArrayDicomPET, (960/256, 960/256, 960/159), order=1)



from pydicom import dcmread

ds = dcmread("C:\\Users\\User\\Desktop\\test\\1.dcm")
# Edit the (0010,0020) 'Patient ID' element
ds.PatientID = dcm_p.PatientID
ds.pixel_array = moving_img_deformed
ds.PixelData = moving_img_deformed.tobytes()
ds.save_as("C:\\Users\\User\\Desktop\\test\\1_reg.dcm")























# Load images with itk floats (itk.F). Necessary for elastix
#fixed_image = itk.imread('data/CT_2D_head_fixed.mha', itk.F)
#moving_image = itk.imread('data/CT_2D_head_moving.mha', itk.F)
fixed_image = np_vol_CT
moving_image = np_vol_PET

parameter_object = itk.ParameterObject.New()
default_rigid_parameter_map = parameter_object.GetDefaultParameterMap('rigid')
parameter_object.AddParameterMap(default_rigid_parameter_map)

registered_image, params = itk.elastix_registration_method(fixed_image, moving_image, True)

# Call registration function
result_image, result_transform_parameters = itk.elastix_registration_method(
    fixed_image, moving_image,
    parameter_object=parameter_object,
    log_to_console=True)
#%%
'''
elastixImageFilter = sitk.ElastixImageFilter()
elastixImageFilter.SetFixedImage(sitk.ReadImage("fixedImage.nii"))
elastixImageFilter.SetMovingImage(sitk.ReadImage("movingImage.nii"))
elastixImageFilter.SetParameterMap(sitk.GetDefaultParameterMap("rigid"))
elastixImageFilter.Execute()
sitk.WriteImage(elastixImageFilter.GetResultImage())
'''



#%%
'''
CT_images_path = base_path + '/origin/PET2CT_4/'
folder_name = listdir(CT_images_path)
CT_images_list = [s for s in listdir(CT_images_path + folder_name[0]) if isfile(join(CT_images_path + folder_name[0], s))]
'''