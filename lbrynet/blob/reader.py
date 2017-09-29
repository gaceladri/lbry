import logging

log = logging.getLogger(__name__)

class HashBlobReader(object):
    """
    This is a file like reader class that supports
    read(size) and close()
    """
    def __init__(self, file_path, finished_cb):
        self.file_path = file_path
        self.finished_cb = finished_cb
        self.finished_cb_d = None
        self.read_handle = open(self.file_path, 'rb')

    def __del__(self):
        if self.finished_cb_d is None:
            log.warn("Garbage collection was called, but reader for %s was not closed yet",
                        self.file_path)
        self.close()

    def read(self, size=-1):
        return self.read_handle.read(size)

    def close(self):
        # if we've already closed and called finished_cb, do nothing
        if self.finished_cb_d is not None:
            return
        self.read_handle.close()
        self.finished_cb_d = self.finished_cb(self)


