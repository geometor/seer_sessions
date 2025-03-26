import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating a larger output grid (double the height and width)
    composed of four quadrants.
    - Top-left quadrant: The original input grid.
    - Top-right quadrant: The input grid flipped horizontally.
    - Bottom-left quadrant: The input grid flipped vertically.
    - Bottom-right quadrant: The input grid flipped both horizontally and vertically.
    """

    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Determine the height (H) and width (W) of the input grid
    H, W = input_np.shape

    # Create a new output grid with dimensions 2H x 2W, initialized with zeros (or any placeholder)
    output_grid = np.zeros((2 * H, 2 * W), dtype=int)

    # 1. Copy the original input grid into the top-left quadrant
    output_grid[0:H, 0:W] = input_np

    # 2. Create a horizontally flipped version and copy to the top-right quadrant
    flipped_horizontal = np.fliplr(input_np)
    output_grid[0:H, W:2*W] = flipped_horizontal

    # 3. Create a vertically flipped version and copy to the bottom-left quadrant
    flipped_vertical = np.flipud(input_np)
    output_grid[H:2*H, 0:W] = flipped_vertical

    # 4. Create a version flipped both horizontally and vertically and copy to the bottom-right quadrant
    # Can flip the original twice or flip one of the already flipped versions once
    flipped_both = np.fliplr(flipped_vertical) # Or np.flipud(flipped_horizontal) or np.fliplr(np.flipud(input_np))
    output_grid[H:2*H, W:2*W] = flipped_both

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()
