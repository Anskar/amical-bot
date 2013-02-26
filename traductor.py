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
import pywikibot
import string


#################
# AVISOS A WIKI #
#################

class Avisos:

    def avisar_usuari(self, pagina,enllac_pagina, missatge_bot):
        """Es deixa un missatge a la pàgina de discussió de l'usuari
        per comunicar que la traducció s'ha completat"""
        if self.discussio_usuari == '':
            falta = u" --~~~~\n*Recorda de signar les peticions de traducció, ja que si no és impossible que una màquina com jo sàpiga qui demana la traducció. Gràcies."
            self.discussio_usuari = self.titol
        else:
            falta = ''
        missatge = u"\n== Petició de traducció ==\n*La vostra petició de traducció de l'article '''" + self.titol_original + u"''' es troba en " + enllac_pagina + u". Quan repasseu la traducció podeu fer suggeriments de millora a [[Usuari:Anskarbot/Errors|la pàgina de millores del bot]] per anar millorant la traducció. Gràcies."+falta+u" --~~~~\n"
        pagina = wikipedia.Page(u'ca', self.discussio_usuari)
        p = re.compile(u'\n== Petició de traducció ==\n')
        pagina_discusio = pagina.get()
        if p.search(pagina_discusio):
            pagina_discusio = p.sub(missatge,pagina_discusio,1)
        else:
            pagina_discusio = pagina_discusio+missatge
        # ATENCIÓ, NO EM DEIXA GRAVAR A AQUESTA PÀGINA PERQUE ESTÀ REDIRIGIDA ¿?
        pagina.put(pagina_discusio, missatge_bot + u'enviant missatge sobre petició de traducció automàtica', minorEdit = False, force=True)

    def paraules(self, idioma):
        """Grava les paraules que Apertium no pot traduir"""
        pagina = u'Usuari:Anskarbot/'+idioma
        pagina = wikipedia.Page(u'ca', pagina)
        text_pagina = pagina.get()
        for paraules_no_trad in self.no_trad:
            text_pagina += u'\n'+paraules_no_trad
        pagina.put(text_pagina, u"Anskarbot escribint la llista de paraules que no s'han pogut traduir", minorEdit=False, force=True)
        self.passos(text_pagina, u'paraules que no es troben dins Apertium per ser traduides')

    def discussio(self, pagina):
        pagina = pagina.replace(u'Usuari:', u'Usuari Discussió:')
        urlversio =wikipedia.Page(self.idioma_original,self.titol_original).permalink()
        versio = re.findall(r'oldid=(\d+)',urlversio)
        pagina.put(u'{{Traduït de|'+self.idioma_original+u'|'+self.titol_original+u'|{{subst:CURRENTDAY}}-{{subst:CURRENTMONTH}}-{{subst:CURRENTYEAR}}|'+versio+u'}}', u'Anskarbot incorporant la plantilla {{traduït de}} a la pàgina de discussió',minorEdit=False, force=True)

#######################
# ACABA AVISOS A WIKI #
#######################

######################################
# CANVIS DE TRADUCCIÓ POST TRADUCTOR #
######################################

class Canvis:

    def pagina_re(self, text, dicc):
        """Reemplazo múltiple de cadenas en Python."""
        print dicc
        regex = re.compile("(%s)" % "|".join(map(re.escape, dicc.keys())))
        return regex.sub(lambda x: unicode(dicc[x.string[x.start() :x.end()]]), text)

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
        return romans

############################################
# ACABA CANVIS DE TRADUCCIÓ POST TRADUCTOR #
############################################

######################
# TRADUCTOR APERTIUM #
######################

class Traductor:

    def traductor(self, text):
        """Crida al programa Apertium"""
        original = open('traduccions/original.txt', 'w')
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
        if enllac.find(u':') !=-1:
            return enllac
        enllac = enllac[2:-2]
        if enllac.find(u'|') != -1:
            marca = enllac.split(u'|')
            enllac_ori = marca[0]
            text = marca[1]
            text_trad = self.traductor(text)
        else:
            text = enllac
            enllac_ori = enllac
            text_trad = self.traductor(enllac)
        print enllac_ori
        try:
            iws = wikipedia.Page(self.idioma_original,enllac_ori).interwiki()
        except wikipedia.IsRedirectPage:
            if wikipedia.Page(self.idioma_original,enllac_ori).get(get_redirect=True).find('#',5) != -1:
                enllac_red = wikipedia.Page(self.idioma_original,enllac_ori).get(get_redirect=True)
                enllac_ori = re.findall(r'\[\[(.+?)[#\|].*?\]\]',enllac_red)[0]
            else:
                enllac_red = wikipedia.Page(self.idioma_original,enllac_ori).get(get_redirect=True)
                enllac_ori = re.findall(r'\[\[(.+?)\]\]',enllac_red)[0]
                print enllac_ori
                print 'Tractem aquesta excepció'
            try:
                iws = wikipedia.Page(self.idioma_original,enllac_ori).linkedPages()[0].interwiki()
            except:
                print u'Ni punyetera idea què fer aqui :('
                iws = ''
        except wikipedia.NoPage:
            print 'Enllaç vermell'
            return text_trad
        enllac_final = u''
        for iw in iws:
            if iw.title().find(u'[[ca:') != -1:
                inici = iw.title().find(u'[[ca:')
                final = iw.title().find(u']]',inici)
                enllac_trad = iw.title()[inici+5:final]
                text_trad = text_trad.replace(u'*',u'')
                if text.istitle():
                    text_trad = text_trad.title()
                elif text.isupper():
                    text_trad = text_trad.upper()
                elif text.islower():
                    text_trad = text_trad.lower()
                    enllac_trad = enllac_trad.lower()
                if enllac_trad.lower() == text_trad.lower():
                    enllac_final = u'[['+text_trad+']]'
                else:
                    enllac_final = u'[['+enllac_trad+u'|'+text_trad+u']]'
                break
        if enllac_final == u'':
            datasite = pywikibot.getSite(self.idioma_original)
            datapage = pywikibot.Page(datasite, enllac_ori)
            try:
                dataiws = pywikibot.DataPage(datapage).interwiki()
            except pywikibot.IsRedirectPage:
                dataiws = pywikibot.DataPage(datapage).linkedPages()[0].interwiki()
            except pywikibot.NoPage:
                dataiws = ''
            for iw in dataiws:
                if unicode(iw.site()) == u'wikipedia:ca':
                    enllac_trad = iw.title()
                    text_trad = text_trad.replace(u'*',u'')
                    if text.istitle():
                        text_trad = text_trad.title()
                        enllac_trad = enllac_trad.title()
                    elif text.isupper():
                        text_trad = text_trad.upper()
                    elif text.islower():
                        text_trad = text_trad.lower()
                        enllac_trad = enllac_trad.lower()
                    if enllac_trad.lower() == text_trad.lower():
                        enllac_final = u'[['+text_trad+']]'
                    else:
                        enllac_final = u'[['+enllac_trad+u'|'+text_trad+u']]'
            if enllac_final == u'':

                print u'Sembla que la pàgina en català no existeix'
                if text.istitle():
                    text_trad = text_trad.title()
                elif text.isupper():
                    text_trad = text_trad.upper()
                elif text.islower():
                    text_trad = text_trad.lower()
                enllac_final = text_trad
        return enllac_final

    def gestiona_plantilles(self, plantilla):
        """Gestiona les plantilles"""
        print u'* PROCESSANT UNA PLANTILLA *'
        plantilla_titol = u'Template:'+plantilla[2:-2].split('|')[0].strip()
        print plantilla_titol
        pagina = wikipedia.Page(self.idioma_original,plantilla_titol)
        print pagina
        plantilla_ca = self.cerca_interwiki(pagina,'ca')
        print plantilla_ca
        if plantilla_ca:
            print u'Trobada la plantilla en català'
            print plantilla_ca
            plantilla_ca = plantilla.replace(plantilla[2:-2].split('|')[0].strip(), plantilla_ca.title())
            print plantilla_ca
            return plantilla_ca
        else:
            print u"No s'ha trobat la plantilla en català"
            print plantilla
            return plantilla

    def plant_ca(self, plantilla, idioma):
        """Cerca la plantilla a ca:viquipedia respecte la plantilla original"""
        print u'* Cercant la plantilla en català *'
        plantilla_ori = plantilla[2:-2]
        if plantilla_ori.find(u'|') != -1:
            plantilla_ori = plantilla_ori.split(u'|')
        else:
            plantilla_ori = [plantilla_ori]
        if plantilla_ori[0].find(u'#') != -1:
            return u'No és una plantilla'
        elif plantilla_ori[0].find(u'REF') != -1:
            plantilla_ori = re.sub(r'\sREF.+', u'',plantilla_ori[0])
        else:
            plantilla_ori = plantilla_ori[0]
        dicc_id = {u'en' : u'Template:',
                   u'fr' : u'Modèle:',
                   u'es' : u'Plantilla:',
                   u'pt' : u'?:',
                   u'oc' : u'?'}

        print u'{{'+plantilla_ori+u'}}'
        nom = plantilla_ori.rstrip()
        nom = nom.lstrip()
        pagina = dicc_id[idioma]+nom
        plantilla_ori = self.redireccions(pagina+u'/doc', self.idioma_original)
        if plantilla_ori == '':
            plantilla_ori = self.redireccions(pagina, self.idioma_original)
        inici = plantilla_ori.find(u'[[ca:')
        if inici == -1:
            missatge = u'No existeix la plantilla en català'
            print missatge
        else:
            print u'Trobada la plantilla en català'
            final = plantilla_ori.find(u']]',inici)
            plantilla_ca = plantilla_ori[inici+15:final]
            missatge = plantilla.replace(nom, plantilla_ca)
        return missatge

    def gestiona_taules(self, taula):
        """Gestiona les taules"""
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

    def redireccions(self, pagina, idioma):
        try:
            pagina_trobada = wikipedia.Page(idioma,pagina)
            text_pagina = pagina_trobada.get(pagina_trobada)
        except wikipedia.IsRedirectPage:
            text_redirect = pagina_trobada.get(get_redirect=True)
            text_redirect = re.findall(r'\[\[.+?\]\]', text_redirect)[0][2:-2]
            pagina_redirect = wikipedia.Page(idioma,text_redirect)
            text_pagina = pagina_redirect.get()
        except wikipedia.NoPage:
            print 'No existeix aquesta pàgina'
            return ''
        except:
            print 'No sé com gestionar aquesta pàgina'
            return ''
        return text_pagina

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
            par +=1
            if valor.find(u'--[[Usuari:') != -1:
                marca = u'[[Usuari:'
                inici = valor.find(marca)
                valor = valor[inici+len(marca):]
                print valor
                self.usuari_peticio = valor
            elif valor.find(u'[[Usuari Discussió:') != -1:
                inici = valor.find(u'Usuari Discussió:')
                print valor[inici:]
                self.discussio_usuari = valor[inici:]
            print par
        if self.discussio_usuari == '':
            print u"¿?¿? ATENCIÓ, NO ES PODRÁ DEIXAR L'AVÍS A L'USUARI DE LA PETICIÓ ¿?¿?"
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
            elif valor.startswith(self.cerques[2][-1][:-3]): # Enllaços de text
                nou_enllac = self.gestiona_enllac(nou_text)
                print nou_enllac
                dicc[valor] = nou_enllac
            elif valor.startswith(self.cerques[3][-1][:-3]): # Enllaços web
                print u'* PROCESSANT ENLLAÇ WEB *'
                inici = nou_text.find(u' ')
                nou_text = nou_text.replace(nou_text[inici:-1], self.traductor(nou_text[inici:-1]))
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[4][-1][:-3]): # Plantilles
                nou_text = self.gestiona_plantilles(nou_text)
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[5][-1][:-3]): # Referències úniques
                print u'* PROCESSANT REFERÈNCIES *'
                inici = nou_text.find(u'>')
                final = nou_text.find(u'</')
                nou_text = nou_text.replace(nou_text[inici+1:final], self.traductor(nou_text[inici+1:final]))
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[6][-1][:-3]): # Referències de grup (name o altres)
                print u'* PROCESSANT REFERÈNCIES DE GRUP *'
                inici = nou_text.find(u'>')
                final = nou_text.find(u'</')
                nou_text = nou_text.replace(nou_text[inici+1:final], self.traductor(nou_text[inici+1:final]))
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[7][-1][:-3]): # Següents ref name
                print u'* PROCESSANT REFERÈNCIES DE GRUP NAME *'
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[1][-1][:-3]): # Altre codi
                print u'* PROCESSANT ALTRE CODI *'
            elif valor.startswith(self.cerques[8][-1][:-3]): # Taules !! ENCARA FALTA
                print u'*** PROCESSANT TAULES ***'
                nou_text = self.gestiona_taules(nou_text)
                dicc[valor] = nou_text
            elif valor.startswith(u' REFZZ'): # Codi d'estils
                print u'* PROCESSANT ESTILS *'
            elif valor.startswith(u' REFWM'): #Codi LaTex
                print u'* PROCESSANT CODI LaTex *'
            elif valor.startswith(u' REFWY'): #Pàgines web
                print u'* PROCESSANT URLs *'
            elif valor.startswith(u' REFWZ'): #Codi entre <code></code>
                print u'* PROCESSANT CODI *'
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

                elif valor.startswith(self.diccionari_cat[self.idioma_original]):
                    break

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
# CERCA INTERWIKIS # ENCARA NO IMPLEMENTAT
####################

class IW:

    def cerca_interwiki(self,pag,iw): # pag = objecte Page; iw = site().lang p.ex. 'it'
        print pag
        pagiw = ''
        try:
            interwikisLocal = pag.interwiki()
            print interwikisLocal
            print type(interwikisLocal)
            i = pag # inicialització
            for i in interwikisLocal:
                print i
                if i.site().lang == iw:
                    break
            if i.site().lang == iw:
                print "Trobat l'enllaç en català"
                pagiw = i
            else:
                print "No s'ha tobat el iw en el text"
                interwikisData = pywikibot.DataPage(pag).interwiki()
                for i in interwikisData:
                    print i
                    if i.site().lang == iw:
                        break
                if i.site().lang == iw:
                    print "S'ha trobat l'enllaç a wikidata"
                    pagiw = i
                else:
                    print "Aquí arribem?"
                    return ''
            try:
                content = pagiw.get()
            except pywikibot.IsRedirectPage, arg:
                pagiwr = pagiw
                pagiw = pywikibot.Page(pagiw.site(), arg[0])
                try:
                    content = pagiw.get()
                except (pywikibot.IsRedirectPage, pywikibot.NoPage): # redirecció doble o trencada
                    return ''
            except pywikibot.NoPage:
                return ''
        except pywikibot.exceptions.IsRedirectPage, arg:
            print "Redirecció"
            pag_red = wikipedia.Page(pag.site(),arg[0])
            print pag_red
            self.cerca_interwiki(wikipedia.Page(self.idioma_original,pag_red.title()), 'ca')
        except pywikibot.NoPage: # per evitar errors en pag
            print "Cagada pastoret, nen"
            return ''
        print pagiw
        return pagiw # Retorna objecte Page o res

##########################
# ACABA CERCA INTERWIKIS #
##########################


##############
# CATEGORIES #
##############

class Categories:

    def cat_ca_superiors(self, llista_cat_ca, n=1,p=1,categories_pare=[]):
        for cats in llista_cat_ca:
            self.passos(cats, u'Categories pare en catala')
            cats_ca = cats.categories()
            self.llista_parents.append(cats.title())
            for categoria in cats_ca:
                if categoria not in llista_cat_ca:
                    self.llista_parents.append(categoria.title())
            supercategories = cats.categories()
            if n <4:
                categories_pare.extend(supercategories)
            if p == len(llista_cat_ca):
                n += 1
                for x in categories_pare:
                    if x not in llista_cat_ca:
                        llista_cat_ca.append(x)
                categories_pare = []
            p += 1

    def cerca_cat_ca(self, n=1,p=1,cat_ca='', categories_ca=[],parents=[],categories_pare=[]):
        pagina = wikipedia.Page(self.idioma_original,self.titol_original)
        wiki_ca = wikipedia.Site(u'ca')
        try:
            categories = pagina.categories()
        except wikipedia.IsRedirect:
            print 'a veure què fa?'
        for categoria in categories:
            iws = categoria.interwiki()
            for y in iws:
                if y.site() == wiki_ca:
                    if u"[[ca:"+y.title()+']]\n' not in categories_ca:
                        if y.title() not in self.llista_parents:
                            if y.title().find(u' per ') == -1:
                                parents.append(y)
                                self.cat_ca_superiors(parents)
                                print u"****************************************************\n***** S'afegirà la següent categoria en català *****"
                                print unicode(y).center(52)
                                print u"****************************************************"
                                categories_ca.append(u"[["+y.title()+u']]\n')
                                self.passos(unicode(categoria.title())+u'\n'+y.title(),u'Categoria original i categoria en catala')
            supercategories = categoria.categories()
            if n < 3:
                categories_pare.extend(supercategories)
            if p == len(categories):
                n += 1
                categories.extend(categories_pare)
                categories_pare = []
                if n == 3 and categories_ca != []:
                    break
            p += 1
        for x in categories_ca:
            cat_ca += x
        return cat_ca

####################
# ACABA CATEGORIES #
####################

####################
# PROCESSA EL TEXT #
####################

class Text:

    def canviar_text(self, text, inici=0, cap=0, text_trad='', text_final='', ncodi=0):
        """Gestiona el text de forma que neteja el possible codi que pugui dificultar la traducció"""
        llista_net = []
        capitol_trad = []
        llista_notrad = []
        self.text = text
        self.passos(text, u'Aquest es el text a traduir:\n\n')
        text_ori = re.split(r'\n\n', self.text)
        for capitol in text_ori:
            cap += 1
            if capitol.find(self.ordena[self.idioma_original]) != -1:
                print "Ha trobat l'ordena"
                capitol = re.sub(r'\{\{%s.*?\}\}' %self.ordena[self.idioma_original], '', capitol)
                print capitol
            capitol_ori = capitol
            if capitol_ori.find(self.diccionari_cat[self.idioma_original]) != -1:
                print u"Trobades les categories"
                print capitol
                categories = re.findall(r'\[\[%s.*?\]\]' %self.diccionari_cat[self.idioma_original], capitol_ori)
                print u'La parrafada que vindrà ara, nen :D\n'
                text = self.cerca_cat_ca()
                capitol_ori = u'<!-- '+capitol_ori+u' -->'
                text_final += capitol_ori+ u'\n\n' + text + u"\n"
                print u'========================\n== Original ==\n========================\n'+capitol_ori
                print u'========================\n== Traducció ==\n========================\n'+text
                continue
#            else:
#                continue
            print u'*********************************\n*** NETEJA DE CAPITOL '+str(cap)+u'/'+str(len(text_ori))+u' ***\n*********************************'
            print capitol
            capitol = capitol.replace(u'\n*', u'\n* ') # La llista no numerada ha de contenir un espai entre l'asterisc i la frase...
            capitol = capitol.replace('*', ' ASTR ')
            capitol = re.sub(r"''(?!')", " '' ", capitol)
            capitol = re.sub(r"'''", " ''' ", capitol)
            capitol = re.sub(r'\n#',' SOSTINGUT ', capitol)
            capitol = re.sub(r'[$]', ' SIMBOLDOLLAR ', capitol)
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
            codi = re.findall(r'<[Mm]ath>.+?</[Mm]ath>',capitol)
            ncodi = 0
            for mates in codi:
                ncodi = str(ncodi).zfill(4)
                valor = u' REFWM%s ' %(ncodi)
                capitol = capitol.replace(mates, valor)
                print mates
                self.refs[valor] = mates
                ncodi = int(ncodi) + 1
                self.passos(valor + u'\n' + mates, u'Codi de formules matematiques' )
            codi = re.findall(r'(http://[\w./\~\+\-&=\d]+)',capitol)
            ncodi = 0
            for webs in codi:
                print webs
#                raw_input()
                ncodi = str(ncodi).zfill(4)
                valor = u' REFWY%s ' %(ncodi)
                capitol = capitol.replace(webs, valor)
                self.refs[valor] = webs
                ncodi = int(ncodi) + 1
                self.passos(valor + u'\n' + webs, u'Pagines web' )
            codi = re.findall(r'<[Cc]ode>.+?</[Cc]ode>',capitol)
            ncodi = 0
            for m_code in codi:
                ncodi = str(ncodi).zfill(4)
                valor = u' REFWZ%s ' %(ncodi)
                capitol = capitol.replace(m_code, valor)
                self.refs[valor] = m_code
                print m_code
                ncodi = int(ncodi) + 1
                self.passos(valor + u'\n' + m_code, u'Codi de codis' )
            if self.idioma_original == u'en' and capitol.find(u'centur') != -1:
                llista3 = re.findall(r'(\d*?)(\w*? [to|and]?)(\d*)(\w* centur[y|ies])(\w*)', capitol)
                for segles in llista3:
                    primer = segles[0]
                    segon = segles[2]
                    tercer = segles[4]
                    regex = segles[0]+segles[1]+segles[2]+segles[3]+segles[4]
                    if tercer == 'AD':
                        crist = ' d.C.'
                    elif tercer == 'BC':
                        crist = ' a.C.'
                    else:
                        crist = ' '+tercer

                    if primer == '':
                        capitol = capitol.replace(regex, 'segle '+self.romans(segon)+crist)
                    else:
                        capitol = capitol.replace(regex, 'segles '+self.romans(primer)+'-'+self.romans(segon)+crist)
            self.text_trad = self.cerca(capitol)
            self.ordena_diccionari(self.refs)
            self.text_trad = self.text_trad.replace(u'{', u' CLAUDATOROBERT ' )
            self.text_trad = self.text_trad.replace(u'}', u' CLAUDATORTANCAT ' )
            self.passos(self.text_trad, u'************************************************************************************************************************\nAquest es el paragraf preparat per traduir:\n************************************************************************************************************************\n')
            paragraf = unicode(self.traductor(self.text_trad)+u'\n\n'.decode('utf-8'))
            self.passos(capitol_ori, u'Original\n')
            self.passos(self.text_trad, u'Original processat\n')
            self.passos(paragraf, u'Catala processat\n')
            paragraf = paragraf.replace(u'*REF',u'REF')
            no_trad = re.findall(r'\*\w+\s',paragraf)
            self.passos(no_trad, u'Llista de paraules no traduides')
            for paraula in no_trad:
                self.passos(paraula, u'Paraula no traduida')
                if paraula[1:].istitle:
                    pass
                else:
                    if paraula not in self.no_trad and paraula not in self.llista_marques:
                        self.passos(paraula, u"Aquesta paraula no s'havia trobat fins ara")
                        self.no_trad.append(paraula)
            self.passos(self.no_trad, u'Llista de paraules que Apertium no tradueix')
            if paragraf.find('REF') != -1:
                text = self.refer_text(paragraf)
            else:
                print u"* NO S'HAN TROBAT REF PER CANVIAR *"
                text = paragraf
            while text.find('REF') != -1:
                text = text.replace(u'*', u'')
                print '*** ENCARA HI HA REF PER CANVIAR ***'
                text = self.refer_text(text)
            print '**************\n*** ACABAT ***\n**************\n'
            text = text.replace(u'*', u'')
            text = text.replace(u' ASTR ', u'*')
            text = text.replace(u' SIMBOLDOLLAR ', u'$')
            text = text.replace(u' SOSTINGUT ', u'\n#')
            text = text.replace(u" '' ", u"''")
            text = text.replace(u" ''' ",u"'''")
            text = text.replace(u' ,', u',')
            text = text.replace(u' CLAUDATOROBERT ', u'{')
            text = text.replace(u' CLAUDATORTANCAT ', u'}')
            text = text.lstrip()
            self.passos(text, u'Catala net final')
            text_final += capitol_ori + u'\n\n' + text
            self.refs = {}
            self.dicc_enllac = {}
            print u'========================\n== Original ==\n========================\n'+capitol_ori
            print u'========================\n== Traducció ==\n========================\n'+text
        while text_final.find(u'  ') != -1:
            text_final = text_final.replace(u'  ', u' ')
        #while text_final.find(u'\n ') != -1:
            #text_final = text_final.replace(u'\n ', u'\n')
        text_final = text_final+u'\n[['+self.idioma_original+u':'+self.titol_original+u"]]\n\n==Notes de traducció==\n*Les plantilles en vermell són les plantilles que no s'han pogut trobar la corresponent plantilla en català. Això no vol dir que la plantilla no existeixi, sino que no s'ha pogut trobar automàticament, ja sigui per que no hi ha el corresponent enllaç interviqui, o per que realment no existeix la plantilla en català. En cas que trobeu la plantilla corresponent us agrairia que li posesiu el seu enllaç interviqui a la plantilla en anglès per poder trobar-la en properes traduccions. Gràcies. --~~~~\n\n*Podeu comentar possibles millores en el bot de traducció en [[Usuari:Anskarbot/Errors|aquesta pàgina]]. --~~~~\n\n*Les paraules que el programa [[Apertium]] encara no tradueix queden registrades automàticament. Si trobeu alguna millora en la traducció podeu expresar-ho a la mateixa [[Usuari:Anskarbot/Errors|pàgina d'errors]]. --~~~~"
        self.passos(text_final,u'\n***************\n** Text finalitzat **\n***************\n')
        return text_final

    def refer_text(self, text):
        """Canvia les referències de codi REF...... pel valor corresponent del diccionari self.refs"""
        print u'*** REFENT EL TEXT ***'
        marca = re.findall(r'REF\w+\d+?\s', text)
        for ref in marca:
            text = text.replace(u' '+ref, self.refs[u' '+ref])
            self.passos(self.refs[u' '+ref], 'Canvi en el text: '+str(ref))
        return text

##########################
# ACABA PROCESSA EL TEXT #
##########################

#######################
# COMENÇA EL PROGRAMA #
#######################

class Amical(Text,PreCercaSubst,Diccionaris,Gestio,Registre,Traductor,Avisos,Canvis,Categories,IW):

    def arrenca(self,gravar_viqui=False):
        resposta = u'supercalifragilisticoespialidoso'
        print
        print u'////////////////////////////'.center(150)
        print u'///**********************///'.center(150)
        print u'///* ARRENCA AMICAL BOT *///'.center(150)
        print u'///**********************///'.center(150)
        print u'////////////////////////////'.center(150)
        print
        while resposta != 's' and resposta != 'n' and resposta != '':
            resposta = raw_input(u'Gravem a la viqui?')
            if resposta == 's':
                gravar_viqui = True
            elif resposta == 'n':
                gravar_viqui = False
            elif resposta == '':
                resposta = 'n'
                gravar_viqui = False
        self.inici(gravar_viqui=gravar_viqui)

    def variables(self):
        """Definim les variables globals"""
        self.refs = {} # Diccionari dels codis processats abans de traduir
        self.cerques =[(u'<!--',u'-->', u' REFCO%s '), # Llista de tuples que ...
                       (u'<' , u'>' , u' REFCW%s '),
                       (u'[[',u']]', u' REFEA%s '),    # ... estableix el caràcter de cerca ...
                       (u'[http:',u']', u' REFEW%s '), # ... i el relaciona amb la referència que substituirà.
                       (u'{{',u'}}', u' REFPL%s '),            # La tupla consta de tres paràmetres:
                       (u'<ref>' , u'</ref>', u' REFRE%s '),   # 1: El primer terme de cerca, (p.e. {{ com a primer terme)
                       (u'<ref', u'</ref>', u' REFRI%s '),     # 2: El darrer terme de cerca, (ha de trobar }} com a darrer terme)
                       (u'<ref name' , u'/>' , u' REFSR%s '),  # 3: La referència que substitueix el codi trobat
#                       (u'<nowiki>' , u'</nowiki>' , u' REFSA%s '),    # És important que la marca REFxx segueixi un ordre alfabètic
#                       (u'<div' , u'</div>' , u' REFSA%s '),           # per gestionar el diccionari de referències en l'ordre correcte
                                          # de forma qualsevol codi inserit dins un altre codi es gestioni primer el que es troba dins un altre,
                       (u'{|',u'|}', u' REFZT%s ')]                   # per això el comentari <!-- --> és el primer en gestionar-se i les taules {| }| l'últim de tots.
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
        self.diccionari_cat = {u'en' : u'Category:',  # Diccionari per gestionar les categories
                               u'es' : u'Categoría:', #... en els diferents idiomes possibles de traducció
                               u'fr' : u'Catégorie:',
                               u'pt' : u'?:',
                               u'oc' : u'?:'}
        self.ordena = { u'en' : u'DEFAULTSORT', # Diccionari per gestionar la plantilla {{ORDENA ...
                        u'es' : u'ORDENAR',     #... en els diferents idiomes de traducció
                        u'fr' : u'DEFAULTSORT'}
        self.cops_k_passa = 0 # Variable global que gestiona el nombre amb que es registra un procés a l'arxiu registre.txt
        self.llista_marques = [u'*ASTR',u'*CLAUDATOROBERT',u'*CLAUDATORTANCAT',u'SIMBOLDOLLAR',u'SOSTINGUT']
        self.dicc_enllac = {}
        self.dicc_cat = {}
        self.llista_parents = []
        self.no_trad = []

    def inici(self, peticions=1, gravar_viqui=True, proves=True):
        print gravar_viqui
        """Comença el programa.
        Els arguments que accepta la funció són:
        1.- peticions: el nombre de la primera petició.
            S'ha de posar aquí la variable per poder cridar-la sense error.
        2.- gravar_viqui: És la variable que permet gravar el resultat a la viqui o no.
            Per defecte es posa False ja que està en fase de proves.
        3.- proves: Mentre estigui en fase de proves no es borrarà la plantilla de petició
            i es posarà el text a la viqui en una pàgina de proves expressa
            per anar provant el bot. True per defecte"""
        projecte = wikipedia.getSite()
        cat = catlib.Category(projecte, u"Categoria:Peticions de còpia i preprocés per traducció automàtica")
        pagines = cat.articles()
        for pagina in pagines:
            self.pagina_original = pagina
            self.variables()
            titol = pagina.title()
            print '*********************************************************************************************************************************'
            print '*********************************************************************************************************************************'
            print  (u'*****  '+str(peticions)+u'.- COMENCA EL PROCES  per la peticio que es troba a -> '+unicode(titol)+u'  *****').center(118)
            print '*********************************************************************************************************************************'
            print '*********************************************************************************************************************************'
            self.titol = titol.encode('utf-8')
            print pagina #Pàgina que té la petició de traducció
            text_ca = pagina.get()
            self.peticio(text_ca)
            self.text_trad = self.redireccions(self.titol_original,self.idioma_original)
            print u"\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
            print (u"% EL REGISTRE ES TROBA A registre-"+unicode(self.titol_original)+".txt %").center(90)
            print u"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
            text = self.canviar_text(self.text_trad)
            print u'\n****************************************'
            print u'********** ACABADA LA PETICIÓ **********'
            print u'****************************************\n'
            if gravar_viqui == True:
                pagina_final = u'Usuari:Anskarbot/Traduccions/'+unicode(self.titol_original)
                if proves == True:
                    enllac_pagina = u'[['+pagina_final+u'|aquesta pàgina de proves]]'
                    missatge_bot = u'Anskarbot EN FASE DE PROVES '
                else:
                    enllac_pagina = u'[['+pagina_final+u']]'
                    missatge_bot = u'Anskarbot '
                text = u"{{Notes de traducció}}\n\n"+text
                pagina_gravar = wikipedia.Page(u'ca',pagina_final)
                pagina_gravar.put(text, missatge_bot + u"generant una nova traducció automàtica", minorEdit = False, force=True)
                self.discussio(pagina_final)
                index = u'Usuari:Anskarbot/Traduccions'
                index = wikipedia.Page(u'ca',index)
                contingut_index = index.get()
                index.put(contingut_index+u'\n* [[/'+self.titol_original+']]. {{u|'+self.usuari_peticio+u'}}\n', missatge_bot + u"creant l'índex de les traduccions fetes", minorEdit=False, force=True)
                self.avisar_usuari(pagina_final, enllac_pagina, missatge_bot)
                self.passos(pagina_final, u'Pagina on es grava el text:')
                self.paraules(self.idioma_original)
            if proves == True:
                raw_input('Seguim?')
            peticions +=1
        print u'\nOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
        print (u'OOOOO   ACABADES LES TRADUCCIONS   OOOOO').center(60)
        print u'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
        return 0

if __name__ == "__main__":
    try:
        app = Amical()
        app.arrenca()
    finally:
        wikipedia.stopme()

####################
# THAT'S ALL FOLKS #
####################
