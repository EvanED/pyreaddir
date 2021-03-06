import posix_bare
import fnmatch
import generic

def create_glob_matcher(glob):
    def matches(entry):
        return fnmatch.fnmatch(entry.name, glob)
    return matches


def every_predicate_matches(predicates, item):
    for p in predicates:
        if not p(item):
            return False
    return True


def genericize(entry_dict, path):
    return generic.DirectoryEntry(entry_dict["name"],
                                  path,
                                  generic._get_file_type_from_string(entry_dict["type"]),
                                  inode = entry_dict["inode"])


def readdir(directory_name, glob="*", extra_filters=None, **kwargs):
    if extra_filters is None:
        extra_filters = []
    if len(kwargs) != 0:
        # Warn unsupported args. Specifically check for 'transaction'
        # and 'limit_information'?
        pass

    if glob != "*":
        extra_filters.append(create_glob_matcher(glob))

    iter = posix_bare.DirectoryIterator(directory_name)

    genericized = (genericize(entry, directory_name)
                   for entry in iter)

    return (generic
            for generic in genericized
            if every_predicate_matches(extra_filters, generic))


