import subprocess
import os
from logger import logger


# Run an external command (e.g., listing files in the current directory)
def execute_command(command, cwd):
    """Execute a shell command and return its output."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, check=True, cwd=cwd)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Command '{e.cmd}' returned non-zero exit status {e.returncode}. Output: {e.output}"


def send_local_cmd(command, cwd):
    # Check if the command is a 'cd' command
    if command.startswith('cd '):
        try:
            new_dir = command[3:].strip()
            os.chdir(new_dir)
            cwd[0] = os.getcwd()  # Update the current working directory
        except FileNotFoundError as e:
            logger.error(f"Error: {e}")
    elif len(command) > 1 and command[1] == ':':  # Changing Drive
        new_dir = command[:2].strip()
        os.chdir(new_dir)
        cwd[0] = os.getcwd()  # Update the current working directory
    else:
        # Execute the command and get the output
        execute_command(command, cwd[0])
        # logger.info(command)
