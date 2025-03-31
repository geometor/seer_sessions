
## train_1

**input:**
```
0 4 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0 0
0 0 0 0 2 0 2 0 0
0 0 0 0 0 0 0 2 0
0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 3
```


**output:**
```
0 0 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0 0
0 0 0 0 2 0 2 0 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 4 4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 1 0 0 0 7 0 0
0 0 2 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 7 0 0 7
0 0 0 3 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 7 0 0 7
2 0 0 0 0 0 7 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0
2 2 2 2 0 0 0 0 0 0 0
2 2 2 2 2 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 6 0 0
0 0 0 0 0 8 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 6 0 0 0 0 0 6
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 6 6 6 6
```


## train_4

**input:**
```
9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 0 8 0 8 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 7 0
0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 8 0 0 0 3 0
```


**output:**
```
7 7 7 7 7 0 0 0 0 0
7 7 7 7 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0
7 7 0 8 0 0 0 0 0 0
7 0 0 0 8 0 8 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   Each input grid contains multiple non-white colors, often scattered.
    *   Each output grid retains some pixels from the input grid in their original locations, while other pixels are removed, and a new geometric shape is added in one of the corners.
    *   There appears to be one "static" color in each pair, whose pixels remain unchanged. All other non-white colors are "dynamic".
    *   The dynamic pixels are removed from their original positions.
    *   A new shape (either a square or a triangle) is drawn in one corner of the grid.
    *   The color of the new shape is determined by one of the dynamic colors – specifically, the dynamic color that appeared most frequently in the input. If there's a tie in frequency, the color with the higher index seems to be chosen. Let's call this the "actor color".
    *   The size of the new shape (side length N for triangles, N x N for squares) is determined by the total count (N) of all dynamic pixels in the input.
    *   The type of shape (square or triangle), its corner location, and its orientation depend specifically on the *actor color's index*.
        *   Actor Red (2): Results in a N-side triangle in the Bottom-Left corner, pointing Up-Right.
        *   Actor Yellow (4): Results in a 2x2 square in the Bottom-Right corner (specifically when N=2).
        *   Actor Magenta (6): Results in a N-side triangle in the Bottom-Right corner, pointing Up-Left.
        *   Actor Orange (7): Results in a N-side triangle in the Top-Left corner, pointing Down-Right.
    *   The final output combines the preserved static pixels and the newly drawn shape on a white background.

*   **Facts:**
    
```yaml
    task_type: object_transformation
    
    components:
      - role: background
        color: white (0)
      - role: static_pixels
        description: Pixels of a specific color that remain unchanged between input and output. Only one such color exists per example pair.
        properties:
          - color: Varies (red(2), orange(7), azure(8))
          - persistence: Position is maintained from input to output.
      - role: dynamic_pixels
        description: All non-white pixels that are not static. These are removed from their original locations.
        properties:
          - color: Varies (multiple colors possible)
          - persistence: Removed from original location.
          - role: contributes_to_size (N)
            value: The total count of all dynamic pixels determines the size parameter N for the output shape.
          - role: determines_actor_color (A)
            value: The dynamic color with the highest frequency (count) becomes the actor color A. Tie-breaking favors higher color index.
      - role: output_shape
        description: A geometric shape drawn in a corner of the output grid.
        properties:
          - color: Determined by the actor color A.
          - size: Determined by the total count N of dynamic pixels.
          - type: Square (if A=4 and N=2) or Triangle (otherwise, based on tested examples).
          - corner_location: Determined by the actor color A (e.g., A=2 -> BL, A=4 -> BR, A=6 -> BR, A=7 -> TL).
          - orientation: Determined by the actor color A (e.g., A=2 -> Up-Right, A=6 -> Up-Left, A=7 -> Down-Right).
    
    relationships:
      - type: identification
        from: input_grid
        to: static_pixels
        rule: Find the color S whose pixel locations are identical in input and output.
      - type: identification
        from: input_grid
        to: dynamic_pixels
        rule: All non-white pixels not belonging to the static color S.
      - type: calculation
        from: dynamic_pixels
        to: size_parameter_N
        rule: N = count(dynamic_pixels).
      - type: selection
        from: dynamic_pixels
        to: actor_color_A
        rule: A = color within dynamic_pixels with max frequency (count). Tie-break using highest color index.
      - type: determination
        from: actor_color_A, size_parameter_N
        to: output_shape properties (type, corner, orientation)
        rule: Based on specific rules mapping A (and potentially N) to shape characteristics (e.g., A=2 -> BL Triangle Up-Right size N; A=4 & N=2 -> BR Square size 2x2).
      - type: composition
        from: static_pixels, output_shape
        to: output_grid
        rule: Combine static pixels and the generated output shape on a white background of the original grid dimensions.
    ```


*   **Natural Language Program:**
    1.  Identify the "static color" `S` by finding which non-white color's pixels have the exact same coordinates in both the input and output grids. Store the locations of these static pixels.
    2.  Identify all "dynamic pixels" in the input grid: these are all non-white pixels that do not have the static color `S`.
    3.  Count the total number `N` of dynamic pixels.
    4.  Determine the frequency (count) of each color present among the dynamic pixels.
    5.  Identify the "actor color" `A` as the dynamic color with the highest frequency. If two or more dynamic colors share the highest frequency, choose the one with the largest color index as `A`.
    6.  Initialize the output grid as a white grid with the same dimensions as the input grid.
    7.  Place the identified static pixels (color `S`) onto the output grid at their original locations.
    8.  Determine the corner, shape type, orientation, and size based on the actor color `A` and the count `N`:
        *   If `A` is Red (2): Draw a right-angled triangle of side length `N` using color `A`, located in the Bottom-Left corner, with the hypotenuse facing Up-Right.
        *   If `A` is Yellow (4) and `N` is 2: Draw a 2x2 square using color `A`, located in the Bottom-Right corner.
        *   If `A` is Magenta (6): Draw a right-angled triangle of side length `N` using color `A`, located in the Bottom-Right corner, with the hypotenuse facing Up-Left.
        *   If `A` is Orange (7): Draw a right-angled triangle of side length `N` using color `A`, located in the Top-Left corner, with the hypotenuse facing Down-Right.
        *   (Define behavior for other potential actor colors or the case where A=Yellow(4) but N is not 2, if necessary based on test cases).
    9.  Draw the determined shape onto the output grid. Existing static pixels should not be overwritten (though based on examples, the shape area seems distinct from static pixel locations).
```python
import numpy as np
from collections import Counter

"""
Transformation Rule Description:

1.  **Identify Static vs. Dynamic Pixels:**
    *   Find all contiguous objects (blocks of the same non-white color).
    *   Determine the largest object (by pixel count). The color of this largest object is the "static color". All pixels of this color remain unchanged in the output.
    *   All other non-white pixels are "dynamic pixels". These are removed from their original positions.

2.  **Determine Actor Color and Shape Size:**
    *   Count the frequency of each color among the dynamic pixels.
    *   The "actor color" is the dynamic color with the highest frequency. If there's a tie in frequency, the color with the highest numerical index wins.
    *   The size parameter `N` for the output shape is the count of pixels of the actor color.

3.  **Construct Output Grid:**
    *   Initialize an output grid of the same dimensions as the input, filled with white (0).
    *   Copy the static pixels (with the static color) to the output grid at their original locations.
    *   Based on the actor color and size `N`, draw a specific shape in a specific corner using the actor color:
        *   **Red (2):** Bottom-Left corner, Right-angled triangle of side `N`, hypotenuse pointing Up-Right. Pixels `(r, c)` where `H-N <= r < H`, `0 <= c < N`, and `(H - 1 - r) + c < N`.
        *   **Yellow (4):** If `N` is 2, Bottom-Right corner, 2x2 square. Pixels `(r, c)` where `H-2 <= r < H` and `W-2 <= c < W`. (Behavior for N!=2 is unspecified by examples, assumed not to occur or not to draw shape).
        *   **Magenta (6):** Bottom-Right corner, Right-angled triangle of side `N`, hypotenuse pointing Up-Left. Pixels `(r, c)` where `H-N <= r < H`, `W-N <= c < W`, and `(H - 1 - r) + (W - 1 - c) < N`.
        *   **Orange (7):** Top-Left corner, Right-angled triangle of side `N`, hypotenuse pointing Down-Right. Pixels `(r, c)` where `0 <= r < N`, `0 <= c < N`, and `r + c < N`.
    *   The final output grid contains the static pixels and the newly drawn shape.
"""

def find_objects(grid):
    """Finds all contiguous objects of non-white colors using BFS."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Start BFS if pixel is non-white and not visited
            if color != 0 and not visited[r, c]:
                obj_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                obj_color = color
                
                while q:
                    row, col = q.pop(0)
                    obj_pixels.append((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, visited status, and color match
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == obj_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({'color': obj_color, 'pixels': obj_pixels, 'size': len(obj_pixels)})
    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Identifies static/dynamic pixels, determines actor color and shape size,
    and constructs the output grid with static pixels and a new shape.
    """
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape
    
    # 1. Identify Static vs. Dynamic Pixels
    objects = find_objects(input_grid_np)
    
    static_color = -1
    static_pixels_coords = []
    dynamic_pixels = [] # List of tuples (r, c, color)
    
    if not objects:
        # Handle case with no non-white pixels
        return input_grid_np.tolist() 
        
    # Find the largest object to determine static color
    largest_object_size = -1
    largest_object_color = -1
    for obj in objects:
        if obj['size'] > largest_object_size:
            largest_object_size = obj['size']
            largest_object_color = obj['color']
        # Handle tie in size - largest color index wins (though not explicitly stated for static, common ARC pattern)
        elif obj['size'] == largest_object_size:
             largest_object_color = max(largest_object_color, obj['color'])
             
    static_color = largest_object_color
    
    # Separate static and dynamic pixels
    for obj in objects:
        if obj['color'] == static_color:
            static_pixels_coords.extend(obj['pixels'])
        else:
            for r, c in obj['pixels']:
                dynamic_pixels.append((r, c, obj['color']))

    # 2. Determine Actor Color and Shape Size (N)
    actor_color = -1
    actor_pixel_count_N = 0
    
    if dynamic_pixels:
        dynamic_colors = [p[2] for p in dynamic_pixels]
        if dynamic_colors:
            color_counts = Counter(dynamic_colors)
            max_count = 0
            
            # Find max frequency among dynamic colors
            if color_counts:
                 max_count = max(color_counts.values())

            # Find candidate colors with max frequency
            candidates = []
            for color, count in color_counts.items():
                if count == max_count:
                    candidates.append(color)

            # Tie-break using highest color index
            if candidates:
                actor_color = max(candidates)
                # N is the count of the winning actor color
                actor_pixel_count_N = color_counts[actor_color] 

    # 3. Construct Output Grid
    output_grid = np.zeros_like(input_grid_np) # Initialize with white (0)
    
    # Place static pixels
    for r, c in static_pixels_coords:
        if 0 <= r < height and 0 <= c < width: # Bounds check just in case
             output_grid[r, c] = static_color

    # Draw the shape based on actor_color and N
    N = actor_pixel_count_N
    if actor_color != -1 and N > 0:
        if actor_color == 2: # Red -> BL Triangle Up-Right
            for r in range(H - N, H):
                for c in range(N):
                    if (H - 1 - r) + c < N:
                         if 0 <= r < height and 0 <= c < width:
                            output_grid[r, c] = actor_color
                            
        elif actor_color == 4: # Yellow -> BR 2x2 Square (only if N=2)
            if N == 2:
                for r in range(H - 2, H):
                    for c in range(W - 2, W):
                         if 0 <= r < height and 0 <= c < width:
                             output_grid[r, c] = actor_color
                             
        elif actor_color == 6: # Magenta -> BR Triangle Up-Left
            for r in range(H - N, H):
                for c in range(W - N, W):
                    if (H - 1 - r) + (W - 1 - c) < N:
                         if 0 <= r < height and 0 <= c < width:
                            output_grid[r, c] = actor_color
                            
        elif actor_color == 7: # Orange -> TL Triangle Down-Right
             for r in range(N):
                 for c in range(N):
                     if r + c < N:
                         if 0 <= r < height and 0 <= c < width:
                             output_grid[r, c] = actor_color

    return output_grid.tolist()

# Helper variables (needed inside draw logic)
H, W = 0, 0 # Global or passed into draw functions is better, setting inside transform

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Identifies static/dynamic pixels, determines actor color and shape size,
    and constructs the output grid with static pixels and a new shape.
    """
    input_grid_np = np.array(input_grid)
    global H, W # Use global H, W - less ideal but works for template
    H, W = input_grid_np.shape # Set grid dimensions H, W
    
    # 1. Identify Static vs. Dynamic Pixels
    objects = find_objects(input_grid_np)
    
    static_color = -1
    static_pixels_coords = []
    dynamic_pixels = [] # List of tuples (r, c, color)
    
    if not objects:
        # Handle case with no non-white pixels
        return input_grid_np.tolist() 
        
    # Find the largest object to determine static color
    largest_object_size = -1
    largest_object_color = -1
    # Use a list to handle potential ties in size correctly before picking max color index
    largest_objects_candidates = [] 
    for obj in objects:
        if obj['size'] > largest_object_size:
            largest_object_size = obj['size']
            largest_objects_candidates = [obj['color']] # Reset candidates
        elif obj['size'] == largest_object_size:
            largest_objects_candidates.append(obj['color']) # Add to candidates
             
    if largest_objects_candidates:
        static_color = max(largest_objects_candidates) # Pick highest color index among largest
    else:
         # If no objects found, maybe return original? or empty?
         # Based on logic flow, this shouldn't happen if objects list is not empty.
         # If objects list *was* empty, it returned earlier.
         # Add a fallback just in case.
         return input_grid_np.tolist()


    # Separate static and dynamic pixels
    for obj in objects:
        if obj['color'] == static_color:
            static_pixels_coords.extend(obj['pixels'])
        else:
            for r, c in obj['pixels']:
                dynamic_pixels.append((r, c, obj['color']))

    # 2. Determine Actor Color and Shape Size (N)
    actor_color = -1
    actor_pixel_count_N = 0
    
    if dynamic_pixels:
        dynamic_colors = [p[2] for p in dynamic_pixels]
        if dynamic_colors:
            color_counts = Counter(dynamic_colors)
            max_count = 0
            
            # Find max frequency among dynamic colors
            if color_counts:
                 max_count = max(color_counts.values())

            # Find candidate colors with max frequency
            candidates = []
            for color, count in color_counts.items():
                if count == max_count:
                    candidates.append(color)

            # Tie-break using highest color index
            if candidates:
                actor_color = max(candidates)
                # N is the count of the winning actor color
                actor_pixel_count_N = color_counts[actor_color] 

    # 3. Construct Output Grid
    output_grid = np.zeros_like(input_grid_np) # Initialize with white (0)
    
    # Place static pixels
    for r, c in static_pixels_coords:
        # Ensure coords are within bounds - shouldn't be necessary if find_objects is correct
        if 0 <= r < H and 0 <= c < W: 
             output_grid[r, c] = static_color

    # Draw the shape based on actor_color and N
    N = actor_pixel_count_N
    if actor_color != -1 and N > 0:
        # Define bounds checks to simplify drawing loops
        def is_valid(r, c):
            return 0 <= r < H and 0 <= c < W

        if actor_color == 2: # Red -> BL Triangle Up-Right
            for r in range(H - N, H):
                for c in range(N):
                    if (H - 1 - r) + c < N:
                         if is_valid(r, c):
                            output_grid[r, c] = actor_color
                            
        elif actor_color == 4: # Yellow -> BR 2x2 Square (only if N=2)
            if N == 2:
                for r in range(H - 2, H):
                    for c in range(W - 2, W):
                         if is_valid(r, c):
                             output_grid[r, c] = actor_color
                             
        elif actor_color == 6: # Magenta -> BR Triangle Up-Left
            for r in range(H - N, H):
                for c in range(W - N, W):
                    # Check triangle condition relative to corner (H-1, W-1)
                    # Equivalent condition: (r - (H-N)) + (c - (W-N)) >= N-1 ? No simpler..
                    # Use original derived condition: (H-1-r) + (W-1-c) < N
                    if (H - 1 - r) + (W - 1 - c) < N:
                         if is_valid(r, c):
                            output_grid[r, c] = actor_color
                            
        elif actor_color == 7: # Orange -> TL Triangle Down-Right
             for r in range(N):
                 for c in range(N):
                     if r + c < N:
                         if is_valid(r, c):
                             output_grid[r, c] = actor_color

    return output_grid.tolist()
```
