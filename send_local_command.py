import subprocess


# Run an external command (e.g., listing files in the current directory)
def send_local_cmd(command):
    try:
        result = subprocess.run([command][0], capture_output=True, text=True, check=True, shell=True)
        print("Command output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
