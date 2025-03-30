import numpy as np

"""
Tiles the input grid pattern to create the output grid. 
The number of vertical repetitions is equal to the height of the input grid (H).
The number of horizontal repetitions is equal to the width of the input grid (W).
The output grid dimensions will be (H * H) rows and (W * W) columns.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Repeats the input grid pattern based on its own dimensions.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the tiled output grid.
    """
    # Convert input list of lists to numpy array if it's not already
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int)

    # Determine the height (H) and width (W) of the input grid
    input_height, input_width = input_grid.shape

    # Calculate the number of repetitions needed vertically (H) and horizontally (W)
    vertical_reps = input_height
    horizontal_reps = input_width

    # Tile the input grid using numpy.tile
    # np.tile repeats the input array according to the specified repetitions tuple (vertical_reps, horizontal_reps)
    output_grid = np.tile(input_grid, (vertical_reps, horizontal_reps))

    return output_grid
