# eb281b96 • 010 • refine_coder

---
```tool_code
Example 1:
  Input shape: (2, 2)
  Output shape: (4, 2)
  Output Matches Expected: True
Example 2:
  Input shape: (4, 3)
  Output shape: (8, 3)
  Output Matches Expected: True
Example 3:
  Input shape: (5, 5)
  Output shape: (10, 5)
  Output Matches Expected: True
Example 4:
  Input shape: (4, 4)
  Output shape: (8, 4)
  Output Matches Expected: True
```

**Refined Natural Language Program:**

The transformation rule is to "double the input grid vertically," meaning the output grid is created by stacking an exact copy of the input grid below the original input grid.  This is equivalent to vertical concatenation.

**Final Python Code:**

```python
"""
The transformation rule is to "double the input grid vertically," meaning
the output grid is created by stacking an exact copy of the input grid
below the original input grid. This is equivalent to vertical concatenation.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replicating it vertically (stacking a copy
    of the input grid below itself).

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed output grid.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Replicate the input grid vertically using concatenation
    output_grid = np.concatenate((input_grid, input_grid), axis=0)

    return output_grid
```

