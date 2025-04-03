```python
import copy

"""
Transforms a 1D input grid by identifying contiguous horizontal blocks of 
green (3) pixels and replacing them with a new color based on the length 
of the block.

- Blocks of length 1 are replaced with yellow (4).
- Blocks of length 2 are replaced with red (2).
- Blocks of length 3 are replaced with maroon (9).
- All other pixels, specifically white (0), remain unchanged.
"""

def transform(input_grid):
    """
    Applies the color transformation based on green block length.

    Args:
        input_grid (list): A list of integers representing the 1D input grid.

    Returns:
        list: A list of integers representing the transformed 1D output grid.
    """
    # Initialize the output grid as a copy of the input
    output_grid = list(input_grid) 
    n = len(input_grid)
    i = 0

    # Define the color mapping based on length
    color_map = {
        1: 4,  # yellow
        2: 2,  # red
        3: 9   # maroon
    }

    # Iterate through the input grid
    while i < n:
        # Check if the current pixel is green (3)
        if input_grid[i] == 3:
            # Found the start of a potential green block
            start_index = i
            current_length = 0
            # Measure the length of the contiguous green block
            while i < n and input_grid[i] == 3:
                current_length += 1
                i += 1
            
            # Determine the replacement color based on the length
            # Use get with a default value (e.g., original color 3) 
            # if a length doesn't match the map, although based on examples,
            # only lengths 1, 2, 3 occur. If unmapped lengths should default
            # to something else (like 0 or keep 3), adjust accordingly.
            # Here, we assume only lengths 1, 2, 3 are relevant as per examples.
            replacement_color = color_map.get(current_length)

            # If a valid replacement color is found (i.e., length was 1, 2, or 3)
            if replacement_color is not None:
                # Update the corresponding pixels in the output grid
                for j in range(start_index, i):
                    output_grid[j] = replacement_color
            # If the length wasn't in the map, the original green pixels 
            # remain in the output_grid (because it was initialized as a copy).
            # We can explicitly handle this if needed, e.g., change to white (0).
            # Given the examples, this 'else' case doesn't seem necessary.
            
            # The loop condition i < n and the inner loop's i += 1 handle moving
            # the index past the processed block, so no extra increment needed here.
        else:
            # If the pixel is not green, just move to the next pixel
            i += 1
            
    return output_grid
```