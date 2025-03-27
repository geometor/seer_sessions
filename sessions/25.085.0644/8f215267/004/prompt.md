
Previous Code:
```python
import numpy as np
from collections import Counter

"""
Transforms the input grid by identifying hollow rectangles, preserving their borders, and drawing a pattern along their internal horizontal midline based on the background color's parity.

1.  **Identify Background:** Determine the most frequent color (`background_color`) and its parity (`background_parity`).
2.  **Initialize Output:** Create an output grid of the same dimensions, filled with `background_color`.
3.  **Find Hollow Rectangles:**
    *   Use a connected components search (like BFS) to find groups of connected, non-background pixels of the same color.
    *   For each component, check if it forms a valid "hollow rectangle":
        *   Must consist of a single color (`rectangle_color`).
        *   Must form a single-pixel thick rectangular border.
        *   The area strictly inside the border must contain only the `background_color` in the input grid.
4.  **Draw Borders:** Draw the border pixels of each identified hollow rectangle onto the output grid using its `rectangle_color`.
5.  **Apply Midline Pattern:** For each hollow rectangle with an internal area:
    *   Calculate the row index of the horizontal midline of its *internal* area.
    *   Identify the column indices corresponding to the *internal* area.
    *   Iterate through these internal columns. If a column index's parity matches the `background_parity`, color the corresponding pixel on the midline row in the output grid with the `rectangle_color`.
6.  **Return:** The modified output grid.
"""

def _get_background_color(grid: np.ndarray) -> int:
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    # Handle potential ties by picking the most frequent; ARC usually has clear background
    background_color = counts.most_common(1)[0][0]
    return background_color

def _find_connected_components(grid: np.ndarray, background_color: int) -> list:
    """
    Finds connected components of non-background colors using BFS.
    Returns a list of components, where each component is a list of (r, c) tuples.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color and not visited[r, c]:
                # Start BFS for a new component
                component_color = grid[r, c]
                component_coords = []
                queue = [(r, c)]
                visited[r, c] = True

                while queue:
                    curr_r, curr_c = queue.pop(0)
                    component_coords.append((curr_r, curr_c))

                    # Check 8 neighbors (including diagonals for connectivity)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = curr_r + dr, curr_c + dc

                            # Check bounds, color match, and visited status
                            if 0 <= nr < height and 0 <= nc < width and \
                               not visited[nr, nc] and \
                               grid[nr, nc] == component_color:
                                visited[nr, nc] = True
                                queue.append((nr, nc))
                
                if component_coords:
                     components.append({"color": component_color, "coords": component_coords})

    return components


def _is_valid_hollow_rectangle(grid: np.ndarray, component_coords: list, background_color: int) -> tuple:
    """
    Checks if a component defined by coords is a hollow rectangle.
    Returns (is_valid, rect_color, bounding_box)
    """
    if not component_coords:
        return False, -1, None

    rows, cols = zip(*component_coords)
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    # Get the color from the first coordinate (all should be the same)
    rect_color = grid[component_coords[0]]

    # 1. Check if all component pixels lie on the bounding box edges
    on_border = True
    for r, c in component_coords:
        if not (r == min_r or r == max_r or c == min_c or c == max_c):
            on_border = False
            break
    if not on_border:
        return False, -1, None
        
    # 2. Check if the number of pixels matches the perimeter for single thickness
    # Perimeter = 2 * (height + width - 2) for rectangles > 1x1
    # Perimeter = N for lines (1xN or Nx1)
    if height > 1 and width > 1:
        expected_perimeter_pixels = 2 * (height + width - 2)
    else: # Handle lines
        expected_perimeter_pixels = max(height, width)
        
    if len(component_coords) != expected_perimeter_pixels :
         return False, -1, None

    # 3. Check internal area (if it exists) for background color
    has_internal_area = (height > 2 and width > 2)
    if has_internal_area:
        internal_slice = grid[min_r + 1:max_r, min_c + 1:max_c]
        if not np.all(internal_slice == background_color):
            return False, -1, None
            
    # If all checks pass
    bounding_box = (min_r, min_c, max_r, max_c)
    return True, rect_color, bounding_box


def transform(input_grid: list) -> list:
    """
    Applies the transformation: finds hollow rectangles, copies their borders,
    and draws a pattern on the internal midline based on background parity.
    """
    # Convert input to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # 1. Identify Background Color and Parity
    background_color = _get_background_color(input_array)
    background_parity = background_color % 2 # 0 for even, 1 for odd

    # 2. Initialize Output Grid
    output_grid = np.full_like(input_array, background_color)

    # 3. Find Connected Components (potential rectangles)
    components = _find_connected_components(input_array, background_color)

    # Store valid hollow rectangles found
    hollow_rectangles = [] 
    
    # Validate each component
    for component in components:
        coords = component["coords"]
        is_valid, rect_color, bbox = _is_valid_hollow_rectangle(
            input_array, 
            coords, 
            background_color
        )
        
        if is_valid:
            hollow_rectangles.append({
                "color": rect_color,
                "coords": coords,
                "bbox": bbox # (min_r, min_c, max_r, max_c)
            })

    # 4. Draw Rectangle Borders onto Output
    for rect in hollow_rectangles:
        rect_color = rect["color"]
        for r, c in rect["coords"]:
            # Basic bounds check (should always be true if coords are from grid)
            if 0 <= r < height and 0 <= c < width:
                output_grid[r, c] = rect_color

    # 5. Apply Midline Pattern
    for rect in hollow_rectangles:
        rect_color = rect["color"]
        min_r, min_c, max_r, max_c = rect["bbox"]
        
        # Calculate internal dimensions
        internal_height = max_r - min_r - 1
        internal_width = max_c - min_c - 1

        # Proceed only if there is an internal area
        if internal_height > 0 and internal_width > 0:
            # Calculate midline row index relative to the top of the grid
            # Add min_r + 1 (start of internal area) to the relative midline index
            midline_row = min_r + 1 + (internal_height // 2) 

            # Iterate through internal column indices
            start_col = min_c + 1
            end_col = max_c # The range stops *before* end_col, corresponding to max_c - 1

            for col in range(start_col, end_col):
                # Check if column index parity matches background parity
                if col % 2 == background_parity:
                    # Check bounds just in case (should be within grid)
                    if 0 <= midline_row < height and 0 <= col < width:
                         # Ensure we only color over background pixels in the output grid
                         # (This prevents overwriting parts of other rectangles if they somehow overlap,
                         # although the hollow rectangle definition should prevent internal overlap).
                        if output_grid[midline_row, col] == background_color:
                            output_grid[midline_row, col] = rect_color

    # 6. Return Output as list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 4 4 4 4 4 4 4 4 4 4 1 1 1 3 3 1 1 1 8 8 1
1 4 1 1 1 1 1 1 1 1 1 4 1 1 1 3 3 1 1 1 1 1 1
1 4 1 1 1 1 1 1 1 1 1 4 1 1 1 1 1 1 1 1 1 1 1
1 4 1 1 1 1 1 1 1 1 1 4 1 1 1 1 1 1 4 4 1 1 1
1 4 4 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 4 4 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 8 8 8 8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 3 1 1
1 8 1 1 1 1 1 1 1 1 1 8 1 1 1 4 4 1 1 1 3 1 1
1 8 1 1 1 1 1 1 1 1 1 8 1 1 1 1 1 1 1 1 1 1 1
1 8 1 1 1 1 1 1 1 1 1 8 1 1 1 1 1 1 1 1 1 1 1
1 8 8 8 8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 1 1 1 1
1 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 2 2 2 1 1 1 1
1 2 1 1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 2 1 1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 2 1 1 1 1 1 1 1 1 1 2 1 1 1 8 8 1 1 1 1 1 1
1 2 2 2 2 2 2 2 2 2 2 2 1 1 1 8 8 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 8 8 1 1 1 1 1 8 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 4 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 1 1 1 1 1
1 4 1 1 1 1 1 1 1 1 1 4 1 1 1 1 1 1 1 1 1 1 1
1 4 1 1 1 1 1 4 1 4 1 4 1 1 1 1 1 1 1 1 1 1 1
1 4 1 1 1 1 1 1 1 1 1 4 1 1 1 1 1 1 1 1 1 1 1
1 4 4 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 8 8 8 8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1
1 8 1 1 1 1 1 1 1 1 1 8 1 1 1 1 1 1 1 1 1 1 1
1 8 1 8 1 8 1 8 1 8 1 8 1 1 1 1 1 1 1 1 1 1 1
1 8 1 1 1 1 1 1 1 1 1 8 1 1 1 1 1 1 1 1 1 1 1
1 8 8 8 8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1
1 2 1 1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 2 1 1 1 1 1 1 1 2 1 2 1 1 1 1 1 1 1 1 1 1 1
1 2 1 1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Transformed Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 4 4 4 4 4 4 4 4 4 4 4 1 1 1 3 3 1 1 1 8 8 1
1 4 1 1 1 1 1 1 1 1 1 4 1 1 1 3 3 1 1 1 1 1 1
1 4 1 4 1 4 1 4 1 4 1 4 1 1 1 1 1 1 1 1 1 1 1
1 4 1 1 1 1 1 1 1 1 1 4 1 1 1 1 1 1 4 4 1 1 1
1 4 4 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 4 4 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 8 8 8 8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 3 1 1
1 8 1 1 1 1 1 1 1 1 1 8 1 1 1 4 4 1 1 1 3 1 1
1 8 1 8 1 8 1 8 1 8 1 8 1 1 1 1 1 1 1 1 1 1 1
1 8 1 1 1 1 1 1 1 1 1 8 1 1 1 1 1 1 1 1 1 1 1
1 8 8 8 8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 1 1 1 1
1 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 2 2 2 1 1 1 1
1 2 1 1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 2 1 2 1 2 1 2 1 2 1 2 1 1 1 1 1 1 1 1 1 1 1
1 2 1 1 1 1 1 1 1 1 1 2 1 1 1 8 8 1 1 1 1 1 1
1 2 2 2 2 2 2 2 2 2 2 2 1 1 1 8 8 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 8 8 1 1 1 1 1 8 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Match: False
Pixels Off: 33
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 24.95274102079395

## Example 2:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 6 6 8
8 8 1 1 1 1 1 1 1 1 1 1 1 8 8 4 4 4 8 8 8 8 8
8 8 1 8 8 8 8 8 8 8 8 8 1 8 8 8 4 8 8 8 8 8 8
8 8 1 8 8 8 8 8 8 8 8 8 1 8 8 8 8 8 8 4 8 8 8
8 8 1 8 8 8 8 8 8 8 8 8 1 8 8 8 8 4 4 4 8 8 8
8 8 1 1 1 1 1 1 1 1 1 1 1 8 8 8 8 8 4 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 6 6 6 6 6 6 6 6 6 6 6 8 8 2 2 8 8 8 3 3 8
8 8 6 8 8 8 8 8 8 8 8 8 6 8 8 2 2 8 8 8 3 8 8
8 8 6 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8 8 8 8
8 8 6 8 8 8 8 8 8 8 8 8 6 8 8 8 8 1 8 8 8 8 8
8 8 6 6 6 6 6 6 6 6 6 6 6 8 8 8 1 1 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 4 4 4 4 4 4 4 4 4 4 4 8 8 8 8 8 8 8 8 8 8
8 8 4 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8 8 8 8 8 8
8 8 4 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8 8 8 8 8 8
8 8 4 8 8 8 8 8 8 8 8 8 4 8 8 6 8 8 8 8 8 8 8
8 8 4 4 4 4 4 4 4 4 4 4 4 8 8 6 8 6 6 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 1 1 1 1 1 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8
8 8 1 8 8 8 8 8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8
8 8 1 8 8 8 8 8 8 8 1 8 1 8 8 8 8 8 8 8 8 8 8
8 8 1 8 8 8 8 8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8
8 8 1 1 1 1 1 1 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 6 6 6 6 6 6 6 6 6 6 6 8 8 8 8 8 8 8 8 8 8
8 8 6 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8 8 8 8
8 8 6 8 8 8 6 8 6 8 6 8 6 8 8 8 8 8 8 8 8 8 8
8 8 6 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8 8 8 8
8 8 6 6 6 6 6 6 6 6 6 6 6 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 4 4 4 4 4 4 4 4 4 4 4 8 8 8 8 8 8 8 8 8 8
8 8 4 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8 8 8 8 8 8
8 8 4 8 8 8 8 8 4 8 4 8 4 8 8 8 8 8 8 8 8 8 8
8 8 4 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8 8 8 8 8 8
8 8 4 4 4 4 4 4 4 4 4 4 4 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 6 8
8 8 1 1 1 1 1 1 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8
8 8 1 8 8 8 8 8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8
8 8 1 8 1 8 1 8 1 8 1 8 1 8 8 8 8 8 8 8 8 8 8
8 8 1 8 8 8 8 8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8
8 8 1 1 1 1 1 1 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 6 6 6 6 6 6 6 6 6 6 6 8 8 2 2 8 8 8 8 8 8
8 8 6 8 8 8 8 8 8 8 8 8 6 8 8 2 2 8 8 8 8 8 8
8 8 6 8 6 8 6 8 6 8 6 8 6 8 8 8 8 8 8 8 8 8 8
8 8 6 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8 8 8 8
8 8 6 6 6 6 6 6 6 6 6 6 6 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 4 4 4 4 4 4 4 4 4 4 4 8 8 8 8 8 8 8 8 8 8
8 8 4 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8 8 8 8 8 8
8 8 4 8 4 8 4 8 4 8 4 8 4 8 8 8 8 8 8 8 8 8 8
8 8 4 8 8 8 8 8 8 8 8 8 4 8 8 6 8 8 8 8 8 8 8
8 8 4 4 4 4 4 4 4 4 4 4 4 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 14
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 10.586011342155018

## Example 3:
Input:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 2 2 2 2 2 2 2 2 2 2 2 3 3 3 3 1 3 3 3 3 3 3
3 2 3 3 3 3 3 3 3 3 3 2 3 3 3 1 1 1 3 3 3 3 3
3 2 3 3 3 3 3 3 3 3 3 2 3 3 3 1 1 1 3 3 3 3 3
3 2 3 3 3 3 3 3 3 3 3 2 3 3 3 3 1 3 3 3 3 3 3
3 2 2 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 4 4 4 4 4 4 4 4 4 4 4 3 3 3 8 3 3 3 1 1 3 3
3 4 3 3 3 3 3 3 3 3 3 4 3 3 8 8 8 3 1 1 1 1 3
3 4 3 3 3 3 3 3 3 3 3 4 3 3 3 8 3 3 3 1 1 3 3
3 4 3 3 3 3 3 3 3 3 3 4 3 3 3 3 3 3 3 3 3 3 3
3 4 4 4 4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 1 1 1 1 1 1 1 1 1 1 1 3 3 3 3 3 4 3 3 3 3 3
3 1 3 3 3 3 3 3 3 3 3 1 3 3 3 3 4 4 4 3 3 3 3
3 1 3 3 3 3 3 3 3 3 3 1 3 3 3 3 3 4 3 3 3 3 3
3 1 3 3 3 3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3
3 1 1 1 1 1 1 1 1 1 1 1 3 3 3 3 3 3 4 4 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 4 4 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Expected Output:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 2 2 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3 3 3
3 2 3 3 3 3 3 3 3 3 3 2 3 3 3 3 3 3 3 3 3 3 3
3 2 3 3 3 3 3 3 3 3 3 2 3 3 3 3 3 3 3 3 3 3 3
3 2 3 3 3 3 3 3 3 3 3 2 3 3 3 3 3 3 3 3 3 3 3
3 2 2 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 4 4 4 4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 3 3 3
3 4 3 3 3 3 3 3 3 3 3 4 3 3 3 3 3 3 3 3 3 3 3
3 4 3 3 3 3 3 4 3 4 3 4 3 3 3 3 3 3 3 3 3 3 3
3 4 3 3 3 3 3 3 3 3 3 4 3 3 3 3 3 3 3 3 3 3 3
3 4 4 4 4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 1 1 1 1 1 1 1 1 1 1 1 3 3 3 3 3 3 3 3 3 3 3
3 1 3 3 3 3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3
3 1 3 3 3 3 3 1 3 1 3 1 3 3 3 3 3 3 3 3 3 3 3
3 1 3 3 3 3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3
3 1 1 1 1 1 1 1 1 1 1 1 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 2 2 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3 3 3
3 2 3 3 3 3 3 3 3 3 3 2 3 3 3 3 3 3 3 3 3 3 3
3 2 3 2 3 2 3 2 3 2 3 2 3 3 3 3 3 3 3 3 3 3 3
3 2 3 3 3 3 3 3 3 3 3 2 3 3 3 3 3 3 3 3 3 3 3
3 2 2 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 4 4 4 4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 3 3 3
3 4 3 3 3 3 3 3 3 3 3 4 3 3 3 3 3 3 3 3 3 3 3
3 4 3 4 3 4 3 4 3 4 3 4 3 3 3 3 3 3 3 3 3 3 3
3 4 3 3 3 3 3 3 3 3 3 4 3 3 3 3 3 3 3 3 3 3 3
3 4 4 4 4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 1 1 1 1 1 1 1 1 1 1 1 3 3 3 3 3 3 3 3 3 3 3
3 1 3 3 3 3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3
3 1 3 1 3 1 3 1 3 1 3 1 3 3 3 3 3 3 3 3 3 3 3
3 1 3 3 3 3 3 3 3 3 3 1 3 3 3 3 3 3 3 3 3 3 3
3 1 1 1 1 1 1 1 1 1 1 1 3 3 3 3 3 3 4 4 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 4 4 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 5.217391304347814
