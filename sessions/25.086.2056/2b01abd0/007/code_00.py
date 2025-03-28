import numpy as np

"""
Reflects objects across a central blue line (axis), swapping specific color 
pairs (Red<->Green, Yellow<->Azure, Gray<->Magenta) only on the reflected 
pixels. The original object pixels remain unchanged unless overwritten by a 
reflection.

1. Initialize the output grid as a copy of the input grid.
2. Find the single blue axis line (color 1), its orientation (horizontal/vertical), 
   and index. If no single axis is found, return the copy.
3. Define color swap pairs: Red(2)<->Green(3), Yellow(4)<->Azure(8), 
   Gray(5)<->Magenta(6). Other colors map to themselves.
4. Iterate through each pixel of the *input* grid.
5. If a pixel is an "object pixel" (not background 0, not axis 1):
   a. Calculate its reflection coordinate across the axis.
   b. Determine the swapped color based on the defined pairs.
   c. If the reflection coordinate is within grid bounds, update the *output grid* 
      at that *reflected* coordinate with the *swapped* color.
6. Return the modified output grid.
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
    horizontal_lines = [r for r in range(rows) if np.all(grid[r, :] == 1)]
    
    # Check for vertical line (all elements in a column are 1)
    vertical_lines = [c for c in range(cols) if np.all(grid[:, c] == 1)]

    # Check validity based on examples: exactly one line, not both
    is_single_horizontal = len(horizontal_lines) == 1 and len(vertical_lines) == 0
    is_single_vertical = len(vertical_lines) == 1 and len(horizontal_lines) == 0

    if is_single_horizontal:
        return 'horizontal', horizontal_lines[0]
    elif is_single_vertical:
        return 'vertical', vertical_lines[0]
    else:
        # No single line found or both found, inconsistent with examples
        return None, None


def transform(input_grid):
    """
    Applies reflection across a blue axis and color swap only to reflected pixels.
    
    Args:
        input_grid (np.array): The input grid as a NumPy array.
        
    Returns:
        np.array: The transformed output grid.
    """
    
    # 1. Initialize output_grid as a copy
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 2. Find the blue axis
    orientation, index = find_blue_axis(input_grid)

    # If no single blue line is found per the examples' pattern, return the original grid copy
    if orientation is None:
        # print("Warning: No single horizontal or vertical blue axis found.") # Optional warning
        return output_grid # Return the unchanged copy

    # 3. Define the color swap map 
    color_swap_map = {
        2: 3, 3: 2,  # Red <-> Green
        4: 8, 8: 4,  # Yellow <-> Azure
        5: 6, 6: 5   # Gray <-> Magenta
    }
    # Include identity mapping for colors not in pairs (0, 1, 7, 9)
    # Although not strictly necessary for the swap logic here, it's good practice
    for i in range(10):
        if i not in color_swap_map:
             color_swap_map[i] = i # Maps color to itself if not in a swap pair

    # 4. Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            original_color = input_grid[r, c]
            
            # 5. Check if it's an object pixel (not background 0, not axis 1)
            if original_color != 0 and original_color != 1:
                
                # 5a. Calculate reflected coordinates
                nr, nc = -1, -1
                if orientation == 'horizontal':
                    axis_row_idx = index
                    nr = axis_row_idx + (axis_row_idx - r)
                    nc = c
                elif orientation == 'vertical':
                    axis_col_idx = index
                    nr = r
                    nc = axis_col_idx + (axis_col_idx - c)

                # 5b. Determine the swapped color based on the original color
                swapped_color = color_swap_map.get(original_color, original_color) # Use .get for safety

                # 5c. Check if the reflection coordinate is within grid bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Update the output grid *only* at the reflected coordinate 
                    # with the *swapped* color.
                    output_grid[nr, nc] = swapped_color
                # Else: Reflection is outside the grid, do nothing. The original pixel
                # remains in the output_grid from the initial copy unless overwritten
                # by *another* pixel's valid reflection.

    # 6. Return the modified grid
    return output_grid