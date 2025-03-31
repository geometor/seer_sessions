```python
import numpy as np
from collections import Counter
import sys

# using sys.path.insert(0, '../') may be necessary if running from notebook
# from util import find_objects # Assuming a utility function for object detection exists if needed

# Color constants just for reference if needed, not strictly required by the logic
WHITE = 0
BLUE = 1
RED = 2
GREEN = 3
YELLOW = 4
GRAY = 5
MAGENTA = 6
ORANGE = 7
AZURE = 8
MAROON = 9


def find_divider_row(grid):
    """
    Finds the index of the last row composed entirely of gray pixels (5) 
    that acts as a divider near the top of the grid.
    Searches from the top down.
    """
    height, width = grid.shape
    last_gray_row = -1
    # Search downwards for the divider row
    for r in range(height // 2): # Limit search to upper half for efficiency
        if np.all(grid[r] == GRAY):
            last_gray_row = r
        else:
            # If we previously found a gray row and this one isn't gray,
            # the previous one was the last one in the sequence.
            if last_gray_row != -1:
                # Ensure we are not just looking at the top border if it's gray
                # We need a non-gray row *after* the gray row sequence.
                 return last_gray_row
                 
    # If the loop completes and the last row checked was gray, it might be the divider
    # This handles cases where the gray divider is at the end of the search range
    # or if the grid structure is unusual. Relying on example structure (row 5) if ambiguous.
    if last_gray_row != -1:
        return last_gray_row
        
    # Fallback based on consistent example structure if no clear divider found
    if height > 5 and np.all(grid[5] == GRAY):
        return 5
        
    # Indicate failure if no suitable row is found
    return -1


def find_target_columns(grid, key_section_end_row):
    """
    Finds the column indices containing non-white/non-gray colors 
    within the key section (between the top and bottom gray borders).
    """
    height, width = grid.shape
    target_columns = set()
    # Key section internal rows are assumed to be between the top border (row 0)
    # and the bottom border (key_section_end_row). Iterate row 1 to end_row-1.
    # Iterate columns 1 to width-2 to avoid grid borders if they are gray.
    for r in range(1, key_section_end_row):
        for c in range(1, width - 1): 
             pixel_color = grid[r, c]
             # Check if the color is one of the 'key' colors (not white, not gray)
             if pixel_color != WHITE and pixel_color != GRAY:
                 target_columns.add(c)
    return sorted(list(target_columns)) # Return sorted list for consistency


def find_most_frequent_data_color(grid_section):
    """
    Finds the most frequent color in the given grid section, excluding white (0).
    """
    # Flatten the grid section into a 1D array
    pixels = grid_section.flatten()
    
    # Count occurrences of each color, excluding white (0)
    color_counts = Counter(p for p in pixels if p != WHITE)
    
    # Find the color with the highest count
    if not color_counts:
        # Handle case where the section is all white or empty
        return -1 # Or another indicator of no data color found
        
    most_common = color_counts.most_common(1)
    return most_common[0][0]


def transform(input_grid):
    """
    Transforms the input grid based on rules derived from a 'key' section at the top.
    1. Identifies a 'key' section bordered by gray (5) rows at the top.
    2. Finds the row index ('divider_row_index') of the bottom gray border of the key section.
    3. Extracts 'target column' indices from unique non-white/non-gray colors within the key section.
    4. Identifies the 'data' section below the key section's bottom border.
    5. Determines the most frequent color ('color_to_change') in the data section (excluding white).
    6. Creates the output grid by copying the data section.
    7. Changes pixels in the output grid from 'color_to_change' to azure (8) if they fall 
       within one of the target columns.
    """
    
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. & 2. Identify key section boundary
    divider_row_index = find_divider_row(input_np)
    
    # Handle error case where divider isn't found properly
    if divider_row_index == -1 or divider_row_index >= height - 1:
        # If no divider or divider is the last row, cannot proceed logically.
        # Return input or raise error, depending on desired behavior for invalid input.
        # Based on task structure, a valid divider is expected. Let's assume error or return copy.
        # For now, returning a copy might be safer in ARC context.
        print(f"Warning: Could not reliably determine divider row. Found index: {divider_row_index}")
        # Attempting fallback based on examples
        if height > 5 and np.all(input_np[5] == GRAY):
             divider_row_index = 5
        else:
             # If fallback fails, return input grid as is.
             return input_grid # Or raise ValueError("Divider row not found")

    # 3. Extract target columns from the key section
    target_columns = find_target_columns(input_np, divider_row_index)

    # 4. Identify and extract the data section
    # Data section starts the row *after* the divider
    data_section = input_np[divider_row_index + 1:, :]

    # Check if data_section is empty
    if data_section.size == 0:
        # Handle case where there's no data below the divider
        return [] # Return empty grid

    # 5. Determine the color to change in the data section
    color_to_change = find_most_frequent_data_color(data_section)
    
    if color_to_change == -1:
        # Handle case where data section is all white
        return data_section.tolist() # Return data section as is

    # 6. Initialize output grid as a copy of the data section
    output_grid = data_section.copy()
    output_height, output_width = output_grid.shape

    # 7. Apply the transformation rule
    for r in range(output_height):
        for c in range(output_width):
            # Check if the column is a target column
            if c in target_columns:
                # Check if the original color in the data section was the one to change
                if data_section[r, c] == color_to_change:
                    # Change the color to azure (8) in the output grid
                    output_grid[r, c] = AZURE
            # Pixels not matching the condition retain their original color from the copy

    return output_grid.tolist() # Convert back to list of lists for standard ARC format
```