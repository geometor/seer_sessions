Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import copy
from collections import deque

"""
Transforms an input grid based on the following rules:
1. Identify marker cells (value 6).
2. For each marker cell, determine if it's "active". A marker is active if a search (BFS) starting from its adjacent background cells (value 0) can eventually reach a cell adjacent to a boundary cell (value 3). The search propagates only through background cells (value 0) using the initial grid state.
3. Identify all background cells (value 0) that are adjacent (up, down, left, right) to any *active* marker cell. These are the potential starting points for the fill.
4. Perform a flood fill operation using color 3.
5. Initiate the fill from each unique potential starting point identified in step 3, if that point hasn't already been filled in the output grid.
6. The flood fill propagates only through background cells (value 0) in the output grid.
7. The fill stops at grid boundaries or any cell that is not a background cell (value 0) - this includes original boundary cells (3), original marker cells (6), and cells already filled with 3 during
---
