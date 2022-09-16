from src.directories import create_command, move_command, delete_command, list_command, Directory
import mock


def test_create():
    with mock.patch("builtins.open") as mock_open:
        
        mock_open.return_value.__enter__ = mock.mock_open
        mock_open.return_value.__iter__ = mock.Mock(
            return_value = iter(['CREATE fruits', 'CREATE vegetables/potatos']))

        correct_dirs = {
            "fruits": Directory("fruits"),
            "vegetables": Directory("vegetables"),
        }
        correct_dirs["vegetables"].add_subdir(Directory("potatos"))
        
        result_dirs: dict[str, Directory] = {}
        create_command(result_dirs, ["fruits"])
        create_command(result_dirs, ["vegetables/potatos"])
        for dir in result_dirs:
            assert dir in correct_dirs
            if result_dirs[dir].subdirs:
                assert result_dirs[dir].subdirs["potatos"].name == correct_dirs[dir].subdirs["potatos"].name


def test_move():
    dirs = {
        "fruits": Directory("fruits"),
        "vegetables": Directory("vegetables"),
    }
    dirs["vegetables"].add_subdir(Directory("potatos"))
    
    # MOVE vegetables/potatos fruits
    move_command(dirs, ["vegetables/potatos", "fruits"])
    assert dirs["vegetables"].subdirs == {}
    assert dirs["fruits"].subdirs.get("potatos")


def test_delete():
    dirs = {
        "fruits": Directory("fruits"),
        "vegetables": Directory("vegetables"),
    }
    dirs["vegetables"].add_subdir(Directory("potatos"))

    # DELETE vegetables/potatos
    delete_command(dirs, ["vegetables/potatos"])
    assert dirs["vegetables"].subdirs == {}
    assert dirs["fruits"].subdirs == {}



def test_list():
    dirs = {
        "fruits": Directory("fruits"),
        "vegetables": Directory("vegetables"),
    }
    dirs["vegetables"].add_subdir(Directory("potatos"))

    result = list_command(dirs)
    assert result == """fruits
vegetables
  potatos
"""
