input = "!entry Panda Fking Gods Win"

args = input.split()
if args[-1] in ["Lose", "lose"]:
    # then update worksheet cell with "Lose"
    print()
if args[-1] in ["Win", "win"]:
    # then update worksheet cell with "Win"
    print()

for liste in args[1:-1]:
    print(liste)

text = "path/dah\\doo/abc.def.ghi.png"
import re

file = re.split('[\\/]', text)[-1]
name = ".".join(file.split('.')[:-1])
