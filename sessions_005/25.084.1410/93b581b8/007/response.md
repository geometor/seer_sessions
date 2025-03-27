```python
"""
Transforms an input grid by first copying it, then identifying a unique 2x2 
non-background (non-white) object within the original grid. Four new 2x2 
solid-colored squares are drawn onto the copied grid's corners, overwriting 
any existing content. The color of each corner square is determined by the 
color of the diagonally opposite pixel within the identified 2x2 object:
- Top-left output corner gets the color of the input object's bottom-right pixel.
- Top-right output corner gets the color of the input object's bottom-left pixel.
- Bottom-left output corner gets the color of the input object's top-right pixel.
- Bottom-right output corner gets the color of the input object's top-left pixel.
"""

import numpy as np

def find_2x2_object(grid):
    """
    Finds the top-left corner coordinates (r, c) of the first 2x2 block
    where all cells are non-zero (non-white/background).
    Assumes exactly one such block exists based on the task's examples.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: The row and column (r, c) of the top-left corner of the 
               2x2 object, or None if not found.
    """
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(width - 1):
            # Check if all four cells in the 2x2 block are non-zero (non-white)
            # using numpy slicing for potential efficiency
            if np.all(grid[r:r+2, c:c+2] != 0):
                return r, c
    return None # Should not be reached based on task description if assumptions hold

def draw_2x2_square(grid, r, c, color):
    """
    Fills a 2x2 area in the grid starting at (r, c) with the specified color.
    Modifies the grid in place. Ensures drawing stays within grid boundaries.

    Args:
        grid (np.array): The grid to modify.
        r (int): The starting row index for the 2x2 square.
        c (int): The starting column index for the 2x2 square.
        color (int): The color value to fill with.
    """
    height, width = grid.shape
    # Calculate the actual range to draw, clipping at grid boundaries
    r_end = min(r + 2, height)
    c_end = min(c + 2, width)
    
    # Ensure start indices are valid before attempting to draw
    # and that the slice dimensions are not zero
    if r < height and c < width and r_end > r and c_end > c:
        grid[r:r_end, c:c_end] = color


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        np.array: The transformed grid as a NumPy array.
    """
    # Convert input list of lists to a NumPy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    
    # 1. Create the output grid as an exact copy of the input grid.
    output_grid = np.copy(input_np)
    height, width = output_grid.shape # H and W

    # 2. Scan the input grid to find the unique 2x2 non-background block.
    obj_coords = find_2x2_object(input_np)
    
    # If no object found (unexpected based on task examples), return the unchanged copy.
    if obj_coords is None:
        # Consider adding logging or raising an error if strict adherence requires an object
        return output_grid 
        
    obj_r, obj_c = obj_coords

    # 3. Extract the colors of the four pixels within this 2x2 block from the INPUT grid.
    # Ensure indices are within bounds, though find_2x2_object should guarantee this
    # if an object was found.
    color_tl = input_np[obj_r, obj_c]     # Top-Left
    color_tr = input_np[obj_r, obj_c+1]   # Top-Right
    color_bl = input_np[obj_r+1, obj_c]   # Bottom-Left
    color_br = input_np[obj_r+1, obj_c+1] # Bottom-Right

    # 4. Modify the output grid by drawing 2x2 squares in the corners,
    #    using the diagonally opposite colors from the source object.
    
    # Draw top-left corner (0, 0) using color_BR.
    draw_2x2_square(output_grid, 0, 0, color_br)
    
    # Draw top-right corner (0, W-2) using color_BL.
    # Check if width allows for a 2x2 square starting at W-2
    if width >= 2:
      draw_2x2_square(output_grid, 0, width-2, color_bl)
    
    # Draw bottom-left corner (H-2, 0) using color_TR.
    # Check if height allows for a 2x2 square starting at H-2
    if height >= 2:
      draw_2x2_square(output_grid, height-2, 0, color_tr)
    
    # Draw bottom-right corner (H-2, W-2) using color_TL.
    # Check if both height and width allow for this square
    if height >= 2 and width >= 2:
      draw_2x2_square(output_grid, height-2, width-2, color_tl)

    # 5. The final modified output grid is the result.
    return output_grid
```