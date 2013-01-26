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
from registre import Registre
from apertium import Traductor
from enllacos import Enllacos
from ref import Ref
import wikipedia
import httplib, urllib2, urllib
import json
from BeautifulSoup import BeautifulSoup
import requests
import time

class Text(Traductor, Enllacos):

    def canviar_text(self, text):
        """Gestiona el text de forma que crida al processament de codi wiki
        en aquest ordre:
        1.- Plantilles. Són substituïdes per REFP
        2.- Enllaços. Només se sustitueixen els enllaços web i els fitxers
        3.- Les referències. Se substitueixen per REFR

        Cal tenir en compte que les marques REF quedaran amb un asterisc per no saber la seva traducció."""
        print u'*** NETEJA DE TEXT ***'
        inici = 0
        count = 1
        text = self.cerca_comentaris(text)
        text = self.cerca_plantilles(text)
        text = self.cerca_enllacos(text)
        text = self.cerca_referencies(text)
#        self.ordena_diccionari(self.refs)
        text = text.encode('utf-8')
        print text
        raw_input('Seguim?')
        inici = text.find('\n==')
        capitol = text[:inici]
        self.traductor(capitol)
        time.sleep(10)
        arxiu_traduit = open('traduccio.html', 'r')
        text_traduit = arxiu_traduit.read()
        arxiu_traduit.close()
#        prec = raw_input('Vols veure el text traduit?\n[S]/n : ')
#        if prec != 'n':
#            print text_traduit
        while text.count('\n==',inici) != 0:
            count += 1
            inici = text.find('\n==',inici)
            final = text.find('==\n', inici)
            final = final +3
            final = text.find('\n==',final)
            capitol = text[inici:final]
            self.traductor(capitol)
            inici = final
            time.sleep(10)
            arxiu_traduit = open('traduccio.html', 'r')
            text_traduit = text_traduit + arxiu_traduit.read()
            arxiu_traduit.close()
#            prec = raw_input('Vols veure el text traduit?\n[S]/n : ')
#            if prec != 'n':
#                print text_traduit
        print text_traduit
        return text_traduit
