import numpy as np

def _get_layer_colors(grid):
    """
    Identifies the colors of concentric layers by checking pixels along the diagonal.
    Assumes layers are simple, concentric rectangles centered or aligned with grid boundaries.
    Returns a list of unique colors ordered from outermost to innermost layer.
    """
    rows, cols = grid.shape
    layer_colors = []
    max_depth = min(rows // 2, cols // 2) # Maximum possible layers based on grid size

    # Iterate diagonally inwards from top-left corner
    for i in range(max_depth + 1):
        if i < rows and i < cols:
            color = grid[i, i]
            # Only add the color if it's the first time we see it
            # (ensures we get the colors in order of layers)
            if color not in layer_colors:
                layer_colors.append(color)
            # If the color is the same as the previous layer's color,
            # we might have reached the center or the pattern repeats.
            # Check if the next diagonal step (if possible) has a different color.
            # If grid[i+1][i+1] exists and is same as grid[i][i], we stop adding new layers.
            elif i > 0 and i + 1 < rows and i + 1 < cols and grid[i+1,i+1] == color:
                 # Indicates the innermost solid block is reached or pattern isn't strictly unique colors per layer.
                 # For the given examples, stopping when a color repeats seems okay.
                 break
            elif i > 0 and color == layer_colors[-1]: # Color repeats immediately, innermost reached.
                 break

        else:
            # Stop if we go out of bounds
            break
            
    # Check if the diagonal walk covered all colors, especially for non-square grids
    # or layers that might not change exactly on the main diagonal.
    # Example: A 2xN grid. grid[0,0] is layer 1, grid[1,1] doesn't exist but layer 2 might.
    # For simplicity based on examples, we rely on the diagonal walk.
            
    return layer_colors

def transform(input_grid):
    """
    Transforms the input grid by recoloring its concentric rectangular layers.
    
    1. Identifies the colors of the layers (C1, C2, C3, ... from outer to inner) 
       by looking along the diagonal from the top-left corner.
    2. Determines the output color for each input layer color based on a fixed mapping:
       - Input Layer 1 color (C1) maps to Input Layer 3 color (C3).
       - Input Layer 2 color (C2) maps to Input Layer 1 color (C1).
       - Input Layer 3 color (C3) maps to Input Layer 2 color (C2).
       - If a 4th layer exists (C4), its color maps to Input Layer 3 color (C3).
    3. Creates a new grid where each pixel's color is replaced according to this mapping.
    """
    
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    output_grid_np = np.zeros_like(input_grid_np)

    # 1. Identify input layer colors
    input_layer_colors = _get_layer_colors(input_grid_np)
    num_layers = len(input_layer_colors)

    # Check if enough layers were found (at least 3 needed for the rule)
    if num_layers < 3:
        # Handle cases with fewer than 3 layers if necessary.
        # Based on examples, assume at least 3 layers.
        # If not, maybe return input or raise error? Returning input for now.
        print(f"Warning: Found only {num_layers} layers. Rule requires at least 3. Returning input.")
        return input_grid # Or return input_grid_np.tolist()
        
    C1 = input_layer_colors[0]
    C2 = input_layer_colors[1]
    C3 = input_layer_colors[2]
    C4 = input_layer_colors[3] if num_layers >= 4 else None

    # 2. Define the color mapping rule
    color_map = {}
    color_map[C1] = C3  # Layer 1 -> Layer 3 color
    color_map[C2] = C1  # Layer 2 -> Layer 1 color
    color_map[C3] = C2  # Layer 3 -> Layer 2 color
    if C4 is not None:
        color_map[C4] = C3  # Layer 4 -> Layer 3 color
        
    # Handle potential cases where colors repeat in layers unexpectedly
    # E.g. if C1 == C3 initially. The map needs careful definition.
    # Let's refine mapping logic slightly for clarity and safety:
    output_map = {}
    output_map[C1] = C3
    output_map[C2] = C1
    output_map[C3] = C2
    if C4 is not None:
        # If C4 is a distinct color, map it.
        # If C4 happens to be C1, C2, or C3, its pixels will already be mapped
        # by the rules above. But the rule says Layer 4 maps to C3.
        # So, any pixel with original color C4 should become C3.
        output_map[C4] = C3
        
    # The most robust way is to map original colors to target colors.
    
    # 3. Create the output grid by applying the mapping
    for r in range(rows):
        for c in range(cols):
            input_color = input_grid_np[r, c]
            # Find the corresponding output color from the map
            # If a color in the grid wasn't identified as a layer color (edge case?),
            # keep its original color or assign a default (e.g., 0/black).
            # Based on examples, all pixels belong to identified layers.
            output_color = output_map.get(input_color, input_color) # Default to input_color if not in map
            output_grid_np[r, c] = output_color

    # Convert back to list of lists for the required output format
    return output_grid_np.tolist()
