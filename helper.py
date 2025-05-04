import os


def normalize_path(path):
	return os.path.normpath(path).replace('\\', '/').lower()