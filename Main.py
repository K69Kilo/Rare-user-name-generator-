# language: Python 3.8+, file: namegen.py, target: Windows cmd
# just a quick name thing i threw together, works fine

import random
import os
from datetime import datetime

# colors so it doesnt look boring
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"

# the big slimey title
TITLE = r"""
 ███╗   ██╗ █████╗ ███╗   ███╗███████╗     ██████╗ ███████╗███╗   ██╗
 ████╗  ██║██╔══██╗████╗ ████║██╔════╝    ██╔════╝ ██╔════╝████╗  ██║
 ██╔██╗ ██║███████║██╔████╔██║█████╗      ██║  ███╗█████╗  ██╔██╗ ██║
 ██║╚██╗██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║██╔══╝  ██║╚██╗██║
 ██║ ╚████║██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝███████╗██║ ╚████║
 ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝
"""

# word lists i scraped / made up over time
PREFIX = [
    "aether", "luna", "nova", "vex", "kyo", "zen", "ryu", "kai", "sol", "nyx",
    "echo", "void", "ash", "frost", "ember", "shade", "silk", "mist", "glow",
    "pixel", "neon", "ghost", "quiet", "soft", "pale", "dim", "faint", "hush",
    "cryo", "orbit", "null", "flux", "veil", "rift", "haze", "wisp", "bloom",
    "drip", "slime", "goo", "muck", "ooze"
]
SUFFIX = [
    "lynx", "fox", "owl", "crow", "wisp", "bloom", "veil", "rift", "core",
    "byte", "pulse", "wave", "drift", "haze", "spark", "dust", "tide", "root",
    "node", "flux", "arc", "orbit", "shade", "veil", "mist", "glow", "hush",
    "zero", "nine", "x", "z", "q", "v", "slime", "drip"
]
MID = list("xzvqykjnrl")
NUMS = ["", "7", "9", "11", "13", "21", "42", "77", "99", "00", "x", "z"]

TAKEN_FILE = "taken_names.txt"

def load_taken():
    if not os.path.exists(TAKEN_FILE):
        # first run, just make an empty one
        open(TAKEN_FILE, "w").close()
        return set()
    with open(TAKEN_FILE, "r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}

def save_taken(taken):
    with open(TAKEN_FILE, "w", encoding="utf-8") as f:
        for name in sorted(taken):
            f.write(name + "\n")

def soft():
    return f"{random.choice(PREFIX)}{random.choice(MID)}{random.choice(SUFFIX)}"

def short():
    length = random.randint(3, 5)
    vowels = "aeiouy"
    cons = "bcdfghjklmnpqrstvwxz"
    name = ""
    for i in range(length):
        name += random.choice(vowels if i % 2 else cons)
    return name

def leet():
    return f"{random.choice(PREFIX + SUFFIX)}{random.choice(NUMS)}"

def double():
    return f"{random.choice(PREFIX)}{random.choice(SUFFIX)}"

def make_name():
    # just pick one of the styles at random
    return random.choice([soft, short, leet, double])()

def main():
    # clear screen a bit so the title looks clean
    os.system("cls" if os.name == "nt" else "clear")

    print(CYAN + TITLE + RESET)
    print(f"{YELLOW}  local name check  ·  green = free  ·  red = taken{RESET}")
    print(f"{YELLOW}  ctrl+c when you got enough{RESET}\n")

    taken = load_taken()
    print(f"loaded {len(taken)} taken names from {TAKEN_FILE}\n")

    available = []
    tried = 0

    try:
        while True:
            name = make_name()
            tried += 1
            low = name.lower()

            if low in taken:
                print(f"{RED}TAKEN     {name}{RESET}")
            else:
                print(f"{GREEN}AVAILABLE {name}{RESET}")
                available.append(name)

            if tried % 40 == 0:
                print(f"{YELLOW}--- checked {tried} | found {len(available)} free ---{RESET}")

    except KeyboardInterrupt:
        print(f"\n{YELLOW}stopped.{RESET}")
        print(f"checked {tried} names")
        print(f"got {len(available)} available ones\n")

        if available:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            out = f"available_{stamp}.txt"
            with open(out, "w", encoding="utf-8") as f:
                f.write("AVAILABLE NAMES\n")
                f.write(f"made on {datetime.now()}\n")
                f.write("-" * 36 + "\n")
                for n in available:
                    f.write(n + "\n")
            print(f"dumped the free ones → {out}")
            print("open it in notepad whenever\n")

        claim = input("wanna mark some as taken so they dont show again? (y/n): ").strip().lower()
        if claim == "y":
            print("type the names one by one, empty line when done:")
            while True:
                line = input("> ").strip()
                if not line:
                    break
                taken.add(line.lower())
            save_taken(taken)
            print(f"updated {TAKEN_FILE}")
        print("later.")

if __name__ == "__main__":
    main()
