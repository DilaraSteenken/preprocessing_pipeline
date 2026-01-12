############################################## create an average template based on baseline images #############################################
import os
import ants
import numpy as np
import pandas as pd
import re
import openpyxl as xl
import nibabel as nib
from nilearn import image, plotting
from matplotlib import pyplot as plt

##################################################################################################################################################
## define folders
main_folder = r'/home/user/dsteenken/data16/Dsteenken/Rats_Database/' # replace with your directory
# these should be the same if in bids format
sub_folder = 'raw' # where raw data is
sub_folder_derivatives = 'derivatives' # where the preprocessed data and the other infos are going to be
sub_folder_preproc = 'preproc' # preprocessed data is saved
# load data table
df = pd.read_excel(os.path.join(main_folder, 'mediso_data_summary.xlsx')) # load your data table with your name
# define atlas
atlas_img = r"/home/user/dsteenken/data16/Dsteenken/Rats_Database/derivatives/atlases/Rat_W.Schiffer/normalization/Rat_W.Schiffer_FDG.nii.gz"

## loop through data table
for idx, row in df.iterrows():

    project = row['project']  # project name
    session = row['session']  # session
    tracer = row['tracer']  # tracer
    subject = row['subject']  # # subject name
    filename_pet = row['filename_pet']  # data file name

    cropped_img_filename = re.sub('rec-stat', 'crop_temp-reg_rec-stat', filename_pet, flags=re.IGNORECASE) # define the cropped image name
    cropped_img = os.path.join(main_folder, sub_folder_derivatives, sub_folder_preproc, project, subject, session, 'pet', cropped_img_filename) # combine directory with file name
    print(f'cropped image: {cropped_img}') # print name

    if os.path.exists(cropped_img): # if cropped image exist
        try: # try to load and register the pet image to the atlas
            fixed = ants.image_read(atlas_img) # atlas is the fixed image
            moving = ants.image_read(cropped_img) # the cropped image is moving into atlas space

            # create the output folder for the registered image to be saved
            output_dir = os.path.join(main_folder, sub_folder_derivatives, sub_folder_preproc, project, subject, session, 'pet') # define directory name
            os.makedirs(output_dir, exist_ok=True) # create actual directory

            # name for the registered image
            atlas_reg_img = re.sub('rec-stat', 'sch-rigid-reg_crop_temp-reg_rec-stat', filename_pet, flags=re.IGNORECASE) # create a name for the atlas registered image
            output_file = os.path.join(output_dir, atlas_reg_img) # combine directory and file name

            # register the moving image to the fixed image
            reg = ants.registration(fixed=fixed, moving=moving, type_of_transform='Rigid') # register pet image to the atlas
            ants.image_write(reg['warpedmovout'], filename=output_file) # move out the registered image and save
            print(f'Registered {atlas_reg_img}') # print atlas reg image

            # display the images
            if os.path.exists(output_file):
                pet_img = nib.load(output_file)  # load the registered pet image
                # visualise pet
                plotting.plot_anat(pet_img, title=f'{atlas_reg_img}', display_mode='ortho', cut_coords=None, annotate=True, draw_cross=False, cmap='jet')
                plt.show()
            else: # if no registered image exist
                print(f"No file: {output_file}")
        except Exception as e: # if error during registration or image loading
            print(e)
    else: # if no cropped image exist
        print(f'No image {cropped_img}')