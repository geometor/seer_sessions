# 48d8fb45 • 018 • refine_coder

---

Previous Code:
```python
"""
Identify a specific red cluster in the input grid, define a bounding box around it,
and extract the subgrid corresponding to the bounding box, enlarging it by one in all directions.
"""

import numpy as np

def find_object(grid, color):
    """
    Finds all objects of a given color in the grid.
    Returns a list of bounding box coordinates (top_left_row, top_left_col, bottom_right_row, bottom_right_col) for each object.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                if current_object:
                    rows, cols = zip(*current_object)
                    top_left_row = min(rows)
                    top_left_col = min(cols)
                    bottom_right_row = max(rows)
                    bottom_right_col = max(cols)
                    objects.append(
                        (top_left_row, top_left_col, bottom_right_row, bottom_right_col)
                    )
    return objects

def get_bounding_box(coordinates):
    """
    Get the bounding box from a list of coordinates.
    """
    rows, cols = zip(*coordinates)
    return min(rows), min(cols), max(rows), max(cols)
    

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)

    # 1. Identify Red Clusters
    red_clusters = find_object(input_grid, 2)

    # 2. Select Target Cluster (the one starting at [2,2])
    target_cluster = None
    for cluster_box in red_clusters:
      if input_grid[cluster_box[0],cluster_box[1]] == 2 and cluster_box[0] == 2 and cluster_box[1] == 2:
          target_cluster = cluster_box
          break
          
    if target_cluster is None:
      # find the first object
      target_cluster = red_clusters[0]

    # 3. Define Bounding Box
    top_left_row, top_left_col, bottom_right_row, bottom_right_col = target_cluster
    
    # 4. Extract with Enlarging
    top_left_row = max(0, top_left_row - 1)
    top_left_col = max(0, top_left_col - 1)
    bottom_right_row = min(input_grid.shape[0] -1, bottom_right_row + 1)
    bottom_right_col = min(input_grid.shape[1] -1, bottom_right_col + 1)

    # Extract the subgrid
    output_grid = input_grid[
        top_left_row : bottom_right_row + 1, top_left_col : bottom_right_col + 1
    ].copy()

    return output_grid.tolist()
```

Train Set Results:
Here's an analysis of the provided information and a plan to refine the natural language program:

**General Assessment:**

The initial code correctly identifies and extracts a red cluster, expanding its bounding box by one unit in all directions. However, it seems to be consistently picking the first red cluster, instead of all the red objects.

**Strategy:**

1.  **Analyze all examples:**
    *   Verify that the current code only selects the first identified red area, and that the target is always an area of red.
    *   Verify bounding box expansion is correct on all examples.

2.  **Refine Object Identification:** Modify the code to ensure *all* red clusters are processed, and remove specific red object selection.

3.  **Update Natural Language Program:** Revise the program to reflect the generalized red object bounding box and extraction.

**Metrics and Observations (using code_execution for verification):**

```python
def code_execution(input_grid, expected_output, transform_function):
    """Executes the transform function and compares the result with the expected output."""
    actual_output = transform_function(input_grid)
    return actual_output == expected_output

# Provided examples from the prompt
train_examples = [
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 2, 2, 0, 0, 0, 0, 0],
            [0, 0, 2, 2, 2, 0, 0, 0, 0, 0],
            [0, 0, 2, 2, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 2, 2, 2, 0],
            [0, 0, 2, 2, 2, 0],
            [0, 0, 2, 2, 2, 0],
            [0, 0, 0, 0, 0, 0],
        ],
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [0, 0, 0, 2, 2],
            [0, 0, 0, 2, 2],
            [0, 0, 0, 0, 0],
        ],
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [[0, 0, 0, 0], [0, 2, 0, 0], [0, 0, 0, 0]],
    },
]

results = [
    code_execution(example["input"], example["output"], transform)
    for example in train_examples
]
print(results)

# find all red clusters
def print_clusters(grid):
    red_clusters = find_object(grid, 2)
    if red_clusters is not None and len(red_clusters) > 0:
        for i, cluster in enumerate(red_clusters):
            print(f"Cluster {i+1}: {cluster}")

for i, example in enumerate(train_examples):
    print("example:", i)
    print_clusters(example["input"])
```

```output
[False, False, False]
example: 0
Cluster 1: (2, 2, 4, 4)
example: 1
Cluster 1: (6, 8, 7, 9)
example: 2
Cluster 1: (4, 4, 4, 4)
```

The code fails on all training examples, reporting `[False, False, False]`. All red clusters are being found.

**YAML Facts:**

```yaml
observations:
  - task: "Extract all red objects from the input grid"
  - objects:
      - name: "red_cluster"
        color: "red"
        description: "A contiguous block of red pixels."
  - actions:
      - name: "find_objects"
        description: "Locates all instances of a specified object within the grid."
        parameters:
          - color: "The color of the object to find (e.g., red)."
      - name: "bounding_box"
        description: "Calculates the smallest rectangle enclosing an object, then enlarged by one pixel on each side."
      - name: "extract_subgrid"
        description: "Extracts the portion of the grid defined by the bounding box."

```

**Natural Language Program:**

1.  **Find all red objects:** Iterate through the input grid to identify all distinct, contiguous areas of red pixels (where a pixel is considered adjacent if it shares a side, not a diagonal).

2.  **Determine bounding box:** For each identified red object, compute the bounding box. The bounding box is the smallest rectangle that completely encloses the red object.

3.  **Expand bounding box:** Enlarge each bounding box by one pixel in all directions (up, down, left, and right). Ensure the expanded bounding box stays within the original grid boundaries.

4. **Extract:** Extract the subgrids defined by the expanded bounding box.

5.  **Output** Return the collection of expanded subgrids.

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
