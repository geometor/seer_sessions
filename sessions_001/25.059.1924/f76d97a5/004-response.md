# f76d97a5 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Initial Yellow:** Identify the pixels that are yellow (4) in the input grid.
2.  **Convert Gray:** Change all gray (5) pixels to yellow (4).
3.  **Convert Original Yellow:** Change all the originally yellow pixels (identified in step 1) to white(0).
4. **Final Output** All initially gray pixels remain as yellow, and only the original yellow pixels become white.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Identify Initial Yellow
    initial_yellow_pixels = []
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
          if input_grid[i,j] == 4:
            initial_yellow_pixels.append((i,j))

    # Convert Gray
    for i in range(input_grid.shape[0]):
      for j in range(input_grid.shape[1]):
        if output_grid[i,j] == 5:
          output_grid[i,j] = 4

    # Convert Original Yellow
    for (i,j) in initial_yellow_pixels:
        output_grid[i,j] = 0


    return output_grid
```
