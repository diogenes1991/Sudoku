def find_missing(array,missing):
    ''' Returns the numbers in missing and not in array '''
    if len(array)==0:
        return missing
    for i,na in enumerate(array):
        for j,nm in enumerate(missing):
            if na == nm:
                del missing[j]
                new_array = array.copy()
                del new_array[i]
                return find_missing(new_array,missing)
    return missing

def find_common(array1,array2,common):
    ''' Returns the common elements between two arrays '''
    if len(array1)==0 or len(array2)==0:
        return common
    for i,na1 in enumerate(array1):
        for j,na2 in enumerate(array2):
            if na1 == na2:
                new_array1 = array1.copy()
                new_array2 = array2.copy()
                common.append(na1)
                del new_array1[i]
                del new_array2[j]
                return find_common(new_array1,new_array2,common)
    return common