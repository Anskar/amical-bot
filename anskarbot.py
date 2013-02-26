#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sense títol.py
#
#  Copyright 2013  <Anskar>
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

class Proves:
    """
    Aquesta classe hauria de classificar les proves que es volen fer per no haver de
    córrer tot el programa. S'hauria de voler especificar sobre quin apartat es volen fer les proves
    i s'ha de poder escollir més d'un. En cas de que fos cap no té sentit demanar proves.
        Maquillatge
        Wiki
    """
    def apartat(self):
        self.prova_maquillatge = self.pregunta(u"Volem fer proves de canvis d'expressions regulars en el text?",False)
        self.prova_plantilles = self.pregunta(u"Volem fer proves amb plantilles?",False)
        self.prova_enllacos = self.pregunta(u"Volem fer proves amb enllacos?",False)
        self.prova_categories = self.pregunta(u"Volem fer proves amb les categories?",False)
        self.prova_taules = self.pregunta(u"Volem fer proves amb les taules?",False)
        self.prova_code = self.pregunta(u"Volem fer proves amb els codis?",False)
        self.prova_mates = self.pregunta(u"Volem fer proves amb el codi LaTex?",False)
        self.prova_imatges = self.pregunta(u"Volem fer proves amb les imatges?",False)
        self.prova_webs = self.pregunta(u"Volem fer proves amb els enllacos web?",False)
        self.prova_traduccio = self.pregunta(u"Volem fer proves amb la traduccio?",False)
        self.prova_interviqui = self.pregunta(u"Volem fer proves amb els enllacos interviqui?",True)

class Maquillatge:

    def segles(self,text):
        print "* PROCESSANT ELS SEGLES TROBATS AL TEXT *"
        return text

    def errorsPre(self,text):
        text = text
        if self.prova_maquillatge == False: return text
        print "* PROCESSANT ELS ERRORS CONEGUTS ABANS DE LA TRADUCCIÓ *"
        if self.idioma_original == 'en': text = self.segles(text)
        self.pagina_re(text,self.canvis_pre)
        return text

    def pagina_re(self, text, dicc):
        """Reemplazo múltiple de cadenas en Python."""
        print dicc.keys()
        try:
            regex = re.compile("(%s)" % "|".join(map(re.escape, dicc.keys())))
            text = regex.sub(lambda x: unicode(dicc[x.string[x.start() :x.end()]]), text)
        except:
            dicc = self.dicc_plantilles
            regex = re.compile("(%s)" % "|".join(map(re.escape, dicc.keys())))
            text = regex.sub(lambda x: unicode(dicc[x.string[x.start() :x.end()]]), text)
        return text

    def errorsPost(self,text):
        print "* PROCESSANT ELS ERRORS CONEGUTS DESPRÉS DE LA TRADUCCIÓ *"
        text = self.pagina_re(text,self.canvis_post)
        return text

class Wiki:

    def article(self,text,peticio):
        if self.prova_gravar_viqui == False: return
        if self.pagina_discussio_usuari == '':
            print 'l´Usuari no ha signat?'
            falta = u" --~~~~\n*Recorda de signar les peticions de traducció, ja que si no, és impossible que una màquina com jo sàpiga qui demana la traducció. Gràcies."
            self.pagina_discussio_usuari = peticio.title()
        else:
            print u"Sembla que l'usuari ha signat'"
            falta = ''

        print "* GRAVANT L'ARTICLE A LA VIQUI *"
        pagina = u'Usuari:Anskarbot/Traduccions/'+self.titol_original
        enllac_pagina = u"[["+pagina+u"|aquesta pàgina de proves]]"
        pagina = wikipedia.Page('ca',pagina)
        pagina.put(text,u"Anskarbot editant un article traduït",minorEdit=False,force=True)

        print "* DEIXANT L'AVÍS A LA PÀGINA DE L'USUARI *"
        missatge = u"\n== Petició de traducció ==\n*La vostra petició de traducció de l'article '''" + self.titol_original + u"''' es troba en " + enllac_pagina + u". Quan repasseu la traducció podeu fer suggeriments de millora a [[Usuari:Anskarbot/Errors|la pàgina de millores del bot]] per anar polint la traducció. Gràcies."+falta+u" --~~~~\n"
        pagina = wikipedia.Page('ca',unicode(self.pagina_discussio_usuari))
        p = re.compile(u'\n== Petició de traducció ==\n')
        pagina_discusio = pagina.get()
        if p.search(pagina_discusio):
            pagina_discusio = p.sub(missatge,pagina_discusio,1)
        else:
            pagina_discusio = pagina_discusio+missatge
        pagina.put(pagina_discusio,u"Anscarbot deixant un missatge a la pàgina de discussió de l'usuari.",minorEdit=False, force=True)

        print "* POSANT LA PLANTILLA {{Traduït de}} A LA PÀGINA DE DISCUSSIÓ DE L'ARTICLE TRADUÏT *"
        pagina = u"Usuari Discussió:Anskarbot/Traduccions/"+self.titol_original
        urlversio =wikipedia.Page(self.idioma_original,self.titol_original).permalink()
        versio = re.findall(r'oldid=(\d+)',urlversio)
        pagina = wikipedia.Page('ca', pagina)
        pagina.put(u'{{Traduït de|'+self.idioma_original+u'|'+self.titol_original+u'|{{subst:CURRENTDAY}}-{{subst:CURRENTMONTH}}-{{subst:CURRENTYEAR}}|'+versio[0]+u'}}', u'Anskarbot incorporant la plantilla {{traduït de}} a la pàgina de discussió',minorEdit=False, force=True)

        print u"* AFEGINT LA TRADUCCIÓ A L'ÍNDEX DE TRADUCCIONS *"
        index = u'Usuari:Anskarbot/Traduccions'
        index = wikipedia.Page(u'ca',index)
        contingut_index = index.get()
        index.put(contingut_index+u'\n* [[/'+self.titol_original+']]. {{u|'+self.usuari_peticio+u'}}\n', u"Anskarbot afegint la traducció a l'índex de les traduccions fetes", minorEdit=False, force=True)

class Apertium:

    def traductor(self, text):
        """Crida al programa Apertium"""
        text = text
        if self.prova_traduccio == False: return text
        print "* TRADUÏNT *"
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

class Categories:

    def treuCategories(self,pagina,text):
        text = text
        if self.prova_categories == False: return text
        print "* NETEJANT CATEGORIES *"
        llista_cat = u"<!-- Categories en l'idioma original. Amagades per no tenir categories en vermell"
        categories = pagina.categories()
        print categories
        for categoria in categories:
            print categoria.title()
            text = re.sub(ur'\[\[%s.+\]\]'%categoria.title() , u'',text)
            print text
            self.pregunta(u'Seguim?',False)
            categoria = u"[["+categoria.title()+u"]]"
            llista_cat += categoria+u'\n'
        llista_cat += u' -->'
        self.cat_original = llista_cat
        return text

    def cercaCategories(self,pagina,text,n=1,p=1,cat_ca='',categories_ca=[],parents=[],categories_pare=[],limit=3):
        text = text
        if self.prova_categories == False: return text
        print "* CERCANT CATEGORIES *"
        wiki_ca = wikipedia.Site(u'ca')
        categories = pagina.categories()
        for categoria in categories:
            print str(n)+':'+str(limit)+'/'+str(p)+'-'+str(len(categories))
            iws = categoria.interwiki()
            for y in iws:
                if y.site() == wiki_ca:
                    if u"[[ca:"+y.title()+u']]\n' not in categories_ca:
                        if y.title() not in self.llista_parents:
                            if y.title().find(u' per ') == -1:
                                parents.append(y)
                                self.cercaCategoriesPare(parents)
                                print u"****************************************************\n***** S'afegirà la següent categoria en català *****"
                                print unicode(y).center(52)
                                print u"****************************************************"
                                categories_ca.append(u"[["+y.title()+u']]\n')
            supercategories = categoria.categories()
            if n < limit:
                categories_pare.extend(supercategories)
            if p == len(categories):
                n += 1
                categories.extend(categories_pare)
                categories_pare = []
                if n == limit and categories_ca != []:
                    break
                if n == limit and categories_ca == []:
                    limit += 1
            p += 1
        for x in categories_ca:
            cat_ca += x
        return cat_ca

    def cercaCategoriesPare(self,llista_cat_ca,n=1,p=1,categories_pare=[]):
        for cats in llista_cat_ca:
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
                    elif text.isupper():
                        text_trad = text_trad.upper()
                    elif text.islower():
                        text_trad = text_trad.lower()
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

    def gestiona_plantilles(self, plantilla):
        """Gestiona les plantilles"""
        print u'* PROCESSANT UNA PLANTILLA *'
        plantilla_titol = u'Template:'+plantilla[2:-2].split('|')[0].strip()
        print plantilla_titol
        pagina = wikipedia.Page(self.idioma_original,plantilla_titol+u"/doc")
        print pagina
        plantilla_ca = self.cercaInterviqui(pagina,'ca')
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

        print u'{{'+plantilla_ori+u'}}'
        nom = plantilla_ori.rstrip()
        nom = nom.lstrip()
        pagina = self.dicc_id[idioma]+nom
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

class Diccionaris:

    def ordena_diccionari(self, dicc, count=0):
        """Repassa el diccionari self.refs per gestional el codi.
        Cada codi té una marca que es troba en el diccionari de tuples self.marques"""
        print u'\n*** PROCESSANT EL DICCIONARI DE REFERÈNCIES ***'
        claus = sorted(dicc.keys(), reverse=True)
        self.count = count
        for valor in claus:
            nou_text = dicc[valor]
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
                par = int(par)
                par += 1
        print u'================================================================'
        return text

class Interviqui:

    def cercaInterviqui(self,pagina,iw):
        if self.prova_interviqui == False: return ''
        print "* CERCANT ENLLAÇOS INTERVIQUI *"
        if pagina.title().find(self.titol_plantilles[self.idioma_original]) != -1:
            pagina = wikipedia.Page(self.idioma_original,pagina.title()+self.us_plantilles[self.idioma_original])
        pagiw = ''
        try:
            interwikisLocal = pagina.interwiki()
            i = pagina # inicialització
            for i in interwikisLocal:
                if i.site().lang == iw:
                    break
            if i.site().lang == iw:
                print "Trobat l'enllaç en català"
                pagiw = i
            else:
                print "No s'ha tobat el iw en el text"
                interwikisData = pywikibot.DataPage(pagina).interwiki()
                for i in interwikisData:
                    print i
                    if i.site().lang == iw:
                        break
                if i.site().lang == iw:
                    print "S'ha trobat l'enllaç en català a wikidata"
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
        except pywikibot.IsRedirectPage, arg:
            print "Redirecció"
            pag_red = wikipedia.Page(pagina.site(),arg[0])
            print pag_red
            self.cercaInterviqui(wikipedia.Page(self.idioma_original,pag_red.title()), 'ca')
        except pywikibot.NoPage: # per evitar errors en pag
            print "Cagada pastoret, nen"
            return ''
        print pagiw
        return pagiw # Retorna objecte Page o res

    def treuInterviquis(self,pagina,text):
        text = text
        if self.prova_interviqui == False: return text
        print "* NETEJANT INTERVIQUIS *"
        iws = pagina.interwiki()
        for iw in iws:
            iw = unicode(iw)
            text = text.replace(iw,'')
            self.llista_iw += iw+u"\n"
        return text

class Pagines:

    def paginesClau(self,pagina):
        self.idioma_original = self.peticions[pagina][1][0]
        print self.idioma_original
        self.titol_original = self.peticions[pagina][1][1]
        print self.titol_original
        print self.peticions[pagina][1][2]
        self.pagina_discussio_usuari = re.findall(ur'Usuari Discussió:\w+', self.peticions[pagina][1][2])[0]
        self.usuari_peticio = re.findall(ur'Usuari:(\w+)', self.peticions[pagina][1][2])[0]
        print self.pagina_discussio_usuari
        try: self.pagina_regex = self.peticions[pagina][1][3]
        except: pass

class Text:

    def preTrad(self, pagina,text_final='',cap=0):
        llista_net = []
        capitol_trad = []
        llista_notrad = []
        text_final = u"{{Notes de traducció}}\n\n"
        print "* GESTIONANT EL TEXT ABANS DE LA TRADUCCIÓ *"
        pagina = wikipedia.Page(self.idioma_original,self.titol_original)
        try:
            text = pagina.get()
        except wikipedia.IsRedirectPage, arg:
            pagina_red = wikipedia.Page(pagina.site(),arg[0])
            pagina = pagina_red
            self.titol_original = pagina_red.title()
            text = pagina.get()
        text_original = text
        text = self.treuInterviquis(pagina,text)
        text = self.treuCategories(pagina,text)
        text = re.sub(r'%s.+\}\}' %self.dicc_ordena[self.idioma_original],'',text)
        text = self.errorsPre(text)
        while text.find(u'\n\n\n') != -1:
            text = text.replace(u'\n\n\n',u'\n\n')
        text = text.replace(u"==\n",u"==\n\n")
        capitols = re.split(r'\n\n', text)
        for capitol in capitols:
            capitol_ori = capitol
            cap += 1
            print u"********************\n********************\n* Capítol "+str(cap)+u"/"+str(len(capitols))+u" *\n********************\n********************"
            if text == '': continue
            if self.prova_traduccio == False: break
            print "&&&&&&&&&&&&&&&&&&&\n&& TEXT ORIGINAL &&\n&&&&&&&&&&&&&&&&&&&"
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
            ncodi = 0
            for estil in codi:
                ncodi = str(ncodi).zfill(4)
                valor = u' REFZZ%s ' %(ncodi)
                capitol = capitol.replace(estil, valor)
                self.refs[valor] = estil
                ncodi = int(ncodi) + 1
            codi = re.findall(r'<[Mm]ath>.+?</[Mm]ath>',capitol)
            ncodi = 0
            for mates in codi:
                ncodi = str(ncodi).zfill(4)
                valor = u' REFWM%s ' %(ncodi)
                capitol = capitol.replace(mates, valor)
                print mates
                self.refs[valor] = mates
                ncodi = int(ncodi) + 1
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
            codi = re.findall(r'<[Cc]ode>.+?</[Cc]ode>',capitol)
            ncodi = 0
            for m_code in codi:
                ncodi = str(ncodi).zfill(4)
                valor = u' REFWZ%s ' %(ncodi)
                capitol = capitol.replace(m_code, valor)
                self.refs[valor] = m_code
                print m_code
                ncodi = int(ncodi) + 1
            if self.idioma_original == u'en' and capitol.find(u'entur') != -1:
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
            text_trad = self.traductor(self.text_trad)
            text_trad = text_trad.replace(u'*REF',u'REF')
            no_trad = re.findall(r'\*\w+\s',text_trad)
            for paraula in no_trad:
                if paraula[1:].isupper:
                    pass
                else:
                    if paraula not in self.no_trad and paraula not in self.llista_marques:
                        self.no_trad.append(paraula)
            if text_trad.find('REF') != -1:
                text = self.referText(text_trad)
            else:
                print u"* NO S'HAN TROBAT REF PER CANVIAR *"
                text = text_trad
            if text.find('REF') != -1:
                text = text.replace(u'*', u' ')
                print '*** ENCARA HI HA REF PER CANVIAR ***'
                text = self.referText(text)
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
            text_final += capitol_ori + u'\n\n' + text
            self.refs = {}
            self.dicc_enllac = {}
            print u'========================\n== Original ==\n========================\n'+capitol_ori
            print u'========================\n== Traducció ==\n========================\n'+text
        while text_final.find(u'  ') != -1:
            text_final = text_final.replace(u'  ', u' ')
        categories = self.cercaCategories(pagina,text)
        text_final += self.cat_original+u"\n\n"+categories+u"\n\n" + self.llista_iw
        text_final = text_final+u'\n[['+self.idioma_original+u':'+self.titol_original+u"]]\n\n==Notes de traducció==\n*Les plantilles en vermell són les plantilles que no s'han pogut trobar la corresponent plantilla en català. Això no vol dir que la plantilla no existeixi, sino que no s'ha pogut trobar automàticament, ja sigui per que no hi ha el corresponent enllaç interviqui, o per que realment no existeix la plantilla en català. En cas que trobeu la plantilla corresponent us agrairia que li posesiu el seu enllaç interviqui a la plantilla en anglès per poder trobar-la en properes traduccions. Gràcies. --~~~~\n\n*Podeu comentar possibles millores en el bot de traducció en [[Usuari:Anskarbot/Errors|aquesta pàgina]]. --~~~~\n\n*Les paraules que el programa [[Apertium]] encara no tradueix queden registrades automàticament. Si trobeu alguna millora en la traducció podeu expresar-ho a la mateixa [[Usuari:Anskarbot/Errors|pàgina d'errors]]. --~~~~"
        registre = open('registres/registre-%s.txt' %self.titol_original,'w')
        registre.write(text_final.encode('utf-8'))
        registre.close()
        return text_final

    def referText(self, text):
        """Canvia les referències de codi REF...... pel valor corresponent del diccionari self.refs"""
        print u'*** REFENT EL TEXT ***'
        marca = re.findall(r'REF\w+\d+?\s', text)
        for ref in marca:
            text = text.replace(u' '+ref, self.refs[u' '+ref])
        return text

    def postTrad(self,text):
        print "* GESTIONANT EL TEXT DESPRÉS DE LA TRADUCCIÓ *"
        text = self.errorsPost(text)

class Peticions:

    def cercaPeticions(self):
        print u'* COMENÇA EL PROCÉS DE CERCA DE PETICIONS DE TRADUCCIÓ *'
        articles = catlib.Category(u'ca',u"Categoria:Peticions de còpia i preprocés per traducció automàtica").articles()
        print u"* COMENÇA EL PROCÉS DE GESTIÓ DE LES PLANTILLES DE PETICIÓ DE TRADUCCIÓ *"
        for pagina in articles:
            plantilles = pagina.templatesWithParams()
            for plant in plantilles:
                if plant[0].find(u'etició de traducció') != -1:
                    self.peticions[pagina] = plant

    def treuPeticio(self, pagina):
        if self.prova_gravar_viqui == False: return
        print u"* COMENÇA EL PROCÉS PER TREURE LA PLANTILLA JA PROCESSADA *"
        text = pagina.get()
        plantilla = self.plantillaAText(self.peticions[pagina])
        text = text.replace(u'{{petició de traducció',u'{{Petició de traducció')
        text = text.replace(plantilla,'')
        pagina.put(text,u"Anskarbot traient la plantilla de traducció." ,minorEdit=False,force=True)

class Pregunta:

    def pregunta(self,pregunta,resposta):
        passem = resposta
        while resposta != 's' and resposta != 'n' and resposta != '' and resposta != True:
            resposta = raw_input(pregunta)
            if resposta == 's':
                print 'True'
                passem = True
            elif resposta == 'n':
                print 'False'
                passem = False
            elif resposta == '':
                print 'False'
                resposta = 'n'
                passem = False
        return passem

class Inici(Pregunta,Peticions,Text,Interviqui,PreCercaSubst,Diccionaris,Gestio,Plantilles,Categories,Apertium,Wiki,Maquillatge,Proves,Pagines):

    def main(self):
        print
        print u'////////////////////////////'.center(100)
        print u'///**********************///'.center(100)
        print u'///* ARRENCA AMICAL BOT *///'.center(100)
        print u'///**********************///'.center(100)
        print u'////////////////////////////'.center(100)
        print
        self.variables()
        self.prova_gravar_viqui = self.pregunta(u'Gravem a la viqui?',False)
        self.proves = self.pregunta(u'Volem fer proves?',False)
        if self.proves == True:
            self.apartat()
        else:
            self.prova_maquillatge = True
            self.prova_plantilles = True
            self.prova_enllacos = True
            self.prova_categories = True
            self.prova_taules = True
            self.prova_code = True
            self.prova_mates = True
            self.prova_imatges = True
            self.prova_webs = True
            self.prova_traduccio = True
            self.prova_interviqui = True
        self.cercaPeticions()
        for peticio in self.peticions.keys():
            self.paginesClau(peticio)
            text = self.preTrad(peticio)
            self.article(text,peticio)
            self.treuPeticio(peticio)

    def variables(self):
        # LLISTES
        self.llista_parents = []
        self.llista_iw = ''
        # DICCIONARIS
        self.refs = {}
        self.peticions = {}
        self.dicc_plantilles = {}
        self.dicc_enllacos = {}
        self.dicc_altres = {}
        self.dicc_ordena = {u"en":u"{{DEFAULTSORT:"}
        self.titol_plantilles = {u'en' : u'Template:',
                                 u'fr' : u'Modèle:',
                                 u'es' : u'Plantilla:',
                                 u'pt' : u'?:',
                                 u'oc' : u'?'}
        self.us_plantilles = {u'en':u"/doc"}
        self.dicc_categories = {u"en":u"Category:"}
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

        self.canvis_pre = {u"Anskar":u"Anskar"}
        self.canvis_post = {u"Veu també":u'Vegeu també',
                            u'*i.*e.':u"per exemple"}
        # ALTRES VARIABLES
        self.cops_k_passa = 1

if __name__ == '__main__':
    try:
        app = Inici()
        app.main()
    finally:
        wikipedia.stopme()
