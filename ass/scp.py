import time

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



class ScpPackage():
    # scp package abstraction
    def __init__(self, package=None):
        # initialize the segment
        self.sequence = bytes([0])
        self.acknowledge = bytes([0])
        self.flag = bytes([0])
        self.window = bytes([0])
        self.checksum = bytes([0, 0])
        # the data flow
        self.header = self.sequence\
                    + self.acknowledge\
                    + self.flag\
                    + self.window\
                    + self.checksum
        self.payload = bytes()
        self.package = self.header + self.payload
        # the flags
        self.ack = False
        self.syn = False
        self.fin = False
        # extract from package
        if (package):
            self.extract_package(package)

    def extract_package(self, package):
        self.package = package
        self.sequence = self.package[0:1]
        self.acknowledge = self.package[1:2]
        self.flag = self.package[2:3]
        self.window = self.package[3:4]
        self.checksum = self.package[4:6]
        self.header = self.package[0:6]
        self.payload = self.package[6:]
        self.extract_flag()

    def extract_flag(self):
        if (self.flag[0] & (1<<4)):
            self.ack = True
        else:
            self.ack = False

        if (self.flag[0] & (1<<1)):
            self.syn = True
        else:
            self.syn = False

        if (self.flag[0] & (1<<0)):
            self.fin = True
        else:
            self.fin = False

    def make_flag(self):
        flag = 0
        if (self.ack):
            flag |= (1<<4)
        if (self.syn):
            flag |= (1<<1)
        if (self.fin):
            flag |= (1<<0)
        self.flag = bytes([flag])

    def make_package(self):
        self.make_flag()
        header_without_checksum = self.sequence\
                                + self.acknowledge\
                                + self.flag\
                                + self.window
        self.checksum = Checksum.calculate_checksum(\
                        header_without_checksum\
                        + self.payload)
        self.header = header_without_checksum + self.checksum
        self.package = self.header + self.payload

    def validate_package(self):
        return Checksum.validate_checksum(self.package)

    def flip_sequence(self):
        if (self.sequence == bytes([0])):
            self.sequence = bytes([1])
        elif (self.sequence == bytes([1])):
            self.sequence = bytes([0])
        else:
            raise "Bad sequence number!"

    def print_package(self):
        print("sequence: ", self.sequence[0])
        print("acknowledge: ", self.acknowledge[0])
        print("flag: ", self.flag[0])
        print("window: ", self.window[0])
        print("checksum: ", self.checksum[0], self.checksum[1])
        print("length of header: ", len(self.header))
        print("length of payload: ", len(self.payload))
        print("length of package: ", len(self.package))
        print("ack: ", self.ack)
        print("syn: ", self.syn)
        print("fin: ", self.fin)

    def checksum_str(self):
        return str(self.checksum[0]) + " " + str(self.checksum[1])


class ScpLogger():
# event time ack-number type-of-packet seq-number number-of-bytes-data
    def __init__(self, log_file):
        self.log_file = log_file
        self.start_time = time.time()
        # create log_file, wirte title to it
        title = '{:10}{:>5}{:>10}{:>10}{:>10}{:>10}{:>10}\n'.format(\
                "event", "time", "ack",\
                "flag", "seq", "size", "checksum")
        with open(self.log_file, 'w+') as fd:
            fd.write(title)


    def log(self, event, scp_package):
        # generate time
        event_time = '{:.2f}'.format(time.time() - self.start_time)
        # generate flag
        flag = ''
        if (scp_package.ack):
            if (flag):
                flag += '/'
            flag += 'A'
        if (scp_package.fin):
            if (flag):
                flag += '/'
            flag += 'F'
        if (scp_package.syn):
            if (flag):
                flag += '/'
            flag += 'S'
        if (not flag):
            flag = 'D'
        # generate line
        line = '{:10}{:>5}{:>10}{:>10}{:>10}{:>10}{:>10}\n'.format(\
                event, event_time, scp_package.acknowledge[0],\
                flag, scp_package.sequence[0],\
                len(scp_package.payload),\
                scp_package.checksum_str())
        # write line to log
        with open(self.log_file, 'a') as fd:
            fd.write(line)




if __name__ == '__main__':
    # test checksum
    # msg = bytes.fromhex('4500003044224000800600008c7c19acae241e2b')
    # checksum = Checksum.calculate_checksum(msg)
    # print("checksum =", checksum[0], checksum[1])
    # msg_with_checksum = msg + checksum
    # if (Checksum.validate_checksum(msg_with_checksum)):
    #     print("checksum is valid!")

    # test package
    data = b'123456abcdef'
    package = ScpPackage(data)
    package.print_package()
    # print(package.checksum_str())
    # package.fin = False
    # package.make_flag()
    # package.print_package()


    # test scplogger
    logger = ScpLogger("log.txt")
    time.sleep(0.5)
    logger.log("send", package)