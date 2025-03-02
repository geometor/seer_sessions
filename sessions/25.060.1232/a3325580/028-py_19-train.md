
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8
0 0 4 0 0 0 0 0 0 8
0 0 4 0 0 6 6 0 0 8
0 0 4 4 0 0 6 0 0 0
0 0 4 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
4 6 8
4 6 8
4 6 8
4 6 8
4 6 8
```
*transformed output:*
```

```
**ERROR**: Could not save image: 'NoneType' object has no attribute 'to_image'

## example 2
*input:*
```
0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0 4
0 9 0 0 0 6 0 0 4 4
0 9 9 0 0 6 0 0 0 4
9 9 0 0 6 6 6 0 0 0
0 9 0 0 0 0 6 0 0 0
0 9 9 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
9 4
9 4
9 4
9 4
9 4
9 4
9 4
9 4
9 4
```
*transformed output:*
```

```
**ERROR**: Could not save image: 'NoneType' object has no attribute 'to_image'

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0 1
7 7 7 0 0 2 2 0 0 1
0 0 7 0 0 0 2 2 0 1
0 0 0 0 0 0 2 0 0 1
0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
2
2
2
2
2
```
*transformed output:*
```
1
1
1
1
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 4
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 6 0 0 0
0 0 8 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
8
8
8
```
*transformed output:*
```
8
8
8
```
size: True
palette: True
color count: True
pixels off: 0
PASSED

## example 5
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 3 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
2 3
2 3
2 3
```
*transformed output:*
```

```
**ERROR**: Could not save image: 'NoneType' object has no attribute 'to_image'

## example 6
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 8 8 8
0 1 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
1 4 8
1 4 8
1 4 8
```
*transformed output:*
```
1
1
1
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**
