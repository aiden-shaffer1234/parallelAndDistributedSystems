import random as rand
import time

initial_permutation = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

final_permutation = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

expansion_permutation = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

permutation = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

permutation_choice_2 = [
    14, 17, 11, 24, 1, 5, 3, 28,
    15, 6, 21, 10, 23, 19, 12, 4,
    26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56,
    34, 53, 46, 42, 50, 36, 29, 32
]

s_box_1 = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
]




def encrypt(str, key):

    # pad with 0 to make length multiple of 8
    pad = 0
    if(len(str)%8==0): 
        pad = 0
    else:
        pad = 8 - (len(str) % 8) 
    for _ in range(pad):
        str = str + '0'
    
    ans = ""
    for x in range(int(len(str)/8)):
        str_section = str[x:(x+1)*8] #isolate 8 chars
        int_section = convert_int(str_section) #convert to 64 bit
        cypher = des(int_section, key, True) 
        ans = convert_str(cypher) + ans 

    return [ans, pad]

def decrypt(str, key, pad):
    ans = ""
    for x in range(int(len(str)/8)):
        str_section = str[x:(x+1)*8]
        int_section = convert_int(str_section)
        plain = des(int_section, key, False)
        ans = convert_str(plain) + ans
    
    ans = ans[:-pad] #strip the padding we added
    return ans
def convert_int(string):
    section = 0
    for c in string:
        section = (section << 8) | ord(c)
    
    return section

def convert_str(num):
    section = 0
    ans = ""
    for i in range(8):
        section = (num >> (i * 8)) & 0xFF
        ans = chr(section) + ans
    
    return ans


def expand(num):
    return perm(expansion_permutation, 48, num)

    
def sbox_shrink(num):
    test = 0
    for i in range (0,48,6):
        section = (num >> (42 - i)) & 0x3F
        row = (((0 | (section >> 5)) & 1) << 1) | (section & 1) 
        col = (section >> 1) & 0xF
        number = s_box_1[row][col]
        test = (test << 4) | number
        

    return test

def perm_shuffle(num):
    return perm(permutation, 32, num)


def round_key(key):
    return perm(permutation_choice_2, 56, key)

def perm(perm_list, num_bits, num):
    counter = 0
    ans = 0
    for p in perm_list:
        bit = (num >> (num_bits - p)) & 1
        ans = ans | (bit << (num_bits - counter - 1))
        counter += 1
    return ans

def des(num, key, encrypt):
    num = perm(initial_permutation, 64, num)
    for i in range(16):
        
        #cyclic shifts based on encrypt or decrypt
        if encrypt:
            front_bit = (key >> 55) & 1
            key = (key << 1) | front_bit
            r_key = round_key(key)

        else:
            r_key = round_key(key)
            back_bit = key & 1
            key = (key >> 1) | (back_bit << 55)
        
#        r_key = round_key(key)

        #isolate the halves
        left = num >> 32
        right = num & 0XFFFFFFFF
        old_right = right

        # 4 main actions
        right = expand(right)
        right = right ^ r_key
        right = sbox_shrink(right)
        right = perm_shuffle(right)

        #final xor and combine
        right = right ^ left
        left = old_right
        num = (left << 32) | right

    # flip the num left and right half
    left = num >> 32 
    right = num & 0XFFFFFFFFF
    old_right = right
    right = left
    left = old_right
    num = ((left & 0xFFFFFFFF) << 32) | right

    #final permutation didnt check
    num = perm(final_permutation, 64, num)

    return num




if __name__ == "__main__":
    
    
    plaintext = input("Enter text to encrypt (\"Exit\" to quit):")
    while plaintext != "Exit":
        # seed with time 
        rand.seed(time.time())
        key = rand.getrandbits(56)
        encrypted = encrypt(plaintext, key)

        print("Encrypted text: '", encrypted[0], "'")
        pad = encrypted[1]
        # #pass in diff key
        for _ in range(16):
            front_bit = key >> 55
            key = (key << 1) | front_bit
            
        decrypted = decrypt(encrypted[0],key, pad)
        print("Decrypted text: '", decrypted, "'")
        plaintext = input("Next text (\"Exit\" to quit):  ")

    