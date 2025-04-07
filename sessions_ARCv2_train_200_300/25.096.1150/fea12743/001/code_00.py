import numpy as np
from scipy.ndimage import label, find_objects
import copy

"""
The transformation identifies connected shapes of color 2 within the input grid. 
It conceptually divides the grid into four quadrants (Top-Left, Top-Right, 
Bottom-Left, Bottom-Right). Shapes within each quadrant are grouped, and 
their combined patterns (relative positions of '2's) and total sizes (number 
of '2's) are calculated.

Comparisons are made between diagonally opposite quadrants:
1. Top-Left (TL) vs. Bottom-Right (BR):
   - If patterns match: TL becomes color 2, BR becomes color 3.
   - If patterns differ:
     - If TL size > BR size: TL becomes 3, BR becomes 8.
     - If TL size <= BR size: TL becomes 8, BR becomes 3.

2. Top-Right (TR) vs. Bottom-Left (BL):
   - If patterns match: TR becomes color 8, BL becomes color 8.
   - If patterns differ:
     - If TR size > BL size: TR becomes 8, BL becomes 2.
     - If TR size <= BL size: TR becomes 2, BL becomes 8.

The cells of the original shapes in the input grid are then recolored in the 
output grid according to the color determined for their respective quadrant 
based on these comparisons. Cells not part of an initial color 2 shape remain 
unchanged.
"""

def find_connected_components(grid: np.ndarray, target_color: int) -> tuple[np.ndarray, int]:
    """Finds connected components of a specific color."""
    labeled_grid, num_features = label(grid == target_color)
    return labeled_grid, num_features

def get_shape_properties(labeled_grid: np.ndarray, num_features: int, grid_rows: int, grid_cols: int) -> dict:
    """
    Calculates properties (coordinates, pattern, size, quadrant) for each shape.

    Returns:
        A dictionary where keys are quadrant names ('TL', 'TR', 'BL', 'BR')
        and values are lists of shapes found in that quadrant. Each shape
        is represented by a dictionary {'coords': set, 'pattern': tuple, 'size': int}.
    """
    shapes_by_quadrant = {'TL': [], 'TR': [], 'BL': [], 'BR': []}
    locations = find_objects(labeled_grid)
    center_row = grid_rows / 2
    center_col = grid_cols / 2

    for i in range(num_features):
        label_id = i + 1
        coords_array = np.argwhere(labeled_grid == label_id)
        coords_set = set(tuple(coord) for coord in coords_array)
        
        if not coords_set:
            continue

        min_r = min(r for r, c in coords_set)
        min_c = min(c for r, c in coords_set)
        
        # Normalize pattern relative to top-left of bounding box
        pattern = tuple(sorted((r - min_r, c - min_c) for r, c in coords_set))
        size = len(coords_set)

        # Determine quadrant based on the center of the shape's coordinates
        avg_row = np.mean([r for r, c in coords_set])
        avg_col = np.mean([c for r, c in coords_set])

        quadrant = ""
        if avg_row < center_row and avg_col < center_col:
            quadrant = 'TL'
        elif avg_row < center_row and avg_col >= center_col:
            quadrant = 'TR'
        elif avg_row >= center_row and avg_col < center_col:
            quadrant = 'BL'
        elif avg_row >= center_row and avg_col >= center_col:
            quadrant = 'BR'
        
        if quadrant:
             shapes_by_quadrant[quadrant].append({
                 'coords': coords_set, 
                 'pattern': pattern, 
                 'size': size,
                 'label': label_id # Store original label for recoloring
                 })

    return shapes_by_quadrant

def get_quadrant_entity(shapes: list[dict]) -> dict:
    """
    Combines multiple shapes in a quadrant into a single entity for comparison.
    Calculates combined pattern (relative to overall bounding box) and total size.
    Returns {'pattern': tuple, 'size': int} or {'pattern': None, 'size': 0} if empty.
    """
    if not shapes:
        return {'pattern': None, 'size': 0}

    all_coords = set().union(*[s['coords'] for s in shapes])
    if not all_coords:
         return {'pattern': None, 'size': 0}

    min_r = min(r for r, c in all_coords)
    min_c = min(c for r, c in all_coords)
    
    # Combined pattern relative to the top-left of the overall bounding box
    combined_pattern = tuple(sorted((r - min_r, c - min_c) for r, c in all_coords))
    total_size = sum(s['size'] for s in shapes)

    return {'pattern': combined_pattern, 'size': total_size}


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Convert to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    output_grid = copy.deepcopy(grid_np)
    grid_rows, grid_cols = grid_np.shape

    # 1. Identify all distinct connected shapes of color 2
    labeled_grid, num_features = find_connected_components(grid_np, 2)
    
    if num_features == 0:
        return input_grid # No shapes to transform

    # 2 & 3. Get properties for each shape and assign to quadrants
    shapes_by_quadrant = get_shape_properties(labeled_grid, num_features, grid_rows, grid_cols)

    # 4. Group shapes by quadrant and get combined properties
    quadrant_entities = {
        q: get_quadrant_entity(shapes_by_quadrant[q]) for q in ['TL', 'TR', 'BL', 'BR']
    }

    # 5. Define shape entities for comparison
    P_TL = quadrant_entities['TL']['pattern']
    S_TL = quadrant_entities['TL']['size']
    P_TR = quadrant_entities['TR']['pattern']
    S_TR = quadrant_entities['TR']['size']
    P_BL = quadrant_entities['BL']['pattern']
    S_BL = quadrant_entities['BL']['size']
    P_BR = quadrant_entities['BR']['pattern']
    S_BR = quadrant_entities['BR']['size']

    # Dictionary to store the output color determined for each quadrant
    quadrant_output_colors = {'TL': 2, 'TR': 2, 'BL': 2, 'BR': 2} # Default to 2 if no comparison applies

    # 6. Compare Top-Left (TL) and Bottom-Right (BR)
    if P_TL is not None or P_BR is not None: # Only compare if at least one exists
        if P_TL == P_BR:
            quadrant_output_colors['TL'] = 2
            quadrant_output_colors['BR'] = 3
        else:
            if S_TL > S_BR:
                quadrant_output_colors['TL'] = 3
                quadrant_output_colors['BR'] = 8
            else: # Covers S_TL <= S_BR 
                quadrant_output_colors['TL'] = 8
                quadrant_output_colors['BR'] = 3
    
    # Handle cases where one quadrant is empty but the other isn't, implicitly handled by size comparison
    # If TL exists but BR doesn't (size 0), TL > BR -> TL=3, BR=8 (but BR has no shape to color)
    # If BR exists but TL doesn't (size 0), TL <= BR -> TL=8, BR=3 (but TL has no shape to color)


    # 7. Compare Top-Right (TR) and Bottom-Left (BL)
    if P_TR is not None or P_BL is not None: # Only compare if at least one exists
        if P_TR == P_BL:
            quadrant_output_colors['TR'] = 8
            quadrant_output_colors['BL'] = 8
        else:
            if S_TR > S_BL:
                quadrant_output_colors['TR'] = 8
                quadrant_output_colors['BL'] = 2
            else: # Covers S_TR <= S_BL
                quadrant_output_colors['TR'] = 2
                quadrant_output_colors['BL'] = 8

    # Handle empty cases similarly to TL/BR


    # 8. Recolor the grid
    # Iterate through the originally identified shapes and recolor based on their quadrant's determined output color
    for quadrant, shapes in shapes_by_quadrant.items():
        output_color = quadrant_output_colors[quadrant]
        for shape in shapes:
             # Find where the original shape (label) is in the labeled_grid and color those cells in output_grid
            rows, cols = np.where(labeled_grid == shape['label'])
            output_grid[rows, cols] = output_color
            
            # Alternative using coords stored earlier (less efficient if many shapes)
            # for r, c in shape['coords']:
            #     output_grid[r, c] = output_color


    # Convert back to list of lists
    return output_grid.tolist()