import os
import sys
import tarfile
import datetime
from io import BytesIO


class Archive:
    """Create archives in gzipped tarballs from a file_list.

    Keyword arguments:
    file_list -- list-like input with the files to be added
    use_script_name -- bool to use the calling script name for the archive
    archive_name -- optional string name to uses if not using script name
    add_datetime_to_name -- bool to append current time to archive name
    """
    def __init__(self,
                 file_list,
                 use_script_name=True,
                 archive_name=None,
                 add_datetime_to_name=True
                 ):
        if use_script_name:
            archive_name = sys.argv[0]  # Name of the top level script
        if add_datetime_to_name or archive_name is None:
            time_now = datetime.datetime.now().strftime("_%Y%m%d%H%M%S")
            archive_name += time_now
        self.name = archive_name + '.tar.gz'

        self.__file_list = set()
        for f in file_list:
            if f in self.__file_list:
                # If file has already been added, do nothing and warn
                print("Warning - File already in archive: " + str(f))
            elif os.path.isfile(f):
                self.__file_list.add(f)
            else:
                # If file is invalid, do nothing and warn
                print("Warning - Not a valid file: " + str(f))

    def writetargzfile(self, directory='archives'):
        """Writes the archive to file in directory."""
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, self.name)

        with tarfile.open(name=filepath, mode='w:gz') as tar_file:
            for f in self.__file_list:
                tar_file.add(name=f)
        print("Archive file written to " + str(filepath))

    def streamtargz(self):
        """Compiles the archive in a streamed buffer that is returned."""
        buffer = BytesIO()
        with tarfile.open(fileobj=buffer, mode='w:gz') as tar_file:
            for f in self.__file_list:
                tar_file.add(name=f)
        buffer.seek(0)  # Reset stream pointer to start of file
        return buffer
