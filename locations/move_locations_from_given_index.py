#! /usr/bin/python3
"""
Some files have index prefixes (like: '1--', '2--').
You can move all that indexes starting from given one.

First argument - directory with files, second - index, starting from
which to move, third - amount on which to move that indexes.
"""


import os
import os.path
import sys




def main ():
	move_indexes_of_files ()


def move_indexes_of_files ():
	#current_files_dir = os.path.dirname (__file__)
	directory_with_files = sys.argv[1]
	temp_dir_path        = create_temp_directory (directory_with_files)
	rename_from_index    = int(get(sys.argv, 2, 1))
	increase_onto_index  = int(get(sys.argv, 3, 1))
	print('directory with files : ', directory_with_files)
	print('given index          : ', rename_from_index)
	print('increase onto        : ', increase_onto_index)

	old_filenames, new_filenames = rename_files (directory_with_files, temp_dir_path, rename_from_index, increase_onto_index)
	remove_temp_directory (temp_dir_path)
	print ('finished')
	print ('old_filenames : ', old_filenames)
	print ('')
	print ('new_filenames : ', new_filenames)


def get (collection, index, default = None):
	try:
		return collection[index]
	except (IndexError, KeyError):
		return default


def create_temp_directory (directory_with_files):
	temp_dir_path = os.path.abspath (os.path.join (directory_with_files, './temp'))
	try:
		os.mkdir (temp_dir_path)
	except FileExistsError:
		pass
	return temp_dir_path


def remove_temp_directory (temp_dir_path):
	try:
		os.rmdir (temp_dir_path)
	except OSError as err:  # directory not empty
		print ("can't remove temp directory: ", err)


def rename_files (directory_with_files, temp_dir_path, rename_from_index, increase_onto_index):
	entries_in_target_dir = os.listdir (directory_with_files)

	def check_is_file (filename, containing_it_dir):
		abs_filepath = os.path.abspath (os.path.join (containing_it_dir, filename))
		is_file      = os.path.isfile  (abs_filepath)
		return is_file

	files_in_target_dir = [fn for fn in entries_in_target_dir if check_is_file (fn, directory_with_files)]

	old_filenames = []
	new_filenames = []

	for filename in files_in_target_dir:
		filename_parts     = filename.split ('--')
		index_prefix       = filename_parts [0]

		try:
			index_prefix  = int(index_prefix)
			should_rename = index_prefix >= rename_from_index
			if not should_rename:
				continue
		except ValueError as err:
			print (f'error renaming file {filename}: ', err)

		index_prefix      += increase_onto_index
		filename_parts [0] = str(index_prefix)
		new_filename       = '--'.join (filename_parts)

		source_abs_path = os.path.join (directory_with_files, filename)
		dest_abs_path   = os.path.join (temp_dir_path,        new_filename)
		os.rename (source_abs_path, dest_abs_path)

		old_filenames.append (filename)
		new_filenames.append (new_filename)

	# return them back separately to avoid naming conflicts
	for new_filename in new_filenames:
		source_abs_path = os.path.join (temp_dir_path,        new_filename)
		dest_abs_path   = os.path.join (directory_with_files, new_filename)
		os.rename (source_abs_path, dest_abs_path)

	return old_filenames, new_filenames




if __name__ == '__main__':
	main ()
