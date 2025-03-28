# Corrected drawing for hollow frame
output_grid[new_min_r, new_min_c:new_max_c+1] = 3  # Top
output_grid[new_max_r, new_min_c:new_max_c+1] = 3  # Bottom
output_grid[new_min_r:new_max_r+1, new_min_c] = 3  # Left
output_grid[new_min_r:new_max_r+1, new_max_c] = 3  # Right