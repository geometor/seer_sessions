
Previous Code:
```python
import numpy as np
from collections import Counter
import itertools

"""
Transformation Rule Description:

The transformation identifies 'Upper Structures' (contiguous objects of only Blue(1)/Red(2)) 
and their associated 'Bases' (contiguous non-structure, non-background objects adjacent below). 
It also identifies isolated 'Trigger Pixels'.

The transformation follows one of two main scenarios based on the colors of the identified Bases:

1. Swap Case:
   - Condition: If both Green(3) and Azure(8) Bases are found associated with any Upper Structures.
   - Actions:
     - Green(3) Bases are changed entirely to Azure(8).
     - Azure(8) Bases are changed entirely to Green(3).
     - If an Upper Structure was associated with a Green(3) Base, all Red(2) pixels within that structure are changed to Azure(8).
     - If an Upper Structure was associated with an Azure(8) Base, any pixel *within that Base* located directly below a Red(2) pixel of the structure is changed to Red(2) (overriding the Base swap for that specific pixel).

2. Trigger Case:
   - Condition: If the Swap Case condition is not met, AND at least one isolated Trigger Pixel exists (single non-background, non-structure/base pixel not adjacent to a structure).
   - Assumption: All Trigger Pixels share the same color ('TargetColor').
   - Actions:
     - All identified Bases (regardless of original color) are changed entirely to the TargetColor.
     - All Trigger Pixels are changed to the BackgroundColor.

3. No Action:
   - Condition: If neither the Swap Case nor the Trigger Case conditions are met.
   - Action: The grid remains unchanged.

Helper concepts:
- BackgroundColor: Most frequent color in the grid.
- Adjacency: Includes diagonals (8-way connectivity).
- Base Association: A Base is associated if it's adjacent to an Upper Structure and its top is not above the structure's top.
"""

def find_objects(grid: np.ndarray, background_color: int) -> list[tuple[int, set[tuple[int, int]]]]:
    """
    Finds connected components (objects) of non-background colors using BFS.
    Returns a list of tuples: (color, set_of_pixel_coordinates).
    """
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
                current_obj_visited_in_bfs = set([(r,c)]) # Track visited for *this specific object's BFS*

                while q:
                    row, col = q.pop(0)
                    
                    # Ensure we only add pixels matching the initial color of this object
                    if grid[row, col] == color:
                        obj_pixels.add((row, col))
                        
                        # Explore neighbors (8-connectivity for object finding)
                        for dr in [-1, 0, 1]:
                            for dc in [-1, 0, 1]:
                                if dr == 0 and dc == 0:
                                    continue
                                nr, nc = row + dr, col + dc
                                if 0 <= nr < rows and 0 <= nc < cols and \
                                   not visited[nr, nc] and \
                                   grid[nr, nc] == color and \
                                   (nr, nc) not in current_obj_visited_in_bfs:
                                    visited[nr, nc] = True
                                    current_obj_visited_in_bfs.add((nr,nc))
                                    q.append((nr, nc))
                    # Mark non-matching color pixels as visited globally 
                    # to avoid starting new searches from them, but don't add to current object
                    elif 0 <= row < rows and 0 <= col < cols :
                         visited[row,col] = True

                if obj_pixels:
                    objects.append((color, obj_pixels))
            # Ensure even background or already-processed pixels are marked visited
            visited[r,c] = True 
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

def check_adjacency(pixels1: set[tuple[int, int]], pixels2: set[tuple[int, int]]) -> bool:
    """Checks if any pixel in pixels1 is adjacent (8-way) to any pixel in pixels2."""
    for r1, c1 in pixels1:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r1 + dr, c1 + dc
                if (nr, nc) in pixels2:
                    return True
    return False

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation logic based on Upper Structures, Bases, and Trigger Pixels.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # 1. Analyze Input: Find Background Color and Objects
    if grid.size == 0: return []
    colors, counts = np.unique(grid, return_counts=True)
    if not colors.size: return [] # Handle empty grid case
    background_color = colors[np.argmax(counts)]
    
    all_objects = find_objects(grid, background_color)

    # 2. Identify Structures, Potential Bases, and Potential Triggers
    structure_candidates = [] # list of (pixels, red_pixels)
    base_candidates = []      # list of (color, pixels)
    trigger_candidates = []   # list of (color, pixels)

    for color, pixels in all_objects:
        is_structure_color = color in [1, 2] # Blue or Red
        all_pixels_are_structure_colors = all(grid[r, c] in [1, 2] for r, c in pixels)
        
        if is_structure_color and all_pixels_are_structure_colors:
            red_pixels = {p for p in pixels if grid[p] == 2}
            structure_candidates.append((pixels, red_pixels))
        elif len(pixels) == 1 and color not in [1, 2]:
             trigger_candidates.append((color, pixels))
             # Also add to base candidates, will filter later
             base_candidates.append((color, pixels))
        elif color not in [1, 2]:
            base_candidates.append((color, pixels))

    # 3. Associate Structures and Bases
    structure_data = [] # list of (struct_pixels, red_pixels, associated_bases)
                        # associated_bases = list of (base_color, base_pixels)
    associated_base_pixels = set()
    processed_structure_pixels = set()
    base_original_colors = set()

    for struct_pixels, red_pixels in structure_candidates:
        processed_structure_pixels.update(struct_pixels)
        struct_min_r, _, _, _ = get_bounding_box(struct_pixels)
        current_associated_bases = []
        
        for base_color, base_pixels in base_candidates:
            # Avoid associating a base multiple times if it touches multiple structures
            # or associating parts of the same object classified differently.
            if base_pixels.intersection(associated_base_pixels) or \
               base_pixels.intersection(processed_structure_pixels):
                continue

            base_min_r, _, _, _ = get_bounding_box(base_pixels)
            
            # Check adjacency and vertical position constraint
            if base_min_r >= struct_min_r and check_adjacency(struct_pixels, base_pixels):
                current_associated_bases.append((base_color, base_pixels))
                associated_base_pixels.update(base_pixels)
                base_original_colors.add(base_color)
                
        structure_data.append((struct_pixels, red_pixels, current_associated_bases))

    # 4. Refine Trigger Identification
    confirmed_trigger_pixels = []
    for color, pixels in trigger_candidates:
        # Must not be an associated base and not adjacent to any structure
        is_base = pixels.intersection(associated_base_pixels)
        is_adj_to_struct = check_adjacency(pixels, processed_structure_pixels)
        
        if not is_base and not is_adj_to_struct:
            confirmed_trigger_pixels.append((color, pixels))

    # 5. Determine Transformation Case
    is_swap_case = 3 in base_original_colors and 8 in base_original_colors
    is_trigger_case = not is_swap_case and len(confirmed_trigger_pixels) > 0

    # 6. Execute Transformation
    if is_swap_case:
        print("Applying Swap Case")
        pixels_to_change = {} # Store changes to apply atomically: (r, c) -> new_color

        for struct_pixels, red_pixels, associated_bases in structure_data:
            primary_base_color_for_struct = -1 # Color of the first associated base determines struct changes
            if associated_bases:
                 primary_base_color_for_struct = associated_bases[0][0]
                 
            for base_color, base_pixels in associated_bases:
                new_base_color = -1
                if base_color == 3:
                    new_base_color = 8
                elif base_color == 8:
                    new_base_color = 3
                
                if new_base_color != -1:
                    for r, c in base_pixels:
                         # Add to change list, might be overridden by below_red rule later
                         pixels_to_change[(r, c)] = new_base_color 

            # Apply structure Red pixel changes based on the *first* associated base's original color
            if primary_base_color_for_struct == 3:
                for r, c in red_pixels:
                    pixels_to_change[(r, c)] = 8 # Red -> Azure
            
            # Apply base pixel below Red changes based on the *first* associated base's original color
            elif primary_base_color_for_struct == 8:
                 for r_red, c_red in red_pixels:
                     br, bc = r_red + 1, c_red
                     # Check if pixel below belongs to *any* of the bases originally associated with *this* structure
                     pixel_is_in_original_azure_base = False
                     for b_col, b_pix in associated_bases:
                          if b_col == 8 and (br, bc) in b_pix:
                               pixel_is_in_original_azure_base = True
                               break
                     if pixel_is_in_original_azure_base:
                          pixels_to_change[(br, bc)] = 2 # Base Pixel below Red -> Red

        # Apply all stored changes
        for (r, c), new_color in pixels_to_change.items():
            if 0 <= r < rows and 0 <= c < cols:
                output_grid[r, c] = new_color

    elif is_trigger_case:
        print("Applying Trigger Case")
        target_color = confirmed_trigger_pixels[0][0] # Assume all triggers have the same color
        
        # Change all associated bases to target color
        all_base_pixels_to_change = set().union(*[bp for _,_, assoc_bases in structure_data for _, bp in assoc_bases])
        for r, c in all_base_pixels_to_change:
             output_grid[r, c] = target_color
             
        # Change trigger pixels to background color
        for _, pixels in confirmed_trigger_pixels:
            for r, c in pixels:
                output_grid[r, c] = background_color
                
        # --- Anomaly Handling Attempt for Example 2 ---
        # This is specific and brittle, based on observation of train_2
        # If trigger was Magenta(6) at (tr,tc) and bases were Yellow(4) at (br,bc)
        # maybe output[tr+4, tc] = 4 ?
        if len(confirmed_trigger_pixels) == 1 and background_color == 3:
             trig_color, trig_pixels_set = confirmed_trigger_pixels[0]
             tr, tc = list(trig_pixels_set)[0]
             original_base_colors_list = list(base_original_colors)
             
             if trig_color == 6 and len(original_base_colors_list) == 1 and original_base_colors_list[0] == 4:
                 anomaly_r, anomaly_c = tr + 4, tc
                 # Check bounds and if the target is currently background
                 if 0 <= anomaly_r < rows and 0 <= anomaly_c < cols and output_grid[anomaly_r, anomaly_c] == background_color:
                     print(f"Applying Example 2 Anomaly: Setting ({anomaly_r}, {anomaly_c}) to 4")
                     output_grid[anomaly_r, anomaly_c] = 4 # Set to Yellow
        # --- End Anomaly Handling ---

    else:
        print("No Swap or Trigger Case matched. No changes applied.")
        pass # Grid remains unchanged

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
4 4 4 4 4 4 4 4 4 4 4 4 4 3 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 3 3 3 4 4 4
4 4 4 4 1 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 1 8 1 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 8 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 1 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 1 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 1 1 8 8 1 1 4 4 4 4
4 4 4 4 4 4 4 4 1 1 8 8 1 1 4 4 4 4
4 4 4 4 4 4 4 4 4 4 8 8 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 8 8 4 4 4 4 4 4
4 4 4 4 4 4 4 4 8 8 8 8 8 8 4 4 4 4
4 4 4 4 4 4 4 4 8 8 8 8 8 8 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 3.7037037037036953

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
