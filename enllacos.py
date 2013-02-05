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

import re, time, wikipedia

class Gestio():

    def gestiona_commons(self, enllac):
        """Gestiona els fitxers de commons"""
        print u'* PROCESSANT UN FITXER DE COMMONS *'
        enllac = enllac[2:-2]
        if enllac.find('REF') != -1:
            marca = re.findall(r' REF\w+[\S]', enllac)
            for ref in marca:
                ref = ref+u' '
                if ref.startswith(u' REFEA'):
                    canvi = self.gestiona_enllac(self.refs[ref])
                    enllac = enllac.replace(ref, canvi)
        marca_enllac = enllac.rfind(u'|')
        text = enllac[marca_enllac+1:]
        text_traduit = self.traductor(text)
        enllac = enllac.replace(text,text_traduit)
        return u'[[' + enllac + u']]'

    def gestiona_enllac(self, enllac):
        """Gestiona els enllaços de text"""
        print u'* PROCESSANT UN ENLLAÇ DE TEXT *'
        enllac = enllac[2:-2]
        if enllac.find(u'|') != -1:
            marca = enllac.find(u'|')
            enllac = enllac[marca+1:]
        return enllac

    def gestiona_plantilles(self, plantilla, key):
        """Gestiona les plantilles"""
        print u'* PROCESSANT UNA PLANTILLA *'
        plantilla_ca = self.plant_ca(plantilla, self.idioma_original)
        if plantilla_ca == u'No existeix la plantilla en català':
            missatge = plantilla+u"<ref group=nt>La plantilla no existeix en català, o almenys, no s'ha pogut trobar automàticament. En cas que trobeu la corresponent plantilla ja traduida poseu-hi l'enllaç interviqui per poder trobar-la en següents traduccions.</ref>"
            return missatge
        else:
            inici = plantilla_ca.rfind(u':')
            plantilla_ca = plantilla_ca[inici+1:-2]
            final = plantilla.find(u'|')
            plantilla = plantilla.replace(plantilla[2:final], plantilla_ca)
        return plantilla

    def plant_ca(self, plantilla, idioma):
        """Cerca la plantilla a ca:viquipedia respecte la plantilla original"""
        plantilla = plantilla[2:-2]
        plantilla = plantilla.split(u'|')
        dicc_id = {u'en' : u'Template:',
                   u'fr' : u'Modèle:',
                   u'es' : u'Plantilla:',
                   u'de' : u'Vorlage:'
                   }
        if plantilla[0].startswith(self.ordena[idioma]):
            missatge = u"Aquesta és la plantilla d'ordenació."
            return missatge
        nom = plantilla[0].rstrip()
        nom = nom.lstrip()
        pagina = dicc_id[idioma]+nom+u'/doc'
        try:
            pagina_plantilla= wikipedia.Page(idioma,pagina)
            plantilla_ori = pagina_plantilla.get()
        except:
            pagina = dicc_id[idioma]+nom
            pagina_plantilla= wikipedia.Page(idioma,pagina)
            try:
                plantilla_ori = pagina_plantilla.get()
            except:
                plantilla_ori = ''
            missatge = u"Aquesta plantilla no té pàgina d'ús"
        inici = plantilla_ori.find(u'[[ca:')
        if inici == -1:
            missatge = u'No existeix la plantilla en català'
            print missatge
        else:
            final = plantilla_ori.find(u'}}',inici)
            missatge = plantilla_ori[inici:final+2]
        return missatge

    def gestiona_codi(self, valor0):
        """Gestiona el codi tancat entre < > que no són referències"""
        print u'* PROCESSANT CODI WIKI *'
        nombre0 = int(valor0[6:])
        nombre1 = nombre0 + 1
        nombre1 = str(nombre1).zfill(4)
        nombre0 = str(nombre0).zfill(4)
        valor1 = valor0[:6] + unicode(nombre1) + u' '
        if self.refs[valor0][1:] == self.refs[valor1][2:]:
            inici = self.text_trad.find(valor0)
            final = self.text_trad.find(valor1)
            nou_text = self.text_trad[inici:final]
            self.text_trad = self.text_trad.replace(nou_text, valor0)
            nou_text = nou_text.replace(valor0, u'')
            self.count = 0
        else:
            print valor0
            print u'¿?¿?¿?¿?¿? COMPTE, AQUEST CODI WIKI ENCARA NO ESTÂ IMPLEMENTAT ¿?¿?¿?¿?¿?'
            print self.refs[valor0]
            raw_input (u'Seguim?')
            nou_text = valor0
        return nou_text
