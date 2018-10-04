#!/usr/bin/python3
# acknowlegement:
#   the test cases comes from
#   http://www.roman10.net/2011/11/27/how-to-calculate-iptcpudp-checksumpart-1-theory/
#


class Checksum():
    @staticmethod
    def sum_up(msg):
        word_sum = 0
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

    @staticmethod
    def fold_up(msg):
        folded_word = msg
        # print("folded_word =", hex(folded_word))
        # fold the result into 16 bits by adding the carry to the result
        while(folded_word > 0xFFFF):
            carry = folded_word // 0x10000
            remainder = folded_word % 0x10000
            folded_word = remainder + carry
            # print("carry = ", hex(carry))
            # print("remaider = ", hex(remainder))
        return folded_word

    @staticmethod
    def ones_complement(msg): 
        complement = msg ^ 0xFFFF
        return complement

    @staticmethod
    def word_to_bytes(word):
        left = word // 0x100
        right = word % 0x100
        return bytes([left, right])

    @staticmethod
    def calculate_checksum(msg):
        word_sum = Checksum.sum_up(msg)
        # print("word_sum =", hex(word_sum))
        folded_word = Checksum.fold_up(word_sum)
        # print("folded_word =", hex(folded_word))
        complement = Checksum.ones_complement(folded_word)
        # print("complement =", hex(complement))
        checksum = Checksum.word_to_bytes(complement)
        return checksum

    @staticmethod
    def validate_checksum(msg):
        word_sum = Checksum.sum_up(msg)
        folded_word = Checksum.fold_up(word_sum)
        if (folded_word == 0xFFFF):
            return True
        else:
            return False


if __name__ == '__main__':
    msg = bytes.fromhex('4500003044224000800600008c7c19acae241e2b')
    checksum = Checksum.calculate_checksum(msg)
    print("checksum =", hex(checksum[0]), hex(checksum[1]))
    msg_with_checksum = checksum + msg
    if (Checksum.validate_checksum(msg_with_checksum)):
        print("checksum is valid!")