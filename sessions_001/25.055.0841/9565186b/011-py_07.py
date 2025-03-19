        # input_grid contains red and blue pixels
        # output_grid = transform(input_grid)
        # assert np.all(output_grid[input_grid == 1] == 1)  # Blue remains blue
        # assert np.all(output_grid[input_grid == 2] == 5) #Red pixels become gray
        ```

*   **Example 2:**
    *   Input: Contains blue and yellow.
    *   Output: Blue pixels remain, yellow pixels turn grey.
    *   *Conceptual Code Execution:*
        ```python
        # input_grid contains blue and yellow pixels
        # output_grid = transform(input_grid)
        # assert np.all(output_grid[input_grid == 1] == 1)  # Blue remains blue
        # assert np.all(output_grid[input_grid == 4] == 5)  # Yellow becomes gray
        ```

*   **Example 3:**
    *   Input: Contains blue and green pixels.
    *    Output: Blue pixels remain, green become gray.
    *   *Conceptual Code Execution:*
        ```python
        # input_grid contains blue, green, and magenta pixels
        # output_grid = transform(input_grid)
        # assert np.all(output_grid[input_grid == 1] == 1) # Blue remains blue
        # assert np.all(output_grid[input_grid == 3] == 5)  # Green becomes gray

        ```

**YAML Facts:**
