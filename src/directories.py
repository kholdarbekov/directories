from typing import List, Tuple, Optional
from enum import Enum


class Directory:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.subdirs: dict[str, Directory] = {}

    def add_subdir(self, dir: "Directory") -> None:
        self.subdirs[dir.name] = dir


class Commands(Enum):
    CREATE = 1
    MOVE = 2
    DELETE = 3
    LIST = 4


LIST_OF_COMMANDS = {
    Commands.CREATE.name,
    Commands.MOVE.name,
    Commands.DELETE.name,
    Commands.LIST.name,
}


def parse_path(args: "list[str]", separator: str = "/") -> List[str]:
    return [path.split(separator) for path in args]


def validate_path(dirs: "dict[str, Directory]", path: "list[str]") -> Tuple[bool, Optional["dict[str, Directory]"]]:
    cwd = dirs
    len_of_dirs_in_path = len(path)
    for i in range(len_of_dirs_in_path):
        if path[i] not in cwd:
            return False, None
        if i != len_of_dirs_in_path - 1:
            cwd = cwd[path[i]].subdirs
    
    return True, cwd


def create_command(dirs: "dict[str, Directory]", args: "list[str]") -> None:
    dirs_in_path = parse_path(args)[0]
    
    # Option 1: do not let creation of nested dirs
    '''
    # validate path except last dir, because it's to be created
    path_is_valid, cwd = validate_path(dirs, dirs_in_path[:-1])
    if path_is_valid:
        new_dir = Directory(dirs_in_path[-1])
        if len(dirs_in_path) == 1:
            cwd[dirs_in_path[0]] = new_dir
        else:
            cwd[dirs_in_path[-2]].add_subdir(new_dir)
    else:
        print(f"Cannot create {args[0]}")
    
    return cwd
    '''
    # Option 2: Let creation of nested dirs
    for dir in dirs_in_path:
        if dir not in dirs:
            dirs[dir] = Directory(dir)
        dirs = dirs[dir].subdirs

def move_command(dirs: "dict[str, Directory]", args: "list[str]") -> None:
    source, destination = parse_path(args)

    # check if source and destination paths are valid
    source_is_valid, src_cwd = validate_path(dirs, source)
    destination_is_valid, dest_cwd = validate_path(dirs, destination)

    if not source_is_valid:
        print(f"Cannot move from {args[0]} - {args[0]} does not exist")
    if not destination_is_valid:
        print(f"Cannot move to {args[1]} - {args[1]} does not exist")
    
    try:
        moving_dir = src_cwd.pop(source[-1])
        dest_cwd[destination[-1]].add_subdir(moving_dir)
    except KeyError:
        print(f"Cannot move {args[0]} to {args[1]}")

def delete_command(dirs: "dict[str, Directory]", args: "list[str]") -> None:
    dirs_in_path = parse_path(args)[0]
    #len_of_dirs_in_path = len(dirs_in_path)

    path_is_valid, cwd = validate_path(dirs, dirs_in_path)
    if path_is_valid:
        cwd.pop(dirs_in_path[-1])
    else:
        print(f"Cannot delete {args[0]} - {args[0]} does not exist")


def list_command(dirs: "dict[str, Directory]", tab_space = 0) -> str:
    result_srt = ""
    for dir_name, dir in dirs.items():
        print(" " * tab_space + dir_name)
        result_srt += " " * tab_space + dir_name + "\n"
        if dir.subdirs:
            result_srt += list_command(dir.subdirs, tab_space + 2)
    return result_srt


def main() -> "dict[str, Directory]":
    dirs: dict[str, Directory] = {}
    with open("commands.txt") as commands:
        for command in commands:
            command = command.replace("\n", "")
            print(command)
            cmd, *args = command.split()
            
            if cmd not in LIST_OF_COMMANDS:
                print("Unknown Command was provided")
            
            if cmd == Commands.CREATE.name:
                # length of args is 1
                if len(args) != 1:
                    print("CREATE command expects 1 argument")

                create_command(dirs, args)

            elif cmd == Commands.MOVE.name:
                # length of args is 2
                if len(args) != 2:
                    print("MOVE command expects 2 arguments")
                
                move_command(dirs, args)

            elif cmd == Commands.DELETE.name:
                # length of args is 1
                if len(args) != 1:
                    print("DELETE command expects 1 arguments")
                
                delete_command(dirs, args)

            elif cmd == Commands.LIST.name:
                # length of args is 0
                if len(args) != 0:
                    print("LIST command does not take arguments")
                list_command(dirs)
    return dirs

if __name__ == "__main__":
    main()
