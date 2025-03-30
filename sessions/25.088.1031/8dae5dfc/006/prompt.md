
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transforms the input grid by processing each distinct non-background object. For each object, it identifies its nested layers by iteratively "peeling" from the outermost layer inwards based on adjacency to pixels outside the currently remaining part of the object. It then swaps the colors of these layers symmetrically, assigning the innermost layer's original color to the outermost layer in the output, the second innermost color to the second outermost layer, and so on.

1. Initialize the output grid as a copy of the input grid.
2. Identify all distinct connected components (objects) formed by non-white (0) pixels using 4-way adjacency.
3. For each identified object:
    a. Initialize an empty list `layers_data` to store pairs of (set_of_layer_pixels, layer_color).
    b. Initialize `remaining_object_pixels` with the coordinates of all pixels in the current object.
    c. **Iteratively Identify Layers (Peeling):**
        i. While `remaining_object_pixels` is not empty:
            A. Find all pixels in `remaining_object_pixels` that have at least one neighbor (4-way adjacent) which is *not* currently in `remaining_object_pixels`. These neighbors can be background pixels (0) or pixels belonging to previously identified layers of the *same* object.
            B. Store these identified pixels as `current_layer_pixels`.
            C. If `current_layer_pixels` is empty but `remaining_object_pixels` is not (e.g., disconnected inner core after peeling), treat all remaining pixels as the last layer.
            D. If `current_layer_pixels` is empty (and `remaining_object_pixels` is also empty), break the inner loop.
            E. Determine the `layer_color` from the first pixel in `current_layer_pixels` (assuming uniform color per layer based on examples).
            F. Append the tuple (`current_layer_pixels`, `layer_color`) to `layers_data`.
            G. Remove `current_layer_pixels` from `remaining_object_pixels`.
    d. **Swap Colors:**
        i. Extract the sequence of original colors from `layers_data`: `original_colors = [color for _, color in layers_data]`.
        ii. Create a reversed sequence: `reversed_colors = original_colors[::-1]`.
        iii. Iterate through the `layers_data` and `reversed_colors`. For the i-th layer (`layer_pixels`, _) in `layers_data`, get the i-th color from `reversed_colors`.
        iv. Update the `output_grid`: For each pixel (r, c) in `layer_pixels`, set `output_grid[r, c]` to the corresponding `reversed_color`.
4. Return the modified `output_grid`.
"""

def get_neighbors(r, c, h, w):
    """ Get valid 4-way neighbors for a cell (coordinates only) """
    neighbors = []
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < h and 0 <= nc < w:
            neighbors.append((nr, nc))
    return neighbors

def find_objects(grid):
    """ Finds connected components of non-background (0) pixels using BFS """
    h, w = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = [] # List to store sets of coordinates for each object

    for r in range(h):
        for c in range(w):
            # Start BFS if we find an unvisited non-background pixel
            if grid[r, c] != 0 and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    obj_coords.add((curr_r, curr_c)) # Add the pixel to the current object

                    # Explore neighbors
                    for nr, nc in get_neighbors(curr_r, curr_c, h, w):
                        # Add neighbor to queue if it's part of the object and not visited
                        if grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Add the completed object's coordinates to the list
                if obj_coords:
                    objects.append(obj_coords)
    return objects


def transform(input_grid_list):
    """
    Transforms the input grid by swapping the colors of symmetric layers within each object,
    identifying layers using an iterative peeling method.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.copy(input_grid)
    h, w = input_grid.shape

    # 1. Identify all distinct objects (connected components of non-background pixels)
    objects = find_objects(input_grid)

    # 2. Process each identified object independently
    for obj_coords in objects:
        layers_data = [] # Stores tuples: (set_of_layer_pixels, layer_color)
        remaining_object_pixels = obj_coords.copy() # Keep track of pixels not yet assigned to a layer

        # 3. Iteratively Identify Layers by "Peeling" from the outside in
        while remaining_object_pixels:
            current_layer_pixels = set()
            
            # Identify pixels in the remaining set that are adjacent to pixels *outside* the remaining set
            for r, c in remaining_object_pixels:
                is_boundary_pixel = False
                for nr, nc in get_neighbors(r, c, h, w):
                    # A pixel is on the boundary if any neighbor is not in the remaining set
                    if (nr, nc) not in remaining_object_pixels:
                        is_boundary_pixel = True
                        break
                if is_boundary_pixel:
                    current_layer_pixels.add((r, c))

            # If peeling doesn't find boundary pixels but pixels remain, they form the innermost core(s).
            # Assign all remaining pixels to the current (last) layer.
            if not current_layer_pixels and remaining_object_pixels:
                 current_layer_pixels = remaining_object_pixels.copy()

            # If no pixels were identified for the layer (and none remain), stop peeling.
            if not current_layer_pixels:
                 break

            # Determine the color of the layer (assuming uniform color per layer based on examples)
            # Take the color of the first pixel found in this layer.
            try:
                # Get an arbitrary pixel from the set to determine the layer's color
                first_pixel_r, first_pixel_c = next(iter(current_layer_pixels))
                layer_color = input_grid[first_pixel_r, first_pixel_c]
            except StopIteration:
                 # This should not happen if current_layer_pixels is not empty. Safety break.
                 print(f"Warning: Could not determine layer color for object containing {obj_coords}. Skipping object.")
                 break 

            # Store the identified layer's pixels and original color
            layers_data.append((current_layer_pixels, layer_color))

            # Remove the identified layer's pixels from the set of remaining pixels
            remaining_object_pixels -= current_layer_pixels

        # 4. Swap colors symmetrically if layers were successfully identified
        if layers_data:
            original_colors = [color for _, color in layers_data]
            reversed_colors = original_colors[::-1]

            # Ensure the number of layers matches the number of reversed colors
            # This check might fail for complex shapes with holes, but examples seem simpler
            if len(layers_data) == len(reversed_colors):
                # Iterate through the identified layers and apply the corresponding reversed color
                for i, (layer_pixels, _) in enumerate(layers_data):
                    new_color = reversed_colors[i]
                    for r, c in layer_pixels:
                        # Update the output grid with the new color
                        output_grid[r, c] = new_color
            else:
                 # Handle potential mismatch (e.g., complex shapes), though not expected based on examples
                 print(f"Warning: Layer count ({len(layers_data)}) mismatch with reversed colors ({len(reversed_colors)}). Applying partial transformation.")
                 min_len = min(len(layers_data), len(reversed_colors))
                 for i in range(min_len):
                     layer_pixels = layers_data[i][0]
                     new_color = reversed_colors[i]
                     for r, c in layer_pixels:
                         output_grid[r, c] = new_color

    # Convert the final grid back to a list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0
0 0 8 7 7 7 7 7 7 7 7 8 0 2 2 2 2 2 2
0 0 8 7 7 7 7 7 7 7 7 8 0 2 1 1 1 1 2
0 0 8 7 7 4 4 4 4 7 7 8 0 2 1 3 3 1 2
0 0 8 7 7 4 3 3 4 7 7 8 0 2 1 3 3 1 2
0 0 8 7 7 4 3 3 4 7 7 8 0 2 1 1 1 1 2
0 0 8 7 7 4 3 3 4 7 7 8 0 2 2 2 2 2 2
0 0 8 7 7 4 3 3 4 7 7 8 0 0 0 0 0 0 0
0 0 8 7 7 4 3 3 4 7 7 8 0 0 0 0 0 0 0
0 0 8 7 7 4 4 4 4 7 7 8 0 0 0 0 0 0 0
0 0 8 7 7 7 7 7 7 7 7 8 0 0 0 0 0 0 0
0 0 8 7 7 7 7 7 7 7 7 8 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 3 4 4 4 4 4 4 4 4 3 0 3 3 3 3 3 3
0 0 3 4 4 4 4 4 4 4 4 3 0 3 1 1 1 1 3
0 0 3 4 4 7 7 7 7 4 4 3 0 3 1 2 2 1 3
0 0 3 4 4 7 8 8 7 4 4 3 0 3 1 2 2 1 3
0 0 3 4 4 7 8 8 7 4 4 3 0 3 1 1 1 1 3
0 0 3 4 4 7 8 8 7 4 4 3 0 3 3 3 3 3 3
0 0 3 4 4 7 8 8 7 4 4 3 0 0 0 0 0 0 0
0 0 3 4 4 7 8 8 7 4 4 3 0 0 0 0 0 0 0
0 0 3 4 4 7 7 7 7 4 4 3 0 0 0 0 0 0 0
0 0 3 4 4 4 4 4 4 4 4 3 0 0 0 0 0 0 0
0 0 3 4 4 4 4 4 4 4 4 3 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 3 4 4 4 4 4 4 4 4 3 0 3 3 3 3 3 3
0 0 3 4 7 7 7 7 7 7 4 3 0 3 2 2 2 2 2
0 0 3 4 7 7 7 7 7 7 4 3 0 3 2 2 2 2 2
0 0 3 4 7 7 8 8 7 7 4 3 0 3 2 2 2 2 2
0 0 3 4 7 7 8 8 7 7 4 3 0 3 2 2 2 2 2
0 0 3 4 7 7 8 8 7 7 4 3 0 3 3 3 3 3 3
0 0 3 4 7 7 8 8 7 7 4 3 0 0 0 0 0 0 0
0 0 3 4 7 7 8 8 7 7 4 3 0 0 0 0 0 0 0
0 0 3 4 7 7 7 7 7 7 4 3 0 0 0 0 0 0 0
0 0 3 4 7 7 7 7 7 7 4 3 0 0 0 0 0 0 0
0 0 3 4 4 4 4 4 4 4 4 3 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 42
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 24.561403508771946

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 1 1 1 1 0 0
0 0 1 1 1 1 1 1 1 1 1 1 1 1 0 0
0 0 1 1 3 3 3 3 3 3 3 3 1 1 0 0
0 0 1 1 3 8 8 8 8 8 8 3 1 1 0 0
0 0 1 1 3 8 8 8 8 8 8 3 1 1 0 0
0 0 1 1 3 8 8 2 2 8 8 3 1 1 0 0
0 0 1 1 3 8 8 2 2 8 8 3 1 1 0 0
0 0 1 1 3 8 8 8 8 8 8 3 1 1 0 0
0 0 1 1 3 8 8 8 8 8 8 3 1 1 0 0
0 0 1 1 3 3 3 3 3 3 3 3 1 1 0 0
0 0 1 1 1 1 1 1 1 1 1 1 1 1 0 0
0 0 1 1 1 1 1 1 1 1 1 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0
0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0
0 0 2 2 8 8 8 8 8 8 8 8 2 2 0 0
0 0 2 2 8 3 3 3 3 3 3 8 2 2 0 0
0 0 2 2 8 3 3 3 3 3 3 8 2 2 0 0
0 0 2 2 8 3 3 1 1 3 3 8 2 2 0 0
0 0 2 2 8 3 3 1 1 3 3 8 2 2 0 0
0 0 2 2 8 3 3 3 3 3 3 8 2 2 0 0
0 0 2 2 8 3 3 3 3 3 3 8 2 2 0 0
0 0 2 2 8 8 8 8 8 8 8 8 2 2 0 0
0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0
0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0
0 0 2 8 8 8 8 8 8 8 8 8 8 2 0 0
0 0 2 8 8 8 8 8 8 8 8 8 8 2 0 0
0 0 2 8 8 3 3 3 3 3 3 8 8 2 0 0
0 0 2 8 8 3 1 1 1 1 3 8 8 2 0 0
0 0 2 8 8 3 1 1 1 1 3 8 8 2 0 0
0 0 2 8 8 3 1 1 1 1 3 8 8 2 0 0
0 0 2 8 8 3 1 1 1 1 3 8 8 2 0 0
0 0 2 8 8 3 3 3 3 3 3 8 8 2 0 0
0 0 2 8 8 8 8 8 8 8 8 8 8 2 0 0
0 0 2 8 8 8 8 8 8 8 8 8 8 2 0 0
0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 48
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 33.333333333333314

## Example 3:
Input:
```
8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
8 2 2 2 2 8 0 0 0 0 0 0 0 0 0 0 0
8 2 1 1 2 8 0 0 0 0 0 0 0 0 0 0 0
8 2 1 1 2 8 0 0 0 0 0 0 0 0 0 0 0
8 2 2 2 2 8 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 0
0 0 0 0 6 3 3 3 3 3 3 3 3 3 3 6 0
0 0 0 0 6 3 4 4 4 4 4 4 4 4 3 6 0
0 0 0 0 6 3 4 2 2 2 2 2 2 4 3 6 0
0 0 0 0 6 3 4 2 1 1 1 1 2 4 3 6 0
0 0 0 0 6 3 4 2 1 1 1 1 2 4 3 6 0
0 0 0 0 6 3 4 2 2 2 2 2 2 4 3 6 0
0 0 0 0 6 3 4 4 4 4 4 4 4 4 3 6 0
0 0 0 0 6 3 3 3 3 3 3 3 3 3 3 6 0
0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 0
```
Expected Output:
```
1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
1 2 2 2 2 1 0 0 0 0 0 0 0 0 0 0 0
1 2 8 8 2 1 0 0 0 0 0 0 0 0 0 0 0
1 2 8 8 2 1 0 0 0 0 0 0 0 0 0 0 0
1 2 2 2 2 1 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 1 2 2 2 2 2 2 2 2 2 2 1 0
0 0 0 0 1 2 4 4 4 4 4 4 4 4 2 1 0
0 0 0 0 1 2 4 3 3 3 3 3 3 4 2 1 0
0 0 0 0 1 2 4 3 6 6 6 6 3 4 2 1 0
0 0 0 0 1 2 4 3 6 6 6 6 3 4 2 1 0
0 0 0 0 1 2 4 3 3 3 3 3 3 4 2 1 0
0 0 0 0 1 2 4 4 4 4 4 4 4 4 2 1 0
0 0 0 0 1 2 2 2 2 2 2 2 2 2 2 1 0
0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 0
```
Transformed Output:
```
8 2 2 2 8 8 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 8 8 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 8 8 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 8 8 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 0
0 0 0 0 6 2 2 2 2 2 2 2 2 2 2 6 0
0 0 0 0 6 2 6 6 6 6 6 6 6 6 2 6 0
0 0 0 0 6 2 6 4 4 4 4 4 4 6 2 6 0
0 0 0 0 6 2 6 4 3 3 3 3 4 6 2 6 0
0 0 0 0 6 2 6 4 3 6 6 3 4 6 2 6 0
0 0 0 0 6 2 6 4 3 6 6 3 4 6 2 6 0
0 0 0 0 6 2 6 4 3 6 6 3 4 6 2 6 0
0 0 0 0 6 2 6 4 3 6 6 3 4 6 2 6 0
0 0 0 0 6 2 6 4 3 6 6 3 4 6 2 6 0
```
Match: False
Pixels Off: 121
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 83.73702422145328

## Example 4:
Input:
```
0 0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 1 1 6 6 6 6 6 1 1 0 0 0 0 0 0 0
0 0 0 1 1 6 8 8 8 6 1 1 0 0 0 0 0 0 0
0 0 0 1 1 6 6 6 6 6 1 1 0 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0
0 2 4 4 4 4 4 4 4 4 4 4 2 0 0 0 0 0 0
0 2 4 1 1 1 1 1 1 1 1 4 2 0 0 0 0 0 0
0 2 4 1 8 8 8 8 8 8 1 4 2 0 0 0 0 0 0
0 2 4 1 8 8 8 8 8 8 1 4 2 0 0 0 0 0 0
0 2 4 1 1 1 1 1 1 1 1 4 2 0 0 0 0 0 0
0 2 4 4 4 4 4 4 4 4 4 4 2 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 8 8 6 6 6 6 6 8 8 0 0 0 0 0 0 0
0 0 0 8 8 6 1 1 1 6 8 8 0 0 0 0 0 0 0
0 0 0 8 8 6 6 6 6 6 8 8 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0
0 8 1 1 1 1 1 1 1 1 1 1 8 0 0 0 0 0 0
0 8 1 4 4 4 4 4 4 4 4 1 8 0 0 0 0 0 0
0 8 1 4 2 2 2 2 2 2 4 1 8 0 0 0 0 0 0
0 8 1 4 2 2 2 2 2 2 4 1 8 0 0 0 0 0 0
0 8 1 4 4 4 4 4 4 4 4 1 8 0 0 0 0 0 0
0 8 1 1 1 1 1 1 1 1 1 1 8 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 1 8 1 1 1 1 1 8 1 0 0 0 0 0 0 0
0 0 0 1 8 1 1 1 1 1 8 1 0 0 0 0 0 0 0
0 0 0 1 8 1 1 1 1 1 8 1 0 0 0 0 0 0 0
0 0 0 1 8 1 1 1 1 1 8 1 0 0 0 0 0 0 0
0 0 0 1 8 1 1 1 1 1 8 1 0 0 0 0 0 0 0
0 0 0 1 8 8 8 8 8 8 8 1 0 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0
0 2 8 8 8 8 8 8 8 8 8 8 2 0 0 0 0 0 0
0 2 8 8 8 8 8 8 8 8 8 8 2 0 0 0 0 0 0
0 2 8 8 1 1 1 1 1 1 8 8 2 0 0 0 0 0 0
0 2 8 8 1 4 4 4 4 1 8 8 2 0 0 0 0 0 0
0 2 8 8 1 4 2 2 4 1 8 8 2 0 0 0 0 0 0
0 2 8 8 1 4 2 2 4 1 8 8 2 0 0 0 0 0 0
0 2 8 8 1 4 2 2 4 1 8 8 2 0 0 0 0 0 0
```
Match: False
Pixels Off: 131
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 81.11455108359134
