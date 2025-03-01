
## example 1
*input:*
```
2 8 3 0 0 0 0
8 3 0 0 0 0 0
3 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
*expected output:*
```
2 8 3 2 8 3 2
8 3 2 8 3 2 8
3 2 8 3 2 8 3
2 8 3 2 8 3 2
8 3 2 8 3 2 8
3 2 8 3 2 8 3
2 8 3 2 8 3 2
```
*transformed output:*
```
2 8 3 8 3 4 8
8 3 3 4 8 3 4
3 4 8 3 4 8 3
8 3 4 8 3 4 8
4 8 3 4 8 3 4
3 4 8 3 4 8 3
8 3 4 8 3 4 8
```
size: True
palette: False
color count: False
pixels off: 34
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 1
0 0 0 0 0 1 2
0 0 0 0 1 2 4
0 0 0 1 2 4 0
0 0 1 2 4 0 0
```
*expected output:*
```
2 4 1 2 4 1 2
4 1 2 4 1 2 4
1 2 4 1 2 4 1
2 4 1 2 4 1 2
4 1 2 4 1 2 4
1 2 4 1 2 4 1
2 4 1 2 4 1 2
```
*transformed output:*
```
8 3 4 8 3 4 8
4 8 3 4 8 3 4
3 4 8 3 4 8 1
8 3 4 8 3 1 2
4 8 3 4 1 2 4
3 4 8 1 2 4 3
8 3 1 2 4 4 8
```
size: True
palette: False
color count: False
pixels off: 32
**FAILED!**

## example 3
*input:*
```
0 0 0 0 8 3 0
0 0 0 8 3 0 0
0 0 8 3 0 0 0
0 8 3 0 0 0 4
8 3 0 0 0 4 0
3 0 0 0 4 0 0
0 0 0 4 0 0 0
```
*expected output:*
```
4 8 3 4 8 3 4
8 3 4 8 3 4 8
3 4 8 3 4 8 3
4 8 3 4 8 3 4
8 3 4 8 3 4 8
3 4 8 3 4 8 3
4 8 3 4 8 3 4
```
*transformed output:*
```
8 3 4 8 8 3 8
4 8 3 8 3 3 4
3 4 8 3 4 8 3
8 8 3 8 3 4 4
8 3 3 4 8 4 4
3 4 8 3 4 8 3
8 3 4 4 3 4 8
```
size: True
palette: True
color count: False
pixels off: 24
**FAILED!**
