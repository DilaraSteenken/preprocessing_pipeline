############################################ suvr ##########################
# load packages
import os
import ants
import numpy as np
import pandas as pd
import re
import openpyxl as xl
import nilearn
from nilearn import image
import nibabel as nib
import matplotlib.pyplot as plt
from nilearn import image, plotting

##################################################################################################################################################
## define folders
main_folder = r'/home/user/dsteenken/data16/Dsteenken/Rats_Database/' # replace with your directory
# these should be the same if in bids format
sub_folder = 'raw' # where raw data is
sub_folder_derivatives = 'derivatives' # where the preprocessed data and the other infos are going to be
sub_folder_preproc = 'preproc' # preprocessed data is saved
# load data table
df = pd.read_excel(os.path.join(main_folder, 'mediso_data_summary.xlsx')) # load your data table with your name
sch_fdg_mask = r'/home/user/dsteenken/data16/Dsteenken/Rats_Database/derivatives/atlases/Rat_W.Schiffer/normalization/Px_Rat_W.Schiffer_FDG_mask.nii.gz' # load the schiffer FDG mask

## loop through data table
for idx, row in df.iterrows():

    project = row['project'] # each project
    session = row['session'] # each session
    subject = row['subject'] # each subject
    filename_pet = row['filename_pet'] # each filename

    main_dir = os.path.join(main_folder, sub_folder_derivatives, sub_folder_preproc, project, subject, session, 'pet') # define the directory where the smoothed image is
    smoothed_img_filename = re.sub('rec-stat', 'gau_sch-rigid-reg_crop_temp-reg_rec-stat', filename_pet, flags=re.IGNORECASE) # define the name of the atlas registered smoothed image
    smoothed_img = os.path.join(main_dir, smoothed_img_filename) # combine directory and filename
    print(smoothed_img) # print name

    gau_img = ants.image_read(smoothed_img) # read the smoothed image
    mask = ants.image_read(sch_fdg_mask) # read the fdg schiffer mask
    mean_val = gau_img[mask].mean()     # Compute mean within mask

    suvr_img = gau_img / mean_val # divide the image to the mean whole brain value
    mean_suvr = suvr_img[mask].mean()  # check the mean suvr
    print(mean_suvr) # print

    if mean_suvr > 1.1:
        print(f'whole brain normalisation did not work: {smoothed_img_filename}')
        plt.hist(suvr_img[mask == 1].flatten(), bins=100)
        plt.title("SUVr distribution")
        plt.xlabel("SUVr")
        plt.ylabel("Count")
        plt.show()
    # suvr image filename
    suvr_filename = re.sub('rec-stat', 'suvr_gau_sch-rigid-reg_crop_temp-reg_rec-stat', filename_pet, flags=re.IGNORECASE) # create a filename for suv image
    suvr_output_file = os.path.join(main_dir, suvr_filename) # combine output dir with filename
    print(suvr_output_file) # print name

    ants.image_write(suvr_img, suvr_output_file) # save the normalised brain image
    print(f'suvr image written to: {suvr_output_file}') # print