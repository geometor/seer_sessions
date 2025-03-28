import copy

"""
Identify all 3x1 vertical and 1x3 horizontal blocks of white pixels (0) in the input grid. 
For each such block, check its external 8-connectivity neighbours (pixels adjacent horizontally, vertically, or diagonally, but not part of the block itself). 
If any external neighbour is gray (5) in the input grid, change all pixels within that white block to blue (1) in the output grid. 
All other pixels retain their original color from the input grid.
"""

def get_neighbours(r, c, height, width):
    """Gets the 8-connectivity neighbours for a pixel (r, c) within grid bounds."""
    neighbours = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the pixel itself
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            # Check if the neighbour is within the grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                neighbours.append((nr, nc))
    return neighbours

def check_for_gray_neighbour(input_grid, block_coords, height, width):
    """
    Checks if any external 8-connectivity neighbour of the given block_coords is gray (5).
    
    Args:
        input_grid: The input grid (list of lists).
        block_coords: A set of (row, col) tuples representing the pixels in the block.
        height: The height of the grid.
        width: The width of the grid.
        
    Returns:
        True if a gray external neighbour is found, False otherwise.
    """
    all_neighbours = set()
    # Collect all neighbours for each pixel in the block
    for r, c in block_coords:
        neighbours = get_neighbours(r, c, height, width)
        all_neighbours.update(neighbours)

    # Remove the block's own coordinates to get only external neighbours
    external_neighbours = all_neighbours - block_coords

    # Check if any external neighbour is gray
    for nr, nc in external_neighbours:
        if input_grid[nr][nc] == 5: # 5 is gray
            return True
            
    return False

def transform(input_grid):
    """
    Transforms the input grid by changing specific 3-pixel white blocks to blue
    if they have an adjacent gray pixel.
    """
    # Initialize output_grid as a deep copy of input_grid
    output_grid = copy.deepcopy(input_grid)
    height = len(input_grid)
    width = len(input_grid[0])
    
    # Use a set to store coordinates of pixels to change to avoid duplicates
    pixels_to_change_to_blue = set()

    # 1. Check for 3x1 vertical white blocks
    for r in range(height - 2):
        for c in range(width):
            # Check if the pixels form a 3x1 vertical white block
            if (input_grid[r][c] == 0 and
                input_grid[r+1][c] == 0 and
                input_grid[r+2][c] == 0):
                
                block_coords = {(r, c), (r+1, c), (r+2, c)}
                
                # Check if any external neighbour of this block is gray
                if check_for_gray_neighbour(input_grid, block_coords, height, width):
                    pixels_to_change_to_blue.update(block_coords)

    # 2. Check for 1x3 horizontal white blocks
    for r in range(height):
        for c in range(width - 2):
            # Check if the pixels form a 1x3 horizontal white block
            if (input_grid[r][c] == 0 and
                input_grid[r][c+1] == 0 and
                input_grid[r][c+2] == 0):
                
                block_coords = {(r, c), (r, c+1), (r, c+2)}

                # Check if any external neighbour of this block is gray
                if check_for_gray_neighbour(input_grid, block_coords, height, width):
                    pixels_to_change_to_blue.update(block_coords)

    # 3. Update the output grid
    for r_change, c_change in pixels_to_change_to_blue:
        output_grid[r_change][c_change] = 1 # 1 is blue

    return output_grid