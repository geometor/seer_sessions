import numpy as np
from collections import Counter

"""
Identify the non-white color (1-9) that appears most frequently in the entire input grid. 
Then, locate the unique 3x3 subgrid within the input that is composed solely of white (0) and this most frequent color. 
Return this 3x3 subgrid as the output.
"""

def find_most_frequent_color(grid):
    """Counts non-white colors and returns the most frequent one."""
    counts = Counter()
    # Flatten the grid and count non-white pixels
    for row in grid:
        for pixel in row:
            if pixel != 0:
                counts[pixel] += 1
    
    # Find the color with the highest count
    if not counts:
        # Handle cases with no non-white colors (though unlikely based on examples)
        return None 
    
    # Find the color with the maximum frequency
    most_frequent = max(counts, key=counts.get)
    return most_frequent

def extract_subgrid(grid, r, c, height=3, width=3):
    """Extracts a subgrid of specified size starting at (r, c)."""
    return [row[c:c+width] for row in grid[r:r+height]]

def is_target_pattern(subgrid, target_color):
    """Checks if a 3x3 subgrid contains only white (0) and the target_color."""
    if len(subgrid) != 3 or any(len(row) != 3 for row in subgrid):
         return False # Ensure it's actually 3x3 before checking colors

    colors_present = set()
    for r in range(3):
        for c in range(3):
             pixel = subgrid[r][c]
             if pixel != 0:
                 colors_present.add(pixel)

    # The pattern should contain the target_color and potentially white (0)
    # It must contain *only* the target_color among non-white colors.
    return colors_present == {target_color} or colors_present == set() # Allows all white, though unlikely pattern target


def transform(input_grid):
    """
    Transforms the input grid by finding the 3x3 pattern associated 
    with the most frequent non-white color.
    """
    
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Count frequencies of non-white colors
    target_color = find_most_frequent_color(input_grid)
    
    if target_color is None:
        # If no non-white colors, return an empty or default grid (e.g., 3x3 white)
        # Based on examples, this shouldn't happen, but good practice.
        # Returning a 3x3 white grid seems plausible if no pattern found.
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]] 

    # 2. Search for the 3x3 pattern containing only white and the target_color
    output_grid = None
    for r in range(height - 2):  # Iterate through possible top-left row indices
        for c in range(width - 2):  # Iterate through possible top-left col indices
            # 3. Extract the 3x3 subgrid
            subgrid = extract_subgrid(input_grid, r, c)
            
            # 4. Check if this subgrid uses the target_color
            # We need to be careful: does the subgrid *define* the pattern or just contain the color?
            # The description implies the pattern is MADE of white and the target color.
            
            colors_in_subgrid = set(np.array(subgrid).flatten())
            
            # Check if the subgrid contains *only* 0 and target_color
            valid_colors = {0, target_color}
            is_correct_pattern = True
            
            # Check if it contains *any* target_color pixel (ruling out all-white subgrids)
            has_target_color = False
            
            for row_idx in range(3):
                for col_idx in range(3):
                    pixel = subgrid[row_idx][col_idx]
                    if pixel not in valid_colors:
                        is_correct_pattern = False
                        break
                    if pixel == target_color:
                        has_target_color = True
                if not is_correct_pattern:
                    break

            if is_correct_pattern and has_target_color:
                output_grid = subgrid
                break  # Found the pattern, stop searching
        if output_grid is not None:
            break

    # If no pattern found (should not happen based on task description), return default
    if output_grid is None:
        # This case implies an issue with assumptions or the input data structure
        # For robustness, maybe return a default or raise an error. Let's return 3x3 white.
         return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    return output_grid