def bitonic_sort(arr, up=True):
    def compare_and_swap(arr, i, j, up):
        if (arr[i] > arr[j]) == up:
            arr[i], arr[j] = arr[j], arr[i]

    def bitonic_merge(arr, low, cnt, up):
        if cnt > 1:
            k = cnt // 2
            for i in range(low, low + k):
                compare_and_swap(arr, i, i + k, up)
            bitonic_merge(arr, low, k, up)
            bitonic_merge(arr, low + k, k, up)

    def bitonic_sort_rec(arr, low, cnt, up):
        if cnt > 1:
            k = cnt // 2
            bitonic_sort_rec(arr, low, k, True)
            bitonic_sort_rec(arr, low + k, k, False)
            bitonic_merge(arr, low, cnt, up)

    bitonic_sort_rec(arr, 0, len(arr), up)
    return arr
