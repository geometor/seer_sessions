import numpy as np

def find_vertical_line(grid, color):
    # Find the rightmost column
    for j in range(grid.shape[1] - 1, -1, -1):
        # Check if the entire column is of the specified color
        if np.all(grid[:, j] == color):
            return j
    return -1  # Not found

def find_horizontal_finger(grid, line_col, line_color):
    # Find the row where the vertical line ends
    for i in range(grid.shape[0] - 1, -1, -1):
        if grid[i, line_col] == line_color:
            # Scan to the left from this point
            finger = []
            for j in range(line_col, -1, -1):
                if grid[i,j] != 0:
                  finger.append( (i, j, grid[i, j]) )
                else:
                   break
            return finger[::-1]  #correct the reversing
    return []  # Not found
def find_finger(grid, line_col, line_color):
    #find the row where line starts
    for start_row in range(grid.shape[0]):
      if grid[start_row, line_col] == line_color:
        break;

    # Find the row where the vertical line ends
    for end_row in range(grid.shape[0] - 1, -1, -1):
        if grid[end_row, line_col] == line_color:
            break
    else:
      return [] #no line found

    #check above
    finger = []
    if start_row > 0:
      for row in range(start_row -1, -1, -1):
        if grid[row, line_col] != 0:
          finger.append( (row, line_col, grid[row, line_col]) )
        else:
          break
    if finger:
      return finger

    #check below
    finger = []
    if end_row < grid.shape[0]-1:
      for row in range(end_row + 1, grid.shape[0]):
        if grid[row, line_col] != 0:
          finger.append( (row, line_col, grid[row, line_col]) )
        else:
          break

    if finger:
      return finger

    # Scan to the left from line end point
    finger = []
    for j in range(line_col, -1, -1):
        if grid[end_row,j] != 0:
          finger.append( (end_row, j, grid[end_row, j]) )
        else:
            break
    if finger:
        return finger[::-1]  #correct the reversing

    #scan to the left from line start point
    finger = []
    for j in range(line_col, -1, -1):
        if grid[start_row,j] != 0:
          finger.append( (start_row, j, grid[start_row, j]) )
        else:
            break
    if finger:
       return finger[::-1]  #correct the reversing

    return []

def analyze_transformation(input_grid, output_grid):
    red_line_col_input = find_vertical_line(input_grid, 2)
    red_line_col_output = find_vertical_line(output_grid, 2)

    finger_input = find_finger(input_grid, red_line_col_input, 2)
    finger_output = find_finger(output_grid, red_line_col_output, 2)

    return {
      "red_line_input": red_line_col_input,
      "red_line_output": red_line_col_output,
      "finger_input_start": finger_input[0] if finger_input else None,
      "finger_input_end": finger_input[-1] if finger_input else None,
        "finger_output_start": finger_output[0] if finger_output else None,
      "finger_output_end": finger_output[-1] if finger_output else None
    }
examples = [
    (
        np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 2],
                  [3, 3, 1, 2, 0, 0, 0, 2]]),
        np.array([[3, 0, 0, 0, 0, 0, 0, 0],
                  [3, 0, 0, 0, 0, 0, 0, 0],
                  [1, 0, 0, 0, 0, 0, 0, 2],
                  [2, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 2]]),
    ),
    (
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2],
                  [4, 4, 4, 8, 2, 0, 0, 0, 2]]),
        np.array([[4, 0, 0, 0, 0, 0, 0, 0, 0],
                  [4, 0, 0, 0, 0, 0, 0, 0, 0],
                  [4, 0, 0, 0, 0, 0, 0, 0, 0],
                  [8, 0, 0, 0, 0, 0, 0, 0, 2],
                  [2, 0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2]]),
    ),
    (
        np.array([[0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 2],
                  [1, 1, 6, 2, 0, 0, 2]]),
        np.array([[1, 0, 0, 0, 0, 0, 2],
                  [1, 0, 0, 0, 0, 0, 2],
                  [6, 0, 0, 0, 0, 0, 2],
                  [2, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 2]]),
    ),
]

def report(examples):
    for i, (input_grid, output_grid) in enumerate(examples):
        analysis = analyze_transformation(input_grid, output_grid)
        print(f"Example {i+1}:")
        print(f"  Input Grid:\n{input_grid}")
        print(f"  Output Grid:\n{output_grid}")
        print(f"  Analysis: {analysis}")
        # Calculate and print the finger movement
        if analysis["finger_input_start"] and analysis["finger_output_start"]:
            row_diff = analysis["finger_output_start"][0] - analysis["finger_input_start"][0]
            col_diff = analysis["finger_output_start"][1] - analysis["finger_input_start"][1]
            print(f"  Finger Movement: Row Offset = {row_diff}, Column Offset = {col_diff}")

            row_diff = analysis["red_line_output"] - analysis["red_line_input"]
            print(f"  Red Line Movement: Column Offset = {row_diff}")
        else:
            print("  Finger Movement: Not applicable (no finger or no movement)")
        print("-" * 20)
report(examples)