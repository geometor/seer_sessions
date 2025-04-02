import numpy as np
from collections import Counter
import collections

"""
Analyzes the input grid to find the most frequent pixel color, designated as the background_color.
Searches the input grid for all unique subgrids (patterns) that appear more than once (repeating patterns).
Filters these repeating patterns to exclude any pattern that is monochromatic (consists of only one color).
From the remaining set of non-monochromatic repeating patterns, selects the pattern that does *not* contain any pixels of the background_color identified initially.
Returns a single instance of the selected pattern. If multiple patterns fit the criteria, the one with the smallest area (height * width) is chosen. If areas are equal, the one with the smaller height is chosen.
"""

def find_most_frequent_color(grid_np):
    """
    Finds the most frequent color in a numpy grid.
    Returns -1 if the grid is empty.
    """
    if grid_np.size == 0:
        return -1
    colors, counts = np.unique(grid_np, return_counts=True)
    # If there's a tie for the most frequent color, np.argmax returns the first one.
    # This seems acceptable based on the task description.
    return colors[np.argmax(counts)]

def is_monochromatic(grid_np):
    """
    Checks if a numpy grid contains only one unique color value.
    Considers empty grids or grids with only one pixel as monochromatic.
    """
    return np.unique(grid_np).size <= 1

def transform(input_grid):
    """
    Identifies a non-monochromatic, repeating pattern in the input grid
    that does not contain the grid's most frequent color (background color).
    If multiple such patterns exist, returns the smallest one based on area, then height.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the identified pattern, or an empty list
        if no such pattern is found.
    """
    # Convert input list of lists to a numpy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    H, W = grid_np.shape

    # Handle edge case of empty input grid
    if H == 0 or W == 0:
        return []

    # Step 1: Identify the background color (most frequent color)
    background_color = find_most_frequent_color(grid_np)
    # Handle case where input grid was empty or finding color failed
    if background_color == -1:
        return []

    # Step 2: Find all unique subgrids and count their occurrences.
    # Store patterns as tuples (hashable key) mapped to their count and np array.
    pattern_info = collections.defaultdict(lambda: {'count': 0, 'array': None})

    # Iterate through all possible pattern heights (ph) and widths (pw)
    for ph in range(1, H + 1):
        for pw in range(1, W + 1):
            # Iterate through all possible top-left starting positions (r, c)
            for r in range(H - ph + 1):
                for c in range(W - pw + 1):
                    # Extract the subgrid
                    subgrid_np = grid_np[r:r+ph, c:c+pw]
                    # Convert the numpy subgrid to a tuple of tuples for use as a dictionary key
                    subgrid_tuple = tuple(map(tuple, subgrid_np))
                    
                    # Increment count for this pattern
                    pattern_info[subgrid_tuple]['count'] += 1
                    # Store the numpy array representation if not already stored
                    if pattern_info[subgrid_tuple]['array'] is None:
                         pattern_info[subgrid_tuple]['array'] = subgrid_np

    # Step 3 & 4: Filter patterns to find candidates meeting criteria
    candidate_patterns = []
    for pattern_data in pattern_info.values():
        count = pattern_data['count']
        pattern_np = pattern_data['array']

        # Check if pattern repeats (appears more than once)
        if count > 1:
            # Check if pattern is non-monochromatic
            if not is_monochromatic(pattern_np):
                # Check if pattern contains the background color
                # np.unique returns sorted unique elements
                if background_color not in np.unique(pattern_np):
                    # This pattern meets all criteria, add it to candidates
                    candidate_patterns.append(pattern_np)

    # Step 5: Select the final pattern from candidates and return it
    if not candidate_patterns:
        # No pattern found matching all criteria
        return []
    else:
        # If multiple candidates exist, select the 'best' one.
        # Prioritize smallest area (height * width), then smallest height.
        candidate_patterns.sort(key=lambda p: (p.shape[0] * p.shape[1], p.shape[0]))
        # Return the chosen pattern converted back to list of lists format
        return candidate_patterns[0].tolist()
