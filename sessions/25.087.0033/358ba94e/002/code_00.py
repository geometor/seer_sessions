    output_grid = np.zeros((block_size, block_size), dtype=int)
    for r_out in range(block_size):
        for c_out in range(block_size):
            reference_color = found_blocks[0][r_out, c_out] # Takes color from the *first* block
            is_consistent = True 
            for i in range(1, len(found_blocks)): # Compares against the first block's color
                current_color = found_blocks[i][r_out, c_out]
                if current_color != reference_color:
                    is_consistent = False
                    break 
            
            if is_consistent:
                output_grid[r_out, c_out] = reference_color # Uses the first block's color if consistent
            else:
                output_grid[r_out, c_out] = 0 