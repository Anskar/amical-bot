#!/usr/bin/env python
# -*- encoding: utf-8 -*-
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

from registre import Registre
import wikipedia

class Plantilles():

    def cerca_plantilles(self, text, inici=0, par= 0, contador=0):
        """Cerca {{ dins el text, les classifica i substitueix.
        Es marca amb l'etiqueta REFP"""
        print '*** CERCA PLANTILLES ***'
        while text.find('{{') != -1:
            inici = text.find('{{')
            final = text.find('}}', inici)
            plantilla = text[inici:final+2]
            self.llista_plantilles.append(plantilla)
            print plantilla
            context = text[inici-20:final+20]
            plantilla = plantilla[2:-2]
            plantilla = plantilla.split('|')
            plantilla.append(context)
            if plantilla[0] == u'Petició de traducció' or plantilla[0] == u'petició de traducció':
                self.peticio(plantilla)
                return
            else:
                plantilla.append(self.plant_ca(plantilla,self.idioma_original))
                for x in plantilla:
                    if x.count('=') != 0:
                        contador = 1
                if contador > 0 :
                    print u'* TAULA *'
                    plantilla = self.desfer_taules(plantilla)
                else:
                    print u'* PLANTILLA DE TEXT *'
            self.refs['*REFP%i' %(par)] = plantilla
            plantilla = text[inici:final+2]
            text = text.replace(plantilla, 'REFP%i' %(par))
            par += 1
        return text

    def peticio(self, plantilla):
        """Gestiona la plantilla de petició"""
        print u'* PLANTILLA DE PETICIÓ DE TRADUCCIÓ *'
        self.idioma_original = plantilla[1].lower()
        for valor in plantilla[1:]:
            print valor
            clau = self.diccionari_peticio.keys()
            clau.sort()
            if valor.count(u'--[[Usuari:') != 0:
                valor = valor[4:]
            self.diccionari_peticio[clau[self.conta_plant]] = valor
            self.conta_plant += 1
        self.conta_plant = 0

    def desfer_taules(self, plantilla):
        """Gestiona les plantilles de tipus parametre=valor"""
        llista_plantilla = []
        for esquema in plantilla:
            llista = esquema.split('=')
            llista_plantilla.append(llista)
        return llista_plantilla

    def plant_ca(self, plantilla, idioma):
        """Cerca la plantilla a ca:viquipedia respecte la plantilla original"""
        dicc_id = {u'en' : u'Template:',
                   u'fr' : u'Modèle:',
                   u'es' : u'Plantilla:',
                   u'de' : u'Vorlage'
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
            plantilla_ori = pagina_plantilla.get()
            missatge = u"Aquesta plantilla no té pàgina d'ús'"

        inici = plantilla_ori.find(u'[[ca:')
        if inici == -1:
            missatge = u'No existeix la plantilla en català'
            return missatge
        else:
            inici = plantilla_ori.find('[[ca:')
            final = plantilla_ori.find(']]',inici)
            missatge = plantilla_ori[inici:final+2]
            return missatge

    def ordena_diccionari(self, dicc):
        print u'\nDiccionari ordenat:'
        clau = dicc.keys()
        clau.sort()
        for x in clau:
            print u'*'+str(x)+u'*'
            print dicc[x]
