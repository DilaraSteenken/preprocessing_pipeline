####################### normalise with suvr ##############
import os
import ants
import numpy as np
import pandas as pd
import re
import openpyxl as xl
import nibabel as nib
from nilearn import image, plotting
from matplotlib import pyplot as plt

#######################################################################################################################
## define folders
main_folder = r'/home/user/dsteenken/data16/Dsteenken/Rats_Database/' # replace with your directory
# these should be the same if in bids format
sub_folder = 'raw' # where raw data is
sub_folder_derivatives = 'derivatives' # where the preprocessed data and the other infos are going to be
sub_folder_preproc = 'preproc' # preprocessed data is saved
## load data table
df = pd.read_excel(os.path.join(main_folder, 'mediso_data_summary.xlsx')) # load your data table with your name

## loop through data table
for idx, row in df.iterrows():

    project = row['project']  # project name
    session = row['session']  # session
    tracer = row['tracer']  # tracer
    subject = row['subject']  # # subject name
    filename_pet = row['filename_pet']  # data file name

    # define the name of the atlas registered image
    atlas_reg_filename = re.sub('rec-stat', 'sch-rigid-reg_crop_temp-reg_rec-stat', filename_pet, flags=re.IGNORECASE)
    print(atlas_reg_filename)
    # load the atlas registered image
    atlas_reg_img = nib.load(os.path.join(main_folder, sub_folder_derivatives, sub_folder_preproc, project, subject, session, 'pet', atlas_reg_filename))

    atlas_reg_affine = atlas_reg_img.affine # get the affine
    smoothed_img = image.smooth_img(atlas_reg_img, 0.4) # smooth the image with fwhm 0.4

    output_dir = os.path.join(main_folder, sub_folder_derivatives, sub_folder_preproc, project, subject, session, 'pet') # define the output dir
    smoothed_img_filename = re.sub('rec-stat', 'gau_sch-rigid-reg_crop_temp-reg_rec-stat', filename_pet, flags=re.IGNORECASE) # create a name for the smoothed file
    output_file = os.path.join(output_dir, smoothed_img_filename) # combine output dir and file name
    print(output_file) # print the  directory and the file name

    smoothed_img.to_filename(output_file) # write the smoothed image to the output file name

    # display the images
    if os.path.exists(output_file): # if the smoothed image exist
        pet_img = nib.load(output_file)  # load the registered pet image
        # visualise pet
        plotting.plot_anat(pet_img, title=f'{smoothed_img_filename}', display_mode='ortho', cut_coords=None, annotate=True, draw_cross=False, cmap='jet')
        plt.show()
    else:
        print(f'{output_file} not found, skipping')