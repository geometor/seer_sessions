```python
import numpy as np

"""
Identify the reflection axis (a straight line of blue pixels, either horizontal or vertical).
Identify source pixels (pixels that are not white (0) and not blue (1)).
Create an output grid initialized as a copy of the input grid.
For each source pixel:
  Calculate its reflection coordinates across the blue line axis.
  Determine the swapped color based on the pairs: 
    Red(2) <-> Green(3), Azure(8) <-> Yellow(4), Gray(5) <-> Magenta(6).
  Place the swapped color at the calculated reflection coordinates in the output grid.
The original source pixels and the blue line remain unchanged.
"""

def transform(input_grid):
    """
    Reflects non-white, non-blue pixels across a blue line, swapping specific colors.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_array)
    height, width = input_array.shape

    line_orientation = None
    line_index = -1

    # Find horizontal blue line
    for r in range(height):
        if np.all(input_array[r, :] == 1):
            line_orientation = 'h'
            line_index = r
            break

    # Find vertical blue line if no horizontal one was found
    if line_orientation is None:
        for c in range(width):
            if np.all(input_array[:, c] == 1):
                line_orientation = 'v'
                line_index = c
                break

    # Define the color swap mapping
    color_swap_map = {
        2: 3, 3: 2,  # Red <-> Green
        8: 4, 4: 8,  # Azure <-> Yellow
        5: 6, 6: 5   # Gray <-> Magenta
        # Other colors map to themselves (though only the above are expected based on examples)
    }

    # Iterate through each pixel in the input grid
    for r in range(height):
        for c in range(width):
            original_color = input_array[r, c]

            # Check if the pixel is a source pixel (not white and not blue)
            if original_color != 0 and original_color != 1:
                
                # Calculate reflection coordinates
                ref_r, ref_c = -1, -1
                if line_orientation == 'h':
                    # Reflect vertically across the horizontal line
                    ref_r = line_index + (line_index - r)
                    ref_c = c
                elif line_orientation == 'v':
                    # Reflect horizontally across the vertical line
                    ref_r = r
                    ref_c = line_index + (line_index - c)
                
                # Get the swapped color for the reflection
                swapped_color = color_swap_map.get(original_color, original_color) # Default to original if not in map

                # Check if the reflected coordinates are within the grid bounds
                if 0 <= ref_r < height and 0 <= ref_c < width:
                    # Place the swapped color at the reflected position in the output grid
                    output_grid[ref_r, ref_c] = swapped_color

    # Convert the numpy array back to a list of lists before returning
    return output_grid.tolist()
```