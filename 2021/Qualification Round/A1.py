def makeConsistent(string):
	req = None
	for i in range(65, 91):
		count = 0
		ltr = chr(i)
		isVowel = ltr in ["A", "E", "I", "O", "U"]
		for c in string:
			if c == ltr:
				continue
			if isVowel == (c in ["A", "E", "I", "O", "U"]):
				count += 2
			else:
				count += 1
		if req is None or count < req:
			req = count
	return req

with open("1_output.txt", "w+") as of:
	with open("consistency_chapter_1_input.txt", "r") as f:
		noSeen = False
		case = 0
		for line in f.read().split("\n"):
			if not noSeen:
				noSeen = int(line)
				continue
			if case >= noSeen:
				break
			case += 1
			if case > 1:
				of.write("\n")
			of.write("Case #" + str(case) + ": " + str(makeConsistent(line)))