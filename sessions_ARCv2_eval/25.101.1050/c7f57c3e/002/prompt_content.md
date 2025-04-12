
Previous Code:
```python
import numpy as np
from collections import Counter, defaultdict

"""
This module transforms an input grid based on the colors and arrangements of specific structures. 

The transformation logic distinguishes between two main cases based on the colors of 'base' objects found beneath 'upper structures' (composed of blue and red pixels):

1. Swap Case: If both Green (3) and Azure (8) bases are present in the input:
    - All Green bases are changed to Azure.
    - All Azure bases are changed to Green.
    - Pixels directly below Red (2) components of the upper structures change color based on the *original* color of the base below them:
        - If the original base was Green, the pixel below Red becomes Azure.
        - If the original base was Azure, the pixel below Red becomes Red.

2. Trigger Case: If the Swap Case condition is not met:
    - Identify 'trigger pixels' - isolated single pixels that are not part of the background, upper structures, or bases.
    - If trigger pixels exist (assuming they all share the same color, the 'TargetColor'):
        - All identified bases (regardless of their original color) are changed to the TargetColor.
        - All trigger pixels are changed to the background color.
    - If no trigger pixels exist, the grid remains unchanged.

The background color is determined as the most frequent color in the grid.
Objects are identified as contiguous blocks of non-background colors.
"""

def find_objects(grid: np.ndarray, background_color: int) -> list[tuple[int, set[tuple[int, int]]]]:
    """Finds connected components (objects) of non-background colors."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != background_color:
                color = grid[r, c]
                obj_pixels = set()
                q = [(r, c)]
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    # Check if pixel color matches the starting color of the object
                    # This handles cases where BFS might cross into a different colored adjacent pixel
                    # that hasn't been visited yet as part of another object search.
                    if grid[row, col] == color:
                         obj_pixels.add((row, col))
                         # Explore neighbors (4-connectivity)
                         for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                    # Mark as visited even if color doesn't match the *initial* object color, 
                    # to prevent reprocessing if it's a different non-background color.
                    # The color check above ensures only same-colored pixels are added to the *current* object.
                    visited[r,c] = True 

                if obj_pixels:
                    objects.append((color, obj_pixels))
    return objects

def get_bounding_box(pixels: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    """Calculates the min/max row/col for a set of pixels."""
    if not pixels:
        return 0, 0, 0, 0
    min_r = min(r for r, c in pixels)
    max_r = max(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_c = max(c for r, c in pixels)
    return min_r, max_r, min_c, max_c

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation logic to the input grid.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # 1. Identify the background color
    colors, counts = np.unique(grid, return_counts=True)
    background_color = colors[np.argmax(counts)]

    # 2. Find all non-background objects
    all_objects = find_objects(grid, background_color)

    # 3. Identify upper structures and their bases
    upper_structures = [] # List of tuples: (structure_pixels, red_pixels)
    bases = [] # List of tuples: (base_color, base_pixels, associated_upper_structure_index)
    potential_triggers = [] # List of tuples: (color, pixels)
    
    processed_pixels = set() # Keep track of pixels belonging to structures or bases

    # First pass: Identify potential upper structures (contain blue and red)
    struct_candidates = []
    other_objects = []
    for color, pixels in all_objects:
        contains_blue = any(grid[r,c] == 1 for r,c in pixels)
        contains_red = any(grid[r,c] == 2 for r,c in pixels)
        
        # Check if it contains *only* blue and red (or just one of them)
        is_pure_struct_colors = all(grid[r,c] in [1, 2] for r,c in pixels)

        # A structure must contain blue or red, and only consist of blue/red
        if (contains_blue or contains_red) and is_pure_struct_colors:
             struct_candidates.append(pixels)
        else:
             other_objects.append((color, pixels))

    # Second pass: Find bases below structures and identify triggers
    base_colors_found = []
    struct_pixels_all = set().union(*struct_candidates)

    for i, struct_pixels in enumerate(struct_candidates):
        processed_pixels.update(struct_pixels)
        min_r, max_r, min_c, max_c = get_bounding_box(struct_pixels)
        red_pixels_in_struct = {p for p in struct_pixels if grid[p] == 2}
        
        found_base = False
        # Look for a base directly below the structure
        for r_offset in range(1, rows - max_r): # Search downwards
             potential_base_row = max_r + r_offset
             base_candidate_pixels = set()
             
             # Check pixels directly below the lowest part of the structure
             pixels_to_check_below = {(max_r + 1, c) for r, c in struct_pixels if r == max_r}
             
             connected_base_pixels = set()
             q = []

             # Find starting points for potential base connected to the structure
             for br, bc in pixels_to_check_below:
                 if 0 <= br < rows and 0 <= bc < cols and grid[br, bc] != background_color and grid[br, bc] not in [1, 2]:
                     # Check if this pixel belongs to any known object in other_objects
                     for obj_color, obj_pixels in other_objects:
                         if (br, bc) in obj_pixels:
                            # Found a potential base object, add all its pixels
                            connected_base_pixels.update(obj_pixels)
                            base_colors_found.append(obj_color)
                            bases.append((obj_color, obj_pixels, i)) # Store original color
                            processed_pixels.update(obj_pixels)
                            upper_structures.append((struct_pixels, red_pixels_in_struct))
                            found_base = True
                            break # Found the base for this structure
                 if found_base:
                     break
             if found_base:
                 break # Stop searching downwards once a base is found

        # If no base was found, it's just a structure without a base
        if not found_base:
             upper_structures.append((struct_pixels, red_pixels_in_struct))


    # Identify triggers: single non-background pixels not part of structures or bases
    trigger_pixels = []
    trigger_locations = set()
    trigger_color = -1 

    # Re-evaluate other_objects now that bases are identified and processed
    remaining_objects = []
    for color, pixels in other_objects:
        if not pixels.intersection(processed_pixels): # Check if any part was claimed as a base
             remaining_objects.append((color, pixels))
             
    for color, pixels in remaining_objects:
         if len(pixels) == 1: # Must be a single pixel
              # Check if it's adjacent (including diagonals) to any structure or base pixel
              is_adjacent = False
              px, py = list(pixels)[0]
              for dr in [-1, 0, 1]:
                   for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0: continue
                        adj_r, adj_c = px + dr, py + dc
                        if (adj_r, adj_c) in processed_pixels:
                             is_adjacent = True
                             break
                   if is_adjacent: break
              
              if not is_adjacent: # Only count if truly isolated from identified structures/bases
                  trigger_pixels.append((color, pixels))
                  trigger_locations.update(pixels)
                  if trigger_color == -1:
                       trigger_color = color
                  elif trigger_color != color:
                       # Assumption violated: multiple trigger colors. Handle error or refine logic.
                       # For now, we'll proceed assuming the first one found dictates the color.
                       pass 
    
    # 4. Determine Transformation Case
    is_swap_case = (3 in base_colors_found and 8 in base_colors_found)

    # 5. Apply Transformations
    if is_swap_case:
        print("Applying Swap Case")
        pixels_below_red_map = {} # (r, c) -> original_base_color
        # First pass: identify changes for bases and pixels below red
        base_changes = {} # original_base_index -> new_color
        pixels_below_red_changes = {} # (r,c) -> new_color
        
        for base_idx, (original_color, base_pixels, struct_idx) in enumerate(bases):
            struct_pixels, red_pixels_in_struct = upper_structures[struct_idx]
            new_base_color = -1
            if original_color == 3:
                new_base_color = 8
                base_changes[base_idx] = 8
            elif original_color == 8:
                new_base_color = 3
                base_changes[base_idx] = 3
            else: # Other base colors remain unchanged in swap case
                 pass

            # Determine changes for pixels directly below red parts
            for r_red, c_red in red_pixels_in_struct:
                pixel_below = (r_red + 1, c_red)
                if 0 <= pixel_below[0] < rows and 0 <= pixel_below[1] < cols:
                    # Check if this pixel_below belongs to the current base we're processing
                    if pixel_below in base_pixels:
                        if original_color == 3:
                            pixels_below_red_changes[pixel_below] = 8 # Green base -> Azure below red
                        elif original_color == 8:
                            pixels_below_red_changes[pixel_below] = 2 # Azure base -> Red below red

        # Second pass: apply changes to output_grid
        for base_idx, new_color in base_changes.items():
            _, base_pixels, _ = bases[base_idx]
            for r, c in base_pixels:
                 # Only change if not overridden by a pixel_below_red rule
                 if (r,c) not in pixels_below_red_changes:
                      output_grid[r, c] = new_color

        for (r,c), new_color in pixels_below_red_changes.items():
             output_grid[r, c] = new_color
             
    elif trigger_pixels: # Trigger Case
        print(f"Applying Trigger Case with TargetColor={trigger_color}")
        target_color = trigger_color

        # Change all bases to target color
        for _, base_pixels, _ in bases:
            for r, c in base_pixels:
                output_grid[r, c] = target_color

        # Change trigger pixels to background color
        for _, pixels in trigger_pixels:
             for r, c in pixels:
                 output_grid[r, c] = background_color
                 
    else: # No swap, no triggers
        print("No swap condition and no triggers found. No changes applied.")
        pass # Output grid remains same as input grid copy

    # Note: The anomaly in train_2 (new yellow pixel) is not handled by this logic.

    return output_grid.tolist()

```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 1 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 1 2 1 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 8 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 8 8 8 4 4 4
4 4 4 4 1 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 1 2 1 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 2 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 3 3 3 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 1 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 1 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 1 1 2 2 1 1 4 4 4 4
4 4 4 4 4 4 4 4 1 1 2 2 1 1 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 2 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 2 4 4 4 4 4 4
4 4 4 4 4 4 4 4 3 3 3 3 3 3 4 4 4 4
4 4 4 4 4 4 4 4 3 3 3 3 3 3 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Expected Output:
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 1 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 1 2 1 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 2 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 3 3 3 4 4 4
4 4 4 4 1 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 1 2 1 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 8 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 1 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 1 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 1 1 2 2 1 1 4 4 4 4
4 4 4 4 4 4 4 4 1 1 2 2 1 1 4 4 4 4
4 4 4 4 4 4 4 4 4 4 8 8 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 8 8 4 4 4 4 4 4
4 4 4 4 4 4 4 4 8 8 8 8 8 8 4 4 4 4
4 4 4 4 4 4 4 4 8 8 8 8 8 8 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Transformed Output:
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 1 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 1 2 1 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 2 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 3 3 3 4 4 4
4 4 4 4 1 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 1 2 1 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 2 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 1 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 1 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 1 1 2 2 1 1 4 4 4 4
4 4 4 4 4 4 4 4 1 1 2 2 1 1 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 2 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 2 4 4 4 4 4 4
4 4 4 4 4 4 4 4 8 8 8 8 8 8 4 4 4 4
4 4 4 4 4 4 4 4 8 8 8 8 8 8 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 3.0864197530864033

## Example 2:
Input:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 1 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 2 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 1 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 4 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 1 1 3 3 1 1 3 3 3 3
3 3 3 3 3 3 3 3 1 1 3 3 1 1 3 3 3 3
3 3 3 3 3 3 3 3 3 3 2 2 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 2 2 3 3 3 3 3 3
3 3 3 6 3 3 3 3 1 1 3 3 1 1 3 3 3 3
3 3 1 3 1 3 3 3 1 1 3 3 1 1 3 3 3 3
3 3 3 2 3 3 3 3 3 3 4 4 3 3 3 3 3 3
3 3 1 3 1 3 3 3 3 3 4 4 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Expected Output:
```
3 3 6 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 1 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 2 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 1 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 6 6 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 6 6 3 3 3 3 3 3
3 3 3 3 3 3 3 3 1 1 3 3 1 1 3 3 3 3
3 3 3 3 3 3 3 3 1 1 3 3 1 1 3 3 3 3
3 3 3 3 3 3 3 3 3 3 2 2 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 2 2 3 3 3 3 3 3
3 3 3 3 3 3 3 3 1 1 3 3 1 1 3 3 3 3
3 3 1 3 1 3 3 3 1 1 3 3 1 1 3 3 3 3
3 3 3 2 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 1 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 4 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 1 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 2 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 1 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 4 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 1 1 3 3 1 1 3 3 3 3
3 3 3 3 3 3 3 3 1 1 3 3 1 1 3 3 3 3
3 3 3 3 3 3 3 3 3 3 2 2 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 2 2 3 3 3 3 3 3
3 3 3 6 3 3 3 3 1 1 3 3 1 1 3 3 3 3
3 3 1 3 1 3 3 3 1 1 3 3 1 1 3 3 3 3
3 3 3 2 3 3 3 3 3 3 4 4 3 3 3 3 3 3
3 3 1 3 1 3 3 3 3 3 4 4 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 7.407407407407419
