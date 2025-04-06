# Previous Code Logic (simplified)
output_grid = copy.deepcopy(input_grid)
num_cols = 5
# for j in range(0, num_cols - 1, 2): -> j = 0, 2
# j = 0: swap(output_grid, 0, 1)
# j = 2: swap(output_grid, 2, 3)