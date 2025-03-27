
Previous Code:
```python
"""
The transformation rule is as follows:
1. Iterate through each pixel of the input grid.
2. Ignore any pixel that is not azure (8).
3. Identify Connected Components: Group contiguous azure pixels into connected regions or "clusters."
4. Classify and Transform: For each azure pixel do the following:
    - top-left most pixels of a cluster become blue (1)
    - top-right most pixels of a cluster become yellow (4)
    - bottom-left most pixels of a cluster become green (3)
    - bottom-right most pixels of a cluster become red (2)
5. Preserve the color of all other (non-azure) pixels.
6. Construct the output grid by applying this transformation to each pixel.
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
Results for code_00.py:
Train Set Error: error:
No module named 'scipy'
Okay, here's a breakdown of the situation and a plan to move forward:

**General Assessment:**

The initial code failed because it relies on the `scipy` library, which wasn't available in the execution environment. This is a simple fix – I need to ensure that any necessary libraries are included when running the code. Beyond that, the logic seems reasonable, targeting azure (8) colored pixels and attempting to identify "corners" of connected regions to change their colors. The strategy to resolve errors will focus on fixing the code, and then re-evaluating based on all training examples.

**Strategy:**

1.  **Fix the Import Error:** Add a check to confirm that `scipy` is available.
2.  **Re-run and Evaluate:** Execute the corrected code against all training examples.
3.  **Analyze Results:** Compare the output of the corrected code with the expected outputs in the training examples.
4.  **Refine Natural Language Program:** Based on discrepancies, adjust the natural language description of the transformation to accurately reflect *all* training examples.
5. **Document Facts:** Create the requested YAML documentation
6. **Provide Deliverables**: all together

**Gather Metrics (using code execution after fixing import):**

I'll hold off on using a `tool_code` block until I've addressed the import issue, as the current code will definitely fail.

**Fact Documentation (YAML):**


```yaml
facts:
  - objects:
      - name: grid
        type: 2D array
        description: Represents the input and output data, composed of pixels.
      - name: pixel
        type: cell
        description: A single element within the grid, represented by a color value (0-9).
      - name: azure_pixel
        type: pixel
        description: A pixel with the color value 8 (azure).
      - name: cluster
        type: connected_component
        description: A contiguous group of azure pixels.
      - name: top_left
        type: pixel
        property: coordinate with minimum row and minimum column in the cluster
        transformed_to: blue (1)
      - name: top_right
        type: pixel
        property: coordinate with minimum row and maximum column in the cluster
        transformed_to: yellow(4)
      - name: bottom_left
        type: pixel
        property: coordinate with maximum row and minimum column in the cluster
        transformed_to: green (3)
      - name: bottom_right
        type: pixel
        property: coordinate with maximum row and maximum column in the cluster
        transformed_to: red (2)
  - actions:
      - name: identify_azure_pixels
        description: Locate all pixels with the value 8 in the input grid.
      - name: group_clusters
        description: Group contiguous azure pixels into connected regions.
      - name: classify_extrema
        description: identify the top-left, top-right, bottom-left and bottom-right of each cluster.
      - name: transform_pixels
        description: Change the color of specific azure pixels based on their position within their cluster.
      - name: preserve_other_pixels
        description: Keep all non-azure pixels unchanged.
```


**Natural Language Program:**

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

