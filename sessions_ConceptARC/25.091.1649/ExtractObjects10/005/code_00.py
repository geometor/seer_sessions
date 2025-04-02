import numpy as np
from collections import defaultdict

"""
Determines the most frequent color in the input grid (background_color).
Identifies all unique rectangular subgrids (patterns) and counts their occurrences.
Filters these patterns to keep only those that:
1. Appear more than once (are repeating).
2. Are not monochromatic (contain more than one color).
3. Do not contain the background_color.
Assumes exactly one pattern meets these criteria and returns it.
"""

def find_most_frequent_color(grid_np):
    """
    Finds the most frequent color in a numpy grid.
    Handles empty grid case.
    In case of a tie, returns the color with the lowest numerical value among the most frequent ones
    due to how np.unique and np.argmax work.
    """
    if grid_np.size == 0:
        return -1 # Indicate error or empty grid
    colors, counts = np.unique(grid_np, return_counts=True)
    if counts.size == 0:
         return -1 # Should not happen if grid_np.size > 0, but safe check
    return colors[np.argmax(counts)]

def is_monochromatic(grid_np):
    """
    Checks if a numpy grid contains only one unique color value.
    Considers empty grids or grids with only one pixel as monochromatic.
    """
    return np.unique(grid_np).size <= 1

def transform(input_grid):
    """
    Identifies and returns a unique repeating, non-monochromatic pattern
    that does not contain the input grid's most frequent color.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the identified pattern, or an empty list
        if no such pattern is found or the input is invalid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    try:
        grid_np = np.array(input_grid, dtype=int)
    except ValueError:
        # Handle potentially inconsistent row lengths or non-integer data
        return [] 

    H, W = grid_np.shape

    # Handle edge case of empty input grid
    if H == 0 or W == 0:
        return []

    # Step 1: Determine the background color (most frequent color)
    background_color = find_most_frequent_color(grid_np)
    if background_color == -1:
        # This case implies the grid was effectively empty after conversion or contained no elements
        return []

    # Step 2 & 3: Identify all unique subgrids and count their occurrences.
    # Store patterns using their byte representation as a key for efficiency and hashability.
    pattern_info = defaultdict(lambda: {'count': 0, 'array': None})

    # Iterate through all possible pattern heights (ph) and widths (pw)
    for ph in range(1, H + 1):
        for pw in range(1, W + 1):
            # Iterate through all possible top-left starting positions (r, c)
            for r in range(H - ph + 1):
                for c in range(W - pw + 1):
                    # Extract the subgrid
                    subgrid_np = grid_np[r:r+ph, c:c+pw]
                    # Use the byte representation of the array as the key
                    subgrid_key = subgrid_np.tobytes() 

                    # Increment count for this pattern
                    pattern_info[subgrid_key]['count'] += 1
                    # Store the numpy array representation only once
                    if pattern_info[subgrid_key]['array'] is None:
                         pattern_info[subgrid_key]['array'] = subgrid_np

    # Step 4: Filter patterns to find candidates meeting criteria
    candidate_patterns = []
    for pattern_data in pattern_info.values():
        # Ensure pattern data is valid (array was stored)
        if pattern_data['array'] is None:
            continue
            
        count = pattern_data['count']
        pattern_np = pattern_data['array']

        # Check criteria:
        # a. Appears more than once
        if count > 1:
            # b. Is not monochromatic
            if not is_monochromatic(pattern_np):
                # c. Does not contain the background color
                if background_color not in np.unique(pattern_np):
                    # This pattern meets all criteria, add it to candidates
                    candidate_patterns.append(pattern_np)

    # Step 5: Select and return the assumed unique pattern
    if len(candidate_patterns) == 1:
        # Found exactly one pattern meeting all criteria
        # Return the chosen pattern converted back to list of lists format
        return candidate_patterns[0].tolist()
    elif len(candidate_patterns) > 1:
        # If multiple candidates exist (unexpected based on examples),
        # default to returning the one with the smallest area, then smallest height as a fallback tie-breaker.
        # This matches the initial guess before uniqueness was assumed.
        # You might want to refine this logic if the task allows multiple valid outputs.
        candidate_patterns.sort(key=lambda p: (p.shape[0] * p.shape[1], p.shape[0]))
        print("Warning: Multiple candidate patterns found. Returning the smallest one.")
        return candidate_patterns[0].tolist()
    else:
        # No pattern found matching all criteria
        return []