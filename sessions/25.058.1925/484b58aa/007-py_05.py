import numpy as np
from dataclasses import dataclass

@dataclass
class Grid:
    grid: np.ndarray
    
    @property
    def height(self):
        return self.grid.shape[0]

    @property
    def width(self):
        return self.grid.shape[1]

    @property
    def unique_colors(self):
        return np.unique(self.grid)
    
    def count_objects(self):
        """simplified object counter - contiguous regions of same color"""
        objects = 0
        visited = set()

        def dfs(row, col, color):
            if (
                row < 0
                or row >= self.height
                or col < 0
                or col >= self.width
                or (row, col) in visited
                or self.grid[row, col] != color
            ):
                return

            visited.add((row, col))
            # Explore adjacent cells
            dfs(row + 1, col, color)
            dfs(row - 1, col, color)
            dfs(row, col + 1, color)
            dfs(row, col - 1, color)

        for row in range(self.height):
            for col in range(self.width):
                if (row, col) not in visited:
                    color = self.grid[row, col]
                    dfs(row, col, color)
                    objects += 1
        return objects
    
    def compare(self, other):
        return np.array_equal(self.grid, other.grid)

def report(input_grid, output_grid, predicted_grid):
    input_g = Grid(input_grid)
    output_g = Grid(output_grid)
    predicted_g = Grid(predicted_grid)
    
    print("Input Grid:")
    print(f"  Dimensions: {input_g.height}x{input_g.width}")
    print(f"  Unique Colors: {input_g.unique_colors}")
    print(f"  Object Count: {input_g.count_objects()}")
    print("Output Grid:")
    print(f"  Dimensions: {output_g.height}x{output_g.width}")
    print(f"  Unique Colors: {output_g.unique_colors}")
    print(f"  Object Count: {output_g.count_objects()}")
    print("Predicted Grid:")
    print(f"  Dimensions: {predicted_g.height}x{predicted_g.width}")
    print(f"  Unique Colors: {predicted_g.unique_colors}")
    print(f"  Object Count: {predicted_g.count_objects()}")
    print(f"  Match: {output_g.compare(predicted_g)}")

# Example Usage (replace with actual grids from the task)

# example 0
input_grid0 = np.array([[0,0,0,0,0,0],[0,3,3,3,3,0],[0,3,3,3,3,0],[0,3,3,3,3,0],[0,3,3,3,3,0],[0,0,0,0,0,0]])
output_grid0 = np.array([[3,3,3,3],[3,3,3,3],[3,3,3,3],[3,3,3,3]])
predicted_grid0 = transform(input_grid0)
report(input_grid0, output_grid0, predicted_grid0)

# example 1
input_grid1 = np.array([[8,8,8,8,8,0,0,0],[8,8,8,8,8,0,0,0],[8,8,8,8,8,0,0,0],[8,8,8,8,8,0,0,0],[8,8,8,8,8,0,0,0],[0,0,0,0,0,1,1,0],[0,0,0,0,0,1,1,0],[0,0,0,0,0,0,0,0]])
output_grid1 = np.array([[8,8,8,8,8,0,0,0],[8,8,8,8,8,0,0,0],[8,8,8,8,8,0,0,0],[8,8,8,8,8,0,0,0],[8,8,8,8,8,0,0,0],[0,0,0,0,0,2,2,0],[0,0,0,0,0,2,2,0],[0,0,0,0,0,0,0,0]])
predicted_grid1 = transform(input_grid1)
report(input_grid1, output_grid1, predicted_grid1)

# example 2
input_grid2 = np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,3,3,3,3,3,3,0,0],[0,0,3,3,3,3,3,3,0,0],[0,0,3,3,3,3,3,3,0,0],[0,0,3,3,3,3,3,3,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])
output_grid2 = np.array([[3,3,3,3,3,3],[3,3,3,3,3,3],[3,3,3,3,3,3],[3,3,3,3,3,3]])
predicted_grid2 = transform(input_grid2)
report(input_grid2, output_grid2, predicted_grid2)