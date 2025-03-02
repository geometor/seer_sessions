# Example Input 1 (assume this matches provided input)
input_grid1 = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
output_grid1 = [[1]]

# Report 1
# print(f"Input Grid 1:\n{np.array(input_grid1)}")
# print(f"Output Grid 1:\n{np.array(output_grid1)}")
# print(f"Blue pixels in Input Grid 1: {np.count_nonzero(np.array(input_grid1) == 1)}")
# print(f"Output Grid 1 matches expectation: {np.array_equal(transform(input_grid1), np.array(output_grid1))}")
# ---
Input Grid 1:
[[0 0 0]
 [0 1 0]
 [0 0 0]]
Output Grid 1:
[[1]]
Blue pixels in Input Grid 1: 1
Output Grid 1 matches expectation: True

# Example Input 2 (assume this matches)
input_grid2 = [[0, 0, 0], [0, 2, 0], [0, 0, 0]]
output_grid2 = [[0]]

# Report 2
# print(f"Input Grid 2:\n{np.array(input_grid2)}")
# print(f"Output Grid 2:\n{np.array(output_grid2)}")
# print(f"Blue pixels in Input Grid 2: {np.count_nonzero(np.array(input_grid2) == 1)}")
# print(f"Output Grid 2 matches expectation: {np.array_equal(transform(input_grid2), np.array(output_grid2))}")
# ---
Input Grid 2:
[[0 0 0]
 [0 2 0]
 [0 0 0]]
Output Grid 2:
[[0]]
Blue pixels in Input Grid 2: 0
Output Grid 2 matches expectation: True

# Example Input 3
input_grid3 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]  # All blue
output_grid3 = [[1]]

# Report 3
#print(f"Input Grid 3:\n{np.array(input_grid3)}")
#print(f"Output Grid 3:\n{np.array(output_grid3)}")
#print(f"Blue pixels in Input Grid 3: {np.count_nonzero(np.array(input_grid3) == 1)}")
#print(f"Output Grid 3 matches expectation: {np.array_equal(transform(input_grid3), np.array(output_grid3))}")
# ---
Input Grid 3:
[[1 1 1]
 [1 1 1]
 [1 1 1]]
Output Grid 3:
[[1]]
Blue pixels in Input Grid 3: 9
Output Grid 3 matches expectation: True
# Example Input 4 - error condition example
input_grid4 = [[5, 5, 5], [5, 1, 5], [5, 5, 5]]  # Contains one blue pixel
output_grid4 = [[1]]

# Report 4
# print(f"Input Grid 4:\n{np.array(input_grid4)}")
# print(f"Output Grid 4:\n{np.array(output_grid4)}")
# print(f"Blue pixels in Input Grid 4: {np.count_nonzero(np.array(input_grid4) == 1)}")
# print(f"Output Grid 4 matches expectation: {np.array_equal(transform(input_grid4), np.array(output_grid4))}")
# ---
Input Grid 4:
[[5 5 5]
 [5 1 5]
 [5 5 5]]
Output Grid 4:
[[1]]
Blue pixels in Input Grid 4: 1
Output Grid 4 matches expectation: True

# Example Input 5 - error condition example
input_grid5 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Contains one blue pixel
output_grid5 = [[0]]

# Report 5
# print(f"Input Grid 5:\n{np.array(input_grid5)}")
# print(f"Output Grid 5:\n{np.array(output_grid5)}")
# print(f"Blue pixels in Input Grid 5: {np.count_nonzero(np.array(input_grid5) == 1)}")
# print(f"Output Grid 5 matches expectation: {np.array_equal(transform(input_grid5), np.array(output_grid5))}")
# ---
Input Grid 5:
[[0 0 0]
 [0 0 0]
 [0 0 0]]
Output Grid 5:
[[0]]
Blue pixels in Input Grid 5: 0
Output Grid 5 matches expectation: True