import numpy as np

def show_grid_diff(grid1, grid2):
    """
    Print an overlay that shows the differences between two grids.
    - Cells that are the same color will be printed.
    - Cells with color changes will use the following legend
    0: "W", 1: "B", 2: "R", 3: "G", 4: "Y", 5: "X", 6: "M", 7: "O", 8: "A", 9: "N"
    """
    rows1, cols1 = grid1.shape
    rows2, cols2 = grid2.shape

    if rows1 != rows2 or cols1 != cols2:
        print("Grids are not the same size. Cannot compare.")
        return

    print("Grid Overlay (changed values labeled by new value):")
    legend = {
        0: "W", 1: "B", 2: "R", 3: "G", 4: "Y",
        5: "X", 6: "M", 7: "O", 8: "A", 9: "N"
    }

    for i in range(rows1):
        for j in range(cols1):
            if grid1[i, j] == grid2[i, j]:
                print(f"{grid1[i, j]}", end=" ")  # print number if colors are equal
            else:
                print(f"{legend[grid2[i, j]]}", end=" ") # print color code if change
        print()  # Newline after each row


# Example data (replace with actual data from the task)
example_data = [
    (np.array([[0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 4, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0],
               [0, 0, 0, 4, 0, 0],
               [0, 0, 0, 4, 0, 0],
               [0, 0, 0, 4, 0, 0],
               [0, 0, 0, 4, 0, 0],
               [0, 0, 0, 4, 0, 0],
               [0, 0, 0, 0, 0, 0]])),

    (np.array([[0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 4, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 4, 0, 0, 0],
               [0, 0, 0, 4, 0, 0, 0],
               [0, 0, 0, 4, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 4, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 4, 0, 0, 0, 0, 0, 0, 0],
               [0, 4, 0, 0, 0, 0, 0, 0, 0],
               [0, 4, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]))
]

for i, (input_grid, output_grid) in enumerate(example_data):
    print(f"Example {i+1}:")
    show_grid_diff(input_grid, output_grid)
    print("-" * 20)