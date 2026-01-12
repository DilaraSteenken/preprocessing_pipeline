############################################ brain parcellation ############################################
# load packages
import numpy as np, nibabel as nib
from nilearn.input_data import NiftiLabelsMasker
from nilearn import image
from nilearn import image, plotting
import pandas as pd
import os
import re

##################################################################################################################################################
## define folders
main_folder = r'/home/user/dsteenken/data16/Dsteenken/Rats_Database/' # replace with your directory
# these should be the same if in bids format
sub_folder = 'raw' # where raw data is
sub_folder_derivatives = 'derivatives' # where the preprocessed data and the other infos are going to be
sub_folder_preproc = 'preproc' # preprocessed data is saved
df = pd.read_excel(os.path.join(main_folder, 'mediso_data_summary.xlsx')) # load your data table with your name
atlas = image.load_img(r"/home/user/dsteenken/data16/Dsteenken/Rats_Database/derivatives/atlases/Rat_W.Schiffer/Px_Rat_W.Schiffer.nii.gz") # load schiffer rat atlas
atlas_data = atlas.get_fdata() # get the data
labels = np.unique(atlas_data) # get the unique labels for each region
print(labels) # print labels

# load text file with the regions to label later
atlas_txt = r"/home/user/dsteenken/data16/Dsteenken/Rats_Database/derivatives/atlases/Rat_W.Schiffer/Px_Rat_W.Schiffer.txt"
# t -> tab separated, no header row
lut = pd.read_csv(atlas_txt, sep="\t", header=None, names=["label_full", "label_short", "id", "color", "description"])
lut["id"] = lut["id"].astype(int) # have the ids as int

## loop through data table
for idx, row in df.iterrows():
    project = row['project'] # loop through project names
    session = row['session'] # loop through sessions
    subject = row['subject'] # each subject
    filename_pet = row['filename_pet'] # each filename
    img_to_parcellate_filename = re.sub('rec-stat', 'suvr_gau_sch-rigid-reg_crop_temp-reg_rec-stat', filename_pet, flags=re.IGNORECASE) # rename the file to get the smoothed and normalised image
    img_to_parcellate = os.path.join(main_folder, sub_folder_derivatives, sub_folder_preproc, project, subject, session, 'pet', img_to_parcellate_filename) # join the dir for the image
    print(f'image to parcellate: {img_to_parcellate}') # print name
    if os.path.exists(img_to_parcellate): # if image exist
        try: # try to fit the atlas
            # fit the atlas on the image
            masker = NiftiLabelsMasker(labels_img=atlas, standardize=False)
            X = masker.fit_transform(img_to_parcellate)
            print(X.shape)

            # Save CSV
            mean_values = X[0, :]  # flatten the shape
            roi_means = pd.DataFrame({"id": np.arange(1, len(mean_values) + 1), "mean_value": mean_values}) # to start with 1 add 1
            results = roi_means.merge(lut, on="id") # merge the mean values and the roi ids
            csv_dir = os.path.join(main_folder, sub_folder_derivatives, sub_folder_preproc, project, subject, session, 'stat') # where to save the csv
            os.makedirs(csv_dir, exist_ok=True) # create the directory
            csv_filename = re.sub('rec-stat_pet.nii.gz', 'parc_suvr_gau_sch-rigid-reg_crop_temp-reg_rec-stat.csv', filename_pet, flags=re.IGNORECASE) # define a filename
            csv_dir_file = os.path.join(csv_dir, csv_filename) # combine new filename with directory
            print(csv_dir_file) # print name
            results.to_csv(csv_dir_file, index=False) # save the csv

        except Exception as e: # if something went wrong print e
            print(e)
    else: # if no image found
        print(f'image to parcellate: {img_to_parcellate} not found')