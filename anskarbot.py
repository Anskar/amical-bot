#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wikipedia, codecs, re, catlib
import os
import subprocess
import sys
import pywikibot
import string
import uberref

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

    def romans(self, nombre,divisio_anterior=0):
        """Canvia un nombre àrab a nombres romans.
        No pot ser major de 3999"""
        try:
            nombre = int(nombre)
        except:
            return nombre
        if nombre > 3999:
            print 'No pot ser més gran de 3999.... encara'
            return nombre
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

    def segles(self,text):
        print "* PROCESSANT ELS SEGLES TROBATS AL TEXT *"
        dicc_temporal = {u"early" : u" principis del ",
                         u"mid" : u" mitjans del ",
                         u"late" : u" finals del ",
                         u"by" : u" durant el "}
        text = text
        for segles in re.finditer('(\w*) (\d*)(\w*).?(\d*)(\w*)[ |-](centur[y|ies])\s(\w*)', text):
            zero0 = segles.group(1)
            zero1 = segles.group(3)
            primer = segles.group(2)
            segon = segles.group(4)
            tercer = segles.group(7)
            if tercer == 'AD':
                crist = ' d.C.'
            elif tercer == 'BC':
                crist = ' a.C.'
            else:
                crist = ' '+tercer
            if primer == '' and segon == '':
                segon = segles.group(5)
            if primer == '':
                durant = self.pagina_re(zero1,dicc_temporal)
                text_trad = durant+' segle '+self.romans(segon)+crist
            elif primer != '' and segon != '':
                durant = self.pagina_re(zero0,dicc_temporal)
                text_trad = durant+' segles '+self.romans(primer)+u'-'+self.romans(segon)+crist
            text = text.replace(segles.group(), text_trad,1)
        return text

    def errorsPre(self,text):
        text = text
        if self.prova_maquillatge == False: return text
        print "* PROCESSANT ELS ERRORS CONEGUTS ABANS DE LA TRADUCCIÓ *"
        uberref.main()

        if self.idioma_original == 'en': text = self.segles(text)
        text = self.pagina_re(text,self.canvis_pre)
        return text

    def pagina_re(self, text, dicc):
        """Reemplazo múltiple de cadenas en Python."""
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
            self.pagina_discussio_usuari = re.search(r'\[\[.+\]\]',peticio)
        else:
            print u"Sembla que l'usuari ha signat'"
            falta = ''

        print "* GRAVANT L'ARTICLE A LA VIQUI *"
        pagina = u'Usuari:Anskarbot/Traduccions/'+self.titol_escollit
        enllac_pagina = u"[["+pagina+u"|aquesta pàgina de proves]]"
        pagina = wikipedia.Page('ca',pagina)
        pagina.put(text,u"Anskarbot editant un article traduït",minorEdit=False,force=True)

        print "* DEIXANT L'AVÍS A LA PÀGINA DE L'USUARI *"
        missatge = u"\n== Petició de traducció ==\n*La vostra petició de traducció de l'article '''" + self.titol_original + u"''' es troba en " + enllac_pagina + u".Fixeu-vos bé '''que no és la mateixa pàgina on havíeu posat la petició de traducció'''. Quan repasseu la traducció podeu fer suggeriments de millora a [[Usuari:Anskarbot/Errors|la pàgina de millores del bot]] per anar polint la traducció. Gràcies."+falta+u" --~~~~\n"
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

class Plantilles:

    def gestionaPlantilles(self,plantillatxt,j=-1):
        plantillatxt = plantillatxt
        if self.prova_plantilles == False: return plantillatxt
        print u'* GESTIONANT PLANTILLA *'
        plantilla = self.textATupla(plantillatxt)
        llista_parametres = []
        parametres_ca = []
        plantilla_txt_ca = ''
        print plantilla[0]
        try:
            plantilla_ca = self.cercaInterviquis(wikipedia.Page(self.idioma_original, self.titol_plantilles[self.idioma_original]+plantilla[0]))
        except:
            self.pregunta('A que la caga aqui?',False)
            return plantillatxt
        if plantilla_ca:
            print plantilla_ca
            print type(plantilla_ca)
            try :
                text = plantilla_ca.get()
            except wikipedia.IsRedirectPage, arg:
                plantilla_ca = wikipedia.Page('ca',arg[0])
                text = plantilla_ca.get()
            parametres = re.findall(r'\{\{\{(\w+)\|\}\}\}',text, re.UNICODE)
            llista_parametres = list(set(x+' = ' for x in parametres if unicode(x).isdigit() == False))
            parametres_ori = [y for y in plantilla[1] if plantilla[1] != []]
            while j < len(parametres_ori)-1:
                j+=1
                print str(j)+':'+str(len(parametres_ori))
                try: nom,valor = parametres_ori[j].split(u'=',1)
                except: llista_parametres.append(self.traductor(parametres_ori[j]).lower());continue

                nom_trad = self.traductor(nom).replace('*','').lower().strip()+' = '

                valor_trad = self.traductor(valor).replace('*','').lstrip()
                print nom_trad

                if nom_trad in llista_parametres:
                    print 'Coincideixen les traduccions dels parametres'
                    llista_parametres[llista_parametres.index(nom_trad)] = nom_trad+valor_trad
                    try:
                        llista_parametres.remove(nom)
                        print 'Esborrat el paràmetre en llengua original dins la plantilla en català'
                    except:
                        print "La plantilla en català no contenia el paràmetre en l'idioma original"
                else:
                    print 'No coincideixen les traduccions dels parametres'
                    llista_parametres.append(nom.strip()+U' = '+valor.strip())
            parametres_ca = llista_parametres
            parametres_ca = [x for x in parametres_ca if x.endswith('= ') == False]
            plant_ca = (plantilla_ca.titleWithoutNamespace(),parametres_ca)
            plantilla_txt_ca = self.plantillaAText(plant_ca)
        else:
            print 'Sembla que la plantilla en catala no existeix'
            plantilla_txt_ca = self.plantillaAText(plantilla)
        plantilla_txt_ori = plantillatxt
        print u"Plantilla original:\n"+plantilla_txt_ori
        print u"Plantilla en català:\n"+plantilla_txt_ca
        return plantilla_txt_ca

    def plantillaAText(self,plantilla):
        plantilla_txt = u"{{"+plantilla[0]+u"\n"
        print plantilla
        for parametre in plantilla[1]:
            parametre = parametre.replace('\n','')
            plantilla_txt += u"|"+parametre+u'\n'
        plantilla_txt += u"}}"
        return plantilla_txt

    def textATupla(self,plantilla):
        plantilla = plantilla[2:-2]
        plantilla = plantilla.replace('\n','')
        llista = plantilla.split(u'|')
        tupla = (llista[0],llista[1:])
        return tupla

class Gestio:

    def gestiona_commons(self, enllac):
        """Gestiona els fitxers de commons"""
        print u'* PROCESSANT UN FITXER DE COMMONS *'
        print enllac
        text_a_trad = re.search(r'[|]([^|]+)\]\]',enllac, re.UNICODE)
        print text_a_trad.group(1)
        if text_a_trad:
            text_traduit = self.traductor(text_a_trad.group(1))
            print text_traduit
            text_traduit = text_traduit.replace('*', '')
            enllac = enllac.replace(text_a_trad.group(1),text_traduit)
        return enllac

    def gestiona_enllac(self, enllac):
        """Gestiona els enllaços de text"""
        enllac = enllac
        if self.prova_enllacos == False: return enllac
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
                enllac_ori = re.findall(r'\[\[(.+?)[#\|].*?\]\]',enllac_red, re.UNICODE)[0]
            else:
                enllac_red = wikipedia.Page(self.idioma_original,enllac_ori).get(get_redirect=True)
                enllac_ori = re.findall(r'\[\[(.+?)\]\]',enllac_red, re.UNICODE)[0]
                print enllac_ori
                print 'Tractem aquesta excepció'
            try:
                iws = wikipedia.Page(self.idioma_original,enllac_ori).linkedPages()[0].interwiki()
                print 'És una redirecció'
            except:
                print u'Ni punyetera idea què fer aqui :('
                iws = ''
        except wikipedia.NoPage:
            print 'Enllaç vermell'
            return text_trad
        except:
            return text_trad
        enllac_final = u''
        try:
            print 'Això hauria de funcionar'
            iw = [x for x in iws if iw.title().find(u'[[ca:') != -1][0]
            enllac_trad = iw.titleWithoutNamespace()
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
        except:
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
                if self.tria_enllacos ==True:
                    enllac_final = u"[[:"+self.idioma_original+u':'+enllac_ori+u'|'+text_trad+u']]'
                else:
                    enllac_final = text_trad
        print enllac_final
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

    def redireccions(self, pagina, idioma,text=True):
        try:
            pagina = wikipedia.Page(idioma,pagina)
            text_pagina = pagina.get()
        except wikipedia.IsRedirectPage:
            text_redirect = pagina_trobada.get(get_redirect=True)
            text_redirect = re.findall(r'\[\[.+?\]\]', text_redirect)[0][2:-2]
            pagina = wikipedia.Page(idioma,text_redirect)
            text_pagina = pagina_redirect.get()
        except wikipedia.NoPage:
            print 'No existeix aquesta pàgina'
            return ''
        except:
            print 'No sé com gestionar aquesta pàgina'
            return ''
        print text_pagina
        if text == True: return text_pagina
        else: return pagina

    def gestiona_plantilles(self, plantilla):
        """Gestiona les plantilles"""
        print u'* PROCESSANT UNA PLANTILLA *'
        plantilla_titol = self.titol_plantilles[self.idioma_original]+plantilla[2:-2].split('|')[0].strip()
        print plantilla_titol
        pagina = wikipedia.Page(self.idioma_original,plantilla_titol+self.us_plantilles[self.idioma_original])
        print pagina
        plantilla_ca = self.plant_ca(plantilla,self.idioma_original)
        print plantilla_ca
        if plantilla_ca:
            print u'Trobada la plantilla en català'
            print plantilla_ca
            plantilla_ca = plantilla.replace(plantilla.split('|')[0].strip(), u"{{"+plantilla_ca.title())
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
            return
        elif plantilla_ori[0].find(u'REF') != -1:
            plantilla_ori = re.sub(r'\sREF.+', u'',plantilla_ori[0])
        else:
            plantilla_ori = plantilla_ori[0]

        print u'{{'+plantilla_ori+u'}}'
        nom = plantilla_ori.rstrip()
        nom = nom.lstrip()
        pagina = self.titol_plantilles[idioma]+nom
        plantilla_ori = self.redireccions(pagina+self.us_plantilles[self.idioma_original], self.idioma_original)
        if plantilla_ori == '':
            plantilla_ori = self.redireccions(pagina, self.idioma_original)
        inici = plantilla_ori.find(u'[[ca:')
        if inici == -1:
            missatge = u'No existeix la plantilla en català'
            return
        else:
            print u'Trobada la plantilla en català'
            final = plantilla_ori.find(u']]',inici)
            plantilla_ca = plantilla_ori[inici+15:final]
            return plantilla_ca

    def plantillaAText(self,plantilla):
        plantilla_txt = u"{{"+plantilla[0]
        for parametre in plantilla[1]:
            parametre = parametre.replace('\n','')
            plantilla_txt += u"|"+parametre+'\n'
        plantilla_txt += u"}}"
        return plantilla_txt

class Diccionaris:

    def ordena_diccionari(self, dicc, count=0,finalc=0):
        """Repassa el diccionari self.refs per gestional el codi.
        Cada codi té una marca que es troba en el diccionari de tuples self.marques"""
        print u'*** PROCESSANT EL DICCIONARI DE REFERÈNCIES ***'
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
                nou_text = self.gestionaPlantilles(nou_text)
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
            elif valor.startswith(u' REFGC'): #Codi entre <gallery></gallery>
                print u'* PROCESSANT FITXERS DE COMMONS DINS <gallery> *'
                print nou_text
                inicic = nou_text.find('|',finalc)
                finalc = nou_text.find('\n', inicic)
                text_peu = self.traductor(nou_text[inicic+1:finalc])
                nou_text = nou_text.replace(nou_text[inicic+1:finalc],text_peu)
                print nou_text
                dicc[valor] = nou_text
            elif valor.startswith(u' REFEC'): # Enllaços de commons
                nou_text = self.gestiona_commons(dicc[valor])
                dicc[valor] = nou_text

class PreCercaSubst:

    def cerca(self, text, par=0, inici=0, comm=0):
        """Cerca les marques de codi i les substitueix per REF"""
        print u'*\n================================================================'
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
                y = [x for x in self.commons.iterkeys() if x in valor]
                if y != [] and valor.startswith(u'[['):
                    print comm
                    print valor
                    print x
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
        print u'================================================================\n*'
        return text

class Interviqui:

    def cercaInterviquis(self,pagina,ca=True):
        print pagina
        print type(pagina)
        try:
            iws_pagina = pagina.interwiki()
            print 'Aquesta pagina esta a wikipedia'
        except wikipedia.IsRedirectPage, arg:
            iws_pagina = wikipedia.Page(self.idioma_original,arg[0]).interwiki()
            print 'Es una redireccio'
        except wikipedia.NoPage:
            print 'Aquesta pàgina no existeix wikipedia?'
            return
        if iws_pagina == [] or iws_pagina == None:
            print 'Pero sembla que no te els enllacos al text'
            print pagina.title()
            print type(pagina.title())
            if pagina.title().find(u'Template:') != -1:
                pagina_doc = wikipedia.Page(self.idioma_original,pagina.title()+'/doc')
                print 'Busquem a la subpagina "/doc"'
                print pagina_doc
                try:
                    text_pagina = pagina_doc.get()
                except wikipedia.IsRedirectPage, arg:
                    print 'Es una redireccio'
                    pagina_doc = wikipedia.Page(self.idioma,arg[0])
                    text_pagina = pagina_doc.get()
                except:
                    print 'Ja no se que fer, nano'
                    text_pagina = ''
                iws = re.search('\[\[ca:(.+)\]\]',text_pagina)
                if iws:
                    return wikipedia.Page('ca',iws.group(1))
                else:
                    print 'Sembla que tampoc hi ha els iws en la pagina "/doc"'
            else:
                print 'Que esta passant qui'
            try:
                iws_pagina = wikipedia.DataPage(pagina).interwiki()
                print 'Trobada la wikidata'
            except wikipedia.IsRedirectPage, arg:
                iws_pagina = wikipedia.DataPage(self.idioma,arg[0]).interwiki()
                print 'Es una redireccio'
            except wikipedia.NoPage:
                print 'Aquesta pàgina no existeix a wikidata'
                return
        for iw in iws_pagina:
            if ca:
                if iw.site().language() == 'ca':
                    print iw
                    return iw
            else:
                return iws_pagina

    def treuInterviquis(self,pagina,text,llista_iw=''):
        text = text
        if self.prova_interviqui == False: return text
        print "* NETEJANT INTERVIQUIS *"
        iws = pagina.interwiki()
        for iw in iws:
            iw = unicode(iw)
            text = text.replace(iw,'')
            llista_iw += iw+u"\n"
        llista_iw += u"[["+self.idioma_original+u":"+self.titol_original+u"]]"
        llista_iw = llista_iw.split(u'\n')
        llista_iw.sort()
        self.llista = u'\n'.join(llista_iw)
        print u"Interviquis trvades al text:\n"+self.llista
        return text

class Pagines:

    def paginesClau(self,pagina):
        self.idioma_original = self.peticions[pagina][1][0]
        print 56*u"*"+u"\nIdioma de traducció: \n*"+self.idioma_original
        self.titol_original = self.peticions[pagina][1][1]
        print u"Títol de la pàgina a traduir: \n*"+self.titol_original
#        print self.peticions[pagina][1][2]
        self.pagina_discussio_usuari = re.findall(ur'Usuari Discussió:\w+', self.peticions[pagina][1][2])[0]
        self.usuari_peticio = re.findall(ur'Usuari:(\w+)', self.peticions[pagina][1][2])[0]
        print u"Pàgina de discussió de l'usuari/a que demana la traducció: \n*"+self.pagina_discussio_usuari
        try: self.pagina_regex = self.peticions[pagina][1][3]
        except: pass
        try:
            if self.peticions[pagina][1][4].find(u'títol=') != -1:
                self.titol_escollit = self.peticions[pagina][4].split()
                missatge =  u"S'ha demanat aquest títol de pàgina provisional: \n*"
            elif self.peticions[pagina][1][5].find(u'títol=') != -1:
                self.titol_escollit = self.peticions[pagina][5].split()
                missatge =  u"S'ha demanat aquest títol de pàgina provisional: \n*"
            else:
                self.titol_escollit = self.titol_original
                missatge = u"El títol de la pàgina provisional coincideix amb el títol original."
        except:
            self.titol_escollit = self.titol_original
            missatge = u"El títol de la pàgina provisional coincideix amb el títol original."
        try:
            if self.peticions[pagina][1][4].find(u'enllaços=') != -1:
                self.tria_enllacos = True
            elif self.peticions[pagina][1][5].find(u'enllaços=') != -1:
                self.tria_enllacos = True
        except:
            self.tria_enllacos = False
        print missatge+self.titol_escollit
        print u"S'ha demanat conservar els enllaços originals?: \n*"+str(self.tria_enllacos)+u"\n"+56*u"*"

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
        except wikipedia.NoPage, arg:
            return u"No he sabut trobar la pàgina demanada. Sembla que "+arg[0]+u" no existeix en la viqui demanada. --~~~~"
        text_original = text
        text = self.treuInterviquis(pagina,text)
        text = self.treuCategories(pagina,text)
        text = re.sub(r'%s.+\}\}\n' %self.dicc_ordena[self.idioma_original],'',text)
        text = self.errorsPre(text)
        while text.find(u'\n\n\n') != -1:
            text = text.replace(u'\n\n\n',u'\n\n')
        text = text.replace(u"==\n",u"==\n\n")
        text = text.replace(u"\n==",u"\n\n==")
        capitols = re.split(r'\n\n', text)
        if '' in capitols:
            capitols.remove('')
        for capitol in capitols:
            if capitol == '':
                print u'**************************\n* Aquest capítol és buit *\n**************************'
                continue
            capitol_ori = capitol
            cap += 1
            #if cap < 8:
                #continue
            print u"********************\n********************\n* Capítol "+str(cap)+u"/"+str(len(capitols))+u" *\n********************\n********************"
            print "&&&&&&&&&&&&&&&&&&&\n&& TEXT ORIGINAL &&\n&&&&&&&&&&&&&&&&&&&"
            print capitol
            capitol = capitol.replace(u'\n*', u'\n* ') # La llista no numerada ha de contenir un espai entre l'asterisc i la frase...
            capitol = capitol.replace('*', ' ASTR ')
            capitol = re.sub(r"(?!')''", " '' ", capitol)
            capitol = re.sub(r"'''", " ''' ", capitol)
            capitol = re.sub(r'\n#',' SOSTINGUT ', capitol)
            capitol = re.sub(r'[$]', ' SIMBOLDOLLAR ', capitol)
            capitol = capitol.replace(u'&ndash;',u'–')
            capitol = capitol.replace(u'&mdash;', u'—')
            codi = re.findall(r'[\w]+=".+?"',capitol)
            ncodi = 0
            for estil in codi:
                print '* CERCANT ESTILS DE TEXT *'
                ncodi = str(ncodi).zfill(4)
                valor = u' REFZZ%s ' %(ncodi)
                capitol = capitol.replace(estil, valor)
                self.refs[valor] = estil
                ncodi = int(ncodi) + 1
            codi = re.findall(r'<[Mm]ath>.+?</[Mm]ath>',capitol,re.MULTILINE)
            ncodi = 0
            for mates in codi:
                print '* CERCANT CODI LaTex *'
                ncodi = str(ncodi).zfill(4)
                valor = u' REFWM%s ' %(ncodi)
                capitol = capitol.replace(mates, valor)
                print mates
                self.refs[valor] = mates
                ncodi = int(ncodi) + 1
            codi = re.findall(r'(http://[\w./\~\+\-&=\?\d]+)',capitol)
            ncodi = 0
            for webs in codi:
                print "* CERCANT URL's *"
                print webs
#                raw_input()
                ncodi = str(ncodi).zfill(4)
                valor = u' REFWY%s ' %(ncodi)
                capitol = capitol.replace(webs, valor)
                self.refs[valor] = webs
                ncodi = int(ncodi) + 1
            codi = re.findall(r'<[Cc]ode>.+?</[Cc]ode>',capitol,re.MULTILINE)
            ncodi = 0
            for m_code in codi:
                print '* CERCANT CODI *'
                ncodi = str(ncodi).zfill(4)
                valor = u' REFWZ%s ' %(ncodi)
                capitol = capitol.replace(m_code, valor)
                self.refs[valor] = m_code
                print m_code
                ncodi = int(ncodi) + 1
            fitxerst = []
            fitxers = re.findall(r'<gallery>.+</gallery>', capitol,re.DOTALL)
            print fitxers
            ncodi = 0
            for m_code in fitxers:
                print '* CERCANT FITXERS DE COMMONS DINS <gallery>*'
                ncodi = str(ncodi).zfill(4)
                valor = u' REFGC%s ' %(ncodi)
                capitol = capitol.replace(m_code, valor)
                self.refs[valor] = m_code
                print m_code
                ncodi = int(ncodi) + 1
            if self.idioma_original == u'en' and capitol.find(u'entur') != -1:
                capitol = self.segles(capitol)
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
            while text.find('REF') != -1:
                text = text.replace(u'*', u' ')
                print '*** ENCARA HI HA REF PER CANVIAR ***'
                text = self.referText(text)
            print '**************\n*** ACABAT ***\n**************'
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
            while text.find(u'  ') != -1:
                text = text.replace(u'  ', u' ')
            text_final += text + u'\n\n' + capitol_ori + u"\n\n"
            self.refs = {}
            self.dicc_enllac = {}
            print u'888888888888888888\n  88 Original 88  \n888888888888888888\n'+capitol_ori
            print u'8888888888888888888\n  88 Traducció 88  \n8888888888888888888\n'+text
        while text_final.find(u'  ') != -1:
            text_final = text_final.replace(u'  ', u' ')
        categories = self.cercaCategories(pagina,text)
        text_final += self.cat_original+u"\n\n"+categories+u"\n\n" + self.llista_iw
        while text_final.find(u'\n\n\n') != -1:
            text_final = text_final.replace(u'\n\n\n',u'\n\n')
        text_final = text_final.replace(u'==\n\n',u'==\n')
        text_final = text_final+u"\n\n==Notes de traducció==\n*Les plantilles en vermell són les que no s'han pogut trobar la corresponent plantilla en català. Això no vol dir que no existeixi, sino que no s'ha pogut trobar automàticament, ja sigui per que no hi ha el corresponent enllaç interviqui, o per que, realment, no existeix la plantilla en català. En cas que trobeu la plantilla corresponent us agrairia que li posesiu el seu enllaç interviqui a la plantilla en l'idioma original per poder trobar-la en properes traduccions. Gràcies. --~~~~\n*He optat per posar totes els possibles paràmetres que admet la plantilla en català perque és complicat encertar els paràmetres coincidents en una traducció literal. Intenteré que almenys les plantills de referènciess quedin perfectament traduïdes i amb la resta anirem poc a poc. --~~~~\n*És possible que quan estigui implementat Wikidata sigui més fàcil saber la coincidència de paràmtres originals i en català, però per ara és força complicat. --~~~~\n*Podeu comentar possibles millores en el bot de traducció en [[Usuari:Anskarbot/Errors|aquesta pàgina]]. --~~~~\n*Les paraules que el programa [[Apertium]] encara no tradueix queden registrades automàticament. Si trobeu alguna millora en la traducció podeu expresar-ho a la mateixa [[Usuari:Anskarbot/Errors|pàgina d'errors]]. --~~~~"
        text_final = self.postTrad(text_final)
        registre = open('registres/registre-%s.txt' %self.titol_original,'w')
        registre.write(text_final.encode('utf-8'))
        registre.close()
        return text_final

    def referText(self, text):
        """Canvia les referències de codi REF...... pel valor corresponent del diccionari self.refs"""
        print u'*** REFENT EL TEXT ***'
        marca = re.findall(r'REF\w+\d+ ', text)
        print text
        for ref in marca:
            print ref
            text = text.replace(ref, self.refs[u' '+ref])
        return text

    def postTrad(self,text):
        print "* GESTIONANT EL TEXT DESPRÉS DE LA TRADUCCIÓ *"
        enxel = re.findall(r' en (\d{1-4})',text)
        print enxel
        for data in enxel:
            text = text.replace(' en %' %data, ' el %' %data)
            text = text.replace(' En %' %data, ' El %' %data)
        text = self.errorsPost(text)
        text = self.pagina_re(text,self.commons)
        return text

class Categories:

    def treuCategories(self,pagina,text):
        text = text
        if self.prova_categories == False: return text
        print "* NETEJANT CATEGORIES *"
        llista_cat = u"<!-- Categories trobades en el text original. Amagades per no tenir categories en vermell"
        categories = pagina.categories()
        for categoria in categories:
            print categoria.title()
            text = re.sub(ur'\[\[%s.?\]\]\n'%categoria.title() , u'',text)
            categoria = u"\n[["+categoria.title()+u"]]"
            llista_cat += categoria
        llista_cat += u' -->'
        self.cat_original = llista_cat
        return text

    def cercaCategories(self,pagina,text,n=1,p=1,cat_ca='',categories_ca=[],parents=[],categories_pare=[],limit=3):
        text = text
        if self.prova_categories == False:
            self.cat_original = ''
            return text
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
                                categoria_print = u"** "+unicode(y)+u" **"
                                print 60*u"*"+u"\n*****     S'afegirà la següent categoria en català     *****\n*"+categoria_print.center(58)+u"*\n"+60*u"*"
                                print

                                categories_ca.append(u"[["+y.title()+u']]\n')
            supercategories = categoria.categories()
            if n < limit:
                categories_pare.extend(supercategories)
            if p == len(categories):
                categories.extend(categories_pare)
                categories_pare = []
                if n == limit and categories_ca != []:
                    break
                if n == limit and categories_ca == []:
                    limit += 1
                n += 1
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

class Peticions:

    def cercaPeticions(self,p=0):
        print u'* COMENÇA EL PROCÉS DE CERCA DE PETICIONS DE TRADUCCIÓ *'
        articles = catlib.Category(u'ca',u"Categoria:Peticions de còpia i preprocés per traducció automàtica").articles()
        print u"* COMENÇA EL PROCÉS DE GESTIÓ DE LES PLANTILLES DE PETICIÓ DE TRADUCCIÓ *"
        for pagina in articles:
            plantilles = pagina.templatesWithParams()
            for plant in plantilles:
                if plant[0].find(u'etició de traducció') != -1:
                    print plant
                    clau = unicode(pagina)+str(p).zfill(2)
                    print clau
                    print pagina
                    self.peticions[clau] = plant
                    p += 1
        if p > 1: peticions = u" peticions"
        else: peticions = u" petició"
        print u"*** S'han trobat "+str(p)+ peticions+u" de traducció ***"

    def treuPeticio(self, pagina):
        if self.prova_gravar_viqui == False: return
        print u"* COMENÇA EL PROCÉS PER TREURE LA PLANTILLA JA PROCESSADA *"
        pagina_txt = re.findall(r'\[\[ca:(.+)\]\]',pagina)
        print pagina_txt
        print pagina
        text = wikipedia.Page('ca',unicode(pagina_txt[0])).get()
        plantilla = self.plantillaAText(self.peticions[pagina])
        plantilla = plantilla.replace('\n','')
        text = text.replace(u'{{petició de traducció',u'{{Petició de traducció')
        text = text.replace(plantilla,'')
        wikipedia.Page('ca',unicode(pagina_txt[0])).put(text,u"Anskarbot traient la plantilla de traducció." ,minorEdit=False,force=True)

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

class Inici(Pregunta,Peticions,Text,Pagines,Interviqui,PreCercaSubst,Diccionaris,Gestio,Categories,Apertium,Wiki,Maquillatge,Proves,Plantilles):

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
            self.netejaVariables()
            self.paginesClau(peticio)
            text = self.preTrad(peticio)
            self.article(text,peticio)
            self.treuPeticio(peticio)
            print u'****************************************'
            print u'********** ACABADA LA PETICIÓ **********'
            print u'****************************************'

        print u'\nOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
        print (u'OOOOO   ACABADES LES TRADUCCIONS   OOOOO').center(60)
        print u'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
        return 0

    def netejaVariables(self):
        self.llista_parents = []
        self.llista_iw = ''
        self.cat_original = []

    def variables(self):
        # DICCIONARIS
        self.refs = {}
        self.peticions = {}
        self.dicc_plantilles = {}
        self.dicc_enllacos = {}
        self.dicc_altres = {}
        self.commons = {u'Image:' : u"Fitxer:",
                        u"Archivo:" : u"Fitxer:",
                        u"File:" : u"Fitxer:",
                        u"Arxiu:" : u"Fitxer:"}
        self.dicc_ordena = {u"en" : u"{{DEFAULTSORT:",
                            u"fr" : u"{{DEFAULTSORT:",
                            u"es" : u"",
                            u"pt" : u"",
                            u"oc" : u"{{DEFAULTSORT:",}
        self.titol_plantilles = {u'en' : u'Template:',
                                 u'fr' : u'Modèle:',
                                 u'es' : u'Plantilla:',
                                 u'pt' : u'Predefinição:',
                                 u'oc' : u'Modèl:'}
        self.us_plantilles = {u'en' : u"/doc",
                              u"fr" : u"/Documentation",
                              u"es" : u"/doc",
                              u"pt" : u"/doc",
                              u"oc" : u"/Documentacion"}
        self.dicc_categories = {u"en" : u"Category:",
                                u"fr" : u"Catégorie",
                                u"es" : u"Categoría",
                                u"pt" : u"Categoria",
                                u"oc" : u"Categoria"}
        self.canvis_pre = {u"Anskar":u"Anskar"}
        self.canvis_post = {u"Veu també":u'Vegeu també',
                            u'*i.*e.':u"per exemple"}
        # ALTRES VARIABLES
        self.cops_k_passa = 1
        # LLISTES
        self.cerques =[(u'<!--',u'-->', u' REFCO%s '), # Llista de tuples que ...
                       (u'<' , u'>' , u' REFWC%s '),
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

if __name__ == '__main__':
    try:
        app = Inici()
        app.main()
    finally:
        wikipedia.stopme()
