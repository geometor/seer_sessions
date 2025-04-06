import numpy as np # Using numpy for easier array slicing and boolean operations

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Combines two 4x4 subgrids from the input using a logical XOR operation 
    to produce a 4x4 output grid. The top subgrid (rows 0-3) uses 1=True, 0=False. 
    The bottom subgrid (rows 5-8) uses 2=True, 0=False. The separator row 
    (row 4) is ignored. The output grid uses 3=True, 0=False.
    """

    # Convert input list of lists to a numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)

    # --- Step 1: Identify and extract the two subgrids ---
    # Extract the top 4x4 subgrid (rows 0-3)
    top_subgrid = input_array[0:4, :]
    # Extract the bottom 4x4 subgrid (rows 5-8)
    bottom_subgrid = input_array[5:9, :] # Note: index 9 is exclusive

    # --- Step 2: Create a new empty 4x4 output_grid ---
    # Initialize with zeros, matching the dimensions of the subgrids
    output_grid = np.zeros((4, 4), dtype=int)

    # --- Step 3 & 4: Iterate and apply XOR logic ---
    # Iterate through each cell position (row i, column j)
    for i in range(4):
        for j in range(4):
            # a. Determine logical value for top subgrid cell
            # Map 1 to True, 0 to False
            top_val_bool = (top_subgrid[i, j] == 1)

            # b. Determine logical value for bottom subgrid cell
            # Map 2 to True, 0 to False
            bottom_val_bool = (bottom_subgrid[i, j] == 2)

            # c. Calculate the logical XOR
            xor_result = top_val_bool ^ bottom_val_bool # '^' is the XOR operator

            # d. Set the output grid value based on XOR result
            # Map True to 3, False to 0
            output_grid[i, j] = 3 if xor_result else 0

    # --- Step 5: Return the completed output_grid ---
    # Convert the numpy array back to a list of lists for the return type
    return output_grid.tolist()
