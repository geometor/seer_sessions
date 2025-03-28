Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from collections import deque

"""
Transformation rule:
1. Identify all pixels belonging to the single non-background color present in the grid (color C, ObjectPixels). If no non-background color exists, return the input grid.
2. Perform a flood fill (4-connectivity) starting from all background pixels (color 0) located on the border of the grid. This fill explores only background pixels and cannot cross into ObjectPixels. Mark all reachable background pixels.
3. Identify enclosed background pixels (EnclosedPixels) as those background pixels (color 0) that were not reached by the border flood fill.
4. Initialize the output grid by copying the input grid.
5. Fill the EnclosedPixels in the output grid with color C.
6. Determine if the collection of ObjectPixels forms a closed loop around the EnclosedPixels. This is true if and only if EnclosedPixels is not empty, and every pixel in Object
---
