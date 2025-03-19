# bc1d5164 • 004 • refine_coder

---
```python
"""
Identifies the largest connected region of non-white pixels, extracts it, removes internal white pixels,
and changes any magenta pixel to the primary color of the object.
"""

import numpy as np
from scipy.ndimage import label, find_objects

def find_largest_object(grid):
    # Find the largest non-white, non-border object
    non_white_mask = grid != 0
    labeled_array, num_features = label(non_white_mask)
    
    # Find bounding box of the entire grid to identify border
    height, width = grid.shape
    border_pixels = set()
    
    # Add top and bottom border pixels
    for col in range(width):
        border_pixels.add((0,col))
        border_pixels.add((height-1, col))
    
    # add left and right border pixels
    for row in range(height):
        border_pixels.add((row, 0))
        border_pixels.add((row, width -1))
    
    # Get labels of border pixels, to exclude them later
    border_labels = set()
    for r, c in border_pixels:
        if labeled_array[r,c] != 0:
            border_labels.add(labeled_array[r,c])
            
    # Exclude border objects
    object_sizes = []
    for i in range(1, num_features + 1):
        if i not in border_labels:
           object_sizes.append(np.sum(labeled_array == i))
        else:
            object_sizes.append(0) # treat border labels as size 0
    
    # find largest non-border object
    if object_sizes:
      largest_object_label = np.argmax(object_sizes) + 1
    else:
       return None, None

    object_mask = labeled_array == largest_object_label
    
    return object_mask, labeled_array

def get_primary_color(grid, mask):
    # Get the most frequent color within the object's mask
    masked_pixels = grid[mask]
    unique_colors, counts = np.unique(masked_pixels, return_counts=True)
    primary_color = unique_colors[np.argmax(counts)]
    return primary_color

def fill_internal_white_pixels(grid, mask):
     # Fill internal white pixels in a boolean mask
    filled_mask = np.copy(mask)
    
    # Invert the mask to label the outside background
    background_mask = ~filled_mask
    labeled_background, num_backgrounds = label(background_mask)
    
    # find background label
    background_label = 0 # initialize
    for label_val in np.unique(labeled_background):
        if label_val != 0:
            if np.any(labeled_background[0,:] == label_val) or \
               np.any(labeled_background[-1,:] == label_val) or \
               np.any(labeled_background[:,0] == label_val) or \
               np.any(labeled_background[:,-1] == label_val):
                background_label = label_val
                break

    # remove the background to isolate inner white pixels
    filled_mask[labeled_background == background_label] = True
        
    return filled_mask

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the largest object and its mask
    object_mask, labeled_array = find_largest_object(input_grid)
    
    if object_mask is None:
      return input_grid.tolist() # nothing to do

    # Get the primary color of the object
    primary_color = get_primary_color(input_grid, object_mask)

    # Fill internal white pixels using the mask
    filled_mask = fill_internal_white_pixels(input_grid, object_mask)

    # Create output grid based on filled mask and primary color
    output_grid = np.zeros_like(input_grid)
    output_grid[filled_mask] = primary_color
    
    # recolor magenta to primary if needed (example 2)
    if np.any(input_grid[object_mask] == 6): # magenta
        output_grid[output_grid==6] = primary_color

    return output_grid.tolist()
```
