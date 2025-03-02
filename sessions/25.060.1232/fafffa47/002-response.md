# fafffa47 • 002 • example_5 • investigate_coder

---
```python
"""
The transformation extracts the top grid from the input, replaces maroon with red, and uses that as the output grid.
"""

import numpy as np

def get_top_grid(grid):
    #find sections separated by rows of all zeros
    
    sections = []
    current_section = []
    for i in range(grid.shape[0]):
        if np.all(grid[i] == 0):
            if len(current_section) > 0:
              sections.append(current_section)
              current_section = []
        else:
          current_section.append(grid[i])
    if len(current_section) > 0:
      sections.append(current_section)
    
    # usually the break is all zeros, but sometimes not, like this one
    # find best place to split into two arrays
    if len(sections) <= 1:
      best_split = 0
      max_diff = 0
      for i in range(1,grid.shape[0]):
        diff = 0
        # compare the two parts
        part1 = grid[:i]
        part2 = grid[i:]

        # just use variance as quick test
        diff = np.var(part1) - np.var(part2)
        if diff > max_diff:
          max_diff = diff
          best_split = i
      
      sections = [ grid[:best_split].tolist(), grid[best_split:].tolist()]

    return np.array(sections[0])

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Get the top grid
    top_grid = get_top_grid(np.array(input_grid))

    # Initialize the output grid with the dimensions of the top grid
    output_grid = np.zeros((top_grid.shape[0], top_grid.shape[1]), dtype=int)

    # Replace colors: maroon (9) to red (2), white (0) remains white (0)
    for i in range(top_grid.shape[0]):
        for j in range(top_grid.shape[1]):
            if top_grid[i, j] == 9:
                output_grid[i, j] = 2
            elif top_grid[i, j] == 0:
                output_grid[i, j] = 0
            # we don't see it, but assume if anything else, leave alone

    return output_grid.tolist()
```
