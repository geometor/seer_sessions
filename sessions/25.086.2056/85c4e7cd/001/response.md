```python
import numpy as np

"""
The transformation identifies concentric rectangular layers within the input grid and inverts the order of their colors.

1. Determine Layers: For each pixel in the grid, calculate its "layer index" based on its minimum distance to any of the four borders (top, bottom, left, right). The outermost pixels form layer 0, the next pixels inward form layer 1, and so on.
2. Extract Input Layer Colors: Find the color associated with each layer index in the input grid. Store these colors, ordered from the outermost layer (index 0) to the innermost layer (index N).
3. Map Output Layer Colors: Reverse the order of the extracted layer colors. The color for output layer `i` will be the color that was originally in input layer `N-i`.
4. Construct Output Grid: Create a new grid of the same dimensions as the input. For each pixel, calculate its layer index `i` and assign it the corresponding color determined in step 3 (the color from input layer `N-i`).
"""

def get_layer_index(r, c, height, width):
  """Calculates the layer index for a pixel at (r, c)."""
  return min(r, c, height - 1 - r, width - 1 - c)

def transform(input_grid):
    """
    Transforms the input grid by inverting the colors of its concentric layers.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output grid as a copy of the input
    output_np = np.copy(input_np)

    # Determine the maximum layer index (N)
    # This corresponds to the innermost layer
    max_layer_index = (min(height, width) - 1) // 2

    # Extract the color for each layer in the input grid
    input_layer_colors = {}
    for i in range(max_layer_index + 1):
      # Pixel (i, i) is guaranteed to be in layer i
      input_layer_colors[i] = input_np[i, i]

    # Create the mapping for output layer colors by inverting the input order
    output_layer_colors = {}
    for i in range(max_layer_index + 1):
        output_layer_colors[i] = input_layer_colors[max_layer_index - i]

    # Populate the output grid based on the layer color mapping
    for r in range(height):
        for c in range(width):
            # Find the layer index for the current pixel
            layer_idx = get_layer_index(r, c, height, width)
            # Assign the corresponding output color to the pixel
            output_np[r, c] = output_layer_colors[layer_idx]

    # Convert the result back to a list of lists
    output_grid = output_np.tolist()
    return output_grid
```