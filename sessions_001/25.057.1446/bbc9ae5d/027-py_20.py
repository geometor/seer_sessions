import numpy as np

def code_execution(input_grid, output_grid):
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)
    print(f"Input shape: {input_shape}, Output shape: {output_shape}")
    print(f"Input colors: {input_colors}, Output colors: {output_colors}")
    # Find the orange pixels in input
    input_orange = np.where(input_grid == 7)
    if len(input_orange[0]) >0:
      print(f"Input orange pixels count:{len(input_orange[0])} locations: {[(input_orange[0][i],input_orange[1][i]) for i in range(len(input_orange[0]))]}")
    else:
      print("No orange pixels in input")
    output_orange = np.where(output_grid == 7)
    if len(output_orange[0]) >0:
      print(f"Output orange pixels count:{len(output_orange[0])} locations: {[(output_orange[0][i],output_orange[1][i]) for i in range(len(output_orange[0]))]}")
    else:
      print("No orange pixels in output")

# Example Usage (replace with actual data from each pair):
# Example usage with data from the prompt (Train Example 1):
input_grid1 = np.array([[0, 0, 0, 0, 0, 0], [0, 7, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
output_grid1 = np.array([[0, 0, 0, 0, 0, 0], [7, 7, 7, 0, 0, 0], [7, 7, 7, 0, 0, 0]])

# Example usage with data from the prompt (Train Example 2):
input_grid2 = np.array([[0, 0, 0, 0, 0, 7, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])
output_grid2 = np.array([[0, 0, 0, 0, 0, 7, 7, 7], [0, 0, 0, 0, 0, 7, 7, 7], [0, 0, 0, 0, 0, 7, 7, 7]])

# Example usage with data from the prompt (Train Example 3):
input_grid3 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0, 0]])
output_grid3 = np.array([[0, 0, 0, 0, 7, 7, 7, 0, 0, 0], [0, 0, 0, 0, 7, 7, 7, 0, 0, 0], [0, 0, 0, 0, 7, 7, 7, 0, 0, 0]])

code_execution(input_grid1, output_grid1)
code_execution(input_grid2, output_grid2)
code_execution(input_grid3, output_grid3)