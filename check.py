#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib, io

class Site():
    deviation = 0.    
    
    def __init__(self, url = 'http://ya.ru/', name = 'test'):
        
        if url[0:7] != 'http://':
            self.url = 'http://' + url
        else:
            self.url = url
            
        self.name = name
        self.content = self.load()
        self.deviation = 100. - self.compare()

    def load(self):        
        return urllib.urlopen( self.url ).readlines()         

    def procent(self, correct, bad ):
        return round((float(correct) / (correct + bad))*100)

    def compare(self):
        correct = 0
        bad = 0
        correct_this = False

        for current_str in self.load():
            correct_this = False

            for old_str in  self.content:
                if current_str == old_str:
                    correct_this = True
                    break

            if correct_this :
                correct += 1
            else:
                bad += 1

        return self.procent(correct, bad)