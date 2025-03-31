
Previous Code:
```python
import numpy as np
from collections import Counter

"""
Transformation Rule Description:

1.  **Identify Static Color:** Determine the non-white color (`S`) that has the highest total pixel count in the input grid. If there's a tie in count, choose the color with the highest numerical index.
2.  **Identify Static and Dynamic Pixels:**
    *   All pixels in the input grid with the static color `S` are "static pixels".
    *   All other non-white pixels in the input grid are "dynamic pixels".
3.  **Calculate Size Parameters:**
    *   `N_total`: Count the total number of dynamic pixels.
    *   `N_actor`: Count the number of dynamic pixels that have the "actor color" (defined below).
4.  **Determine Actor Color `A`:** Find the color that appears most frequently among the dynamic pixels. If there's a tie for the highest frequency, choose the color with the highest numerical index as the "actor color" `A`.
5.  **Construct Output Grid:**
    *   Initialize an output grid of the same dimensions (height `H`, width `W`) as the input, filled with white (0).
    *   Copy all static pixels (color `S`) from the input grid to the output grid at their original coordinates.
    *   Determine the shape to draw based on the actor color `A` and the relevant size parameter (`N_total` or `N_actor`):
        *   If `A` is Yellow (4): Draw a vertical line of length `N_actor` using color `A` in the Bottom-Right corner (column `W-1`, rows `H-N_actor` to `H-1`).
        *   If `A` is Red (2): Draw a right-angled triangle of side length `N_total` using color `A` in the Bottom-Left corner, with the hypotenuse pointing Up-Right. Pixels `(r, c)` satisfy `H - N_total <= r < H`, `0 <= c < N_total`, and `(H - 1 - r) + c < N_total`.
        *   If `A` is Magenta (6): Draw a right-angled triangle of side length `N_actor` using color `A` in the Bottom-Right corner, with the hypotenuse pointing Up-Left. Pixels `(r, c)` satisfy `H - N_actor <= r < H`, `W - N_actor <= c < W`, and `(H - 1 - r) + (W - 1 - c) < N_actor`.
        *   If `A` is Orange (7): Draw a right-angled triangle of side length `N_total` using color `A` in the Top-Left corner, with the hypotenuse pointing Down-Right. Pixels `(r, c)` satisfy `0 <= r < N_total`, `0 <= c < N_total`, and `r + c < N_total`.
    *   Draw the determined shape onto the output grid. Only draw if the corresponding size parameter (`N_total` or `N_actor`) is greater than 0.
"""

def find_pixel_coords_by_color(grid):
    """Creates a dictionary mapping each non-white color to a list of its pixel coordinates."""
    coords_map = {}
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0: # Ignore background
                if color not in coords_map:
                    coords_map[color] = []
                coords_map[color].append((r, c))
    return coords_map

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid_np = np.array(input_grid, dtype=np.int64)
    height, width = input_grid_np.shape
    
    # --- Helper function for bounds checking ---
    def is_valid(r, c):
        return 0 <= r < height and 0 <= c < width

    # --- 1. Identify Static Color ---
    coords_map = find_pixel_coords_by_color(input_grid_np)
    
    static_color = -1
    max_count = -1
    
    # Sort colors by index descending for tie-breaking during count comparison
    sorted_colors = sorted(coords_map.keys(), reverse=True) 
    
    for color in sorted_colors:
        count = len(coords_map[color])
        # If current count is higher, or equal with higher color index (already handled by sort)
        if count >= max_count: 
            max_count = count
            static_color = color
            
    # Handle edge case: grid is all white
    if static_color == -1:
        return input_grid_np.tolist()

    # --- 2. Identify Static and Dynamic Pixels ---
    static_pixels_coords = coords_map.get(static_color, [])
    dynamic_pixels_info = [] # List of (r, c, color)
    dynamic_colors_list = []
    
    for color, coords in coords_map.items():
        if color != static_color:
            for r, c in coords:
                dynamic_pixels_info.append((r, c, color))
                dynamic_colors_list.append(color)

    # --- 3/4. Calculate N_total, Determine Actor Color A, Calculate N_actor ---
    N_total = len(dynamic_pixels_info)
    
    actor_color = -1
    N_actor = 0
    
    if dynamic_colors_list: # Proceed only if there are dynamic pixels
        color_counts = Counter(dynamic_colors_list)
        max_freq = 0
        if color_counts: # Check if counter is not empty
             max_freq = max(color_counts.values())
        
        candidates = []
        for color, count in color_counts.items():
            if count == max_freq:
                candidates.append(color)
        
        if candidates:
            actor_color = max(candidates) # Tie-break with highest index
            N_actor = color_counts[actor_color] # Get count for the chosen actor color

    # --- 5. Construct Output Grid ---
    output_grid = np.zeros_like(input_grid_np) # Initialize with white (0)

    # Place static pixels
    for r, c in static_pixels_coords:
        if is_valid(r, c): # Bounds check (should be redundant if coords_map is correct)
            output_grid[r, c] = static_color

    # Draw the shape based on actor_color and relevant N
    if actor_color != -1: # Only draw if an actor color was determined
        
        if actor_color == 4: # Yellow -> BR Vertical Line, Length N_actor
            if N_actor > 0:
                for r in range(height - N_actor, height):
                    c = width - 1
                    if is_valid(r, c):
                        output_grid[r, c] = actor_color
                         
        elif actor_color == 2: # Red -> BL Triangle Up-Right, Size N_total
            if N_total > 0:
                for r in range(height - N_total, height):
                    for c in range(N_total):
                        # Condition for triangle pixels relative to BL corner (H-1, 0)
                        if (height - 1 - r) + c < N_total:
                             if is_valid(r, c):
                                output_grid[r, c] = actor_color
                            
        elif actor_color == 6: # Magenta -> BR Triangle Up-Left, Size N_actor
            if N_actor > 0:
                for r in range(height - N_actor, height):
                    for c in range(width - N_actor, width):
                        # Condition for triangle pixels relative to BR corner (H-1, W-1)
                        if (height - 1 - r) + (width - 1 - c) < N_actor:
                             if is_valid(r, c):
                                output_grid[r, c] = actor_color
                            
        elif actor_color == 7: # Orange -> TL Triangle Down-Right, Size N_total
             if N_total > 0:
                 for r in range(N_total):
                     for c in range(N_total):
                         # Condition for triangle pixels relative to TL corner (0, 0)
                         if r + c < N_total:
                             if is_valid(r, c):
                                 output_grid[r, c] = actor_color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 4 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0 0
0 0 0 0 2 0 2 0 0
0 0 0 0 0 0 0 2 0
0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 3
```
Expected Output:
```
0 0 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0 0
0 0 0 0 2 0 2 0 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 4 4
```
Transformed Output:
```
0 0 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0 0
0 0 0 0 2 0 2 0 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 4
```
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 3.7037037037036953

## Example 2:
Input:
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
Expected Output:
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
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 7 0 0 7
2 0 0 0 0 0 7 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0
2 2 2 7 0 0 0 0 0 0 0
2 2 2 2 0 0 0 0 0 0 0
2 2 2 2 2 0 0 0 0 0 0
```
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 1.6528925619834638

## Example 3:
Input:
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
Expected Output:
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
Transformed Output:
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
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 4:
Input:
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
Expected Output:
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
Transformed Output:
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
0 0 0 0 8 0 0 0 0 0
```
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 2.0
