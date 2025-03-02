import numpy as np

def grid_to_np(grid_str):
    return np.array([list(map(int, row)) for row in grid_str.split('\n')])
def print_analysis(input_grid, output_grid, predicted_grid):
  input_np = grid_to_np(input_grid)
  output_np = grid_to_np(output_grid)
  predicted_np = grid_to_np(predicted_grid)
  print(f"Input:\n{input_np}\n")
  print(f"Expected Output:\n{output_np}\n")
  print(f"Predicted Output:\n{predicted_np}\n")
  print(f"Equal: {np.array_equal(output_np, predicted_np)}\n")
  print(f"Input Green Count: {np.sum(input_np == 3)}")
  print(f"Input Red Count: {np.sum(input_np == 2)}")
  print(f"Output Green Count: {np.sum(output_np == 3)}")
  print(f"Output Red Count: {np.sum(output_np == 2)}")

input_grid1 = """
00000000
00000000
00003000
00000000
00000000
00000002
""".strip()

output_grid1 = """
00000000
00000000
00000000
00000000
00003000
22222222
""".strip()

predicted_grid1 = """
00000002
00000002
00003002
00000002
00000002
00000002
""".strip()
print_analysis(input_grid1, output_grid1, predicted_grid1)

input_grid2 = """
0000000000
0000000000
8888888888
0000000200
0000003000
""".strip()

output_grid2 = """
8888888888
8888888888
8888888888
2222222222
0000000000
""".strip()

predicted_grid2 = """
8888888888
8888888888
8888888888
2222222222
0000003000
""".strip()

print_analysis(input_grid2, output_grid2, predicted_grid2)

input_grid3 = """
0000000000
0000000000
0000000000
0222222220
0000000300
""".strip()

output_grid3 = """
0000000000
0000000000
0000000000
2222222222
0000000000
""".strip()
predicted_grid3 = """
0000000000
0000000000
0000000000
2222222222
0000000300
""".strip()
print_analysis(input_grid3, output_grid3, predicted_grid3)
