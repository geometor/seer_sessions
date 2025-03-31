Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from scipy.ndimage import label, find_objects, center_of_mass
from collections import defaultdict

"""
The transformation rule involves identifying connected components of non-background colors in the input grid using diagonal connectivity. 
For each non-background color present in multiple components, one component is designated as the "source" (typically the largest one containing that color) and the others are "targets". 
The source component is then copied to new locations. The location of each copy is determined by aligning specific pixels ("anchors" in the source, "targets" in the target components) of the same color.

1.  **Find Components:** Identify all connected components of non-background pixels using 8-way (diagonal) connectivity. Record the pixels (row, col, color) for each component.
2.  **Identify Background:** Determine the background color (most frequent color).
3.  **Group Components by Color:** Create a mapping from each non-background color to the list of components containing that color.
4.  **Determine Source/Target and Schedule Copies:**
    a.  Iterate through each color `C` present in multiple components.
    b.  Select the "Source Component" (`Obj_S`) for color `C`: the component with the most pixels containing `C`. Tie-breaking: largest bounding box area, then top-most, then left-most bounding box corner.
    c.  Identify all other components containing `C` as "Target Components" (`T_C`).
    d.  Extract anchor pixels `P_s` (list of (r, c)) of color `C` from `Obj_S`, sorted by row then column.
    e.  For each `T_C`:
        i.  Extract target pixels `P_t` (list of (r, c)) of color `C` from `T_C`, sorted by row then column.
        ii. Pair the i-th target pixel `P_t[i]` with the i-th anchor pixel `P_s[i]`.
        iii. Calculate the offset: `offset = P_t[i] - P_s[i]`.
        iv. Schedule a copy: store `(P_t[i], Obj_S_pixels, offset)`, where `Obj_S_pixels` is the list of (r, c, color) tuples for the source component.
5.  **Sort Copies:** Sort the scheduled copies based on the target pixel position (`P_t[i]`), first by row, then by column.
6.  **Apply Copies:**
    a.  Initialize the output grid as a copy of the input grid.
    b.  Iterate through the sorted scheduled copies.
    c.  For each copy `(target_pos, Obj_S_pixels, offset)`:
        i.  For each pixel `(r_src, c_src, color)` in `Obj_S_pixels`:
            *   Calculate destination `(dest_r, dest_c) = (r_src + offset[0], c_src + offset[1])`.
            *   If the destination is within the grid bounds, update `output_grid[dest_r, dest_c] = color`. Overwriting is permitted.
7.  **Return Output Grid.**
"""

def find_components(grid):
    """Finds connected components of non-background pixels using 8-way connectivity."""
    background_color = np.bincount(grid.ravel()).argmax()
    components = []
    mask = grid != background_color
    labeled_array, num_features = label(mask, structure=np.ones((3,3), dtype=bool))

    if num_features > 0:
        # Use find_objects to get bounding boxes, which helps iterate efficiently
        objects_slices = find_objects(labeled_array)
        for i in range(1, num_features + 1):
            component_mask = labeled_array == i
            coords = np.argwhere(component_mask)
            component_pixels = []
            for r, c in coords:
                component_pixels.append((r, c, grid[r, c]))
            if component_pixels: # Ensure component is not empty
                 components.append(component_pixels)
                 
    # Sort components by top-left coordinate (min_r, then min_c) for deterministic order
    components.sort(key=lambda comp: (min(p[0] for p in comp), min(p[1] for p in comp)))
    return components, background_color

def get_component_properties(component):
    """Calculates properties of a component."""
    if not component:
        return 0
---
