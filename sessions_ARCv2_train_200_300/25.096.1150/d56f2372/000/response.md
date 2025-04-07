Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
**Perception of Task Elements:**

1.  **Input:** The input is a 2D grid (matrix) containing non-negative integers. Zero represents the background. Non-zero integers represent different "colors" or types of objects. The input grid typically contains multiple distinct objects, where each object is a connected component of cells sharing the same non-zero integer value.
2.  **Output:** The output is also a 2D grid, generally smaller than the input. It represents a single object extracted from the input grid.
3.  **Transformation:** The core task involves identifying all distinct objects in the input, selecting one specific object based on a set of criteria, and then creating a new grid containing only that selected object, cropped to its minimal bounding box.
4.  **Object Identification:** Objects are groups of connected cells (sharing an edge or corner, i.e., 8-connectivity) with the same non-zero value.
5.  **Selection Criteria:** A specific object must be chosen from the multiple objects present. Analysis of the examples suggests a primary rule with a specific exception:
    *   **Primary Rule:** Identify the object whose bounding box appears "highest" (minimum top row index) in the grid. If multiple objects share the same minimum top row, select the one whose bounding box is "leftmost" (minimum left column index). Let's call this object `O_hl`.
    *   **Exception Rule:** Find the minimum color value (`min_c`) among all objects and the maximum size (pixel count) (`max_s`) among all objects. If there is exactly one object (`O_special`) that simultaneously has the color `min_c` AND the size `max_s`, AND this `O_special` object is *different* from `O_hl`, then select `O_special`.
---
