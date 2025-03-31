"""
Select one of three 3x3 subgrids from a 9x3 input grid based on specific
patterns in the Most Frequent Color (MFC) counts of the subgrids.

1. Divide the input 9x3 grid into three 3x3 subgrids vertically: S1 (top, index 0),
   S2 (middle, index 1), and S3 (bottom, index 2).
2. For each subgrid, calculate its Most Frequent Color count (MFC) by finding the
   color that appears most often and counting its occurrences. Let these counts
   be m1, m2, and m3.
3. Determine the subgrid to select using the following specific pattern checks,
   applied in order:
    a. If m2 is strictly greater than m1 AND m2 is strictly greater than m3 AND
       m1 equals m3 (pattern [min, max, min]), select S2 (index 1).
    b. Else if m2 equals m3 AND m2 is strictly less than m1 (pattern [max, min, min]),
       select S3 (index 2).
    c. Else if m1, m2, and m3 are all different values, select S1 (index 0).
    d. Otherwise (for any other pattern, including all equal, other shared patterns, etc.),
       select S1 (index 0).
4. The selected subgrid is the output.
"""

import numpy as np
from collections import Counter

def _calculate_mfc(subgrid):
    """
    Calculates the frequency count of the most frequent color in a subgrid (numpy array).
    """
    # Flatten the 2D subgrid into a 1D list of pixels
    pixels = subgrid.flatten()
    # Count occurrences of each color, handle empty grid case
    if not pixels.size:
        return 0
    counts = Counter(pixels)
    # Find the highest frequency count
    # If counts is empty (e.g., empty subgrid), return 0
    # Otherwise, get the count of the most common item
    most_common_count = counts.most_common(1)[0][1] if counts else 0
    return most_common_count

def transform(input_grid):
    """
    Applies the transformation rules based on MFC pattern analysis to the input grid.
    """
    # Convert input list of lists to numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Basic validation for expected structure
    if height != 9 or width != 3:
        # Handle unexpected dimensions - return empty grid for this task
        print(f"Warning: Unexpected input dimensions {height}x{width}. Expected 9x3.")
        return [[]]

    # 1. Divide the input grid into three 3x3 subgrids
    subgrid_height = 3
    subgrids = []
    try:
        for i in range(0, height, subgrid_height):
            subgrid = input_np[i:i+subgrid_height, :]
            # Ensure subgrid has the correct shape before adding
            if subgrid.shape == (subgrid_height, width):
                 subgrids.append(subgrid)
            else:
                # This should ideally not happen with height=9, width=3, subgrid_height=3
                raise ValueError("Subgrid slicing resulted in unexpected shape.")
        
        # Ensure we got exactly 3 subgrids
        if len(subgrids) != 3:
             raise ValueError(f"Input height {height} did not yield 3 subgrids.")

    except ValueError as e:
         print(f"Error during subgrid creation: {e}")
         return [[]] # Return empty grid on error

    # 2. Calculate MFC for each subgrid
    m1 = _calculate_mfc(subgrids[0])
    m2 = _calculate_mfc(subgrids[1])
    m3 = _calculate_mfc(subgrids[2])
    mfcs = [m1, m2, m3] # For the distinct check

    # 3. Determine the subgrid to select using prioritized pattern checks
    selected_index = -1 # Initialize with an invalid index

    # 3a: Check for [min, max, min] pattern
    if m2 > m1 and m2 > m3 and m1 == m3:
        selected_index = 1
    # 3b: Check for [max, min, min] pattern
    elif m2 == m3 and m2 < m1:
        selected_index = 2
    # 3c: Check for distinct values
    elif len(set(mfcs)) == 3:
        selected_index = 0
    # 3d: Default for all other cases
    else:
        selected_index = 0

    # 4. The selected subgrid is the output
    # Check if a valid index was selected (should always happen with the logic above)
    if selected_index == -1:
         print("Error: No selection rule matched and no default applied.")
         return [[]] # Return empty grid on error

    output_grid_np = subgrids[selected_index]

    # Convert the NumPy array output back to a list of lists
    return output_grid_np.tolist()
