# 2bcee788 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Background Replacement:** Replace all white pixels (color 0) in the input grid with green pixels (color 3).
2.  **Color Change:** Replace all red pixels (color 2) in the input grid with magenta pixels (color 6).
3.   **Preservation:** Keep the magenta pixels (color 6) unchanged.
The final output is a grid where the background is green, and the original "L" shape made by red and magenta is wholly magenta.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Replace all white (0) pixels with green (3)
    output_grid[output_grid == 0] = 3

    # Replace all red (2) pixels with magenta (6)
    output_grid[output_grid == 2] = 6

    # Magenta (6) pixels remain unchanged, so no additional operations are needed.

    return output_grid
```
