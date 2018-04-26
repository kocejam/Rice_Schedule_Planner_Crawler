import csv
import re

def readCsvFile(fname):
    """
    @param fname: string, name of file to write
    @param data: list of list of items

    Read data from file
    """
    data = []
    with open(fname, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)


    return data

course_data = readCsvFile("dist1.csv")


index = {}
reverse_index = {}
for idx in range(len(course_data[0])):
    index[course_data[0][idx]] = idx
    reverse_index[idx] = course_data[0][idx]

prompts = {}
prompts[1] = "Input the name of the instructor you wish to filter by. "
prompts[2] = "Input the average organization rating, where 1 = Outstanding, 2 = Good, 3 = Average, 4 = Fair, 5 = Poor. "
prompts[3] = "Input the average assignment rating, where 1 = Outstanding, 2 = Good, 3 = Average, 4 = Fair, 5 = Poor. "
prompts[4] = "Input the average overall rating, where 1 = Outstanding, 2 = Good, 3 = Average, 4 = Fair, 5 = Poor. "
prompts[5] = "Input the average 'Were you challenged?' rating, where 1 = Strongly Agree, 2 = Agree, 3 = Neutral, 4 = Disagree, 5 = Strongly Disagree. "
prompts[6] = "Input the average workload rating, where 1 = Much Lighter, 2 = Somewhat Lighter, 3 = Average, 4 = Somewhat Heavier, 5 = Much Heavier. "
prompts[7] = "Lol do you really care about this.. "
prompts[8] = "Input the average expected grade, where 1 = A, 2 = B, 3 = C, 4 = D, 5 = F. "
prompts[9] = "Input the average P/F grade, where 1 = P, 2 = F, 3 = S, 4 = U, 5 = N/A. "
prompts[10] = "Input the number of response counts. "

# course_data = course_data[1:]

print course_data

MENU = ""

# def line_test(line, percentages):
#     for idx in range(len(line)):
#         if

def filter_data(data, categories, percentages):
    percentage_filtered = []
    filtered = []

    percentage_filtered.append(data[0])
    for idx in range(1, len(data)):
        bad = False
        line = data[idx]
        for category in percentages:
            if category == 10:  #special case for counts
                if float(line[category]) < percentages[category]:
                    bad = True
                continue

            if float(line[category]) > percentages[category]:
                bad = True

        if bad:
            continue
        else:
            percentage_filtered.append(line)


    sorted_cats = list(categories)
    sorted_cats.append(0)
    if 2 not in sorted_cats:
        sorted_cats.append(1)
    sorted_cats.sort()

    for line in percentage_filtered:
        new_line = []
        for idx in sorted_cats:
            new_line.append(line[idx])
        filtered.append(new_line)

    return filtered

def runMenu():
    while (True):
        print(MENU)

        options = raw_input("Which categories do you care about? ")

        split_strings = re.split("[,\s]+", str(options))

        categories = []

        if split_strings[0] == "":
            print "You didn't ask for anything!\n"
            raw_input("Press enter to return to the menu.\n")
            continue

        if split_strings[-1] == "":
            split_strings.pop()

        for idx in range(len(split_strings)):

            try:
                category = int(split_strings[idx])
            except:
                print "Error: incorrect input.\n"
                raw_input("Press enter to return to the menu.\n")
                continue

            if category > len(index) - 1 or category < 1:
                print "Error: category does not exist.\n"
                raw_input("Press enter to return to the menu.\n")
                continue

            if category in categories:
                continue

            categories.append(category)

        percentages = {}

        error = False

        for num in categories:
            answer = raw_input(prompts[num])

            try:
                answer = float(answer)
            except:
                print "Error: Bad input.\n"
                error = True
                break

            if num == 10:
                if answer < 0:
                    print "Error: That's an impossible count number!\n"
                    error = True
                    break
            elif answer < 0 or answer > 5:
                print "Error: That's an impossible average!\n"
                error = True
                break

            percentages[num] = answer

        if error:
            raw_input("Press enter to return to the menu.\n")
            continue

        print filter_data(course_data, categories, percentages)

        raw_input("Press enter to return to the menu.\n")

    return

# print reverse_index
# print filter_data(course_data, [3, 4, 8, 10], {8: 2, 10: 7})
runMenu()