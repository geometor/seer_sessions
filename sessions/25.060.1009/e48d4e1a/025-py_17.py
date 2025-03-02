    import numpy as np
    grid = np.array([[5, 0, 3, 0, 0], [0, 0, 3, 0, 0], [3, 3, 3, 3, 3], [0, 0, 3, 0, 0], [0, 0, 3, 0, 0]])
    rows, cols = grid.shape
    horizontal_line = None
    vertical_line = None

    for r in range(rows):
        if np.all(grid[r, :] == grid[r, 0]) and grid[r,0] != 0:
            horizontal_line = r
            break

    for c in range(cols):
        if np.all(grid[:, c] == grid[0, c]) and grid[0,c] != 0:
            vertical_line = c
            break
            
    print(horizontal_line, vertical_line)
    ```
    output
    ```text
    None None
    ```
    - Find cross is not working as expected.

**Example 1 (Incorrect):**

*   **Input:** A green cross-like shape and grey at (0,5).
*   **Expected Output:** move green from (2,1) to (2,0) and gray disappears.
*   **Actual Output:** Green pixel at (2,1) disappears, and the grey pixel in (0,5) remains.
*    Find Cross Results:
    ```python
    import numpy as np
    grid = np.array([[0, 0, 0, 0, 0, 5, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0], [0, 3, 3, 3, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3]])
    rows, cols = grid.shape
    horizontal_line = None
    vertical_line = None

    for r in range(rows):
        if np.all(grid[r, :] == grid[r, 0]) and grid[r,0] != 0:
            horizontal_line = r
            break

    for c in range(cols):
        if np.all(grid[:, c] == grid[0, c]) and grid[0,c] != 0:
            vertical_line = c
            break
            
    print(horizontal_line, vertical_line)
    ```
    output
    ```text
    None None
    ```
    - Find cross is not working as expected.

**Example 2 (Incorrect):**

*   **Input:** green at (1,2), (2,0), (2,1), (2,2) and grey at (0,3)
*   **Expected Output:** green at (1,1), (2,0), (2,1), (2,2), no grey.
*   **Actual Output:** no green at (1,2), grey still exist.
*    Find Cross Results:
    ```python
    import numpy as np
    grid = np.array([[0, 0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    rows, cols = grid.shape
    horizontal_line = None
    vertical_line = None

    for r in range(rows):
        if np.all(grid[r, :] == grid[r, 0]) and grid[r,0] != 0:
            horizontal_line = r
            break

    for c in range(cols):
        if np.all(grid[:, c] == grid[0, c]) and grid[0,c] != 0:
            vertical_line = c
            break
            
    print(horizontal_line, vertical_line)
    ```
    output
    ```text
    None None
    ```
     - Find cross is not working as expected.

**YAML Facts:**
