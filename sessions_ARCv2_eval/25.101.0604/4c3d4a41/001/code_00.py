import numpy as np
from scipy.ndimage import label, find_objects

"""
Transforms a 2D grid based on the following rules:
1. Defines a Frame Color (5) and a Background Color (0).
2. Identifies the "Main Frame": the largest connected component of Frame Color cells that touches any edge of the grid.
3. Initializes the output grid as a copy of the input grid.
4. Modifies cells that have the Frame Color in the input but are *not* part of the Main Frame ("Non-Frame 5s"):
    a. If the cell directly below a Non-Frame 5 in the input grid contains a "content color" (neither Frame Color nor Background Color), the Non-Frame 5 cell in the output grid takes the color of the cell below.
    b. Otherwise (if the cell below is Frame Color or Background Color, or if it's the last row), the Non-Frame 5 cell in the output grid becomes Background Color.
5. Modifies cells that contain a "content color" in the input grid:
    a. If the cell directly below such a cell in the input grid is Background Color, the content color cell in the output grid becomes Frame Color.
6. Cells belonging to the Main Frame and cells not otherwise modified retain their original color.
"""

def find_main_frame_mask(grid: np.ndarray, frame_color: int) -> np.ndarray:
    """
    Identifies the largest connected component of frame_color cells
    that touches any edge of the grid.
    Returns a boolean mask where True indicates a cell is part of the main frame.
    """
    H, W = grid.shape
    # Create a binary mask where frame_color cells are True
    binary_mask = (grid == frame_color)
    
    # Label connected components
    labeled_array, num_features = label(binary_mask)
    
    if num_features == 0:
        return np.zeros_like(grid, dtype=bool) # No frame color cells found

    # Find the locations of each labeled component
    component_slices = find_objects(labeled_array)
    
    largest_edge_component_label = 0
    max_size = -1

    for i in range(1, num_features + 1):
        component_mask = (labeled_array == i)
        component_size = np.sum(component_mask)
        
        # Check if this component touches any edge
        touches_edge = False
        coords = np.argwhere(component_mask)
        for r, c in coords:
            if r == 0 or r == H - 1 or c == 0 or c == W - 1:
                touches_edge = True
                break
        
        # If it touches an edge and is larger than the current max, update
        if touches_edge and component_size > max_size:
            max_size = component_size
            largest_edge_component_label = i
            
    if largest_edge_component_label == 0:
         # Fallback: if no component touches the edge, maybe it's just the largest? 
         # Or maybe there's no 'main frame' according to the definition.
         # Let's stick to the definition: if none touch edge, return empty mask.
         # Revisit if tests fail.
         # Alternative: Find largest overall component if none touch edge?
         # Let's check if any component exists first. If so, maybe pick the largest regardless of edge.
         # Re-evaluating: The examples clearly show a large frame, usually touching edges.
         # If no component touches the edge, assume there's no main frame by this definition.
         return np.zeros_like(grid, dtype=bool)


    # Create the final mask for the largest edge-touching component
    main_frame_mask = (labeled_array == largest_edge_component_label)
    
    return main_frame_mask


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid.
    """
    # Convert input to numpy array for easier processing
    input_arr = np.array(input_grid, dtype=int)
    H, W = input_arr.shape
    
    # Initialize output grid as a copy of the input
    output_arr = np.copy(input_arr)
    
    FRAME_COLOR = 5
    BACKGROUND_COLOR = 0

    # 1. Identify the Main Frame
    main_frame_mask = find_main_frame_mask(input_arr, FRAME_COLOR)

    # 2. Process Non-Frame 5s
    for r in range(H):
        for c in range(W):
            # Check if the current cell is a '5' but NOT part of the main frame
            if input_arr[r, c] == FRAME_COLOR and not main_frame_mask[r, c]:
                # Check the cell below
                if r + 1 < H:
                    v_below = input_arr[r + 1, c]
                    # Rule 4a: If below is content color, propagate up
                    if v_below != BACKGROUND_COLOR and v_below != FRAME_COLOR:
                        output_arr[r, c] = v_below
                    # Rule 4b: Otherwise, set to background
                    else:
                        output_arr[r, c] = BACKGROUND_COLOR
                else:
                    # Rule 4b (boundary case): Last row, set to background
                    output_arr[r, c] = BACKGROUND_COLOR

    # 3. Process Content Colors (check input, modify output)
    # Note: We iterate up to H-2 because we look at the cell below (r+1)
    for r in range(H - 1):
        for c in range(W):
            current_color = input_arr[r, c]
            # Check if it's a content color
            if current_color != BACKGROUND_COLOR and current_color != FRAME_COLOR:
                v_below = input_arr[r + 1, c]
                # Rule 5a: If cell below is background, change current cell to Frame Color
                if v_below == BACKGROUND_COLOR:
                    output_arr[r, c] = FRAME_COLOR
                    
    # Convert the result back to a list of lists
    output_grid = output_arr.tolist()
    
    return output_grid
