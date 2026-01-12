###################### crop the brain ##############################
# import packages
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ants
import os
import warnings
import openpyxl as xl
import re
import nibabel as nib
from nilearn import plotting
import matplotlib.pyplot as plt

#######################################################################################################################
## define folders
main_folder = r'/home/user/dsteenken/data16/Dsteenken/Rats_Database/' # replace with your directory
# these should be the same if in bids format
sub_folder = 'raw' # where raw data is
sub_folder_derivatives = 'derivatives' # where the preprocessed data and the other infos are going to be
sub_folder_preproc = 'preproc' # preprocessed data is saved
## load data table
df = pd.read_excel(os.path.join(main_folder, 'mediso_data_summary.xlsx')) # load your data table with your name

# loop through rows
for idx, row in df.iterrows():
    project = row['project']  # project name
    session = row['session']  # session
    tracer = row['tracer']  # tracer
    subject = row['subject']  # # subject name
    filename_pet = row['filename_pet']  # data file name

    temp_reg_filename = re.sub('rec-stat', 'temp-reg_rec-stat', filename_pet, flags=re.IGNORECASE) # rename from the data table to load the template registered image
    print(temp_reg_filename) # print the name or comment out

    original_img = os.path.join(main_folder, sub_folder_derivatives, sub_folder_preproc, project, subject, session, 'pet', temp_reg_filename) # join the path for the template registered image
    print(f'original image: {original_img}') # named this as original image as it is not cropped yet

    # plot the image before cropping
    plotting.plot_anat(original_img, title=temp_reg_filename, display_mode='ortho', cut_coords=None, annotate=True, draw_cross=False, radiological=False)
    plt.show()

    # load the original image
    img = nib.load(original_img)
    data = img.get_fdata() # get the data as a matrix
    affine = img.affine # get the affine matrix
    header = img.header # get the header

    ## create mask for cropping based on the templates so that you keep the whole brain, you can arrange the 1s and the 0s based on your images, but they should fit these masks as they are registered to the same average template
    mask = np.zeros_like(data, dtype=bool) # create a mask same as the data matrix with zeros
    mask[70:150, 115:165, 50:165] = True # voxels that should be included in the mask are 1, not included 0, this is for fdg
    #mask[70:150, 115:165, 40:153] = True # this is for ucbh if you do not have ucbh leave it commented out, otherwise first crop fdg and then comment out fdg and uncomment this to crop ucbh

    cropped_img = data * mask # to create the cropped image by multiplying the data with the mask

    fig, ax = plt.subplots(1,3, figsize=(12,6)) # display the cropped image with different views
    ax[0].imshow(cropped_img[100,:,:].T, cmap='gray', origin='lower')
    ax[0].axis('off')
    ax[1].imshow(cropped_img[:, 140, :].T, cmap='gray', origin='lower')
    ax[1].axis('off')
    ax[2].imshow(cropped_img[:, :, 100].T, cmap='gray', origin='lower')
    ax[2].axis('off')
    plt.show()

    # rename the cropped image
    cropped_filename = re.sub('rec-stat', 'crop_temp-reg_rec-stat', filename_pet, flags=re.IGNORECASE) # rename
    output_dir = os.path.join(main_folder, sub_folder_derivatives, sub_folder_preproc, project, subject, session, 'pet') # define directory
    output_filename = os.path.join(output_dir, cropped_filename) # combine directory and filename
    os.makedirs(output_dir, exist_ok=True) # create an actual folder
    nib.save(nib.Nifti1Image(cropped_img, affine, header), output_filename) # save the image
    print(f"cropped image saved: {output_filename}") # print saved image
