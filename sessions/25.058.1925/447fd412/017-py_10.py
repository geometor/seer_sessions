import numpy as np

def describe_grid(grid, grid_name):
    """Provides a high-level description of objects in the grid."""
    description = f"Grid: {grid_name}\n"
    blue_objects = find_object(grid, 1)
    red_objects = find_object(grid, 2)
    
    if blue_objects:
        num = len(blue_objects)
        description += f"  Blue objects: {num}\n"
        
        for i in range(num):
          description += f"  Blue object {i}:\n"
          shape = "other"
          rows = []
          for r,c in blue_objects[i]:
            rows.append(r)

          if (len(set(rows))==1):
            shape = "horizontal line"
          description += f"    shape = {shape}\n"          
            
    if red_objects:
        num = len(red_objects)
        description += f"  Red objects: {num}\n"
        for i in range(num):
          description += f"  Red object {i}:\n"
          shape = "other"
          rows = []
          cols = []
          for r,c in red_objects[i]:
            rows.append(r)
            cols.append(c)

          min_row = min(rows)
          max_row = max(rows)
          min_col = min(cols)
          max_col = max(cols)

          # Check if it's a square
          if (max_row - min_row + 1) == (max_col - min_col + 1) and len(red_objects[i]) == (max_row-min_row+1)**2:
            shape = "square"
            
          description += f"    shape = {shape}\n"

    return description
  

def compare_grids(grid1, grid2, grid1_name="Grid 1", grid2_name="Grid 2"):
    """Compares two grids and describes the differences."""
    if grid1.shape != grid2.shape:
        return "Grids have different shapes."

    diff = grid1 != grid2
    if not np.any(diff):
        return "Grids are identical."

    description = f"Differences between {grid1_name} and {grid2_name}:\n"
    rows, cols = np.where(diff)
    for r, c in zip(rows, cols):
        description += f"  Pixel at ({r}, {c}): {grid1_name} = {grid1[r, c]}, {grid2_name} = {grid2[r, c]}\n"
    return description

# Example grids (replace with your actual data)
task_id = '6d76b1b6'
train_inputs = [
    np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,1,1,1,2,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,2,2,2,0,0,0],[0,0,0,2,2,2,0,0,0],[0,0,0,2,2,2,0,0,0]]),
    np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,1,1,1,1,1,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,2,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]),
    np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,1,1,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,2,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]),
    np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[2,2,0,0,0,0,0,0,0,0],[2,2,0,0,0,0,0,0,0,0],[2,2,0,0,0,0,0,0,0,0]])
]
train_outputs = [
    np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,1,1,1,2,0,0],[0,0,0,1,1,1,1,0,0],[0,0,0,1,1,1,1,0,0],[0,0,0,1,1,1,1,0,0],[0,0,0,2,2,2,0,0,0],[0,0,0,2,2,2,0,0,0],[0,0,0,2,2,2,0,0,0]]),
    np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,1,1,1,1,1,0],[0,0,0,1,1,1,1,1,0],[0,0,0,1,1,1,1,1,0],[0,0,0,1,1,1,1,1,0],[0,2,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]),
    np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,1,1,0,0,0],[0,0,0,0,0,1,1,0,0,0],[0,0,0,0,0,1,1,0,0,0],[0,0,0,0,0,1,1,0,0,0],[0,0,0,0,0,1,1,0,0,0],[0,0,0,0,0,1,1,0,0,0],[0,0,0,0,0,2,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]),
    np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,1,1,1,0,0,0],[0,0,0,0,1,1,1,0,0,0],[0,0,0,0,1,1,1,0,0,0],[0,0,0,0,1,1,1,0,0,0],[0,0,0,0,1,1,1,0,0,0],[2,2,0,0,0,0,0,0,0,0],[2,2,0,0,0,0,0,0,0,0],[2,2,0,0,0,0,0,0,0,0]])
]

transformed_grids = []
for grid in train_inputs:
  transformed_grids.append(transform(grid))
  

# Generate descriptions and comparisons
for i in range(len(train_inputs)):
    print(describe_grid(train_inputs[i], f"train_input_{i}"))
    print(describe_grid(train_outputs[i], f"train_output_{i}"))
    print(describe_grid(transformed_grids[i], f"transformed_{i}"))
    print(compare_grids(train_outputs[i], transformed_grids[i], f"train_output_{i}",f"transformed_{i}"))

    print("---")