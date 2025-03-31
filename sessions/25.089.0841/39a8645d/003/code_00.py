import numpy as np
from typing import List, Tuple, Dict, Any, Optional

"""
The transformation identifies all 3x3 subgrids within the input grid that contain pixels of exactly one non-white color (along with potentially white pixels). Among these valid monochromatic subgrids, a specific one is selected based on a hierarchy of criteria:
1. Highest non-white color value: Prioritize subgrids with the numerically highest single non-white color.
2. Highest count of the primary color: Among those tied for the highest color value, prioritize subgrids containing the most pixels of that color.
3. Position (top-left preference): If a tie remains after considering color value and count, select the subgrid whose center pixel is located at the highest row index, and among those, the leftmost column index.
The output is the selected 3x3 subgrid. If no monochromatic 3x3 subgrids are found, the output is a 3x3 grid of white pixels (0).
"""

def _check_monochromatic(subgrid: np.ndarray) -> Tuple[bool, int, int]:
    """
    Checks if a 3x3 subgrid is monochromatic (exactly one non-white color).

    Args:
        subgrid: A 3x3 numpy array representing the subgrid.

    Returns:
        A tuple (is_monochromatic, color, count).
        is_monochromatic is True if the subgrid contains exactly one non-white color.
        color is the non-white color value if is_monochromatic is True, otherwise -1.
        count is the number of pixels of that color if is_monochromatic is True, otherwise 0.
    """
    # Find all unique pixel values in the subgrid
    unique_colors = np.unique(subgrid)
    
    # Filter out the white color (0) to get unique non-white colors
    non_white_colors = unique_colors[unique_colors != 0]

    # Check if there is exactly one unique non-white color
    if len(non_white_colors) == 1:
        color = int(non_white_colors[0])
        # Count the occurrences of this non-white color
        count = int(np.sum(subgrid == color))
        return True, color, count
    else:
        # Either zero or more than one non-white color
        return False, -1, 0

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Finds and returns a specific 3x3 monochromatic subgrid based on highest color,
    highest count of that color, and top-left position preference.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the selected 3x3 output grid, or a 3x3 white
        grid if no valid monochromatic subgrid is found or input is too small.
    """
    # Convert input list of lists to a NumPy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Default 3x3 white grid
    default_output = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Check if the grid is large enough to contain a 3x3 subgrid
    if height < 3 or width < 3:
        return default_output

    # Store information about valid monochromatic subgrids found
    valid_candidates: List[Dict[str, Any]] = []

    # 1. Find all valid monochromatic subgrids and their properties
    # Iterate through all possible center coordinates (r, c) for 3x3 subgrids.
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            # Extract the 3x3 subgrid centered at (r, c)
            subgrid = input_np[r-1 : r+2, c-1 : c+2]

            # Check if the extracted subgrid is monochromatic
            is_mono, color, count = _check_monochromatic(subgrid)

            if is_mono:
                # Store relevant information for valid candidates
                valid_candidates.append({
                    'grid': subgrid,
                    'center_r': r,
                    'center_c': c,
                    'color': color,
                    'count': count
                })

    # 2. Handle case where no valid subgrids were found
    if not valid_candidates:
        return default_output

    # 3. Apply selection criteria hierarchically
    
    # 3a. Find the maximum color value among valid candidates
    max_color = -1
    for candidate in valid_candidates:
        if candidate['color'] > max_color:
            max_color = candidate['color']

    # Filter candidates to keep only those with the max color
    max_color_candidates = [
        cand for cand in valid_candidates if cand['color'] == max_color
    ]

    # 3b. Find the maximum count of the max color among the remaining candidates
    max_count = -1
    for candidate in max_color_candidates:
        if candidate['count'] > max_count:
            max_count = candidate['count']
            
    # Filter candidates to keep only those with the max count for the max color
    max_count_candidates = [
        cand for cand in max_color_candidates if cand['count'] == max_count
    ]

    # 3c. Apply position tie-breaker (top-left preference) if needed
    if len(max_count_candidates) == 1:
        # Only one candidate remains
        selected_candidate = max_count_candidates[0]
    else:
        # Find the minimum center row index among tied candidates
        min_r = height # Initialize with a value larger than any possible row index
        for candidate in max_count_candidates:
            if candidate['center_r'] < min_r:
                min_r = candidate['center_r']
        
        # Filter based on minimum row index
        top_row_candidates = [
            cand for cand in max_count_candidates if cand['center_r'] == min_r
        ]

        # Find the minimum center column index among the top-row candidates
        min_c = width # Initialize with a value larger than any possible col index
        selected_candidate = None 
        for candidate in top_row_candidates:
             if candidate['center_c'] < min_c:
                min_c = candidate['center_c']
                selected_candidate = candidate # Update the selected candidate

        # Ensure a candidate was selected (should always happen if top_row_candidates was not empty)
        if selected_candidate is None and top_row_candidates:
             selected_candidate = top_row_candidates[0] # Fallback just in case
        elif selected_candidate is None:
             # This case should not happen if initial valid_candidates list was not empty
             # But handle defensively
             return default_output


    # 4. Return the selected grid as a list of lists
    return selected_candidate['grid'].tolist()