
## train_1

**input:**
```
0 0 0 5 0 2 0 5 2 0 0
2 0 0 5 0 0 0 5 0 0 2
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
2 0 0 5 0 0 0 5 0 0 0
2 0 0 5 0 0 2 5 0 0 0
0 0 0 5 0 0 0 5 0 2 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
2 0 0 5 0 0 2 5 0 0 2
0 0 0 5 0 0 0 5 0 0 0
```


**output:**
```
0 0 0 5 0 0 0 5 2 2 2
0 0 0 5 0 0 0 5 2 2 2
0 0 0 5 0 0 0 5 2 2 2
5 5 5 5 5 5 5 5 5 5 5
2 2 2 5 0 0 0 5 0 0 0
2 2 2 5 0 0 0 5 0 0 0
2 2 2 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
```


## train_2

**input:**
```
0 0 0 5 0 0 0 5 0 0 0
1 0 0 5 0 0 0 5 0 1 0
0 0 0 5 0 0 1 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 1 5 0 0 0
0 0 0 5 0 0 0 5 0 1 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 1 0 0
0 1 0 5 0 0 0 5 0 0 1
0 0 0 5 0 0 0 5 0 0 0
```


**output:**
```
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 1 1 1
0 0 0 5 0 0 0 5 1 1 1
0 0 0 5 0 0 0 5 1 1 1
```


## train_3

**input:**
```
3 3 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 3 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 3 0 5 0 3 0 5 0 0 0
0 0 0 5 3 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 3 0 5 3 0 0 5 3 3 0
0 0 0 5 0 0 0 5 0 0 3
```


**output:**
```
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 3 3 3
0 0 0 5 0 0 0 5 3 3 3
0 0 0 5 0 0 0 5 3 3 3
```

Okay, let's analyze the provided examples.

**Perception of Elements:**

1.  **Grid Structure:** The input and output grids are consistently 11x11.
2.  **Invariant Frame:** There's a persistent frame made of gray (5) pixels. Horizontal gray lines are at rows 3 and 7 (0-indexed), and vertical gray lines are at columns 3 and 7. These lines divide the grid into nine distinct 3x3 subgrids or "cells". These gray lines remain unchanged in the output.
3.  **Content Pixels:** Inside the 3x3 cells, pixels can be white (0) or other colors (red=2, blue=1, green=3 in the examples).
4.  **Transformation:** The core transformation happens within the 3x3 cells. In the output, some 3x3 cells become entirely filled with a single color (e.g., red, blue, or green), while others become entirely filled with white (0).
5.  **Color Selection:** In each example pair, only one primary color (other than white or gray) seems active in the transformation.
    *   Example 1: Red (2) pixels in the input lead to solid red blocks in the output.
    *   Example 2: Blue (1) pixels in the input lead to solid blue blocks in the output.
    *   Example 
```python
import numpy as np

"""
Identifies a gray (5) frame structure located at rows 3 and 7, and columns 3 and 7 (0-indexed), which divides the grid into nine 3x3 subgrids.
Determines the single "active" color present within the 3x3 subgrids of the input grid. The active color is any color other than white (0) or gray (5).
Creates an output grid initialized to white (0).
Copies the gray (5) frame from the input grid to the output grid.
Iterates through each of the nine 3x3 subgrid locations defined by the frame.
For each location, it examines the corresponding 3x3 subgrid in the input grid.
If the input subgrid contains at least one pixel of the active color, the corresponding 3x3 subgrid in the output grid is filled entirely with that active color.
If the input subgrid does not contain any pixel of the active color, the corresponding 3x3 subgrid in the output grid remains filled with white (0).
The gray frame is explicitly maintained in the final output.
"""

def find_active_color(grid):
    """
    Finds the first non-white (0) and non-gray (5) color within the areas
    not occupied by the gray frame (assumed at rows 3, 7 and cols 3, 7).
    
    Args:
        grid (np.array): The input grid.
        
    Returns:
        int or None: The active color value, or None if no active color is found.
    """
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            # Skip pixels belonging to the gray frame
            # Assumes frame is at fixed indices 3 and 7
            if r == 3 or r == 7 or c == 3 or c == 7:
                continue
            
            pixel = grid[r, c]
            # Check if the pixel is neither white (0) nor gray (5)
            if pixel != 0 and pixel != 5: 
                return pixel # Found the active color
                
    return None # No active color found in the designated subgrid areas

def transform(input_grid):
    """
    Transforms the input grid based on the presence of an 'active color' 
    within 3x3 subgrids defined by a gray frame. Subgrids containing the 
    active color are filled with it; others become white. The frame is preserved.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # Initialize the output grid with white (0)
    output_np = np.zeros_like(input_np)
    
    # Define the color for the frame
    gray_color = 5

    # Find the single active color in the input grid (ignoring the frame)
    active_color = find_active_color(input_np)

    # Define the top-left corner coordinates of the 3x3 subgrids.
    # These are determined by the placement of the gray frame lines.
    # Assumes the standard 11x11 grid structure from examples for index calculation.
    subgrid_starts = []
    # Iterate potential row starts (0, 4, 8, ...)
    for r_start in range(0, rows, 4): 
         # Iterate potential col starts (0, 4, 8, ...)
         for c_start in range(0, cols, 4):
             # Check if a 3x3 grid starting here fits within the bounds
             if r_start + 3 <= rows and c_start + 3 <= cols:
                 subgrid_starts.append((r_start, c_start))

    # Process each 3x3 subgrid location
    for r_start, c_start in subgrid_starts:
        # Extract the corresponding 3x3 subgrid from the input grid
        subgrid_input = input_np[r_start:r_start+3, c_start:c_start+3]

        # Check if the active color exists within this input subgrid
        # This check is only meaningful if an active_color was found
        contains_active_color = False
        if active_color is not None:
            contains_active_color = np.any(subgrid_input == active_color)

        # Fill the corresponding subgrid area in the output grid
        if contains_active_color:
            # Fill the 3x3 area with the active color
            output_np[r_start:r_start+3, c_start:c_start+3] = active_color
        else:
            # If no active color, or subgrid doesn't contain it, 
            # the area remains white (0) as initialized. No action needed.
            pass 

    # Explicitly reconstruct the gray frame in the output grid AFTER processing subgrids.
    # This ensures the frame is intact, even if subgrid fills touched frame indices.
    # Horizontal frame lines
    if rows > 3:
        output_np[3, :] = gray_color
    if rows > 7:
        output_np[7, :] = gray_color
    # Vertical frame lines
    if cols > 3:
        output_np[:, 3] = gray_color
    if cols > 7:
        output_np[:, 7] = gray_color
        
    # Ensure frame intersection points are gray (important if frame lines are thin)
    # These might be redundant if the line assignments above cover them, but it's safe.
    if rows > 3 and cols > 3: output_np[3, 3] = gray_color
    if rows > 3 and cols > 7: output_np[3, 7] = gray_color
    if rows > 7 and cols > 3: output_np[7, 3] = gray_color
    if rows > 7 and cols > 7: output_np[7, 7] = gray_color

    # Convert the final numpy array back to a list of lists
    return output_np.tolist()
```
