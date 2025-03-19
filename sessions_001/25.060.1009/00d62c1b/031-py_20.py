import numpy as np

def get_neighbors(grid, row, col):
    """Gets the neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append(grid[row - 1, col])  # Up
    if row < rows - 1:
        neighbors.append(grid[row + 1, col])  # Down
    if col > 0:
        neighbors.append(grid[row, col - 1])  # Left
    if col < cols - 1:
        neighbors.append(grid[row, col + 1])  # Right
    return neighbors

def has_white_neighbor(grid, row, col):
    """Checks if a cell has any white neighbors."""
    neighbors = get_neighbors(grid, row, col)
    return any(neighbor == 0 for neighbor in neighbors)

# Example Data (replace with actual data from the task)
task_id = '6f8cd79b'
train_inputs = [
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 3, 3, 3, 3, 0],
              [0, 3, 3, 3, 3, 0],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0],
              [0, 3, 3, 3, 0],
              [0, 3, 3, 3, 0],
              [0, 3, 3, 3, 0],
              [0, 0, 0, 0, 0]]),
    np.array([[5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 3, 3, 3, 0, 0, 0],
              [0, 0, 0, 3, 3, 3, 0, 0, 0],
              [0, 0, 0, 3, 3, 3, 0, 0, 0],
              [0, 0, 0, 3, 3, 3, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]])
]
train_outputs = [
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 3, 3, 3, 3, 0],
              [0, 3, 3, 3, 3, 0],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0],
              [0, 3, 3, 3, 0],
              [0, 3, 3, 3, 0],
              [0, 3, 3, 3, 0],
              [0, 0, 0, 0, 0]]),
    np.array([[5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 3, 3, 3, 0, 0, 0],
              [0, 0, 0, 3, 4, 3, 0, 0, 0],
              [0, 0, 0, 3, 3, 3, 0, 0, 0],
              [0, 0, 0, 3, 3, 3, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]])
]

# Example 1:
# Examine where green is NOT surrounded by green and has no white neighbors - should not turn yellow.
input_grid = train_inputs[0]
output_grid = train_outputs[0]

print(f"Example 1 Analysis:")
rows, cols = input_grid.shape
for r in range(rows):
    for c in range(cols):
        if input_grid[r,c] == 3:
          neighbors = get_neighbors(input_grid, r, c)
          white_neighbor = has_white_neighbor(input_grid, r, c)
          all_green = all(neighbor == 3 for neighbor in neighbors)
          print(f'Pixel at: ({r},{c}) - Neighbors:{neighbors}, White Neighbor: {white_neighbor}, All Green Neighbors: {all_green}, Output: {output_grid[r,c]}')


# Example 2:
# Examine where green is NOT surrounded by green and has no white neighbors - should not turn yellow.
input_grid = train_inputs[1]
output_grid = train_outputs[1]

print(f"\nExample 2 Analysis:")
rows, cols = input_grid.shape
for r in range(rows):
    for c in range(cols):
        if input_grid[r,c] == 3:
          neighbors = get_neighbors(input_grid, r, c)
          white_neighbor = has_white_neighbor(input_grid, r, c)
          all_green = all(neighbor == 3 for neighbor in neighbors)
          print(f'Pixel at: ({r},{c}) - Neighbors:{neighbors}, White Neighbor: {white_neighbor}, All Green Neighbors: {all_green}, Output: {output_grid[r,c]}')

# Example 3:
input_grid = train_inputs[2]
output_grid = train_outputs[2]

print(f"\nExample 3 Analysis:")
rows, cols = input_grid.shape
for r in range(rows):
    for c in range(cols):
        if input_grid[r,c] == 3:
          neighbors = get_neighbors(input_grid, r, c)
          white_neighbor = has_white_neighbor(input_grid, r, c)
          all_green = all(neighbor == 3 for neighbor in neighbors)
          print(f'Pixel at: ({r},{c}) - Neighbors:{neighbors}, White Neighbor: {white_neighbor}, All Green Neighbors: {all_green}, Output: {output_grid[r,c]}')

# Example 4:
input_grid = train_inputs[3]
output_grid = train_outputs[3]

print(f"\nExample 4 Analysis:")
rows, cols = input_grid.shape
for r in range(rows):
    for c in range(cols):
        if input_grid[r,c] == 3:
          neighbors = get_neighbors(input_grid, r, c)
          white_neighbor = has_white_neighbor(input_grid, r, c)
          all_green = all(neighbor == 3 for neighbor in neighbors)
          print(f'Pixel at: ({r},{c}) - Neighbors:{neighbors}, White Neighbor: {white_neighbor}, All Green Neighbors: {all_green}, Output: {output_grid[r,c]}')