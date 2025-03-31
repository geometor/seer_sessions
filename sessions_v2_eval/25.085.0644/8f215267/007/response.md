```python
import numpy as np
from collections import Counter

"""
Transforms a grid by identifying strictly hollow rectangular shapes (width > 2, height > 2, 1-pixel border, background interior), 
modifying their interior based on background color parity, and removing all other non-background shapes.

1.  **Identify Background**: Determine the most frequent color (`background_color`) and its parity (`background_parity`).
2.  **Initialize Output**: Create an output grid of the same dimensions, filled with `background_color`.
3.  **Find Connected Components**: Use a connected components search (like BFS) to find groups of connected, non-background pixels of the same color.
4.  **Filter for Hollow Rectangles**: 
    *   For each component, check if it forms a valid "hollow rectangle":
        *   Must consist of a single color (`rectangle_color`).
        *   Calculate its bounding box (min/max row/col).
        *   Bounding box `height` and `width` must both be strictly greater than 2.
        *   Must form a single-pixel thick rectangular border (check pixel count against expected perimeter).
        *   The area strictly inside the border must contain only the `background_color` in the input grid.
    *   Keep only the components that satisfy all these conditions.
5.  **Draw Borders**: Draw the border pixels of each identified hollow rectangle onto the output grid using its `rectangle_color`.
6.  **Apply Midline Pattern**: For each identified hollow rectangle:
    *   Calculate the row index of the horizontal midline of its *internal* area.
    *   Identify the column indices corresponding to the *internal* area.
    *   Iterate through these internal columns. If a column index's parity is **different** from the `background_parity` (`col % 2 != background_parity`), color the corresponding pixel on the midline row in the output grid with the `rectangle_color`.
7.  **Return**: The modified output grid. All shapes not identified as hollow rectangles are effectively removed as they are not drawn onto the background-filled output grid.
"""

def _get_background_color(grid: np.ndarray) -> int:
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    # Handle potential ties by picking the most frequent; ARC usually has clear background
    if not counts:
        return 0 # Default to white if grid is empty
    background_color = counts.most_common(1)[0][0]
    return background_color

def _find_connected_components(grid: np.ndarray, background_color: int) -> list:
    """
    Finds connected components of non-background colors using BFS.
    Returns a list of components, where each component is a dict 
    containing {"color": color_value, "coords": list_of_tuples}.
    Uses 4-way connectivity (up, down, left, right) for defining components.
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

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
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


def _is_strict_hollow_rectangle(grid: np.ndarray, component_coords: list, background_color: int) -> tuple:
    """
    Checks if a component defined by coords is a STRICT hollow rectangle.
    STRICT means: 1-pixel border, height > 2, width > 2, interior is background.
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

    # 1. CRITICAL CHECK: Must have height > 2 AND width > 2 to have an interior
    if not (height > 2 and width > 2):
        return False, -1, None

    # 2. Check if all component pixels lie on the bounding box edges
    on_border = True
    for r, c in component_coords:
        if not (r == min_r or r == max_r or c == min_c or c == max_c):
            on_border = False
            break
    if not on_border:
        return False, -1, None
        
    # 3. Check if the number of pixels matches the perimeter for single thickness
    # Perimeter = 2 * (height + width - 2) for rectangles with H>1, W>1
    expected_perimeter_pixels = 2 * (height + width - 2)
    if len(component_coords) != expected_perimeter_pixels :
         return False, -1, None

    # 4. Check internal area for background color
    # This slice is guaranteed to exist because height > 2 and width > 2
    internal_slice = grid[min_r + 1:max_r, min_c + 1:max_c]
    if not np.all(internal_slice == background_color):
        return False, -1, None
            
    # If all checks pass
    bounding_box = (min_r, min_c, max_r, max_c)
    return True, rect_color, bounding_box


def transform(input_grid: list) -> list:
    """
    Applies the transformation: finds STRICT hollow rectangles, copies their borders,
    draws a pattern on the internal midline based on the opposite of the background parity, 
    and removes all other shapes.
    """
    # Convert input to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # 1. Identify Background Color and Parity
    background_color = _get_background_color(input_array)
    background_parity = background_color % 2 # 0 for even, 1 for odd

    # 2. Initialize Output Grid - CRITICAL: Start with clean background
    output_grid = np.full_like(input_array, background_color)

    # 3. Find Connected Components (potential shapes)
    components = _find_connected_components(input_array, background_color)

    # Store valid hollow rectangles found
    hollow_rectangles = [] 
    
    # 4. Validate each component to find STRICT hollow rectangles
    for component in components:
        coords = component["coords"]
        is_valid, rect_color, bbox = _is_strict_hollow_rectangle(
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

    # 5. Draw Rectangle Borders onto Output
    for rect in hollow_rectangles:
        rect_color = rect["color"]
        for r, c in rect["coords"]:
            # Basic bounds check (should always be true if coords are from grid)
            if 0 <= r < height and 0 <= c < width:
                output_grid[r, c] = rect_color

    # 6. Apply Midline Pattern to the identified hollow rectangles
    for rect in hollow_rectangles:
        rect_color = rect["color"]
        min_r, min_c, max_r, max_c = rect["bbox"]
        
        # Calculate internal dimensions (guaranteed > 0 due to validation)
        internal_height = max_r - min_r - 1
        internal_width = max_c - min_c - 1

        # Calculate midline row index relative to the top of the grid
        # Add min_r + 1 (start of internal area) to the relative midline index
        midline_row = min_r + 1 + (internal_height // 2) 

        # Iterate through internal column indices
        start_col = min_c + 1
        end_col = max_c # The range stops *before* end_col, corresponding to max_c - 1

        for col in range(start_col, end_col):
            # *** CORRECTED LOGIC ***
            # Check if column index parity is DIFFERENT from background parity
            if col % 2 != background_parity: 
                # Check bounds just in case (should be within grid)
                if 0 <= midline_row < height and 0 <= col < width:
                     # Since output_grid was initialized with background, we can directly color
                     output_grid[midline_row, col] = rect_color

    # 7. Return Output as list of lists
    return output_grid.tolist()
```