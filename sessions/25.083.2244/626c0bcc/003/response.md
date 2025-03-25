```python
"""
1.  **Iterate through Input:** Examine each pixel of the input grid.
2.  **Identify Azure Pixels:** Find pixels that are colored azure (value 8).
3.  **Cluster Detection:** Group the azure pixels into connected components (clusters), where pixels are considered connected if they are adjacent (up, down, left, or right – not diagonally).
4. **Find Extrema:** For each cluster found, identify the following special pixels:
      - **Top-Left:** The pixel with the smallest row and smallest column value.
      - **Top-Right:** The pixel with the smallest row and largest column value.
      - **Bottom-Left:** The pixel with the largest row and smallest column value.
      - **Bottom-Right:** The pixel with the largest row and largest column value.

5.  **Color Transformation:** Change colors:
    *   Top-Left pixel to blue (1).
    *   Top-Right pixel to yellow (4).
    *   Bottom-Left pixel to green (3).
    *   Bottom-Right pixel to red (2).

6.  **Preserve Other Colors:** All pixels that are *not* azure (8) in the original input grid should remain the same color in the output grid.
7.  **Output:** Construct the output grid by applying the above rules to every pixel in the input grid.
"""

import numpy as np
from scipy.ndimage import label, find_objects

def get_cluster_extrema(coords):
    """
    Find the top-left, top-right, bottom-left, and bottom-right pixel coordinates.
    """
    min_row, min_col = np.min(coords, axis=0)
    max_row, max_col = np.max(coords, axis=0)

    top_left_candidates = coords[(coords[:, 0] == min_row) & (coords[:, 1] == min_col)]
    top_right_candidates = coords[(coords[:, 0] == min_row) & (coords[:, 1] == max_col)]
    bottom_left_candidates = coords[(coords[:, 0] == max_row) & (coords[:, 1] == min_col)]
    bottom_right_candidates = coords[(coords[:, 0] == max_row) & (coords[:, 1] == max_col)]
    
    #there should always just be 1
    top_left = top_left_candidates[0]
    top_right = top_right_candidates[0]
    bottom_left = bottom_left_candidates[0]
    bottom_right = bottom_right_candidates[0]    

    return top_left, top_right, bottom_left, bottom_right

def transform(input_grid):
    """
    Transforms the input grid according to the identified rule.
    """
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()
    
    # Identify azure pixels
    azure_pixels = (input_grid == 8)
    
    # Label connected components (clusters) of azure pixels
    labeled_array, num_features = label(azure_pixels)
    
    # Iterate through each cluster
    for i in range(1, num_features + 1):  # Labels start from 1
        cluster_coords = np.array(np.where(labeled_array == i)).T
        
        # Determine extrema within cluster
        top_left, top_right, bottom_left, bottom_right = get_cluster_extrema(cluster_coords)

        # Transform based on relative position
        output_grid[tuple(top_left)] = 1      # Top-left -> Blue
        output_grid[tuple(top_right)] = 4     # Top-right -> Yellow
        output_grid[tuple(bottom_left)] = 3   # Bottom-left -> Green
        output_grid[tuple(bottom_right)] = 2  # Bottom-right -> Red
    

    return output_grid.tolist()
```