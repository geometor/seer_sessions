    # If structure is invalid or not found, return the original grid
    if boundaries is None:
        # print("Warning: Could not determine grid structure. Returning original grid.")
        return input_grid # <<<< Returns original LIST input

    # ... later ...
    # Step 9: Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist() # <<<< Returns modified NUMPY array converted to list