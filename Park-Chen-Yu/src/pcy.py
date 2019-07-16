# import resource
import sys
import time
import BitVector
# This program uses the Park-Chen-Yu algorithem to find the frequent item sets
# Uses s values of 2, 5, 10, 25, and 50
# It calculates the memory requirments and time for the s values
# The results are stored in the results dir
# 
# Author: Kyle Knight

# Runs the whole program 
# file_name: where the data is stored
# s: the number of times that the pair needs to appear to be considered frequent
def pcy(file_name, s):
    print('\n')
    hash_size = 4000
    start = time.time()
    item_frequency = find_frequency_in_file(file_name)
    pair_hash_table = populat_hash_table(file_name, hash_size)
    bit_vector = hash_table_to_bit_vector(pair_hash_table, s)
    frequent_singles = calculate_frequent_items(item_frequency, s)
    frequent_candidate_pairs = second_loop(file_name, frequent_singles, s, bit_vector, hash_size)
    end = time.time()
    frequent_pairs = refine_pairs(s, frequent_candidate_pairs)
    write_report_file(s, frequent_singles, frequent_candidate_pairs, frequent_pairs, item_frequency, end-start, pair_hash_table, bit_vector)

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

# Puts all the pairs in to buckets in a hash table so it can be used to create 
# Bitmap of the buckets for the second loop
# to be considered a canidate pair it has to land in a bucket that has more then s values in it
def populat_hash_table(file_name, hash_size):
    with open("data/"+file_name) as file:
        # hash_size = 4000
        hash_table = create_empty_table(hash_size)
        for line in file:
            basket = line.split(",")
            #removeing the \n at the end of the line
            last = list(basket[len(basket)-1])
            last = ''.join(last[:-1])
            basket[len(basket)-1] = last
            # print(basket)
            for index, item in enumerate(basket):
                for secondItem in basket[index+1:]:
                    hash_table[abs(hash(item+secondItem))%hash_size] += 1
        return hash_table

# Convertes that hash table into a bitvector setting one it the
# bucket has more than s value in it
def hash_table_to_bit_vector(hash_table, s):
    bit_vector = BitVector.BitVector(size = len(hash_table))
    for index, value in enumerate(hash_table):
        if hash_table[value] >= s:
            bit_vector[index] = 1
    return bit_vector

# Creates an empty hash table of the provided size
def create_empty_table(size):
    hash_table = {}
    for num in range(size):
        hash_table[num] = 0
    return hash_table

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
# made from the frequent_singls appear in the data set also checks that the values land in a bucket that has more than s items in it
# returns a list of all the frequent candidate pairs (all the values that could be frequent pairs)
def second_loop(file_name, frequent_singles, s, bit_vector, hash_size):
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
                        if int(secondItem) in frequent_singles and bit_vector[abs(hash(item+secondItem))%hash_size] == 1:
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

def refine_pairs(s, frequent_candidate_pairs):
    frequent_pairs = {}
    num =0
    for pair, frq in frequent_candidate_pairs.items():
        if frq >= s:
            num +=1
            # print('{}  {}:{}'.format(num, pair, frq))
            frequent_pairs[pair] = frq

    return frequent_pairs

# Sets up the header for the report file
# This file holds the over all data for all the s values
def set_up_report(hash_size):
    with open("results/report_all.txt", "w") as file:
        file.write('This is a collection of all the values.\nMore details can be found in there individual result files.\n')
        file.write('There were to many valus to show legibly in one file\n')
        file.write('I used a hash table of size {} because it made Phase1 use about the same\n'.format(hash_size)+
            'memory as the largest loop of the second phase using the A-Priori method.\n'+
            'It apears that the Phase2 of PCY uses as much memory as A-Prori so the adding the bit vector\n'+
            'did not help. It also made the PCY take more time to do the computations.\n')

        file.write('\n{:6}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}\n'.format('S', 'Num Frquent', 'Num Frquent', 'Num Candidant', 'Phase1', 'Phase2', 'Total time', 'Size Singles','Size Pairs','Size Bit', 'Size Item Frq', 'Size Hash '))
        file.write('{:6}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}\n\n'.format('Value', 'Single', 'Pair', 'Pairs', 'Mem Usage', 'Mem Usage', '', 'List P2', 'List P2', 'Vector P2', 'List P1', 'Table P1'))
        
# Writes the results data to the files 
# report_all.txt holds numbers for all the different s values
# results_S holds the results for each individual s value 
def write_report_file(s, frequent_singles, frequent_candidate_pairs, frequent_pairs, item_frequency, time, pair_hash_table, bit_vector):
    with open("results/results_S"+str(s)+".txt", "w") as file:
        file.write('\nWith a s value of {} there are {} frequent pairs\n'.format(s, len(frequent_pairs)))
        file.write('With a s value of {} there are {} frequent candidate pairs\n'.format(s, len(frequent_candidate_pairs)))
        file.write('With a s value of {} there are {} frequent singles\n'.format(s, len(frequent_singles)))
        file.write('There are {} items\n'.format(len(item_frequency)-1))
        file.write('I used a hash table with 4000 buckets to compute the bit vector\n')
        file.write('\n\nThe frequent pairs are:\n{}'.format(frequent_pairs))
        file.write('\n\nThe frequent singles are:\n{}'.format(frequent_singles))
        file.write('\n\nThe bitvector is :\n{}'.format(bit_vector))
        file.write('\n\nThe hash table for the pairs:\n{}'.format(pair_hash_table))
        file.write('\n\nThe item frequencys are (index is item name):\n{}'.format(item_frequency))
    with open("results/report_all.txt", "a") as file:
        file.write("{:6}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}{:15}\n".format(str(s), str(len(frequent_singles)), str(len(frequent_pairs)), str(len(frequent_candidate_pairs)), str(sys.getsizeof(item_frequency)+sys.getsizeof(pair_hash_table))+' bytes', str(sys.getsizeof(frequent_singles)+sys.getsizeof(frequent_pairs)+sys.getsizeof(bit_vector))+' bytes', str(round(time, 4))+' sec', str(sys.getsizeof(frequent_singles))+' bytes', str(sys.getsizeof(frequent_pairs))+' bytes', str(sys.getsizeof(bit_vector))+' bytes',str(sys.getsizeof(item_frequency))+' bytes',str(sys.getsizeof(pair_hash_table))+' bytes'))
    

# runs the test_data looking for sets of 2, 5, 10, 25, and 50
if __name__ == '__main__':
    set_up_report(4000)
    pcy("test_data.txt", 2)
    pcy("test_data.txt", 5)
    pcy("test_data.txt", 10)
    pcy("test_data.txt", 25)
    pcy("test_data.txt", 50)
