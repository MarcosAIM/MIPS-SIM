import json
import os
from pathlib import Path


class Index:
    absolute_path = None
    OpCode = {"j": 2,
              "beq": 4,
              "add": 0,
              "addi": 8,
              "sub": 0,
              "sw": 43,
              "lw": 35,
              "sll": 0,
              "srl": 0,
              "mul": 28,
              "and": 0,
              "or": 0,
              "nop": 0}

    Function = {"j": None,
                "beq": None,
                "add": 32,
                "addi": None,
                "sub": 34,
                "sw": None,
                "lw": None,
                "sll": 0,
                "srl": 2,
                "mul": 2,
                "and": 36,
                "or": 37,
                "nop": 0}

    Registers = {"$0": 0,
                 "$at": 1,
                 "$v0": 2,
                 "$v1": 3,
                 "$a0": 4,
                 "$a1": 5,
                 "$a2": 6,
                 "$a3": 7,
                 "$t0": 8,
                 "$t1": 9,
                 "$t2": 10,
                 "$t3": 11,
                 "$t4": 12,
                 "$t5": 13,
                 "$t6": 14,
                 "$t7": 15,
                 "$s0": 16,
                 "$s1": 17,
                 "$s2": 18,
                 "$s3": 19,
                 "$s4": 20,
                 "$s5": 21,
                 "$s6": 22,
                 "$s7": 23,
                 "$t8": 24,
                 "$t9": 25,
                 "$k0": 26,
                 "$k1": 27,
                 "$gp": 28,
                 "$sp": 29,
                 "$fp": 30,
                 "$ra": 31
                 }
    KeyWords = {"OpCode": OpCode, "Function": Function, "Registers": Registers}

    file_name = "../Index.json"

    @staticmethod
    def create_index():
        try:
            with open(Index.file_name, "w") as write:
                json.dump(Index.KeyWords, write)
                Index.absolute_path = Path(Index.file_name).resolve()
        except FileExistsError:
            "<ERROR: FILE EXISTS>"
            return

    @staticmethod
    def destroy_index():
        try:
            os.remove(Index.file_name)
        except FileNotFoundError:
            return
