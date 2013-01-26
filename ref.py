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

<<<<<<< HEAD
    def cerca_referencies(self,text, par=0):
        """Cerca <ref i les substitueix en el text.
        Es marquen amb l'etiqueta REFR"""
        print u'*** REFERÈNCIES ***'

        while text.find('<ref') != -1:
            inici = text.find('<ref')
=======
    def referencies(self,text, inici=0, par=0):
        """Cerca <ref i les substitueix en el text. Es marquen amb l'etiqueta
        REFR"""
        print u'*** REFERÈNCIES ***'

        while text.find('<ref',inici) != -1:
            inici = text.find('<ref', inici)
>>>>>>> 1faf3bd32661f0382917c65bd9c5c0163b0b7546
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
<<<<<<< HEAD
            text = text.replace(ref, 'REFR%i' %(par))
            context = text[inici-20:final+20]
            ref = [ref,context]
            self.refs['*REFR%i' %(par)] = ref
            par += 1
        text = self.altre_codi(text)
        return text

    def altre_codi(self, text, par=0):
        """Cerca i substitueix altre codi entre <>.
        Es marca amb l'etiqueta REFW"""
        print u'*** ALTRE CODI ***'
        while text.find(u'<') != -1:
            inici = text.find(u'<')
            prefinal = text.find(u'</')
            final = text.find(u'>',prefinal)
            wiki = text[inici:final+1]
            print wiki
            text = text.replace(wiki, 'REFW%i' %(par))
            context = text[inici-20:final+20]
            wikicodi = [wiki, context]
            self.refs['*REFW%i' %(par)] = wikicodi
            par +=1
        return text

    def cerca_comentaris(self, text, par=0):
        """Cerca i substitueix els comentaris no visibles.
        Es marquen amb l'etiqueta REFN"""
        print u'*** COMENTARIS ***'
        while text.find(u'<!--') != -1:
            inici = text.find(u'<!--')
            final = text.find(u'-->', inici)
            comentari = text[inici:final+1]
            print comentari
            text = text.replace(comentari, 'REFN%i' %(par))
            context = text[inici-20:final+20]
            comentari = [comentari, context]
            self.refs['*REFW%i' %(par)] = comentari
            par +=1
        return text

=======
            context = text[inici-20:final+20]
            ref = [ref,context]
            self.refs['REFR%i' %(par)] = ref
            par += 1
            inici = final

        return 0
>>>>>>> 1faf3bd32661f0382917c65bd9c5c0163b0b7546

if __name__ == '__main__':
    main()

