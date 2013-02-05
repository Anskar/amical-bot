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

import wikipedia
import time
import re
import codecs

class Plantilles():

    def peticio(self, plantilla, par=0):
        """Gestiona la plantilla de petició"""
        print u'* PLANTILLA DE PETICIÓ DE TRADUCCIÓ *'
        final = plantilla.find('}}')
        plantilla = plantilla[1:final].split('|')
        self.idioma_original = plantilla[1].lower()
        self.titol_original = plantilla[2]
        for valor in plantilla[1:]:
            print valor
            clau = self.diccionari_peticio.keys()
            clau.sort()
            if valor.count(u'--[[Usuari:') != 0:
                valor = valor[4:]
            self.diccionari_peticio[clau[par]] = valor
            par +=1
        self.passos(self.diccionari_peticio, u'Plantilla de peticio de traduccio')

    def ordena_diccionari(self, dicc, count=0):
        """Repassa el diccionari self.refs per gestional el codi.
        Cada codi té una marca que es troba en el diccionari de tuples self.marques"""
        print u'\n*** PROCESSANT EL DICCIONARI DE REFERÈNCIES ***'
        claus = sorted(dicc.keys(), reverse=True)
        self.count = count
        for valor in claus:
            nou_text = dicc[valor]
            self.passos([str(valor),dicc[valor]], 'Diccionari ordenat en brut:')
            if valor.startswith(self.cerques[0][-1][:-3]): # Comentaris
                print u'* PROCESSANT COMENTARI *'
                nou_text = u'<!--' + self.traductor(nou_text[4:-3]) + u'-->'
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[1][-1][:-3]): # Enllaços de text
                nou_enllac = self.gestiona_enllac(nou_text)
                self.text_trad = self.text_trad.replace(valor, nou_enllac)
                dicc[valor] = nou_enllac
                continue
            elif valor.startswith(self.cerques[2][-1][:-3]): # Enllaços web
                print u'* PROCESSANT ENLLAÇ WEB *'
                inici = nou_text.find(u' ')
                nou_text = nou_text.replace(nou_text[inici:], self.traductor(nou_text[inici:]))
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[3][-1][:-3]): # Plantilles !! ENCARA FALTA
                nou_text = self.gestiona_plantilles(nou_text, valor)
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[4][-1][:-3]): # Referències úniques
                print u'* PROCESSANT REFERÈNCIES *'
                inici = nou_text.find(u'>')
                final = nou_text.find(u'</')
                nou_text = nou_text.replace(nou_text[inici+1:final], self.traductor(nou_text[inici+1:final]))
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[5][-1][:-3]): # Primers ref name
                print u'* PROCESSANT REFERÈNCIES *'
                inici = nou_text.find(u'>')
                final = nou_text.find(u'</')
                nou_text = nou_text.replace(nou_text[inici+1:final], self.traductor(nou_text[inici+1:final]))
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[6][-1][:-3]): # Següents ref name
                print u'* PROCESSANT REFERÈNCIES *'
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[7][-1][:-3]): # Taules !! ENCARA FALTA
                print u'* PROCESSANT TAULES *'
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[8][-1][:-3]): # Altre codi !! ENCARA FALTA
                if nou_text in self.passa_codi:
                    continue
                if self.count != 1:
                    self.count = 1
                    continue
                else:
                    marca = self.refs[valor]
                    nou_text = self.gestiona_codi(valor)
                    dicc[valor] = marca + nou_text
            else: # Enllaços de commons que no tenen cabuda en la llista de tuples self.cerques però queden dins del diccionari selfs.ref
                nou_text = self.gestiona_commons(dicc[valor])
                dicc[valor] = nou_text
            self.passos([str(valor),dicc[valor]], 'Diccionari ordenat traduit:')
