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
import time

class Enllacos():

    def cerca_enllacos(self, text, par = 0):
        """Cerca [], els classifica i substitueix en el text.
        Es marca amb l'etiquetra REFE"""
        print u'*** ENLLAÇOS ***'
        marca = ''
        categoria = 0
        llista_http = []
        llista_simple = []
        llista_complexa = []
        llista_fitxer = []
        llista_categoria = []
        llista_interviqui = []
        while text.find('[') != -1:
            contador = 0
            inici = text.find('[')
            final = text.find(']')
            inici2 = inici
            while marca != 'prou':
                if text.find('[',inici2+2,final) != -1:
                    inici2 = final
                    final = text.find(']', final+2)
                else:
                    marca = 'prou'
            marca = ''
            if text.startswith(u'[http:', inici):
                print u'* ENLLAÇ WEB *'
                enllac = text[inici:final+1]
                context = text[inici-20:final+20]
                text = text.replace(enllac, 'REFE%i' %(par))
                enllac = [enllac,context]
                llista_http.append(enllac)
            elif text.startswith('[[File:', inici) or text.startswith(u'[[Image:', inici):
                print '* FITXER DE COMMONS * '
                if text[final+3] == ']':
                    final = final + 2
                enllac = text[inici:final+2]
                context = text[inici-20:final+20]
                text = text.replace(enllac, 'REFE%i' %(par))
                enllac = [enllac,context]
                llista_fitxer.append(enllac)
            elif text.startswith(self.diccionari_cat[self.idioma_original], inici):
                print '* ENLLAÇ DE CATEGORIA *'
                enllac = text[inici:final+2]
                context = text[inici-20:final+20]
                text = text.replace(enllac, 'REFE%i' %(par))
                enllac = [enllac,context]
                llista_categoria.append(enllac)
                categoria = 1
            else:
                if categoria == 1:
                    print '* ENLLAÇ INTERVIQUI *'
                    enllac = text[inici:final+2]
                    context = text[inici-20:final+20]
                    text = text.replace(enllac, 'REFE%i' %(par))
                    enllac = [enllac,context]
                    llista_interviqui.append(enllac)
                else:
                    print '* ENLLAÇ DE TEXT *'
                    enllac = text[inici:final+2]
                    if enllac.find('|') != -1:
                        inici_marca = enllac.find('|')
                        context = text[inici-20:final+20]
                        enllac = [enllac,context]
                        text = text.replace(enllac[0], enllac[0][inici_marca+1:-2])
                        print enllac[0][inici_marca+1:-2]
                        llista_complexa.append(enllac)
                    else:
                        context = text[inici-20:final+20]
                        enllac = [enllac,context]
                        print enllac[0][2:-2]
                        text = text.replace(enllac[0], enllac[0][2:-2])
                        llista_simple.append(enllac)
            inici = final-1
            print enllac
            self.refs['*REFE%i' %(par)] = enllac
            par += 1
            time.sleep(1)
        self.llista_enllacos = [llista_http,llista_simple,llista_complexa,llista_fitxer,llista_categoria,llista_interviqui]
        return text

if __name__ == '__main__':
    main()

