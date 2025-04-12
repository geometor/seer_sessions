import numpy as np

def analyze_pixels(grid_list):
    grid = np.array(grid_list)
    unique_colors = np.unique(grid)
    analysis = {}

    for color in unique_colors:
        if color == 0 or color == 5: # Skip background and gray
            continue

        coords = np.argwhere(grid == color)

        if coords.shape[0] == 0:
            continue

        min_r = np.min(coords[:, 0])
        min_c = np.min(coords[:, 1])
        max_r = np.max(coords[:, 0])
        max_c = np.max(coords[:, 1])

        height = max_r - min_r + 1
        width = max_c - min_c + 1

        coord_set = set(tuple(c) for c in coords)

        is_3x3_bbox = (height == 3 and width == 3)

        is_2x2_diag = False
        # Check for the specific 2x2 diagonal pattern
        if height == 2 and width == 2 and coords.shape[0] == 2:
             # Check if the only two pixels are top-left and bottom-right of bbox
             if (min_r, min_c) in coord_set and (max_r, max_c) in coord_set:
                 is_2x2_diag = True

        analysis[int(color)] = {
            'coords_count': len(coord_set),
            'bbox': (int(min_r), int(min_c), int(max_r), int(max_c)),
            'bbox_size': (int(height), int(width)),
            'is_3x3_bbox': is_3x3_bbox,
            'is_2x2_diagonal_pattern': is_2x2_diag
        }

    return analysis

train_1_input = [
    [0, 0, 0, 0, 0, 0, 0, 5, 5, 5],
    [0, 0, 0, 4, 0, 0, 0, 5, 5, 5],
    [0, 0, 0, 0, 0, 0, 0, 5, 5, 5],
    [0, 0, 0, 4, 4, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 6, 6, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 6, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

train_2_input = [
    [0, 0, 0, 0, 0, 0, 0, 5, 0, 5],
    [0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
    [0, 7, 0, 0, 0, 0, 0, 5, 5, 5],
    [0, 0, 7, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 6, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

print("Train 1 Analysis:")
print(analyze_pixels(train_1_input))

print("\nTrain 2 Analysis:")
print(analyze_pixels(train_2_input))