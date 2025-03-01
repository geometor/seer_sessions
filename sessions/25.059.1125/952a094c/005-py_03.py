        import numpy as np
        input_grid = np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 0],
            [0, 8, 8, 8, 8, 8, 0],
            [0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ])
        expected_output = np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 8, 8, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ])
        actual_output = transform(input_grid)
        print(np.array_equal(expected_output,actual_output))
        ```
        `True`

*   **Example 2:**
    *   **Input:** 9x9 grid with an incomplete azure cross (more like a plus sign) in the top-left quadrant. A yellow pixel is above the horizontal line of the azure shape, and a magenta pixel is to its left.
    *   **Expected Output:** The yellow pixel is moved to the second row, and the magenta pixel is moved to the second-to-last row, in their respective columns.
    *   **Actual Output:** Does *not* match. The code likely doesn't identify the "cross" correctly, or miscalculates positions.
        ```python
        import numpy as np
        input_grid = np.array([
            [8, 8, 8, 8, 0, 0, 0, 0, 0],
            [8, 8, 4, 8, 0, 0, 0, 0, 0],
            [8, 8, 8, 8, 0, 0, 0, 0, 0],
            [6, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        expected_output = np.array([
            [8, 8, 8, 8, 0, 0, 0, 0, 0],
            [8, 8, 4, 8, 0, 0, 0, 0, 0],
            [8, 8, 8, 8, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        actual_output = transform(input_grid)
        print(np.array_equal(expected_output, actual_output))

        ```
        `False`
*   **Example 3:**
    *   **Input:**  11x11 grid. An azure "L" shape. a yellow pixel is adjacent and above the azure shape.
    *   **Expected Output:**  The yellow moves to row 2 in the same column.
    *   **Actual Output:** Does *not* match.
        ```python
        import numpy as np
        input_grid = np.array([
          [8,8,0,0,0,0,0,0,0,0,0],
          [8,8,0,0,0,0,0,0,0,0,0],
          [8,4,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0]
        ])
        expected_output = np.array([
          [8,8,0,0,0,0,0,0,0,0,0],
          [8,4,0,0,0,0,0,0,0,0,0],
          [8,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0]
        ])
        actual_output = transform(input_grid)
        print(np.array_equal(expected_output, actual_output))
        ```
        `False`

**YAML Facts**
