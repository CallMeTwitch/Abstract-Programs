# #########################
# SHA256 is a VERY complex 
# hashing algorithm that 
# changes any amount (or 
# in this case of to 64 
# characters) of data 
# into 256 bits. SHA256 
# is used in BitCoin, 
# and if anyone were to 
# figure out how to go 
# from hash back to the 
# original data they 
# could break the BitCoin 
# market.
#
# Code written for
# efficiency
# #########################

# Preset Constants. 3rd root of the first 64 primes and the 2rd root of the first 8 primes.
CONSTANTS = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,]
STATE_REGISTER = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]

# Return Encoded 256 bit Hash
def sha256(message):
    constants = CONSTANTS[:]

    ROTR = lambda bin, n: (((bin & 0xffffffff) >> (n & 31)) | (bin << (32 - (n & 31)))) & 0xffffffff
    SHR = lambda bin, n: (bin & 0xffffffff) >> n

    ADD = lambda lst: ('0' * (32 - len(bin(sum(lst)%(2**32))[2:]))) + bin(sum(lst)%(2**32))[2:]
    CHOOSE = lambda bin1, bin2, bin3: bin3 ^ (bin1 & (bin2 ^ bin3))
    MAJORITY = lambda bin1, bin2, bin3: ((bin1 | bin2) & bin3) | (bin1 & bin2)
    Σ0 = lambda bin: ROTR(bin, 2) ^ ROTR(bin, 13) ^ ROTR(bin, 22)
    Σ1 = lambda bin: ROTR(bin, 6) ^ ROTR(bin, 11) ^ ROTR(bin, 25)
    σ0 = lambda bin: ROTR(bin, 7) ^ ROTR(bin, 18) ^ SHR(bin, 3)
    σ1 = lambda bin: ROTR(bin, 17) ^ ROTR(bin, 19) ^ SHR(bin, 10)

    binary = ''.join(('0' *  (10 - len(bin(ord(q))))) + bin(ord(q))[2:] for q in message)
    padded = binary + ''.join(['0' if q != 0 else '1' for q in range(512 - len(binary) - (len(bin(len(binary))) - 2))] + [q for q in bin(len(binary))[2:]])

    message_schedule = [padded[q * 32:(q + 1) * 32] for q in range(16)]
    while len(message_schedule) != 64:
        message_schedule.append(ADD([σ1(int(message_schedule[-2], 2)), int(message_schedule[-7], 2), σ0(int(message_schedule[-15], 2)), int(message_schedule[-16], 2)]))

    state_register = STATE_REGISTER[:]
    for w in range(len(message_schedule)):
        t1 = ADD([Σ1(state_register[4]), CHOOSE(state_register[4], state_register[5], state_register[6]), constants[w], int(message_schedule[w], 2), state_register[7]])
        t2 = ADD([Σ0(state_register[0]), MAJORITY(state_register[0], state_register[1], state_register[2])])

        state_register.pop()
        state_register = [int(ADD([int(t1, 2), int(t2, 2)]), 2)] + state_register
        state_register[4] = int(ADD([state_register[4], int(t1, 2)]), 2)

    for q in range(len(state_register)):
        state_register[q] = ADD([state_register[q], STATE_REGISTER[q]])

    return ''.join(list(map(lambda x:('0'*(8-len(x)))+x, [hex(int(''.join(list(map(str, list(q)))), 2))[2:] for q in state_register])))

# Print Hash
print(sha256(input('Original Message: ')))