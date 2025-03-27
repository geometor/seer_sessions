import copy

def transform(input_grid):
    """
    Initialize the output grid as a copy of the input grid.
    Iterate through each cell (pixel) of the input grid.
    If a cell contains a gray (5) pixel:
        Identify the 8 neighboring cells (horizontally, vertically, and diagonally adjacent) around this gray pixel.
        For each valid neighbor (within the grid boundaries):
            If the neighbor cell in the input grid is white (0), change its color to blue (1) in the output grid.
    Return the modified output grid.
    """

    # Determine grid dimensions
    height = len(input_grid)
    width = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input_grid
    # This preserves the original gray pixels and background
    output_grid = [row[:] for row in input_grid]

    # Define the 8 relative offsets for neighbors (including diagonals)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell contains a gray pixel (5)
            if input_grid[r][c] == 5:
                # Iterate through the 8 neighbor offsets
                for dr, dc in neighbor_offsets:
                    # Calculate the neighbor's coordinates
                    nr, nc = r + dr, c + dc

                    # Check if the neighbor is within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor cell in the *original* input grid was white (0)
                        # This prevents overwriting other gray pixels if they were neighbors
                        # Although the examples don't show this case, it follows the NL description.
                        # Based on output examples, it seems we should just overwrite regardless of original color,
                        # as long as it's not the center gray pixel itself. Let's adjust based on example outputs.
                        # The examples show the 3x3 area around the gray pixel becomes blue, except the center.
                        # So, we modify the output_grid directly.

                        # Check if the neighbor cell is within the grid boundaries
                        if 0 <= nr < height and 0 <= nc < width:
                           # Set the neighbor cell in the output grid to blue (1)
                           # The initial copy ensures the center gray (5) remains.
                           output_grid[nr][nc] = 1

                # After processing neighbors, ensure the center pixel itself remains gray (5)
                # This is technically already handled by starting with a copy, but reinforces the logic.
                output_grid[r][c] = 5


    return output_grid