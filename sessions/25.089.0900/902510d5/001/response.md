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