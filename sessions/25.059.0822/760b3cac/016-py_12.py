"""
The transformation rule preserves yellow (4) pixels and rearranges azure (8) pixels. The azure pixels in the top left corner form an "L" shape (3 pixels). This "L" shape's is replicated. Empty spaces to the left and right of "L" shape are also filled.
"""

import numpy as np

def get_l_shape_block(grid):
    # find azure pixels
    azure_pixels = np.argwhere(grid == 8)
    # return if no azure
    if len(azure_pixels) == 0:
        return None, None
    
    # Find top-leftmost azure pixel
    top_left_most = azure_pixels[np.lexsort((azure_pixels[:, 1], azure_pixels[:, 0]))[0]]
    
    # check whether two azure pixels by checking one row below, and one col right
    block = [top_left_most.tolist()]

    # Check right
    right_neighbor = [top_left_most[0], top_left_most[1] + 1]
    if list(right_neighbor) in azure_pixels.tolist():
        block.append(right_neighbor)
    
    # Check bottom
    bottom_neighbor = [top_left_most[0] + 1, top_left_most[1]]
    if list(bottom_neighbor) in azure_pixels.tolist():
        block.append(bottom_neighbor)

    # check diagonal
    diagonal_neighbor = [top_left_most[0] + 1, top_left_most[1] + 1]
    if list(diagonal_neighbor) in azure_pixels.tolist():
        block.append(diagonal_neighbor)

    # check left
    left_neighbor = [top_left_most[0], top_left_most[1] - 1]
    if list(left_neighbor) in azure_pixels.tolist():
        block.append(left_neighbor)
    
    
    # Check two bottom
    two_bottom_neighbor = [top_left_most[0] + 2, top_left_most[1]]
    if list(two_bottom_neighbor) in azure_pixels.tolist():
        block.append(two_bottom_neighbor)

    
    
    return block, len(block)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # get l shape block, do it only if azure is present
    l_shape_block, num = get_l_shape_block(input_grid)
    
    if (l_shape_block is not None) and (num==3) :

        # turn all azure to white
        output_grid[output_grid == 8] = 0

        # get dimensions to fill
        min_row = min(l_shape_block, key=lambda x: x[0])[0]
        max_row = max(l_shape_block, key=lambda x: x[0])[0]
        min_col = min(l_shape_block, key=lambda x: x[1])[1]
        max_col = max(l_shape_block, key=lambda x: x[1])[1]

        for row in range(min_row, max_row + 1):
                for col in range(min_col-1, max_col + 2): # expand on two sides, left and right
                    if 0<= row < output_grid.shape[0] and 0 <= col < output_grid.shape[1]:
                        output_grid[row, col] = 8


    return output_grid