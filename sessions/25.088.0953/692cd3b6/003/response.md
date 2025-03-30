```python
import numpy as np
from scipy.ndimage import label, find_objects

"""
Identify all distinct connected objects composed of non-white pixels in the input grid.
For each distinct object found:
  Calculate the minimal bounding box that encloses all pixels of this object.
  Iterate through each pixel location (row, column) within this object's bounding box.
  If the corresponding pixel in the original input grid at this location is white (0), change the corresponding pixel in the output grid to yellow (4).
  Otherwise, the pixel in the output grid retains its original color.
Pixels outside of any object's bounding box remain unchanged.
"""

def transform(input_grid):
    """
    Fills the bounding box of each non-white object with yellow (4), 
    only replacing original white (0) pixels within each box.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    
    # 1. Create a mask for non-white pixels
    # Pixels with value 0 (white) will be 0, others will be 1.
    mask = (input_np != 0).astype(int) 
    
    # 2. Find connected components (objects) in the mask
    # `labeled_array` will have a unique integer label for each object.
    # `num_labels` is the total number of objects found (excluding the background).
    # We use a structure that considers diagonal connections as well.
    structure = np.array([[1,1,1],[1,1,1],[1,1,1]]) # Connects adjacent and diagonal pixels
    labeled_array, num_labels = label(mask, structure=structure)
    
    # Handle case with no non-white pixels
    if num_labels == 0:
        return output_grid.tolist()

    # 3. Find the bounding box for each labeled object
    # `find_objects` returns a list of slice objects, where each slice defines the bounding box.
    object_slices = find_objects(labeled_array)

    # 4. Iterate through each object's bounding box
    for i in range(num_labels):
        # Get the bounding box slices for the current object (label i+1)
        obj_slice = object_slices[i] 
        min_r, max_r = obj_slice[0].start, obj_slice[0].stop
        min_c, max_c = obj_slice[1].start, obj_slice[1].stop
        
        # 5. Iterate through each pixel within the bounding box
        for r in range(min_r, max_r):
            for c in range(min_c, max_c):
                # 6. Check if the pixel in the *original* input grid is white (0)
                if input_np[r, c] == 0:
                    # 7. If it's white, change the corresponding pixel in the output grid to yellow (4)
                    output_grid[r, c] = 4
                # 8. If it's not white, it retains its original color (already copied)

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```