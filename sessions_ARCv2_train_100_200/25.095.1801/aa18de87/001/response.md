```python
import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding horizontal segments between non-zero 
    boundary markers within each row and filling the zeros within those segments 
    with the value 2.

    1. Initialize the output grid as a deep copy of the input grid.
    2. Iterate through each row of the input grid.
    3. For the current row, find the column indices of all cells containing 
       non-zero values (boundary markers).
    4. If there are fewer than two boundary markers in the row, skip to the next row.
    5. If there are two or more boundary markers, sort their column indices.
    6. Iterate through consecutive pairs of these sorted boundary column indices 
       (col_start, col_end).
    7. For all column indices 'c' strictly between col_start and col_end:
       a. If the cell in the *input* grid at the current row and column 'c' 
          is 0, change the value of the corresponding cell in the *output* 
          grid to 2.
    8. Return the modified output grid.
    """

    # Initialize output_grid as a deep copy to avoid modifying the input directly
    # or having unintended side effects if elements were mutable objects.
    # Using list comprehension for a shallow copy is also sufficient here 
    # since integers are immutable.
    output_grid = [row[:] for row in input_grid] 
    
    num_rows = len(input_grid)
    if num_rows == 0:
        return []
    num_cols = len(input_grid[0]) # Assume non-empty grid or handle empty case

    # Iterate through each row
    for r_idx in range(num_rows):
        row = input_grid[r_idx]
        
        # Find column indices of non-zero boundary markers in the current row
        boundary_indices = [c_idx for c_idx, value in enumerate(row) if value != 0]
        
        # Need at least two markers to define a segment
        if len(boundary_indices) < 2:
            continue
            
        # Sort indices (though enumerate gives them in order, explicit sort is safer)
        boundary_indices.sort() 
        
        # Iterate through consecutive pairs of boundary markers
        for i in range(len(boundary_indices) - 1):
            col_start = boundary_indices[i]
            col_end = boundary_indices[i+1]
            
            # Fill zeros between the boundary markers (exclusive)
            for c_idx in range(col_start + 1, col_end):
                # Check the value in the *original* input grid
                if input_grid[r_idx][c_idx] == 0:
                    # Modify the *output* grid
                    output_grid[r_idx][c_idx] = 2
                    
    return output_grid
```