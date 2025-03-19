        import numpy as np
        input_grid = np.array([[0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0],
                              [0, 0, 1, 0, 0],
                              [0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0]])
        expected_output = np.array([[0, 0, 0, 0, 0],
                                   [0, 2, 2, 2, 0],
                                   [0, 2, 1, 2, 0],
                                   [0, 2, 2, 2, 0],
                                   [0, 0, 0, 0, 0]])
        actual_output = transform(input_grid)
        print(np.array_equal(actual_output, expected_output))

        ```
        Output:
        ```
        True
        ```
*   **Example 2:**

    *   Input: A 7x7 grid with two blue pixels, one at (1,1) and another at (5,5).
    *   Expected Output: The blue pixels and their neighbors are red.
    *   `transform(input_grid)` output: Matches the expected output.
    *   Metrics:
        ```python
        import numpy as np
        input_grid = np.array([[0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 0, 0, 0]])
        expected_output = np.array([[2, 2, 0, 0, 0, 0, 0],
                                    [2, 1, 2, 0, 0, 0, 0],
                                    [0, 2, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 2, 2],
                                    [0, 0, 0, 0, 0, 1, 2],
                                    [0, 0, 0, 0, 0, 2, 0]])
        actual_output = transform(input_grid)
        print(np.array_equal(actual_output, expected_output))

        ```
        Output:
        ```
        True
        ```

*   **Example 3:**

    *   Input: 6x6 grid. There is one blue pixel at (2,2) and a horizontal line of three blue pixels at the bottom row.
    *   Expected output: Blue pixels and their neighbors are red.
    *   `transform(input_grid)` output: Matches expected output.
        ```python
        import numpy as np
        input_grid = np.array([[0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [1, 1, 1, 0, 0, 0]])
        expected_output = np.array([[0, 0, 2, 0, 0, 0],
                                   [0, 2, 2, 2, 0, 0],
                                   [0, 2, 1, 2, 0, 0],
                                   [2, 2, 2, 0, 0, 0],
                                   [1, 1, 1, 0, 0, 0],
                                   [2, 2, 2, 0, 0, 0]])
        actual_output = transform(input_grid)
        print(np.array_equal(actual_output, expected_output))
        ```
        Output:
        ```
        True
        ```
**YAML Facts:**
