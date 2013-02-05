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

import codecs

class Registre:
    def passos(self, pas, comentari):
        """Cada cop que es cridi aquesta funció escriurà en un
        arxiu els passos que es fan. L'arxiu queda registrat a la subcarpeta /registres
        dins la carpeta que es troba el fitxer *bot.py
        """
        arxiu = codecs.open('registres/registre-%s.txt' %(self.titol_original), 'a', 'utf-8')
        if self.cops_k_passa == 1:
            primer_comentari = u"\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"+(u"% REGISTRE DE "+unicode(self.titol_original)+u" %").center(60)+"\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
            arxiu.write(primer_comentari)
        try:
            pas = str(pas)
            pas = pas.encode('utf-8')
            comentari = str(comentari)
            comentari = comentari.encode('utf-8')
            arxiu.write('\n******\n* '+str(self.cops_k_passa)+' * \n******\n')
            arxiu.write(comentari+'\n')
            arxiu.write(pas+'\n')
        except UnicodeEncodeError:
            comentari = comentari.encode('utf-8')
            arxiu.write('\n******\n* '+str(self.cops_k_passa)+' * \n******\n')
            arxiu.write(comentari+'\n')
            arxiu.write(pas+'\n')
            pass
        except UnicodeDecodeError:
            pas = pas.decode('utf-8')
            comentari = comentari.encode('utf-8')
            arxiu.write('\n******\n* '+str(self.cops_k_passa)+' * \n******\n')
            arxiu.write(comentari+'\n')
            arxiu.write(pas+'\n')
        self.cops_k_passa += 1
        arxiu.close()
