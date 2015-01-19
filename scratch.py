
        
		#checkin posessive clitic
		g for posessive clitic
	    if i + 2 == len(word) and word[i] == "'" and word[i + 1] == "s":
                print "Found posessive clitic!"
                tokens.append(word[last_split: i])
	    elif i + 1 == len(word) and word[i] == "'" and word[i - 1 ] == "s":
                print "Found posessive clitic!"
		tokens.append(word[last_split :i])

