import numpy as np

def get_objects(grid):
    """Find contiguous regions of non-blue pixels."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, color, obj_coords):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 1 and not visited[r, c]:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                objects.append({
                    'color': grid[r, c],
                    'coords': obj_coords
                })
    return objects

def is_adjacent(coord1, coord2):
    """Check if two coordinates are adjacent (not diagonally)."""
    return (abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])) == 1

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Get the objects in a list
    objects = get_objects(input_grid)
    
    #create azure object list
    azure_objects = [obj for obj in objects if obj['color'] == 8]

    # Iterate through each non-blue object
    for obj in objects:
        if obj['color'] != 8 and obj['color'] !=1:
            
            #For each coord in the current object
            for obj_coord in obj['coords']:

                # check each coord of azure object
                for azure_obj in azure_objects:
                    for azure_coord in azure_obj['coords']:
                        #if is_adjacent(obj_coord, azure_coord): #Original condition
                        # Check if the azure block is to the right or below
                        if (azure_coord[0] == obj_coord[0] and azure_coord[1] == obj_coord[1] + 1) or \
                           (azure_coord[1] == obj_coord[1] and azure_coord[0] == obj_coord[0] + 1):

                            #fill all the neighboring cells with the current object color
                            neighbors = []
                            r, c = azure_coord
                            
                            # if r > 0: neighbors.append((r-1,c))  # Removed top neighbor
                            # if r < rows - 1: neighbors.append((r+1, c)) # Removed, consider only right or below source
                            # if c > 0 : neighbors.append((r, c-1))  # Removed left neighbor
                            # if c < cols - 1: neighbors.append((r, c+1)) # Removed, consider only right or below source
                            for neighbor in [(r,c)]:
                                if input_grid[neighbor] == 8:
                                     output_grid[neighbor] = obj['color']

    return output_grid
def transform_and_compare(input_grid, expected_output_grid):
    """Transforms the input grid and compares it with the expected output."""

    print("Input Grid:")
    print(input_grid)
    print("Expected Output Grid:")
    print(expected_output_grid)

    transformed_grid = transform(input_grid)
    print("Transformed Grid:")
    print(transformed_grid)

    objects = get_objects(input_grid)
    print("Objects in Input Grid:")
    for obj in objects:
        print(obj)

    correct = np.array_equal(transformed_grid, expected_output_grid)
    print(f"Transformed grid is correct: {correct}")
    print("-" * 20)
    return correct

# Example usage with the training data (replace with actual data)
task_id = '57aa98a4'
import json
with open('data/training/'+task_id+'.json', 'r') as f:
    task = json.load(f)

num_correct = 0
for i, example in enumerate(task['train']):
  print(f"train example {i}")
  if transform_and_compare(np.array(example['input']), np.array(example['output'])):
    num_correct += 1

print(f"Total correct {num_correct} out of {len(task['train'])}")
