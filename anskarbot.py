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

import wikipedia, codecs, re, catlib
#import httplib, urllib
import time
import os
import subprocess
import sys

# Importar els altres arxius
from text import Text
from precerca import PreCercaSubst
from plantilles import Plantilles
from enllacos import Gestio
from registre import Registre
from apertium import Traductor

class Amical(Text,PreCercaSubst,Plantilles,Gestio,Registre,Traductor):

    def arrenca(self):
        """Només mostra aquest començament quan arrenca el bot desde consola.
        Apartat completament suprimible... però queda tant bufó... :P """
        print
        print u'////////////////////////////'.center(150)
        print u'///**********************///'.center(150)
        print u'///* ARRENCA AMICAL BOT *///'.center(150)
        print u'///**********************///'.center(150)
        print u'////////////////////////////'.center(150)
        print
        self.inici()

    def variables(self):
        """Definim les variables globals"""
        self.refs = {} # Diccionari dels codis processats abans de traduir
        self.cerques =[(u'<!--',u'-->', u' REFCO%s '), # Llista de tuples que ...
                       (u'[[',u']]', u' REFEA%s '),    # ... estableix el caràcter de cerca ...
                       (u'[http:',u']', u' REFEW%s '), # ... i el relaciona amb la referència que substituirà.
                       (u'{{',u'}}', u' REFPL%s '),                # La tupla consta de tres paràmetres:
                       (u'<ref>' , u'</ref>', u' REFRE%s '),       # 1: El primer terme de cerca, (p.e. {{ com a primer terme)
                       (u'<ref name' , u'</ref>' , u' REFRI%s '),  # 2: El darrer terme de cerca, (ha de trobar }} com a darrer terme)
                       (u'<ref name', u'/>', u' REFRN%s '),      # 3: La referència que substitueix el codi trobat
                       (u'{|',u'|}', u' REFTA%s '),
                       (u'<' , u'>' , u' REFWC%s ')
                        ]
        self.titol_original = ''   # Variables que defineixen la plantilla de petició de traducció
        self.idioma_original = ''  # a saber: titol original de la pàgina que es vol traduir
        self.usuari_peticio = ''   # idioma original i l'usuari que demana la traducció
        self.diccionari_peticio = {u'a_idioma' : self.idioma_original, # Diccionari de la plantilla de peticio de traduccio
                    u'b_titol' : self.titol_original,
                    u'c_usuari' : self.usuari_peticio,
                    u'd_par1' : '',
                    u'e_par2' : '',
                    u'f_par3' : '',
                    u'g_par4' : '',
                    u'h_par5' : '',
                    u'i_par6' : ''}
        self.diccionari_cat = {u'en' : u'[[Category',  # Diccionari per gestionar les categories
                               u'es' : u'[[Categoría', #... en els diferents idiomes possibles de traducció
                               u'fr' : u'[[Catégorie',
                               u'de' : u'[[Kategorie'}
        self.ordena = { u'en' : u'DEFAULTSORT', # Diccionari per gestionar la plantilla {{ORDENA ...
                        u'es' : u'ORDENAR',     #... en els diferents idiomes de traducció
                        u'fr' : u'DEFAULTSORT'}
        self.cops_k_passa = 0 # Variable global que gestiona el nombre de vegades que es registra un procés a l'arxiu registre.txt
        self.passa_codi = [u'<references/>', u'<br>']

    def inici(self, peticions=1):
        """Comença el programa"""
        projecte = wikipedia.getSite()
        cat = catlib.Category(projecte, u"Categoria:Peticions de còpia i preprocés per traducció automàtica")
        pagines = cat.articles()
        for pagina in pagines:
            self.variables()
            titol = pagina.title()
            print '***********************************************************************************************************************'
            print '***********************************************************************************************************************'
            print  (u'*****  '+str(peticions)+u'.- COMENCA EL PROCES  per la peticio que es troba a ->'+unicode(titol)+u'  *****').center(118)
            print '***********************************************************************************************************************'
            print '***********************************************************************************************************************'
            self.titol = titol.encode('utf-8')
            print pagina
            text_ca = pagina.get()
            self.peticio(text_ca)
            pagina_trad = wikipedia.Page(self.diccionari_peticio[u'a_idioma'],self.diccionari_peticio[u'b_titol'])
            print pagina_trad
            self.text_trad = pagina_trad.get()
            print u"\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
            print (u"% EL REGISTRE ES TROBA A registre-"+unicode(self.titol_original)+".txt %").center(90)
            print u"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
            text = self.canviar_text(self.text_trad)
            print u'\n****************************************'
            print u'********** ACABADA LA PETICIÓ **********'
            print u'****************************************\n'
            pagina_gravar = wikipedia.Page(u'ca',u'Usuari:Anskar/Traduccions/'+unicode(str(peticions)))
            pagina_gravar.put(text)
            peticions +=1
            prec = raw_input('Seguim amb la següent petició?\n[S]/n :')
            if prec == 'n':
                return 0
        print u'\nOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
        print (u'OOOOO   ACABADES LES TRADUCCIONS   OOOOO').center(60)
        print u'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
        return 0

app = Amical()
app.arrenca()
