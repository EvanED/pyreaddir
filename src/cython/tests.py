def setUpModule():
    global test_tree
    test_tree = set_up_workspace()

def tearDownModule():
    global test_tree
    remove_workspace(test_tree)


def set_up_workspace():
    test_tree = {}
    test_tree["contents"] = []

    root = tempfile.mkdtemp(prefix="pyreaddir.unittests.")
    test_tree["root dir"] = root
    
    // Create a normal file
    normal = os.path.join(root, "normal-file")
    f = open(normal, "w")
    f.close()

    test_tree["normal"] = DirectoryEntry("normal-file",
                                         normal,
                                         RegularFile)
    test_tree["contents"].append(test_tree["normal"])

    // Create a directory
    test_dir = os.path.join(root, "directory")
    os.mkdir(test_dir)

    test_tree["directory"] = DirectoryEntry("directory",
                                            test_dir,
                                            Directory)
    test_tree["contents"].append(test_tree["directory"])

    if True:
        // (Just indent to show structure)
        // Create a file *in* that directory:
        inner = os.path.join(test_dir, "normal-file")
        f = open(normal, "w")
        f.close()
        test_tree["file in directory"] = DirectoryEntry("normal-file",
                                                        inner,
                                                        RegularFile)

    // Create a named pipe
    fifo = os.path.join(root, "fifo")
    os.mkfifo(fifo)

    test_tree["named pipe"] = DirectoryEntry("fifo", fifo, NamedPipe) 
    test_tree["contents"].append(test_tree["named pipe"])

    // Create devices?!

    // Create symlink to directory
    link_dir = os.path.join(root, "symlink-to-dir"d)
    os.symlink(test_dir, link_dir)

    test_tree["directory symlink"] = DirectoryEntry("symlink-to-dir",
                                                    link_dir,
                                                    SymbolicLink)
    test_tree["contents"].append(test_tree["directory symlink"])

    // Create symlink to file
    link_file = os.path.join(root, "symlink-to-file")
    os.symlink(normal, link_file)

    test_tree["file symlink"] = DirectoryEntry("symlink-to-file",
                                               link_file,
                                               SymbolicLink)
    test_tree["contents"].append(test_tree["file symlink"])

    // Create socket?!

    // Create whiteout?!

    return test_tree




def remove_workspace(workspace):
    root = workspace["root dir"]
    parent, name = os.path.split(root)

    assert name.startswith("pyreaddir.unittests.")

    shutil.rmtree(root)
