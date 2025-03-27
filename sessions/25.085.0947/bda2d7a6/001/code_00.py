import numpy as np

"""
Identifies concentric rectangular layers in the input grid based on color changes starting from the boundary inwards.
Determines the number of layers (N).
Reassigns the colors of these layers based on whether N is odd or even, preserving the shape and position of the layers.

If N is odd:
- The color of the innermost layer (Layer N) moves to the outermost layer (Layer 1).
- The color of each other layer k (from 1 to N-1) moves to the next inner layer (Layer k+1).

If N is even:
- The color of the second-to-innermost layer (Layer N-1) moves to both the outermost layer (Layer 1) and the innermost layer (Layer N).
- The color of each other layer k (from 1 to N-2) moves to the next inner layer (Layer k+1).

The output grid is constructed by filling the layers with their newly assigned colors.
"""

def get_layers(input_grid):
    """
    Identifies the colors and starting depths of concentric layers.

    Args:
        input_grid (np.ndarray): The input grid.

    Returns:
        tuple: A tuple containing:
            - list: layer_colors (colors of layers from outermost to innermost)
            - list: layer_start_depths (depths where each layer starts)
    """
    grid_h, grid_w = input_grid.shape
    layer_colors = []
    layer_start_depths = []
    max_depth = (min(grid_h, grid_w) + 1) // 2

    for depth in range(max_depth):
        # Check corners at the current depth
        # Need to handle cases where grid is thin (e.g., 1xN or Nx1)
        if depth >= grid_h or depth >= grid_w:
            break # Should not happen with max_depth calculation, but for safety

        current_color = input_grid[depth, depth]

        # If it's the first layer or the color is different from the previous layer
        if not layer_colors or current_color != layer_colors[-1]:
            layer_colors.append(current_color)
            layer_start_depths.append(depth)
        # Optional: If the color is the same as the previous layer, it just means the layer continues.
        # We only record the start of a new color band.

    # Handle potential edge case where the very center might be a new color
    # This is usually covered by the loop, but consider a 1x1 grid or odd dimensions
    if max_depth > 0 and len(layer_colors) > 0:
         center_r, center_c = (grid_h - 1) // 2, (grid_w - 1) // 2
         center_color = input_grid[center_r, center_c]
         center_depth = min(center_r, center_c, grid_h - 1 - center_r, grid_w - 1 - center_c)
         # If the center pixel belongs to a depth >= the last recorded start depth
         # AND its color is different from the last recorded color, it might indicate
         # a final innermost layer missed if the check path didn't hit it exactly.
         # This requires careful thought, but the `(d,d)` check usually suffices for squares/rectangles.
         # Let's stick to the `(d,d)` check for now as it worked for the examples.


    return layer_colors, layer_start_depths


def transform(input_grid):
    """
    Applies the layer color transformation rule to the input grid.
    """
    input_grid = np.array(input_grid)
    grid_h, grid_w = input_grid.shape

    # 1. Identify concentric layers and their colors/depths
    input_colors, layer_start_depths = get_layers(input_grid)
    n_layers = len(input_colors)

    if n_layers == 0: # Should not happen for valid ARC tasks
        return input_grid.tolist()
    if n_layers == 1: # Only one color, no transformation needed
         return input_grid.tolist()

    # 2. Determine output layer colors based on N (number of layers)
    output_colors = [0] * n_layers # Initialize with placeholder

    if n_layers % 2 != 0: # N is odd
        # Output Layer 1 color = Input Layer N color
        output_colors[0] = input_colors[n_layers - 1]
        # Output Layer k color = Input Layer (k-1) color, for k = 2 to N (index 1 to N-1)
        for k in range(1, n_layers):
            output_colors[k] = input_colors[k - 1]
    else: # N is even
        # Check if N >= 2 before accessing N-2
        if n_layers >= 2:
             # Output Layer 1 color = Input Layer (N-1) color
             output_colors[0] = input_colors[n_layers - 2]
             # Output Layer N color = Input Layer (N-1) color
             output_colors[n_layers - 1] = input_colors[n_layers - 2]
        # Output Layer k color = Input Layer (k-1) color, for k = 2 to N-1 (index 1 to N-2)
        for k in range(1, n_layers - 1):
            output_colors[k] = input_colors[k - 1]

    # 3. Construct Output Grid
    output_grid = np.zeros_like(input_grid) # Initialize with 0s

    # Iterate through each pixel and determine its layer and assign the output color
    for r in range(grid_h):
        for c in range(grid_w):
            # Calculate the depth of the pixel (minimum distance to any edge)
            pixel_depth = min(r, c, grid_h - 1 - r, grid_w - 1 - c)

            # Find which layer this pixel belongs to based on depth
            layer_idx = 0
            # Iterate backwards through start depths to find the correct layer index
            for i in range(n_layers - 1, -1, -1):
                if pixel_depth >= layer_start_depths[i]:
                    layer_idx = i
                    break

            # Assign the corresponding output color to the pixel
            output_grid[r, c] = output_colors[layer_idx]

    return output_grid.tolist()