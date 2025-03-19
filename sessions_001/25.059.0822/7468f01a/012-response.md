# 7468f01a • 012 • refine_coder

---
```python
"""
1.  **Identify Connected Components:** Find all distinct, contiguous regions (connected components) of yellow (4) pixels within the input grid.  Two yellow pixels are considered connected if they are adjacent horizontally, vertically, *or diagonally*.
2.  **Determine Bounding Boxes:** For *each* connected component identified in step 1, find the smallest rectangle (bounding box) that encloses all pixels within that component.
3.  **Crop and Output:** For *each* bounding box found in step 2, extract the corresponding region from the input grid.  Each extracted region becomes a separate output grid.
4. **Handle Empty Case:** If there are no yellow pixels, return an empty output list (or a single empty grid, depending on the desired output format).
"""

import numpy as np
from scipy.ndimage import label

def find_connected_components(grid):
    # Label connected regions of yellow pixels
    labeled_grid, num_labels = label(grid == 4)
    return labeled_grid, num_labels

def find_bounding_boxes(labeled_grid, num_labels):
    bounding_boxes = []
    for i in range(1, num_labels + 1):  # Iterate through each labeled region
        # Find row and column indices of the current labeled region
        rows, cols = np.where(labeled_grid == i)
        
        # Calculate min and max row/col to define the bounding box
        min_row, max_row = np.min(rows), np.max(rows)
        min_col, max_col = np.min(cols), np.max(cols)
        
        bounding_boxes.append((min_row, max_row, min_col, max_col))
    return bounding_boxes

def transform(input_grid):
    # Find connected components of yellow pixels
    labeled_grid, num_labels = find_connected_components(input_grid)
    
    # If there are no yellow pixels, return an empty list
    if num_labels == 0:
        return []
    
    # Find bounding boxes for each connected component
    bounding_boxes = find_bounding_boxes(labeled_grid, num_labels)
    
    output_grids = []
    # Crop the input grid to each bounding box
    for min_row, max_row, min_col, max_col in bounding_boxes:
        output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]
        output_grids.append(output_grid)

    return output_grids
```
