
## example 1
*input:*
```
0 8
0 0
0 8
```
*expected output:*
```
8 0 0 8
0 0 0 0
8 0 0 8
8 0 0 8
0 0 0 0
8 0 0 8
8 0 0 8
0 0 0 0
8 0 0 8
```
*transformed output:*
```
8 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 8
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
2 0
2 2
2 0
```
*expected output:*
```
0 2 2 0
2 2 2 2
0 2 2 0
0 2 2 0
2 2 2 2
0 2 2 0
0 2 2 0
2 2 2 2
0 2 2 0
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: index 0 is out of bounds for axis 0 with size 0

## example 3
*input:*
```
0 0
0 5
5 0
```
*expected output:*
```
0 5 5 0
5 0 0 5
0 0 0 0
0 0 0 0
5 0 0 5
0 5 5 0
0 5 5 0
5 0 0 5
0 0 0 0
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: index 0 is out of bounds for axis 0 with size 0
