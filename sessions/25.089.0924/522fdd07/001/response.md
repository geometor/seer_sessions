```python
import numpy as np

"""
Transforms an input grid based on the properties of non-background objects (assumed to be solid rectangles).

The transformation rule depends on the presence of exactly one 1x1 object:

1. If exactly one 1x1 non-background object exists in the input grid:
   - This 1x1 object expands into a 9x9 square of the same color, centered at the original pixel's location, in the output grid.
   - All other non-background objects in the input grid shrink by removing their outer layer (1 pixel from each side). An object of size WxH becomes (W-2)x(H-2). Objects smaller than 3x3 in either dimension disappear after shrinking.

2. If the number of 1x1 non-background objects is not exactly one (zero or more than one):
   - All non-background objects shrink by removing their outer layer, as described above.

The background color (orange, 7) remains unchanged unless overwritten by expanding or shrinking objects.
"""

def find_objects(grid, background_color=7):
    """
    Finds all contiguous objects of the same color, excluding the background color.
    Assumes objects are solid rectangles based on task description.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color to ignore.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color', 'pixels' (set of (r, c) tuples), and
              'bbox' (tuple: min_r, min_c, max_r, max_c).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != background_color:
                color = grid[r, c]
                obj_pixels = set()
                q = [(r, c)]
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.pop(0)
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity should be sufficient for solid rectangles)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def draw_rectangle(grid, r1, c1, r2, c2, color):
    """Draws a solid rectangle on the grid, handling boundary conditions."""
    rows, cols = grid.shape
    min_r = max(0, r1)
    min_c = max(0, c1)
    max_r = min(rows - 1, r2)
    max_c = min(cols - 1, c2)
    if min_r <= max_r and min_c <= max_c:
        grid[min_r:max_r + 1, min_c:max_c + 1] = color


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list or np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    background_color = 7

    # Initialize output grid with background color
    output_grid = np.full_like(input_np, background_color)

    # Find all non-background objects
    objects = find_objects(input_np, background_color)

    # Count 1x1 objects and identify the expanding one if applicable
    one_by_one_objects = []
    other_objects = []
    expander_obj = None

    for obj in objects:
        min_r, min_c, max_r, max_c = obj['bbox']
        height = max_r - min_r + 1
        width = max_c - min_c + 1
        if height == 1 and width == 1:
            one_by_one_objects.append(obj)
        else:
            other_objects.append(obj)

    # Determine if the special expansion case applies
    apply_expansion = len(one_by_one_objects) == 1
    if apply_expansion:
        expander_obj = one_by_one_objects[0]

    # Apply transformations
    if apply_expansion:
        # Case 1: Expand the 1x1 object and shrink others
        print(f"Found one 1x1 object. Expanding.")
        
        # Expand the 1x1 object
        r, c = list(expander_obj['pixels'])[0] # Get the single pixel coordinate
        color = expander_obj['color']
        draw_rectangle(output_grid, r - 4, c - 4, r + 4, c + 4, color)
        print(f"  Expanded object {expander_obj['color']} at ({r},{c}) to 9x9.")


        # Shrink other objects
        for obj in other_objects:
            min_r, min_c, max_r, max_c = obj['bbox']
            height = max_r - min_r + 1
            width = max_c - min_c + 1
            color = obj['color']

            if width >= 3 and height >= 3:
                draw_rectangle(output_grid, min_r + 1, min_c + 1, max_r - 1, max_c - 1, color)
                print(f"  Shrunk object {color} from {width}x{height} to {width-2}x{height-2}.")
            else:
                 print(f"  Object {color} ({width}x{height}) disappeared after shrinking.")


    else:
        # Case 2: Shrink all objects (including any 1x1 or larger ones)
        print(f"Found {len(one_by_one_objects)} 1x1 objects. Shrinking all.")
        for obj in objects: # Process all original objects
            min_r, min_c, max_r, max_c = obj['bbox']
            height = max_r - min_r + 1
            width = max_c - min_c + 1
            color = obj['color']

            if width >= 3 and height >= 3:
                draw_rectangle(output_grid, min_r + 1, min_c + 1, max_r - 1, max_c - 1, color)
                print(f"  Shrunk object {color} from {width}x{height} to {width-2}x{height-2}.")
            else:
                 print(f"  Object {color} ({width}x{height}) disappeared after shrinking.")


    return output_grid.tolist() # Return as list of lists per ARC standard

```