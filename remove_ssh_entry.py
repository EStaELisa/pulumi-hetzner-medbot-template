import os

def remove_ssh_entry(file_path, host):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        skip = False
        for line in lines:
            if line.strip().startswith('Host') and host in line:
                skip = True
            elif not line.startswith(' ') and skip:
                skip = False
            if not skip:
                file.write(line)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 remove_ssh_entry.py <file_path> <host>")
        sys.exit(1)
    file_path = sys.argv[1]
    host = sys.argv[2]
    remove_ssh_entry(file_path, host)