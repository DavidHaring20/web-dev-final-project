def dictionary_factory(cursor, row):
    # Make dictionary
    dictionary = {}
    # For-loop through cursor description and add data to dictionary
    for index, column in enumerate(cursor.description):
        dictionary[column[0]] = row[index]
    return dictionary

def dictionary_factory_JSON(cursor, row):
    # Make dictionary
    dictionary = {}
    # For-loop through cursor description and add data to dictionary
    for index, column in enumerate(cursor.description):
        # Capture column name, tranform to list and get length
        word = column[0]
        wordlist = list(word)
        length = len(wordlist) - 1
        # Loop through word, remove "_" and capitalize letters
        for i in range(length, -1, -1):
            # Check if there is next letter
            if i != 0:
                # Check if the next letter is "_"
                if wordlist[i - 1] == "_":
                    # Get current letter and capitalize it
                    uppercaseLetter = wordlist[i].upper()
                    # Remove current letter and "_" from word
                    wordlist.pop(i)
                    wordlist.pop(i-1)
                    # Insert uppercase letter to word
                    wordlist.insert(i - 1, uppercaseLetter)
        # Transform list back to string
        word = "".join(wordlist)
        dictionary[word] = row[index]
    return dictionary