# For each training example:
#   input_grid, expected_output = get_example(example_number)
#   predicted_output = transform(input_grid)
#   differences = find_differences(predicted_output, expected_output)
#   print(f"Example {example_number}:")
#   print(f"  Input Shape: {input_grid.shape}")
#   print(f"  Majority Color: {get_majority_color(input_grid)}")
#   print(f"  Special Pixels: {get_special_pixels(input_grid)}")
#   print(f"  Number of Differences: {len(differences)}")
#   print(f"  Locations of Differences: {differences}") # (row, col, predicted_color, expected_color)

# Example 0 - Correct
# Example 1
# Input Shape: (11, 11)
#   Majority Color: 0
#   Special Pixels: {(1, 1): 8, (1, 2): 8, (2, 1): 8, (2, 2): 8, (1, 5): 1, (2, 5): 1, (1, 8): 4, (2, 8): 4, (5, 1): 1, (5, 2): 1, (8, 1): 4, (8, 2): 4, (5, 5): 8, (5, 6): 8, (6, 5): 8, (6, 6): 8, (5, 9): 4, (6, 9): 4, (8, 5): 1, (8, 6): 1, (9, 5): 1, (9, 6): 1, (8, 9): 8, (9, 9): 8}
#  Number of Differences: 0

# Example 2
# Input Shape: (15, 15)
#   Majority Color: 0
#   Special Pixels:  {(1, 2): 5, (1, 3): 5, (2, 2): 5, (2, 3): 5, (4, 8): 6, (4, 9): 6, (5, 8): 6, (5, 9): 6, (1, 12): 8, (1, 13): 8, (2, 12): 8, (2, 13): 8, (7, 4): 5, (7, 5): 5, (8, 4): 5, (8, 5): 5, (10, 10): 6, (10, 11): 6, (11, 10): 6, (11, 11): 6, (7, 12): 8, (7, 13): 8, (8, 12): 8, (8, 13): 8, (13, 2): 5, (13, 3): 5, (14, 2): 5, (14, 3): 5, (13, 8): 6, (13, 9): 6, (14, 8): 6, (14, 9): 6, (13, 12): 8, (13, 13): 8, (14, 12): 8, (14, 13): 8}
#  Number of Differences: 0

# Example 3
#  Input Shape: (17, 17)
#   Majority Color: 0
# Special Pixels: {(1, 1): 3, (1, 2): 3, (2, 1): 3, (2, 2): 3, (1, 5): 6, (1, 6): 6, (2, 5): 6, (2, 6): 6, (1, 9): 3, (1, 10): 3, (2, 9): 3, (2, 10): 3, (1, 14): 6, (1, 15): 6, (2, 14): 6, (2, 15): 6, (4, 1): 8, (4, 2): 8, (5, 1): 8, (5, 2): 8, (4, 5): 8, (4, 6): 8, (5, 5): 8, (5, 6): 8, (4, 9): 8, (4, 10): 8, (5, 9): 8, (5, 10): 8, (4, 14): 8, (4, 15): 8, (5, 14): 8, (5, 15): 8, (7, 1): 3, (7, 2): 3, (8, 1): 3, (8, 2): 3, (7, 5): 6, (7, 6): 6, (8, 5): 6, (8, 6): 6, (7, 9): 3, (7, 10): 3, (8, 9): 3, (8, 10): 3, (7, 14): 6, (7, 15): 6, (8, 14): 6, (8, 15): 6, (10, 1): 8, (10, 2): 8, (11, 1): 8, (11, 2): 8, (10, 5): 8, (10, 6): 8, (11, 5): 8, (11, 6): 8, (10, 9): 8, (10, 10): 8, (11, 9): 8, (11, 10): 8, (10, 14): 8, (10, 15): 8, (11, 14): 8, (11, 15): 8, (13, 1): 3, (13, 2): 3, (14, 1): 3, (14, 2): 3, (13, 5): 6, (13, 6): 6, (14, 5): 6, (14, 6): 6, (13, 9): 3, (13, 10): 3, (14, 9): 3, (14, 10): 3, (13, 14): 6, (13, 15): 6, (14, 14): 6, (14, 15): 6}
# Number of Differences: 272

# Example 4
# Input Shape: (5, 11)
# Majority Color: 0
# Special Pixels: {(1, 1): 1, (1, 2): 1, (1, 4): 1, (1, 6): 1, (1, 8): 1, (1, 9): 1, (3, 1): 1, (3, 2): 1, (3, 4): 1, (3, 6): 1, (3, 8): 1, (3, 9): 1}
# Number of Differences: 0