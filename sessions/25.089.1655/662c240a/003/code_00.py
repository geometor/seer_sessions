"""
Select one of three 3x3 subgrids from a 9x3 input grid based on color frequency analysis.

1. Divide the input 9x3 grid into three 3x3 subgrids vertically: Subgrid 1 (top, index 0), Subgrid 2 (middle, index 1), and Subgrid 3 (bottom, index 2).
2. For each subgrid, calculate its Most Frequent Color count (MFC) by finding the color that appears most often and counting its occurrences. Let these counts be MFC1, MFC2, and MFC3.
3. Determine the subgrid to select using the following rules, checked in order:
    a. First Check: If MFC1, MFC2, and MFC3 are all different values, select Subgrid 1 (index 0).
    b. Second Check: Otherwise, if exactly one subgrid has the maximum MFC value observed among the three, select that subgrid.
    c. Third Check: Otherwise, if exactly two subgrids share the minimum MFC value observed among the three, select the one of those two that has the higher index (index 2 over index 1, etc.).
    d. Default: Otherwise (if none of the above conditions were met), select Subgrid 1 (index 0).
4. The selected subgrid is the output.
"""

import numpy as np
from collections import Counter

def _calculate_mfc(subgrid):
    """Calculates the frequency count of the most frequent color in a subgrid."""
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
    Applies the transformation rules based on MFC analysis to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Basic validation for expected structure (can be adapted if needed)
    if height != 9 or width != 3:
        # Decide how to handle invalid input - returning empty or original?
        # For now, let's assume valid inputs based on the task description.
        print(f"Warning: Unexpected input dimensions {height}x{width}. Expected 9x3.")
        # Returning an empty grid might be safer than returning original input.
        return [[]]

    # 1. Divide the input grid into three 3x3 subgrids
    subgrid_height = 3
    subgrids = []
    for i in range(0, height, subgrid_height):
        subgrid = input_np[i:i+subgrid_height, :]
        subgrids.append(subgrid)

    # Ensure we got exactly 3 subgrids
    if len(subgrids) != 3:
         print(f"Error: Input height {height} did not yield 3 subgrids of height {subgrid_height}.")
         return [[]] # Return empty grid on error

    # 2. Calculate MFC for each subgrid
    mfcs = [_calculate_mfc(sg) for sg in subgrids] # [mfc1, mfc2, mfc3]

    # 3. Determine the subgrid to select using prioritized rules
    selected_index = -1 # Initialize with an invalid index

    # Rule 3a: All Distinct MFCs
    if len(set(mfcs)) == 3:
        selected_index = 0 # Select the first subgrid (index 0)
    else:
        # Calculate min/max and indices only if needed
        min_mfc = min(mfcs)
        max_mfc = max(mfcs)
        min_indices = [i for i, mfc in enumerate(mfcs) if mfc == min_mfc]
        max_indices = [i for i, mfc in enumerate(mfcs) if mfc == max_mfc]

        # Rule 3b: Unique Maximum MFC
        if len(max_indices) == 1:
            selected_index = max_indices[0] # Select the subgrid with the unique max
        # Rule 3c: Shared Minimum MFC (exactly two)
        elif len(min_indices) == 2:
            selected_index = max(min_indices) # Select the one with the higher index among the two minimums
        # Rule 3d: Default (covers all other cases, e.g., all MFCs equal, two share max)
        else:
            selected_index = 0 # Select the first subgrid

    # Check if a valid index was selected (should always happen with the logic above)
    if selected_index == -1:
         print("Error: No selection rule matched.")
         return [[]] # Return empty grid on error

    # 4. The selected subgrid is the output
    output_grid = subgrids[selected_index]

    # Convert the NumPy array output back to a list of lists
    return output_grid.tolist()