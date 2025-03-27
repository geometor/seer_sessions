```python
import numpy as np
from collections import Counter

def find_most_frequent_color(block):
    """
    Finds the most frequent non-background color in a 2x2 block.
    If there's a tie (two colors appear twice), returns the color
    at the bottom-right corner of the block.

    Args:
        block (np.array): A 2x2 numpy array representing the block.

    Returns:
        int: The selected color.
    """
    pixels = block.flatten().tolist()
    counts = Counter(p for p in pixels if p != 0) # Count non-white colors

    if not counts:
        return 0 # Should not happen based on task description, but handle defensively

    max_freq = 0
    for color in counts:
        if counts[color] > max_freq:
            max_freq = counts[color]

    most_frequent_colors = [color for color, freq in counts.items() if freq == max_freq]

    if len(most_frequent_colors) == 1:
        # Only one most frequent color
        return most_frequent_colors[0]
    else:
        # Tie-breaker: return the bottom-right pixel's color
        return block[1, 1]


def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. The input grid contains six 2x2 blocks of colors.
    2. The output grid is 4x5.
    3. Each 2x2 block in the input maps to a specific pixel in the output.
    4. The color of the output pixel is determined by the most frequent
       non-white color in the corresponding input 2x2 block.
    5. If there is a tie in frequency (two colors appear twice), the color
       of the bottom-right pixel within the 2x2 block is chosen.
    """
    # Convert input list of lists to numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)

    # Initialize the 4x5 output grid with white (0)
    output_grid = np.zeros((4, 5), dtype=int)

    # Define the mapping from input block top-left corners to output pixel coordinates
    mapping = {
        (1, 1): (1, 1),
        (1, 4): (1, 2),
        (1, 7): (1, 3),
        (5, 1): (2, 1),
        (5, 4): (2, 2),
        (5, 7): (2, 3),
    }

    # Process each block
    for (r_in, c_in), (r_out, c_out) in mapping.items():
        # Extract the 2x2 block from the input grid
        block = input_np[r_in:r_in+2, c_in:c_in+2]

        # Find the color based on frequency and tie-breaker rule
        selected_color = find_most_frequent_color(block)

        # Place the selected color into the output grid
        output_grid[r_out, c_out] = selected_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```