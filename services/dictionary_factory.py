def dictionary_factory(cursor, row):
    # Make dictionary
    dictionary = {}
    # For-loop through cursor description and add data to dictionary
    for index, column in enumerate(cursor.description):
        dictionary[column[0]] = row[index]
    return dictionary