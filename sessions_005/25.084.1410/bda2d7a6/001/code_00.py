import numpy as np

"""
Transforms the input grid based on nested layer color swapping.
1. Identify the colors of the three outermost nested layers using fixed indices:
   C1 (border color at [0,0]), C2 (next layer color at [1,1]), C3 (third layer color at [2,2]).
   This assumes a structure consistent with the training examples where layers are distinct near the top-left corner.
2. Create an output grid.
3. Create a primary mapping: C1 -> C3, C2 -> C1, C3 -> C2.
4. Iterate through each pixel of the input grid:
   a. If the original color is C1, C2, or C3, apply the primary mapping to the corresponding output grid pixel.
   b. If the original color is NOT C1, C2, or C3 (considered 'inner content'):
      i. If the original color is White (0), set the output pixel to White (0).
      ii. Otherwise (original color is not C1/C2/C3 and not White), set the output pixel to C3 (which is the color C1 was mapped to).
"""

def transform(input_grid):
    """
    Applies a color transformation based on swapping colors of nested layers.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.

    Raises:
        ValueError: If the input grid is smaller than 3x3, as the logic relies
                    on indexing up to [2, 2].
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Ensure grid is large enough for the assumed indexing based on examples
    if rows < 3 or cols < 3:
         raise ValueError("Grid is too small (must be at least 3x3) for the assumed layer structure based on examples.")

    # 1. Identify C1, C2, C3 using fixed indices near the top-left corner.
    # This assumes the pattern observed in training examples holds.
    c1 = input_array[0, 0] # Outermost border color
    c2 = input_array[1, 1] # Second layer color
    c3 = input_array[2, 2] # Third layer color

    # Optional: Add checks here if c1, c2, c3 must be distinct, or handle cases
    # where the structure differs, although the current logic might still work
    # if, e.g., c3 happens to be the same as c1 or c2, but the examples don't show this.

    # 2. Create an output grid (initialize by copying input, then modify)
    # Using copy ensures dimensions are correct and non-mapped pixels retain original values temporarily.
    output_array = np.copy(input_array)

    # 3. Define the primary color mapping for the identified layers
    # C1 maps to C3, C2 maps to C1, C3 maps to C2
    layer_color_map = {
        c1: c3,
        c2: c1,
        c3: c2
    }

    # 4. Iterate through each pixel and apply transformations
    for r in range(rows):
        for c in range(cols):
            original_color = input_array[r, c]

            # Check if the pixel's color matches one of the identified layer colors
            if original_color in layer_color_map:
                # a. Apply layer swap mapping
                output_array[r, c] = layer_color_map[original_color]
            else:
                # b. Handle inner content (pixels not matching C1, C2, or C3)
                # i. If the original color is White (0)
                if original_color == 0:
                    output_array[r, c] = 0 # Keep it White (0)
                else:
                    # ii. Otherwise (inner content, not White), map it to C3
                    # (which is the color that C1 was mapped to).
                    output_array[r, c] = c3

    # Convert the final NumPy array back to a list of lists for the required output format
    output_grid = output_array.tolist()
    return output_grid