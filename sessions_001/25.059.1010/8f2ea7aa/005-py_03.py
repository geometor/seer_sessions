import numpy as np

def analyze_grid(grid, color):
    """Counts and locates pixels of a specific color in a grid."""
    grid_np = np.array(grid)
    count = np.sum(grid_np == color)
    locations = np.argwhere(grid_np == color).tolist()
    return count, locations

# Example usage (Illustrative)
# For the first training example:
input_grid_1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
output_grid_1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

# I would test more colors/examples here, but it's illustrative
azure_count_in, azure_loc_in = analyze_grid(input_grid_1, 8)
black_count_in, black_loc_in = analyze_grid(input_grid_1, 0)

azure_count_out, azure_loc_out = analyze_grid(output_grid_1, 8)
black_count_out, black_loc_out = analyze_grid(output_grid_1, 0)

print(f"Input: Azure Count: {azure_count_in}, Azure Locations: {azure_loc_in}")
print(f"Input: Black Count: {black_count_in}, Black Locations: {black_loc_in}")
print(f"Output: Azure Count: {azure_count_out}, Azure Locations: {azure_loc_out}")
print(f"Output: Black Count: {black_count_out}, Black Locations: {black_loc_out}")

# Repeat for other examples and colors.