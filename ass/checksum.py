#!/usr/bin/python3
# acknowlegement:
#   the test cases comes from
#   http://www.roman10.net/2011/11/27/how-to-calculate-iptcpudp-checksumpart-1-theory/
#   the calculation modified from
#   http://www.bitforestinfo.com/2018/01/python-codes-to-calculate-tcp-checksum.html
#

# class Checksum()


def get_checksum(msg):

    s = 0       # Binary Sum
    # loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
        if (i+1) < len(msg):
            a = msg[i]
            b = msg[i+1]
            s = s + (a+(b << 8))
        elif (i+1)==len(msg):
            s += msg[i]
        else:
            raise "Something Wrong here"
    # One's Complement
    s = s + (s >> 16)
    s = ~s & 0xffff
    high = s // 256
    low = s % 256
    return high, low


def sum_up(msg):
    word_sum = 0       # Binary Sum
    # calculate sum
    for i in range(0, len(msg), 2):
        if (i+1) < len(msg):
            left = msg[i]
            right = msg[i+1]
            word = (left << 8) + right
            word_sum += word
        elif (i+1)==len(msg):
            left = msg[i]
            word_sum += left
        else:
            raise "Checksum could not be calculated!"
    return word_sum


def fold_up(msg):
    folded_word = msg
    print("folded_word =", hex(folded_word))
    # fold the result into 16 bits by adding the carry to the result
    while(folded_word > 0xFFFF):
        carry = folded_word // 0xFFFF
        remainder = folded_word % 0xFFFF
        folded_word = remainder + carry

        print("carry = ", hex(carry))
        print("remaider = ", hex(remainder))
    return folded_word



def calculate_checksum(msg):
    word_sum = sum_up(msg)
    print(hex(word_sum))
    folded_word = fold_up(word_sum)
    print(hex(folded_word))
    # One's Complement
    # s = s + (s >> 16)
    # s = ~s & 0xffff
    # high = s // 256
    # low = s % 256
    # return high, low




if __name__ == '__main__':
    a = '4500003044224000800600008c7c19acae241e2b'
    print(a)
    b = bytes.fromhex(a)
    print(b)
    calculate_checksum(b)
    # print(c)