# 2013d3e2 • 001 • all training • investigate_dreamer

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0
0 0 0 6 8 8 6 0 0 0
0 0 7 8 4 4 8 7 0 0
0 0 7 8 4 4 8 7 0 0
0 0 0 6 8 8 6 0 0 0
0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7A3E78F9E530>

**output:**
```
0 0 7
0 6 8
7 8 4
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7A3E78FC5A90>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 1 0 0 0
0 0 3 6 5 3 0 0 0 0
0 0 5 2 2 6 0 0 0 0
0 0 6 2 2 5 0 0 0 0
0 0 3 5 6 3 0 0 0 0
0 1 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7A3E78FC5C70>

**output:**
```
1 0 0
0 3 6
0 5 2
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7A3E78FC5BD0>
<PIL.Image.Image image mode=RGB size=1340x882 at 0x7A3E78FC6170>**INSTRUCTIONS**

above is an example pair for a task

this is your opportunity to perceive the underlying logic that transforms the
input into the output

respond with the following deliverables:

- your perception of the elements of the task
- a YAML block documenting facts - Focus on identifying objects, their properties, actions performed on them, and the relationships between them
- a natural language program - Be as clear and concise as possible, providing a complete description of the transformation rule.


your responses should be considered as information in a report - not a conversation
