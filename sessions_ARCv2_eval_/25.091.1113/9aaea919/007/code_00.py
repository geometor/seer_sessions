import numpy as np
from collections import Counter, deque

# Define color constants for rules based on observations from examples
PLUS_TO_GRAY_COLORS = {9, 6, 3}  # Maroon, Magenta, Green plus shapes become Gray
LINE_TO_REMOVE_COLORS = {2, 3}   # Red, Green horizontal lines are removed
GRAY_COLOR = 5

def _find_background_color(grid):
    """Finds the most frequent color in the grid, assumed to be the background."""
    counts = Counter(grid.flatten())
    # Handle empty grid case if necessary
    if not counts:
        return 0 # Default to white if grid is empty
    # Find the color with the highest count
    background_color = counts.most_common(1)[0][0]
    return background_color

def _find_objects(grid, background_color):
    """Finds all connected objects of non-background colors using BFS."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If pixel is not background and not yet visited, start BFS
            if grid[r, c] != background_color and not visited[r, c]:
                obj_color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if neighbor has the same color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == obj_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if obj_coords:
                    objects.append({'color': obj_color, 'coords': obj_coords})
    return objects

def _check_shape(coords):
    """Determines if the object shape is a 5-pixel plus or horizontal line."""
    # Rule applies only to 5-pixel objects based on examples
    if len(coords) != 5:
        return None 

    rows = sorted([r for r, c in coords])
    cols = sorted([c for r, c in coords])
    min_r, max_r = rows[0], rows[-1]
    min_c, max_c = cols[0], cols[-1]
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Check for 3x3 bounding box (characteristic of a plus)
    if height == 3 and width == 3:
        # Verify it's a plus shape. The median coordinate should be the center.
        center_r = rows[2] # Median row of the 5 sorted rows
        center_c = cols[2] # Median col of the 5 sorted cols
        # Check if the median coordinate is the center and if all expected points exist
        expected_plus_coords = {
            (center_r, center_c), 
            (center_r - 1, center_c), 
            (center_r + 1, center_c), 
            (center_r, center_c - 1), 
            (center_r, center_c + 1)
        }
        if coords == expected_plus_coords:
            return "plus"

    # Check for 1x5 bounding box (characteristic of a horizontal line)
    if height == 1 and width == 5:
         # Verify all 5 pixels form a contiguous horizontal line
        expected_line_coords = set((min_r, c) for c in range(min_c, max_c + 1))
        if coords == expected_line_coords:
             return "horizontal_line"

    # Note: Vertical lines (5x1) are not present in examples, so not explicitly checked.
    
    return None # Not a recognized 5-pixel shape for the rules

def transform(input_grid):
    """
    Transforms the input grid based on specific rules applied to 5-pixel objects.
    1. Identifies the background color (most frequent color).
    2. Creates an output grid filled with the background color.
    3. Finds all connected objects (contiguous blocks of same color) 
       that are not the background color.
    4. For each object:
        a. If the object has exactly 5 pixels:
            i. Determine its shape ('plus' or 'horizontal_line').
            ii. Apply rules:
                - Remove 5-pixel horizontal lines if Red(2) or Green(3).
                - Change 5-pixel plus shapes to Gray(5) if Maroon(9), Magenta(6), or Green(3).
                - Keep other 5-pixel shapes/colors unchanged.
        b. If the object does not have 5 pixels, keep it unchanged (copy to output).
    5. Draws the final state of each object onto the output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape

    # Step 1: Identify the background color
    background_color = _find_background_color(input_grid_np)

    # Step 2: Create an output grid initialized with the background color
    output_grid = np.full_like(input_grid_np, background_color)

    # Step 3: Find all distinct non-background objects
    objects = _find_objects(input_grid_np, background_color)

    # Step 4 & 5: Process each object and draw on output grid
    for obj in objects:
        color = obj['color']
        coords = obj['coords']
        
        output_color = color # Default: keep original color
        apply_change = True # Flag to indicate if drawing is needed

        # Step 4a: Check if object has 5 pixels
        if len(coords) == 5:
            # Step 4a.i: Determine shape
            shape = _check_shape(coords)

            # Step 4a.ii: Apply rules based on shape and color
            if shape == "horizontal_line":
                if color in LINE_TO_REMOVE_COLORS:
                    # Remove the line by not drawing it (output remains background)
                    apply_change = False 
                # else: keep original color (output_color = color, apply_change = True)

            elif shape == "plus":
                if color in PLUS_TO_GRAY_COLORS:
                    # Change color to Gray
                    output_color = GRAY_COLOR
                # else: keep original color (output_color = color, apply_change = True)
                
            # else shape is None (not plus or hline): keep original color

        # else (Step 4b): Object does not have 5 pixels, keep original color

        # Draw the object onto the output grid if it wasn't removed
        if apply_change:
             for r, c in coords:
                 # Bounds check just in case, though coords from _find_objects should be valid
                 if 0 <= r < rows and 0 <= c < cols: 
                     output_grid[r, c] = output_color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()