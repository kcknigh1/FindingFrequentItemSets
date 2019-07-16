import sys
import time
# This prigram uses the A-Priori algorithem to find the frequent item sets
# Uses s values of 2, 5, 10, 25, and 50
# It calculates the memory requirments and time for the s values
# The results are stored in the results dir
# 
# Author: Kyle Knight

# Runs the whole program 
# file_name: where the data is stored
# s: the number of times that the pair needs to appear to be considered frequent
def a_priori(file_name, s):
    print('\n')
    start = time.time()
    item_frequency = find_frequency_in_file(file_name)
    frequent_singles = calculate_frequent_items(item_frequency, s)
    frequent_candidate_pairs = second_loop(file_name, frequent_singles, s)
    end = time.time()
    frequent_pairs = refine_pairs(s, frequent_candidate_pairs)
    write_report_file(s, frequent_singles, frequent_candidate_pairs, frequent_pairs, item_frequency, end-start)

# Loops through the provided file and counts how often each value appears
# Returns an array that holds how often each value appears in the set of data
def find_frequency_in_file(file_name):
    with open("data/"+file_name) as file:
        itemCount = [0 for x in range(2001)]
        for line in file:
            items = line.split(",")
            last = list(items[len(items)-1])
            last = ''.join(last[:-1])
            items[len(items)-1] = last
            for item in items:
                itemCount[int(item)] += 1
        return itemCount

# Finds all the values that appear in the data set more than the s value
# Returns the list of frequent items
def calculate_frequent_items(item_frequency, s):
    frequent_items = []
    for index, count in enumerate(item_frequency):
        if count >= s:
            frequent_items.append(index)
    return frequent_items

# Makes a triange matrix to hold all the possible frequent pairs 
# Based on the frequent_singles that are provided
# Returns the triangle matrix
def construct_pairs(frequent_singles):
    pairs = []
    for index, item in enumerate(frequent_singles):
        pairs.append([0 for x in range(len(frequent_singles)-index)])
    return pairs

# The second loop goes through all the data again and counts how many times pairs 
# made from the frequent_singls appear in the data set
# returns a list of all the frequent candidate pairs (all the values that could be frequent pairs)
def second_loop(file_name, frequent_singles, s):
    with open("data/"+file_name) as file:
        frequent_pairs = {}
        for line in file:
            basket = line.split(",")
            last = list(basket[len(basket)-1])
            last = ''.join(last[:-1])
            basket[len(basket)-1] = last
            for index, item in enumerate(basket):
                if int(item) in frequent_singles and index < len(basket)-2:
                    for secondItem in basket[index+1:]:
                        if int(secondItem) in frequent_singles:
                            pair = item+","+secondItem
                            if pair not in frequent_pairs:
                                frequent_pairs[pair] = 1
                            else:
                                frequent_pairs[pair] += 1
        print("number of candidant pairs: {}".format(len(frequent_pairs)))
        print("size of pairs set: {}Bytes".format(sys.getsizeof(frequent_pairs)))
        numSPairs = 0
        for x, y in frequent_pairs.items():
            if y >=s:
                numSPairs += 1
        print("number of pairs that apair more than {} times {}".format(s, numSPairs))           
        return frequent_pairs

# Goes through the list of frequent_candidate_pairs and collects all the pairs that appear more that s times
# returns that final list of frequent_pairs that appear more than s times
def refine_pairs(s, frequent_candidate_pairs):
    frequent_pairs = {}
    num =0
    for pair, frq in frequent_candidate_pairs.items():
        if frq >= s:
            num +=1
            frequent_pairs[pair] = frq
    return frequent_pairs

# Sets up the header for the report file
# This file holds the over all data for all the s values
def set_up_report():
    with open("results/report_all.txt", "w") as file:
        file.write('This is a collection of all the values.\nMore details can be found in there individual result files.\n')
        file.write('There were to many valus to show legibly in one file\n')
        file.write('\n{:6}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}\n'.format('S', 'Num Frquent', 'Num Frquent', 'Num Candidant', 'Phase1', 'Phase2', 'Total time', 'Size Singles', 'Size Pairs', 'Size Item Frq'))
        file.write('{:6}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}\n\n'.format('Value', 'Single', 'Pair', 'Pairs', 'Mem Usage', 'Mem Usage', '', 'List', 'List', 'List'))
        
# Writes the results data to the files 
# report_all.txt holds numbers for all the different s values
# results_S holds the results for each individual s value 
def write_report_file(s, frequent_singles, frequent_candidate_pairs, frequent_pairs, item_frequency, time):
    with open("results/results_S"+str(s)+".txt", "w") as file:
        file.write('\nWith a s value of {} there are {} frequent pairs\n'.format(s, len(frequent_pairs)))
        file.write('With a s value of {} there are {} frequent candidate pairs\n'.format(s, len(frequent_candidate_pairs)))
        file.write('With a s value of {} there are {} frequent singles\n'.format(s, len(frequent_singles)))
        file.write('There are {} items\n'.format(len(item_frequency)-1))
        file.write('\n\nThe frequent pairs are:\n{}'.format(frequent_pairs))
        file.write('\n\nThe frequent singles are:\n{}'.format(frequent_singles))
        file.write('\n\nThe item frequencys are (index is item name):\n{}'.format(item_frequency))
    with open("results/report_all.txt", "a") as file:
        file.write("{:6}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}\n".format(str(s), str(len(frequent_singles)), str(len(frequent_pairs)), str(len(frequent_candidate_pairs)), str(sys.getsizeof(item_frequency))+' bytes', str(sys.getsizeof(frequent_singles)+sys.getsizeof(frequent_pairs))+' bytes', str(round(time, 4))+' sec', str(sys.getsizeof(frequent_singles))+' bytes', str(sys.getsizeof(frequent_pairs))+' bytes',str(sys.getsizeof(item_frequency))+' bytes'))

# runs the test_data looking for sets of 2, 5, 10, 25, and 50
if __name__ == '__main__':
    set_up_report()
    a_priori("test_data.txt", 2)
    a_priori("test_data.txt", 5)
    a_priori("test_data.txt", 10)
    a_priori("test_data.txt", 25)
    a_priori("test_data.txt", 50)
