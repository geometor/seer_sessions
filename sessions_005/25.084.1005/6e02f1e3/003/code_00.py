"""
Transforms a 3x3 input grid into a 3x3 output grid based on the set of unique colors present in the input. The output grid consists only of white (0) and gray (5) pixels arranged in specific patterns.

1. Identify the set of unique colors in the 3x3 input grid.
2. Create a 3x3 output grid, initialized to all white (0).
3. Apply transformation rules based on the unique color set:
    a. If the input contains only Green (3) OR only Yellow (4): Set the top row of the output to gray (5).
    b. Else if the input contains both Red (2) AND Yellow (4): Set the anti-diagonal (top-right to bottom-left) of the output to gray (5).
    c. Else if the input contains Red (2) (and implicitly not Yellow, due to rule 'b'): Set the main diagonal (top-left to bottom-right) of the output to gray (5).
    d. Else if the input has more than one color (polychromatic) and does NOT contain Red (2): Set the main diagonal of the output to gray (5).
    e. Else (input is monochromatic with a color other than Green or Yellow): Set the entire output grid to gray (5).
4. Return the transformed 3x3 output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule based on the unique colors in the input grid.

    Args:
        input_grid (list of lists): A 3x3 grid represented as a list of lists of integers.

    Returns:
        list of lists: The transformed 3x3 grid.
    """
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Ensure the input is 3x3 as observed in examples
    if height != 3 or width != 3:
        # In a real scenario, might raise an error or handle differently.
        # For this task, we assume valid 3x3 input based on examples.
        print("Warning: Input grid is not 3x3. Behavior might be unpredictable.")
        # Fallback: return a default grid or raise error? Let's try default for now.
        return np.zeros((3, 3), dtype=int).tolist() 

    # 1. Identify unique colors
    unique_colors = set(np.unique(input_array))
    num_unique_colors = len(unique_colors)
    is_monochromatic = num_unique_colors == 1

    # 2. Initialize output grid (default to white)
    output_array = np.zeros((height, width), dtype=int)

    # 3. Apply transformation rules based on unique color set
    if is_monochromatic:
        mono_color = list(unique_colors)[0]
        # 3a. Monochromatic Green or Yellow
        if mono_color == 3 or mono_color == 4:
            output_array[0, :] = 5 # Set top row to gray
        # 3e. Other Monochromatic
        else:
            output_array[:, :] = 5 # Set all to gray
    else: # Polychromatic cases
        contains_red = 2 in unique_colors
        contains_yellow = 4 in unique_colors

        # 3b. Contains Red AND Yellow
        if contains_red and contains_yellow:
            # Set anti-diagonal to gray
            for i in range(height):
                output_array[i, width - 1 - i] = 5
        # 3c. Contains Red (but not Yellow, based on previous condition)
        elif contains_red:
            # Set main diagonal to gray
            for i in range(height):
                output_array[i, i] = 5
        # 3d. Polychromatic, Does NOT contain Red
        elif not contains_red:
             # Set main diagonal to gray
            for i in range(height):
                output_array[i, i] = 5
        # Note: This 'elif not contains_red' implicitly covers Example 4 ({3, 4})
        # which does not contain red and results in the main diagonal.

    # 4. Return the generated output grid as a list of lists
    return output_array.tolist()
