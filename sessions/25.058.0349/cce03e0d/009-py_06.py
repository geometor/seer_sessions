def get_grid_dimensions(grid_string):
    rows = grid_string.strip().split('\n')
    height = len(rows)
    width = len(rows[0]) if rows else 0
    return height, width

# Example grids represented as strings for code execution
example_grids = {
    "train_1_in": "111\n111\n111",
    "train_1_out": "000000111\n000000111\n000000111\n000000000\n000000000\n000000000\n111000000\n111000000\n111000000",
    "train_2_in": "11111\n11111\n11111\n11111\n11111",
    "train_2_out": "0000000000011111\n0000000000011111\n0000000000011111\n0000000000011111\n0000000000011111\n000000000000000\n000000000000000\n000000000000000\n000000000000000\n000000000000000\n000000000000000\n111110000000000\n111110000000000\n111110000000000\n111110000000000",
    "train_3_in": "11\n11",
    "train_3_out": "000011\n000011\n000000\n000000\n110000\n110000",
}

dimensions = {}
for name, grid_string in example_grids.items():
    dimensions[name] = get_grid_dimensions(grid_string)

print(dimensions)