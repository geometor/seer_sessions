```python
import numpy as np

"""
Reflects objects across a central blue line, swapping specific color pairs,
and conditionally removing the original object based on the line's orientation.

1. Identify the blue line (axis) and its orientation (horizontal/vertical).
2. Define color swap pairs: Red(2)<->Green(3), Yellow(4)<->Azure(8), Gray(5)<->Magenta(6).
3. Initialize the output grid as a copy of the input.
4. Iterate through each pixel of the input grid.
5. If a pixel is part of an object (not background-0 or axis-1):
   a. Calculate its reflection coordinate across the blue axis.
   b. Determine the swapped color based on the defined pairs.
   c. Place the swapped color at the reflected coordinate in the output grid, if within bounds.
   d. Record the location of this original object pixel.
6. If the axis is horizontal:
   a. Determine which side of the axis (above or below) contained the original objects.
   b. Iterate through the recorded original object pixel locations.
   c. If an original object pixel was on the identified side, set its location in the output grid to background color (0).
7. If the axis is vertical, the original objects remain alongside the reflection (no removal step).
8. Return the modified output grid.
"""

def find_blue_axis(grid):
    """
    Finds the blue line axis (row/col index) and its orientation ('horizontal'/'vertical').
    
    Args:
        grid (np.array): The input grid.
        
    Returns:
        tuple: (orientation, index) where orientation is 'horizontal' or 'vertical',
               and index is the row or column index of the axis. Returns (None, None) 
               if no single blue line axis is found.
    """
    rows, cols = grid.shape
    
    # Check for horizontal line (all elements in a row are 1)
    for r in range(rows):
        if np.all(grid[r, :] == 1):
            # Verify it's the only horizontal line
            is_only_line = True
            for r_check in range(rows):
                if r_check != r and np.all(grid[r_check, :] == 1):
                    is_only_line = False
                    break
            if is_only_line:
                 # Also ensure no vertical line exists simultaneously
                 for c_check in range(cols):
                     if np.all(grid[:, c_check] == 1):
                         is_only_line = False
                         break
            if is_only_line:
                return 'horizontal', r
            else: # Found multiple lines or crossing lines, invalid state based on examples
                return None, None
            
    # Check for vertical line (all elements in a column are 1)
    for c in range(cols):
        if np.all(grid[:, c] == 1):
             # Verify it's the only vertical line (and no horizontal line exists)
            is_only_line = True
            for c_check in range(cols):
                if c_check != c and np.all(grid[:, c_check] == 1):
                    is_only_line = False
                    break
            # No need to re-check for horizontal lines here, would have been caught above
            if is_only_line:
                return 'vertical', c
            else: # Found multiple lines, invalid state based on examples
                return None, None
                
            
    # Return None if no single blue axis is found
    return None, None

def transform(input_grid):
    """
    Applies the reflection, color swap, and conditional removal transformation.
    
    Args:
        input_grid (np.array): The input grid as a NumPy array.
        
    Returns:
        np.array: The transformed output grid.
    """
    
    # Initialize output_grid as a copy
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the blue axis
    orientation, index = find_blue_axis(input_grid)

    # If no single blue line is found per the examples' pattern, return the original grid
    if orientation is None:
        # This case suggests an input structure different from the training examples
        print("Warning: No single horizontal or vertical blue axis found.")
        return output_grid

    # Define the color swap map based on observed pairs
    color_swap_map = {
        2: 3, 3: 2,  # Red <-> Green
        4: 8, 8: 4,  # Yellow <-> Azure
        5: 6, 6: 5   # Gray <-> Magenta
    }

    # Store original object pixel coordinates and their rows/columns for potential removal
    original_object_pixels = [] 
    # Keep track of rows/columns occupied by original objects relative to the axis
    original_object_rows = set() 
    
    # --- Step 1: Reflect pixels, Swap colors, and Record original object locations ---
    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]

            # Skip background (0) and axis (1) pixels
            if color == 0 or color == 1:
                continue
                
            # This pixel is part of an original object. Record its location.
            original_object_pixels.append((r, c))
            # Store the row index if relevant for horizontal removal logic
            if orientation == 'horizontal': 
                 original_object_rows.add(r)

            # Calculate reflected coordinates based on axis orientation and index
            nr, nc = -1, -1
            if orientation == 'horizontal':
                axis_row_idx = index
                # Reflect vertically across the horizontal line
                nr = axis_row_idx + (axis_row_idx - r)
                nc = c
            elif orientation == 'vertical':
                axis_col_idx = index
                # Reflect horizontally across the vertical line
                nr = r
                nc = axis_col_idx + (axis_col_idx - c)

            # Get swapped color, default to original color if not in the swap map
            swapped_color = color_swap_map.get(color, color)

            # Place the swapped color onto the output grid IF the reflected coordinate is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                output_grid[nr, nc] = swapped_color
            # Else: The reflection falls outside the grid; it's simply not drawn.

    # --- Step 2: Conditional Removal (Only applies if the axis was horizontal) ---
    if orientation == 'horizontal':
        axis_row_idx = index
        
        # Determine if the original objects were located primarily above or below the axis.
        # Based on examples, objects are entirely on one side.
        rows_above_axis = {r for r in original_object_rows if r < axis_row_idx}
        rows_below_axis = {r for r in original_object_rows if r > axis_row_idx}

        # Decide which side needs to be cleared based on where the original objects were.
        clear_above = False
        clear_below = False
        # If objects were found above the axis AND none were found below
        if len(rows_above_axis) > 0 and len(rows_below_axis) == 0:
            clear_above = True
        # If objects were found below the axis AND none were found above
        elif len(rows_below_axis) > 0 and len(rows_above_axis) == 0:
            clear_below = True
        # Handle potential edge cases or deviations from examples (e.g., objects on both sides)
        # For now, strictly following examples where objects are on one side. If ambiguous, do nothing.

        # Iterate through the list of pixels that belonged to the original objects
        for r, c in original_object_pixels:
            # If we determined the objects were above, and this pixel is above, clear it.
            if clear_above and r < axis_row_idx:
                 output_grid[r, c] = 0 # Set to background color (white)
            # If we determined the objects were below, and this pixel is below, clear it.
            elif clear_below and r > axis_row_idx:
                 output_grid[r, c] = 0 # Set to background color (white)

    # If the orientation was 'vertical', no removal step is performed; the original objects persist.
    
    return output_grid
```