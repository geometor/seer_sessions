import numpy as np

def transform(input_grid):
    """
    The transformation extracts four overlapping 3x3 subgrids from the 5x7 input grid:
    1. Top-Left (TL): rows 0-2, columns 0-2
    2. Top-Right (TR): rows 0-2, columns 4-6
    3. Bottom-Left (BL): rows 2-4, columns 0-2
    4. Bottom-Right (BR): rows 2-4, columns 4-6

    It then creates a 3x3 output grid by overlaying these four subgrids. 
    For each cell (r, c) in the output grid, its color is determined by taking the 
    maximum color value found at the corresponding cell (r, c) across the four 
    extracted subgrids. This effectively combines the non-white pixels from the 
    four subgrids onto the output grid, treating white (0) as the background.
    """

    # Convert input list of lists to a numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)

    # Define the coordinates for the four 3x3 subgrids
    # Top-Left subgrid
    tl_subgrid = input_array[0:3, 0:3]
    # Top-Right subgrid
    tr_subgrid = input_array[0:3, 4:7]
    # Bottom-Left subgrid
    bl_subgrid = input_array[2:5, 0:3]
    # Bottom-Right subgrid
    br_subgrid = input_array[2:5, 4:7]

    # Initialize the output grid (3x3) with zeros (white)
    output_array = np.zeros((3, 3), dtype=int)

    # Perform element-wise maximum operation to overlay the subgrids
    # Start with the top-left subgrid
    output_array = np.maximum(output_array, tl_subgrid)
    # Overlay the top-right subgrid
    output_array = np.maximum(output_array, tr_subgrid)
    # Overlay the bottom-left subgrid
    output_array = np.maximum(output_array, bl_subgrid)
    # Overlay the bottom-right subgrid
    output_array = np.maximum(output_array, br_subgrid)

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
