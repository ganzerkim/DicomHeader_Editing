# -*- coding: utf-8 -*-
"""
@author: Mingeon
"""
import glob, pylab, pandas as pd

import pydicom, numpy as np
from os import listdir
from os.path import isfile, join
import cv2 as cv

import matplotlib.pylab as plt
import os

import numpy as np

import hmac
import binascii
import hashlib
import random


#%%
#Series 별 폴더 나누기.

def hash_acc(num, length, sideID):
   try:
       siteID = str.encode(sideID)
       num = str.encode(num)
                              # hash
       m = hmac.new(siteID, num, hashlib.sha256).digest()
                              #convert to dec
       m = str(int(binascii.hexlify(m),16))
                              #split till length
       m=m[:length]
       return m
   except Exception as e:
          print("Something went wrong hashing a value :(")
          return

images_path = 'D:/dicom_data/PETCT/DICOM'


path_tmp = []
name_tmp = []


for (path, dir, files) in os.walk(images_path):
    for filename in files:
        ext = os.path.splitext(filename)[-1]
        
        if ext == '.dcm' or '.IMA':
            print("%s/%s" % (path, filename))
            path_tmp.append(path)
            name_tmp.append(filename)


dcm_tmp = []
print("파일 로딩 중 입니다~ 처리 데이터 양이 많을 수록 오래 기다려주셔야 합니다 ㅠㅠ")
for i in range(len(path_tmp)):
    dcm_p = pydicom.dcmread(path_tmp[i] + '/' + name_tmp[i], force = True)
    dcm_tmp.append(dcm_p)
    
print(str(i) + "개 로딩완료!")

print("Scan 프로토콜 별로 폴더를 정리 중 입니다. 처리 데이터 양이 많을 수록 오래 기다려주셔야 됩니다.")


folder_name = sorted(listdir(images_path), key = int)

idx = 0;

savedir = os.path.join('C:/Users/User/Desktop/MI_Anonymized')
if not(os.path.exists(savedir)):
    os.mkdir(savedir)
    
for idx in range(0, len(name_tmp)):
    
    dcm_tmp = pydicom.dcmread(path_tmp[idx] + '/' +  name_tmp[idx])
    #dcm_tmp.PatientName = "777777"  # Patient Name    
    
    savedir2 = os.path.join(savedir +'/' + str(folder_name[0]) + '/' + str(dcm_tmp.AccessionNumber) + '/' + str(dcm_tmp.SeriesDescription))
    if not(os.path.exists(savedir2)):
        os.makedirs(savedir2)
        
    dcm_tmp.save_as(savedir2 + '/' + str(dcm_tmp.SeriesInstanceUID) + str(idx) + ".dcm")
    print("Total " + str(i) + " dataset 중 " + str(idx))
print("교수님~! Series별 폴더정리가 완료되었습니다. 다음 코드를 실행하여 익명화를 진행해 주세요~")   

#%% 익명화 하기

save_path = 'C:/Users/User/Desktop/MI_Anonymized/'
i = 0
temp_folder = []
folder_name = listdir(save_path)

cohort_num = []
acc_inform = []

for i in range(0, len(folder_name)):
    print(i)
    temp_folder = listdir(save_path + folder_name[i])
    
    

    
    for ac in range(0, len(temp_folder)):
        series_num = listdir(save_path + folder_name[i] + '/' + temp_folder[ac]) #folder_name loop
        
        for sr in range(0, len(series_num)):
            PET_images_list = [s for s in listdir(save_path + folder_name[i] + '/' + temp_folder[ac] + '/' + series_num[sr]) if isfile(join(save_path + folder_name[i] + '/' + temp_folder[ac] + '/' + series_num[sr], s))]
            
            temp_dcm = []
            for dd in range(0, len(PET_images_list)):
                dcm_p = pydicom.dcmread(save_path + folder_name[i] + '/' + temp_folder[ac] + '/' + series_num[sr] + '/' + PET_images_list[dd])
                temp_dcm.append(dcm_p)
                
                savedir = os.path.join('C:/Users/User/Desktop/' + 'ANONYMIZED')
                if not(os.path.exists(savedir)):
                    os.makedirs(savedir)
                
                savedir2 = os.path.join(savedir + '/' + temp_folder[ac] + '/' + series_num[sr])
                if not(os.path.exists(savedir2)):
                    os.makedirs(savedir2)
                    
                #dcm_tmp.PatientName = hash_acc(dcm_tmp.PatientID,16, "Korhospital1" ) # Patient Name
                dcm_p.PatientName = 'R-' + str(ac) # Patient Name
                dcm_p.PatientBirthDate = "777777" # Patient Birtday 
                dcm_p.PatientID = hash_acc(dcm_tmp.PatientID,16, "Korhospital") # Patient ID
                dcm_p.AccessionNumber = hash_acc(dcm_tmp.AccessionNumber,16,"Korhospital1") # Accession number 
                # dcm_p.StudyID = hash_acc(dcm_p.studyID,16,"Korhospital1") # Patient ID
                dcm_p.StudyInstanceUID = hash_acc(dcm_tmp.StudyInstanceUID,16,"Korhospital1")
                dcm_p.SeriesInstanceUID = hash_acc(dcm_tmp.SeriesInstanceUID,16,"Korhospital1")
                dcm_p.SOPInstanceUID = hash_acc(dcm_tmp.SOPInstanceUID,16,"Korhospital1")
                dcm_p.InstitutionName = hash_acc(dcm_tmp.InstitutionName,16,"Korhospital1")
                dcm_p.StudyID = hash_acc(dcm_tmp.StudyID,16,"Korhospital1")
                if "ProcedureCodeSequence" in dcm_p:
                    dcm_p.ProcedureCodeSequence[0].CodeValue = "Annoymized"
                if "OtherPatientIDsSequence" in dcm_p:
                    dcm_p.OtherPatientIDsSequence[0].PatientID = hash_acc(dcm_tmp.PatientID,16, "Korhospital")
                if "RequestedProcedureCodeSequence" in dcm_p:
                    dcm_p.RequestedProcedureCodeSequence[0].CodeValue = "Annoymized"
                if "RequestAttributesSequence" in dcm_p:
                    dcm_p.RequestAttributesSequence[0].ScheduledProcedureStepID = "Annoymized"
                    dcm_p.RequestAttributesSequence[0].RequestedProcedureID = "Annoymized"

                #RequestedProcedureCodeSequence
                #
                dcm_p.save_as(savedir2 + '/' + str(dd + 1) + ".dcm")
  
               
                
            print(sr)
        cohort_num.append('R-'+ str(ac))
        acc_inform.append(str(temp_folder[ac]))
    
annoy = {'익명화 이름': cohort_num, 'Accession Number 정보': acc_inform}
df = pd.DataFrame(annoy)

# .to_csv 
# 최초 생성 이후 mode는 append
if not os.path.exists(savedir + '/information.csv'):
    df.to_csv(savedir + '/information.csv', index=False, mode='w', encoding='utf-8-sig')
else:
    df.to_csv(savedir + '/information.csv', index=False, mode='a', encoding='utf-8-sig', header=False)

print("익명화가 완료되었습니다, Study 진행 하실 때 Excel sheet를 확인해주세요~")