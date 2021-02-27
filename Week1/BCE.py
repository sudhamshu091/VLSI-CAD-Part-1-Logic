import sys
import pcn
import urp
import os


class BCE(object):
    def __init__(self, pathin, pathout):
        self.pathin = pathin
        self.pathout = pathout
        self.eqs = {}
        self.op = {"r": self.read_pcn, "!": self.logic_not, "+": "+": self.logic_or,"&": self.logic_and,"p": self.write_pcn, "q": self.quit}
        self.done = False

    def read_pcn(self, fnum):
        _, self.eqs[fnum] = pcn.parse(os.path.join(self.pathin, fnum + ".pcn"))

    def write_pcn(self, fnum):
        with open(os.path.join(self.pathout, fnum + ".pcn"), "w") as f:
            pcn.write(f, None, self.eqs[fnum])

    def logic_not(self, resultnum, innum):
        self.eqs[resultnum] = urp.complement(self.eqs[innum])

    def logic_or(self, resultnum, leftnum, rightnum):
        self.eqs[resultnum] = urp.cubes_or(self.eqs[leftnum], self.eqs[rightnum])

    def logic_and(self, resultNnum, leftnum, rightnum):
        self.eqs[resultNum] = urp.cubes_and(self.eqs[leftnum], self.eqs[rightnum])

    def quit(self):
        self.done = True

    def proc(self, commandfilepath):
        with open(commandfilepath, "r") as f:
            for i in f:
                command, *args = line.split()
                self.operations[command](*args)

                if self.done:
                    return

Usage = """\
USAGE = {} COMMAND_FILE
"""
if __name__ == "__main__":
    if len(sys.argv) > 1:
        soldirec = "BCESolutions"
        SolDir = os.path.join(soldirec, sys.argv[1][-5])
        try:
            os.mkdir()
        except OSError:
            pass

        bce = BCE("BooleanCalculatorEngine", SolDir)
        bce.process(sys.argv[1])
    else:
        print(Usage.format(sys.argv[0]))
