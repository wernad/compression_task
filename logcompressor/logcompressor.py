import os
import gzip
import shutil
import argparse

def get_arguments():
    """Returns a namespace object with parsed command line arguments."""
    parser = argparse.ArgumentParser(description = 'Script for compressing log files in a given directory')
    parser.add_argument('-c', '--compress', type=int, default=6, choices=range(1,10), help = 'Compression level 1-9 (default: 6)')
    parser.add_argument('-p', '--paths', default=['var/logs'], nargs='+', help = 'Path(s) to the folder(s) with logs (default: /var/logs)')
    parser.add_argument('-d', help = 'If set, script deletes log files after compression.', action='store_true')
    parser.add_argument('-r', help = 'If set, script searches for logs in given path(s) recursively', action='store_true')
    args = parser.parse_args()
    
    return args 

def compress_logs(options): 
    """Compresses all files in a given directory. Behaviour can be modified with options parameter.
    Args:
        options: namespace object
    """

    log_dirs = [*options.paths]
    compression_level = int(options.compress) 
    files_found = False
    log_counter = 0

    for dir_name in log_dirs:
        if not os.path.isdir(dir_name):
            print('Path not found. The path that caused this: \'' + dir_name + '\'')
            return 2

    for dir_name in log_dirs:
            for root, _, files in os.walk(dir_name):
                files = filter(lambda x: not x.lower().endswith('.gz'), files)

                for file in files:
                    if not files_found:
                        files_found = True
                    
                    with open(os.path.join(root, file), 'rb') as log_file:
                        with gzip.open(os.path.join(root, file) + '.gz', 'wb', compresslevel=compression_level) as compressed_file:
                            shutil.copyfileobj(log_file, compressed_file)
                            log_counter += 1
                    if options.d:        
                        os.remove(os.path.join(root, file))

                if not options.r:
                    break           

    if not files_found:
        print('No logs found.')
        return 1
    
    print('Compression was finished. Number of compressed files: ' + str(log_counter))

if __name__ == '__main__':
    args = get_arguments()
    compress_logs(args)