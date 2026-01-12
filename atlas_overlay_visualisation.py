####################################################### overlay images with the atlas ####################################
# load packages
import numpy as np, nibabel as nib
from nilearn.input_data import NiftiLabelsMasker
from nilearn import image
from nilearn import image, plotting
import pandas as pd
import os
import re
import matplotlib.pyplot as plt

##########################################################################################################################
## define folders
main_folder = r'/home/user/dsteenken/data16/Dsteenken/Rats_Database/' # replace with your directory
# these should be the same if in bids format
sub_folder = 'raw' # where raw data is
sub_folder_derivatives = 'derivatives' # where the preprocessed data and the other infos are going to be
sub_folder_preproc = 'preproc' # preprocessed data is saved
# load data table
df = pd.read_excel(os.path.join(main_folder, 'mediso_data_summary.xlsx')) # load your data table with your name
# load schiffer rat atlas
atlas = image.load_img(r"/home/user/dsteenken/data16/Dsteenken/Rats_Database/derivatives/atlases/Rat_W.Schiffer/Px_Rat_W.Schiffer.nii.gz")

## loop through data table
for idx, row in df.iterrows():
    project = row['project'] # loop through project names
    session = row['session'] # loop through sessions
    subject = row['subject'] # subject
    filename_pet = row['filename_pet'] # file name

    img_to_overlay_filename = re.sub('rec-stat', 'gau_sch-rigid-reg_crop_temp-reg_rec-stat', filename_pet, flags=re.IGNORECASE) # rename the file to get the smoothed and normalised image
    img_to_overlay = os.path.join(main_folder, sub_folder_derivatives, sub_folder_preproc, project, subject, session, 'pet', img_to_overlay_filename) # join the dir for the image
    print(f'image to overlay: {img_to_overlay}') # print name

    if os.path.exists(img_to_overlay): # if the image exist
        fig_dir = os.path.join(main_folder, sub_folder_derivatives, sub_folder_preproc, project, subject, session, 'figure') # create a directory for figures
        os.makedirs(fig_dir, exist_ok=True) # make the directory
        out_png = re.sub('rec-stat_pet.nii.gz', 'atlas-overlay_gau_sch-reg_crop_temp-reg_rec-stat.png', filename_pet, flags=re.IGNORECASE) # name the pgn files
        fig_dir_file = os.path.join(fig_dir, out_png) # combine directory with png file names

        # create the figure
        roi3d = image.index_img(atlas, 0) # index axis 0
        display = plotting.plot_anat(img_to_overlay, cut_coords= (4, 0, -2), display_mode='ortho', draw_cross=False, annotate=True, cmap='jet', title=f'{out_png}') # plot image
        display.add_contours(roi3d, levels=[0.5], linewidths=2.0, colors='red')  # add contours of ROI
        plt.show() # show the figure
        display.savefig(fig_dir_file)  # save the image
        print("Multi-view figure saved to:", f'{fig_dir_file}') # print where the image is saved to
    else:
        print(f'image to parcellate: {img_to_overlay} not found')