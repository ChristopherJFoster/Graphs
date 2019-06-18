def earliest_ancestor(data, id, ancs=None):
    # Create an empty list for ancestors. Each ancestor will itself be a list that begins with the starting id and ends with the ancestor, with each descendent (if any) in between. It is prepopulated with the provided id.
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
            ancs.insert(0, temp_anc) if len(temp_anc) > len(
                ancs[0]) else ancs.append(temp_anc)
            # Recursively call earliest_ancestor on each parent
            earliest_ancestor(data, data[i][0], ancs)

    # Return the earliest ancestor from ancs (the ancestor represented by the longest list). Return lowest id if tied. If len(ancs) is not greater than 1, that means the provided id has no parents: return -1.
    return min([x[-1] for x in ancs if len(
        x) == len(ancs[0])]) if len(ancs) > 1 else -1
