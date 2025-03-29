```python
import numpy as np
from collections import deque

"""
The transformation rule involves identifying two types of structures in the input grid: "templates" and "triggers".

1.  **Template Identification:**
    *   A template consists of a single "inner pixel" of color C_inner surrounded by an "outer shape" made of a single color C_outer (where C_inner != C_outer).
    *   The key condition is that all non-background neighbors (8-way connectivity, including diagonals) of the inner pixel must belong to the *same* contiguous outer shape of color C_outer.
    *   Multiple templates might exist in the grid.

2.  **Trigger Identification:**
    *   A trigger is a single pixel of color C_trigger that has no neighbors (8-way connectivity) of the same color C_trigger.
    *   A pixel identified as the inner pixel of a template cannot simultaneously be a trigger.

3.  **Transformation Process:**
    *   Initialize the output grid as a copy of the input grid.
    *   Find all templates and triggers in the input grid.
    *   For each identified trigger pixel (color C_trigger at location L_trigger):
        *   Find all identified templates whose inner pixel color (C_inner) matches C_trigger.
        *   For each matching template:
            *   Calculate the relative position of all pixels (inner and outer) in the template with respect to its original inner pixel location (L_inner_original).
            *   Copy the template structure (inner pixel color C_inner and outer shape color C_outer).
            *   Paste this copied structure onto the output grid, anchoring it such that the template's inner pixel is placed at the trigger's location (L_trigger). The outer shape pixels are placed relative to this new anchor point.
            *   Pasting overwrites existing pixel values in the output grid.
    *   If multiple templates match a trigger, or multiple triggers exist, apply the pasting process for all valid trigger-template pairs. The examples suggest placements are usually distinct, but the rule implies overwriting if overlaps occur.
    *   The final output grid contains the original grid modified by the pasted templates.
"""

def find_contiguous_object(grid, start_r, start_c, target_color):
    """Finds all connected pixels of target_color starting from (start_r, start_c) using BFS."""
    if grid[start_r, start_c] != target_color:
        return set()

    rows, cols = grid.shape
    q = deque([(start_r, start_c)])
    visited = set([(start_r, start_c)])
    object_pixels = set([(start_r, start_c)])

    while q:
        r, c = q.popleft()

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc

                if 0 <= nr < rows and 0 <= nc < cols and \
                   grid[nr, nc] == target_color and \
                   (nr, nc) not in visited:
                    visited.add((nr, nc))
                    object_pixels.add((nr, nc))
                    q.append((nr, nc))
    return object_pixels

def get_neighbors(grid, r, c):
    """Gets coordinates and colors of 8-way neighbors."""
    rows, cols = grid.shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append(((nr, nc), grid[nr, nc]))
    return neighbors

def identify_templates_and_triggers(grid):
    """Identifies templates and triggers in the grid."""
    rows, cols = grid.shape
    templates = []
    potential_triggers = []
    template_inner_pixels = set()

    # Step 1: Identify potential templates and their inner pixels
    for r in range(rows):
        for c in range(cols):
            inner_color = grid[r, c]
            if inner_color == 0:  # Skip background
                continue

            neighbors = get_neighbors(grid, r, c)
            non_bg_neighbors = [(loc, color) for loc, color in neighbors if color != 0]

            if not non_bg_neighbors:
                continue # Isolated pixel, might be a trigger, handle later

            # Check if all non-bg neighbors have the same color C_outer != inner_color
            first_outer_color = non_bg_neighbors[0][1]
            if inner_color == first_outer_color:
                continue # Neighbors are same color as center pixel

            all_same_outer_color = True
            for _, color in non_bg_neighbors:
                if color != first_outer_color:
                    all_same_outer_color = False
                    break

            if not all_same_outer_color:
                continue # Neighbors have mixed colors

            # Now check if these neighbors belong to a single contiguous object
            outer_color = first_outer_color
            start_nr, start_nc = non_bg_neighbors[0][0]
            outer_object_pixels = find_contiguous_object(grid, start_nr, start_nc, outer_color)

            # Verify all non_bg_neighbors are part of this single object
            part_of_same_object = True
            for loc, _ in non_bg_neighbors:
                if loc not in outer_object_pixels:
                    part_of_same_object = False
                    break

            if part_of_same_object:
                # Found a template!
                template_inner_pixels.add((r,c))
                templates.append({
                    'inner_color': inner_color,
                    'inner_loc': (r, c),
                    'outer_color': outer_color,
                    'outer_pixels': outer_object_pixels
                })

    # Step 2: Identify potential triggers (isolated pixels)
    for r in range(rows):
        for c in range(cols):
            trigger_color = grid[r, c]
            if trigger_color == 0:
                continue

            neighbors = get_neighbors(grid, r, c)
            has_same_color_neighbor = False
            for _, color in neighbors:
                if color == trigger_color:
                    has_same_color_neighbor = True
                    break

            if not has_same_color_neighbor:
                 potential_triggers.append({
                    'color': trigger_color,
                    'loc': (r, c)
                 })

    # Step 3: Filter triggers - remove any that were template inner pixels
    triggers = [pt for pt in potential_triggers if pt['loc'] not in template_inner_pixels]

    return templates, triggers


def transform(input_grid):
    """
    Applies the template copying transformation based on triggers.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    rows, cols = output_grid.shape

    # Identify all templates and triggers in the original input grid
    templates, triggers = identify_templates_and_triggers(input_grid_np)

    if not triggers or not templates:
        # Handle train_1 case specifically if needed, or return copy if no operation
        # For now, if no templates/triggers match, return copy
        # Let's check train 1: it might fall here
        # Train 1 Input analysis:
        # Green pixel (3) at (2,2) - isolated
        # Azure object (8) at (2,3), (2,4), (3,2) - surrounds Green? Neighbors of (2,2) are (2,3)=8, (3,2)=8. Yes. Template? inner=3, outer=8
        # Red pixel (2) at (1,10) - isolated
        # Yellow pixel (4) at (7,6) - isolated
        # Red pixel (2) at (7,7) - isolated
        # Yellow object (4) at (7,8), (8,7), (8,8). Neighbors of (7,7)=2 are (7,6)=4, (7,8)=4, (8,7)=4, (8,8)=4. All yellow=4. Template? inner=2, outer=4
        # Green pixel (3) at (8,1) - isolated
        # In Train 1:
        # Template 1: inner=3 at (2,2), outer=8 (pixels {(2,3), (2,4), (3,2)})
        # Template 2: inner=2 at (7,7), outer=4 (pixels {(7,6), (7,8), (8,7), (8,8)})
        # Triggers: Red at (1,10), Yellow at (7,6), Green at (8,1)
        # Matching:
        # Trigger Green(3) at (8,1) matches Template 1 (inner=3). Paste T1 anchored at (8,1).
        # Trigger Red(2) at (1,10) matches Template 2 (inner=2). Paste T2 anchored at (1,10).
        # This matches the output logic! So train_1 is not an anomaly.

        pass # Continue with the main logic even if empty initially

    # Iterate through triggers and apply matching templates
    for trigger in triggers:
        trigger_loc = trigger['loc']
        trigger_color = trigger['color']

        for template in templates:
            if template['inner_color'] == trigger_color:
                # Found a match, paste this template anchored at trigger_loc
                inner_orig_loc = template['inner_loc']
                inner_color = template['inner_color']
                outer_color = template['outer_color']
                outer_pixels = template['outer_pixels']

                # Calculate offset
                delta_r = trigger_loc[0] - inner_orig_loc[0]
                delta_c = trigger_loc[1] - inner_orig_loc[1]

                # Paste inner pixel
                target_inner_r, target_inner_c = trigger_loc
                if 0 <= target_inner_r < rows and 0 <= target_inner_c < cols:
                    output_grid[target_inner_r, target_inner_c] = inner_color

                # Paste outer pixels
                for (r_orig, c_orig) in outer_pixels:
                    target_outer_r = r_orig + delta_r
                    target_outer_c = c_orig + delta_c

                    if 0 <= target_outer_r < rows and 0 <= target_outer_c < cols:
                        output_grid[target_outer_r, target_outer_c] = outer_color

    return output_grid.tolist()
```