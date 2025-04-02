Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from scipy.ndimage import label, find_objects

"""
Identifies 'template' shapes and 'pattern' shapes within the input grid based on a 'placeholder' color. 
The placeholder color acts as noise within templates and as the background for patterns.
Each template object has a primary color C1 and contains noise pixels of the placeholder color P.
Each pattern object has a background of the placeholder color P and contains pattern pixels of color C2.
Templates and patterns are identified and sorted based on their top-left corner coordinates (row-major order).
A specific permutation rule, dependent on the number of template/pattern pairs (N), maps the i-th template to a pattern color from the perm[i]-th pattern.
- For N=2 pairs, the permutation is [0, 1] (template 0 -> pattern 0 color, template 1 -> pattern 1 color).
- For N=4 pairs, the permutation is [1, 3, 0, 2] (template 0 -> pattern 1 color, template 1 -> pattern 3 color, template 2 -> pattern 0 color, template 3 -> pattern 2 color).
For other N, a default [0, 1, ..., N-1] mapping is assumed.
The transformation extracts the subgrid for each template, replaces all pixels of the placeholder color P with the mapped pattern color C2.
Finally, the modified template subgrids are assembled into an output grid, preserving their original relative spatial arrangement (determined by sorting their top-left coordinates). The output grid size is determined by the grid layout (e.g., 1xN, Nx1, 2x2) and the dimensions of the templates.
"""

def find_contiguous_objects(grid, color):
    """Finds all contiguous objects of a given color."""
    mask = grid == color
    labeled_array, num_features = label(mask)
    objects_slices = find_objects(labeled_array)
    object_details = []
    if objects_slices:
        for i, obj_slice in enumerate(objects_slices):
            # Calculate bounding box
            bbox = (obj_slice[0].start, obj_slice[1].start,
                    obj_slice[0].stop, obj_slice[1].stop) # min_r, min_c, max_r, max_c
            # Extract coordinates relative to the original grid
            coords = np.argwhere(labeled_array[obj_slice] == (i + 1))
            abs_coords = coords + np.array([obj_slice[0].start, obj_slice[1].start])
            
            object_details.append({
                'id': i + 1,
                'color': color,
                'slice': obj_slice,
                'bbox': bbox,
                'coords': abs_coords,
                'size': len(abs_coords)
            })
    return object_details

def get_subgrid(grid, bbox):
    """Extracts a subgrid based on bounding box."""
    return grid[bbox[0]:bbox[2], bbox[1]:bbox[3]]

def analyze_grid(input_grid):
    """
    Analyzes the input grid to identify the placeholder color,
    template objects, and pattern objects.
    Returns: placeholder_color, sorted_templates, sorted_patterns
    """
    colors, counts = np.unique(input_grid, return_counts=True)
    
    all_objects_by_color = {}
    for color in colors:
        # Exclude color 0 if it's just background, adjust if 0 is meaningful
        # if color == 0 and counts[colors == 0] > 0.8 * input_grid.size: continue 
        all_objects_by_color[color] = find_contiguous_objects(input_grid, color)

    potential_patterns = [] # {placeholder, pattern_color, bbox}
    possible_placeholders = {} # {p_candidate: [pattern_colors C2]}

    # 1. Identify potential patterns: regions dominated by P containing single other color C2
    for p_candidate in colors:
        if p_candidate not in all_objects_by_color: continue
        for p_obj_detail in all_objects_by_color[p_candidate]:
            p_bbox = p_obj_detail['bbox']
            p_subgrid = get_subgrid(input_grid, p_bbox)
            subgrid_colors, subgrid_counts = np.unique(p
---
