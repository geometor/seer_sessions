```python
import numpy as np
from collections import deque

"""
Transformation Rule Description:
1. Define the border color as Yellow (4) and the background color as White (0).
2. Identify all distinct objects within the input grid. An object is a contiguous group of pixels of the same color, where the color is neither the border color nor the background color.
3. Determine which of these objects are "enclosed". An object is enclosed if:
    a. None of its pixels touch the absolute outer edges of the grid.
    b. All pixels immediately adjacent (up, down, left, right) to the object's pixels are either part of the object itself, the border color (Yellow/4), or the background color (White/0).
4. Collect the color, coordinates, and bounding box (specifically the top-left corner coordinates: min_row, min_col) of each enclosed object.
5. Examine the colors of all identified enclosed objects.
6. Apply the selection rule:
    a. Rule A: If the color Blue (1) is *not* present among the colors of the enclosed objects, select the enclosed object whose color is Azure (8).
    b. Rule B: If the color Blue (1) *is* present among the colors of the enclosed objects, select the object whose bounding box top-left corner (`min_row`, `min_col`) is the minimum lexicographically (i.e., smallest `min_row`, breaking ties with the smallest `min_col`).
7. Isolate the selected object's pixels and its bounding box dimensions.
8. Create the output grid: its dimensions match the height and width of the selected object's bounding box. Initialize this grid with the background color (White/0).
9. Copy the pixels from the selected object onto the output grid, preserving their color and relative positions. A pixel from the input grid at coordinates `(r, c)` belonging to the selected object is placed at coordinates `(r - min_row, c - min_col)` in the output grid, where `min_row` and `min_col` are from the selected object's bounding box.
"""

# --- Constants ---
BORDER_COLOR = 4  # Yellow
BACKGROUND_COLOR = 0  # White
BLUE = 1
AZURE = 8

# --- Helper Functions ---

def is_enclosed(grid, component_coords):
    """
    Checks if a component (set of coordinates) is enclosed according to the rules:
    - Not touching the grid edge.
    - Adjacent non-component pixels are only BORDER_COLOR or BACKGROUND_COLOR.
    """
    height, width = grid.shape
    if not component_coords:
        return False # An empty component cannot be enclosed

    # Check if any pixel touches the edge
    for r, c in component_coords:
        if r == 0 or r == height - 1 or c == 0 or c == width - 1:
            return False # Touches edge, not enclosed

    # Check neighbors of all component pixels
    for r, c in component_coords:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4-directional neighbors
            nr, nc = r + dr, c + dc

            # Neighbor coordinates are guaranteed to be within bounds because
            # we already checked that component pixels are not on the edge.
            # Check if the neighbor is outside the component
            if (nr, nc) not in component_coords:
                neighbor_color = grid[nr, nc]
                # If an adjacent pixel is *not* part of the object,
                # it *must* be either BORDER or BACKGROUND color.
                if neighbor_color != BORDER_COLOR and neighbor_color != BACKGROUND_COLOR:
                    return False # Found an adjacent pixel of another color

    # If all checks passed for all coordinates
    return True

def find_enclosed_objects(grid):
    """
    Finds all enclosed objects in the grid.
    Returns a list of dictionaries, each containing object info:
    'color', 'coords', 'bbox', 'top_left'.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    enclosed_objects = []

    for r in range(height):
        for c in range(width):
            pixel_color = grid[r, c]
            # Start BFS only if it's a potential object color (non-border, non-background)
            # and hasn't been visited as part of another object yet.
            if pixel_color != BORDER_COLOR and pixel_color != BACKGROUND_COLOR and not visited[r, c]:
                object_color = pixel_color
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c, max_r, max_c = r, c, r, c

                # Perform BFS to find all connected pixels of the *same* color
                while q:
                    curr_r, curr_c = q.popleft()
                    component_coords.add((curr_r, curr_c))

                    # Update bounding box dynamically
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check neighbor validity: within bounds, same color, not visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == object_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # After finding the full component, check if it's enclosed
                if is_enclosed(grid, component_coords):
                     enclosed_objects.append({
                        'color': object_color,
                        'coords': component_coords,
                        'bbox': (min_r, min_c, max_r, max_c),
                        'top_left': (min_r, min_c) # Store for easier sorting
                    })

    return enclosed_objects

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # 1-4: Find all enclosed objects and their properties
    enclosed_objects_data = find_enclosed_objects(input_grid)

    # Check if any enclosed objects were found
    if not enclosed_objects_data:
        # Behavior for no enclosed objects isn't strictly defined by examples.
        # Returning an empty grid or raising an error are options.
        # Let's raise an error for clarity during testing.
        raise ValueError("No objects enclosed by the border/background were found.")

    # 5: Examine the colors of all enclosed objects.
    enclosed_colors = {obj['color'] for obj in enclosed_objects_data}

    # 6: Apply the selection rule.
    selected_object = None
    if BLUE not in enclosed_colors:
        # Rule A: Blue is absent, select Azure.
        azure_found = False
        for obj in enclosed_objects_data:
            if obj['color'] == AZURE:
                selected_object = obj
                azure_found = True
                break
        if not azure_found:
             # This case implies an assumption was violated (Azure should be present if Blue isn't)
             raise ValueError(f"Rule conflict: Blue ({BLUE}) is absent, but required Azure ({AZURE}) object not found among enclosed objects.")
    else:
        # Rule B: Blue is present, select the top-leftmost object.
        # Sort by top_left: first by row (index 0), then by column (index 1)
        enclosed_objects_data.sort(key=lambda x: x['top_left'])
        # Since we know Blue is present, the list cannot be empty here.
        selected_object = enclosed_objects_data[0]

    # If selected_object is still None here, something went wrong in the logic above.
    if selected_object is None:
         raise ValueError("Could not select an object based on the rules after processing.")

    # 7: Isolate selected object properties
    sel_color = selected_object['color']
    sel_coords = selected_object['coords']
    min_r, min_c, max_r, max_c = selected_object['bbox']

    # 8: Create the output grid based on bounding box size
    output_h = max_r - min_r + 1
    output_w = max_c - min_c + 1
    output_grid = np.full((output_h, output_w), BACKGROUND_COLOR, dtype=int)

    # 9: Copy selected object pixels to the output grid with relative positioning
    for r, c in sel_coords:
        output_r = r - min_r
        output_c = c - min_c
        # Double check bounds just in case, though bbox should guarantee this
        if 0 <= output_r < output_h and 0 <= output_c < output_w:
             output_grid[output_r, output_c] = sel_color
        else:
             # This indicates an issue with coordinate mapping or bounding box calculation
             print(f"Warning: Coordinate ({r},{c}) mapped outside output grid bounds ({output_h}x{output_w}) during pixel copy.")

    return output_grid
```