Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from scipy.ndimage import label, find_objects

"""
The transformation identifies connected components of green (3) pixels in the input grid. 
For each green object, it determines its symmetry and aspect ratio to decide on a reflection:
1. Find all distinct green (3) objects.
2. For each object:
   a. Extract its shape (mask) within its bounding box.
   b. Check for vertical symmetry. If true: reflect horizontally, color blue (1), place adjacent to the right.
   c. If not vertically symmetric, check for horizontal symmetry. If true: reflect vertically, color azure (8), place adjacent below.
   d. If not symmetric:
      i. If height > width: reflect vertically, color azure (8), place adjacent below.
      ii. If width >= height: reflect horizontally, color blue (1), place adjacent to the right.
3. Create an output grid of the same dimensions as the input grid, initialized with the input grid's content.
4. Place the calculated reflections onto the output grid.
   - Horizontal reflections (blue) start at column `max_c` (right edge of the bounding box) and row `min_r`.
   - Vertical reflections (azure) start at row `max_r` (bottom edge of the bounding box) and column `min_c`.
5. If a reflection extends beyond the original grid boundaries, it is truncated to fit within the grid.
6. Reflections overwrite existing pixels only where the reflection mask is true (non-zero).
"""

def is_vertically_symmetric(mask):
    """Checks if a 2D boolean mask is vertically symmetric."""
    h, w = mask.shape
    if w == 1: # Single column is always vertically symmetric
        return True
    mid = w // 2
    left = mask[:, :mid]
    right = mask[:, -mid:] # Take last 'mid' columns
    return np.array_equal(left, np.fliplr(right))

def is_horizontally_symmetric(mask):
    """Checks if a 2D boolean mask is horizontally symmetric."""
    h, w = mask.shape
    if h == 1: # Single row is always horizontally symmetric
        return True
    mid = h // 2
    top = mask[:mid, :]
    bottom = mask[-mid:, :] # Take last 'mid' rows
    return np.array_equal(top, np.flipud(bottom))

def transform(input_grid):
    """
    Applies the reflection transformation based on symmetry and aspect ratio,
    placing reflections within the original grid boundaries (truncating if necessary).
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid_np = np.copy(input_grid_np)
    H, W = output_grid_np.shape
    
    # Define the color of interest (green) and background
    target_color = 3
    background_color = 0

    # Find connected components of the target color
    labeled_array, num_features = label(input_grid_np == target_color)
    
    # Find the locations (slices) of these components
    object_slices = find_objects(labeled_array)

    # Store reflection details to apply after finding all objects
    reflections_to_add = [] # List of (mask, color, place_r, place_c) tuples

    # --- Analysis Phase: Determine reflections for each object ---
    for i in range(num_features):
        obj_slice = object_slices[i]
        min_r, max_r = obj_slice[0].start, obj_slice[0].stop
        min_c, max_c = obj_slice[1].start, obj_slice[1].stop
        
        # Extract the object's boolean mask within its bounding box
        # Ensure we only consider pixels belonging to the current object label
        object_mask = (labeled_array[obj_slice] == (i + 1))
        
        h, w = object_mask.shape

        # Determine symmetry
        vert_sym = is_vertically_symmetric(object_mask)
        horiz_sym = is_horizontally_symmetric(object_mask)

        reflected_mask = None
        new_color = 0
        place_r, place_c = 0, 0
        reflection_type = None # 'h' for horizontal, 'v' for vertical

        # Apply rules based on symmetry and aspect ratio
        if vert_sym:
            # Rule 1: Vertically symmetric -> Reflect horizontally, color blue, place right
            reflected_mask = np.fliplr(object_mask)
            new_color = 1  # blue
            place_r = min_r
            place_c = max_c # Place starting at the column *after* the bounding box
            reflection_type = 'h'
            
        elif horiz_sym:
            # Rule 2: Horizontally symmetric (and not vertically) -> Reflect vertically, color azure, place below
            reflected_mask = np.flipud(object_mask)
            new_color = 8  # azure
            place_r = max_r # Place starting at the row *after* the bounding box
            place_c = min_c
            reflection_type = 'v'
            
        else: # Not symmetric
            if h > w:
                 # Rule 3: Not symmetric, height > width -> Reflect vertically, color azure, place below
                reflected_mask = np.flipud(object_mask)
                new_color = 8  # azure
                place_r = max_r
                place_c = min_c
                reflection_type = 'v'
            else: # width >= height
                # Rule 4: Not symmetric, width >= height -> Reflect horizontally, color blue, place right
                reflected_mask = np.fliplr(object_mask)
                new_color = 1  # blue
                place_r = min_r
                place_c = max_c
                reflection_type = 'h'

        # Store the reflection details if a reflection was generated
        if reflected_mask is not None:
            reflections_to_add.append((reflected_mask, new_color, place_r, place_c))

    # --- Placement Phase: Add reflections to the output grid (with truncation) ---
    for mask, color, r, c in reflections_to_add:
        h_shape, w_shape = mask.shape
        
        # Calculate the slice coordinates for the reflection in the output grid
        grid_r_start = r
        grid_c_start = c
        grid_r_end = r + h_shape
        grid_c_end = c + w_shape
        
        # Calculate the slice coordinates for the mask itself (init
---
