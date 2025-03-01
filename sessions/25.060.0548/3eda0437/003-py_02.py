import numpy as np

def compare_grids(grid1, grid2):
    """
    Compares two grids and returns a dictionary of differences.
    """
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"

    diff_coords = np.where(grid1 != grid2)
    differences = []
    for i in range(len(diff_coords[0])):
        row = diff_coords[0][i]
        col = diff_coords[1][i]
        differences.append({
            'row': row,
            'col': col,
            'grid1_value': int(grid1[row, col]),
            'grid2_value': int(grid2[row, col])
        })

    return differences

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for i in range(rows):
      row_sequences = get_contiguous_sequences(input_grid[i,:])
      
      #check each row
      for start, end, value in row_sequences:
        if value == 0: #if white
          if end+1 < cols and input_grid[i,end+1] == 1: #if blue to the right
            for j in range(start,end+1):
              output_grid[i,j] = 6
    
    # Iterate through each column
    for j in range(cols):
      col_sequences = get_contiguous_sequences(input_grid[:,j])
          
      #check each column
      for start, end, value in col_sequences:
        if value == 0: #if white
          if end+1 < rows and input_grid[end+1,j] == 1: #if blue to the bottom
            for i in range(start,end+1):
              output_grid[i,j] = 6

    return output_grid

def get_contiguous_sequences(row):
    """
    Finds contiguous sequences of the same value in a row.
    Returns a list of (start_index, end_index, value) tuples.
    """
    sequences = []
    if not row.size:
        return sequences

    start = 0
    current_value = row[0]
    for i in range(1, len(row)):
        if row[i] != current_value:
            sequences.append((start, i - 1, current_value))
            start = i
            current_value = row[i]
    sequences.append((start, len(row) - 1, current_value))
    return sequences

# Example Usage (replace with your actual task data)
task_examples = [
  (np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]]),
   np.array([[6,6,6,6,6,6,6,6,6,6,6,6,6,6,1,0,0,0,0,0],
             [6,6,6,6,6,6,6,6,6,6,6,6,6,6,1,0,0,0,0,0],
             [6,6,6,6,6,6,6,6,6,6,6,6,6,6,1,0,0,0,0,0],
             [6,6,6,6,6,6,6,6,6,6,6,6,6,6,1,0,0,0,0,0],
             [6,6,6,6,6,6,6,6,6,6,6,6,6,6,1,0,0,0,0,0],
             [6,6,6,6,6,6,6,6,6,6,6,6,6,6,1,0,0,0,0,0]])),
  
    (np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]),
   np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])),
    
    (np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]]),
     np.array([[6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,1,0],
              [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,1,0],
              [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,1,0],
              [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,1,0],
              [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,1,0],
              [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,1,0]])),
              ]

results = []
for input_grid, expected_output in task_examples:
    predicted_output = transform(input_grid)
    differences = compare_grids(predicted_output, expected_output)
    results.append({
        'input': input_grid.tolist(),
        'expected_output': expected_output.tolist(),
        'predicted_output': predicted_output.tolist(),
        'differences': differences
    })
print(results)