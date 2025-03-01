# 3428a4f5 • 022 • example_4 • investigate_coder

---
```python
"""
1. **Initialization:** Start with the input grid.
2. **Color Replacement:** Replace all occurrences of red (2) and yellow (4) with green (3).
3. **Grid Reduction/Compression:** Reduce the grid size. The output grid is significantly smaller than the input. The exact method of reduction needs further examples, but it is preserving the locations of transitions to the background color 0. White pixels are in positions of transition or edge of object.
4. **Output**: Return new compressed grid.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to modify
    modified_grid = np.copy(input_grid)

    # Replace red (2) and yellow (4) with green (3)
    modified_grid[modified_grid == 2] = 3
    modified_grid[modified_grid == 4] = 3

    # Define the output grid dimensions (from example: 6x5)
    output_height = 6
    output_width = 5
    output_grid = np.zeros((output_height, output_width), dtype=int)
   
    # Pattern Mapping (hardcoded based on this specific example, needs generalization)
    # This section is highly speculative and depends on the specific reduction rule,
    # which isn't fully clear from a single example.
    for i in range(output_height):
        for j in range(output_width):
            #check section in input
            input_i = int(i * (input_grid.shape[0] / output_height))
            input_j = int(j * (input_grid.shape[1] / output_width))
           
            input_section =  input_grid[max(0,input_i-1):min(input_grid.shape[0],input_i + 2),max(0,input_j-1):min(input_grid.shape[1],input_j + 2)]
            
            if np.any(input_section == 0) and  np.any(input_section != 0):
              output_grid[i,j] = 0
            else:
              output_grid[i,j] = 3



    return output_grid
```
