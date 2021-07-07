#Pass 1 for compression or 2 for decompression

# @brief--
#nc - No Compression
#rle - Run Length Encoding
#bitmask - BitMask type
#1bm - 1 Bit Mismatch
#2bcm - 2 Bit Consecutive Mismatch
#4bcm - 4 Bit Consecutive Mismatch
#2bm - 2 Bit Mismatch 
#dm - Direct Mismatch

import itertools
import sys
dictionary_counter_list = {}
dictionary = {} 
temp_compressed_Binary_string = ''
DICTIONARY_LENGTH = 16
DIC_BITS = 4
reference_pattern = {'nc': '000', 'rle': '001', 'bitmask': '010', '1bm': '011', '2bcm': '100', '4bcm': '101',
                     '2bm': '110', 'dm': '111'}
 
def read_original_txt():
    file = open("original.txt", "r")
    binary_instructions = file.readlines()
    return binary_instructions

def create_frequency_dictionary(dic_length):
    binary_instructions = read_original_txt()
    dic_counter = 0
    for instruction in binary_instructions:
        ins_to_match = instruction.strip('\n')
        for instxn in binary_instructions:
            ins = instxn.strip('\n')
            if ins_to_match == ins:
                dic_counter += 1
        dictionary_counter_list[ins_to_match] = dic_counter
        dic_counter = 0
    sdic = dict(sorted(dictionary_counter_list.items(), key=lambda item: -item[1]))
    return dict(itertools.islice(sdic.items(), dic_length))


def binary_gen(n):
    l = [bin(x)[2:].rjust(n, '0') for x in range(2 ** n)]
    return l


def binnarynum_threeb(n):
    return "{0:03b}".format(n)


def binnarynum_fiveb(n):
    return "{0:05b}".format(n)


def str_to_bin(num):
    n = int(num, 2)
    return "{0:032b}".format(n)


def make_dictionary():
    freq_dic = create_frequency_dictionary(DICTIONARY_LENGTH)
    bin_list = binary_gen(DIC_BITS)
    i = 0
    for key, value in freq_dic.items():
        freq_dic[key] = bin_list[i]
        i += 1
    i = 0
    return freq_dic


def check_Compression_match():
    global binary_instructions
    global temp_compressed_Binary_string
    dic = make_dictionary()
    execution_flag = 1
    bininstruction = str_to_bin(binary_instructions[I_cnt])

    if execution_flag == 1:  # direct match
        for key in dic.keys():
            binkey = str_to_bin(key)
            xorr = "{0:032b}".format(int(bininstruction, 2) ^ int(binkey, 2))
            hammingdistance = xorr.count("1")
            if hammingdistance == 0:
                # print("dm")
                temp_compressed_Binary_string += reference_pattern['dm'] + dic[bininstruction]
                execution_flag = 0
                break
    if execution_flag == 1:  # bitmask
        for key in dic.keys():
            binkey = str_to_bin(key)
            xorr = "{0:032b}".format(int(bininstruction, 2) ^ int(binkey, 2))
            hammingdistance = xorr.count("1")
            if hammingdistance == 2 or hammingdistance == 3:
                if ((xorr.rindex("1") - xorr.index("1")) == 3) or ((xorr.rindex("1") - xorr.index("1")) == 2):
                    pos1 = xorr.index("1")
                    bitmask_value = xorr[pos1:(pos1 + 4)]
                    temp_compressed_Binary_string += reference_pattern['bitmask'] + binnarynum_fiveb(
                        pos1) + bitmask_value + dic[binkey]
                    execution_flag = 0
                    break

    if execution_flag == 1:
        for key in dic.keys():
            binkey = str_to_bin(key)
            xorr = "{0:032b}".format(int(bininstruction, 2) ^ int(binkey, 2))
            hammingdistance = xorr.count("1")
            if hammingdistance == 1:
                pos5 = xorr.index("1")
                temp_compressed_Binary_string += reference_pattern['1bm'] + binnarynum_fiveb(pos5) + dic[binkey]
                execution_flag = 0
                break

    if execution_flag == 1:
        for key in dic.keys():
            binkey = str_to_bin(key)
            xorr = "{0:032b}".format(int(bininstruction, 2) ^ int(binkey, 2))
            hammingdistance = xorr.count("1")
            if hammingdistance == 2:
                if (xorr.rindex("1") - xorr.index("1")) == 1:  # 2 bit conecutive mismatches
                    position = xorr.index("1")
                    temp_compressed_Binary_string += reference_pattern['2bcm'] + binnarynum_fiveb(position) + dic[
                        binkey]
                    execution_flag = 0
                    break

    if execution_flag == 1:
        for key in dic.keys():
            binkey = str_to_bin(key)
            xorr = "{0:032b}".format(int(bininstruction, 2) ^ int(binkey, 2))
            hammingdistance = xorr.count("1")
            if hammingdistance == 4:
                if (xorr.rindex("1") - xorr.index("1")) == 3:  # 4 bit conecutive mismatches
                    pos3 = xorr.index("1")
                    temp_compressed_Binary_string += reference_pattern['4bcm'] + binnarynum_fiveb(pos3) + dic[binkey]
                    execution_flag = 0
                    break

    if execution_flag == 1:
        for key in dic.keys():
            binkey = str_to_bin(key)
            xorr = "{0:032b}".format(int(bininstruction, 2) ^ int(binkey, 2))
            hammingdistance = xorr.count("1")
            if hammingdistance == 2:
                if (xorr.rindex("1") - xorr.index("1")) > 3:
                    position1 = xorr.index("1")
                    position2 = xorr.rindex("1")
                    temp_compressed_Binary_string += reference_pattern['2bm'] + binnarynum_fiveb(
                        position1) + binnarynum_fiveb(position2) + dic[binkey]
                    execution_flag = 0
                    break

    if execution_flag == 1:
        for key in dic.keys():
            binkey = str_to_bin(key)
            xorr = "{0:032b}".format(int(bininstruction, 2) ^ int(binkey, 2))
            hammingdistance = xorr.count("1")
            if hammingdistance >= 4:
                if (xorr.rindex("1") - xorr.index("1")) > 3:
                    temp_compressed_Binary_string += reference_pattern['nc'] + bininstruction
                    execution_flag = 0
                    break

    return temp_compressed_Binary_string


def create_compressed_file():
    global temp_compressed_Binary_string
    compressed_code = temp_compressed_Binary_string
    fi = open("cout.txt", "w")
    dic_flg = 0
    while 1:
        if len(compressed_code) > 32:
            line = compressed_code[:32]
            compressed_code = compressed_code[32:]
            fi.write(line)
            fi.write("\n")
        else:
            trailing_zeros_count = 32 - len(compressed_code)
            compressed_code += '0' * trailing_zeros_count
            line = compressed_code
            fi.write(line)
            fi.write("\n")
            dic_flg = 1

        if dic_flg:
            fi.write("xxxx")
            fi.write("\n")
            for key in dic.keys():
                binkey = str_to_bin(key)
                fi.write(binkey)
                fi.write("\n")
            fi.close()
            break

def parse_compressed_txt():
    global decompressed_code
    with open('comp.txt') as f:
        for line in iter(lambda: f.readline().rstrip(), 'xxxx'):
            decompressed_code += line
    return decompressed_code
def parse_dic_from_compressed_text():
    global dic_dcomp_flag
    with open('comp.txt') as fi:
        for li in fi.readlines():
            if dic_dcomp_flag:
                decomp_dictionary.append(li.rstrip("\n"))
            if li.rstrip("\n") == 'xxxx':
                dic_dcomp_flag = 1
    return decomp_dictionary
def create_decompressed_file():
    global decompression_output
    de_compressed_code = decompression_output
    fil = open("dout.txt", "w")
    dic_flg = 0
    while 1:
        if len(de_compressed_code) >= 32:
            line = de_compressed_code[:32]
            de_compressed_code = de_compressed_code[32:]
            fil.write(line)
            fil.write("\n")

        else:
            fil.close()
            break
mode = sys.argv[1]

if int(mode) ==1:
    global binary_instructions
    binary_instructions = read_original_txt()
    rle_counter = 0
    rle_flag = False
    I_cnt = 0
    rle_counter = 0
    rle_freq = 0
    dic = make_dictionary()
    for I_cnt in range(len(binary_instructions)):
        if I_cnt == 0:
            check_Compression_match()

        else:
            if binary_instructions[I_cnt] != binary_instructions[I_cnt - 1]:
                check_Compression_match()

            elif binary_instructions[I_cnt] == binary_instructions[I_cnt - 1] and rle_freq == 0:
                rle_counter += 1

                if I_cnt != (len(binary_instructions)):
                    if rle_counter != 8 and binary_instructions[I_cnt] == binary_instructions[I_cnt + 1]:
                        continue
                    elif rle_counter == 8 and binary_instructions[I_cnt] == binary_instructions[I_cnt + 1]:
                        temp_compressed_Binary_string += reference_pattern['rle'] + binnarynum_threeb(rle_counter - 1)
                        rle_counter = 0
                        rle_freq = 1
                    else:
                        temp_compressed_Binary_string += reference_pattern['rle'] + binnarynum_threeb(rle_counter - 1)
                        rle_counter = 0
                elif I_cnt == (len(binary_instructions)):
                    temp_compressed_Binary_string += reference_pattern['rle'] + binnarynum_threeb(rle_counter - 1)
                    rle_counter = 0
            else:
                check_Compression_match()
                rle_freq = 0
    create_compressed_file()
elif int(mode)==2:
    decompressed_code = ''
    decomp_dictionary = []
    dic_index = binary_gen(4)
    dic_dcomp_flag = 0

    parse_compressed_txt()
    parse_dic_from_compressed_text()
    decompression_output = ''
    ref_mask = '0' * 32
    dic_dict = dict(zip(dic_index, decomp_dictionary))
    while (len(decompressed_code) != 0):

        # direct match
        if decompressed_code[:3] == '111':
            decompressed_code = decompressed_code[3:]
            dic_val = decompressed_code[:4]
            decompressed_code = decompressed_code[4:]
            decompression_output += dic_dict[dic_val]

        if decompressed_code[:3] == '000':
            if len(decompressed_code) >= 35:  # 35 = 32(uncomp code size) + 3bit(indexing)
                decompressed_code = decompressed_code[3:]
                dic_val = decompressed_code[:32]
                decompressed_code = decompressed_code[32:]
                decompression_output += dic_val
            else:
                decompressed_code = ''

        if decompressed_code[:3] == '001':
            decompressed_code = decompressed_code[3:]
            dic_val = decompression_output[-32:] * (int(decompressed_code[:3], 2) + 1)
            decompressed_code = decompressed_code[3:]
            decompression_output += dic_val

        if decompressed_code[:3] == '011':
            bitmask = '1'
            decompressed_code = decompressed_code[3:]
            mis_position = int(decompressed_code[:5], 2)
            decompressed_code = decompressed_code[5:]
            xor_value1 = ref_mask[:mis_position] + bitmask + ref_mask[(mis_position + 1):]
            dic_val1 = decompressed_code[:4]
            decompressed_code = decompressed_code[4:]
            ins = '{:032b}'.format(int(xor_value1, 2) ^ int(dic_dict[dic_val1], 2))
            decompression_output += ins

        if decompressed_code[:3] == '010':
            decompressed_code = decompressed_code[3:]
            int_index = int(decompressed_code[:5], 2)
            decompressed_code = decompressed_code[5:]
            bitmask1 = decompressed_code[:4]
            decompressed_code = decompressed_code[4:]
            xor_value = ref_mask[:int_index] + bitmask1 + ref_mask[(int_index + 4):]
            dic_val = decompressed_code[:4]
            decompressed_code = decompressed_code[4:]
            ins = '{:032b}'.format(int(xor_value, 2) ^ int(dic_dict[dic_val], 2))
            decompression_output += ins

        if decompressed_code[:3] == '100':
            decompressed_code = decompressed_code[3:]
            index = decompressed_code[:5]
            int_index = int(index, 2)
            decompressed_code = decompressed_code[5:]
            bitmask = '11'
            xor_value = ref_mask[:int_index] + bitmask + ref_mask[(int_index + 2):]
            dic_val = decompressed_code[:4]
            decompressed_code = decompressed_code[4:]
            ins = '{:032b}'.format(int(xor_value, 2) ^ int(dic_dict[dic_val], 2))
            decompression_output += ins

        if decompressed_code[:3] == '101':
            decompressed_code = decompressed_code[3:]
            index = decompressed_code[:5]
            int_index = int(index, 2)
            decompressed_code = decompressed_code[5:]
            bitmask = '1111'
            xor_value = ref_mask[:int_index] + bitmask + ref_mask[(int_index + 4):]
            dic_val = decompressed_code[:4]
            decompressed_code = decompressed_code[4:]
            ins = '{:032b}'.format(int(xor_value, 2) ^ int(dic_dict[dic_val], 2))
            decompression_output += ins

        if decompressed_code[:3] == '110':
            decompressed_code = decompressed_code[3:]
            index = decompressed_code[:5]
            int_index = int(index, 2)
            decompressed_code = decompressed_code[5:]
            index2 = int(decompressed_code[:5], 2)
            decompressed_code = decompressed_code[5:]
            bitmask = '1'
            xor_value = ref_mask[:int_index] + bitmask + ref_mask[(int_index + 1):index2] + bitmask + ref_mask[
                                                                                                      (index2 + 1):]
            dic_val = decompressed_code[:4]
            decompressed_code = decompressed_code[4:]
            ins = '{:032b}'.format(int(xor_value, 2) ^ int(dic_dict[dic_val], 2))
            decompression_output += ins
    create_decompressed_file()

else:
    print("Pass 1 for compression or 2 for decompression")
