
Previous Code:
```python
import numpy as np
from collections import deque, Counter

"""
Transformation Rule:

1.  Isolate the top 6 rows as the 'Palette' and the rest as the 'Canvas'. Handle grids too small for a standard palette.
2.  Identify the 'paintable background color' as the single most frequent color in the initial Canvas, excluding azure (8).
3.  Locate all initial azure (8) pixels in the Canvas; these are the 'seeds'.
4.  Perform an 8-way connected flood fill starting from the seeds. The fill propagates only onto adjacent pixels whose color matches the identified 'paintable background color'.
5.  Pixels that are filled become azure (8). All other colors (including original seeds and any other colors present) act as barriers.
6.  The final output is the modified Canvas grid after the flood fill is complete.
"""

def get_background_color(canvas):
    """
    Identifies the single most frequent background color in the canvas, excluding azure (8).

    Args:
        canvas (np.ndarray): The canvas section of the input grid.

    Returns:
        int or None: The integer representing the background color, or None if no suitable background is found.
    """
    if canvas.size == 0:
        return None # Handle empty canvas

    canvas_colors, counts = np.unique(canvas, return_counts=True)
    color_counts = Counter(dict(zip(canvas_colors, counts)))

    # Remove azure (8) from consideration for background
    if 8 in color_counts:
        del color_counts[8]

    # Find the most frequent remaining color
    if color_counts:
        background_color = color_counts.most_common(1)[0][0]
        return int(background_color) # Ensure it's a standard int
    else:
        # Handle cases where the canvas only contains azure or is empty after excluding azure.
        return None

def transform(input_grid):
    """
    Applies the flood fill transformation based on canvas background color.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid (canvas section only).
    """
    input_grid_np = np.array(input_grid, dtype=np.int64) # Use numpy for easier manipulation

    # 1. Isolate Sections
    # Assume palette is always the top 6 rows if grid height allows
    palette_rows = 6 if input_grid_np.shape[0] > 6 else 0 # Handle grids too small for a palette
    if palette_rows > 0:
        # palette = input_grid_np[:palette_rows, :] # Palette isn't directly used in this logic
        canvas = input_grid_np[palette_rows:, :]
    else:
        # If no distinct palette possible, treat the whole grid as canvas
        canvas = input_grid_np

    # Handle case where canvas might be empty after splitting
    if canvas.size == 0:
        return [] # Return empty list for empty canvas

    output_canvas = canvas.copy()
    canvas_h, canvas_w = canvas.shape

    # 2. Identify Paintable Background Color
    paintable_color = get_background_color(canvas)

    # If no paintable background color exists (e.g., canvas only has azure or is empty),
    # no filling can occur, return the original canvas.
    if paintable_color is None:
        return output_canvas.tolist()

    # 3. Locate Azure Seeds
    seed_points = deque()
    initial_azure_locations = set() # Keep track of original seeds
    for r in range(canvas_h):
        for c in range(canvas_w):
            if canvas[r, c] == 8:
                # Add seeds to the queue *and* the visited set
                # This prevents seeds from being immediately repainted if adjacent to background
                seed_tuple = (r, c)
                if seed_tuple not in initial_azure_locations:
                    seed_points.append(seed_tuple)
                    initial_azure_locations.add(seed_tuple)

    # 4 & 5. Perform Flood Fill
    visited_for_fill = set(initial_azure_locations) # Start visited set with seeds

    while seed_points:
        r, c = seed_points.popleft()

        # Check 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue # Skip self

                nr, nc = r + dr, c + dc

                # Check boundaries
                if 0 <= nr < canvas_h and 0 <= nc < canvas_w:
                    neighbor_loc = (nr, nc)

                    # Check if not visited AND color matches the paintable background color
                    if neighbor_loc not in visited_for_fill:
                        current_neighbor_color = output_canvas[nr, nc]
                        if current_neighbor_color == paintable_color:
                            output_canvas[nr, nc] = 8 # Paint it azure
                            visited_for_fill.add(neighbor_loc)
                            seed_points.append(neighbor_loc) # Add to queue for further expansion

    # 6. Final Output
    return output_canvas.tolist() # Return as list of lists per ARC format
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 1 0 0 0 5 5 6 0 0 0 5 5 4 0 0 0 5 5 2 0 0 0 5
5 1 0 0 0 5 5 6 0 0 0 5 5 4 0 0 0 5 5 2 0 0 0 5
5 1 0 0 0 5 5 6 0 0 0 5 5 4 0 0 0 5 5 2 0 0 0 5
5 1 0 0 0 5 5 6 0 0 0 5 5 4 0 0 0 5 5 2 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
1 1 1 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
1 1 1 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 4 4 4 4 3 3
1 1 1 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 4 4 4 4 3 3
1 1 1 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 4 4 4 4 3 3
1 1 1 1 3 3 3 3 8 8 3 3 3 3 3 3 3 3 4 4 4 4 3 3
1 1 1 1 3 3 3 3 8 8 3 3 3 3 3 3 3 3 4 4 4 4 3 3
1 1 1 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 4 4 4 4 3 3
1 1 1 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 4 4 4 4 3 3
1 1 1 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 2 2 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3
3 3 3 3 2 2 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3
3 3 3 3 2 2 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3
```
Expected Output:
```
3 3 3 3 3 3 3 3 8 8 3 3 3 3 3 3 8 8 3 3 3 3 3 3
3 3 3 3 3 3 3 3 8 8 3 3 3 3 3 3 8 8 3 3 3 3 3 3
3 3 3 3 3 3 3 3 8 8 3 3 3 3 3 3 8 8 3 3 3 3 3 3
1 1 1 1 3 3 3 3 8 8 3 3 3 3 3 3 8 8 3 3 3 3 3 3
1 1 1 1 3 3 3 3 8 8 3 3 3 3 3 3 8 8 4 4 4 4 3 3
1 1 1 1 3 3 3 3 8 8 3 3 3 3 3 3 8 8 4 4 4 4 3 3
1 1 1 1 3 3 3 3 8 8 3 3 3 3 3 3 8 8 4 4 4 4 3 3
1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 4 4 3 3
1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 4 4 3 3
1 1 1 1 8 8 3 3 8 8 3 3 3 3 3 3 3 3 4 4 4 4 3 3
1 1 1 1 8 8 3 3 8 8 3 3 3 3 3 3 3 3 4 4 4 4 3 3
1 1 1 1 8 8 3 3 8 8 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 8 8 3 3 8 8 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 8 8 3 3 8 8 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
3 3 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
3 3 3 3 2 2 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3
3 3 3 3 2 2 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3
3 3 3 3 2 2 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 4 4 8 8
1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 4 4 8 8
1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 4 4 8 8
1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 4 4 8 8
1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 4 4 8 8
1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 4 4 8 8
1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 4 4 8 8
1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 243
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 106.57894736842105

## Example 2:
Input:
```
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 2 5 5 4 0 0 0 5 5 0 0 0 6 5 5 3 0 0 0 5
5 0 0 0 2 5 5 4 0 0 0 5 5 0 0 0 6 5 5 3 0 0 0 5
5 0 0 0 2 5 5 4 0 0 0 5 5 0 0 0 6 5 5 3 0 0 0 5
5 0 0 0 2 5 5 4 0 0 0 5 5 0 0 0 6 5 5 3 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
1 1 1 1 1 1 1 1 1 1 1 1 1 6 6 6 6 6 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 6 6 6 6 6 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 3 3 3 3 1 1 1 1
2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 3 3 3 3 1 1 1 1
2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 3 3 3 3 1 1 1 1
2 2 2 2 1 1 1 1 8 8 1 1 1 1 1 1 3 3 3 3 1 1 1 1
2 2 2 2 1 1 1 1 8 8 1 1 1 1 1 1 3 3 3 3 1 1 1 1
2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 3 3 3 3 1 1 1 1
2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 4 4 4 4 4 4 4 4 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 4 4 4 4 4 4 4 4 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 4 4 4 4 4 4 4 4 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
1 1 1 1 8 8 1 1 8 8 1 1 1 6 6 6 6 6 1 1 1 1 1 1
1 1 1 1 8 8 1 1 8 8 1 1 1 6 6 6 6 6 1 1 1 1 1 1
1 1 1 1 8 8 1 1 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8
1 1 1 1 8 8 1 1 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8
1 1 1 1 8 8 1 1 8 8 1 1 1 1 8 8 1 1 1 1 1 1 1 1
2 2 2 2 8 8 1 1 8 8 1 1 1 1 8 8 3 3 3 3 1 1 1 1
2 2 2 2 8 8 1 1 8 8 1 1 1 1 8 8 3 3 3 3 1 1 1 1
2 2 2 2 8 8 1 1 8 8 1 1 1 1 8 8 3 3 3 3 1 1 1 1
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 3 3 3 3 1 1 1 1
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 3 3 3 3 1 1 1 1
2 2 2 2 1 1 1 1 8 8 1 1 1 1 1 1 3 3 3 3 1 1 1 1
2 2 2 2 1 1 1 1 8 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 8 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 8 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
1 1 1 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
1 1 1 1 1 4 4 4 4 4 4 4 4 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 4 4 4 4 4 4 4 4 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 4 4 4 4 4 4 4 4 1 1 1 1 1 1 1 1 1 1 1
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 6 6 6 6 6 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 6 6 6 6 6 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 3 3 3 3 8 8 8 8
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 3 3 3 3 8 8 8 8
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 3 3 3 3 8 8 8 8
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 3 3 3 3 8 8 8 8
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 3 3 3 3 8 8 8 8
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 3 3 3 3 8 8 8 8
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 4 4 4 4 4 4 4 4 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 4 4 4 4 4 4 4 4 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 4 4 4 4 4 4 4 4 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 246
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 107.89473684210526

## Example 3:
Input:
```
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 4 5 5 6 0 0 0 5 5 3 0 0 0 5 5 0 0 0 2 5
5 0 0 0 4 5 5 6 0 0 0 5 5 3 0 0 0 5 5 0 0 0 2 5
5 0 0 0 4 5 5 6 0 0 0 5 5 3 0 0 0 5 5 0 0 0 2 5
5 0 0 0 4 5 5 6 0 0 0 5 5 3 0 0 0 5 5 0 0 0 2 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
7 7 7 7 7 7 7 7 3 3 3 3 3 3 3 3 3 3 7 7 7 7 7 7
7 7 7 7 7 7 7 7 3 3 3 3 3 3 3 3 3 3 7 7 7 7 7 7
7 7 7 7 7 7 7 7 3 3 3 3 3 3 3 3 3 3 7 7 7 7 7 7
7 7 7 7 7 7 7 7 3 3 3 3 3 3 3 3 3 3 7 7 6 6 6 6
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 6 6 6 6
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 6 6 6 6
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 6 6 6 6
2 2 2 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 6 6 6 6
2 2 2 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 6 6 6 6
2 2 2 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 6 6 6 6
2 2 2 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 6 6 6 6
2 2 2 7 7 7 7 7 7 7 7 7 8 8 7 7 7 7 7 7 6 6 6 6
2 2 2 7 7 7 7 7 7 7 7 7 8 8 7 7 7 7 7 7 6 6 6 6
2 2 2 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 6 6 6 6
2 2 2 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
2 2 2 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
2 2 2 7 7 7 7 7 4 4 4 4 4 4 4 4 4 4 4 4 4 4 7 7
2 2 2 7 7 7 7 7 4 4 4 4 4 4 4 4 4 4 4 4 4 4 7 7
2 2 2 7 7 7 7 7 4 4 4 4 4 4 4 4 4 4 4 4 4 4 7 7
```
Expected Output:
```
7 7 7 8 8 7 7 7 3 3 3 3 3 3 3 3 3 3 8 8 7 7 7 7
7 7 7 8 8 7 7 7 3 3 3 3 3 3 3 3 3 3 8 8 7 7 7 7
7 7 7 8 8 7 7 7 3 3 3 3 3 3 3 3 3 3 8 8 7 7 7 7
7 7 7 8 8 7 7 7 3 3 3 3 3 3 3 3 3 3 8 8 6 6 6 6
8 8 8 8 8 8 8 8 8 8 8 8 8 8 7 7 7 7 8 8 6 6 6 6
8 8 8 8 8 8 8 8 8 8 8 8 8 8 7 7 7 7 8 8 6 6 6 6
7 7 7 8 8 7 7 7 7 7 7 7 8 8 7 7 7 7 8 8 6 6 6 6
2 2 2 8 8 7 7 7 7 7 7 7 8 8 7 7 7 7 8 8 6 6 6 6
2 2 2 8 8 7 7 7 7 7 7 7 8 8 7 7 7 7 8 8 6 6 6 6
2 2 2 8 8 7 7 7 7 7 7 7 8 8 7 7 7 7 8 8 6 6 6 6
2 2 2 8 8 7 7 7 7 7 7 7 8 8 7 7 7 7 8 8 6 6 6 6
2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 6 6 6
2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 6 6 6
2 2 2 8 8 7 7 7 7 7 7 7 8 8 7 7 7 7 7 7 6 6 6 6
2 2 2 8 8 8 8 8 8 8 8 8 8 8 7 7 7 7 7 7 7 7 7 7
2 2 2 8 8 8 8 8 8 8 8 8 8 8 7 7 7 7 7 7 7 7 7 7
2 2 2 7 7 7 7 7 4 4 4 4 4 4 4 4 4 4 4 4 4 4 7 7
2 2 2 7 7 7 7 7 4 4 4 4 4 4 4 4 4 4 4 4 4 4 7 7
2 2 2 7 7 7 7 7 4 4 4 4 4 4 4 4 4 4 4 4 4 4 7 7
```
Transformed Output:
```
8 8 8 8 8 8 8 8 3 3 3 3 3 3 3 3 3 3 8 8 8 8 8 8
8 8 8 8 8 8 8 8 3 3 3 3 3 3 3 3 3 3 8 8 8 8 8 8
8 8 8 8 8 8 8 8 3 3 3 3 3 3 3 3 3 3 8 8 8 8 8 8
8 8 8 8 8 8 8 8 3 3 3 3 3 3 3 3 3 3 8 8 6 6 6 6
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 6 6 6
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 6 6 6
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 6 6 6
2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 6 6 6
2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 6 6 6
2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 6 6 6
2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 6 6 6
2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 6 6 6
2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 6 6 6
2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 6 6 6
2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
2 2 2 8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8 8
2 2 2 8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8 8
2 2 2 8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8 8
```
Match: False
Pixels Off: 156
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 68.42105263157893
