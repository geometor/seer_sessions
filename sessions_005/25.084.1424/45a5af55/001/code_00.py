"""
Transforms an input grid composed of horizontal stripes into a larger output grid
featuring nested square frames.

1.  Analyze the input grid to identify the sequence of horizontal stripes. A stripe
    is a contiguous block of one or more identical rows.
2.  For each stripe, record its color (from any cell in the stripe) and its
    thickness (the number of rows it occupies). Store these as a list of
    (color, thickness) pairs in top-to-bottom order.
3.  Calculate the dimension `D` for the square output grid. If the thicknesses are
    t1, t2, ..., tN, then D = (2 * sum(t1 to tN-1)) + tN. If N=1, D = t1.
4.  Create a new square grid of size D x D, initially filled with a placeholder or
    the color of the outermost frame.
5.  Iterate through the stripes from the first (index 0) to the second-to-last
    (index N-2). For each stripe `i` with `(color_i, thickness_i)`:
    a.  Determine the current boundary based on the thicknesses of the stripes
        already processed. Let `current_offset` be the sum of thicknesses of
        stripes 0 to `i-1`.
    b.  Draw the frame: Fill the top `thickness_i` rows, bottom `thickness_i` rows,
        left `thickness_i` columns, and right `thickness_i` columns within the
        square defined by `(current_offset, current_offset)` and
        `(D - current_offset - 1, D - current_offset - 1)` with `color_i`.
    c.  Update `current_offset` by adding `thickness_i`.
6.  After processing the frames, take the last stripe `(color_N, thickness_N)`.
7.  Fill the central square area of the output grid with `color_N`. This area
    starts at `(current_offset, current_offset)` and has dimensions
    `thickness_N x thickness_N`.
8.  Return the constructed output grid.
"""

import numpy as np

def _identify_stripes(input_grid_np):
    """Identifies horizontal stripes and their properties."""
    stripes = []
    height = input_grid_np.shape[0]
    if height == 0:
        return stripes
        
    r = 0
    while r < height:
        # Get the representative row for the current stripe
        current_row = input_grid_np[r]
        # Assuming all rows in a valid stripe are identical, color is the same everywhere
        # Check if row is non-empty before accessing index 0
        if current_row.size > 0:
             color = current_row[0]
        else:
             # Handle empty rows if necessary, maybe assign a default color or skip
             color = 0 # Default to 'white' or handle as error/special case
        
        thickness = 1
        # Find the total thickness of this stripe
        k = r + 1
        while k < height and np.array_equal(input_grid_np[k], current_row):
            thickness += 1
            k += 1
            
        stripes.append((color, thickness))
        # Move the row pointer past the current stripe
        r += thickness
        
    return stripes

def transform(input_grid):
    """
    Transforms the input grid based on stripe information into nested frames.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    
    # 1 & 2: Identify stripes (color, thickness)
    stripes = _identify_stripes(input_grid_np)
    
    if not stripes:
        # Handle empty input case
        return [] 
        
    num_stripes = len(stripes)
    
    # 3: Calculate output dimension D
    if num_stripes == 1:
        last_thickness = stripes[0][1]
        sum_prev_thicknesses = 0
    else:
        last_thickness = stripes[-1][1]
        sum_prev_thicknesses = sum(t for _, t in stripes[:-1])
        
    dimension = (2 * sum_prev_thicknesses) + last_thickness
    
    # 4: Create output grid (initialize with a value not expected, like -1, or use first color)
    # Let's initialize with 0 (white), common background
    output_grid = np.zeros((dimension, dimension), dtype=int) 
    
    # 5 & 6: Draw frames
    current_offset = 0
    for i in range(num_stripes - 1):
        color, thickness = stripes[i]
        
        # Define the boundaries for the current frame drawing
        start = current_offset
        end = dimension - current_offset 
        
        # Fill top border rows
        output_grid[start : start + thickness, start:end] = color
        # Fill bottom border rows
        output_grid[end - thickness : end, start:end] = color
        # Fill left border columns (between top and bottom borders)
        output_grid[start + thickness : end - thickness, start : start + thickness] = color
        # Fill right border columns (between top and bottom borders)
        output_grid[start + thickness : end - thickness, end - thickness : end] = color
        
        # Update offset for the next inner frame/center
        current_offset += thickness
        
    # 7: Fill the center square with the last stripe's color
    if num_stripes > 0:
        center_color, center_thickness = stripes[-1]
        start = current_offset
        # The end index for slicing should be start + thickness
        end = start + center_thickness 
        
        # Verify calculation: D - current_offset should equal end
        # D - offset = (2*sum_prev + last_thick) - sum_prev = sum_prev + last_thick
        # start + thick = sum_prev + last_thick. They match.
        
        output_grid[start:end, start:end] = center_color
        
    # 8: Return the result as list of lists
    return output_grid.tolist()
