import numpy as np
from collections import Counter

"""
Transformation Rule Description:

1.  **Identify Static Color:** Determine the non-white color (`S`) that has the highest total pixel count in the input grid. If there's a tie in count, choose the color with the highest numerical index.
2.  **Identify Static and Dynamic Pixels:**
    *   All pixels in the input grid with the static color `S` are "static pixels".
    *   All other non-white pixels in the input grid are "dynamic pixels".
3.  **Calculate Shape Size Parameter `N`:** Count the total number of dynamic pixels. This count is `N`.
4.  **Determine Actor Color `A`:** Find the color that appears most frequently among the dynamic pixels. If there's a tie for the highest frequency, choose the color with the highest numerical index as the "actor color" `A`.
5.  **Construct Output Grid:**
    *   Initialize an output grid of the same dimensions as the input, filled with white (0).
    *   Copy all static pixels (color `S`) from the input grid to the output grid at their original coordinates.
    *   Determine the shape to draw based on the actor color `A`:
        *   If `A` is Yellow (4): Draw a 2x2 square using color `A` in the Bottom-Right corner.
        *   If `A` is Red (2): Draw a right-angled triangle of side length `N` using color `A` in the Bottom-Left corner, with the hypotenuse pointing Up-Right.
        *   If `A` is Magenta (6): Draw a right-angled triangle of side length `N` using color `A` in the Bottom-Right corner, with the hypotenuse pointing Up-Left.
        *   If `A` is Orange (7): Draw a right-angled triangle of side length `N` using color `A` in the Top-Left corner, with the hypotenuse pointing Down-Right.
    *   Draw the determined shape onto the output grid.
"""

def find_pixel_coords_by_color(grid):
    """Creates a dictionary mapping each color to a list of its pixel coordinates."""
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
    
    # --- 1. Identify Static Color ---
    coords_map = find_pixel_coords_by_color(input_grid_np)
    
    static_color = -1
    max_count = -1
    
    # Sort colors by index descending for tie-breaking
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
    dynamic_pixels = [] # List of (r, c, color)
    dynamic_colors_list = []
    
    for color, coords in coords_map.items():
        if color != static_color:
            for r, c in coords:
                dynamic_pixels.append((r, c, color))
                dynamic_colors_list.append(color)

    # --- 3. Calculate Shape Size Parameter N ---
    N = len(dynamic_pixels)

    # --- 4. Determine Actor Color A ---
    actor_color = -1
    if dynamic_colors_list:
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

    # --- 5. Construct Output Grid ---
    output_grid = np.zeros_like(input_grid_np) # Initialize with white (0)

    # Place static pixels
    for r, c in static_pixels_coords:
        output_grid[r, c] = static_color

    # Draw the shape based on actor_color and N
    if actor_color != -1: # Only draw if an actor color was determined
        # Helper for bounds checking
        def is_valid(r, c):
            return 0 <= r < height and 0 <= c < width

        if actor_color == 4: # Yellow -> BR 2x2 Square
            # Size N is ignored for Yellow, always 2x2
            for r in range(height - 2, height):
                for c in range(width - 2, width):
                     if is_valid(r, c):
                         output_grid[r, c] = actor_color
                         
        elif actor_color == 2 and N > 0: # Red -> BL Triangle Up-Right, Size N
            for r in range(height - N, height):
                for c in range(N):
                    # Condition for triangle pixels relative to BL corner (H-1, 0)
                    if (height - 1 - r) + c < N:
                         if is_valid(r, c):
                            output_grid[r, c] = actor_color
                            
        elif actor_color == 6 and N > 0: # Magenta -> BR Triangle Up-Left, Size N
            for r in range(height - N, height):
                for c in range(width - N, width):
                    # Condition for triangle pixels relative to BR corner (H-1, W-1)
                    if (height - 1 - r) + (width - 1 - c) < N:
                         if is_valid(r, c):
                            output_grid[r, c] = actor_color
                            
        elif actor_color == 7 and N > 0: # Orange -> TL Triangle Down-Right, Size N
             for r in range(N):
                 for c in range(N):
                     # Condition for triangle pixels relative to TL corner (0, 0)
                     if r + c < N:
                         if is_valid(r, c):
                             output_grid[r, c] = actor_color
        # Note: If N=0 for triangles, the loops won't run, effectively drawing nothing.
        # If actor_color is determined but not 2, 4, 6, or 7, nothing is drawn.

    return output_grid.tolist()