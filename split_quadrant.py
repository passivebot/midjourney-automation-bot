import os
import cv2 
import numpy as np 
import glob

# Loop through every file ending with .png in the file.
for filename in glob.glob('*.png'): 
    # Print the image name.
    print(filename)
    
    # Load the image.
    img = cv2.imread(filename)
    
    # Split the image into four equal parts.
    h, w, c = img.shape
    quad1 = img[0:h//2, 0:w//2]
    quad2 = img[0:h//2, w//2:w]
    quad3 = img[h//2:h, 0:w//2]
    quad4 = img[h//2:h, w//2:w]
    
    # Create filenames for each quadrant.
    name_quad1 = filename[:-4] + '_quad1.png'
    name_quad2 = filename[:-4] + '_quad2.png'
    name_quad3 = filename[:-4] + '_quad3.png'
    name_quad4 = filename[:-4] + '_quad4.png'
    
    # Create a new folder with the same name as the original image.
    os.mkdir(filename[:-4])
    
    # Save the four images in the newly created folder.
    cv2.imwrite(os.path.join(filename[:-4], name_quad1), quad1)
    cv2.imwrite(os.path.join(filename[:-4], name_quad2), quad2)
    cv2.imwrite(os.path.join(filename[:-4], name_quad3), quad3)
    cv2.imwrite(os.path.join(filename[:-4], name_quad4), quad4)


    # Delete the original image.
    os.remove(filename)
    