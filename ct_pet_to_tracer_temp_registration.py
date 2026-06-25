########################################## register ct registered pet images to the averaged template #######################################################
# import packages
import numpy as np
import ants
import os
import warnings
import openpyxl as xl
import re
import pandas as pd
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

# templates for each ucbh (46 images) and fdg (101 images) were created and they are used as fixed image to be registered so that they are in the same space for cropping
fixed_ucbh_img = r'/home/user/dsteenken/data16/Dsteenken/Rats_Database/derivatives/templates/baseline_ucbh_template.nii.gz' # ucbh template
print(f'Fixed {fixed_ucbh_img}') # can comment out
fixed_fdg_img = r'/home/user/dsteenken/data16/Dsteenken/Rats_Database/derivatives/templates/baseline_fdg_template.nii.gz' # fdg template
print(f'Fixed {fixed_fdg_img}') # can comment out

# if you have the data table and all the info in it, you can loop through the table
for idx, row in df.iterrows(): # iterates over rows

    project = row['project'] # project name
    session = row['session'] # session
    tracer = row['tracer'] # tracer
    subject = row['subject'] # # subject name
    filename_pet = row['filename_pet'] # data file name
    pet = row['pet'] # if pet exists 1, no 0
    ct = row['ct'] # if ct exist 1, not 0
    fixed_img = None # need to give the fixed image variable

    if tracer == 'fdg': # if tracer fdg defines the fdg template, # if only 1 tracer do not worry it will just do it for the existing one
        fixed_img = fixed_fdg_img
    elif tracer == 'ucbh': # if tracer ucbh defines the ucbh template
        fixed_img = fixed_ucbh_img

    if pet == 1 and ct == 1: # if both pet and ct exist load the images
        ct_reg_filename = re.sub('rec-stat', 'ct-reg_rec-stat', filename_pet, flags=re.IGNORECASE) # defines the pet to ct registered file name
        moving_img = os.path.join(main_folder, sub_folder_derivatives, sub_folder_preproc, project, subject, session, 'pet', ct_reg_filename) # the ct registered pet image is moving, so defining the working directory
        print(f'Moving {moving_img}') # print the name
    elif pet == 1 and ct == 0: # if only pet image is available, take that and directly register it to the average template
        moving_img = os.path.join(main_folder, sub_folder, project, subject, session, 'pet', filename_pet) # the original pet image is moving
        print(f'Moving {moving_img}')

    else: # if only ct or both ct and pet do not exist, them no image to register
        moving_img = None
        print(f'{moving_img} does not exist')

    if os.path.exists(fixed_img) and os.path.exists(moving_img): # check if both images exist
        try: # try to load the images and register, if not it will give an error but continue with the next image
            fixed = ants.image_read(fixed_img) # load the template as fixed image
            moving = ants.image_read(moving_img) # load the moving image

            # create the output folder for the registered image to be saved
            output_dir = os.path.join(main_folder, sub_folder_derivatives, sub_folder_preproc, project, subject, session, 'pet') # create a name
            os.makedirs(output_dir, exist_ok=True) # create the actual folder

            # name for the registered image
            temp_reg_filename = re.sub('rec-stat', 'temp-reg_rec-stat', filename_pet, flags=re.IGNORECASE) # replace the raw data name with the registered name
            output_file = os.path.join(output_dir, temp_reg_filename) # define the working directory with the file name

            # register the moving image to the fixed image
            reg = ants.registration(fixed=fixed, moving=moving, type_of_transform='Rigid') # register
            ants.image_write(reg['warpedmovout'], filename=output_file) # get the registered image and save it
            print(f'Registered {temp_reg_filename}') # print name

            # display the images
            if os.path.exists(output_file): # if the registered image exists

                pet_img = nib.load(output_file)  # load the registered pet image
                plotting.plot_anat(pet_img, title=f'{temp_reg_filename}', display_mode='ortho', cut_coords=None, annotate=True, draw_cross=False)
                plt.show()

            else: # if not
                print(f"No file: {output_file}")

        except Exception as e: # if an error occurred during registration
                print(e)

    else:
        print(f'{fixed_img} or {moving_img} not found') # if images are not found
