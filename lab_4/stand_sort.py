def strand_sort(arr):
    def merge_lists(a, b):
        result = []
        i = j = 0
        while i < len(a) and j < len(b):
            if a[i] < b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        result.extend(a[i:])
        result.extend(b[j:])
        return result

    if len(arr) <= 1:
        return arr.copy()

    strand = [arr[0]]
    remaining = []

    for i in range(1, len(arr)):
        if not (arr[i] < strand[-1]):
            strand.append(arr[i])
        else:
            remaining.append(arr[i])

    return merge_lists(strand, strand_sort(remaining))
