"""
Processes the input grid column by column.
For each column:
1. Identify all unique non-background colors and their counts.
2. If exactly two unique non-background colors are present:
   a. Determine the 'primary_color' (the one with the higher count).
   b. Determine the 'trigger_color' (the one with the lower count).
   c. Find all row indices where the 'trigger_color' appears ('trigger_rows').
   d. For each 'row_trigger' in 'trigger_rows':
      i. Iterate through all rows 'row' above 'row_trigger' (0 <= row < row_trigger).
      ii. If the pixel at input_grid[row, col] is the 'primary_color', change the corresponding pixel in the output_grid to the 'trigger_color'.
3. If the number of unique non-background colors is not exactly two, the column remains unchanged.
The final modified grid is returned.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each column
    for col in range(width):
        # Extract the current column
        current_column = input_grid[:, col]

        # Find unique non-background colors and their counts in this column
        non_background_pixels = current_column[current_column != 0]
        color_counts = Counter(non_background_pixels)
        unique_colors = list(color_counts.keys())

        # Check if there are exactly two unique non-background colors
        if len(unique_colors) == 2:
            # Determine primary and trigger colors based on counts
            color1, count1 = unique_colors[0], color_counts[unique_colors[0]]
            color2, count2 = unique_colors[1], color_counts[unique_colors[1]]

            # Handle cases where counts might be equal (although not seen in examples)
            # Based on examples, trigger is less frequent. If equal, skip? Let's assume counts differ for now.
            if count1 == count2:
                 continue # Skip this column if counts are equal as rule is ambiguous

            if count1 > count2:
                primary_color = color1
                trigger_color = color2
            else:
                primary_color = color2
                trigger_color = color1

            # Find all row indices where the trigger_color appears
            trigger_rows = np.where(current_column == trigger_color)[0]

            # For each trigger pixel, modify primary pixels above it in the output grid
            for row_trigger in trigger_rows:
                # Iterate through rows above the trigger row
                for row in range(row_trigger):
                    # Check if the pixel in the *input* grid is the primary color
                    if input_grid[row, col] == primary_color:
                        # Change the corresponding pixel in the *output* grid to the trigger color
                        output_grid[row, col] = trigger_color

        # If not exactly two unique non-background colors, do nothing (column remains as copied)

    return output_grid