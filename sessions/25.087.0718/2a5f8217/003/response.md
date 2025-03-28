Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
"""
Transformation Rule Description:

1.  Identify all distinct connected components (objects) of blue pixels (color 1) in the input grid.
2.  Identify all distinct connected components (objects) of "influencer" pixels (any color other than white (0) or blue (1)).
3.  For each blue object, determine its size (number of pixels).
4.  For each influencer object, determine its size (number of pixels) and its color.
5.  Match each blue object to exactly one influencer object based on the following criteria:
    a.  **Primary Criterion: Size.** A blue object should ideally be matched with an influencer object of the exact same size.
    b.  **Secondary Criterion (if no exact size match): Closest Size.** If a blue object has no exact size match among the available (unmatched) influencer objects, match it with an available influencer object whose size is closest to the blue object's size.
    c.  **Tie-breaking (if multiple influencers have the same closest size):** 
        i.  Identify all blue objects that need tie-breaking (i.e., have multiple potential matches based on closest size).
        ii. Identify all influencer objects involved in these ties.
        iii. Sort the tied blue objects based on their top-left coordinate (first by row index, then by column index).
        iv. Sort the tied influencer objects based on their color index (ascending).
        v. Assign the first sorted blue object to the first sorted influencer object, the second to the second, and so on.
    d.  **Uniqueness:** Each influencer object can only be matched to one blue object. Perform exact size matches first. Then handle closest-size matches, resolving ties as needed.
6.  Create the output grid by copying the input grid.
7.  For each blue object in the input grid, change the color of all its pixels in the output grid to the color of the influencer object it was matched with.
8.  If there are no blue pixels or no influencer pixels, the output grid is identical to the input grid.
"""

import numpy as np
from scipy.ndimage import label, find_objects
from collections import defaultdict
import copy

def get_component_info(grid, target_color=None, exclude_colors=None):
    """
    Finds connected components of a specific color or all colors except excluded ones.
    
    Args:
        grid (np.ndarray): The input grid.
        target_color (int, optional): If specified, find components of this color.
        exclude_colors (list, optional): If specified, find components of any color not in this list.

    Returns:
        list: A list of dictionaries, each containing info about a component:
              {'label': int, 'coords': list of tuples, 'size': int, 'color': int, 'top_left': tuple}
              Returns empty list if no components are found.
    """
    components_info = []
    if target_color is not None:
        mask = (grid == target_color)
        labeled_array, num_features = label(mask)
        if num_features == 0:
            return []
        
        object_slices = find_objects(labeled_array)
        for i in range(num_features):
            label_val = i + 1
            coords = np.argwhere(labeled_array == label_val)
            top_left = tuple(coords.min(axis=0))
            components_info.append({
                'label': label_val,
                'coords': coords.tolist(),
                'size': len(coords),
                'color': target_color,
                'top_left': top_left
            })
            
    elif exclude_colors is not None:
        unique_colors = np.unique(grid)
        influencer_colors = [c for c in unique_colors if c not in exclude_colors]
        
        current_label = 0
        # We need a way to store labeled components across different colors
        master_labeled_array = np.zeros_like(grid, dtype=int)

        for color in influencer_colors:
            mask = (grid == color)
            # Use structure for diagonal connectivity if needed, default is orthogonal
            labeled_array, num_features = label(mask) 
            
            if num_features > 0:
                 object_slices = find_objects(labeled_array)
                 for i in range(num_features):
                    component_label_in_color = i + 1
                    current_label += 1 # Unique label across all colors
                    
                    coords = np.argwhere(labeled_array == component_label_in_color)
                    top_left = tuple(coords.min(axis=0))
                    
                    # Add to master labeled array (optional, mainly for visualization/debug)
                    master_labeled_array[labeled_array == component_label_in_color] = current_label
                    
                    components_info.append({
                        'label': current_label, # Use the unique master label
                        'coords': coords.tolist(),
                        'size': len(coords),
                        'color': color,
                        'top_left': top_left

---
