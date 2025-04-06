# Modified check inside loop:
            if is_valid(nr, nc, rows, cols) and \
               (nr, nc) not in visited and \
               output_grid[nr][nc] == fillable_value: # Check output_grid instead of input_grid