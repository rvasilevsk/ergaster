from pathlib import Path


#######################################################################################################################
def log(*args):
    log_path = Path(__file__).parent.parent / "_test.log"
    args = " ".join(map(str, args))
    with open(log_path, "a", encoding="utf8") as f:
        f.write(args)
        f.write("\n")
