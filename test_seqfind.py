#!/usr/bin/env python2

import os
import shutil
import unittest
import subprocess

class FileCreator(object):
    @staticmethod
    def make_files():
        cwd = os.getcwd()
        
        print(cwd)
        os.makedirs(os.path.join(cwd, 'path'))
        os.makedirs(os.path.join(cwd, 'path/to'))
        os.makedirs(os.path.join(cwd, 'path/to/a'))
        os.makedirs(os.path.join(cwd, 'path/to/a/b'))
        os.makedirs(os.path.join(cwd, 'path/to/a/b/c'))
        os.makedirs(os.path.join(cwd, 'path/to/z'))
        
        open(os.path.join(cwd, 'path/to/a/image.0001.exr'), 'a').close()
        open(os.path.join(cwd, 'path/to/a/image.0002.exr'), 'a').close()
        open(os.path.join(cwd, 'path/to/a/image.0003.exr'), 'a').close()
        
        open(os.path.join(cwd, 'path/to/a/b/image.0001.exr'), 'a').close()
        open(os.path.join(cwd, 'path/to/a/b/image.0002.exr'), 'a').close()
        open(os.path.join(cwd, 'path/to/a/b/image.0003.exr'), 'a').close()
        
        open(os.path.join(cwd, 'path/to/a/b/c/image.0001.exr'), 'a').close()
        open(os.path.join(cwd, 'path/to/a/b/c/image.0002.exr'), 'a').close()
        
        open(os.path.join(cwd, 'path/to/z/image.0001.exr'), 'a').close()
        open(os.path.join(cwd, 'path/to/z/image.0002.exr'), 'a').close()
        open(os.path.join(cwd, 'path/to/z/image.0003.exr'), 'a').close()
        
    @staticmethod
    def remove_files():
        cwd = os.getcwd()
        shutil.rmtree(os.path.join(cwd, 'path'))
        
    
class TestPathUtils(unittest.TestCase):
    def test_depth_first_search(self):
        from seqfind import PathUtils
        FileCreator.make_files()
        
        cwd = os.getcwd()
        
        paths = []
        paths.append(os.path.join(cwd, 'path/to'))
        paths.append(os.path.join(cwd, 'path/to/a'))
        paths.append(os.path.join(cwd, 'path/to/a/b'))
        paths.append(os.path.join(cwd, 'path/to/a/b/c'))
        paths.append(os.path.join(cwd, 'path/to/z'))
        
        findPaths = PathUtils.search_paths(os.path.join(cwd, 'path'), True)
        
        FileCreator.remove_files()
        
        self.assertEqual(findPaths, paths)
        
    def test_breadth_first_search(self):
        from seqfind import PathUtils
        FileCreator.make_files()
        
        cwd = os.getcwd()
        
        paths = []
        paths.append(os.path.join(cwd, 'path/to'))
        paths.append(os.path.join(cwd, 'path/to/a'))
        paths.append(os.path.join(cwd, 'path/to/z'))
        paths.append(os.path.join(cwd, 'path/to/a/b'))
        paths.append(os.path.join(cwd, 'path/to/a/b/c'))
        
        findPaths = PathUtils.search_paths(os.path.join(cwd, 'path'), False)
        
        FileCreator.remove_files()
        
        self.assertEqual(findPaths, paths)
        

class TestFileUtils(unittest.TestCase):
    def test_search_files(self):
        from seqfind import FileUtils
        
        FileCreator.make_files()
        
        cwd = os.getcwd()
        
        files = []
        files.append(os.path.join(cwd, 'path/to/z/image.0001.exr'))
        files.append(os.path.join(cwd, 'path/to/z/image.0002.exr'))
        files.append(os.path.join(cwd, 'path/to/z/image.0003.exr'))
        
        findFiles = FileUtils.search_files(os.path.join(cwd, 'path/to/z'))
        
        FileCreator.remove_files()
        
        self.assertEqual(all(ff in files for ff in findFiles), True)
        
    def test_sequence_file_info(self):
        from seqfind import FileUtils
        
        FileCreator.make_files()
        
        cwd = os.getcwd()
        
        result = (os.path.join(cwd, 'path/to/z/image.'), 4, 'exr', 1, 3, 3)
        fileTest = os.path.join(cwd, 'path/to/z/image.0002.exr')
        
        fileInfo = FileUtils.sequence_file_info(fileTest)
        
        FileCreator.remove_files()
        
        self.assertEqual(fileInfo, result)
        
           
if __name__ == '__main__':
    FileCreator.make_files()
    #FileCreator.remove_files()
    #unittest.main()
