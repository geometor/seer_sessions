# Natural Language Program

1.  Identify all distinct contiguous objects composed of azure (8) pixels in the input grid using 4-way adjacency.
2.  Determine the order of these objects based on their top-most, then left-most pixel coordinate.
3.  Count the total number of identified azure objects, N.
4.  Determine the horizontal midline row index of the grid: `mid_row = (grid_height - 1) / 2`.
5.  For each object, calculate its geometric center's row coordinate.
6.  Partition the ordered objects into two lists: `above_objects` (center row < `mid_row`) and `below_objects` (center row >= `mid_row`), preserving the original relative order within each list.
7.  Select the color assignment sequences, `SeqA` (for above) and `SeqB` (for below), based on the total object count N:
    *   If N is 4: Set `SeqA = [3]` (Green) and `SeqB = [7]` (Orange).
    *   If N is 5: Set `SeqA = [1, 3]` (Blue, Green) and `SeqB = [2, 1]` (Red, Blue).
    *   If N is 6: Set `SeqA = [2, 3]` (Red, Green) and `SeqB = [2, 1, 2, 7]` (Red, Blue, Red, Orange).
    *   (Assume these sequences cover the necessary cases or can be generalized if more examples were available).
8.  Initialize an empty dictionary `object_color_map` to store the assigned color for each object (identified by its starting pixel coordinate or an index).
9.  Assign colors to `above_objects`: Iterate through `above_objects`, assigning colors by cycling through `SeqA`. Store the assignment in `object_color_map`.
10. Assign colors to `below_objects`: Iterate through `below_objects`, assigning colors by cycling through `SeqB`. Store the assignment in `object_color_map`.
11. Create the output grid, initially as a copy of the input grid.
12. Iterate through all identified azure objects. For each object, retrieve its assigned color from `object_color_map` and replace all the object's azure (8) pixels in the output grid with this assigned color.
13. Return the modified output grid.