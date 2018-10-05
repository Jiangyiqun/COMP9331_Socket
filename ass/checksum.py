class Checksum():
    # Usage: 
    # checksum = checksumcalculate_checksum(msg)
    #   msg: bytes type
    #   checksum: bytes type
    # 
    # bool = validate_checksum(msg)
    #   msg: bytes type
    #   bool: True or False
    #
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
        # print(checksum)
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
    # msg = bytes.fromhex('4500003044224000800600008c7c19acae241e2b')
    msg = b'\x00%PDF-1.3\r\n%\xe2\xe3\xcf\xd3\r\n\r\n1 0 obj\r\n<<\r\n/Type /Catalog\r\n/Outlines 2 0 R\r\n/Pages 3 0 R\r\n>>\r\nendobj\r\n\r\n2 0 obj\r\n<<\r\n/Type /Outlines\r\n/Count 0\r\n>>\r\nendobj\r\n\r\n3 0 obj\r\n<<\r\n/Type /Pages\r\n/Count 2\r\n/Kids [ 4 0 R 6 0 R ] \r\n>>\r\nendobj\r\n\r\n4 0 obj\r\n<<\r\n/Type /Page\r\n/Parent 3 0 R\r\n/Resources <<\r\n/Font <<\r\n/F1 9 0 R \r\n>>\r\n/ProcSet 8 0 R\r\n>>\r\n/MediaBox [0 0 612.0000 792.0000]\r\n/Contents 5 0 R\r\n>>\r\nendobj\r\n\r\n5 0 obj\r\n<</Length 1074 >>\r\nstream\r\n2 J\r\nBT\r\n0 0 0 rg\r\n/F1 0027 Tf\r\n57.3750 722.2800 Td\r\n( A Simple PDF File ) Tj\r\nET\r\nBT'
    checksum = Checksum.calculate_checksum(msg)
    # print("checksum =", checksum[0], checksum[1])
    msg_with_checksum = msg + checksum
    if (Checksum.validate_checksum(msg_with_checksum)):
        print("checksum is valid!")