# Hashmatch
## Challenge overview
This is a PWN challenge using ROP.
When run, it appears as though you have to reverse an MD5 to get a flag.
This is a fake flag however, which is unobfuscated in the binary. 
In reality, you need to overflow the input buffer to get execution and find the contents of flag.txt.

## Deployment
This challenge can be run via docker, so deployment should be easy.
First, change the content of `flag.txt` in the main directory from `flag{replace_with_real_flag}` to whatever the flag should be.
Then, run `build.sh` to compile the challenge, zip the challenge files meant to be provided to participants, and make a `run` directory for actual deployment.
The `run` directory is meant to be overwritten every time you rebuild so don't put permanent changes in there.
To start the challenge, run `docker run -p 5000:5000 --privileged $(docker build -q .)` in the `run` directory
(feel free to change the port as desired).

Provide participants with the generated `hashmatch.zip`.
There doesn't need to be any hints in the description, so feel free to make it whatever you want, or use this one:
"This server is asking me to reverse a hash for a flag, but brute forcing MD5 sounds tedious. Maybe there's something more... fun we can do to find the flag."

This challenge is a medium-difficult challenge, but can be made a fair bit easier (medium) by providing the source code (just copy it into the hashmatch directory).
The flag in the source is fake, so there's no issue providing it.
The hints from having the source code would be the overflow should be easy to spot and
seeing the ASM gadgets pre-compile will help build the chain.
I did name the `mov` gadget so it's easier to find since automatic ROP tools won't find it.

## Challenge Details
As mentioned above, this challenge supposedly wants the user to reverse an MD5, but that's not actually the purpose of the challenge.
The flag provided from succeeding in this task is fake (obviously so) and easily recovered from the binary.

The real challenge is to exploit a simple buffer overflow in the game function.
The input buffer is `1000` long, but the fgets maxes out at `0x1000` bytes, which is far longer.
This simple overflow should be easy to exploit, but some pieces of a final exploit are missing.

The binary is compiled without pie, so building a ROP chain should be easy. 
However, since it's dynamically compiled and ASLR is still on, the only easy gadgets are in the binary itself - 
no easy access to libc gadgets / strings.
This is why there are a couple of gadgets added before the other functions, these will be necessary to building the chain.

So once we overflows the buffer, we have access to the entire binary for ROP.
The ultimate goal is to run `system` with `/bin/sh`.
The `system` call is easy since we have a reference to it in the binary, but we don't have a good command string.
We could use the `add_char_to_string` function to build the string if we can pass it the right args.
We need to put the destination in `rdi` and the character into `sil`, which is the bottom eight bits of `rsi`.
We can use the first gadget to set `rdi`, but we don't appear to have an easy way to set `rsi`. 
The other gadget would let us move `rax` into `rsi`, but we also don't have a way to set `rax`.
Of course, `rax` is the return register, so if we could manipulate a function into returning what we want, we could use it to also set `rsi`.

Hopefully the only function we can manipulate the output of is `rand()`, which we can manipulate by seeding the prng. 
So the solution is to set `rdi` for `srand()`, then call `rand()`, move the output in `rax` to `rsi`, set `rdi` to writable memory, 
and finally call `add_char_to_string()` to write that character to memory.
Repeat this for all characters in "/bin/sh", then pass the address to `system` and win.

This of course will require knowing what seeds to use in order to get `rand()` to output what you want.
Since it only requires the bottom byte to be right, this is easy to brute force.

Solve scripts are available in the solve directory:
`generate_seeds` will brute force the necessary seeds and 
`solve.py` will solve the challenge, dropping you in the shell.
