
Previous Code:
```python
import numpy as np

"""
Transformation Rule:
1. Initialize the output grid as a copy of the input grid.
2. Identify the largest connected red (2) object that forms a solid rectangle in the input grid. Determine its bounding box coordinates: `min_row`, `min_col`, `max_row`, `max_col`. If no such rectangle is found, return the original grid.
3. Identify all "marker" pixels in the input grid. A marker pixel is any pixel whose color is neither white (0) nor red (2). Record the position (`marker_row`, `marker_col`) of each marker.
4. Iterate through each identified marker pixel:
    a. Determine the marker's position relative to the red rectangle's bounding box.
    b. If the marker is Above the rectangle (`marker_row < min_row`):
        Draw a vertical red (2) line in the output grid in column `marker_col`. This line should extend from row 0 down to `min_row - 1`. Only change pixels if their current color is white (0).
    c. If the marker is Below the rectangle (`marker_row > max_row`):
        Draw a vertical red (2) line in the output grid in column `marker_col`. This line should extend from row `max_row + 1` down to the bottom edge of the grid. Only change pixels if their current color is white (0).
    d. If the marker is Left of the rectangle (`marker_col < min_col`):
        For each row `r` from `min_row` to `max_row` (inclusive), draw a horizontal red (2) line in the output grid. This line should be in row `r` and extend from column 0 across to `min_col - 1`. Only change pixels if their current color is white (0).
    e. If the marker is Right of the rectangle (`marker_col > max_col`):
        For each row `r` from `min_row` to `max_row` (inclusive), draw a horizontal red (2) line in the output grid. This line should be in row `r` and extend from column `max_col + 1` across to the right edge of the grid. Only change pixels if their current color is white (0).
5. Return the modified output grid.
"""

# --- Helper Functions ---

def find_connected_components(grid, color):
    """Finds all connected components of a given color using BFS."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                component = []
                q = [(r, c)]
                visited[r, c] = True
                component_rows = set()
                component_cols = set()
                
                # BFS to find all connected pixels of the same color
                queue_idx = 0
                while queue_idx < len(q):
                    row, col = q[queue_idx]
                    queue_idx += 1
                    component.append((row, col))
                    component_rows.add(row)
                    component_cols.add(col)
                    
                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Check if the component forms a solid rectangle
                if not component_rows or not component_cols: continue # Skip if empty component somehow
                
                min_r, max_r = min(component_rows), max(component_rows)
                min_c, max_c = min(component_cols), max(component_cols)
                is_rectangle = True
                # Verify the count of pixels matches the bounding box area
                if len(component) != (max_r - min_r + 1) * (max_c - min_c + 1):
                    is_rectangle = False
                else:
                    # Optionally, double-check all cells within the bounding box are the correct color
                    # This check is implicitly handled by the component size check if connectivity is correct.
                    # for row_idx in range(min_r, max_r + 1):
                    #     for col_idx in range(min_c, max_c + 1):
                    #          if grid[row_idx, col_idx] != color: # Should not happen if component finding is correct
                    #             is_rectangle = False
                    #             break
                    #     if not is_rectangle:
                    #         break
                     pass # Assume component finding is correct

                if component and is_rectangle: # Only add if it's a non-empty rectangle
                    components.append(component)
    return components

def find_largest_component(grid, color):
    """Finds the largest connected rectangular component of a given color."""
    components = find_connected_components(grid, color)
    if not components:
        return None
    # Find the component with the maximum number of pixels
    largest_component = max(components, key=len)
    return largest_component

def get_bounding_box(component_coords):
    """Calculates the bounding box (min_row, min_col, max_row, max_col) of a component."""
    if not component_coords:
        return None, None, None, None
    rows = [r for r, c in component_coords]
    cols = [c for r, c in component_coords]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, min_col, max_row, max_col

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rule based on marker positions relative to the largest red rectangle.
    Draws lines from the rectangle edges towards markers, filling only white space.
    Horizontal lines now span the full height of the original rectangle.
    """
    # 1. Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    red_color = 2
    background_color = 0

    # 2. Find the largest red rectangular object and its bounding box
    red_component = find_largest_component(output_grid, red_color)
    if not red_component:
        # Handle case where no red object is found (return original grid)
        # print("Warning: No red rectangular component found.") # Optional debug message
        return output_grid 
        
    min_row, min_col, max_row, max_col = get_bounding_box(red_component)

    # Check if bounding box is valid (should be if red_component exists)
    if min_row is None:
        # print("Warning: Could not determine bounding box for red component.") # Optional debug message
        return output_grid 

    # 3. Find all marker pixels
    marker_coords = []
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] != background_color and output_grid[r, c] != red_color:
                marker_coords.append((r, c))

    # 4. Process each marker and draw lines, only overwriting background
    for marker_row, marker_col in marker_coords:
        # a. Determine relative position
        is_above = marker_row < min_row
        is_below = marker_row > max_row
        is_left = marker_col < min_col
        is_right = marker_col > max_col

        # b. Draw vertical line if Above
        if is_above:
            # Ensure marker_col is within grid bounds
            if 0 <= marker_col < cols:
                for r in range(min_row): # From row 0 up to min_row - 1
                    if 0 <= r < rows: # Boundary check for row
                        if output_grid[r, marker_col] == background_color:
                           output_grid[r, marker_col] = red_color

        # c. Draw vertical line if Below
        if is_below:
            # Ensure marker_col is within grid bounds
            if 0 <= marker_col < cols:
                for r in range(max_row + 1, rows): # From max_row + 1 down to the end
                     if 0 <= r < rows: # Boundary check for row (redundant but safe)
                         if output_grid[r, marker_col] == background_color:
                            output_grid[r, marker_col] = red_color

        # d. Draw horizontal lines if Left (Corrected Logic)
        if is_left:
            # Iterate through all rows spanned by the original rectangle
            for r in range(min_row, max_row + 1):
                # Ensure row index is valid
                if 0 <= r < rows:
                    # Draw horizontal line from col 0 up to min_col - 1
                    for c in range(min_col): 
                        if 0 <= c < cols: # Boundary check for column
                            if output_grid[r, c] == background_color:
                                output_grid[r, c] = red_color

        # e. Draw horizontal lines if Right (Corrected Logic)
        if is_right:
            # Iterate through all rows spanned by the original rectangle
            for r in range(min_row, max_row + 1):
                 # Ensure row index is valid
                if 0 <= r < rows:
                    # Draw horizontal line from max_col + 1 across to the end
                    for c in range(max_col + 1, cols): 
                        if 0 <= c < cols: # Boundary check for column (redundant but safe)
                            if output_grid[r, c] == background_color:
                                 output_grid[r, c] = red_color

    # 5. Return the modified grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 2 0 0 0 3 0 0
0 0 0 0 2 2 2 2 2 0 0 0 0 0 0
0 3 0 0 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 2 2 2 2 2 0 0 0 0 3 0
0 0 0 0 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 2 0 2 0 0 0 0 0 0 0
0 0 0 0 3 2 0 2 3 0 0 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 0 0 0 0
0 0 0 0 0 2 3 2 0 0 0 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 0 0 0 3 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 3 0 0 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 0 0 0 0 3 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 2 0 2 2 0 0 0 0 0 0 0
0 0 0 0 2 0 2 2 0 0 0 0 0 0 0
0 0 0 0 2 0 2 2 0 0 0 0 0 0 0
0 0 0 0 2 0 2 2 3 0 0 0 0 0 0
0 0 0 0 2 0 2 2 0 0 0 0 0 0 0
0 0 0 0 2 0 2 2 0 0 0 0 0 0 0
0 0 0 0 2 3 2 2 0 0 0 0 0 0 0
0 0 0 0 2 0 2 2 0 0 0 0 0 0 0
0 0 0 0 2 0 2 2 0 0 0 0 0 0 0
0 0 0 0 2 0 2 2 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 2 0 2 0 2 0 0 0 0 0 0
0 0 0 0 3 0 2 0 3 0 0 0 0 0 0
0 0 0 0 2 0 2 0 2 0 0 0 0 0 0
0 0 0 0 2 0 3 0 2 0 0 0 0 0 0
0 0 0 0 2 0 2 0 2 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 3 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 3 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 3 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 2 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 0 0 3 0 0 0 0 0 0
0 0 0 0 0 2 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 0 0 2 0 0 0 0 0 0
0 0 0 0 0 3 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 0 0 2 0 0 0 0 0 0
```
Match: False
Pixels Off: 83
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 55.333333333333314

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 2 0 2 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 8 2 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 2 2 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 8 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 2 2 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 2 2 2
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 2 2 2 2 2
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 8 2 2 2 2 2 2 2 2 2
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 2 2 2 2 2 2
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 2 0 2 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 2 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 2 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 8 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 8 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 172
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 65.52380952380952

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 2 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 0 0 0 0 0 0
0 4 0 0 0 2 2 2 2 2 2 0 0 0 0 0 0
0 0 4 0 0 2 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 2 0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 2 4 2 2 2 4 0 0 0 0 0 0
0 0 0 0 0 2 0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 2 0 2 2 2 0 0 0 0 0 0 0
0 0 4 0 0 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 4 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2
0 0 4 0 0 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 0 0 0 4 0 0
0 0 0 0 0 0 2 2 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 0 2 0 0 0 0 0 0
0 0 0 0 0 4 2 2 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 4 2 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 0 2 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0
2 2 4 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 4 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 4 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 4 2 2
0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 97
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 57.05882352941177
