
Previous Code:
```python
"""
1.  **Input:** A 2D grid of integer values (0-9) representing colors.
2.  **Azure Cluster Identification:** Identify connected regions (clusters) of azure (8) colored pixels.  Pixels are connected if they are adjacent horizontally or vertically, but *not* diagonally.
3.  **Extrema Determination:** Within each identified azure cluster, locate four "extrema" pixels:
    *   **Top-Left:** The azure pixel with the smallest row and smallest column index.
    *   **Top-Right:** The azure pixel with the smallest row and largest column index.
    *   **Bottom-Left:** The azure pixel with the largest row and smallest column index.
    *   **Bottom-Right:** The azure pixel with the largest row and largest column index.
4.  **Color Transformation:**  Change the color of the identified extrema pixels as follows:
    *   Top-Left pixel becomes blue (1).
    *   Top-Right pixel becomes yellow (4).
    *   Bottom-Left pixel becomes green (3).
    *   Bottom-Right pixel becomes red (2).
5. **Preservation of other colors.** All non-azure pixels must retain their original color.
6.  **Output:** The modified 2D grid with the color transformations applied.
"""

import numpy as np

def find_clusters(grid, color):
    """
    Finds clusters of a specific color in the grid.
    
    Args:
        grid: A 2D numpy array representing the grid.
        color: The color to find clusters of.

    Returns:
        A list of clusters, where each cluster is a list of (row, col) coordinates.
    """
    visited = set()
    clusters = []

    def is_valid(row, col):
        return 0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]

    def dfs(row, col, current_cluster):
        if (row, col) in visited or not is_valid(row, col) or grid[row, col] != color:
            return

        visited.add((row, col))
        current_cluster.append((row, col))

        # Explore adjacent cells (up, down, left, right)
        dfs(row + 1, col, current_cluster)
        dfs(row - 1, col, current_cluster)
        dfs(row, col + 1, current_cluster)
        dfs(row, col - 1, current_cluster)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_cluster = []
                dfs(row, col, current_cluster)
                clusters.append(current_cluster)

    return clusters

def get_cluster_extrema(cluster):
    """
    Find the top-left, top-right, bottom-left, and bottom-right pixel coordinates of a cluster.
    """
    if not cluster:
        return None, None, None, None

    rows, cols = zip(*cluster)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    top_left = (min_row, min_col)
    top_right = (min_row, max_col)
    bottom_left = (max_row, min_col)
    bottom_right = (max_row, max_col)
    
    return top_left, top_right, bottom_left, bottom_right


def transform(input_grid):
    """
    Transforms the input grid according to the identified rule.
    """
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()
    
    # Find azure clusters
    azure_clusters = find_clusters(input_grid, 8)
    
    # Iterate through each cluster
    for cluster in azure_clusters:
        # Determine extrema within cluster
        top_left, top_right, bottom_left, bottom_right = get_cluster_extrema(cluster)

        # Transform based on relative position
        output_grid[top_left] = 1      # Top-left -> Blue
        output_grid[top_right] = 4     # Top-right -> Yellow
        output_grid[bottom_left] = 3   # Bottom-left -> Green
        output_grid[bottom_right] = 2  # Bottom-right -> Red
    

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 8 0 0 8 0 0
8 8 0 0 8 8 0
0 8 8 0 8 8 0
0 8 8 0 8 8 0
0 0 8 8 0 0 0
0 0 0 8 0 0 0
0 0 0 0 0 0 0
```
Expected Output:
```
0 2 0 0 4 0 0
2 2 0 0 4 4 0
0 1 1 0 1 1 0
0 1 1 0 1 1 0
0 0 3 3 0 0 0
0 0 0 3 0 0 0
0 0 0 0 0 0 0
```
Transformed Output:
```
1 8 0 4 1 4 0
8 8 0 0 8 8 0
0 8 8 0 8 8 0
0 8 8 0 3 2 0
0 0 8 8 0 0 0
3 0 0 2 0 0 0
0 0 0 0 0 0 0
```
Match: False
Pixels Off: 21
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 171.42857142857144

## Example 2:
Input:
```
0 0 8 8 0 0 0
8 8 8 8 8 0 0
0 8 8 0 8 8 0
0 8 8 8 8 0 0
0 0 0 8 8 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
Expected Output:
```
0 0 1 1 0 0 0
3 3 1 1 4 0 0
0 3 2 0 4 4 0
0 2 2 1 1 0 0
0 0 0 1 1 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
Transformed Output:
```
1 0 8 8 0 4 0
8 8 8 8 8 0 0
0 8 8 0 8 8 0
0 8 8 8 8 0 0
3 0 0 8 8 2 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
Match: False
Pixels Off: 21
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 171.42857142857144

## Example 3:
Input:
```
8 8 8 0 0 0 0
8 8 8 8 0 0 0
8 8 0 8 0 0 0
0 8 8 8 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
Expected Output:
```
1 1 4 0 0 0 0
1 1 4 4 0 0 0
3 3 0 2 0 0 0
0 3 2 2 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
Transformed Output:
```
1 8 8 4 0 0 0
8 8 8 8 0 0 0
8 8 0 8 0 0 0
3 8 8 2 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
Match: False
Pixels Off: 13
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 106.12244897959181
Okay, let's analyze the results of the first coding attempt and strategize for improvement.

**General Assessment:**

The initial code correctly identifies the core concept: finding azure (8) colored clusters and modifying specific pixels within them. However, it fails to accurately determine the "extrema" pixels within *all* clusters, leading to incorrect color transformations. The primary issue is that the `get_cluster_extrema` function simply finds the min/max row and min/max col, which are indeed the top-left, bottom-left, top-right and bottom-right pixels, but it doesn't handle the case where a cluster stretches and there are multiple min/max rows and cols. It doesn't account for cases where clusters can cause incorrect identification of these pixels.

**Strategy for Resolution:**

1.  **Refine Extrema Identification:** The `get_cluster_extrema` function needs to be improved. Instead of directly using `min(rows)`, `max(rows)`, `min(cols)`, and `max(cols)`, it needs to find all pixels corresponding to the min/max row and find the min/max column among those to deal with non-rectangular, and diagonal shapes. The same is true for min/max columns, check multiple instances of them.

2.  **Test-Driven Refinement:** We'll focus on correcting the issues revealed by the test examples, particularly addressing the discrepancies in pixel color transformations. We can iteratively adjust the `get_cluster_extrema` logic and use the existing test cases as immediate validation.

**Metrics and Observations per Example (using visual inspection since code execution is limited to computation, not grid comparisons)**

*Example 1*

*   Input Shape: 7x7
*   Expected Output Shape: 7x7
*   Transformed Output Shape: 7x7
*   Number of Azure Clusters (Expected): 2
*   Number of Azure Clusters Identified (Actual): 2
*   Issues:  The corners are not correctly selected

*Example 2*

*   Input Shape: 7x7
*   Expected Output Shape: 7x7
*   Transformed Output Shape: 7x7
*   Number of Azure Clusters (Expected): 2
*   Number of Azure Clusters Identified (Actual): 2
*   Issues: The corners are not correctly selected

*Example 3*

*   Input Shape: 7x7
*   Expected Output Shape: 7x7
*   Transformed Output Shape: 7x7
*   Number of Azure Clusters (Expected): 1
*   Number of Azure Clusters Identified (Actual): 1
*    Issues: The corners are not correctly selected

**YAML Facts:**


```yaml
objects:
  - name: grid
    type: 2D array
    description: Represents the input and output data, with each cell containing a color code.
  - name: azure_cluster
    type: connected_region
    description: A group of adjacent azure (8) colored pixels. Adjacency is horizontal or vertical, not diagonal.
    properties:
      - name: top_left_pixel
        type: coordinate
        description: The azure pixel within the cluster having the smallest row and smallest column indices.
      - name: top_right_pixel
        type: coordinate
        description: The azure pixel within the cluster having the smallest row and largest column indices.
      - name: bottom_left_pixel
        type: coordinate
        description: The azure pixel within the cluster having the largest row and smallest column indices.
      - name: bottom_right_pixel
        type: coordinate
        description: The azure pixel within the cluster having the largest row and largest column indices.

actions:
  - name: identify_clusters
    description: Finds all azure clusters within the grid.
  - name: determine_extrema
    description: Locates the top-left, top-right, bottom-left, and bottom-right pixels within each azure cluster.
  - name: transform_color
    description: Changes the color of the extrema pixels based on their relative positions.
    rules:
      - top_left: Change to blue (1)
      - top_right: Change to yellow (4)
      - bottom_left: Change to green (3)
      - bottom_right: Change to red (2)
  - name: preserve_other_colors
    description: all non azure colored pixels are not modified.
```


**Natural Language Program:**

1.  **Input:** Receive a 2D grid of integers (0-9), where each integer represents a color.

2.  **Cluster Identification:** Identify all distinct clusters of azure (8) colored pixels.  Pixels are part of the same cluster if they are directly adjacent horizontally or vertically (not diagonally).

3.  **Extrema Identification (Revised):** Within each identified azure cluster:
    *   **Top-Left:** Find all pixels with minimum row. Of those, find the one the smallest column.
    *   **Top-Right:** Find all pixels with the minimum row. Of those, find the one with the largest column.
    *   **Bottom-Left:** Find all pixels with the maximum row. Of those, find the one with the smallest column.
    *   **Bottom-Right:** Find all pixels with maximum row, and of those, find the one with maximum column.

4.  **Color Transformation:** Change the colors of the identified extrema pixels as follows:
    *   Top-Left pixel: Change to blue (1).
    *   Top-Right pixel: Change to yellow (4).
    *   Bottom-Left pixel: Change to green (3).
    *   Bottom-Right pixel: Change to red (2).

5.  **Preservation:** Ensure all pixels that are *not* azure retain their original color.

6.  **Output:** Return the modified 2D grid with the color transformations applied to the identified extrema pixels within each azure cluster.

