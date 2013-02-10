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
import os
import subprocess
import sys

#################
# AVISOS A WIKI #
#################

class Avisos:

    def avisar_usuari(self, pagina):
        """Es deixa un missatge a la pàgina de discussió de l'usuari
        per comunicar que la traducció s'ha completat"""
        if self.proves:
            enllac_pagina = u'[['+pagina+u'|aquesta pàgina de proves]]'
            missatge_bot = u'Anskarbot EN FASE DE PROVES '
        else:
            enllac_pagina = u'[['+pagina+u']]'
            missatge_bot = u'Anskarbot '
        missatge = u"\n== Petició de traducció ==\n*La vostra petició de traducció de l'article " + self.titol_original + u" es troba a " + enllac_pagina + u". Quan repasseu la traducció podeu fer suggeriments de millora a [[Usuari:Anskarbot/Errors|la pàgina de millores del bot]] per anar millorant la traducció. Gràcies. --~~~~\n"
        pagina = wikipedia.Page(u'ca', self.discussio_usuari)
        p = re.compile(u'\n== Petició de traducció ==\n')
        pagina_discusio = pagina.get()
        if p.search(pagina_discusio):
            pagina_discusio = p.sub(missatge,pagina_discusio,1)
        else:
            pagina_discusio = pagina_discusio+missatge
        # ATENCIÓ, NO EM DEIXA GRAVAR A AQUESTA PÀGINA PERQUE ESTÀ REDIRIGIDA ¿?
        pagina.put(pagina_discusio, missatge_bot + u'enviant missatge sobre petició de traducció automàtica', minorEdit = False, force=True)
        index = u'Usuari:Anskarbot/Traduccions'
        index = wikipedia.Page(u'ca',index)
        contingut_index = index.get()
        index.put(contingut_index+u'\n* [[/'+self.titol_original+']]. {{u|'+self.usuari_peticio+u'}}\n', missatge_bot + u"creant l'índex de les traduccions fetes")

    def paraules(self, idioma):
        pagina = u'Usuari:Anskarbot/'+idioma
        text_pagina = wikipedia.Page(u'ca', pagina)
        text_pagina = text_pagina.get()
        for paraules_no_trad in self.llista_no_trad:
            text_pagina += paraules_no_trad+u'\n'
        pagina.put(text_pagina, u"Anskarbot escribint la llista de paraules que no s'han pogut traduir", minorEdit=False, force=True)
        self.passos(text_pagina, u'paraules que no es troben dins Apertium per ser traduides')

#######################
# ACABA AVISOS A WIKI #
#######################

######################################
# CANVIS DE TRADUCCIÓ POST TRADUCTOR #
######################################

class Canvis:

    def pagina_re(self):
        pass

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
        1000 : u'M'}
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

############################################
# ACABA CANVIS DE TRADUCCIÓ POST TRADUCTOR #
############################################

######################
# TRADUCTOR APERTIUM #
######################

class Traductor:

    def traductor(self, text):
        original = open('traduccions/original.txt', 'w')
        print u'Traduint...: '
        print text
        text = text.encode('utf-8')
        original.write(text)
        original.close()
        if self.idioma_original == 'en':
            text_trad = subprocess.call(['apertium en-ca traduccions/original.txt traduccions/traduccio.txt'], shell = True)
        elif self.idioma_original == 'es':
            text_trad = subprocess.call(['apertium es-ca traduccions/original.txt traduccions/traduccio.txt'], shell = True)
        elif self.idioma_original == 'fr':
            text_trad = subprocess.call(['apertium fr-ca traduccions/original.txt traduccions/traduccio.txt'], shell = True)
        elif self.idioma_original == 'pt':
            text_trad = subprocess.call(['apertium pt-ca traduccions/original.txt traduccions/traduccio.txt'], shell = True)
        elif self.idioma_original == 'oc':
            text_trad = subprocess.call(['apertium oc-ca traduccions/original.txt traduccions/traduccio.txt'], shell = True)
        arxiu_traduit = open(u'traduccions/traduccio.txt', 'r')
        text_traduit = arxiu_traduit.read()
        arxiu_traduit.close()
        text_traduit = unicode(text_traduit.decode('utf-8'))
        print text_traduit
        print u'Traducció acabada'
        return text_traduit

############################
# ACABA TRADUCTOR APERTIUM #
############################

############################
# REGISTRE D'ESDEVENIMENTS #
############################

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

##################################
# PROCESSA LA DIVERSITAT DE CODI #
##################################

class Gestio:

    def gestiona_commons(self, enllac):
        """Gestiona els fitxers de commons"""
        print u'* PROCESSANT UN FITXER DE COMMONS *'
        enllac = enllac[2:-2]
        enllac = enllac.replace(u'File:' , u'Fitxer:')
        if enllac.find('REF') != -1:
            marca = re.findall(r' REF\w+\d+?', enllac)
            for ref in marca:
                ref = ref+u' '
                if ref.startswith(u' REFEA'):
                    canvi = self.gestiona_enllac(self.refs[ref])
                    enllac = enllac.replace(ref, canvi)
        marca_enllac = enllac.rfind(u'|')
        if marca_enllac != -1:
            text = enllac[marca_enllac+1:]
            text_traduit = self.traductor(text)
            enllac = enllac.replace(text,text_traduit)
        return u'[[' + enllac + u']]'

    def gestiona_enllac(self, enllac):
        """Gestiona els enllaços de text"""
        print u'* PROCESSANT UN ENLLAÇ DE TEXT *'
        print enllac
        enllac = enllac[2:-2]
        if enllac.find(u'|') != -1:
            marca = enllac.find(u'|')
            enllac_ori = enllac[:marca]
            text = enllac[marca+1:]
            text_trad = self.traductor(text)
        else:
            text_trad = self.traductor(enllac)
        try:
            pagina_enllac = wikipedia.Page(self.idioma_original,enllac)
            enllac_ori = pagina_enllac.get()
        except:
            missatge = u'És un enllaç vermell'
            enllac_ori = ''

        if enllac_ori.count(u'[[ca:') == 1:
            inici = enllac_ori.find(u'[[ca:')
            final = enllac_ori.find(u']]',inici)
            enllac_trad = enllac_ori[inici+5:final]
            enllac1 = enllac_trad[0].lower()
            enllac_trad1 = enllac1+enllac_trad[1:]
            text_trad = text_trad.replace(u'*',u'')
            if enllac_trad.lower() == text_trad.lower():
                enllac = u'[['+text_trad+']]'
            else:
                enllac = u'[['+enllac_trad1+u'|'+text_trad+u']]'
        else:
            enllac = text_trad
        return enllac

    def gestiona_plantilles(self, plantilla, key):
        """Gestiona les plantilles"""
        print u'* PROCESSANT UNA PLANTILLA *'
        if self.web:
            plantilla_ca = self.plant_ca(plantilla, self.idioma_original)
            if plantilla_ca.startswith(u'No'):
                missatge = plantilla+u"<ref group=nt>La plantilla no existeix en català, o almenys, no s'ha pogut trobar automàticament. En cas que trobeu la corresponent plantilla ja traduda poseu-hi l'enllaç interviqui per poder trobar-la en següents traduccions.</ref>"
                return missatge
            else:
                inici = plantilla_ca.rfind(u':')
                plantilla_ca = plantilla_ca[inici+1:-2]
                final = plantilla.find(u'|')
                plantilla = plantilla.replace(plantilla[2:final], plantilla_ca)
        return plantilla

    def plant_ca(self, plantilla, idioma):
        """Cerca la plantilla a ca:viquipedia respecte la plantilla original"""
        print u'* Cercant la plantilla en català *'
        plantilla = plantilla[2:-2]
        plantilla = plantilla.split(u'|')
        if plantilla[0].find(u'#') != -1:
            return u'No és una plantilla'
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
            print u"Aquesta plantilla no té pàgina d'ús"
        inici = plantilla_ori.find(u'[[ca:')
        if inici == -1:
            missatge = u'No existeix la plantilla en català'
            print missatge
        else:
            final = plantilla_ori.find(u']]',inici)
            missatge = plantilla_ori[inici:final+2]
        return missatge

    def gestiona_taules(self, taula):
        print u'* GESTIONANT TAULA *'
        taula = taula.replace(u'{|', u' INICI ')
        taula = taula.replace(u'|}', u' FINALMENT ')
        taula = taula.replace(u'|+', u' CAPÇALERA ')
        taula = taula.replace(u'|-', u' CANVI ')
        taula = taula.replace(u'|', u' BARRA ')
        taula = taula.replace(u'!', u' ADMIRACIO ')
        taula = self.traductor(taula)
        self.passos(taula,u'Linia de la taula')
        taula = taula.replace(u'*' , u'')
        marca = re.findall(r' REF\w+[\S]', taula)
        for ref in marca:
            ref = ref+u' '
            if ref.startswith(u' REFEA'):
                canvi = self.gestiona_enllac(self.refs[ref])
                taula = taula.replace(ref, canvi)
            elif ref.startswith(u' REFEC'):
                canvi = self.gestiona_commons(self.refs[ref])
                taula = taula.replace(ref, canvi)
            elif ref.startswith(u' REFEW'):
                u'* PROCESSANT ENLLAÇ WEB *'
                nou_text = self.refs[ref]
                inici = nou_text.find(u' ')
                nou_text = nou_text.replace(nou_text[inici:], self.traductor(nou_text[inici:]))
                taula = taula.replace(ref, nou_text)
            elif ref.startswith(u' REFR'):
                print u'* PROCESSANT REFERÈNCIES *'
                nou_text = self.refs[ref]
                inici = nou_text.find(u'>')
                final = nou_text.find(u'</')
                nou_text = nou_text.replace(nou_text[inici+1:final], self.traductor(nou_text[inici+1:final]))
                taula = taula.replace(ref, nou_text)
            elif ref.startswith(u' REFPL'):
                canvi = self.gestiona_plantilles(self.refs[ref], ref)
                taula = taula.replace(ref, canvi)
            elif ref.startswith(u' REFCO'):
                print u'* PROCESSANT UN COMENTARI *'
                nou_text = self.refs[ref]
                nou_text = self.traductor(nou_text[4:-3])
                taula = taula.replace(ref, nou_text)
        taula = taula.replace(u' INICI ' , u'{|')
        taula = taula.replace(u' FINALMENT ' , u'|}')
        taula = taula.replace(u' CAPÇALERA ' , u'|+')
        taula = taula.replace(u' CANVI ' , u'|-')
        taula = taula.replace(u' BARRA ' , u'|')
        taula = taula.replace(u' ADMIRACIO ' , u'!')
        return taula

########################################
# ACABA PROCESSA LA DIVERSITAT DE CODI #
########################################

##########################################
# GESTIONA ELS DICCIONARIS DEL PROGRAMA #
##########################################

class Diccionaris:

    def peticio(self, plantilla, par=0):
        """Gestiona la plantilla de petició"""
        print u'* PLANTILLA DE PETICIÓ DE TRADUCCIÓ *'
        final = plantilla.find('}}')
        plantilla = plantilla[2:final].split('|')
        self.idioma_original = plantilla[1].lower()
        self.titol_original = plantilla[2]
        for valor in plantilla:
            print valor
            if valor.count(u'--[[Usuari:') != 0:
                marca = u'[[Usuari:'
                inici = valor.find(marca)
                valor = valor[inici+len(marca):]
                self.usuari_peticio = valor
                print valor
                raw_input('Seguim')
            elif valor.count(u'([[Usuari Discussió:') != 0:
                inici = valor.find(u'Usuari Discussió:')
                self.discussio_usuari = valor[inici:]
                print self.discussio_usuari
                raw_input('Seguim')
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
            if valor.startswith(self.cerques[0][-1][:-3]):   # Comentaris
                print u'* PROCESSANT COMENTARI *'
                nou_text = u'<!--' + self.traductor(nou_text[4:-3]) + u'-->'
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[1][-1][:-3]): # Enllaços de text
                nou_enllac = self.gestiona_enllac(nou_text)
                dicc[valor] = nou_enllac
            elif valor.startswith(self.cerques[2][-1][:-3]): # Enllaços web
                print u'* PROCESSANT ENLLAÇ WEB *'
                inici = nou_text.find(u' ')
                nou_text = nou_text.replace(nou_text[inici:-1], self.traductor(nou_text[inici:-1]))
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[3][-1][:-3]): # Plantilles
                print nou_text
                nou_text = self.gestiona_plantilles(nou_text, valor)
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[4][-1][:-3]): # Referències úniques
                print u'* PROCESSANT REFERÈNCIES *'
                inici = nou_text.find(u'>')
                final = nou_text.find(u'</')
                nou_text = nou_text.replace(nou_text[inici+1:final], self.traductor(nou_text[inici+1:final]))
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[5][-1][:-3]): # Referències de grup (name o altres)
                print u'* PROCESSANT REFERÈNCIES DE GRUP *'
                inici = nou_text.find(u'>')
                final = nou_text.find(u'</')
                nou_text = nou_text.replace(nou_text[inici+1:final], self.traductor(nou_text[inici+1:final]))
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[6][-1][:-3]): # Següents ref name
                print u'* PROCESSANT REFERÈNCIES DE GRUP NAME *'
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[7][-1][:-3]): # Altre codi
                print u'* PROCESSANT ALTRE CODI *'
            elif valor.startswith(self.cerques[8][-1][:-3]): # Taules !! ENCARA FALTA
                print u'*** PROCESSANT TAULES ***'
                nou_text = self.gestiona_taules(nou_text)
                dicc[valor] = nou_text
            elif valor.startswith(u' REFZZ'): # Codi d'estils
                print u'* PROCESSANT ESTILS *'
            else: # Enllaços de commons que no tenen cabuda en la llista de tuples self.cerques però queden dins del diccionari selfs.ref
                nou_text = self.gestiona_commons(dicc[valor])
                dicc[valor] = nou_text
            self.passos([str(valor),dicc[valor]], 'Diccionari ordenat traduit:')

################################################
# ACABA GESTIONA ELS DICCI0NARIS DEL PROGRAMA #
################################################

########################################
# CERCA I SUBSTITUEIX EL DIFERENT CODI #
########################################

class PreCercaSubst:

    def cerca(self, text, par=0, inici=0, comm=0):
        """Cerca les marques de codi i les substitueix per REF"""
        print u'\n================================================================'
        dicc_refs = self.refs
        for cerca in self.cerques:
            inici_m = cerca[0]
            final_m = cerca[1]
            ref = cerca[2]
            par = 0
            print U'Cercant ',inici_m, final_m, u'per substituir-ho per la referència',ref
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
                if valor.startswith(u'[[File:') or valor.startswith(u'[[Image:'):
                    ref = u' REFEC%s '
                    comm = str(comm).zfill(4)
                    text = text.replace(valor, ref %(comm))
                    dicc_refs[ref %(comm)] = valor
                    self.passos(valor, u'Codi a canviar: '+ref %(comm))
                    comm = int(comm)
                    comm += 1
                    continue
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
        print u'================================================================'
        return text

##############################################
# ACABA CERCA I SUBSTITUEIX EL DIFERENT CODI #
##############################################

####################
# PROCESSA EL TEXT #
####################

class Text:

    def canviar_text(self, text, inici=0, cap=1, x=0, text_trad='', text_final='', ncodi=0):
        """Gestiona el text de forma que neteja el possible codi que pugui dificultar la traducció"""
        llista_net = []
        capitol_trad = []
        llista_notrad = []
        self.text = text
        self.passos(text, u'Aquest es el text a traduir:\n\n')
        text_ori = re.split(r'\n\n', self.text)
        for capitol in text_ori:
            capitol_ori = capitol
            print u'*** NETEJA DE CAPITOL ***'
            print capitol
            capitol = capitol.replace(u'\n*', u'\n* ') # La llista no numerada ha de contenir un espai entre l'asterisc i la frase...
            capitol = capitol.replace('*', ' ASTR ')
            capitol = re.sub(r"'{3}", " ''' ", capitol)
            capitol = re.sub(r"(?!')'{2}'", " '' ", capitol)
            capitol = capitol.replace(u'&ndash;',u'–')
            capitol = capitol.replace(u'&mdash;', u'—')
            codi = re.findall(r'[\w]+=".+?"',capitol)
            for estil in codi:
                ncodi = str(ncodi).zfill(4)
                valor = u' REFZZ%s ' %(ncodi)
                capitol = capitol.replace(estil, valor)
                self.refs[valor] = estil
                ncodi = int(ncodi) + 1
                self.passos(valor + u'\n' + estil, u'Codi no traduible' )
            codi = re.findall(r'<math>.+?</math>',capitol)
            ncodi = 0
            for mates in codi:
                ncodi = str(ncodi).zfill(4)
                valor = u' REFWM%s ' %(ncodi)
                capitol = capitol.replace(mates, valor)
                self.refs[valor] = mates
                ncodi = int(ncodi) + 1
                self.passos(valor + u'\n' + mates, u'Codi de formules matematiques' )
            self.text_trad = self.cerca(capitol)

            self.ordena_diccionari(self.refs)
            self.passos(self.text_trad, u'Aquest es el paragraf preparat per traduir:\n\n************************************************************************************************************************\n\n')

            paragraf = unicode(self.traductor(self.text_trad)+u'\n\n'.decode('utf-8'))
            print paragraf
            self.passos(capitol_ori, u'Angles original\n')
            self.passos(self.text_trad, u'Angles processat\n')
            self.passos(paragraf, u'Catala processat\n')
            paragraf = paragraf.replace(u'*REF',u'REF')
            no_trad = re.findall(r'\*\w+[\S]',paragraf)
            self.passos(no_trad, u'Llista de paraules no traduides')
            for paraula in no_trad:
                print paraula
                self.passos(paraula, u'Paraula no traduida')
                if paraula not in self.llista_no_trad:
                    print paraula
                    self.passos(paraula, u"Aquesta paraula no s'havia trobat fins ara")
                    self.llista_no_trad.append(paraula)
            self.passos(self.llista_no_trad, u'Llista de paraules que Apertium no tradueix')
            if paragraf.find('REF') != -1:
                text = self.refer_text(paragraf)
            else:
                print u"* NO S'HAN TROBAT REF PER CANVIAR *"
                text = paragraf
            while text.find('REF') != -1:
                print '*** ENCARA HI HA REF PER CANVIAR ***'
                text = self.refer_text(text)
            print '*** ACABAT ***\n'
            text = text.replace(u'*', u'')
            text = text.replace(u' ASTR ', u'*')
            text = text.replace(u" ''' ",u"'''")
            text = text.replace(u" '' ", u"''")
            text = text.replace(u' ,', u',')
            text = text.lstrip()
            self.passos(text, u'Catala net final')
            text_final += capitol_ori + u'\n\n' + text
            x += 1
            self.refs = {}
        while text_final.find(u'  ') != -1:
            text_final = text_final.replace(u'  ', u' ')
        #while text_final.find(u'\n ') != -1:
            #text_final = text_final.replace(u'\n ', u'\n')
        text_final = text_final+u'\n[['+self.idioma_original+u':'+self.titol_original+u"]]\n\n==Notes de traducció==\nLes plantilles en vermell són les plantilles que no s'ha pogut trobar la plantilla corresponent en català, això no vol dir que la plantilla no existeixi, sino que no s'ha pogut trobar automàticament per que no hi ha el corresponent enllaç interviqui, o per que realment no esxisteix la plantilla en català. En cas que trobeu la plantilla corresponent us agrairia que li posesiu el seu enllaç interviqui a la plantilla en anglès per poder trobar-la en properes traduccions. Gràcies."
        self.passos(text_final,u'\n***************\n** Text finalitzat **\n***************\n')
        return text_final

    def refer_text(self, text):
        """Canvia les referències de codi REF...... pel valor corresponent del diccionari self.refs"""
        print u'*** REFENT EL TEXT ***'
        marca = re.findall(r'REF\w+\d+?', text)
        for ref in marca:
            ref1 = u' '+ref+u' '
            print ref1
            text = text.replace(ref, self.refs[ref1])
            self.passos(self.refs[ref1], 'Canvi en el text: '+str(ref))
        return text

##########################
# ACABA PROCESSA EL TEXT #
##########################

#######################
# COMENÇA EL PROGRAMA #
#######################

class Amical(Text,PreCercaSubst,Diccionaris,Gestio,Registre,Traductor,Avisos,Canvis):

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
                       (u'{{',u'}}', u' REFPL%s '),            # La tupla consta de tres paràmetres:
                       (u'<ref>' , u'</ref>', u' REFRE%s '),   # 1: El primer terme de cerca, (p.e. {{ com a primer terme)
                       (u'<ref', u'</ref>', u' REFRI%s '),     # 2: El darrer terme de cerca, (ha de trobar }} com a darrer terme)
                       (u'<ref name' , u'/>' , u' REFSR%s '),  # 3: La referència que substitueix el codi trobat
#                       (u'<nowiki>' , u'</nowiki>' , u' REFSA%s '),    # És important que la marca REFxx segueixi un ordre alfabètic
#                       (u'<div' , u'</div>' , u' REFSA%s '),           # per gestionar el diccionari de referències en l'ordre correcte
                       (u'<' , u'>' , u' REFWC%s '),                   # de forma qualsevol codi inserit dins un altre codi es gestioni primer el que es troba dins un altre,
                       (u'{|',u'|}', u' REFZT%s ')                     # per això el comentari <!-- --> és el primer en gestionar-se i les taules {| }| l'últim de tots.
                       ]
        self.titol_original = ''   # Variables que defineixen la plantilla de petició de traducció
        self.idioma_original = ''  # a saber: titol original de la pàgina que es vol traduir
        self.usuari_peticio = ''   # idioma original i l'usuari que demana la traducció
        self.discussio_usuari = ''
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
        self.cops_k_passa = 0 # Variable global que gestiona el nombre amb que es registra un procés a l'arxiu registre.txt
        self.llista_no_trad = []

    def inici(self, peticions=2, gravar_viqui=False, proves=True, web=False):
        """Comença el programa.
        Els arguments que accepta la funció són:
        1.- peticions: el nombre de la primera petició.
            S'ha de posar aquí la variable per poder cridar-la sense error.
        2.- gravar_viqui: És la variable que permet gravar el resultat a la viqui o no.
            Per defecte es posa False ja que està en fase de proves.
        3.- proves: Mentre estigui en fase de proves no es borrarà la plantilla de petició
            i es posarà el text a la viqui en una pàgina de proves expressa
            per anar provant el bot. True per defecte"""
        self.web = web
        gravar_viqui = raw_input(u"Per defecte els canvis no seran gravats a la viqui.\nEn cas que es vulgui gravar el resultat de la traducció automàticament haureu d'escriure 'True' en aquesta pregunta:\n** Vols gravar els canvis a la pàgina corresponent de la viquipèdia? **:\nTrue/[False]".encode('utf-8'))
        projecte = wikipedia.getSite()
        cat = catlib.Category(projecte, u"Categoria:Peticions de còpia i preprocés per traducció automàtica")
        pagines = cat.articles()
        for pagina in pagines:
            self.variables()
            titol = pagina.title()
            print '*********************************************************************************************************************************'
            print '*********************************************************************************************************************************'
            print  (u'*****  '+str(peticions)+u'.- COMENCA EL PROCES  per la peticio que es troba a ->'+unicode(titol)+u'  *****').center(118)
            print '*********************************************************************************************************************************'
            print '*********************************************************************************************************************************'
            self.titol = titol.encode('utf-8')
            print pagina #Pàgina que té la petició de traducció
            text_ca = pagina.get()
            self.peticio(text_ca)
            pagina_trad = wikipedia.Page(self.idioma_original,self.titol_original)
            print pagina_trad
            self.text_trad = pagina_trad.get()
            print u"\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
            print (u"% EL REGISTRE ES TROBA A registre-"+unicode(self.titol_original)+".txt %").center(90)
            print u"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
            text = self.canviar_text(self.text_trad)
            print u'\n****************************************'
            print u'********** ACABADA LA PETICIÓ **********'
            print u'****************************************\n'
            if gravar_viqui:
                pagina_final = u'Usuari:Anskarbot/Traduccions/'+unicode(self.titol_original)
                self.proves = proves
                pagina_gravar = wikipedia.Page(u'ca',pagina_final)
                pagina_gravar.put(text, u"Anskarbot EN FASE DE PROVES generant una nova traducció automàtica", minorEdit = False, force=True)
                self.avisar_usuari(pagina_final)
                self.passos(pagina_final, u'Pagina on es grava el text:')
                self.paraules(self.idioma_original)
            if proves:
                raw_input('Seguim?')
            peticions +=1
        print u'\nOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
        print (u'OOOOO   ACABADES LES TRADUCCIONS   OOOOO').center(60)
        print u'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
        return 0

try:
    app = Amical()
    app.arrenca()
finally:
    wikipedia.stopme()

####################
# THAT'S ALL FOLKS #
####################
