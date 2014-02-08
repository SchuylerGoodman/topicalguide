#!/usr/bin/python
## -*- coding: utf-8 -*-

from __future__ import print_function

import os
import json


class GenericTools:
    
    @staticmethod
    def json_to_dict(file_path):
        '''\
        Takes a file path to a .json file and converts the contents to a dictionary.
        If an error occurs, an empty dictionary is returned.
        '''
        try:
            result = {}
            with open(file_path, 'r') as json_file:
                file_contents = json_file.read()
                result = json.loads(file_contents)
            return result
        except Exception:
            return {}
    
    @staticmethod
    def seperate_metadata_and_content(s):
        '''\
        Given a string the metadata is seperated from the content. The string must be in the following format:
        
        metadata_tag1: metadata_value1
        metadata_tag2: metadata_value2
        ...
        metadata_tagn: metadata_valuen
        <Two newlines>
        content
        content
        
        content
        ...
        
        Returns (metadata, content)
        
        If no metadata is present then an empty string is returned, same with content.
        '''
        m_and_c = s.split("\n\n", 1)
        metadata = ''
        content = ''
        
        # normal case where we have content and metadata
        if len(m_and_c) == 2:
            metadata = m_and_c[0].strip()
            content = m_and_c[1].strip()
        # if we only have one of content or metadata this process determines which it is
        elif len(m_and_c) == 1:
            value = m_and_c[0].strip()
            if not len(value) == 0:
                lines = m_and_c[0].split('\n')
                is_metadata = True
                for l in lines:
                    key_value = l.split(':')
                    if len(key_value) != 2:
                        is_metadata = False
                        break
                
                if is_metadata:
                    metadata = value
                else:
                    content = value
        
        return (metadata, content)
    
    @staticmethod
    def metadata_to_dict(metadata):
        '''\
        Takes metadata as specified in seperate_metadata_and_content() documentation and\
        converts it to a dictionary.
        Note that white space on either side of the metadata tags and values will be stripped; \
        also, if there are any duplicate metadata key names, the value of the last duplicate will \
        be in the resulting dictionary.
        Also, the tags will have any spaces replaced with underscores and be set to lowercase.
        '''
        result = {}
        lines = metadata.split('\n')
        for l in lines:
            key_value = l.split(':', 1)
            if len(key_value) == 2:
                key = key_value[0].strip().replace(' ', '_').lower()
                value = key_value[1].strip()
        return result
    
    @staticmethod
    def get_all_files_from_directory(directory, recursive=False):
        '''\
        Returns a list of absolute file paths starting at the given directory.
        Set recursive to True to recursively find files.
        Note that hidden files are ignored.
        '''
        
        def get_all_files(arg, dirname, names):
            for name in names:
                file_name = os.path.abspath(os.path.join(dirname, name))
                arg.append(file_name)
                
        list_of_files = []
        
        if recursive:
            os.path.walk(directory, get_all_files, list_of_files)
        else:
            get_all_files(list_of_files, directory, os.listdir(directory))
        return list_of_files
        







# vim: et sw=4 sts=4
