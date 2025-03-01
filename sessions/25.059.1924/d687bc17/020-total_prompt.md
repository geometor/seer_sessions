# d687bc17 • 020 • refine_coder

---

Previous Code:
```python
"""
1. Preserve Borders: Keep the top and bottom horizontal bands, and the leftmost and rightmost vertical bands, unchanged.
2. Clear Interior: Set all pixels located *within* the inner region (i.e., not part of the preserved borders) to black (0).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Clear the interior region. Iterate through all rows and columns,
    # excluding the first and last row/column, and set their values to 0.
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            output_grid[r, c] = 0

    return output_grid
```

Train Set Results:
Okay, let's analyze the results of running the initial code against the training examples and refine our natural language program accordingly.

**General Assessment and Strategy**

The initial code implements a "preserve borders and clear interior" rule. This works perfectly for the first example, but fails on the others. This indicates that the initial natural language program was too specific to the first example and doesn't capture the underlying general rule. The strategy is to:

1.  **Analyze the failures:** Carefully examine the input, expected output, and actual output for each failed example. Look for patterns in *what* changed and *where* the changes occurred, that the current code *doesn't* account for.
2.  **Identify Common Principles:** Find the common transformation principles across *all* examples, including those that currently fail. We expect some changes in how the input grid is *perceived*.
3.  **Revise the Natural Language Program:** Rewrite the natural language program to accurately and completely describe the transformation observed in *all* examples.
4.  **Prepare for Code Update:** The revised natural language program will guide the next code iteration.

**Example and Result Metrics**

To gather accurate metrics, I'll create a summary as a list of python dicts
which can then be used to create a pandas dataframe.

```tool_code
import numpy as np

def describe_grid(grid):
    rows, cols = grid.shape
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    return {
        'rows': rows,
        'cols': cols,
        'color_counts': color_counts,
    }
    
examples = []

# example 1
input_grid = np.array([
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
])
output_grid = np.array([
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
])
examples.append({
    "example_id":1,
    "input": describe_grid(input_grid),
    "output": describe_grid(output_grid),
    "result": "success"
})

# example 2
input_grid = np.array([
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
])
output_grid = np.array([
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
])
examples.append({
    "example_id":2,
    "input": describe_grid(input_grid),
    "output": describe_grid(output_grid),
    "result": "failure"
})

# example 3
input_grid = np.array([
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
])
output_grid = np.array([
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
])

examples.append({
    "example_id":3,
    "input": describe_grid(input_grid),
    "output": describe_grid(output_grid),
    "result": "success"
})
import pandas as pd
df = pd.DataFrame(examples)
print(df)
```
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
