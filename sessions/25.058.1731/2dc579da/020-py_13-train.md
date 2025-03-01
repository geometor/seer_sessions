
## example 1
*input:*
```
8 8 3 8 8
8 8 3 8 8
3 3 3 3 3
8 8 3 8 8
4 8 3 8 8
```
*expected output:*
```
8 8
4 8
```
*transformed output:*
```
0 0 0 0 0
0 0 0 0 0
0 0 8 0 0
0 0 0 0 0
0 0 0 0 0
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
4 4 4 2 4 4 4
4 4 4 2 4 1 4
4 4 4 2 4 4 4
2 2 2 2 2 2 2
4 4 4 2 4 4 4
4 4 4 2 4 4 4
4 4 4 2 4 4 4
```
*expected output:*
```
4 4 4
4 1 4
4 4 4
```
size: None
palette: None
color count: None
pixels off: None
**FAILED!**

## example 3
*input:*
```
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
3 8 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
1 1 1 1 1 1 1 1 1 1 1
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
```
*expected output:*
```
3 3 3 3 3
3 3 3 3 3
3 8 3 3 3
3 3 3 3 3
3 3 3 3 3
```
*transformed output:*
```
0 0 0 0 0
0 0 0 0 0
0 0 8 0 0
0 0 0 0 0
0 0 0 0 0
```
size: True
palette: False
color count: False
pixels off: 25
**FAILED!**
