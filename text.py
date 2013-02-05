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

class Text():

    def canviar_text(self, text, inici=0, cap=1, x=0, text_trad='', text_final=''):
        """Gestiona el text de forma que neteja el possible codi que pugui dificultar la traducció"""
        self.text = text
        self.passos(text, u'Aquest es el text a traduir:\n\n')
        print u'*** NETEJA DE TEXT ***'
#        text = text.replace(u"'''", u'') # Es treuen les marques de text en negreta
#        text = text.replace(u"''", u'') # Es treuen les marques de text en cursiva
        text = text.replace(u'\n*', u'\n* ') # La llista no numerada ha de contenir un espai entre l'asterisc i la frase...
        text = text.replace('*', ' ASTR ')
        self.text_trad = self.cerca(text)
        self.ordena_diccionari(self.refs)
        self.passos(self.text_trad, u'Aquest es el text preparat per traduir:\n\n************************************************************************************************************************\n\n')
        marca = u'\n\n'
        text_ori = re.split(r'\n\n', self.text)
        text_trad = re.split(r'\n\n', self.text_trad)
        capitol_trad = []
        print len(text_ori)
        print len(text_trad)
        for capitol in text_trad:
            paragraf = unicode(self.traductor(capitol)+u'\n\n'.decode('utf-8'))
            capitol_trad.append(paragraf)
            self.passos(capitol, u'Angles\n')
            self.passos(paragraf, u'Catala\n')
            if paragraf.find('*REF') != -1:
                print u'*** REFENT EL TEXT ***'
                text = self.refer_text(paragraf)
            else:
                print u"* NO S'HAN TROBAT REF PER CANVIAR *"
                text = paragraf
            print '***** ACABAT EL PRIMER CANVI DE REFS *****'
            text = text.replace('REF', '*REF')
            if text.find('*REF') != -1:
                print '*** ENCARA HI HA REF PER CANVIAR ***'
                text = self.refer_text(text)
                print '*** ACABAT ***'
            text = text.replace(u'*', u'')
            text = text.replace(u'ASTR', u'*')
            while text.find(u'  ') != -1:
                text = text.replace(u'  ', u' ')
            while text.find(u'\n ') != -1:
                text = text.replace(u'\n ', u'\n')
            text_final += text_ori[x] + u'\n\n' + text
            x += 1
        text_final = text_final+u'\n==Notes de traducció==\n{{referències|group=nt}}\n\n[['+self.diccionari_peticio[u'a_idioma']+u':'+self.diccionari_peticio[u'b_titol']+u']]'
        self.passos(text_final,u'\n***************\n** Text finalitzat **\n***************\n')
        return text_final

    def refer_text(self, text):
        """Canvia les referències de codi REF...... pel valor corresponent del diccionari self.refs"""
        marca = re.findall(r'REF\w+[\S]', text)
        for ref in marca:
            ref1 = u' '+ref+u' '
            text = text.replace(ref, self.refs[ref1])
            self.passos(self.refs[ref1], 'Canvi en el text: '+str(ref))
        return text
