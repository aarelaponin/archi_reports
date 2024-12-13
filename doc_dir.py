#!/usr/bin/env python
import os
import argparse


def combine_directory(input_dir, output_file, excluded_dirs=None, included_extensions=None):
    """
    Combines files from a specific directory into a single output file.

    Args:
        input_dir (str): Path to the directory to process
        output_file (str): Path to the output file
        excluded_dirs (set): Set of directory names to exclude
        included_extensions (set): Set of file extensions to include
    """
    if excluded_dirs is None:
        excluded_dirs = {'.venv', '__pycache__', '.git', 'build', 'dist'}

    if included_extensions is None:
        included_extensions = {'.py', '.yml', '.yaml'}

    def write_file_content(outfile, file_path, relative_path):
        """Helper function to write file content with appropriate markers"""
        outfile.write(f"# Begin {relative_path}\n")
        with open(file_path, 'r', encoding='utf-8') as infile:
            outfile.write(infile.read())
        outfile.write(f"\n# End {relative_path}\n\n")

    # Ensure input directory exists
    if not os.path.exists(input_dir):
        raise ValueError(f"Directory '{input_dir}' does not exist")

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Write header with processing information
        outfile.write(f"# Combined contents from directory: {input_dir}\n")
        outfile.write(f"# Included extensions: {', '.join(included_extensions)}\n")
        outfile.write(f"# Excluded directories: {', '.join(excluded_dirs)}\n\n")

        for root, dirs, files in os.walk(input_dir):
            # Modify dirs in-place to exclude certain directories
            dirs[:] = [d for d in dirs if d not in excluded_dirs]

            for file in files:
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in included_extensions:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, input_dir)

                    # Add a special marker for config files
                    if file_ext in {'.yml', '.yaml'}:
                        outfile.write(f"# Configuration File: {relative_path}\n")
                        outfile.write("# " + "=" * 60 + "\n")
                        write_file_content(outfile, file_path, relative_path)
                        outfile.write("# " + "=" * 60 + "\n\n")
                    else:
                        # Python files
                        write_file_content(outfile, file_path, relative_path)


def main():
    parser = argparse.ArgumentParser(description='Combine files from a specific directory into a single file.')
    parser.add_argument('input_dir', help='Directory to process')
    parser.add_argument('output_file', help='Output file path')
    parser.add_argument('--exclude-dirs', nargs='+', default=None,
                        help='Directories to exclude (space-separated)')
    parser.add_argument('--include-extensions', nargs='+', default=None,
                        help='File extensions to include (space-separated)')

    args = parser.parse_args()

    excluded_dirs = set(args.exclude_dirs) if args.exclude_dirs else None
    included_extensions = set(args.include_extensions) if args.include_extensions else None

    try:
        combine_directory(args.input_dir, args.output_file, excluded_dirs, included_extensions)
        print(f"Successfully combined files into {args.output_file}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

# to document one directory. For example:
# ./doc_dir.py src mysrc.txt
# ./doc_dir.py tests mytests.txt
#
if __name__ == "__main__":
    main()
