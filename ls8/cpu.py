"""CPU functionality."""

import sys

 #create instructions for LDI, PRN, and HLT programs
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101 #added pus, pop and sp
POP = 0b01000110
SP = 7 #stack pointer

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #setup ram,register and pc
        self.ram = [0] * 256 
        self.reg = [0] * 8
        self.pc = 0
        self.halted = False
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
        #register 7 is reserved as the stack pointer, which is 0xf4 per specs
        self.reg[SP] = 0xf4
        

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr
        
    
    def load(self, filename):
        """Load a program into memory."""

        
    #     program = sys.argv[1]

    #     address = 0 #pointer to currently executing instruction

    #     # For now, we've just hardcoded a program:

    #     # program = [
    #     #     # From print8.ls8
    #     #     0b10000010, # LDI R0,8
    #     #     0b00000000,
    #     #     0b00001000,
    #     #     0b01000111, # PRN R0
    #     #     0b00000000,
    #     #     0b00000001, # HLT
    #     # ]



        try:
            address = 0
            #open file
            with open(filename) as f:
                #read the lines
                for line in f:
                    # split line before and after comment symbol
                    comment_split = line.split("#")

                    # extract our number
                    num = comment_split[0].strip() # trim whitespace

                    # ignore blank lines
                    if num == '':
                        continue 

                    # convert our binary string to a number
                    val = int(num, 2)

                    # store val at address in memory
                    self.ram_write(val, address)

                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b] 
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def handle_ldi(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        self.reg[operand_a] = operand_b

    def handle_prn(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.reg[operand_a])

    def handle_hlt(self):
        self.halted = True

    def handle_mul(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("MUL", operand_a, operand_b)

      #method to handle push on the stack
    def handle_push(self):
        #decrement the SP register
        self.reg[SP] -= 1
        #set operand_a
        operand_a = self.ram_read(self.pc + 1)
        # copy the value in the given register to the address pointed to by SP
        operand_b = self.reg[operand_a]
        self.ram[self.reg[SP]] = operand_b


     #method to handle popping from the stack to the register
    def handle_pop(self):
        operand_a = self.ram_read(self.pc + 1)
        # copy the value from the address pointed to by SP to the given reg
        operand_b = self.ram[self.reg[SP]]
        self.reg[operand_a] = operand_b
        #increment the SP
        self.reg[SP] += 1  
     

    def run(self):
        while self.halted is False:
            IR = self.ram[self.pc]
            val = IR
            op_count = val >> 6
            IR_length = op_count + 1
            self.branchtable[IR]()

            if IR == 0 or None:
                print(f"Unknown instructions and index {self.pc}")
                sys.exit(1)
            self.pc += IR_length    

 
    # def run(self):
    #     """Run the CPU."""
       
    #     #set running to True
    #     running = True
        
    #     #while cpu is running
    #     while running:
    #         #  set instruction register per step 3
    #         IR = self.ram[self.pc]

    #         # set operand_a to pc+1 per step 3
    #         operand_a = self.ram_read(self.pc + 1)
    #         # set operand_b to pc+2 per step 3
    #         operand_b = self.ram_read(self.pc + 2)

    #         # if the instruction register is LDI
    #         if IR == LDI:
    #             #set register of operand_a to operand_b, jump 3 in PC (to PRN currently)
    #             self.reg[operand_a] = operand_b
    #             self.pc +=3
    #         # if the instruction register is PRN
    #         elif IR == PRN:
    #             #print the register of operand_a, jump 2 in PC
    #             print(self.reg[operand_a])
    #             self.pc +=2
    #         # if the instruction register is the halt command
    #         elif IR == HLT:
    #             #set running to false and exit
    #             running = False
    #             sys.exit(0)
    #         # if anything else, invalid command and quit with failure code 1
    #         else:
    #             print(f"Invalid Command: {self.ram[self.pc]}")
    #             sys.exit(1)

  