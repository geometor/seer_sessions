import numpy as np

def transform(input_grid):
    """
    Transforms an input grid based on the following rule:
    Iterate through each interior cell of the input grid. If a cell's value is 4 
    and all four of its cardinal neighbors (up, down, left, right) also have the 
    value 4, change the cell's value to 6 in the output grid. Otherwise, the cell's 
    value remains unchanged. Border cells are never changed.
    """

    # Convert input list of lists to a NumPy array for easier indexing
    input_array = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the grid
    rows, cols = input_array.shape
    
    # Initialize the output grid as a copy of the input grid
    # This handles border cells and cells that don't meet the transformation criteria
    output_array = np.copy(input_array)

    # Iterate through the interior cells of the grid
    # Exclude the border rows (0 and rows-1) and border columns (0 and cols-1)
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            # Check if the current cell's value is 4
            if input_array[r, c] == 4:
                # Check if all four cardinal neighbors are also 4
                is_up_4 = input_array[r - 1, c] == 4
                is_down_4 = input_array[r + 1, c] == 4
                is_left_4 = input_array[r, c - 1] == 4
                is_right_4 = input_array[r, c + 1] == 4
                
                # If all neighbors are 4, change the cell value in the output grid to 6
                if is_up_4 and is_down_4 and is_left_4 and is_right_4:
                    output_array[r, c] = 6
            # No explicit 'else' needed because output_array was initialized as a copy

    # Convert the NumPy array back to a list of lists for the return value
    output_grid = output_array.tolist()
    
    return output_grid
