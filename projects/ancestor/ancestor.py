example = [(1, 3),
           (2, 3),
           (3, 6),
           (5, 6),
           (5, 7),
           (4, 5),
           (4, 8),
           (8, 9),
           (11, 8),
           (10, 1)]


def earliest_ancestor(id, data, ancs=None):
    # Create an empty list for ancestors. Each ancestor will itself be a list that begins with the starting id and ends with the ancestor, with each descendent (if any) in between. It is prepopulated with the starting id.
    if ancs == None:
        ancs = []
        ancs.append([id])
    # Find parents of the current id by looking through data for any list that ends with the id. Add any parents to ancs.
    for i in range(len(data)):
        if data[i][1] == id:
            # Add parent to ancs:
            print(ancs)
            temp_anc = []
            for j in range(len(ancs)):
                if ancs[j][-1] == id:
                    temp_anc = list(ancs[j])
            temp_anc.append(data[i][0])
            ancs.append(temp_anc)
            # Recursively call earliest_ancestor on each parent
            earliest_ancestor(data[i][0], data, ancs)

    # Base case is when there are no parents for a given id

    # return the ancestor from ancs with the longest list (lowest id if tied). Not yet sure how to check for this in a recursive function.
    earliest = sorted(ancs, key=lambda anc: -len(anc))
    return earliest


print(earliest_ancestor(6, example))
