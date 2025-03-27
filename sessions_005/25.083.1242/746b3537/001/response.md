```python
"""
Iterate through each unique row in the input grid.
For each row being iterated, store the first value.
  Iterate through the stored values from step two, inserting each unique value on a newline in the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = []

    # Iterate through each row of input grid
    seen_rows = []
    for row in input_grid:
        # check if we've see this row before, using the first value
        if row[0] not in seen_rows:
            #add this to the rows we have seen
            seen_rows.append(row[0])
            #append the unique first value
            output_grid.append([row[0]])

    return output_grid
```
