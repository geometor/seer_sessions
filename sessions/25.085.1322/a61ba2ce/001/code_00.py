import numpy as np

"""
Identifies four distinct L-shaped objects (3 pixels) in the input grid.
Determines the 2x2 pattern for each object based on its bounding box.
Assigns each object to a quadrant (Top-Left, Top-Right, Bottom-Left, Bottom-Right) based on its center of mass relative to the input grid's center.
Checks if either of the objects assigned to the top quadrants has a bounding box that crosses the input grid's vertical center line.
Constructs a 4x4 output grid by placing the 2x2 patterns into corresponding 2x2 sections of the output.
If the crossing condition is met, the patterns for the top-left and top-right quadrants are swapped in the output grid. Otherwise, they maintain their relative positions.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of non-background colors in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'color': The color of the object's pixels.
              'pixels': A list of (row, col) coordinates of the object's pixels.
              'bbox': A tuple (min_row, min_col, max_row, max_col) of the bounding box.
              'center_of_mass': A tuple (avg_row, avg_col) of the object's center.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    background_color = 0

    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                pixels = []
                q = [(r, c)]
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                sum_r, sum_c = 0, 0

                while q:
                    row, col = q.pop(0)
                    pixels.append((row, col))
                    sum_r += row
                    sum_c += col
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                center_of_mass = (sum_r / len(pixels), sum_c / len(pixels))
                bbox = (min_r, min_c, max_r, max_c)
                objects.append({
                    'color': color,
                    'pixels': pixels,
                    'bbox': bbox,
                    'center_of_mass': center_of_mass
                })
    return objects

def get_object_pattern(grid, bbox):
    """
    Extracts the 2x2 pattern of an object starting from its bounding box top-left.

    Args:
        grid (np.ndarray): The input grid.
        bbox (tuple): The object's bounding box (min_r, min_c, max_r, max_col).

    Returns:
        np.ndarray: A 2x2 numpy array representing the pattern.
    """
    min_r, min_c, _, _ = bbox
    height, width = grid.shape
    pattern = np.zeros((2, 2), dtype=int) # Default background color 0
    
    obj_color = 0
    # Find the object's color by checking the first non-zero pixel within the bbox area
    # This assumes the object exists within the 2x2 area starting at bbox top-left
    for r_offset in range(2):
        for c_offset in range(2):
             r, c = min_r + r_offset, min_c + c_offset
             if 0 <= r < height and 0 <= c < width and grid[r,c] != 0:
                 obj_color = grid[r,c]
                 break
        if obj_color != 0:
            break
            
    # Fill the pattern grid
    for r_offset in range(2):
        for c_offset in range(2):
            r, c = min_r + r_offset, min_c + c_offset
            # Check if the coordinate is within grid bounds and belongs to the object
            if 0 <= r < height and 0 <= c < width and grid[r, c] == obj_color:
                 pattern[r_offset, c_offset] = grid[r, c]

    return pattern


def transform(input_grid):
    """
    Transforms the input grid based on object identification, quadrant assignment,
    and a potential swap condition for the top quadrants.
    """
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape
    center_row = height // 2
    center_col = width // 2

    # 1. Identify Objects
    objects = find_objects(input_grid_np)

    if len(objects) != 4:
        # Handle error case or unexpected input - returning empty for now
        return np.zeros((4, 4), dtype=int)

    # 2. Characterize Objects and Assign Quadrants
    quadrant_patterns = {}
    quadrant_bboxes = {} # Store bboxes for swap check

    for obj in objects:
        com_r, com_c = obj['center_of_mass']
        bbox = obj['bbox']
        pattern = get_object_pattern(input_grid_np, bbox)

        quadrant = ""
        if com_r < center_row:
            quadrant += "T"
        else:
            quadrant += "B"
        if com_c < center_col:
            quadrant += "L"
        else:
            quadrant += "R"

        quadrant_patterns[quadrant] = pattern
        quadrant_bboxes[quadrant] = bbox

    # 3. Check Swap Condition
    swap_top_quadrants = False
    # Ensure TL and TR objects were found before checking their bboxes
    if 'TL' in quadrant_bboxes and 'TR' in quadrant_bboxes:
        tl_bbox = quadrant_bboxes['TL']
        tr_bbox = quadrant_bboxes['TR']
        # Check if TL bbox crosses the center column
        if tl_bbox[1] < center_col and tl_bbox[3] >= center_col:
            swap_top_quadrants = True
        # Check if TR bbox crosses the center column
        if tr_bbox[1] < center_col and tr_bbox[3] >= center_col:
            swap_top_quadrants = True
            
    # Check if all quadrants are present before assembling
    required_quadrants = {'TL', 'TR', 'BL', 'BR'}
    if not required_quadrants.issubset(quadrant_patterns.keys()):
         # Handle error case: not all quadrants found
         print(f"Warning: Missing quadrants. Found: {quadrant_patterns.keys()}")
         return np.zeros((4, 4), dtype=int)


    # 4. Construct Output
    output_grid = np.zeros((4, 4), dtype=int)

    # Place bottom quadrants
    output_grid[2:4, 0:2] = quadrant_patterns['BL']
    output_grid[2:4, 2:4] = quadrant_patterns['BR']

    # Place top quadrants based on swap condition
    if swap_top_quadrants:
        output_grid[0:2, 0:2] = quadrant_patterns['TR'] # Swap: TR goes to TL position
        output_grid[0:2, 2:4] = quadrant_patterns['TL'] # Swap: TL goes to TR position
    else:
        output_grid[0:2, 0:2] = quadrant_patterns['TL'] # No swap: TL stays in TL
        output_grid[0:2, 2:4] = quadrant_patterns['TR'] # No swap: TR stays in TR

    return output_grid.tolist() # Return as list of lists per ARC standard