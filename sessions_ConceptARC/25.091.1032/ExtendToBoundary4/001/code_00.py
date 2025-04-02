import numpy as np
from collections import deque

# --- Helper Functions ---

def _find_objects(grid):
    """
    Finds connected components of non-background (non-zero) pixels using BFS.
    
    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color' (int) and 'coords' (set of (row, col) tuples).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS if a non-background pixel is found that hasn't been visited
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    
                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and if visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({'color': color, 'coords': obj_coords})
    return objects

def _get_line_details(obj):
    """
    Checks if a given object (set of coordinates) forms a straight 
    horizontal or vertical line and returns its details.

    Args:
        obj (dict): An object dictionary with 'color' and 'coords'.

    Returns:
        dict or None: A dictionary with line details ('type', 'color', 
                      'row'/'col', 'cols'/'rows', 'coords') if it's a line, 
                      otherwise None.
    """
    coords = obj['coords']
    color = obj['color']
    
    if not coords:
        return None

    rows = {r for r, c in coords}
    cols = {c for r, c in coords}

    # Check if it's a potential vertical line (all coords in the same column)
    if len(cols) == 1:
        col = list(cols)[0]
        min_row = min(rows)
        max_row = max(rows)
        # Check for contiguity: the number of pixels must match the line length
        if len(coords) == (max_row - min_row + 1):
             # Verify all pixels within the line's bounding box are part of the object
             is_contiguous = True
             for r in range(min_row, max_row + 1):
                 if (r, col) not in coords:
                     is_contiguous = False
                     break
             if is_contiguous:
                return {'type': 'v', 'color': color, 'col': col, 'rows': (min_row, max_row), 'coords': coords}

    # Check if it's a potential horizontal line (all coords in the same row)
    if len(rows) == 1:
        row = list(rows)[0]
        min_col = min(cols)
        max_col = max(cols)
        # Check for contiguity: the number of pixels must match the line length
        if len(coords) == (max_col - min_col + 1):
            # Verify all pixels within the line's bounding box are part of the object
            is_contiguous = True
            for c in range(min_col, max_col + 1):
                if (row, c) not in coords:
                    is_contiguous = False
                    break
            if is_contiguous:
                return {'type': 'h', 'color': color, 'row': row, 'cols': (min_col, max_col), 'coords': coords}

    # If neither vertical nor horizontal contiguous line, return None
    return None


# --- Main Transformation Function ---

def transform(input_grid_list):
    """
    Identifies one horizontal and one vertical line in the input grid that are 
    separated by a single row or column gap consisting entirely of white pixels (0). 
    It then extends the appropriate line to fill this gap. If the gap is vertical 
    (along a column), the vertical line is extended using its color. If the gap 
    is horizontal (along a row), the horizontal line is extended using its color.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_grid = np.array(input_grid_list, dtype=int)
    # Create a copy to modify, preserving the original input
    output_grid = np.copy(input_grid)
    
    # Find all distinct connected non-white objects in the grid
    objects = _find_objects(input_grid)
    
    # Identify which objects are the horizontal and vertical lines
    h_line = None
    v_line = None
    for obj in objects:
        line_details = _get_line_details(obj)
        if line_details:
            if line_details['type'] == 'h':
                h_line = line_details
            elif line_details['type'] == 'v':
                v_line = line_details
                
    # Proceed only if exactly one horizontal and one vertical line are found
    if h_line is None or v_line is None:
        # If the expected lines aren't found, return the unchanged grid
        # This handles unexpected inputs gracefully.
        return output_grid.tolist() 
        
    # Extract properties of the horizontal line
    h_row, h_cols, h_color = h_line['row'], h_line['cols'], h_line['color']
    # Extract properties of the vertical line
    v_col, v_rows, v_color = v_line['col'], v_line['rows'], v_line['color']

    # --- Check for Vertical Gap ---
    # Condition: The vertical line's column must align with the horizontal line's span
    if h_cols[0] <= v_col <= h_cols[1]:
        gap_rows = []
        # Determine the rows that constitute the gap
        if h_row < v_rows[0]: # Horizontal line is above vertical line
            gap_rows = range(h_row + 1, v_rows[0])
        elif h_row > v_rows[1]: # Horizontal line is below vertical line
            gap_rows = range(v_rows[1] + 1, h_row)
            
        # If a potential gap exists (gap_rows is not empty)
        if gap_rows:
            # Check if all pixels in the gap path along the vertical line's column are white (0)
            is_clear = all(input_grid[r, v_col] == 0 for r in gap_rows)
            if is_clear:
                # Fill the gap in the output grid using the vertical line's color
                for r in gap_rows:
                    output_grid[r, v_col] = v_color
                # The transformation is complete, return the result
                return output_grid.tolist() 

    # --- Check for Horizontal Gap ---
    # Condition: The horizontal line's row must align with the vertical line's span
    if v_rows[0] <= h_row <= v_rows[1]:
        gap_cols = []
        # Determine the columns that constitute the gap
        if v_col < h_cols[0]: # Vertical line is to the left of horizontal line
            gap_cols = range(v_col + 1, h_cols[0])
        elif v_col > h_cols[1]: # Vertical line is to the right of horizontal line
            gap_cols = range(h_cols[1] + 1, v_col)
            
        # If a potential gap exists (gap_cols is not empty)
        if gap_cols:
            # Check if all pixels in the gap path along the horizontal line's row are white (0)
            is_clear = all(input_grid[h_row, c] == 0 for c in gap_cols)
            if is_clear:
                # Fill the gap in the output grid using the horizontal line's color
                for c in gap_cols:
                    output_grid[h_row, c] = h_color
                # The transformation is complete, return the result
                return output_grid.tolist() 

    # If no gap was found and filled according to the rules, 
    # return the grid copy (which is identical to the input).
    return output_grid.tolist()