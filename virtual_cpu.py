import struct
from flask import Flask, request, jsonify

class VirtualCPU:
    def __init__(self):
        self.registers = [0] * 8  # R0-R7
        self.memory = [0] * 256   # 256-byte memory
        self.pc = 0               # Program Counter
        self.stack = []           # Stack for function calls
        self.output = ""          # Output buffer
        self.running = True       # Execution state
    
    def load_bytecode(self, bytecode):
        self.memory[:len(bytecode)] = bytecode  # Load into memory
        self.pc = 0  # Reset program counter
    
    def fetch_byte(self):
        byte = self.memory[self.pc]
        self.pc = (self.pc + 1) % 256  # Wrap-around memory
        return byte
    
    def execute(self):
        steps = []
        while self.running:
            steps.append({"pc": self.pc, "registers": self.registers.copy()})
            opcode = self.fetch_byte()
            if opcode == 0x01:  # LOAD_CONST
                reg = self.fetch_byte()
                value = self.fetch_byte()
                self.registers[reg] = value
            elif opcode == 0x02:  # MOVE
                dest = self.fetch_byte()
                src = self.fetch_byte()
                self.registers[dest] = self.registers[src]
            elif opcode == 0x03:  # ADD
                dest = self.fetch_byte()
                src1 = self.fetch_byte()
                src2 = self.fetch_byte()
                self.registers[dest] = (self.registers[src1] + self.registers[src2]) % 256
            elif opcode == 0x04:  # SUB
                dest = self.fetch_byte()
                src1 = self.fetch_byte()
                src2 = self.fetch_byte()
                self.registers[dest] = (self.registers[src1] - self.registers[src2]) % 256
            elif opcode == 0x05:  # MUL
                dest = self.fetch_byte()
                src1 = self.fetch_byte()
                src2 = self.fetch_byte()
                self.registers[dest] = (self.registers[src1] * self.registers[src2]) % 256
            elif opcode == 0x06:  # DIV
                dest = self.fetch_byte()
                src1 = self.fetch_byte()
                src2 = self.fetch_byte()
                if self.registers[src2] == 0:
                    self.running = False
                    return {"success": False, "error": "Division by zero"}
                self.registers[dest] = (self.registers[src1] // self.registers[src2]) % 256
            elif opcode == 0x07:  # LOAD_MEM
                reg = self.fetch_byte()
                addr = self.fetch_byte()
                self.registers[reg] = self.memory[addr]
            elif opcode == 0x08:  # STORE_MEM
                addr = self.fetch_byte()
                reg = self.fetch_byte()
                self.memory[addr] = self.registers[reg]
            elif opcode == 0x09:  # JUMP
                addr = self.fetch_byte()
                self.pc = addr
            elif opcode == 0x0A:  # JUMP_IF_ZERO
                reg = self.fetch_byte()
                addr = self.fetch_byte()
                if self.registers[reg] == 0:
                    self.pc = addr
            elif opcode == 0x0B:  # JUMP_IF_NEG
                reg = self.fetch_byte()
                addr = self.fetch_byte()
                if self.registers[reg] & 0x80:
                    self.pc = addr
            elif opcode == 0x0C:  # CALL
                addr = self.fetch_byte()
                self.stack.append(self.pc)
                self.pc = addr
            elif opcode == 0x0D:  # RETURN
                if self.stack:
                    self.pc = self.stack.pop()
            elif opcode == 0x0E:  # HALT
                self.running = False
            elif opcode == 0x0F:  # PRINT
                reg = self.fetch_byte()
                self.output += str(self.registers[reg])
            else:
                self.running = False
                return {"success": False, "error": "Invalid opcode"}
        return {"success": True, "registers": self.registers, "output": self.output, "execution_steps": steps}

app = Flask(__name__)

@app.route("/execute", methods=["POST"])
def execute_program():
    data = request.get_json()
    bytecode = bytes.fromhex(data.get("bytecode", ""))
    cpu = VirtualCPU()
    cpu.load_bytecode(bytecode)
    result = cpu.execute()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
