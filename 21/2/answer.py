class Opcodes:

    # Addition:

    @staticmethod
    def addr(register_a, register_b, register_c, registers):
        '''addr (add register)
        stores into register C the result of adding register A and register B.'''
        result = registers[:]
        result[register_c] = result[register_a] + result[register_b]
        return result

    @staticmethod
    def addi(register_a, value_b, register_c, registers):
        '''addi (add immediate)
        stores into register C the result of adding register A and value B.'''
        result = registers[:]
        result[register_c] = result[register_a] + value_b
        return result

    # Multiplication:

    @staticmethod
    def mulr(register_a, register_b, register_c, registers):
        '''mulr (multiply register)
        stores into register C the result of multiplying register A and register B.'''
        result = registers[:]
        result[register_c] = result[register_a] * result[register_b]
        return result

    @staticmethod
    def muli(register_a, value_b, register_c, registers):
        '''muli (multiply immediate)
        stores into register C the result of multiplying register A and value B.'''
        result = registers[:]
        result[register_c] = result[register_a] * value_b
        return result

    # Bitwise AND:

    @staticmethod
    def banr(register_a, register_b, register_c, registers):
        '''banr (bitwise AND register)
        stores into register C the result of the bitwise AND of register A and register B.'''
        result = registers[:]
        result[register_c] = result[register_a] & result[register_b]
        return result

    @staticmethod
    def bani(register_a, value_b, register_c, registers):
        '''bani (bitwise AND immediate)
        stores into register C the result of the bitwise AND of register A and value B.'''
        result = registers[:]
        result[register_c] = result[register_a] & value_b
        return result

    # Bitwise OR:

    @staticmethod
    def borr(register_a, register_b, register_c, registers):
        '''borr (bitwise OR register)
        stores into register C the result of the bitwise OR of register A and register B.'''
        result = registers[:]
        result[register_c] = result[register_a] | result[register_b]
        return result

    @staticmethod
    def bori(register_a, value_b, register_c, registers):
        '''bori (bitwise OR immediate)
        stores into register C the result of the bitwise OR of register A and value B.'''
        result = registers[:]
        result[register_c] = result[register_a] | value_b
        return result

    # Assignment:

    @staticmethod
    def setr(register_a, _register_b, register_c, registers):
        '''setr (set register)
        copies the contents of register A into register C. (Input B is ignored.)'''
        result = registers[:]
        result[register_c] = result[register_a]
        return result

    @staticmethod
    def seti(value_a, _register_b, register_c, registers):
        '''seti (set immediate)
        stores value A into register C. (Input B is ignored.)'''
        result = registers[:]
        result[register_c] = value_a
        return result

    # Greater-than testing:

    @staticmethod
    def gtir(value_a, register_b, register_c, registers):
        '''gtir (greater-than immediate/register)
        sets register C to 1 if value A is greater than register B.
        Otherwise, register C is set to 0.'''
        result = registers[:]
        result[register_c] = int(value_a > result[register_b])
        return result

    @staticmethod
    def gtri(register_a, value_b, register_c, registers):
        '''gtri (greater-than register/immediate)
        sets register C to 1 if register A is greater than value B.
        Otherwise, register C is set to 0.'''
        result = registers[:]
        result[register_c] = int(result[register_a] > value_b)
        return result

    @staticmethod
    def gtrr(register_a, register_b, register_c, registers):
        '''gtrr (greater-than register/register)
        sets register C to 1 if register A is greater than register B.
        Otherwise, register C is set to 0.'''
        result = registers[:]
        result[register_c] = int(
            result[register_a] > result[register_b])
        return result

    # Equality testing:

    @staticmethod
    def eqir(value_a, register_b, register_c, registers):
        '''eqir (equal immediate/register)
        sets register C to 1 if value A is equal to register B.
        Otherwise, register C is set to 0.'''
        result = registers[:]
        result[register_c] = int(value_a == result[register_b])
        return result

    @staticmethod
    def eqri(register_a, value_b, register_c, registers):
        '''eqri (equal register/immediate)
        sets register C to 1 if register A is equal to value B.
        Otherwise, register C is set to 0.'''
        result = registers[:]
        result[register_c] = int(result[register_a] == value_b)
        return result

    @staticmethod
    def eqrr(register_a, register_b, register_c, registers):
        '''eqrr (equal register/register)
        sets register C to 1 if register A is equal to register B.
        Otherwise, register C is set to 0.'''
        result = registers[:]
        result[register_c] = int(
            result[register_a] == result[register_b])
        return result


def section_optimized(registers):

    registers[3] = 1
    if (registers[4] + 1) * 256 <= registers[2]:
        start_reg4 = registers[4]
        registers[4] = registers[2] // 256
        weight = (registers[4] - start_reg4) * 7 + 4
    else:
        weight = 4
    return 23, weight


def process_instructions(instruction_pointer, instructions, registers):
    pointer_value = registers[instruction_pointer]
    instruction_count = 0
    reg_5 = set()
    largest_reg_5 = 0
    largest_count = 0
    while pointer_value < len(instructions):
        instruction_count += 1
        if pointer_value == 28 and registers[5] not in reg_5:
            largest_reg_5 = registers[5]
            reg_5.add(largest_reg_5)
            largest_count = instruction_count

        if instruction_count >= 10000000000:
            print(f'Total instructions: {largest_count}')
            print(f'reg 5 value: {largest_reg_5}')
            break

        # optimize this section
        if pointer_value == 18:
            registers[instruction_pointer] = pointer_value
            # assume specific instruction pointer boundings
            pointer_value, weight = section_optimized(registers)
            instruction_count += weight

        registers[instruction_pointer] = pointer_value
        opcode, opcode_a, opcode_b, opcode_c = instructions[pointer_value]

        registers = getattr(Opcodes, opcode)(
            opcode_a, opcode_b, opcode_c, registers)

        pointer_value = registers[instruction_pointer] + 1
    return registers, pointer_value


def main():
    with open('inputs\\input21.txt') as input_file:
        instruction_pointer = int(input_file.readline().split(' ')[1])
        if instruction_pointer != 1:
            raise ValueError(
                'This part is only optimized for specific rules / bounded pointer')

        instructions = []
        for line in input_file:
            instruction: list = line.split(' ')
            instruction[1] = int(instruction[1])
            instruction[2] = int(instruction[2])
            instruction[3] = int(instruction[3])
            instructions.append(instruction)

        registers = [0, 0, 0, 0, 0, 0]
        registers, pointer_value = process_instructions(
            instruction_pointer, instructions, registers)
        print(f'Registers: {registers}\nPointer Value: {pointer_value}')


if __name__ == "__main__":
    main()
