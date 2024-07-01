#!/usr/bin/env python3
import subprocess


def run_as_sudo(sudo_user, cmd_str, shell=False, timeout=None):
    sudo_args = ["sudo", "-u", sudo_user]

    r = run_cmd(sudo_args + cmd_str.split(), shell=shell, timeout=timeout)
    return r


def run_cmd(cmd_array, shell=False, timeout=None):
    if shell:
        return subprocess.run(" ".join(cmd_array), shell=shell, timeout=timeout)

    # https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess
    return subprocess.run(cmd_array, shell=shell, timeout=timeout)
