def is_greater(val1, val2):
    """
    if val1 >= val2 return True
    else return False
    """
    splits1 = val1.split('.')
    splits2 = val2.split('.')
    for v1, v2 in zip(splits1,splits2):

        if int(v1) > int(v2):
            return True
        elif int(v1) < int(v2):
            return False
    if len(splits1) >= len(splits2):
        return True
    return False

def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1     # left = 2*i + 1
    r = 2 * i + 2     # right = 2*i + 2
  
    # See if left child of root exists and is
    # greater than root
    if l < n and is_greater(arr[l], arr[i]):
        largest = l
  
    # See if right child of root exists and is
    # greater than root
    if r < n and is_greater(arr[r], arr[largest]):
        largest = r
  
    # Change root, if needed
    if largest != i:
        arr[i],arr[largest] = arr[largest],arr[i]  # swap
  
        # Heapify the root.
        heapify(arr, n, largest)


def solution(arr):
    n = len(arr)
  
    # Build a maxheap.
    # Since last parent will be at ((n//2)-1) we can start at that location.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
  
    # One by one extract elements
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]   # swap
        heapify(arr, i, 0)

    return arr