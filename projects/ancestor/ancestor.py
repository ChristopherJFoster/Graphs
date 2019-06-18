example = [[1, 3],
           [2, 3],
           [3, 6],
           [5, 6],
           [5, 7],
           [4, 5],
           [4, 8],
           [8, 9],
           [11, 8],
           [10, 1]]


def earl_anc(id, data, ancs=None):
    # Create an empty list for ancestors. Each ancestor will itself be a list that begins with the starting id and ends with the ancestor, with each descendent (if any) in between. It is prepopulated with the starting id.
    if ancs == None:
        ancs = [[id]]
        earl_anc(ancs[-1][-1], data, ancs)
    # Find parents of the current id by looking through data for any list that ends with the id. Add any parents to ancestors.

    # Recursively call earl_and on each parent

    # Base case is when there are no parents for a given id

    # return the ancestor from ancs with the longest list (lowest id if tied). Not yet sure how to check for this in a recursive function.


print(earl_anc(6, example))
