```python
"""
Combine four 4x4 input quadrants into a single 4x4 output grid based on a color priority rule applied pixel-wise.
The 8x8 input grid is divided into four 4x4 quadrants: Top-Left (TL), Top-Right (TR), Bottom-Left (BL), and Bottom-Right (BR).
For each position (r, c) in the 4x4 output grid, the color is determined by looking at the colors at the same position (r, c) within each of the four input quadrants.
The output color is chosen based on the following priority order if multiple non-white colors are present: Gray (5) > Magenta (6) > Maroon (9) > Yellow (4).
If all four corresponding input pixels are white (0), the output pixel is also white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an 8x8 input grid into a 4x4 output grid by overlaying four quadrants
    based on a color priority rule.
    """
    # Ensure input is a numpy array
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape

    # Calculate the dimensions of the quadrants and the output grid
    output_height = input_height // 2
    output_width = input_width // 2

    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Define the quadrants
    # Top-Left (TL): rows 0 to output_height-1, cols 0 to output_width-1
    tl_quadrant = input_grid[0:output_height, 0:output_width]
    # Top-Right (TR): rows 0 to output_height-1, cols output_width to input_width-1
    tr_quadrant = input_grid[0:output_height, output_width:input_width]
    # Bottom-Left (BL): rows output_height to input_height-1, cols 0 to output_width-1
    bl_quadrant = input_grid[output_height:input_height, 0:output_width]
    # Bottom-Right (BR): rows output_height to input_height-1, cols output_width to input_width-1
    br_quadrant = input_grid[output_height:input_height, output_width:input_width]

    # Define the color priority list (highest to lowest)
    priority_colors = [5, 6, 9, 4] # Gray, Magenta, Maroon, Yellow

    # Iterate through each cell of the output grid
    for r in range(output_height):
        for c in range(output_width):
            # Get the colors from the corresponding positions in the four quadrants
            colors_at_pos = [
                tl_quadrant[r, c],
                tr_quadrant[r, c],
                bl_quadrant[r, c],
                br_quadrant[r, c]
            ]

            # Determine the output color based on priority
            output_color = 0 # Default to white
            for color in priority_colors:
                if color in colors_at_pos:
                    output_color = color
                    break # Stop once the highest priority color is found

            # Assign the determined color to the output grid
            output_grid[r, c] = output_color

    return output_grid.tolist() # Return as a list of lists as per ARC format
```