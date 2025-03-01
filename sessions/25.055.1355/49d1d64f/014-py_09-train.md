
## example 1
*input:*
```
1 2
3 8
```
*expected output:*
```
0 1 2 0
1 1 2 2
3 3 8 8
0 3 8 0
```
*transformed output:*
```
0 0 0 0 0
0 1 2 1 0
0 3 8 3 0
0 1 2 1 0
0 0 0 0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
1 8 4
8 3 8
```
*expected output:*
```
0 1 8 4 0
1 1 8 4 4
8 8 3 8 8
0 8 3 8 0
```
*transformed output:*
```
0 0 0 0 0
0 4 8 4 0
0 8 3 8 0
0 4 8 4 0
0 0 0 0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
2 1 4
8 0 2
3 2 8
```
*expected output:*
```
0 2 1 4 0
2 2 1 4 4
8 8 0 2 2
3 3 2 8 8
0 3 2 8 0
```
*transformed output:*
```
0 0 0 0 0
0 8 2 8 0
0 2 0 2 0
0 8 2 8 0
0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 17
**FAILED!**
