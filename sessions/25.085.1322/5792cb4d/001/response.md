Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np

"""
Transforms the input grid by rotating all non-background pixels by 180 
degrees around the center of their collective bounding box.

1.  Determines the background color (assumed to be 8, azure).
2.  Finds all pixels not matching the background color.
3.  If no non-background pixels are found, returns the input grid unchanged.
4.  Calculates the minimal bounding box containing these non-background pixels.
5.  Calculates the geometric center coordinates (potentially fractional) of this bounding box.
6.  Creates a new output grid of the same dimensions, initialized entirely with the background color.
7.  For each non-background pixel in the input grid:
    a. Calculates its new position after a 180-degree rotation around the calculated center.
    b. Rounds the resulting (potentially fractional) coordinates to the nearest integer coordinates (rounding .5 up).
    c. Places the color of the original non-background pixel at the calculated new position in the output grid.
8.  Returns the completed output grid.
"""

# Helper function to find non-background pixels and bounding box
def find_non_background
---
