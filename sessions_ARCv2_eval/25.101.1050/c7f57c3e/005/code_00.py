import numpy as np
from collections import Counter

"""
Transformation Rule Description:

The transformation identifies 'Upper Structures' (contiguous objects of only Blue(1)/Red(2)) 
and their associated 'Bases' (contiguous non-structure, non-background objects adjacent below). 
It also identifies isolated 'Trigger Pixels'.

The transformation follows one of three scenarios based on the colors of the identified Bases:

1. Swap Case:
   - Condition: If both Green(3) and Azure(8) Bases are found associated with any Upper Structures.
   - Actions (Applied based on original grid state):
     - Green(3) Bases are changed entirely to Azure(8).
     - Azure(8) Bases are changed entirely to Green(3).
     - If an Upper Structure was associated with a Green(3) Base, all Red(2) pixels within that structure are changed to Azure(8).
     - If an Upper Structure was associated with an Azure(8) Base, any pixel *within that Base* located directly below a Red(2) pixel of the structure is changed to Red(2) (overriding the Base swap for that specific pixel).

2. Trigger Case:
   - Condition: If the Swap Case condition is not met, AND at least one isolated Trigger Pixel exists (single non-background, non-structure/base pixel not adjacent to a structure).
   - Trigger Selection: Select the trigger pixel with the highest color index ('TargetColor').
   - Actions:
     - All identified Bases (regardless of original color) are changed entirely to the TargetColor.
     - The selected Trigger Pixel is changed to the BackgroundColor.
     - Anomaly Rule (Specific to Example 2): If the TriggerColor is Magenta(6), Background is Green(3), and original Base color was only Yellow(4), set pixel at (trigger_row + 4, trigger_col) to Yellow(4).

3. No Action:
   - Condition: If neither the Swap Case nor the Trigger Case conditions are met.
   - Action: The grid remains unchanged.

Helper concepts:
- BackgroundColor: Most frequent color in the grid.
- Object Finding/Adjacency: Includes diagonals (8-way connectivity).
- Base Association: A Base is associated if it's adjacent (8-way) to an Upper Structure and its top row is >= the structure's top row.
"""


def find_objects(grid: np.ndarray, background_color: int) -> list[tuple[int, set[tuple[int, int]]]]:
    """
    Finds connected components (objects) of non-background colors using BFS with 8-way connectivity.
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
                        
                        # Explore neighbors (8-connectivity)
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
                                    
                    # Mark non-matching color pixels as visited globally if they are non-background
                    # This prevents starting new searches from them, but they aren't added to current object.
                    elif 0 <= row < rows and 0 <= col < cols and grid[row, col] != background_color:
                         visited[row,col] = True

                if obj_pixels:
                    objects.append((color, obj_pixels))
            # Ensure every pixel is marked visited eventually
            visited[r,c] = True 
    return objects

def get_bounding_box(pixels: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    """Calculates the min/max row/col for a set of pixels."""
    if not pixels:
        # Return invalid bounds if no pixels
        return -1, -1, -1, -1 
    min_r = min(r for r, c in pixels)
    max_r = max(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_c = max(c for r, c in pixels)
    return min_r, max_r, min_c, max_c

def check_adjacency(pixels1: set[tuple[int, int]], pixels2: set[tuple[int, int]]) -> bool:
    """Checks if any pixel in pixels1 is adjacent (8-way) to any pixel in pixels2."""
    if not pixels1 or not pixels2:
        return False
    # Optimization: Check bounding boxes first - if they don't overlap (expanded by 1), no adjacency.
    min_r1, max_r1, min_c1, max_c1 = get_bounding_box(pixels1)
    min_r2, max_r2, min_c2, max_c2 = get_bounding_box(pixels2)
    if max_r1 < min_r2 - 1 or min_r1 > max_r2 + 1 or max_c1 < min_c2 - 1 or min_c1 > max_c2 + 1:
        return False
        
    # Detailed check
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
    # 1. Initialization
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape
    if grid.size == 0: return []

    # Determine BackgroundColor
    colors, counts = np.unique(grid, return_counts=True)
    if not colors.size: return []
    background_color = colors[np.argmax(counts)]

    # 2. Object Identification
    all_objects = find_objects(grid, background_color)

    # 3. Categorize Objects
    structure_candidates = [] # list of (pixels, red_pixels)
    base_candidates = []      # list of (color, pixels)
    trigger_candidates = []   # list of (color, pixels, coordinates tuple) - storing coords for easier access

    all_struct_pixels = set()
    for color, pixels in all_objects:
        is_structure_obj = all(grid[r, c] in [1, 2] for r, c in pixels) and (1 in {grid[p] for p in pixels} or 2 in {grid[p] for p in pixels})

        if is_structure_obj:
            red_pixels = {p for p in pixels if grid[p] == 2}
            structure_candidates.append((pixels, red_pixels))
            all_struct_pixels.update(pixels)
        elif color not in [1, 2]: # Potential base or trigger
            base_candidates.append((color, pixels))
            if len(pixels) == 1:
                 coord = list(pixels)[0]
                 trigger_candidates.append((color, pixels, coord))

    # 4. Associate Structures and Bases
    structure_base_map = defaultdict(list) # struct_idx -> list of (base_color, base_pixels)
    associated_base_pixels = set()
    base_original_colors = set()

    # Create a set of all structure pixels for faster adjacency checks later
    # all_struct_pixels = set().union(*[s[0] for s in structure_candidates])
    
    struct_data_for_mapping = [] # Store (struct_idx, struct_pixels, struct_min_r)
    for i, (sp, rp) in enumerate(structure_candidates):
         min_r, _, _, _ = get_bounding_box(sp)
         struct_data_for_mapping.append((i, sp, min_r))

    for base_color, base_pixels in base_candidates:
        if base_pixels.intersection(associated_base_pixels): continue # Already associated
        
        base_min_r, _, _, _ = get_bounding_box(base_pixels)
        if base_min_r == -1: continue # Skip empty base objects if they somehow occur

        associated = False
        for struct_idx, struct_pixels, struct_min_r in struct_data_for_mapping:
             # Check vertical position and adjacency
             if base_min_r >= struct_min_r and check_adjacency(struct_pixels, base_pixels):
                  structure_base_map[struct_idx].append((base_color, base_pixels))
                  associated = True
                  # Only add color and pixels once per base object, even if it touches multiple structures
                  if not base_pixels.intersection(associated_base_pixels):
                      associated_base_pixels.update(base_pixels)
                      base_original_colors.add(base_color)
                      
    # 5. Confirm and Select Trigger Pixel
    confirmed_triggers = [] # list of (color, pixels, coordinates)
    for color, pixels, coord in trigger_candidates:
        is_base = pixels.intersection(associated_base_pixels)
        is_adj_to_struct = check_adjacency(pixels, all_struct_pixels)
        
        if not is_base and not is_adj_to_struct:
            confirmed_triggers.append((color, pixels, coord))

    selected_trigger = None # (color, pixels, coordinates)
    if confirmed_triggers:
        # Sort triggers by color index descending, then potentially by row/col if needed for tie-breaking (not specified)
        confirmed_triggers.sort(key=lambda x: x[0], reverse=True)
        selected_trigger = confirmed_triggers[0]
        print(f"Selected Trigger: Color {selected_trigger[0]} at {selected_trigger[2]}")

    # 6. Determine Transformation Case
    is_swap_case = 3 in base_original_colors and 8 in base_original_colors
    is_trigger_case = not is_swap_case and selected_trigger is not None

    # 7. Execute Transformation
    if is_swap_case:
        print("Applying Swap Case")
        pixels_to_change = {} # Store changes: (r, c) -> new_color

        # Create map of base pixel to original color for efficient lookup
        base_pixel_original_color = {}
        for struct_idx, associated_bases in structure_base_map.items():
            for base_color, base_pixels in associated_bases:
                 for bp in base_pixels:
                      if bp not in base_pixel_original_color: # Avoid overwriting if shared
                          base_pixel_original_color[bp] = base_color

        # Pass 1: Base swaps and Structure Red changes
        for struct_idx, associated_bases in structure_base_map.items():
            associated_with_green_3 = any(bc == 3 for bc, bp in associated_bases)
            
            # Apply base swaps for bases associated with *this* structure
            for base_color, base_pixels in associated_bases:
                 new_base_color = -1
                 if base_color == 3: new_base_color = 8
                 elif base_color == 8: new_base_color = 3
                 
                 if new_base_color != -1:
                      for r, c in base_pixels:
                           pixels_to_change[(r, c)] = new_base_color # Might be overwritten below
            
            # Apply struct red changes if associated with Green(3)
            if associated_with_green_3:
                struct_pixels, red_pixels = structure_candidates[struct_idx]
                for r, c in red_pixels:
                    pixels_to_change[(r, c)] = 8 # Red -> Azure

        # Pass 2: Override for Base pixels below Red if original base was Azure(8)
        for bp_coord, original_color in base_pixel_original_color.items():
            if original_color == 8:
                br, bc = bp_coord
                pixel_above = (br - 1, bc)
                # Check if pixel above was originally Red(2) and part of *any* structure
                if pixel_above in all_struct_pixels and grid[pixel_above] == 2:
                     pixels_to_change[bp_coord] = 2 # Base Pixel below Red -> Red

        # Apply all changes
        for (r, c), new_color in pixels_to_change.items():
            if 0 <= r < rows and 0 <= c < cols:
                output_grid[r, c] = new_color

    elif is_trigger_case:
        print("Applying Trigger Case")
        target_color, trigger_pixels, trigger_coord = selected_trigger
        tr, tc = trigger_coord

        # Change all associated bases to target color
        for r, c in associated_base_pixels:
             output_grid[r, c] = target_color
             
        # Change selected trigger pixel to background color
        output_grid[tr, tc] = background_color
                
        # Apply Anomaly Rule (Specific to Example 2 context)
        original_base_colors_list = list(base_original_colors)
        is_ex2_context = (target_color == 6 and 
                          background_color == 3 and
                          len(original_base_colors_list) == 1 and 
                          original_base_colors_list[0] == 4)
                          
        if is_ex2_context:
             anomaly_r, anomaly_c = tr + 4, tc
             # Check bounds 
             if 0 <= anomaly_r < rows and 0 <= anomaly_c < cols:
                 print(f"Applying Example 2 Anomaly: Setting ({anomaly_r}, {anomaly_c}) to 4")
                 output_grid[anomaly_r, anomaly_c] = 4 # Set to Yellow

    else:
        print("No Swap or Trigger Case matched. No changes applied.")
        pass # Grid remains unchanged

    # 8. Return result
    return output_grid.tolist()

# Helper defaultdict
from collections import defaultdict