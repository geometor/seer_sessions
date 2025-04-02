import copy

def transform(input_grid):
    """
    Applies a gravity-like effect to orange pixels (7) within a grid. 
    Orange pixels fall downwards within their respective columns until they 
    reach the bottom edge of the grid or land on top of another orange pixel 
    in the same column. White pixels (0) remain unchanged.
    """

    # Get grid dimensions
    height = len(input_grid)
    width = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input_grid
    # We will modify this grid directly
    output_grid = [row[:] for row in input_grid] 

    # Iterate through each column
    for c in range(width):
        # Keep track of where the next fallen pixel should land in this column
        # Start from the bottom row
        landing_row = height - 1

        # Iterate through the rows of the current column from bottom to top
        for r in range(height - 1, -1, -1):
            # If the current pixel is orange (the falling object)
            if input_grid[r][c] == 7:
                # If the original position is not the target landing position
                if r != landing_row:
                    # Move the orange pixel to the landing spot
                    output_grid[landing_row][c] = 7
                    # Make the original spot white (empty)
                    output_grid[r][c] = 0 
                
                # Update the next landing spot to be one row above the current one
                landing_row -= 1
            # If the original pixel was white and we are below the current landing_row,
            # ensure the output grid also reflects white (this handles clearing space above settled pixels)
            elif input_grid[r][c] == 0 and r < landing_row + 1:
                 output_grid[r][c] = 0


    return output_grid