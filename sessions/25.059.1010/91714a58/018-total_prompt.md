# 91714a58 • 018 • refine_coder

---

Previous Code:
```python
"""
Finds the largest contiguous cluster of pixels with the value 7 in the input grid and reproduces it in the output grid, setting all other pixels to 0.
"""

import numpy as np

def find_largest_cluster(grid, target_color):
    """
    Finds the largest contiguous cluster of a target color in a grid.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    max_cluster = []

    def dfs(row, col):
        """Depth-First Search to find contiguous pixels."""
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != target_color
        ):
            return []

        visited[row, col] = True
        cluster = [(row, col)]

        cluster.extend(dfs(row + 1, col))
        cluster.extend(dfs(row - 1, col))
        cluster.extend(dfs(row, col + 1))
        cluster.extend(dfs(row, col - 1))
        return cluster

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and not visited[r, c]:
                current_cluster = dfs(r, c)
                if len(current_cluster) > len(max_cluster):
                    max_cluster = current_cluster

    return max_cluster


def transform(input_grid):
    # Initialize output_grid with all zeros
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Find the largest cluster of 7s
    target_color = 7
    largest_cluster = find_largest_cluster(input_grid, target_color)

    # Reconstruct the largest cluster in the output grid
    for row, col in largest_cluster:
        output_grid[row, col] = target_color

    return output_grid
```

Train Set Results:
Okay, let's analyze the results of running the provided code against the training examples and formulate a plan to refine the natural language program and, subsequently, the code.

**General Assessment and Strategy**

The initial code focuses on identifying the largest contiguous cluster of pixels with the value 7 (orange) and reproducing it in the output grid. This approach works for the first example but fails on others. The core issue is that the transformation rule isn't universally applicable across all examples. Some examples involve different colors, multiple clusters, or different criteria for selecting the output.

My strategy is as follows:

1.  **Analyze Each Example:** Carefully examine each input-output pair, noting the specific colors, shapes, and spatial relationships involved. Pay close attention to cases where the current code fails.
2.  **Identify Common Patterns (and Differences):** Look for recurring patterns in how the inputs are transformed to outputs. Determine if there's a single, consistent rule, or if multiple rules are applied based on certain conditions.
3.  **Refine the Natural Language Program:** Based on the analysis, update the natural language program to accurately describe the observed transformation. This might involve adding conditions, specifying different target colors, or describing more complex selection criteria.
4.  **Metrics and Facts:** Gather metrics to quantify observations. These help make the program more precise. The YAML facts will formally document the consistent features.

**Example Analysis and Metrics**

To effectively analyze the examples, I'll use a structured approach to describe each example and calculate the specific metrics that will inform updates.

Here's a breakdown of each example:

*   **Example 1:**
    *   Input has one large orange (7) cluster.
    *   Output is the same orange cluster.
    *   `Result`: `Correct`. The code works as expected.
*   **Example 2:**
    *    Input: contains one large and several small magenta (6) objects.
    *    Output: Shows only the largest magenta object from the input.
    *    `Result`: `Incorrect`. The code looks for orange (7), not magenta (6).
*   **Example 3:**
    *   Input has multiple gray (5) clusters of different sizes.
    *   Output has the largest gray cluster.
    *   `Result`: `Incorrect`. The code looks for orange (7), not gray (5).

**YAML Facts**

```yaml
facts:
  - observation: The transformation selects the largest contiguous cluster of a specific color.
  - observation: The target color varies across examples (orange, magenta, gray).
  - property: size: The size of a cluster is determined by the number of pixels it contains.
  - action: selection: The largest cluster of the target color is selected.
  - action: reproduction: The selected cluster is reproduced in the output grid.
  - constraint: Other pixels in the output grid are set to black (0).
```

**Natural Language Program**

1.  **Identify the Target Color:** Determine the target color for the specific input grid. *Note: The method for how to determine this is currently a mystery and subject of further investigation*.
2.  **Find Clusters:** Identify all contiguous clusters of pixels of the target color within the input grid.
3.  **Calculate Cluster Sizes:** Determine the size of each cluster by counting the number of pixels it contains.
4.  **Select Largest Cluster:** Select the cluster with the largest size.
5.  **Reproduce Cluster:** Create an output grid where all pixels are initially black (0). Copy the selected largest cluster from the input grid to the output grid, maintaining its shape and position.

**Next Steps**
The next coder phase will need to update the python code to use the appropriate color from the input grid.

**INSTRUCTIONS**

- generate a Python module to represent the natural language program 
- follow the template below
- all common math and science libraries are available
- create docstring only at top - but comment the workflow in the function
- use helper functions for common operations like finding objects, counting,
  measuring, moving, etc. 

remember - we are working iteratively - so this code will inform your future
self as we converge on the solution

*template:*

```python
"""
{{ natural language description of the transformation rule }}
"""

{{ imports }}

def transform(input_grid):
    # initialize output_grid

    # change output pixels 

    return output_grid

```
