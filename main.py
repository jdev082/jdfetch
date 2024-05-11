#!/usr/bin/env python3
# simple python system information
# fetch program
# jdev082
# mit license, 2024
import platform
import os
import subprocess

rel = "v0.1.0"

system = platform.system().lower()
if system == "linux":
    import distro

def user():
    if system == "linux":
        return(os.environ.get("USER"))

def hostname():
    if system == "linux":
        o = subprocess.run(['hostname'], stdout=subprocess.PIPE)
        return o.stdout.decode('utf-8')

def osinfo():
    details = []
    if system == "linux":
        details.append("System Type: " + system)
        if distro.id() == "nixos":
            details.append("Distribution: " + "NixOS " + subprocess.run(['nixos-version'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip())
        else:     
            details.append("Distribution: " + distro.name(pretty=True))
        details.append("Kernel: " + subprocess.run(['uname', '-r'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
        return details

def nixuser():
    home = os.environ.get("HOME")
    u1 = subprocess.run(['nix-store', '-qR', f'{home}/.nix-profile'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    u2 = subprocess.run(['nix-store', '-qR', f'/etc/profiles/per-user/{user()}'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return(u1 + u2).count('\n')

def nixsystem():
    return subprocess.run(['nix-store', '-qR', '/run/current-system/sw'], stdout=subprocess.PIPE).stdout.decode('utf-8').count('\n')

def packages():
    packages = ""
    if system == "linux":
        if os.path.isdir('/nix'):
            packages = packages + "nix-user " + str(nixuser()) + " "
            packages = packages + "nix-system " + str(nixsystem())
            return packages

def sprint(s):
    l = (len(s))
    c = "-"
    print(f"{s}{c * l}")

def main():
    sprint(f"{user()}@{hostname()}")
    print("\n".join([f"{i}" for i in osinfo()]))
    print(packages())

if __name__ == "__main__":
    main()