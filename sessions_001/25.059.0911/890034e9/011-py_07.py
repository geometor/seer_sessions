        import numpy as np

        input_grid2 = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 8, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])

        output_grid2 = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        
        def get_positions(grid, color):
            positions = []
            for r in range(grid.shape[0]):
                for c in range(grid.shape[1]):
                    if grid[r,c] == color:
                        positions.append((r,c))
            return positions
        
        azure_pixels_in = get_positions(input_grid2, 8)
        azure_pixels_out = get_positions(output_grid2, 8)

        print(f"Azure Pixels Input: {azure_pixels_in}")
        print(f"Azure Pixels Output: {azure_pixels_out}")

        ```
        
        ```
        Azure Pixels Input: [(2, 4), (3, 4), (3, 7), (4, 4)]
        Azure Pixels Output: [(3, 7)]
        ```

*   **Example 3:**
    *    Input: Multiple separated azure regions, mostly 1x1, one 1 x 2.
    *   Expected Output: All azure pixels replaced with the color of the pixel above.
    *   Actual Output: Only the 1x2 region of azure is replaced.
    *   Metrics:
         ```python
         import numpy as np

         input_grid3 = np.array([
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
             [0, 8, 0, 0, 8, 0, 0, 8, 0, 0],
             [0, 0, 0, 0, 8, 8, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
         ])

         output_grid3 = np.array([
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
         ])
        
         def get_positions(grid, color):
             positions = []
             for r in range(grid.shape[0]):
                 for c in range(grid.shape[1]):
                     if grid[r,c] == color:
                         positions.append((r,c))
             return positions
        
         azure_pixels_in = get_positions(input_grid3, 8)
         azure_pixels_out = get_positions(output_grid3, 8)

         print(f"Azure Pixels Input: {azure_pixels_in}")
         print(f"Azure Pixels Output: {azure_pixels_out}")

         ```
         
         ```
        Azure Pixels Input: [(2, 1), (2, 4), (2, 7), (3, 4), (3, 5)]
        Azure Pixels Output: []
         ```

**YAML Facts**
