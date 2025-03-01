
## example 1
*input:*
```
6 0 6
0 6 6
6 0 6
4 0 4
0 4 4
4 0 4
8 8 8
8 0 8
8 8 8
```
*expected output:*
```
8 8 8
8 0 8
8 8 8
```
*transformed output:*
```



```
**ERROR**: Could not save image: 'NoneType' object has no attribute 'to_image'

## example 2
*input:*
```
2 0 0 3 0 0 7 0 7 1 0 0
2 0 0 3 0 0 0 7 0 1 0 0
0 2 2 0 3 3 7 0 7 0 1 1
```
*expected output:*
```
7 0 7
0 7 0
7 0 7
```
*transformed output:*
```
3 0 0
3 0 0
0 3 3
```
size: True
palette: False
color count: False
pixels off: 7
**FAILED!**

## example 3
*input:*
```
3 0 0 4 0 4 2 0 0 8 0 0 1 0 0
0 3 3 4 4 4 0 2 2 0 8 8 0 1 1
0 3 0 4 0 4 0 2 0 0 8 0 0 1 0
```
*expected output:*
```
4 0 4
4 4 4
4 0 4
```
*transformed output:*
```
4 0 4
4 4 4
4 0 4
```
size: True
palette: True
color count: True
pixels off: 0
PASSED
