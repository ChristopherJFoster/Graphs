def earliest_ancestor(data, id, ancs=None):
    # Create an empty list for ancestors. Each ancestor will itself be a list that begins with the starting id and ends with the ancestor, with each descendent (if any) in between. It is prepopulated with the provided id.
    if ancs == None:
        ancs = [[id]]
    # Find parents of the current id by looking through data for any list that ends with the id. Add any parents to ancs.
    for i in range(len(data)):
        if data[i][1] == id:
            # Create the correct lineage for new ancestor by finding and copying the lineage for that ancestor's child (which is the current id):
            lineage = [list(ancs[j])
                       for j in range(len(ancs)) if ancs[j][-1] == id][0]
            lineage.append(data[i][0])
            # Add new ancestor to the front of ancs if it's a new record for longest lineage; otherwise add new ancestor to the back of ancs.
            ancs.insert(0, lineage) if len(lineage) > len(
                ancs[0]) else ancs.append(lineage)
            # Recursively call earliest_ancestor() on the new ancestor
            earliest_ancestor(data, data[i][0], ancs)
    # Return the earliest ancestor from ancs (the ancestor represented by the longest list). Return lowest id if tied. If len(ancs) is not greater than 1, that means the provided id has no parents: return -1. The following code takes advantage of the fact that ancs is partially sorted such that the earliest ancestor (or one which is tied) is in the front of ancs.
    return min([x[-1] for x in ancs if len(
        x) == len(ancs[0])]) if len(ancs) > 1 else -1
