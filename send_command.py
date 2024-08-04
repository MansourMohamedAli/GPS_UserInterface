import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
remote_cmd_path = os.path.join(parent, "RemoteCMD")
sys.path.append(remote_cmd_path)

from RemoteCMDClient import main as send_cmd_client

args = ['--host', '10.0.0.132', '--command', 'dir']
send_cmd_client(args)
