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

class Avisos:

    def avisar_usuari(self):
        """Es deixa un missatge a la pàgina de discussió de l'usuari
        per comunicar que la traducció s'ha completat"""
        missatge = u"\n== Petició de traducció ==\n*La vostra petició de traducció de l'article " + self.titol_original + " es troba a [[" + self.titol + u"|la pàgina on tenieu la plantilla de petició de traducció]]. --~~~~\n"
        pagina = wikipedia.Page(u'ca', self.discussio_usuari)
        p = re.compile(u'\n== Petició de traducció ==\n')
        pagina_discusio = pagina.get()
        if p.search(pagina_discusio):
            pagina_discusio = p.sub(missatge,pagina_discusio,1)
        else:
            pagina_discusio = pagina_discusio+missatge
        pagina.put(pagina_discusio,u'bot enviant missatge sobre petició de traducció automàtica', minorEdit = False)

class Canvis:

    def romans(self, nombre,divisio_anterior=0):
        """Canvia un nombre àrab a nombres romans.
        No pot ser major de 3999"""
        nombre = int(nombre)
        if nombre > 3999:
            print 'No pot ser més gran de 3999.... encara'
            return
        dicc = {0 : '',
        1 : u'I',
        5 : u'V',
        10 : u'X',
        50 : u'L',
        100 : u'C',
        500 : u'D',
        1000 : u'M',
        5000 : u'\u0305U'}
        romans = dicc[0]
        ordre = sorted(dicc.keys(),reverse = True)
        portem = -1
        for marca in ordre:
            portem +=1
            if marca == 0 or marca >5000:
                continue
            divisio = nombre/marca
            if divisio == 4:
                if divisio_anterior == 1:
                    romans = romans[:-1]+unicode(dicc[ordre[portem]]+dicc[ordre[portem-2]])
                else:
                    romans += unicode(dicc[ordre[portem]]+dicc[ordre[portem-1]])
                nombre = nombre - (divisio*marca)
                continue
            divisio_anterior = divisio
            nombre = nombre - (divisio*marca)
            romans += unicode(divisio*dicc[marca])
        print romans
        return romans

class Traductor:

    def traductor(self, text):
        original = open('traduccions/original.txt', 'w')
        print u'Traduint...: '
        text = text.encode('utf-8')
        original.write(text)
        original.close()
        if self.idioma_original == 'en':
            text_trad = subprocess.call(['apertium en-ca traduccions/original.txt traduccions/traduccio.txt'], shell=True)
        elif self.idioma_original == 'es':
            text_trad = subprocess.call(['apertium es-ca traduccions/original.txt traduccions/traduccio.txt'], shell=True)
        elif self.idioma_original == 'fr':
            text_trad = subprocess.call(['apertium fr-ca traduccions/original.txt traduccions/traduccio.txt'], shell=True)
        elif self.idioma_original == 'pt':
            text_trad = subprocess.call(['apertium pt-ca traduccions/original.txt traduccions/traduccio.txt'], shell=True)
        arxiu_traduit = open(u'traduccions/traduccio.txt', 'r')
        text_traduit = arxiu_traduit.read()
        arxiu_traduit.close()
        text_traduit = unicode(text_traduit.decode('utf-8'))
        print u'Traducció acabada'
        return text_traduit

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

class Gestio:

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

class Plantilles:

    def peticio(self, plantilla, par=0):
        """Gestiona la plantilla de petició"""
        print u'* PLANTILLA DE PETICIÓ DE TRADUCCIÓ *'
        final = plantilla.find('}}')
        plantilla = plantilla[1:final].split('|')
        self.idioma_original = plantilla[1].lower()
        self.titol_original = plantilla[2]
        for valor in plantilla[1:]:
            print valor
            if valor.count(u'--[[Usuari:') != 0:
                valor = valor[4:]
                self.usuari_peticio = valor
            elif valor.count(u'([[Usuari Discussió:') != 0:
                inici = valor.find(u'Usuari Discussió:')
                self.discussio_usuari = valor[inici:]
        self.passos(plantilla, u'Plantilla de peticio de traduccio')

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

class PreCercaSubst:

    def cerca(self, text, par=0, inici=0, comm=0):
        """Cerca les marques de codi i les substitueix per REF"""
        dicc_refs = self.refs
        for cerca in self.cerques:
            inici_m = cerca[0]
            final_m = cerca[1]
            ref = cerca[2]
            par = 0
            print U'Cercant ',inici_m, final_m, u'per substituir-ho per la referència ',ref
            while text.find(inici_m) != -1:
                ref = cerca[2]
                par = str(par).zfill(4)
                inici = text.find(inici_m)
                final = text.find(final_m, inici)
                while text.count(inici_m,inici,final+len(final_m)) != text.count(final_m,inici,final+len(final_m)):
                    inici2 = text.find(inici_m,inici+len(inici_m),final)
                    valor = text[inici2:final+len(final_m)]
                    text = text.replace(valor, ref %(par))
                    dicc_refs[ref %(par)] = valor
                    final = text.find(final_m,final+len(final_m))
                    self.passos(valor, u'Codi a canviar: '+ref %(par))
                    final = text.find(final_m)
                    par = int(par)
                    par += 1
                    par = str(par).zfill(4)
                valor = text[inici:final+len(final_m)]
                if valor.startswith(self.diccionari_cat[self.idioma_original]):
                    self.passos(valor, u"Es una categoria, s'esborra fins al final del text")
                    text = text.replace(text[inici:], '')
                elif valor.startswith(u'[[File:') or valor.startswith(u'[[Image:'):
                    ref = u' REFEC%s '
                    comm = str(comm).zfill(4)
                    text = text.replace(valor, ref %(comm))
                    dicc_refs[ref %(comm)] = valor
                    self.passos(valor, u'Codi a canviar: '+ref %(comm))
                    comm = int(comm)
                    comm += 1
                    continue
                elif valor[2:].startswith(self.ordena[self.idioma_original]):
                    text = text.replace(text[inici:], '')
                    self.passos(valor, u"Es la plantilla {{ORDENA, s'esborra fins al final del text")
                elif valor is u'':
                    print u'Què passa aqui?', ref
                    print inici, final+len(final_m)
                    print text[inici-40:inici+80]
                    break
                else:
                    text = text.replace(valor, ref %(par), 1)
                    dicc_refs[ref %(par)] = valor
                    self.passos(valor, u'Codi a canviar: '+ref %(par))
                par = int(par)
                par += 1
        return text

class Text:

    def canviar_text(self, text, inici=0, cap=1, x=0, text_trad='', text_final=''):
        """Gestiona el text de forma que neteja el possible codi que pugui dificultar la traducció"""
        self.text = text
        self.passos(text, u'Aquest es el text a traduir:\n\n')
        print u'*** NETEJA DE TEXT ***'
#        text = text.replace(u"'''", u'') # Es treuen les marques de text en negreta
#        text = text.replace(u"''", u'') # Es treuen les marques de text en cursiva
        text = text.replace(u'\n*', u'\n* ') # La llista no numerada ha de contenir un espai entre l'asterisc i la frase...
        text = text.replace('*', ' ASTR ')
        text = text.replace(u'&ndash;',u'–')
        text = text.replace(u'&mdash;', u'—')'-'
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

class Amical(Text,PreCercaSubst,Plantilles,Gestio,Registre,Traductor,Avisos,Canvis):

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

    def inici(self, peticions=1, put=False):
        """Comença el programa"""
        put = raw_input(u"Per defecte els canvis no seran gravats a la viqui.\nEn cas que es vulgui gravar el resultat de la traducció automàticament haureu d'escriure 'True' en aquesta pregunta:\n** Vols gravar els canvis a la pàgina corresponent de la viquipèdia? **:\nTrue/[False]")
        projecte = wikipedia.getSite()
        cat = catlib.Category(projecte, u"Categoria:Peticions de còpia i preprocés per traducció automàtica")
        pagines = cat.articles()
        for pagina in pagines:
            self.variables()
            self.titol = pagina.title()
            print '*********************************************************************************************************************************'
            print '*********************************************************************************************************************************'
            print  (u'*****  '+str(peticions)+u'.- COMENCA EL PROCES  per la peticio que es troba a ->'+unicode(self.titol)+u'  *****').center(118)
            print '*********************************************************************************************************************************'
            print '*********************************************************************************************************************************'
            print pagina #Pàgina que té la petició de traducció
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
            if put:
                pagina_gravar = wikipedia.Page(u'ca',u'Usuari:Anskar/Traduccions/'+unicode(str(peticions)))
                pagina_gravar.put(text, u"bot generant una nova traducció automàtica", minorEdit = False)
                self.avisar_usuari()
            peticions +=1
        print u'\nOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
        print (u'OOOOO   ACABADES LES TRADUCCIONS   OOOOO').center(60)
        print u'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
        return 0

app = Amical()
app.arrenca()
