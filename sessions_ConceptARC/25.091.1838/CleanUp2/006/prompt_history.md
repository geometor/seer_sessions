
## train_1

**input:**
```
3 3 3 3 3 4
4 3 3 3 3 3
3 3 3 4 3 3
3 3 3 3 3 3
3 3 3 3 3 3
3 3 3 4 3 3
```


**output:**
```
3 3 3 3 3 3
3 3 3 3 3 3
3 3 3 3 3 3
3 3 3 3 3 3
3 3 3 3 3 3
3 3 3 3 3 3
```


## train_2

**input:**
```
6 6 6 6 8 6
8 6 6 3 6 6
6 6 6 6 6 6
6 6 8 6 3 6
3 6 6 6 6 6
6 6 6 6 6 6
```


**output:**
```
6 6 6 6 6 6
6 6 6 6 6 6
6 6 6 6 6 6
6 6 6 6 6 6
6 6 6 6 6 6
6 6 6 6 6 6
```


## train_3

**input:**
```
0 5 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 5 0
0 2 2 2 2 2 2 2 2 0
5 2 2 2 2 2 2 2 2 0
0 2 2 5 2 2 5 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 5 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The task involves cleaning up or homogenizing the input grid based on the dominant color. In each example, the input grid contains a primary 'background' color and one or more other 'noise' or 'foreground' colors scattered within it. The output grid consists only of the background color, replacing all the noise pixels. In one case (example 3), there's a distinct border color which is preserved, and the homogenization happens only within this border.

*   **YAML Facts:**
    
```yaml
    task_type: homogenization
    input_characteristics:
      - grid_dimensions: variable (e.g., 6x6, 10x10)
      - pixel_colors: multiple distinct colors present
      - structure:
          - often a dominant background color
          - scattered pixels of other colors ('noise')
          - potential for a uniform border color (e.g., white in example 3)
    output_characteristics:
      - grid_dimensions: same as input
      - pixel_colors:
          - primarily the dominant background color from the input
          - preserves the border color if one was present and distinct in the input
      - structure: uniform area of the background color, potentially enclosed by the preserved border color
    transformation:
      - identify the dominant color (most frequent, potentially excluding a border)
      - identify if a uniform border exists (all pixels in first/last rows/columns are the same color, different from the dominant internal color)
      - replace all pixels that are neither the dominant color nor the border color (if applicable) with the dominant color
    color_mapping:
      - example 1: background=green(3), noise=yellow(4) -> output=all green(3)
      - example 2: background=magenta(6), noise=azure(8), green(3) -> output=all magenta(6)
      - example 3: border=white(0), background=red(2), noise=gray(5) -> output=red(2) inside white(0) border
    ```


*   **Natural Language Program:**
    1.  Determine the dimensions (height H, width W) of the input grid.
    2.  Identify the color present in the majority of the pixels in the input grid; this is the 'background color'.
    3.  *Optional Border Check:* Check if all pixels forming the perimeter (row 0, row H-1, column 0, column W-1) share the same color, and if this color is different from the overall background color identified in step 2. If both conditions are true, identify this perimeter color as the 'border color'.
    4.  Create a new output grid with the same dimensions (H x W).
    5.  Iterate through each pixel (at row `r`, column `c`) of the input grid:
        a.  If a 'border color' was identified in step 3 and the current pixel's color matches the 'border color', place the 'border color' at position (`r`, `c`) in the output grid.
        b.  Else if the current pixel's color matches the 'background color' identified in step 2, place the 'background color' at position (`r`, `c`) in the output grid.
        c.  Otherwise (the pixel is neither the background color nor the identified border color), place the 'background color' at position (`r`, `c`) in the output grid.
    6.  Return the completed output grid.
```python
"""
Transforms an input grid by identifying a dominant 'background' color and potentially a distinct 'border' color. 
If a uniform border color exists (all perimeter pixels are the same color and different from the most frequent color in the interior), it is preserved. 
All other pixels in the grid are set to the dominant background color (the most frequent color, excluding the border if one exists).
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Applies the homogenization transformation to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    border_color = None
    background_color = None

    # Check for a uniform border
    perimeter_pixels = []
    if height > 1 and width > 1:
        perimeter_pixels.extend(input_array[0, :])      # Top row
        perimeter_pixels.extend(input_array[-1, :])     # Bottom row
        perimeter_pixels.extend(input_array[1:-1, 0])   # Left column (excluding corners)
        perimeter_pixels.extend(input_array[1:-1, -1])  # Right column (excluding corners)
    elif height == 1 and width > 0 : # single row
        perimeter_pixels.extend(input_array[0, :])
    elif width == 1 and height > 0: # single col
        perimeter_pixels.extend(input_array[:, 0])
    elif height == 1 and width == 1: # single pixel
        perimeter_pixels.append(input_array[0,0])
        
    potential_border_color = -1 # Use -1 as default invalid color
    is_uniform_border = False
    if perimeter_pixels:
        potential_border_color = perimeter_pixels[0]
        is_uniform_border = all(p == potential_border_color for p in perimeter_pixels)

    # Determine background color and confirm border color
    if is_uniform_border and height > 2 and width > 2:
        # If a uniform border exists, find the dominant color inside the border
        inner_grid = input_array[1:-1, 1:-1]
        if inner_grid.size > 0:
            inner_counts = Counter(inner_grid.flatten())
            # Check if the potential border color is the most frequent *inside*
            most_common_inner = inner_counts.most_common(1)
            if most_common_inner:
                 # Check if potential border color is different than inner dominant
                 if potential_border_color != most_common_inner[0][0]:
                      border_color = potential_border_color
                      background_color = most_common_inner[0][0]
                 else: # Border color is same as most common inner, treat as no border
                      is_uniform_border = False 
            else: # Inner grid is empty or uniform with border color
                 if potential_border_color != input_array[1,1]: #check if border different than one inside pixel
                     border_color = potential_border_color
                     background_color = input_array[1,1] #assign inside pixel value as background
                 else:
                    is_uniform_border = False # treat as no border

    # If no distinct border was confirmed, find the dominant color in the whole grid
    if background_color is None:
        all_pixels = input_array.flatten()
        if all_pixels.size > 0:
            all_counts = Counter(all_pixels)
            background_color = all_counts.most_common(1)[0][0]
        else:
             return [] # Handle empty input grid case

    # Create the output grid
    # Initialize with the background color
    output_array = np.full_like(input_array, background_color)

    # If a distinct border was identified, draw it onto the output grid
    if border_color is not None:
        if height > 0:
            output_array[0, :] = border_color   # Top row
            output_array[-1, :] = border_color  # Bottom row
        if width > 0 :
            output_array[:, 0] = border_color   # Left column
            output_array[:, -1] = border_color  # Right column

    # Convert back to list of lists for the expected output format
    output_grid = output_array.tolist()
    
    return output_grid
```
```python
"""
Transforms an input grid based on color frequency and the potential presence of a white (0) frame.

If a 'white frame' is identified (meaning white pixels exist, at least one white pixel touches the grid perimeter, and at least one non-white pixel exists), the transformation preserves the white pixels in their original positions and fills all other (non-white) positions with the most frequent color found among those non-white pixels.

If no such white frame is identified, the transformation fills the entire output grid with the single most frequent color found in the overall input grid.
"""

import numpy as np
from collections import Counter

def check_perimeter_touch(grid_array, color_value):
    """Checks if any pixel of color_value touches the perimeter."""
    height, width = grid_array.shape
    if height == 0 or width == 0:
        return False
    
    # Check top and bottom rows
    if height > 0:
        if np.any(grid_array[0, :] == color_value): return True
        if np.any(grid_array[-1, :] == color_value): return True
        
    # Check left and right columns (excluding corners already checked)
    if width > 0:
        if np.any(grid_array[:, 0] == color_value): return True
        if np.any(grid_array[:, -1] == color_value): return True
        
    return False

def transform(input_grid):
    """
    Applies the conditional homogenization transformation.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Handle empty grid case
    if height == 0 or width == 0:
        return []

    # --- Analysis Step ---
    
    # 1. Count all pixel colors
    all_pixels = input_array.flatten()
    if all_pixels.size == 0: # Should not happen due to height/width check, but safety first
        return []
    color_counts = Counter(all_pixels)
    
    # 2. Identify overall dominant color
    dominant_overall_color = color_counts.most_common(1)[0][0]

    # 3. Check for white frame conditions
    has_white_pixels = 0 in color_counts
    white_touches_perimeter = False
    has_non_white_pixels = any(color != 0 for color in color_counts)
    
    if has_white_pixels:
        white_touches_perimeter = check_perimeter_touch(input_array, 0)

    # 4. Determine if a white frame exists
    white_frame_exists = has_white_pixels and white_touches_perimeter and has_non_white_pixels

    # --- Transformation Step ---
    
    output_array = np.zeros_like(input_array) # Initialize output array

    if white_frame_exists:
        # 5a. Identify interior (non-white) pixels
        white_mask = (input_array == 0)
        interior_pixels = input_array[~white_mask]
        
        # 5b. Find dominant interior color
        if interior_pixels.size > 0:
            interior_counts = Counter(interior_pixels)
            dominant_interior_color = interior_counts.most_common(1)[0][0]
        else:
            # This case should technically not be reached if has_non_white_pixels is true
            # but as a fallback, use the overall dominant color if interior is empty.
             dominant_interior_color = dominant_overall_color 
             # Or handle as an error/edge case? For now, fill with something.
             # If the grid was ONLY white, white_frame_exists would be False.
             # So this implies white frame exists but *only* non-white noise was present?
             # Let's default to preserving white and filling rest with overall dominant.
             # This logic might need refinement based on more edge case examples.


        # 5c/d. Create output grid: preserve white, fill interior
        output_array = np.full_like(input_array, dominant_interior_color) # Fill with interior color first
        output_array[white_mask] = 0 # Put back the white pixels


    else:
        # 6a. Create output grid filled with overall dominant color
        output_array = np.full_like(input_array, dominant_overall_color)

    # Convert back to list of lists for the expected output format
    output_grid = output_array.tolist()
    
    return output_grid
```
```python
"""
Transforms an input grid based on the presence and location of white (0) pixels.

If white pixels (color 0) exist, touch the grid's perimeter, and non-white pixels also exist, 
then the transformation preserves the white pixels and replaces all non-white pixels with the 
single most frequent non-white color found in the input grid.

Otherwise (if white pixels are absent, don't touch the perimeter, or no non-white pixels exist), 
the transformation replaces the entire grid with the single most frequent color found in the 
overall input grid.
"""

import numpy as np
from collections import Counter

def _check_perimeter_touch(grid_array, color_value):
    """
    Checks if any pixel of the specified color touches the outer perimeter of the grid.

    Args:
        grid_array (np.array): The input grid as a NumPy array.
        color_value (int): The color value to check for.

    Returns:
        bool: True if the color touches the perimeter, False otherwise.
    """
    height, width = grid_array.shape
    if height == 0 or width == 0:
        return False
    
    # Check top row
    if height > 0 and np.any(grid_array[0, :] == color_value):
        return True
    # Check bottom row
    if height > 1 and np.any(grid_array[-1, :] == color_value):
        return True
    # Check left column
    if width > 0 and np.any(grid_array[:, 0] == color_value):
        return True
    # Check right column
    if width > 1 and np.any(grid_array[:, -1] == color_value):
        return True
        
    return False

def transform(input_grid):
    """
    Applies the conditional homogenization transformation to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert input to NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Handle empty grid case
    if height == 0 or width == 0:
        return []

    # --- Analysis Step ---
    
    # 1. Count all pixel colors
    all_pixels = input_array.flatten()
    if all_pixels.size == 0: 
        return [] # Should not happen if height/width > 0, but safety check
    color_counts = Counter(all_pixels)
    
    # 2. Check for the 'white frame' conditions
    has_white_pixels = 0 in color_counts
    white_touches_perimeter = False
    if has_white_pixels:
        white_touches_perimeter = _check_perimeter_touch(input_array, 0)
        
    has_non_white_pixels = any(color != 0 for color in color_counts)
    
    # Determine if the special white frame logic applies
    apply_white_frame_logic = has_white_pixels and white_touches_perimeter and has_non_white_pixels

    # --- Transformation Step ---
    
    output_array = np.zeros_like(input_array) # Initialize output array (content will be overwritten)

    if apply_white_frame_logic:
        # Branch 1: Preserve white, fill rest with dominant non-white color
        
        # Find dominant interior (non-white) color
        non_white_pixels = all_pixels[all_pixels != 0]
        # We know non_white_pixels is not empty because has_non_white_pixels is True
        interior_counts = Counter(non_white_pixels)
        dominant_interior_color = interior_counts.most_common(1)[0][0]
        
        # Create output grid: fill with dominant interior color first
        output_array = np.full_like(input_array, dominant_interior_color) 
        # Identify white pixel locations
        white_mask = (input_array == 0)
        # Put back the white pixels in their original locations
        output_array[white_mask] = 0 

    else:
        # Branch 2: Fill entire grid with the overall dominant color
        
        # Find the most frequent color overall
        dominant_overall_color = color_counts.most_common(1)[0][0]
        
        # Create output grid filled with the overall dominant color
        output_array = np.full_like(input_array, dominant_overall_color)

    # Convert the result back to list of lists format
    output_grid = output_array.tolist()
    
    return output_grid
```
