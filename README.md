# rat preprocessing_pipeline
preprocess images in the following order:
1- bids conversion
2- pet_to_ct_registration
3- ct_pet_to_avg_img_registration
4- brain_cropping
5- atlas_registration
6- gaussian_filter
7- atlas_overlay_visualisation
8- suvr
9- parcellation

!! Only run the tracer specific template creation script if you want to create a template. 
!! if emission/transmiion PET scanner. First mask the second animals out, rotate the animal at the top, so that always only one animal in each nii file and create a separate study-specific tracer template as no teeth holder was used at the time. (They do not align with the PET/CT scanner template). For this purpose, run the split_door_animal.py script and then rotate_door_animal.py script, before atlas registration, check image origins if different, run set origin and then run atlas registration. 
