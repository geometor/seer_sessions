Warning: Response generation stopped. Finish Reason: FINISH_REASON_UNSPECIFIED (0)
Partial text available:
---
**General Assessment and Strategy:**

The initial code correctly identifies the core concept of filtering based on object enclosure but fails across all examples. The consistent production of empty grids indicates that the `_is_enclosed` condition is never met for any object. Reviewing the examples and the logic, the crucial missing condition is that the enclosing object's color must be *different* from the enclosed object's color. The current `_is_enclosed` function only checks that all neighbors are non-zero and have the *same* color, but it doesn't compare this neighbor color to the color of the object under consideration.

The strategy is to:
1.  Modify the `_is_enclosed` function or the calling logic in `transform` to include a check comparing the object's color with the detected neighbor color.
2.  Verify this updated logic against the provided examples.
3.  Update the YAML facts and natural language program to accurately reflect this refined enclosure rule.

**Metrics Gathering:**

Let's analyze Train Example 1, focusing on the object with color 4, which *should* be kept.


``` python
import numpy as np
from collections import deque

# Function to find neighbors (copied from previous attempt)
def _find_neighbors(grid_shape, object_coords):
    rows, cols = grid_shape
    neighbors = set()
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  ( 0, -1),          ( 0, 1),
                  ( 1, -1), ( 1, 0), ( 1, 1)]
    for r, c in object_coords:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_coord = (nr, nc)
                if neighbor_coord not in object_coords:
                    neighbors.add(neighbor_coord)
    return neighbors

# Input grid for Train Example 1
input_grid_list = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,2,2,2,2,2,2,2,2,0,3,3,3,3,0,0,0],
    [0,0,2,0,0,0,0,0,0,2,0,3,0,0,3,0,0,0],
    [0,0,2,0,4,4,4,0,0,2,0,3,0,0,3,0,0,0],
    [0,0,2,0,4,0,4,0,0,2,0,3,3,3,3,0,0,0],
    [0,0,2,0,4,4,4,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,0,0,0,2,0,0,6,6,6,0,0,0],
    [0,0,2,2,2,2,2,2,2,2,0,0,6,0,6,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
grid = np.array(input_grid_list)
rows, cols = grid.shape
visited = np.zeros_like(grid, dtype=bool)

# Find the object with color 4
object_color_target = 4
object_coords_target = set()
start_coord = None
for r in range(rows):
    for c in range(cols):
        if grid[r,c] == object_color_target:
            start_coord = (r,c)
            break
    if start_coord:
        break

if start_coord:
    q = deque([start_coord])
    visited[start_coord] = True
    while q:
        curr_r, curr_c = q.popleft()
        object_coords_target.add((curr_r, curr_c))
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = curr_r + dr, curr_c + dc
                if (0 <= nr < rows and 0 <= nc < cols and
                        not visited[nr, nc] and
                        grid[nr, nc] == object_color_target):
                    visited[nr, nc] = True
                    q.append((nr, nc))

# Find neighbors of the target object
neighbor_coords_target = _find_neighbors(grid.shape, object_coords_target)

# Get the colors of the neighbors
neighbor_colors = {grid[r, c] for r, c in neighbor_coords_target}

print(f"Target Object Color: {object_color_target}")
print(f"Target Object Coords Count: {len(object_coords_target)}")
# print(f"Target Object Coords: {sorted(list(object_coords_target))}")
print(f"Neighbor Coords Count: {len(neighbor_coords_target)}")
# print(f"Neighbor Coords: {sorted(list(neighbor_coords_target))}")
print(f"Unique Neighbor Colors: {neighbor_colors}")

# Check enclosure conditions manually based on findings
is_enclosed = False
if neighbor_coords_target: # Check if neighbors exist
    first_neighbor_val = grid[next(iter(neighbor_coords_target))] # Get color of one neighbor
    all_neighbors_same_color = all(grid[r,c] == first_neighbor_val for r,c in neighbor_coords_target)
    no_background_neighbors = all(grid[r,c] != 0 for r,c in neighbor_coords_target)
    # *** The NEW condition check ***
    enclosing_color_different = (first_neighbor_val != object_color_target)

    if no_background_neighbors and all_neighbors_same_color and enclosing_color_different:
         is_enclosed = True

print(f"Is Enclosed (Manual Check with New Rule): {is_enclosed}")
```
```
Target Object Color: 4
Target Object Coords Count: 8
Neighbor Coords Count: 17
Unique Neighbor Colors: {np.int64(0)}
Is Enclosed (Manual Check with New Rule): False

```
**Analysis of Metrics:**

The analysis for object 4 in Train Example 1 reveals:
*   Object Color: 4
*   Object Size: 8 pixels
*   Neighbor Count: 17 pixels
*   **Unique Neighbor Colors: {0}** - This is incorrect based on visual inspection. The neighbors should all be color 2.

Let's re-run the neighbor finding, printing the actual coordinates and values.


``` python
import numpy as np
from collections import deque

# Function to find neighbors (copied from previous attempt)
def _find_neighbors(grid_shape, object_coords):
    rows, cols = grid_shape
    neighbors = set()
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  ( 0, -1),          ( 0, 1),
                  ( 1, -1), ( 1, 0), ( 1, 1)]
    for r, c in object_coords:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_coord = (nr, nc)
                if neighbor_coord not in object_coords:
                    neighbors.add(neighbor_coord)
    return neighbors

# Input grid for Train Example 1
input_grid_list = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,2,2,2,2,2,2,2,2,0,3,3,3,3,0,0,0],
    [0,0,2,0,0,0,0,0,0,2,0,3,0,0,3,0,0,0],
    [0,0,2,0,4,4,4,0,0,2,0,3,0,0,3,0,0,0],
    [0,0,2,0,4,0,4,0,0,2,0,3,3,3,3,0,0,0],
    [0,0,2,0,4,4,4,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,0,0,0,2,0,0,6,6,6,0,0,0],
    [0,0,2,2,2,2,2,2,2,2,0,0,6,0,6,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
grid = np.array(input_grid_list)
rows, cols = grid.shape
visited = np.zeros_like(grid, dtype=bool)

# Find the object with color 4
object_color_target = 4
object_coords_target = set()
start_coord = None
# Manually identify a starting coordinate for object 4
start_coord = (4, 4) # A known cell with value 4

if start_coord:
    q = deque([start_coord])
    # Make sure visited is clear for this object search
    visited_obj_search = np.zeros_like(grid, dtype=bool)
    visited_obj_search[start_coord] = True
    while q:
        curr_r, curr_c = q.popleft()
        object_coords_target.add((curr_r, curr_c))
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = curr_r + dr, curr_c + dc
                if (0 <= nr < rows and 0 <= nc < cols and
                        not visited_obj_search[nr, nc] and # Use separate visited for this search
                        grid[nr, nc] == object_color_target):
                    visited_obj_search[nr, nc] = True
                    q.append((nr, nc))

# Find neighbors of the target object
neighbor_coords_target = _find_neighbors(grid.shape, object_coords_target)

# Get the coordinates and colors of the neighbors
neighbor_details = {(r, c): grid[r, c] for r, c in neighbor_coords_target}
unique_neighbor_colors = set(neighbor_details.values())

print(f"Target Object Color: {object_color_target}")
print(f"Target Object Coords Count: {len(object_coords_target)}")
print(f"Target Object Coords: {sorted(list(object_coords_target))}")
print(f"Neighbor Coords Count: {len(neighbor_coords_target)}")
print(f"Neighbor Coords and Colors: {sorted(neighbor_details.items())}")
print(f"Unique Neighbor Colors: {unique_neighbor_colors}")

# Check enclosure conditions manually based on findings
is_enclosed = False
enclosing_color = -1
if neighbor_coords_target: # Check if neighbors exist
    first_neighbor_val = grid[next(iter(neighbor_coords_target))]
    all_neighbors_same_color = all(grid[r,c] == first_neighbor_val for r,c in neighbor_coords_target)
    no_background_neighbors = all(grid[r,c] != 0 for r,c in neighbor_coords_target)
    enclosing_color_different = (first_neighbor_val != object_color_target)

    if no_background_neighbors and all_neighbors_same_color and enclosing_color_different:
         is_enclosed = True
         enclosing_color = first_neighbor_val # Store the color

print(f"Is Enclosed (Manual Check with New Rule): {is_enclosed}")
print(f"Enclosing Color (if enclosed): {enclosing_color}")
```
```
Target Object Color: 4
Target Object Coords Count: 8
Target Object Coords: [(4, 4), (4, 5), (4, 6), (5, 4), (5, 6), (6, 4), (6, 5), (6, 6)]
Neighbor Coords Count: 17
Neighbor Coords and Colors: [((3, 3), np.int64(0)), ((3, 4), np.int64(0)), ((3, 5), np.int64(0)), ((3, 6), np.int64(0)), ((3, 7), np.int64(0)), ((4, 3), np.int64(0)), ((4, 7), np.int64(0)), ((5, 3), np.int64(0)), ((5, 5), np.int64(0)), ((5, 7), np.int64(0)), ((6, 3), np.int64(0)), ((6, 7), np.int64(0)), ((7, 3), np.int64(0)), ((7, 4), np.int64(0)), ((7, 5), np.int64(0)), ((7, 6), np.int64(0)), ((7, 7), np.int64(0))]
Unique Neighbor Colors: {np.int64(0)}
Is Enclosed (Manual Check with New Rule): False
Enclosing Color (if enclosed): -1

```
**Revised Analysis of Metrics:**

There was an error in my manual analysis or the code execution setup previously. The second code execution correctly identifies the neighbours of the object '4'.
*   Object Color: 4
*   Object Coords: {(4, 4), (4, 5), (4, 6), (5, 4), (5, 6), (6, 4), (6, 5), (6, 6)}
*   Neighbor Coords Count: 17
*   **Neighbor Colors: All are 0.** (e.g., (3,3)=0, (3,4)=0, ..., (7,7)=0)

This contradicts the visual expectation that object 4 is enclosed by object 2. Let's re-examine the input grid visually.


```
...
0 0 2 2 2 2 2 2 2 2 ...  <- Row 2
0 0 2 0 0 0 0 0 0 2 ...  <- Row 3
0 0 2 0 4 4 4 0 0 2 ...  <- Row 4 (Object 4 starts)
0 0 2 0 4 0 4 0 0 2 ...  <- Row 5
0 0 2 0 4 4 4 0 0 2 ...  <- Row 6 (Object 4 ends)
0 0 2 0 0 0 0 0 0 2 ...  <- Row 7
...
```

The neighbors of the '4' at (4, 4) include (3, 3) which is 2, (3, 4) which is 0, (3, 5) which is 0, (4, 3) which is 0, (5, 3) which is 0, (5, 5) which is 0. Wait, the code output says the neighbor colors are *all* 0. This implies my `_find_neighbors` or the BFS object identification might be flawed.

Let's rethink the process:
1.  Find *all* cells belonging to an object (BFS).
2.  Find *all* unique adjacent cells to those object cells.
3.  Exclude cells belonging to the object itself.
4.  Check the values of the remaining neighbor cells.

Re-checking the `_find_neighbors` logic: It iterates through object cells, finds neighbors, checks bounds, and adds if *not* part of the object. This seems correct.
Re-checking the BFS: It starts, adds to queue, adds to object coords, explores neighbors, adds valid ones (boundary, same color, not visited) to queue. This also seems standard.

Could the `visited` array in the main loop be causing issues? If a cell belonging to the *enclosing* object (like color 2) is marked `visited` before we process the *enclosed* object (color 4), could that interfere? No, the BFS uses its own `visited_obj_search` (or should) and the main loop's `visited` just prevents re-starting BFS for the same object.

Let's re-run the metric gathering but be explicit about clearing the `visited` array for the specific object search.

Okay, the second run of the code execution *did* correctly identify the object coordinates. The neighbor calculation was the part that produced the unexpected result ({0}). Let's look closely at the neighbor coordinates found: `[(3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3), (4, 7), (5, 3), (5, 5), (5, 7), (6, 3), (6, 7), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]`.
And their values in the grid:
(3,3)=2, (3,4)=0, (3,5)=0, (3,6)=0, (3,7)=0, (4,3)=0, (4,7)=0, (5,3)=0, (5,5)=0, (5,7)=0, (6,3)=0, (6,7)=0, (7,3)=0, (7,4)=0, (7,5)=0, (7,6)=0, (7,7)=0.

Aha! The neighbor set includes cells with value 0 *and* value 2. My previous code's `_is_enclosed` function correctly returns `False` because `val == 0` is true for many neighbors. The visual perception of enclosure was perhaps misleading, or the definition is stricter.

Let's reconsider the definition: "An object 'A' is enclosed if every cell adjacent to 'A' (but not part of 'A') belongs to exactly one other single object 'B'." This implies *no* adjacent cell can be the background (0).

Looking at Train 1's Object 4 again:
*   Cell (4,4) has neighbors (3,3)=2, (3,4)=0, (3,5)=0, (4,3)=0, (5,3)=0, (5,4)=4, (5,5)=0.
*   Since neighbor (3,4) is 0, object 4 is *not* enclosed by this definition.

But the expected output *keeps* object 4. This means my definition of enclosure derived from the initial dreamer phase must be wrong.

**New Hypothesis:** An object is kept if it is "internal" to another object, meaning it does *not* touch the background (0) *or* any *other* color besides its immediate container.

Let's refine the enclosure check:
1.  Find all neighbors.
2.  Check if *any* neighbor is background (0). If yes, the object is *not* enclosed.
3.  If no background neighbors, find the unique *non-zero* colors among the neighbors.
4.  If there is exactly one unique non-zero neighbor color, *and* this color is different from the object's own color, then the object is enclosed.

Let's re-evaluate Train 1, Object 4 with this new rule:
1. Neighbors found: `{(3,3)=2, (3,4)=0, (3,5)=0, ...}`
2. Does it contain 0? Yes. -> Not enclosed by the *new* rule.

This *still* doesn't match the expected output. The rule must be different.

**Alternative Hypothesis:** Maybe the "enclosing" object doesn't need to touch *every* cell of the enclosed object? What if the rule is simply: An object is kept if *none* of its cells are adjacent to the background (0)?

Let's test this simpler hypothesis:
*   **Train 1, Object 4:**
    *   Neighbors include 0s. Is any cell of object 4 adjacent to 0? Yes, (4,4) is adjacent to (3,4)=0, (4,3)=0, etc. So, by this rule, object 4 is *removed*. Still doesn't match.
*   **Train 1, Object 2:**
    *   Is any cell of object 2 adjacent to 0? Yes, (2,10)=0, (3,2) is adjacent to (3,1)=0, etc. Removed. Matches output.
*   **Train 1, Object 3:**
    *   Is any cell of object 3 adjacent to 0? Yes, (2,10)=0, (3,11) is adjacent to (3,10)=0, etc. Removed. Matches output.
*   **Train 1, Object 6:**
    *   Is any cell of object 6 adjacent to 0? Yes, (9,11)=0, (8,11)=0 etc. Removed. Matches output.

This simple rule ("remove if adjacent to background") works for objects 2, 3, and 6 in Train 1, but incorrectly removes object 4.

What is special about object 4? It's inside object 2, but object 2 has "holes" (0s) inside it. Maybe the rule is about being enclosed by a *solid* object?

**Hypothesis 3 (Refined Enclosure):** An object A is kept if:
1.  It is not adjacent to the background (0).
2.  All its non-zero neighbors belong to exactly one other color B (where B != A).

Let's re-test this on Train 1, Object 4:
1. Is it adjacent to 0? Yes (e.g., (4,4) adjacent to (3,4)=0). Condition 1 fails. Object 4 is removed. Still doesn't match.

This is puzzling. The visual pattern strongly suggests object 4 is kept because it's "inside" 2. The failure of simple adjacency rules suggests something more complex or a misinterpretation of the examples.

Could it be related to the "frame" or "border" cells of an object?
An object is kept if its "border cells" (cells adjacent to anything *not* of the object's color) are *all* adjacent to cells of *only one* other non-zero color.

Let's try this:
*   **Train 1, Object 4:**
    *   Cells: {(4, 4), (4, 5), (4, 6), (5, 4), (5, 6), (6, 4), (6, 5), (6, 6)}
    *   Neighbors: {(3,3)=2, (3,4)=0, (3,5)=0, (3,6)=0, (3,7)=0, (4,3)=0, (4,7)=0, (5,3)=0, (5,5)=0, (5,7)=0, (6,3)=0, (6,7)=0, (7,3)=0, (7,4)=0, (7,5)=0, (7,6)=0, (7,7)=0}
    *   What are the colors of the neighbors? {0, 2}.
    *   Are *all* neighbors of a single non-zero color different from 4? No, because there are 0s and 2s. Fails.

Let's reconsider **Train 3**:
Input: Object 8 is enclosed by 7. Object 3 is enclosed by 8. Another 8 is enclosed by 3.
Output: Keeps outer 8, inner 3, bottom-right 8.

*   Outer Object 8: Let's check its neighbors. They should all be color 7 (or 3 for the inner part).
*   Inner Object 3: Neighbors should all be color 8.
*   Bottom-right Object 8: Neighbors should all be color 3.

Perhaps the definition of "neighbor" or "adjacent" is wrong? If we only consider 4-way adjacency (N, S, E, W)?

Let's try the "Enclosed by single *different* non-zero color, no background contact" rule again, but with 4-way adjacency.


``` python
import numpy as np
from collections import deque

# Function to find neighbors (4-way adjacency)
def _find_neighbors_4way(grid_shape, object_coords):
    rows, cols = grid_shape
    neighbors = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # N, S, W, E
    for r, c in object_coords:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_coord = (nr, nc)
                if neighbor_coord not in object_coords:
                    neighbors.add(neighbor_coord)
    return neighbors

# Input grid for Train Example 1
input_grid_list = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,2,2,2,2,2,2,2,2,0,3,3,3,3,0,0,0],
    [0,0,2,0,0,0,0,0,0,2,0,3,0,0,3,0,0,0],
    [0,0,2,0,4,4,4,0,0,2,0,3,0,0,3,0,0,0],
    [0,0,2,0,4,0,4,0,0,2,0,3,3,3,3,0,0,0],
    [0,0,2,0,4,4,4,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,0,0,0,2,0,0,6,6,6,0,0,0],
    [0,0,2,2,2,2,2,2,2,2,0,0,6,0,6,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
grid = np.array(input_grid_list)
rows, cols = grid.shape
visited = np.zeros_like(grid, dtype=bool)

# Find the object with color 4
object_color_target = 4
object_coords_target = set()
start_coord = (4, 4) # A known cell with value 4

q = deque([start_coord])
visited_obj_search = np.zeros_like(grid, dtype=bool)
visited_obj_search[start_coord] = True
while q:
    curr_r, curr_c = q.popleft()
    object_coords_target.add((curr_r, curr_c))
    # Use 8-way for object finding itself
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue
            nr, nc = curr_r + dr, curr_c + dc
            if (0 <= nr < rows and 0 <= nc < cols and
                    not visited_obj_search[nr, nc] and
                    grid[nr, nc] == object_color_target):
                visited_obj_search[nr, nc] = True
                q.append((nr, nc))

# Find neighbors using 4-way adjacency
neighbor_coords_target = _find_neighbors_4way(grid.shape, object_coords_target)
neighbor_details = {(r, c): grid[r, c] for r, c in neighbor_coords_target}
unique_neighbor_colors = set(neighbor_details.values())

print(f"Target Object Color: {object_color_target}")
print(f"Target Object Coords: {sorted(list(object_coords_target))}")
print(f"4-Way Neighbor Coords and Colors: {sorted(neighbor_details.items())}")
print(f"Unique 4-Way Neighbor Colors: {unique_neighbor_colors}")

# Check enclosure: No background neighbors AND exactly one unique non-zero neighbor color different from object color
is_enclosed = False
enclosing_color = -1
if neighbor_coords_target:
    has_background_neighbor = any(grid[r,c] == 0 for r,c in neighbor_coords_target)
    if not has_background_neighbor:
        non_zero_neighbor_colors = {grid[r,c] for r,c in neighbor_coords_target if grid[r,c] != 0}
        if len(non_zero_neighbor_colors) == 1:
            the_neighbor_color = next(iter(non_zero_neighbor_colors))
            if the_neighbor_color != object_color_target:
                is_enclosed = True
                enclosing_color = the_neighbor_color

print(f"Is Enclosed (4-Way Neighbors, No Background, Single Different Color): {is_enclosed}")
print(f"Enclosing Color (if enclosed): {enclosing_color}")
```
```
Target Object Color: 4
Target Object Coords: [(4, 4), (4, 5), (4, 6), (5, 4), (5, 6), (6, 4), (6, 5), (6, 6)]
4-Way Neighbor Coords and Colors: [((3, 4), np.int64(0)), ((3, 5), np.int64(0)), ((3, 6), np.int64(0)), ((4, 3), np.int64(0)), ((4, 7), np.int64(0)), ((5, 3), np.int64(0)), ((5, 5), np.int64(0)), ((5, 7), np.int64(0)), ((6, 3), np.int64(0)), ((6, 7), np.int64(0)), ((7, 4), np.int64(0)), ((7, 5), np.int64(0)), ((7, 6), np.int64(0))]
Unique 4-Way Neighbor Colors: {np.int64(0)}
Is Enclosed (4-Way Neighbors, No Background, Single Different Color): False
Enclosing Color (if enclosed): -1

```
Still failing. The 4-way neighbors for Object 4 are *all* 0. This object definitely touches background cells according to the grid data.

Let's reconsider the **definition of the object itself**. The BFS uses 8-way connectivity. What if the objects are defined by 4-way connectivity?

Let's re-run the BFS for object identification using 4-way, then check neighbors (using 8-way as per original assumption, and the latest rule: no background neighbors, single different non-zero neighbor color).


``` python
import numpy as np
from collections import deque

# Function to find neighbors (8-way adjacency)
def _find_neighbors_8way(grid_shape, object_coords):
    rows, cols = grid_shape
    neighbors = set()
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for r, c in object_coords:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_coord = (nr, nc)
                if neighbor_coord not in object_coords:
                    neighbors.add(neighbor_coord)
    return neighbors

# Input grid for Train Example 1
input_grid_list = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,2,2,2,2,2,2,2,2,0,3,3,3,3,0,0,0],
    [0,0,2,0,0,0,0,0,0,2,0,3,0,0,3,0,0,0],
    [0,0,2,0,4,4,4,0,0,2,0,3,0,0,3,0,0,0],
    [0,0,2,0,4,0,4,0,0,2,0,3,3,3,3,0,0,0],
    [0,0,2,0,4,4,4,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,0,0,0,2,0,0,6,6,6,0,0,0],
    [0,0,2,2,2,2,2,2,2,2,0,0,6,0,6,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
grid = np.array(input_grid_list)
rows, cols = grid.shape

# Find the object with color 4 using 4-way BFS
object_color_target = 4
object_coords_target = set()
start_coord = (4, 4) # A known cell with value 4

q = deque([start_coord])
visited_obj_search = np.zeros_like(grid, dtype=bool)
visited_obj_search[start_coord] = True
while q:
    curr_r, curr_c = q.popleft()
    object_coords_target.add((curr_r, curr_c))
    # Use 4-way for object finding
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # N, S, W, E
        nr, nc = curr_r + dr, curr_c + dc
        if (0 <= nr < rows and 0 <= nc < cols and
                not visited_obj_search[nr, nc] and
                grid[nr, nc] == object_color_target):
            visited_obj_search[nr, nc] = True
            q.append((nr, nc))

# Find neighbors using 8-way adjacency
neighbor_coords_target = _find_neighbors_8way(grid.shape, object_coords_target)
neighbor_details = {(r, c): grid[r, c] for r, c in neighbor_coords_target}
unique_neighbor_colors = set(neighbor_details.values())

print(f"Target Object Color: {object_color_target}")
print(f"4-Way Object Coords: {sorted(list(object_coords_target))}") # Note: Object coords might change
print(f"8-Way Neighbor Coords and Colors: {sorted(neighbor_details.items())}")
print(f"Unique 8-Way Neighbor Colors: {unique_neighbor_colors}")

# Check enclosure: No background neighbors AND exactly one unique non-zero neighbor color different from object color
is_enclosed = False
enclosing_color = -1
if neighbor_coords_target:
    has_background_neighbor = any(grid[r,c] == 0 for r,c in neighbor_coords_target)
    if not has_background_neighbor:
        non_zero_neighbor_colors = {grid[r,c] for r,c in neighbor_coords_target if grid[r,c] != 0}
        if len(non_zero_neighbor_colors) == 1:
            the_neighbor_color = next(iter(non_zero_neighbor_colors))
            if the_neighbor_color != object_color_target:
                is_enclosed = True
                enclosing_color = the_neighbor_color

print(f"Is Enclosed (4-Way Object ID, 8-Way Neighbors, No Background, Single Different Color): {is_enclosed}")
print(f"Enclosing Color (if enclosed): {enclosing_color}")
```
```
Target Object Color: 4
4-Way Object Coords: [(4, 4), (4, 5), (4, 6), (5, 4), (5, 6), (6, 4), (6, 5), (6, 6)]
8-Way Neighbor Coords and Colors: [((3, 3), np.int64(0)), ((3, 4), np.int64(0)), ((3, 5), np.int64(0)), ((3, 6), np.int64(0)), ((3, 7), np.int64(0)), ((4, 3), np.int64(0)), ((4, 7), np.int64(0)), ((5, 3), np.int64(0)), ((5, 5), np.int64(0)), ((5, 7), np.int64(0)), ((6, 3), np.int64(0)), ((6, 7), np.int64(0)), ((7, 3), np.int64(0)), ((7, 4), np.int64(0)), ((7, 5), np.int64(0)), ((7, 6), np.int64(0)), ((7, 7), np.int64(0))]
Unique 8-Way Neighbor Colors: {np.int64(0)}
Is Enclosed (4-Way Object ID, 8-Way Neighbors, No Background, Single Different Color): False
Enclosing Color (if enclosed): -1

```
---
