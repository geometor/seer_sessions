import numpy as np

# Example Data (replace with actual data from the task)
# ... (Input and Output grids for all training examples)

#Function for ease of use
def get_grid(grid_string):
    rows = grid_string.strip().split('\n')
    return np.array([[int(pixel) for pixel in row] for row in rows])

example_data = [
  {
    "input": get_grid("""
000000000
000000000
000006660
111111111
000000000
000000000
000000000
000000000
000000000"""),
    "output": get_grid("""
0060
0060
7777
0000""")
    },
  {
    "input": get_grid("""
000002220
000000000
000000000
111111111
000000000
000000000
000000000
000000000
000000000"""),
    "output": get_grid("""
0220
0000
7777
0000""")
      
  },
  {
    "input": get_grid("""
000003330
000000000
000000000
000000000
111111111
000000000
000000000
000000000
000000000"""),
    "output": get_grid("""
0330
0000
7777
0000""")
  }
]

# Function to check the blue row
def find_blue_row(grid):
    for i in range(grid.shape[0]):
        if all(grid[i, :] == 1):
            return i
    return None  # No blue row found

# Test on input data
for example in example_data:
    input_grid = example["input"]
    output_grid = example["output"]
    
    
    blue_row_index = find_blue_row(input_grid)
    print(f"Blue Row Index: {blue_row_index}")
    
    print(f"input shape: {input_grid.shape}")
    print(f"output shape: {output_grid.shape}")

    # check first row object correspondence
    input_row_1 = input_grid[0]
    input_blue_row = blue_row_index
    output_row_1 = []
    for j in range(output_grid.shape[1]):
        output_row_1.append(input_row_1[j + input_grid.shape[1]-output_grid.shape[1]])
        
    print(f"output_row_1 match: {output_row_1 == list(output_grid[0])}")
    
    # check row below blue row correspondence
    input_row_blue_plus_one = input_grid[input_blue_row + 1]
    output_row_4 = []
    for j in range(output_grid.shape[1]):
        output_row_4.append(input_row_blue_plus_one[j + input_grid.shape[1]-output_grid.shape[1]])

    print(f"output_row_4 match: {output_row_4 == list(output_grid[3])}")