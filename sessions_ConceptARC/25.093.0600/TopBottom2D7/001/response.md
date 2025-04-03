```python
import numpy as np
from scipy.ndimage import label, find_objects

"""
Identifies all contiguous blocks of non-zero numbers (1s and 3s) in the input grid.
Determines the "target number" (1 or 3) based on the block whose top-left corner is highest (minimum row index) and, in case of a tie, leftmost (minimum column index).
Extracts all blocks composed of this target number from the input grid.
Constructs the output grid containing only the cells belonging to these selected blocks, preserving their values and relative positions, cropped to their combined bounding box.
"""

def find_blocks(grid):
    """
    Finds all connected components (blocks) of non-zero values in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a block
              and contains 'value', 'coords' (list of (r, c) tuples),
              and 'top_left' (r, c) tuple. Returns empty list if no blocks.
    """
    blocks = []
    # Structure for 4-connectivity (up, down, left, right)
    # Use 8-connectivity if diagonal connections count: structure = np.ones((3, 3), dtype=bool)
    structure = np.array([[0,1,0],[1,1,1],[0,1,0]])
    
    # Label connected components for 1s
    labeled_grid_1, num_features_1 = label(grid == 1, structure=structure)
    objects_1 = find_objects(labeled_grid_1)
    for i in range(num_features_1):
        label_id = i + 1
        coords = list(zip(*np.where(labeled_grid_1 == label_id)))
        if not coords:
            continue
        min_r = min(r for r, c in coords)
        min_c = min(c for r, c in coords if r == min_r)
        blocks.append({'value': 1, 'coords': coords, 'top_left': (min_r, min_c)})

    # Label connected components for 3s
    labeled_grid_3, num_features_3 = label(grid == 3, structure=structure)
    objects_3 = find_objects(labeled_grid_3)
    for i in range(num_features_3):
        label_id = i + 1
        coords = list(zip(*np.where(labeled_grid_3 == label_id)))
        if not coords:
            continue
        min_r = min(r for r, c in coords)
        min_c = min(c for r, c in coords if r == min_r)
        blocks.append({'value': 3, 'coords': coords, 'top_left': (min_r, min_c)})
        
    return blocks


def transform(input_grid):
    """
    Transforms the input grid based on the described rules.

    Args:
        input_grid (list of list of int): The input 8x8 grid.

    Returns:
        list of list of int: The transformed, cropped output grid.
    """
    grid = np.array(input_grid, dtype=int)

    # 1. Identify all distinct contiguous blocks of non-zero numbers
    all_blocks = find_blocks(grid)

    if not all_blocks:
        return [] # Handle empty input or input with only zeros

    # 2. Find the top-most, left-most block to determine the target number
    min_r = float('inf')
    min_c_at_min_r = float('inf')
    target_value = -1 # Initialize with an invalid value

    for block in all_blocks:
        r, c = block['top_left']
        if r < min_r:
            min_r = r
            min_c_at_min_r = c
            target_value = block['value']
        elif r == min_r:
            if c < min_c_at_min_r:
                min_c_at_min_r = c
                target_value = block['value']

    # 3. Select all blocks matching the target number
    selected_blocks = [block for block in all_blocks if block['value'] == target_value]

    if not selected_blocks:
         return [] # Should not happen if all_blocks was not empty, but good practice

    # 4. Collect all coordinates from selected blocks
    all_selected_coords = []
    for block in selected_blocks:
        all_selected_coords.extend(block['coords'])

    if not all_selected_coords:
        return [] # Should not happen

    # 5. Determine the bounding box of the selected coordinates
    min_row = min(r for r, c in all_selected_coords)
    max_row = max(r for r, c in all_selected_coords)
    min_col = min(c for r, c in all_selected_coords)
    max_col = max(c for r, c in all_selected_coords)

    # 6. Create the output grid
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    # Initialize with 0, though not strictly necessary as we fill non-zero values
    output_grid_np = np.zeros((output_height, output_width), dtype=int) 

    # 7. Populate the output grid
    for r, c in all_selected_coords:
        # Adjust coordinates relative to the bounding box top-left
        output_r = r - min_row
        output_c = c - min_col
        # The value is the target_value
        output_grid_np[output_r, output_c] = target_value

    # Convert back to list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid
```