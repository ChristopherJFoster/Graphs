def earliest_ancestor(data, id, ancs=None):
    # Create an empty list for ancestors. Each ancestor will itself be a list that begins with the starting id and ends with the ancestor, with each descendent (if any) in between. It is prepopulated with the starting id.
    if ancs == None:
        ancs = []
        ancs.append([id])
    # Find parents of the current id by looking through data for any list that ends with the id. Add any parents to ancs.
    for i in range(len(data)):
        if data[i][1] == id:
            # Add parent to ancs:
            temp_anc = []
            for j in range(len(ancs)):
                if ancs[j][-1] == id:
                    temp_anc = list(ancs[j])
            temp_anc.append(data[i][0])
            ancs.append(temp_anc)
            # Recursively call earliest_ancestor on each parent
            earliest_ancestor(data, data[i][0], ancs)

    # Base case is when there are no parents for a given id

    # return the ancestor from ancs with the longest list (lowest id if tied). Not yet sure how to check for this in a recursive function.
    if len(ancs) == 1:
        return -1
    else:
        sorted_by_earliest = sorted(ancs, key=lambda anc: -len(anc))
        earliest = [x[-1] for x in sorted_by_earliest if len(
            x) == len(sorted_by_earliest[0])]
        # earliest =
        return min(earliest)
