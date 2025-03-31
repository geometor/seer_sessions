"""
Transformation rule:
1. Identify the most frequent color in the input grid (the background color).
2. Define a fixed mapping for specific non-background colors to target colors:
   - Red (2) -> Magenta (6)
   - Magenta (6) -> Gray (5)
   - Gray (5) -> Red (2)
   - Yellow (4) -> Green (3)
   - Green (3) -> Maroon (9)
   - Maroon (9) -> Yellow (4)
3. Iterate through each column of the input grid.
4. For each column, determine the set of unique colors present.
5. Check if the column contains exactly two unique colors: the background color and one other color ('O').
6. If the condition in step 5 is met AND the 'other color' ('O') is one of the keys in the fixed mapping, then:
   - Find the corresponding target color ('T') from the mapping.
   - Change all pixels in that column that have the background color to the target color ('T').
7. If the condition in step 5 is not met, or if the 'other color' is not in the mapping, the column remains unchanged.
8. Pixels that are not the background color always remain unchanged.
9. The output grid has the same dimensions as the input grid.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Applies the transformation rule based on column context and color mapping.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = input_np.copy() # Initialize output grid as a copy
    height, width = input_np.shape

    # 1. Identify Background Color
    all_pixels = input_np.flatten()
    if not all_pixels.size: # Handle empty grid case
        return input_grid 
        
    pixel_counts = Counter(all_pixels)
    # Find the color with the highest frequency
    # If there's a tie, the first one encountered by most_common will be chosen.
    # In case the grid contains only one color, that will be the background.
    background_color = pixel_counts.most_common(1)[0][0]

    # 2. Define Mapping
    color_map = {
        2: 6,  # Red -> Magenta
        6: 5,  # Magenta -> Gray
        5: 2,  # Gray -> Red
        4: 3,  # Yellow -> Green
        3: 9,  # Green -> Maroon
        9: 4   # Maroon -> Yellow
    }

    # 3. Process Columns
    for j in range(width):
        column = input_np[:, j]
        
        # 4. Determine unique colors in the column
        unique_colors = set(np.unique(column))

        # 5. Check if the column contains exactly two unique colors: background and one other
        if len(unique_colors) == 2 and background_color in unique_colors:
            # Find the 'other color'
            other_color = list(unique_colors - {background_color})[0]

            # 6. Check if the 'other color' is in the mapping
            if other_color in color_map:
                target_color = color_map[other_color]
                
                # Apply transformation within the column in the output grid
                for i in range(height):
                    if input_np[i, j] == background_color:
                        output_np[i, j] = target_color
                        
        # 7. If conditions are not met, the column in output_np remains as copied initially.

    # Convert numpy array back to list of lists for the final output
    return output_np.tolist()
