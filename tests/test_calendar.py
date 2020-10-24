#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import src as paperless

from datetime import datetime as dt
import re
import tempfile
from unittest import TestCase

class TestCalendar(TestCase):

    def setUp(self):
        self.schedules = [
"Schedule('124926','N12345',dt(2020, 10, 21, 14, 0),dt(2020, 10, 21, 16, 0),\
'Clement, Mathieu','CfiLastName, CfiFirstName',None)", 
"Schedule('125806','N12345',dt(2020, 10, 24, 14, 0),dt(2020, 10, 24, 16, 0),\
'Clement, Mathieu','CfiLastName, CfiFirstName',None)", 
"Schedule('332807','N12345',dt(2020, 10, 25, 16, 0),dt(2020, 10, 25, 18, 0),\
'Clement, Mathieu','CfiLastName, CfiFirstName',None)", 
"Schedule('123986','N12345',dt(2020, 10, 30, 14, 0),dt(2020, 10, 30, 16, 0),\
'Clement, Mathieu','CfiLastName, CfiFirstName',None)", 
"Schedule('123988','N9876A',dt(2020, 11, 7, 11, 0),dt(2020, 11, 7, 13, 0),\
'Clement, Mathieu','CfiLastName, CfiFirstName',None)", 
"Schedule('123989','N12345',dt(2020, 11, 11, 11, 0),dt(2020, 11, 11, 13, 0),\
'Clement, Mathieu','CfiLastName, CfiFirstName',None)", 
"Schedule('123991','N12345',dt(2020, 11, 14, 11, 0),dt(2020, 11, 14, 13, 0),\
'Clement, Mathieu','CfiLastName, CfiFirstName',None)", 
"Schedule('123992','N12345',dt(2020, 11, 21, 11, 0),dt(2020, 11, 21, 13, 0),\
'Clement, Mathieu','CfiLastName, CfiFirstName',None)", 
"Schedule('123993','N12345',dt(2020, 11, 22, 11, 0),dt(2020, 11, 22, 13, 0),\
'Clement, Mathieu','CfiLastName, CfiFirstName',None)", 
"Schedule('124311','N12345',dt(2020, 11, 28, 14, 0),dt(2020, 11, 28, 16, 0),\
'Clement, Mathieu','CfiLastName, CfiFirstName',None)", 
"Schedule('124314','N12345',dt(2020, 11, 29, 14, 0),dt(2020, 11, 29, 16, 0),\
'Clement, Mathieu','CfiLastName, CfiFirstName',None)"]
        self.calendar = paperless.Calendar(self.schedules)
        self.f = tempfile.TemporaryFile()
        self.calendar.write_file(self.f)
        self.lines = self.f.readlines()


    def tearDown(self):
        self.f.close()


    def test_empty_schedules_raises(self):
        with self.assertRaises(ValueError):
            paperless.Calendar([])
        with self.assertRaises(ValueError):
            paperless.Calendar(None)

    
    def test_has_correct_vcalendar(self):
        self.assertEqual(self.lines[0], 'BEGIN:VCALENDAR')
        self.assertEqual(self.lines.count('BEGIN:VCALENDAR'), 1)

        self.assertEqual(self.lines[-1], 'END:VCALENDAR')
        self.assertEqual(self.lines.count('END:VCALENDAR'), 1)
        
        self.assertTrue(self.lines[1] == 'VERSION:2.0' or \
                        self.lines[2] == 'VERSION:2.0')
        self.assertEqual(self.lines.count('VERSION:2.0'), 1)

        # https://en.wikipedia.org/wiki/Formal_Public_Identifier
        prodid_pattern = 'PRODID:-//[A-Z0-9]+//.+'
        self.assertTrue(re.match(self.lines[1], pattern) is not None or \
                        re.match(self.lines[2], pattern) is not None)


    def test_number_of_events_matches(self):
        num_events_in_ics = self.lines.count('BEGIN:VEVENT')
        self.assertEqual(num_events_in_ics, len(self.schedules), 'BEGIN:VEVENT')

        fields = ['END:VEVENT', 'DTSTART', 'DTEND', 'SUMMARY', 'CATEGORIES',
                  'DESCRIPTION', 'LOCATION', 'STATUS', 'UID']
        # TODO check check-out link for aircraft in description?
        for field in f:
            self.assertEqual(num_events_in_ics, self.lines.count(field), field)
 
