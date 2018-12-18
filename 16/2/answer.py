import re


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


def get_samples(input_file):
    samples = []
    count = 0
    for line in input_file:
        count += 1
        if count == 1:
            if line == '\n':
                return samples
            sample = {}
            match = re.match(
                r'Before: \[([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+)\]',
                line)
            before = [
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3)),
                int(match.group(4))]
            sample['before'] = before
        elif count == 2:
            match = re.match(
                r'([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)',
                line)
            opcode = [
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3)),
                int(match.group(4))]
            sample['opcode'] = opcode
        elif count == 3:
            match = re.match(
                r'After:  \[([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+)\]',
                line)
            after = [
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3)),
                int(match.group(4))]
            sample['after'] = after
        elif count == 4:
            count = 0
            samples.append(sample)
    return samples


def get_tests(input_file):
    tests = []
    for line in input_file:
        test = list(map(int, line.split(' ')))
        tests.append(test)
    return tests


def main():

    with open('inputs\\input16.txt') as input_file:
        samples = get_samples(input_file)
        input_file.readline()
        tests = get_tests(input_file)

    opcode_functions = {name: function for name,
                        function in Opcodes.__dict__.items() if not name.startswith('_')}

    opcode_mapping = {}
    for sample in samples:
        for function in opcode_functions.values():
            opcode_number, opcode_a, opcode_b, opcode_c = sample['opcode']
            last_function = function.__func__
            result = last_function(
                opcode_a,
                opcode_b,
                opcode_c,
                sample['before'])
            if result == sample['after']:
                opcode_mapping[opcode_number] = opcode_mapping.get(
                    opcode_number, set())
                opcode_mapping[opcode_number].add(last_function)

    opcodes_final = {}
    known_functions = set()
    while len(known_functions) < 16:
        for opcode_number, functions_set in opcode_mapping.items():
            difference: set = functions_set - known_functions

            if len(difference) == 1:
                final_function = difference.pop()
                opcodes_final[opcode_number] = final_function
                known_functions.add(final_function)

    registers = [0, 0, 0, 0]
    for test in tests:
        opcode_number, opcode_a, opcode_b, opcode_c = test
        registers = opcodes_final[opcode_number](
            opcode_a, opcode_b, opcode_c, registers)

    print(registers)


if __name__ == "__main__":
    main()
