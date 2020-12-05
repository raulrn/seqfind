#!/usr/bin/env python2

"""
seqfind version 1.0.0
author: Jorge Raul Ramirez Nieves

usage: seqfind [-h] [--dfs] [--bfs] path

Tool for search sequences of files

positional arguments:
  path        Path to search

optional arguments:
  -h, --help  show this help message and exit
  --dfs       Use Depth-first search
  --bfs       Use Breadth-first search
"""

import sys
import os
import glob
import re
import subprocess
import argparse


class PathUtils(object):
    @staticmethod
    def search_paths(path, useDFS=False):
        return PathUtils.breadth_first_search(path, navigate=True) if not useDFS else PathUtils.depth_first_search(path, navigate=True)
        
    @staticmethod
    def depth_first_search(path, accPaths=None, navigate=False):
        """Search paths recursively using Depth-first search."""
        
        if not isinstance(accPaths, list):
            accPaths = []
       
        filesOrDirs = os.listdir(path)
        filesOrDirs.sort()
        
        for fod in filesOrDirs:
            realfod = os.path.join(path, fod)
            if not os.path.isfile(realfod):
                accPaths.append(realfod)
                
                if navigate:
                    # Each subpath is explored
                    PathUtils.depth_first_search(realfod, accPaths, navigate)
                    
        return accPaths

        
    @staticmethod
    def breadth_first_search(path, accPaths=None, navigate=False):
        """Search paths recursively using Breadth-first search."""
        
        if not isinstance(accPaths, list):
            accPaths = []
            
        filesOrDirs = os.listdir(path)
        filesOrDirs.sort()
        
        tempAccPaths = []
        
        for fod in filesOrDirs:
            realfod = os.path.join(path, fod)
            if not os.path.isfile(realfod):
                tempAccPaths.append(realfod)
                
        accPaths += tempAccPaths
                
        if navigate:
            # All collected paths are explored at the end
            [PathUtils.breadth_first_search(rfod, accPaths, navigate) for rfod in tempAccPaths]
                    
        return accPaths
    

class FileUtils(object):
    @staticmethod
    def search_files(path):
        """Get the files."""
        
        filesOrDirs = os.listdir(path)
        files = []
        
        for fod in filesOrDirs:
            realfod = os.path.join(path, fod)
            if os.path.isfile(realfod):
                files.append(realfod)
                
        return files
    
    @staticmethod
    def sequence_file_info(filePath):
        """Function for extract sequence info from file."""
        
        dirName = os.path.dirname(filePath)
        fileBaseName = os.path.basename(filePath)
        
        try:
            seqNum = re.findall(r'\d+', fileBaseName)[-1] # Extract sequence number of this file
            numPad = len(seqNum)
            baseName = fileBaseName.split(seqNum)[0]
            fileExt = fileBaseName.split('.')[-1]
            globString = baseName + ('?' * numPad)
            theGlob = glob.glob(dirName + '/' + globString + fileBaseName.split(seqNum)[1]) # List of the other numerated files
            numFrames = len(theGlob)
            theGlob.sort()
            # Substracting frames
            firstFrame = int(theGlob[0].replace(dirName + '/', '').replace(baseName, '').replace('.' + fileExt, ''))
            lastFrame = int(theGlob[-1].replace(dirName + '/', '').replace(baseName, '').replace('.' + fileExt, ''))
            return os.path.join(dirName, baseName), numPad, fileExt, firstFrame, lastFrame, numFrames # Returning the sequence info
        except IndexError:
            return filePath
        

class SequenceSearch(object):
    @staticmethod
    def _find_sequence_results(path, useDFS=True):
        """Function for search possible file sequence infos."""

        sequenceResults = []
        paths = PathUtils.search_paths(path, useDFS) # Called with the elected method and stored in a list of subpaths
        
        for p in paths: # Iterates each subpath 
            files = FileUtils.search_files(p)
            for f in files:
                if not any(sqr[0] in f and sqr[2] in f for sqr in sequenceResults): # Test if the file is in the sequence info produced by any other file of its same sequence
                    analysisResult = FileUtils.sequence_file_info(f)
                    
                    if isinstance(analysisResult, tuple):
                        sequenceResults.append(analysisResult)
                        
        return sequenceResults
    
    @staticmethod
    def _make_command(sequenceResults):
        """Function for generate the bash command."""

        finalFileNames = ['%s%s.%s' % (sqr[0], '#' * sqr[1], sqr[2]) for sqr in sequenceResults] # Processing the complete names of each file adding ####
        columnWidth = max([len(ffn) for ffn in finalFileNames]) + 5 # size of column for the shell printing
        arrayFile = ' '.join(finalFileNames)
        arrayFirstFrame = ' '.join([str(sqr[3]) for sqr in sequenceResults]) # Array of startframes
        arrayLastFrame = ' '.join([str(sqr[4]) for sqr in sequenceResults]) # Array of lastframes
        
        return 'ARRAY_FILE=( ' + arrayFile + ' ); ARRAY_FIRSTFRAME=( ' + arrayFirstFrame + ' ); ARRAY_LASTFRAME=( ' + arrayLastFrame + ' ); for((i=0;i<' + str(len(finalFileNames)) + ';i++)); do printf "%-' + str(columnWidth) + 's (%s-%s)\n" ${ARRAY_FILE[$i]} ${ARRAY_FIRSTFRAME[$i]} ${ARRAY_LASTFRAME[$i]}; done' # Bash command
    
    @staticmethod
    def find_file_sequences(path, useDFS=True):
        """Function for search and display in shel the sequence info."""
        
        sequenceResults = SequenceSearch._find_sequence_results(path, useDFS)
                        
        if sequenceResults:
            command = SequenceSearch._make_command(sequenceResults)
            subprocess.call(command , shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool for search sequences of files')
    parser.add_argument(dest='path', type=str, help='Path to search')
    parser.add_argument('--dfs', action='store_true', help='Use Depth-first search')
    parser.add_argument('--bfs', action='store_true', help='Use Breadth-first search')
    
    args = parser.parse_args()
    
    if os.path.isdir(args.path):
        if not args.dfs and args.bfs:
            SequenceSearch.find_file_sequences(args.path, useDFS=False)
        else:
            SequenceSearch.find_file_sequences(args.path, useDFS=True)
    
