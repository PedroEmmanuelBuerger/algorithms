def find_duplicate(nums):
    if len(nums) == 0:
        return False
    if not verify_numbers(nums):
        return False
    duplicate_count = {}
    for num in nums:
        if num in duplicate_count:
            return num
        else:
            duplicate_count[num] = 1
    return False


def verify_numbers(nums):
    try:
        for num in nums:
            if num < 0 or type(num) != int:
                return False
        return True
    except TypeError:
        return False


print(find_duplicate(["a", "b"]))