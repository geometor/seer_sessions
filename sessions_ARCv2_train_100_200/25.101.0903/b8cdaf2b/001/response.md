```python
import numpy as np
from collections import deque

"""
Transforms the input grid based on identifying a single composite object at the bottom.

1.  Identifies a single connected block of non-background pixels touching the bottom edge (the "object").
2.  Determines the object's properties:
    - Lowest row index (`r_base`).
    - Horizontal extent on the lowest row (`c_min`, `c_max`).
    - Base width (`W = c_max - c_min + 1`).
    - Total height (`H`).
    - Color of the bottom corners (`CornerC`).
    - "Content color" (`C`), identified as the color of the pixel at the horizontal center of the base row.
3.  Selects one of two symmetrical pixel placement patterns (A or B) based on `CornerC` and `W`:
    - If `CornerC` is Magenta (6), use Pattern A.
    - If `CornerC` is Azure (8), use Pattern B.
    - If `CornerC` is Red (2):
        - If `W <= 3`, use Pattern A.
        - If `W > 3`, use Pattern B.
4.  Adds new pixels of color `C` to the grid above the original object according to the selected pattern, preserving the original object.
    - Pattern A: Adds pixels at `(r_base - H, c_min)` and `(r_base - H, c_max)`.
    - Pattern B: Adds pixels at `(r_base - H - 1, c_min)`, `(r_base - H - 1, c_max)`, `(r_base - H, c_min + 1)`, and `(r_base - H, c_max - 1)`.
"""

def find_object_coords(grid: np.ndarray) -> list[tuple[int, int]]:
    """
    Finds the coordinates of the single connected non-background object
    touching the bottom edge using Breadth-First Search (BFS).
    Assumes 4-connectivity and a single such object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    object_coords = []
    q = deque()

    # Find starting points on the bottom row (non-background)
    start_points_found = False
    for c in range(cols):
        # Check the bottom row pixel
        if grid[rows - 1, c] != 0:
            # If this pixel hasn't been visited (part of the current object search)
            if not visited[rows - 1, c]:
                # Start a new BFS from this point
                q_current = deque([(rows - 1, c)])
                visited[rows - 1, c] = True
                current_object_coords = []
                start_points_found = True # Mark that we found at least one starting point

                while q_current:
                    r, c_curr = q_current.popleft()
                    current_object_coords.append((r, c_curr))

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c_curr + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] != 0:
                            visited[nr, nc] = True
                            q_current.append((nr, nc))
                
                # Assuming only one object touches the bottom, we take the first one found
                object_coords = current_object_coords
                break # Stop searching for other starting points on the bottom row

    if not start_points_found:
        return [] # No object touching the bottom found

    # Sort coordinates for consistency
    object_coords.sort()
    return object_coords

def get_object_properties(grid: np.ndarray, object_coords: list[tuple[int, int]]) -> tuple[int, int, int, int, int, int, int]:
    """
    Calculates properties of the object from its coordinates.
    Returns: r_base, c_min, c_max, H, W, corner_c, content_color
    Raises ValueError if object_coords is empty.
    """
    if not object_coords:
        raise ValueError("No object coordinates provided.")

    # Extract row and column indices
    rows_arr = np.array([r for r, c in object_coords])
    cols_arr = np.array([c for r, c in object_coords])

    # Determine vertical extent and height
    r_min = np.min(rows_arr) # Topmost row index
    r_base = np.max(rows_arr) # Bottommost row index (base row)
    H = r_base - r_min + 1 # Height of the object

    # Filter coordinates to get only those on the base row
    base_coords = [(r, c) for r, c in object_coords if r == r_base]
    base_cols = np.array([c for r, c in base_coords])

    # Determine horizontal extent on the base row and base width
    c_min = np.min(base_cols) # Leftmost column index on base row
    c_max = np.max(base_cols) # Rightmost column index on base row
    W = c_max - c_min + 1 # Width of the object on the base row

    # Get corner color (using the bottom-left corner pixel)
    corner_c = grid[r_base, c_min]

    # Get content color (defined as the color at the horizontal center of the base row)
    # Use integer division for the center index
    center_c_idx = (c_min + c_max) // 2
    content_color = grid[r_base, center_c_idx]

    return r_base, c_min, c_max, H, W, corner_c, content_color


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation logic to the input grid by adding pixels above
    an object found at the bottom edge, based on the object's properties.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input object
    output_grid_np = np.copy(grid_np)
    rows, cols = grid_np.shape

    # --- Step 1 & 2: Find the object and its properties ---
    object_coords = find_object_coords(grid_np)
    if not object_coords:
        # If no object is found touching the bottom, return the original grid
        return input_grid

    try:
        # Calculate relevant properties of the identified object
        r_base, c_min, c_max, H, W, corner_c, content_color = get_object_properties(grid_np, object_coords)
    except ValueError:
        # Handle cases where properties couldn't be determined (e.g., empty coords)
        return input_grid # Return original grid if properties are invalid

    # --- Step 3: Determine the placement pattern ---
    # Define color constants relevant to the pattern selection rules
    MAGENTA = 6
    AZURE = 8
    RED = 2

    use_pattern_A = False
    pattern_selected = False
    if corner_c == MAGENTA:
        use_pattern_A = True
        pattern_selected = True
    elif corner_c == AZURE:
        use_pattern_A = False # Use Pattern B
        pattern_selected = True
    elif corner_c == RED:
        if W <= 3:
            use_pattern_A = True
        else: # W > 3
            use_pattern_A = False # Use Pattern B
        pattern_selected = True

    # If the corner color doesn't match any rule, do nothing
    if not pattern_selected:
        return input_grid

    # --- Step 4: Apply the selected pattern ---
    if use_pattern_A:
        # Pattern A: Adds two pixels
        target_r = r_base - H # Row above the object's top
        target_c_left = c_min
        target_c_right = c_max

        # Add left pixel, checking grid boundaries
        if 0 <= target_r < rows and 0 <= target_c_left < cols:
            output_grid_np[target_r, target_c_left] = content_color
        # Add right pixel, checking grid boundaries
        if 0 <= target_r < rows and 0 <= target_c_right < cols:
            output_grid_np[target_r, target_c_right] = content_color
    else: # Use Pattern B
        # Pattern B: Adds four pixels in two pairs
        # Pair 1 (row r_base - H - 1)
        target_r1 = r_base - H - 1
        target_c1_left = c_min
        target_c1_right = c_max

        # Pair 2 (row r_base - H)
        target_r2 = r_base - H
        target_c2_left = c_min + 1
        target_c2_right = c_max - 1

        # Add first pair, checking grid boundaries
        if 0 <= target_r1 < rows:
            if 0 <= target_c1_left < cols:
                output_grid_np[target_r1, target_c1_left] = content_color
            if 0 <= target_c1_right < cols:
                output_grid_np[target_r1, target_c1_right] = content_color

        # Add second pair, checking grid boundaries
        # Note: Pattern B is used when W>3 (for RED) or W=5 (for AZURE example),
        # ensuring target_c2_left < target_c2_right.
        if 0 <= target_r2 < rows:
            if 0 <= target_c2_left < cols:
                output_grid_np[target_r2, target_c2_left] = content_color
            if 0 <= target_c2_right < cols:
                 output_grid_np[target_r2, target_c2_right] = content_color

    # --- Step 5: Return the result ---
    # Convert the modified NumPy array back to a list of lists
    output_grid = output_grid_np.tolist()
    return output_grid
```