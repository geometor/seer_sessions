# 5582e5ca • 014 • example_3 • investigate_coder

---
```python
"""
1.  **Identify the most frequent color:** Examine the input grid and determine the color that appears most often. In case of a tie that includes the color at the top and middle element, it looks like the top/middle value wins.
2.  **Flood Fill:** Create an output grid of the same dimensions as the input grid (3x3). Fill every pixel of the output grid with the color identified.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find the most frequent color in the input grid
    colors = input_grid.flatten()
    color_counts = Counter(colors)
    
    most_common_color = color_counts.most_common(1)[0][0]
    # change output pixels 
    output_grid[:] = most_common_color

    return output_grid
```
