"""
Transforms a 2D grid based on the following rules:
1. Defines a Frame Color (5) and a Background Color (0). Any other color is a Content Color.
2. Identifies the "Main Frame": the largest connected component of Frame Color cells in the input grid that touches at least one edge.
3. Initializes an output grid of the same dimensions.
4. Determines the color of each cell (r, c) in the output grid based on the input grid and the Main Frame mask:
    a. Main Frame Cell: If the cell is part of the Main Frame, the output color is Frame Color.
    b. Background Cell: If the cell is not part of the Main Frame and its input color is Background Color, the output color is Background Color.
    c. Non-Frame 5 Cell: If the cell is not part of the Main Frame and its input color is Frame Color:
        i. Check the color directly below in the input grid (I_bel1). Treat out-of-bounds as Background Color.
        ii. If I_bel1 is a Content Color, the output color is I_bel1.
        iii. Otherwise (I_bel1 is Frame or Background), the output color is Background Color.
    d. Content Color Cell (C): If the cell is not part of the Main Frame and its input color C is a Content Color:
        i. Check if it's the top of a vertical stack of C's (r=0 or cell above is different).
        ii. If it is the top, the output color is C.
        iii. If it is not the top:
            1. Find the height h of the stack of C's downwards.
            2. Get the terminating color T at (r+h, c) (treat out-of-bounds as Background Color).
            3. If T is Background Color or Frame Color, the output color is Frame Color.
            4. Otherwise (T is a Content Color), the output color is C.
"""

import numpy as np
from scipy.ndimage import label

def find_main_frame_mask(grid: np.ndarray, frame_color: int) -> np.ndarray:
    """
    Identifies the largest connected component of frame_color cells
    that touches any edge of the grid.
    Returns a boolean mask where True indicates a cell is part of the main frame.
    Uses 8-connectivity.
    """
    H, W = grid.shape
    # Create a binary mask where frame_color cells are True
    binary_mask = (grid == frame_color)
    
    # Label connected components using 8-connectivity (default for label)
    labeled_array, num_features = label(binary_mask)
    
    if num_features == 0:
        return np.zeros_like(grid, dtype=bool) # No frame color cells found

    largest_edge_component_label = 0
    max_size = -1

    # Iterate through each component label (1 to num_features)
    for i in range(1, num_features + 1):
        component_mask = (labeled_array == i)
        component_size = np.sum(component_mask)
        
        # Check if this component touches any edge
        touches_edge = False
        # Get coordinates where the component exists
        coords = np.argwhere(component_mask)
        # Check if any coordinate touches an edge
        if coords.size > 0: # Ensure component is not empty
             if np.any(coords[:, 0] == 0) or np.any(coords[:, 0] == H - 1) or \
                np.any(coords[:, 1] == 0) or np.any(coords[:, 1] == W - 1):
                 touches_edge = True
        
        # If it touches an edge and is larger than the current max, update
        if touches_edge and component_size > max_size:
            max_size = component_size
            largest_edge_component_label = i
            
    # If no component touching an edge was found, return an empty mask
    if largest_edge_component_label == 0:
         # This might happen if the only '5's are internal and don't touch edges.
         # Based on examples, we expect a frame touching edges.
         return np.zeros_like(grid, dtype=bool) 

    # Create the final mask for the largest edge-touching component
    main_frame_mask = (labeled_array == largest_edge_component_label)
    
    return main_frame_mask


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """Applies the transformation rules to the input grid."""
    
    # --- Initialization ---
    input_arr = np.array(input_grid, dtype=int)
    H, W = input_arr.shape
    output_arr = np.full_like(input_arr, -1) # Initialize with temporary value
    
    FRAME_COLOR = 5
    BACKGROUND_COLOR = 0

    # --- Step 1: Identify the Main Frame ---
    main_frame_mask = find_main_frame_mask(input_arr, FRAME_COLOR)

    # --- Step 2: Determine Output for Each Cell ---
    for r in range(H):
        for c in range(W):
            # --- Rule 4a: Main Frame Cell ---
            if main_frame_mask[r, c]:
                output_arr[r, c] = FRAME_COLOR
                continue

            input_color = input_arr[r, c]

            # --- Rule 4b: Background Cell (not main frame) ---
            if input_color == BACKGROUND_COLOR:
                output_arr[r, c] = BACKGROUND_COLOR
                continue

            # --- Rule 4c: Non-Frame 5 Cell (not main frame) ---
            if input_color == FRAME_COLOR:
                color_below_in = BACKGROUND_COLOR # Default if out of bounds
                if r + 1 < H:
                    color_below_in = input_arr[r + 1, c]
                
                # Check if color_below is a Content Color
                is_content_below = (color_below_in != BACKGROUND_COLOR and color_below_in != FRAME_COLOR)
                
                if is_content_below:
                    output_arr[r, c] = color_below_in # Rule 4c.ii
                else:
                    output_arr[r, c] = BACKGROUND_COLOR # Rule 4c.iii
                continue

            # --- Rule 4d: Content Color Cell (not main frame) ---
            # This handles the remaining case: input_color is a Content Color (C)
            C = input_color 
            
            # Check if top of stack
            is_top_of_stack = (r == 0 or input_arr[r - 1, c] != C)

            if is_top_of_stack: # Rule 4d.ii
                output_arr[r, c] = C
            else: # Rule 4d.iii - Not top of stack
                # Find stack height h downwards
                h = 0
                while True:
                    check_r = r + h
                    if check_r < H and input_arr[check_r, c] == C:
                        h += 1
                    else:
                        break 
                
                # Get terminating color T
                term_r = r + h
                terminating_color = BACKGROUND_COLOR # Default if out of bounds
                if term_r < H:
                    terminating_color = input_arr[term_r, c]

                # Apply rule based on terminating color
                if terminating_color == BACKGROUND_COLOR or terminating_color == FRAME_COLOR:
                    output_arr[r, c] = FRAME_COLOR # Rule 4d.iii.3
                else: # Terminating color is a Content Color
                    output_arr[r, c] = C # Rule 4d.iii.4

    # --- Finalization ---
    # Sanity check if any cell remained unassigned
    if np.any(output_arr == -1):
        raise ValueError("Error: Not all cells were assigned an output color.")
        
    output_grid = output_arr.tolist()
    return output_grid