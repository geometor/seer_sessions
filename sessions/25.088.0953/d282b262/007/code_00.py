import numpy as np
from collections import deque
from collections import defaultdict

"""
Transformation Rule:
1. Identify all distinct non-background objects (connected groups of non-white pixels using 4-way adjacency). Record the pixels, min column, and max column for each object.
2. Group these objects based on column overlap. Two objects belong to the same group if their horizontal extents (from min column to max column) overlap. This grouping is transitive (if A overlaps B, and B overlaps C, then A, B, C are in the same group).
3. For each group of objects:
    a. Determine the overall maximum column index (`group_max_c`) occupied by any pixel belonging to any object within that group.
    b. Calculate the required horizontal shift for the entire group: `shift = (grid_width - 1) - group_max_c`, where `grid_width` is the width of the input grid.
4. Initialize an output grid with the same dimensions as the input grid, filled with the background color (white, 0).
5. Apply the calculated shift to all pixels of all objects within each group. For each pixel `(row, col)` with `color` belonging to an object in a group, place the `color` at the new coordinates `(row, col + shift)` in the output grid.
6. If no objects are found, return the input grid unchanged.
7. Return the completed output grid.
"""

class DSU:
    """Disjoint Set Union (Union-Find) data structure."""
    def __init__(self, n):
        # Initialize parent array: each element is its own parent initially.
        self.parent = list(range(n))
        # Keep track of additional data associated with each set (e.g., max column).
        self.data = {}

    def find(self, i):
        # Find the representative (root) of the set containing element i with path compression.
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i]) # Path compression
        return self.parent[i]

    def union(self, i, j, merge_data_func):
        # Merge the sets containing elements i and j.
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            # Merge the sets by making one root the parent of the other.
            # Here, we make root_j the parent of root_i.
            self.parent[root_i] = root_j
            # Merge associated data using the provided function.
            # The merged data is stored with the new root (root_j).
            self.data[root_j] = merge_data_func(self.data.get(root_j), self.data.get(root_i))
            # Remove data associated with the old root (root_i) if it exists.
            if root_i in self.data:
                del self.data[root_i]
            return True # Indicates a successful merge
        return False # Indicates i and j were already in the same set

def find_objects(grid_np):
    """
    Finds all distinct connected components (objects) of non-background pixels
    using Breadth-First Search (BFS) and determines their column bounds.

    Args:
        grid_np: A NumPy array representing the input grid.

    Returns:
        A list of objects. Each object is represented as a dictionary containing:
        'pixels': A list of tuples, where each tuple is ((row, col), color).
        'min_c': The minimum column index occupied by any pixel in this object.
        'max_c': The maximum column index occupied by any pixel in this object.
        'id': A unique index for the object.
    """
    height, width = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    objects = []
    object_id_counter = 0

    for r in range(height):
        for c in range(width):
            # If pixel is non-white and not yet visited, start BFS for a new object
            if grid_np[r, c] != 0 and not visited[r, c]:
                current_object_pixels = []
                object_min_c = width
                object_max_c = -1
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    color = grid_np[row, col]

                    # Add pixel to the current object list
                    current_object_pixels.append(((row, col), color))
                    # Update the min/max column for this object
                    object_min_c = min(object_min_c, col)
                    object_max_c = max(object_max_c, col)

                    # Explore neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check if neighbor is within bounds, is non-white, and not visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid_np[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Store the found object's pixels and its column bounds
                if current_object_pixels:
                     objects.append({
                         'pixels': current_object_pixels,
                         'min_c': object_min_c,
                         'max_c': object_max_c,
                         'id': object_id_counter
                     })
                     object_id_counter += 1

    return objects

def group_objects_by_column_overlap(objects):
    """
    Groups objects based on column overlap using Disjoint Set Union (DSU).

    Args:
        objects: A list of object dictionaries, each containing 'min_c', 'max_c', and 'id'.

    Returns:
        A dictionary where keys are group representatives (from DSU) and values are
        dictionaries containing:
        'objects': A list of object dictionaries belonging to the group.
        'group_max_c': The maximum column index across all objects in the group.
    """
    num_objects = len(objects)
    if num_objects == 0:
        return {}

    dsu = DSU(num_objects)

    # Initialize DSU data with the max_c of each individual object.
    for i, obj in enumerate(objects):
        dsu.data[i] = obj['max_c']

    # Define how to merge the max_c data when sets are unioned.
    def merge_max_c(data1, data2):
        # If either data is None (shouldn't happen with proper init, but safe),
        # return the other. Otherwise, return the max.
        if data1 is None: return data2
        if data2 is None: return data1
        return max(data1, data2)

    # Iterate through all pairs of objects to check for overlap and union sets.
    for i in range(num_objects):
        for j in range(i + 1, num_objects):
            obj_i = objects[i]
            obj_j = objects[j]

            # Check for column overlap: max(start1, start2) <= min(end1, end2)
            if max(obj_i['min_c'], obj_j['min_c']) <= min(obj_i['max_c'], obj_j['max_c']):
                # If they overlap, union their sets in the DSU structure.
                # The merge_max_c function ensures the representative stores the
                # overall max_c for the potentially growing group.
                dsu.union(i, j, merge_max_c)

    # Collect the final groups based on the DSU structure.
    groups = defaultdict(lambda: {'objects': [], 'group_max_c': -1})
    for i, obj in enumerate(objects):
        representative = dsu.find(i)
        groups[representative]['objects'].append(obj)
        # The group's max_c is stored in dsu.data associated with the representative.
        # We retrieve it once per group after finding all members.
        if representative in dsu.data:
             groups[representative]['group_max_c'] = dsu.data[representative]
        else:
             # Fallback: recalculate if data wasn't found (shouldn't happen with DSU logic)
             current_max = groups[representative]['group_max_c']
             groups[representative]['group_max_c'] = max(current_max, obj['max_c'])


    return dict(groups)


def transform(input_grid):
    """
    Identifies objects, groups them by column overlap, and shifts each group
    horizontally so that the group's rightmost edge aligns with the grid's right edge.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)

    # Handle empty input grid case
    if input_grid_np.size == 0:
        return []

    height, width = input_grid_np.shape

    # Find all distinct objects in the input grid
    objects = find_objects(input_grid_np)

    # If there are no non-white pixels (no objects), return the original grid
    if not objects:
        return input_grid

    # Group objects based on column overlap
    grouped_objects_data = group_objects_by_column_overlap(objects)

    # Initialize the output grid with the background color (0)
    output_grid_np = np.zeros_like(input_grid_np)
    grid_width = width

    # Process each group of objects
    for group_rep, group_info in grouped_objects_data.items():
        objects_in_group = group_info['objects']
        group_max_c = group_info['group_max_c']

        # Calculate the horizontal shift required for this entire group
        # shift = target_right_edge - current_group_right_edge
        shift = (grid_width - 1) - group_max_c

        # Apply the calculated shift to all pixels of all objects in this group
        for obj in objects_in_group:
            for (r, c), color in obj['pixels']:
                new_c = c + shift
                # Place the pixel in the output grid at its new position
                # Bounds check (though shift calculation should guarantee this)
                if 0 <= r < height and 0 <= new_c < width:
                    output_grid_np[r, new_c] = color

    # Convert the output NumPy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid