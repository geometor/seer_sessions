# 85c4e7cd • 002 • example_4 • investigate_coder

---
```python
"""
The transformation inverts the order of concentric square layers in a grid and applies a specific color mapping within each layer.
"""

import numpy as np

def get_layers(grid):
    """
    Divides the grid into concentric square layers.
    """
    layers = []
    rows, cols = grid.shape
    num_layers = min(rows, cols) // 2
    for i in range(num_layers):
        layer = []
        # Top row
        layer.extend(grid[i, i:cols-i])
        # Right column
        layer.extend(grid[i+1:rows-i-1, cols-i-1])
        # Bottom row
        layer.extend(grid[rows-i-1, i:cols-i][::-1])
        # Left Column
        layer.extend(grid[i+1:rows-i-1, i][::-1])

        layers.append(np.array(layer))
    return layers


def get_layer_mapping(input_layers, output_layers):
    """
    Determines the color mapping for each layer pair.
    """
    mapping = {}
    for i in range(len(input_layers)):
        input_colors = np.unique(input_layers[i])
        output_colors = np.unique(output_layers[i])
        #Simple one-to-one
        layer_map = {}
        for in_color in input_colors:
            #find position of this color
            pos = np.where(input_layers[i] == in_color)[0][0]
            out_color = output_layers[i][pos]
            layer_map[in_color] = out_color
            
        mapping[i] = layer_map
    return mapping

def transform(input_grid):
    """
    Transforms the input grid by inverting layer order and applying a layer-specific color mapping.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    
    input_layers = get_layers(input_grid)

    #Create a dummy output, fill with layers, and get the mapping
    dummy_output = np.zeros_like(input_grid)
    num_layers = len(input_layers)
    for i in range(num_layers):
        # Fill dummy output in reversed order
        layer_index = num_layers - 1 - i
        for r in range(rows):
            for c in range(cols):
                if (
                    (r == layer_index or r == rows - 1 - layer_index) and layer_index <= c <= cols - 1 - layer_index
                ) or (
                    (c == layer_index or c == cols - 1 - layer_index) and layer_index <= r <= rows - 1 - layer_index
                ):
                    dummy_output[r,c] = 1 #Filler value, does not matter

    dummy_layers = get_layers(dummy_output)
    #Reverse the order of the dummy layers to match output
    dummy_layers = dummy_layers[::-1]


    layer_mapping = get_layer_mapping(input_layers, dummy_layers)



    # Apply transformation, inverting layer order
    for i in range(num_layers):
        # Fill output in reversed order
        layer_index = num_layers - 1 - i

        # Get color mapping for this layer
        color_map = layer_mapping[i]

        for r in range(rows):
            for c in range(cols):
                if (
                    (r == i or r == rows - 1 - i) and i <= c <= cols - 1 - i
                ) or (
                    (c == i or c == cols - 1 - i) and i <= r <= rows - 1 - i
                ):
                    original_color = input_grid[r, c]

                    #Check if color needs change
                    if original_color in color_map:
                        output_grid[r, c] = color_map[original_color]
                    else:
                        output_grid[r,c] = original_color

    return output_grid.tolist()
```
