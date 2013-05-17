#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request, io

class Site():
    deviation = 0.
    is_bad = False
    matches = 0.

    def __init__(self, url = 'http://ya.ru/', name = 'test'):

        if url[0:7] != 'http://':
            self.url = 'http://' + url
        else:
            self.url = url

        self.name = name
        self.content = self.load()
        self.compare()
        self.deviation = 100. - self.matches

    def load(self):
        return  urllib.request.urlopen( self.url ).readlines()

    def _procent(self, correct, bad ):
        return (float(correct) / (correct + bad)*100)

    def compare(self, max = 30. ):
        correct = 0
        bad = 0
        found = []
        not_found = []

        for current in self.load():

            for old in self.content:
                if current not in found:
                    if str(current).strip() == str(old).strip():
                        found.append(current)
                        break

            if current not in found:
                not_found.append(current)

        for item in self.content:
            if item not in found:
                not_found.append(item)

        for item in found:
            correct += 1

        for item in not_found:
            bad += 1

        self.matches = self._procent(correct, bad)
        if (100. - (self.matches + self.deviation)) >= max:
            self.is_bad = True
        else:
            self.is_bad = False

    def __str__(self):
        return (' Site - %s ,url - %s ,matches - %3.2f, deviation - %3.2f ,bad deviation - %3.2f, is bad - %s. \n' % (
                                                                    self.name,
                                                                    self.url,
                                                                    self.matches,
                                                                    self.deviation,
                                                                    100. - (self.matches + self.deviation),
                                                                    self.is_bad))
