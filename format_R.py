import json
import subprocess
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(description="Format an R notebook.")
parser.add_argument(
    "filename", metavar="filename", help="enter the filename of the jupyter notebook"
)
args = parser.parse_args()

with open(args.filename, "r") as f:
    json_data = json.load(f)

bash_command = "Rscript cli_formatR.r tmp_file.r"
for cell in tqdm(json_data["cells"]):
    # Check if cell contains cod
    if cell["cell_type"] == "code":
        # Remove all magic lines (would be good to find a way to reinsert them)
        source = [line for line in cell["source"]]

        # Get indices of magic commands (% matplotlib etc.)
        indices = [idx for idx, line in enumerate(source) if line[0] == "%"]

        magic_lines = []
        for idx in indices:
            source[idx] = "# " + source[idx]
            magic_lines.append(source[idx].rstrip() + "\n")

        # Write pure source to a temporary file
        with open("tmp_file.r", "w") as f:
            # I think print will wait until the write is done(?) whereas write is non-blocking(?)
            print("".join(source), file=f)

        # Call `black` to format the temporary file
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        output, error = process.communicate()

        # Read in the formatted file
        with open("tmp_file.r", "r") as f:
            formatted_code = f.read()

        formatted_code = formatted_code.splitlines(keepends=True)
        formatted_code[-1] = formatted_code[-1].rstrip("\n")

        indices = [
            idx for idx, line in enumerate(formatted_code) if line in magic_lines
        ]
        
        for idx in indices:
            formatted_code[idx] = formatted_code[idx].replace("# ", "")

        # Change source code to formatted version
        cell["source"] = formatted_code

with open(args.filename[:-6] + "_formatted.ipynb", "w") as f:
    json.dump(json_data, f)
