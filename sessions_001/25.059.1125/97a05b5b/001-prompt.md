# 97a05b5b • 001 • all training • investigate_dreamer

---


## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 0 2 2 2 2 2 0 2 0 0 1 2 1 0 0 0
0 0 2 0 0 2 2 2 2 0 2 0 0 2 2 2 0 0 0
0 0 2 2 2 2 2 2 2 0 2 0 0 1 2 1 0 0 0
0 0 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 0 2 2 2 2 0 0 0 3 3 3 0 0
0 0 2 2 2 0 0 0 2 2 2 0 0 0 2 2 2 0 0
0 0 2 2 2 2 0 2 2 2 2 0 0 0 3 3 3 0 0
0 0 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 0 0 2 2 2 0 2 2 0 0 0 0 0 0 0 0
0 0 2 2 0 2 2 2 0 2 2 0 0 0 0 0 0 0 0
0 0 2 0 0 2 2 0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 2 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 8 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 4 4 4 0 0 5 5 2 0 0 0 0 0 0 0 0
0 0 0 4 2 4 0 0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 2 2 4 0 0 5 5 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1216x1536 at 0x7F4C1B75CD50>

**output:**
```
2 2 2 2 2 2 2 2 2
2 2 4 4 2 2 3 2 3
2 2 2 4 2 2 3 2 3
2 4 4 4 2 2 3 2 3
2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2
2 2 2 1 2 1 2 2 2
2 2 2 2 2 2 2 2 2
2 2 2 1 2 1 2 2 2
2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2
8 2 2 2 2 5 2 5 2
8 8 2 2 2 5 2 5 2
8 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=576x1088 at 0x7F4C1B74F8D0>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0
0 2 2 0 2 2 2 2 2 0
0 2 0 0 0 2 2 2 2 0
0 2 2 2 2 2 2 2 2 0
0 2 2 2 2 0 0 2 2 0
0 2 2 2 2 0 2 0 2 0
0 2 2 2 2 2 0 0 2 0
0 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 2 4 0 0 0 0 0 0
0 2 2 4 0 0 0 0 0 0
0 4 2 4 0 2 2 3 0 0
0 0 0 0 0 2 3 2 0 0
0 0 0 0 0 3 2 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x1280 at 0x7F4C1B67DF50>

**output:**
```
2 2 2 2 2 2 2 2
2 4 2 4 2 2 2 2
2 2 2 2 2 2 2 2
2 4 4 4 2 2 2 2
2 2 2 2 2 2 3 2
2 2 2 2 2 3 2 2
2 2 2 2 3 2 2 2
2 2 2 2 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=512x512 at 0x7F4C2318BCD0>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 2 8 0 0 0 0
0 0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 8 2 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 2 0 0
0 2 2 2 0 2 2 2 2 2 0 0
0 2 2 0 0 0 2 2 2 2 0 0
0 2 2 2 0 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x1024 at 0x7F4C2318BED0>

**output:**
```
2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2
2 2 8 2 8 2 2 2 2
2 2 2 2 2 2 2 2 2
2 2 8 2 8 2 2 2 2
2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7F4C1B7007D0>
<PIL.Image.Image image mode=RGB size=2752x2704 at 0x7F4C1B6BF5D0>
**INSTRUCTIONS**

above is an example pair for a task

this is your opportunity to perceive the underlying logic that transforms the
input into the output

respond with the following deliverables:

- your perception of the elements of the task
- a YAML block documenting facts - Focus on identifying objects, their properties, actions performed on them, and the relationships between them
- a natural language program - Be as clear and concise as possible, providing a complete description of the transformation rule.


your responses should be considered as information in a report - not a conversation
