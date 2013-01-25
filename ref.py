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

class Ref():

    def referencies(self,text, inici=0, par=0):
        """Cerca <ref i les substitueix en el text. Es marquen amb l'etiqueta
        REFR"""
        print u'*** REFERÈNCIES ***'

        while text.find('<ref',inici) != -1:
            inici = text.find('<ref', inici)
            final = text.find('</ref',inici)
            if text.find('<ref',inici+4,final) != -1:
                final = text.find('>',inici +3)
                final = final + 1
                print 'És un ref name'
            else:
                print 'No és un ref name'
                final = final+6
            ref = text[inici:final]
            print ref
            self.llista_refs.append(ref)
            context = text[inici-20:final+20]
            ref = [ref,context]
            self.refs['REFR%i' %(par)] = ref
            par += 1
            inici = final

        return 0

if __name__ == '__main__':
    main()

