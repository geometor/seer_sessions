import numpy as np
from typing import List, Optional

"""
Transforms an input grid based on the presence and location of axes marked by the number 4.

The transformation rule depends on the axes found:
1. No Axes: Output is identical to input.
2. Horizontal Axis Only (at row h): The region above the axis in the input is copied to both the region above and the region below the axis in the output. The axis itself is copied. Other areas remain 0.
3. Vertical Axis Only (at column v): The region left of the axis in the input is copied to both the region left and the region right of the axis in the output. The axis itself is copied. Other areas remain 0.
4. Both Axes (at row h, column v): 
   - Input Top-Left (TL) quadrant is copied to Output Top-Left (TL).
   - Input Bottom-Left (BL) quadrant is copied to Output Top-Right (TR).
   - Input Top-Left (TL) quadrant is copied to Output Bottom-Left (BL).
   - Input Bottom-Right (BR) quadrant is copied to Output Bottom-Right (BR).
   - Both axes are copied.
"""

def find_horizontal_axis(grid: np.ndarray) -> Optional[int]:
    """Finds the row index of a horizontal axis (all 4s). Returns None if not found."""
    rows, _ = grid.shape
    for r in range(rows):
        # Check if all elements in the row are equal to 4
        if np.all(grid[r, :] == 4):
            return r
    return None

def find_vertical_axis(grid: np.ndarray) -> Optional[int]:
    """Finds the column index of a vertical axis (all 4s). Returns None if not found."""
    _, cols = grid.shape
    for c in range(cols):
        # Check if all elements in the column are equal to 4
        if np.all(grid[:, c] == 4):
            return c
    return None

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """Applies the transformation rule based on identified axes of 4s."""

    # Convert input list of lists to a numpy array for efficient slicing
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Locate the horizontal and vertical axes
    h_axis_idx = find_horizontal_axis(input_np)
    v_axis_idx = find_vertical_axis(input_np)

    # Case 1: No axes found
    if h_axis_idx is None and v_axis_idx is None:
        # If no axes are present, return the input grid unchanged
        return input_grid

    # Initialize the output grid with zeros, same shape as input
    # This is done for all cases where transformation occurs (axes found)
    output_np = np.zeros_like(input_np)

    # Case 4: Both horizontal and vertical axes found
    if h_axis_idx is not None and v_axis_idx is not None:
        h = h_axis_idx
        v = v_axis_idx

        # Copy the horizontal and vertical axes from input to output
        output_np[h, :] = input_np[h, :]
        output_np[:, v] = input_np[:, v] # Note: The intersection cell input_np[h, v] = 4 is correctly handled.

        # Define source quadrants based on input grid slices
        # Need Input Top-Left (TL), Bottom-Left (BL), Bottom-Right (BR)
        source_tl = input_np[0:h, 0:v]       # Rows < h, Cols < v
        source_bl = input_np[h+1:rows, 0:v]   # Rows > h, Cols < v
        source_br = input_np[h+1:rows, v+1:cols] # Rows > h, Cols > v

        # Perform the quadrant copies based on the rule:
        # Input TL -> Output TL
        if source_tl.size > 0: # Check ensures the quadrant exists (h>0 and v>0)
             output_np[0:h, 0:v] = source_tl
        # Input BL -> Output TR
        if source_bl.size > 0: # Check ensures source BL exists (h+1<rows and v>0)
            if h > 0 and v + 1 < cols: # Check ensures target TR exists
                 output_np[0:h, v+1:cols] = source_bl
        # Input TL -> Output BL
        if source_tl.size > 0: # Check ensures source TL exists (h>0 and v>0)
            if h + 1 < rows and v > 0: # Check ensures target BL exists
                output_np[h+1:rows, 0:v] = source_tl
        # Input BR -> Output BR
        if source_br.size > 0: # Check ensures source BR exists (h+1<rows and v+1<cols)
            # Target BR uses the same indices as source BR, check already done
            output_np[h+1:rows, v+1:cols] = source_br

    # Case 2: Only horizontal axis found
    elif h_axis_idx is not None:
        h = h_axis_idx

        # Copy the horizontal axis from input to output
        output_np[h, :] = input_np[h, :]

        # Define the source region (area above the axis in the input)
        source_upper = input_np[0:h, :] # Rows < h

        # Copy the source region to the upper and lower regions of the output
        if source_upper.size > 0: # Check ensures upper region exists (h>0)
            # Copy to Output Upper region (Rows < h)
            output_np[0:h, :] = source_upper
            # Copy to Output Lower region (Rows > h)
            if h + 1 < rows: # Check ensures lower region exists
                 output_np[h+1:rows, :] = source_upper

    # Case 3: Only vertical axis found
    elif v_axis_idx is not None:
        v = v_axis_idx

        # Copy the vertical axis from input to output
        output_np[:, v] = input_np[:, v]

        # Define the source region (area left of the axis in the input)
        source_left = input_np[:, 0:v] # Cols < v

        # Copy the source region to the left and right regions of the output
        if source_left.size > 0: # Check ensures left region exists (v>0)
            # Copy to Output Left region (Cols < v)
            output_np[:, 0:v] = source_left
            # Copy to Output Right region (Cols > v)
            if v + 1 < cols: # Check ensures right region exists
                output_np[:, v+1:cols] = source_left

    # Convert the final numpy array back to a list of lists format
    return output_np.tolist()