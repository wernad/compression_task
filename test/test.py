import os
from unittest.mock import patch
import shutil
import unittest
from io import StringIO 
from argparse import Namespace

from logcompressor.logcompressor import compress_logs

class TestLogCompression(unittest.TestCase):
    main_folder = 'test/test_folder'
    log_folder = 'test/log_files'
    test_paths = [main_folder + '/test_multiple_path_1', main_folder + '/test_multiple_path_2', main_folder + '/test_multiple_path_3']
    original_log_count = len([name for name in os.listdir(log_folder)])
    
    @classmethod
    def setUpClass(self) -> None:   
        if not os.path.exists(self.main_folder):
            os.makedirs(self.main_folder) 

    @classmethod
    def tearDownClass(self) -> None:
        shutil.rmtree(self.main_folder)        
    
    @classmethod
    def tearDown(self) -> None:
        for log in os.listdir(self.main_folder):
            path_to_delete = os.path.join(self.main_folder, log)
            try:
                shutil.rmtree(path_to_delete)
            except OSError:
                os.remove(path_to_delete)
        
    def test_empty_folder(self):
        args = Namespace(paths = [self.main_folder], d = False, r = False, compress=6)
        
        for log in os.listdir(self.main_folder):
            os.remove(str(os.path.join(self.main_folder, log)))

        with patch('sys.stdout', new = StringIO()) as _:
            self.assertEqual(compress_logs(args), 1)

        print('Empty folder test succesful.')

    def test_basic_compression(self):
        args = Namespace(paths = [self.main_folder], d = False, r = False, compress=6)

        shutil.copytree(self.log_folder, self.main_folder, dirs_exist_ok=True)
        original_log_count = self.original_log_count 

        with patch('sys.stdout', new = StringIO()) as _:
            self.assertEqual(compress_logs(args), None)

        file_count = len([name for name in os.listdir(self.main_folder)])

        with patch('sys.stdout', new = StringIO()) as _:
            self.assertEqual(file_count, original_log_count * 2)

        print('Basic compression test succesful.')
    
    def test_multiple_paths(self):
        args = Namespace(paths = self.test_paths, d = False, r = False, compress=6)

        for path in self.test_paths:
            os.makedirs(path) 
            shutil.copytree(self.log_folder, path, dirs_exist_ok=True)
        
        original_log_count = self.original_log_count * len(self.test_paths)

        with patch('sys.stdout', new = StringIO()) as _:
            self.assertEqual(compress_logs(args), None)

        file_count = 0
        for path in self.test_paths:
            file_count += len([name for name in os.listdir(path)])
        
        with patch('sys.stdout', new = StringIO()) as _:
            self.assertEqual(file_count, original_log_count * 2)

        args.paths = ['nonexistent_path/logs']
        
        with patch('sys.stdout', new = StringIO()) as _:
            self.assertEqual(compress_logs(args), 2)

        args.paths = [self.log_folder, 'nonexistent_path/logs']
        
        with patch('sys.stdout', new = StringIO()) as _:
            self.assertEqual(compress_logs(args), 2)

        print('Multiple paths test succesful.')

    def test_delete_after_compression(self):
        args = Namespace(paths = [self.main_folder], d = True, r = False, compress=6)

        shutil.copytree(self.log_folder, self.main_folder, dirs_exist_ok=True)
        original_log_count = self.original_log_count 
        
        with patch('sys.stdout', new = StringIO()) as _:
            self.assertEqual(compress_logs(args), None)

        file_count = len([name for name in os.listdir(self.main_folder)])

        with patch('sys.stdout', new = StringIO()) as _:
            self.assertEqual(file_count, original_log_count)

        print('Delete logs after compression test succesful.')

    def test_recursive(self):    
        args = Namespace(paths = [self.main_folder], d = False, r = True, compress=6)

        for path in self.test_paths:
            os.makedirs(path) 
            shutil.copytree(self.log_folder, path, dirs_exist_ok=True)

        shutil.copytree(self.log_folder, self.main_folder, dirs_exist_ok=True)
        
        original_log_count = self.original_log_count * 4
        
        with patch('sys.stdout', new = StringIO()) as _:
            self.assertEqual(compress_logs(args), None)

        file_count = sum([len(file) for file in [files for _, _, files in os.walk(self.main_folder)]])

        with patch('sys.stdout', new = StringIO()) as _:
            self.assertEqual(file_count, original_log_count * 2)

        print('Recursive log search test succesfull.')

    def test_delete_with_recursive(self):
        args = Namespace(paths = [self.main_folder], d = True, r = True, compress=6)

        for path in self.test_paths:
            os.makedirs(path) 
            shutil.copytree(self.log_folder, path, dirs_exist_ok=True)

        shutil.copytree(self.log_folder, self.main_folder, dirs_exist_ok=True)
        
        original_log_count = self.original_log_count * 4
        
        with patch('sys.stdout', new = StringIO()) as _:
            self.assertEqual(compress_logs(args), None)

        file_count = sum([len(file) for file in [files for _, _, files in os.walk(self.main_folder)]])

        with patch('sys.stdout', new = StringIO()) as _:
            self.assertEqual(file_count, original_log_count)

        print('Recursive log search with delete after compression test succesfull.')

    def test_compression_levels(self):
        args = Namespace(paths = [self.main_folder], d = False, r = False)

        shutil.copytree(self.log_folder, self.main_folder, dirs_exist_ok=True)
        
        for i in range(1,10):
            args.compress = i
            
            with patch('sys.stdout', new = StringIO()) as _:
                self.assertEqual(compress_logs(args), None)

        print('Compression levels test succesfull.')

if __name__ == '__main__':
    unittest.main()