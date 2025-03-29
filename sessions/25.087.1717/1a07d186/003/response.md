Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
import collections

"""
Transforms an input grid based on the following rules:

1.  Identify static elements: Horizontal and vertical lines (contiguous segments of 2+ identical non-white pixels) and the white background. These remain unchanged in the output unless overwritten by a moved agent.
2.  Identify agent elements: Single non-white pixels that are not part of any identified line.
3.  For each agent pixel:
    a.  Find all lines in the grid that have the same color as the agent.
    b.  If no same-colored line exists, the agent is removed (becomes white) in the output.
    c.  If same-colored lines exist, find the nearest one based on strict perpendicular distance. That is, for a horizontal line, the agent must be in the same column as some part of the line segment; for a vertical line, the agent must be in the same row as some part of the line segment. If multiple lines are equidistant, the first one found (implicit order: horizontal then vertical, then by row/col index) is chosen.
    d.  Calculate the target position, which is one step away from the nearest line, on the same side as the agent's original position (moving towards the line).
    e.  Check the path: Examine
---
