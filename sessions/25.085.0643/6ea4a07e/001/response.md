```python
"""
Transforms an input grid by swapping its two colors and applying a specific color mapping.

1. Identifies the unique non-white color (input_color) in the input grid.
2. Determines the corresponding output color (output_color) based on a predefined mapping:
   - Gray (5) maps to Yellow (4).
   - Azure (8) maps to Red (2).
   - Green (3) maps to Blue (1).
3. Creates an output grid of the same dimensions.
4. Iterates through each pixel of the input grid:
   - If the input pixel is the input_color, the corresponding output pixel is set to white (0).
   - If the input pixel is white (0), the corresponding output pixel is set to the output_color.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the color swap and mapping transformation to the input grid.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Initialize the output grid as a numpy array of the same shape, filled with zeros
    output_array = np.zeros_like(input_array)

    # --- Identify the unique non-white input color ---
    input_color = 0
    unique_colors = np.unique(input_array)
    for color in unique_colors:
        if color != 0:
            input_color = color
            break # Found the non-white color

    # Handle edge case where input is all white (though not present in examples)
    if input_color == 0:
        return input_grid # Or return an all-zero grid? Based on examples, only two colors exist.

    # --- Determine the output color based on the input color mapping ---
    output_color = 0 # Default or error value
    if input_color == 5: # Gray
        output_color = 4 # Yellow
    elif input_color == 8: # Azure
        output_color = 2 # Red
    elif input_color == 3: # Green
        output_color = 1 # Blue
    # Add error handling if an unexpected input color is found
    # else:
    #     print(f"Warning: Unexpected input color {input_color}")

    # --- Apply the pixel-wise transformation ---
    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # If the pixel color is the input_color, change it to white (0) in the output grid.
            if input_array[r, c] == input_color:
                output_array[r, c] = 0
            # If the pixel color is white (0), change it to the output_color in the output grid.
            elif input_array[r, c] == 0:
                output_array[r, c] = output_color

    # Convert the numpy array back to a list of lists for the expected output format
    output_grid = output_array.tolist()

    return output_grid
```