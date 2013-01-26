#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sense títol.py
#
#  Copyright 2013  <anskar@margarida-desktop>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import os
import subprocess
import sys

class Traductor:

    def traductor(self, text):
        original = open('original.txt', 'w')
        original.write(text)
        original.close()
        if self.idioma_original == 'en':
            text_trad = subprocess.Popen(['apertium en-ca original.txt traduccio.txt'], shell=True)
        if self.idioma_original == 'es':
            text_trad = subprocess.Popen(['apertium es-ca original.txt traduccio.txt'], shell=True)
        if self.idioma_original == 'fr':
            text_trad = subprocess.Popen(['apertium fr-ca original.txt traduccio.txt'], shell=True)
        if self.idioma_original == 'pt':
            text_trad = subprocess.Popen(['apertium pt-ca original.txt traduccio.txt'], shell=True)

if __name__ == '__main__':
    app = Traductor()
    app.traductor()

