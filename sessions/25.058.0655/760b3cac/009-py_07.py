    import numpy as np
    input_grid = np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,4,4,4,0,0,0],[0,0,0,0,4,4,4,0,0,0],[0,0,0,0,4,4,4,0,0,0],[0,0,0,0,0,0,0,0,0,0],[8,8,8,8,8,8,8,8,8,8],[8,8,8,8,8,8,8,8,8,8]])
    expected_output = np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,4,4,4,0,0,0],[0,0,0,0,4,4,4,0,0,0],[0,0,0,0,4,4,4,0,0,0],[0,0,0,0,0,0,0,0,0,0],[8,8,8,8,8,8,8,8,8,8],[8,8,8,8,8,8,8,8,8,8]])
    actual_output = transform(input_grid)

    # check to see if they are equal
    print(np.array_equal(expected_output,actual_output))
    # show where they are not equal
    print(np.where(expected_output != actual_output))
    # find azure
    print(f"Azure: {np.argwhere(input_grid == 8)}")
    # find yellow
    print(f"Yellow: {np.argwhere(input_grid == 4)}")

    ```

    ```
    True
    (array([], dtype=int64), array([], dtype=int64))
    Azure: [[8 0]
    [8 1]
    [8 2]
    [8 3]
    [8 4]
    [8 5]
    [8 6]
    [8 7]
    [8 8]
    [8 9]
    [9 0]
    [9 1]
    [9 2]
    [9 3]
    [9 4]
    [9 5]
    [9 6]
    [9 7]
    [9 8]
    [9 9]]
    Yellow: [[4 4]
    [4 5]
    [4 6]
    [5 4]
    [5 5]
    [5 6]
    [6 4]
    [6 5]
    [6 6]]
    ```
*   Observation: The code works as expected for this case.

**Example 2**

*   **Summary:** Azure extends to the right until blocked by the yellow object. Yellow shape remains in place.
*   Metrics:

    ```python
    import numpy as np

    input_grid = np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,4,4,4,0,0,0,0],[0,0,0,4,4,4,0,0,0,0],[0,0,0,4,4,4,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[8,8,8,8,8,8,0,0,0,0],[8,8,8,8,8,8,0,0,0,0],[8,8,8,8,8,8,0,0,0,0]])
    expected_output = np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,4,4,4,0,0,0,0],[0,0,0,4,4,4,0,0,0,0],[0,0,0,4,4,4,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,8,8,0,0],[0,0,8,8,8,8,8,8,0,0],[0,0,8,8,8,8,8,8,0,0]])
    actual_output = transform(input_grid)

    print(np.array_equal(expected_output, actual_output))
    print(np.where(expected_output != actual_output))
    print(f"Azure: {np.argwhere(input_grid == 8)}")
    print(f"Yellow: {np.argwhere(input_grid == 4)}")
    ```

    ```
    False
    (array([7, 7, 8, 8, 9, 9]), array([2, 3, 2, 3, 2, 3]))
    Azure: [[7 0]
    [7 1]
    [7 2]
    [7 3]
    [7 4]
    [7 5]
    [8 0]
    [8 1]
    [8 2]
    [8 3]
    [8 4]
    [8 5]
    [9 0]
    [9 1]
    [9 2]
    [9 3]
    [9 4]
    [9 5]]
    Yellow: [[2 3]
    [2 4]
    [2 5]
    [3 3]
    [3 4]
    [3 5]
    [4 3]
    [4 4]
    [4 5]]

    ```
*   Observation: The azure extends all the way to the edge. The yellow object prevents further extension, but the program does not recognize this and extends azure anyway, overwriting the empty space.

**Example 3**

*   **Summary:** The azure shape expands to the right and down, filling the available space adjacent to its initial position, stopping when it encounters the yellow shape or the grid boundaries.
*   Metrics:

    ```python
    import numpy as np

    input_grid = np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,4,4,4,0,0,0,0],[0,0,0,4,4,4,0,0,0,0],[0,0,0,4,4,4,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[8,8,8,0,0,0,0,0,0,0],[8,8,8,0,0,0,0,0,0,0],[8,8,8,0,0,0,0,0,0,0]])
    expected_output = np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,4,4,4,0,0,0,0],[0,0,0,4,4,4,0,0,0,0],[0,0,0,4,4,4,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,8,8,8,0,0,0,0,0,0],[0,8,8,8,0,0,0,0,0,0],[0,8,8,8,0,0,0,0,0,0]])
    actual_output = transform(input_grid)

    print(np.array_equal(expected_output, actual_output))
    print(np.where(expected_output != actual_output))
    print(f"Azure: {np.argwhere(input_grid == 8)}")
    print(f"Yellow: {np.argwhere(input_grid == 4)}")

    ```

    ```
    False
    (array([7, 8, 9]), array([1, 1, 1]))
    Azure: [[7 0]
    [7 1]
    [7 2]
    [8 0]
    [8 1]
    [8 2]
    [9 0]
    [9 1]
    [9 2]]
    Yellow: [[3 3]
    [3 4]
    [3 5]
    [4 3]
    [4 4]
    [4 5]
    [5 3]
    [5 4]
    [5 5]]
    ```
*   Observation: The azure should only extend one space to the right on each row. Currently it only changes the first column next to the original object.

**YAML Documentation**
