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

import wikipedia, codecs, re, catlib
import  httplib, time, urllib
from time import strftime as date

# Importar els altres arxius
from registre import Registre
from plantilles import Plantilles
from apertium import Traductor
from text import Text
from ref import Ref


class Amical(Plantilles,Text, Traductor,Ref):

    def arrenca(self):
        print
        print u'////////////////////////////'
        print u'///**********************///'
        print u'///* ARRENCA AMICAL BOT *///'
        print u'///**********************///'
        print u'////////////////////////////'
        print
        self.inici()

    def variables(self):
        """Definim les variables globals"""
        self.refs = {}
        self.llista_plantilles = []
        self.llista_enllacos = []
        self.llista_refs = []
        self.titol_original = ''
        self.idioma_original = ''
        self.usuari_peticio = ''
        self.diccionari_peticio = {'a_idioma' : self.idioma_original,
                    'b_titol' : self.titol_original,
                    'c_usuari' : self.usuari_peticio,
                    'd_par1' : '',
                    'e_par2' : '',
                    'f_par3' : '',
                    'g_par4' : '',
                    'h_par5' : '',
                    'i_par6' : ''}
        self.parametres = 0
        self.conta_plant = 0
        self.diccionari_cat = {u'en' : u'[[Category:',
                               u'es' : u'[[Categoría:',
                               u'fr' : u'[[Catégorie:',
                               u'de' : u'[[Kategorie:'}
        self.ordena = { 'en' : u'DEFAULTSORT',
                         'es' : u'ORDENAR',
                         'fr' : u'DEFAULTSORT'}
<<<<<<< HEAD

=======
>>>>>>> 1faf3bd32661f0382917c65bd9c5c0163b0b7546
    def inici(self):
        peticions = 1
        arxiu = open(u'passos.txt', 'w')
        arxiu.write('')
        arxiu.close()
        projecte = wikipedia.getSite()
        cat = catlib.Category(projecte, u"Categoria:Peticions de còpia i preprocés per traducció automàtica")
        pagines = cat.articles()
        for pagina in pagines:
            self.variables()
            titol = pagina.title()
            print '***********************************************************************************************************************'
            print '***********************************************************************************************************************'
            print  u'**********        ',peticions,u'.- COMENÇA EL PROCÉS  per la petició que es troba a ->',titol,u'        **********'
            print '***********************************************************************************************************************'
            print '***********************************************************************************************************************'
            self.titol = titol.encode('utf-8')
            print pagina
            text_ca = pagina.get()
            self.cerca_plantilles(text_ca)
            pagina_trad = wikipedia.Page(self.diccionari_peticio['a_idioma'],self.diccionari_peticio['b_titol'])
            print pagina_trad
            self.canviar_text(pagina_trad.get())
            peticions +=1
            prec = raw_input('Seguim amb la següent petició?\n[S]/n :')
            if prec == 'n':
                return 0
        return 0

app = Amical()
app.arrenca()
