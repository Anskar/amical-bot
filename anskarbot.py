#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    i s'ha de pod<source lang=python>
#!/usr/bin/env python
# -*- coding: utf-8 -*-


import wikipedia, codecs, re, catlib
import os
import subprocess
import sys
import pywikibot
import string
import time
import logging
import mwparserfromhell
import urllib

from gi.repository import Gtk

path = os.path.dirname(sys.argv[0])
logging.basicConfig()

class Finestra:
    def finestra(self):
        self.escull = 0
        self.final = 0
        idiomes = {'en':'Anglès',
                   'es':'Castellà',
                   'fr':'Francès',
                   'pt':'Portuguès',
                   'oc':'Occità',
                   'it':'Italià'}
        win = Gtk.Builder()
        win.add_from_file('frame.glade')
        self.prog = win.get_object('window1')
        self.prog.connect('destroy',self.destroy)

        cancella = win.get_object('button1')
        cancella.connect('clicked',self.cancella)
        desfes = win.get_object('button2')
        desfes.connect('clicked',self.desfes)
        aplica = win.get_object('button3')
        aplica.connect('clicked',self.aplica)
        self.boto_desa = win.get_object('button4')
        self.boto_desa.connect('clicked',self.desa)

        idioma = win.get_object('label1')
        idioma.set_text(idiomes[self.idioma_original])


        titol_plantilla_ori = win.get_object('label3')
        titol_plantilla_ori.set_text(self.tupla_ori[0])
        titol_plantilla_ca = win.get_object('label4')
        titol_plantilla_ca.set_text(self.tupla_ca[0])

        self.marca_ori = win.get_object('cellrenderertoggle1')
        self.marca_ori.connect('toggled',self.escull_ori)
        self.amaga_ori = win.get_object('cellrenderertoggle4')
        self.amaga_ori.connect('toggled', self.vista_ori)
        self.marca_ca = win.get_object('cellrenderertoggle2')
        self.marca_ca.connect('toggled',self.escull_ca)
        self.amaga_ca = win.get_object('cellrenderertoggle5')
        self.amaga_ca.connect('toggled', self.vista_ca)

        self.marca_final = win.get_object('cellrenderertoggle3')
        self.marca_final.connect('toggled',self.marca)

        self.conta_par_ori = win.get_object('label5')
        self.conta_par_ca = win.get_object('label6')

        self.llista_tria = win.get_object('treestore1')

        self.llista_original = win.get_object('liststore1')
        self.cons_ori()
        self.llista_catala = win.get_object('liststore2')
        self.cons_ca()

        self.ordre_ori = win.get_object('ordre-ori')
        self.ordre_ca = win.get_object('ordre-ca')
        self.par_ori = win.get_object('par-ori')
        self.par_ca = win.get_object('par-ca')

        self.prog.show()

        Gtk.main()

    def vista_ori(self, path, cell_toggled):
        print "S'amaga?"
        iter_amaga = self.llista_original.get_iter(cell_toggled)
        self.llista_original.set_value(iter_amaga,1,False)
        self.llista_original.set_value(iter_amaga,0,'z')

    def vista_ca(self, path, cell_toggled):
        iter_amaga = self.llista_catala.get_iter(cell_toggled)
        self.llista_catala.set_value(iter_amaga,1,False)
        self.llista_catala.set_value(iter_amaga,0,'z')

    def marca(self,path,cell_toggled):
        iter_marca = self.llista_tria.get_iter(Gtk.TreePath(cell_toggled))
        bol = self.llista_tria.get_value(iter_marca,2)
        self.llista_tria.set_value(iter_marca,2,not bol)
        marca_fill = not bol
        print self.llista_tria.iter_has_child(iter_marca)
        if self.llista_tria.iter_has_child(iter_marca) == True:
            iter_fill = self.llista_tria.iter_children(iter_marca)
            while iter_fill:
                self.llista_tria.set_value(iter_fill,2,marca_fill)
                iter_fill = self.llista_tria.iter_next(iter_fill)


        print cell_toggled
        print len(cell_toggled)

    def cons_ori(self):
        count = 0
        self.conta_par_ori.set_text(str(self.escull)+u':'+str(len(self.tupla_ori[1])))
        self.llista_original.clear()
        for parametre in self.tupla_ori[1]:
            count += 1
            plantilla_original = self.llista_original.append([parametre,True,count,False])

    def cons_ca(self):
        count = 0
        self.conta_par_ca.set_text(str(len(self.llista_tria))+u':'+str(len(self.tupla_ca[1])))
        self.llista_catala.clear()
        for parametre in self.tupla_ca[1]:
            count += 1
            plantilla_ca = self.llista_catala.append([parametre,True,count,False])

    def escull_ori(self,path, cell_toggled):
        path = Gtk.TreePath(cell_toggled)
        iter_marca = self.llista_original.get_iter(path)
        bol = self.llista_original.get_value(iter_marca,3)
        print self.llista_original.get_value(iter_marca,0)
        self.llista_original.set_value(iter_marca,3,not bol)
        if not bol == False: self.escull -= 1
        else: self.escull += 1

    def escull_ca(self,path, cell_toggled):
        self.cons_ca()
        path = Gtk.TreePath(cell_toggled)
        iter_marca = self.llista_catala.get_iter(path)
        bol = self.llista_catala.get_value(iter_marca,3)
        print self.llista_catala.get_value(iter_marca,0)
        self.llista_catala.set_value(iter_marca,3,not bol)

    def desa(self,*args):
        text = u''
        pagina = 'Usuari:Anskarbot/'+self.idioma_original+'/Plantilles'
        pagina = wikipedia.Page('ca',pagina)
        try:
            text = pagina.get()
        except:
            pass
        text += u"\n=="+self.tupla_ca[0]+u"=="
        for x in range(len(self.llista_tria)):
            iter_pare = self.llista_tria.get_iter(x)
            parametre_ca = self.llista_tria.get_value(iter_pare,0)
            iter_fill = self.llista_tria.iter_children(iter_pare)
            while iter_fill:
                parametre_ori = self.llista_tria.get_value(iter_fill,1)
                iter_fill = self.llista_tria.iter_next(iter_fill)
                text += u'\n'+unicode(parametre_ori.decode('utf-8'))+u';'+unicode(parametre_ca.decode('utf-8'))
        pagina.put(text,u"Anskarbot traduïnt els paràmetres d'una nova plantilla")
        self.plantilla_ca_plant = text
        self.prog.destroy()

    def aplica(self, *args):
        self.ordre_ori.clicked()
        self.ordre_ca.clicked()
        parametre = [self.llista_catala.get_iter(Gtk.TreePath(x)) for x in range(len(self.llista_catala)) if self.llista_catala.get_value(self.llista_catala.get_iter(Gtk.TreePath(x)),3) == True][0]
        print self.tupla_ca[1][self.llista_catala.get_value(parametre,2)-1]
        del self.tupla_ca[1][self.llista_catala.get_value(parametre,2)-1]
        parametre = self.llista_catala.get_value(parametre,0)
        self.llista_tria.append(None,[parametre,None,False,True])
        parametres_ori = [self.llista_original.get_iter(Gtk.TreePath(x)) for x in range(len(self.llista_original)) if self.llista_original.get_value(self.llista_original.get_iter(Gtk.TreePath(x)),3) == True]
        for parametre in parametres_ori:
            del self.tupla_ori[1][self.llista_original.get_value(parametre,2)-1]
            parametre = self.llista_original.get_value(parametre,0)
            self.llista_tria.append(self.llista_tria.get_iter(Gtk.TreePath(len(self.llista_tria)-1)),[None,parametre, False,False])
        self.cons_ori()
        self.cons_ca()
        self.conta_par_ori.set_text(str(self.escull)+u':'+str(len(self.tupla_ori[1])))
        self.conta_par_ca.set_text(str(len(self.llista_tria))+u':'+str(len(self.tupla_ca[1])))
        self.final += 1
        self.par_ca.clicked()
        self.par_ori.clicked()

    def desfes(self, *args):
        esborra_pares = [self.llista_tria.get_iter(Gtk.TreePath(x)) for x in range(len(self.llista_tria)) if self.llista_tria.get_value(self.llista_tria.get_iter(Gtk.TreePath(x)),2) == True]
        print esborra_pares

        pass

    def cancella(self, *args):

        llista_ca = []
        llista_ori = []
        for x in range(len(self.llista_tria)):
            iter_pare = self.llista_tria.get_iter(Gtk.TreePath(x))
            llista_ca.append(self.llista_tria.get_value(iter_pare,0))
            iter_fill = self.llista_tria.iter_children(iter_pare)
            print llista_ca
            while iter_fill:
                llista_ori.append(self.llista_tria.get_value(iter_fill,1))
                iter_fill = self.llista_tria.iter_next(iter_fill)
            print llista_ori
        self.tupla_ca[1].extend(llista_ca)
        self.tupla_ori[1].extend(llista_ori)
        self.llista_tria.clear()
        self.escull = 0
        self.final = 0
        self.cons_ori()
        self.cons_ca()

    def destroy(self,widget):
        Gtk.main_quit()

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
        return romans

    def segles(self,text):
        segles_pas = 0
        print "* PROCESSANT ELS SEGLES TROBATS AL TEXT *"
        dicc_temporal = {u"early" : u" principis del ",
                         u"mid" : u" mitjans del ",
                         u"late" : u" finals del ",
                         u"by" : u" durant el ",
                         u"to" : u" fins ",
                         u"and" : u" i ",
                         u"the" : u" el ",
                         u"in" : u" en "}
        text = text
        ref = u" [REFSEG%s] "
        for segles in re.finditer('(\w*) (\d*)(\w*).?(\d*)(\w*)[ |-](centur[y|ies])\s(\w*)', text):
            print segles.group()
#            raw_input()
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
            if primer == '':
                if segon == '':
                    segon = segles.group(5)
                    durant = ''
                else:
                    durant = self.paginaRe(zero1,dicc_temporal)
                text_trad = durant+' segle '+self.romans(segon)+crist
            elif primer != '' and segon != '':
                durant = self.paginaRe(zero0,dicc_temporal)
                text_trad = durant+' segles '+self.romans(primer)+u'-'+self.romans(segon)+crist
            else:
                continue
            segles_pas = str(segles_pas).zfill(4)
            self.refs[ref %(segles_pas)] = text_trad
            text = text.replace(segles.group(), ref %(segles_pas),1)
            segles_pas = int(segles_pas)
            segles_pas += 1
        print text
        return text

    def errorsPre(self,text):
        text = text
        if self.prova_maquillatge == False: return text
        print "* PROCESSANT ELS ERRORS CONEGUTS ABANS DE LA TRADUCCIÓ *"
        if self.idioma_original == 'en': text = self.segles(text)
        text = self.paginaRe(text,self.canvis_pre)
        return text

    def paginaRe(self, text, dicc):
        """Reemplazo múltiple de cadenas en Python."""
        if text == "":
            return text
        if dicc == {}:
            return text
        regex = re.compile("(%s)" % "|".join(map(re.escape, dicc.keys())))
        text = regex.sub(lambda x: unicode(dicc[x.string[x.start() :x.end()]]), text)
        return text

    def errorsPost(self,text):
        print "* PROCESSANT ELS ERRORS CONEGUTS DESPRÉS DE LA TRADUCCIÓ *"
        text = self.paginaRe(text,self.canvis_post)
        return text

class Wiki:

    def article(self,text,peticio,ns=0):
        print u"PROCËS DE GRAVAR EL TEXT A LA WIKI"
        if self.prova_gravar_viqui == False:
            traduccio = codecs.open(u'traduccions/'+self.titol_original,'w',"utf-8")
            traduccio.write(text)

            traduccio.close()
            self.wikinotrad()
            return
        if self.pagina_discussio_usuari == '':
            print 'l´Usuari no ha signat?'
            falta = u" --~~~~\n*Recorda de signar les peticions de traducció, ja que si no, és impossible que una màquina com jo sàpiga qui demana la traducció. Gràcies."
            self.pagina_discussio_usuari = re.search(r'\[\[.+\]\]',peticio)
        else:
            print u"Sembla que l'usuari ha signat'"
            falta = ''

        print "* GRAVANT L'ARTICLE A LA VIQUI *"
        if self.titol_escollit:
            if u'Usuari' in self.titol_escollit:
                pagina = self.titol_escollit
                pagina_traduitde = pagina.replace(u'Usuari',u'Usuari Discussió')
            else:
                pagina = u'Usuari:Anskarbot/Traduccions/'+self.titol_escollit
                pagina_traduitde = u"Usuari Discussió:Anskarbot/Traduccions/"+self.titol_escollit
        else:
            pagina = u'Usuari:Anskarbot/Traduccions/'+self.titol_original
            pagina_traduitde = u"Usuari Discussió:Anskarbot/Traduccions/"+self.titol_original
        enllac_pagina = u"[["+pagina+u"|aquesta pàgina de proves]]"
        pagina_final = wikipedia.Page('ca',pagina)
        pagina_final.put(text,u"Anskarbot editant un article traduït",minorEdit=False,force=True)

        print "* DEIXANT L'AVÍS A LA PÀGINA DE L'USUARI *"
        missatge = u"\n== Petició de traducció ==\n*La vostra petició de traducció de l'article '''" + self.titol_original + u"''' es troba en " + enllac_pagina + u".Fixeu-vos bé '''que no és la mateixa pàgina on havíeu posat la petició de traducció'''. Quan repasseu la traducció podeu fer suggeriments de millora a [[Usuari:Anskarbot/Errors|la pàgina de millores del bot]] per anar polint la traducció. Gràcies."+falta+u" --~~~~\n"
        pagina_usuari = wikipedia.Page('ca',unicode(self.pagina_discussio_usuari))
        p = re.compile(u'\n== Petició de traducció ==\n')
        pagina_discusio = pagina_usuari.get()
        if p.search(pagina_discusio):
            pagina_discusio = p.sub(missatge,pagina_discusio,1)
        else:
            pagina_discusio = pagina_discusio+missatge
        pagina_usuari.put(pagina_discusio,u"Anscarbot deixant un missatge a la pàgina de discussió de l'usuari.",minorEdit=False, force=True)

        print "* POSANT LA PLANTILLA {{Traduït de}} A LA PÀGINA DE DISCUSSIÓ DE L'ARTICLE TRADUÏT *"
        urlversio =wikipedia.Page(self.idioma_original,self.titol_original).permalink()
        versio = re.findall(r'oldid=(\d+)',urlversio)
        pagina_traduitde = wikipedia.Page('ca', pagina_traduitde)
        pagina_traduitde.put(u'{{Traduït de|'+self.idioma_original+u'|'+self.titol_original+u'|{{subst:CURRENTDAY}}-{{subst:CURRENTMONTH}}-{{subst:CURRENTYEAR}}|'+versio[0]+u'}}\n--~~~~', u'Anskarbot incorporant la plantilla {{traduït de}} a la pàgina de discussió',minorEdit=False, force=True)

        print u"* AFEGINT LA TRADUCCIÓ A L'ÍNDEX DE TRADUCCIONS *"
        index = u'Usuari:Anskarbot/Traduccions'
        index = wikipedia.Page(u'ca',index)
        contingut_index = index.get()
        if self.titol_escollit:
            titol = self.titol_escollit
        else:
            titol = self.titol_original
        contingut_index = contingut_index.replace(u"|}",u'|-\n|* [['+pagina+'|'+titol+']]||{{ud|'+self.usuari_peticio+u'}}||{{subst:CURRENTDAY}}/{{subst:CURRENTMONTH}}/{{subst:CURRENTYEAR}}||{{subst:PAGESIZE:'+pagina+'|R}}||{{PAGESIZE:'+pagina+'|R}}\n|}')
        index.put(contingut_index, u"Anskarbot afegint la traducció a l'índex de les traduccions fetes", minorEdit=False, force=True)
        self.wikinotrad()

    def wikinotrad(self):
        traduccio = codecs.open(u'traduccions/paraules-'+self.titol_original,'w',"utf-8")
        traduccio.write("\n".join(self.no_trad))
        traduccio.close()
        if self.prova_gravar_viqui == False:
            return
        print u"* AFEGINT LES PARAULES NO TRADUIDES *"
        pagina_dicc = u"Usuari:Anskarbot/"+self.idioma_original
        pagina = wikipedia.Page('ca',pagina_dicc)
        text = pagina.get()
        print self.no_trad
        for x in self.no_trad:
            text += u"\n"+x
        pagina.put(text,u"Anskarbot afegint les paraules no traduïdes",minorEdit=False, force=True)

class Apertium:

    def traductor(self, text):
        """Crida al programa Apertium"""
        text = text
        if self.prova_traduccio == False:
            return text
        try:
            text_val = int(text)
            return text
        except:
            pass
        print "* TRADUÏNT *"
        print '=== ORIGINAL===\n' + text
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
        elif self.idioma_original == 'it':
            text_trad = subprocess.call(['apertium it-ca traduccions/original.txt traduccions/traduccio.txt'], shell = True)
#        print text_trad
        arxiu_traduit = open('traduccions/traduccio.txt', 'r')
        text_traduit = arxiu_traduit.read()
        print '=== TRADUCCIÓ ===\n' + text_traduit
        arxiu_traduit.close()
        text_traduit = unicode(text_traduit.decode('utf-8'))
        no_trad = re.findall(ur'\*\w+\s',text_traduit)
        for paraula in no_trad:
            if paraula.startswith('*REF') \
            or paraula in self.no_trad \
            or paraula.isupper() \
            or paraula.istitle():
                pass
            else:
                self.no_trad.append(paraula)
        return text_traduit

class Plantilles:

    def muntaPlantillesProcessades(self):
        pagina = wikipedia.Page('ca',u'Usuari:Anskarbot/'+self.idioma_original+u'/Plantilles')
        print u'* GESTIONANT ELS PARÀMETRES DE LA PLANTILLA *'

        text = pagina.get()
        self.seccions = pagina.getSections()
        self.plantilles_wiki = text[text.find(u'\n=='):]
#        print self.plantilles_wiki

    def parametres(self,plant_ori,plant_ca):
        n = 0
        text = self.plantilles_wiki
        self.plantilla_ca_plant = ''

        seccio = [seccio for seccio in self.seccions if plant_ca in seccio[3]]
        if seccio == []:
            print u"La plantilla no es troba en les plantilles dictades"
            plant_ori = plant_ori.strip()
            plantilla_ori = self.titol_plantilles[self.idioma_original]+plant_ori+self.us_plantilles[self.idioma_original]
            plantilla_ca = u'Plantilla:'+plant_ca
            print plantilla_ca
            try:
                text_ori = wikipedia.Page(self.idioma_original,plantilla_ori).get()
                print u'* EXTRAIENT EL TEXT DE LA PLANTILLA*'
            except:
                print '¿?¿? ALGUNA COSA HA FALLAT ¿?¿?'
                return
            parametres_ori = re.findall(r'\| *(\w+ ?-?\w* ?\w*) *=',text_ori, re.UNICODE)
            llista_parametres = list(set(x.strip() for x in parametres_ori if unicode(x).isdigit() == False))
            if llista_parametres == []:
                print 'potser no ha trobat els paràmetres originals'
                return
            self.tupla_ori = (plant_ori,llista_parametres)
            try:
                print "O potser no troba la pàgina d'ús en català?"
                text_ca = wikipedia.Page('ca',plantilla_ca).get()
            except:
                print 'Cagada pastoret'
                return
            parametres_ca = re.findall(r'\| *(\w+ ?-?\w* ?\w*) *=',text_ca, re.UNICODE)
            llista_parametres = list(set(x.strip() for x in parametres_ca if unicode(x).isdigit() == False))
            if llista_parametres == []:
                return
            self.tupla_ca = (plant_ca,llista_parametres)
            self.finestra()
            time.sleep(2)
            self.muntaPlantillesProcessades()
            plantilla_gestionada = self.plantilla_ca_plant
        else:
            print u"La plantilla ja s'ha processat en alguna altra traducció"
            inici = text.find(u"\n=="+plant_ca+u"==")
            print inici
            final = text.find(u"\n==",inici+len(u'\n=='+plant_ca+u"=="))
            print final
            if final == -1:
                plantilla_gestionada = text[inici+len(u'\n=='+plant_ca+u"=="):]
            else:
                plantilla_gestionada = text[inici+len(u'\n=='+plant_ca+u"=="):final]
        print plantilla_gestionada
        plantilla_wiki_ret = self.muntaPlantilla(plantilla_gestionada)

        print 'EUREKA'
        return plantilla_wiki_ret

    def gestionaPlantilles(self,plantillatxt,j=-1):
        if u'{{#' in plantillatxt: return plantillatxt
        plantillatxt = plantillatxt.replace('=',' = ')
        plantillatxt = plantillatxt.replace('|',' | ')

        if self.prova_plantilles == False: return plantillatxt
        print u'** GESTIONANT PLANTILLA **'
        plantilla = self.textATupla(plantillatxt)
        llista_parametres = []
        parametres_ca = []
        plantilla_txt_ca = ''
#        print plantilla[0]
        try:
            plantilla_ca = self.cercaInterviquis(wikipedia.Page(self.idioma_original, self.titol_plantilles[self.idioma_original]+plantilla[0].strip()))
        except:
            self.pregunta('¿?¿? HA SORGIT UN PROBLEMA AMB ELS ENLLAÇOS INTERWIKI ¿?¿?',False)
            return plantillatxt
        if plantilla_ca:
            prova = self.parametres(plantilla[0],plantilla_ca.titleWithoutNamespace())
            if not prova:
                return plantillatxt.replace(plantilla[0],plantilla_ca.titleWithoutNamespace())
            plantilla_a1 = self.paginaRe(plantillatxt,prova)
#            print plantilla_a1
            plantilla = self.textATupla(plantilla_a1)
            if plantilla == None:
                return plantillatxt
            parametres_ori = [y for y in plantilla[1] if plantilla[1] != []]
#            print parametres_ori
            plantilla_wiki_ges = {}
            while j < len(parametres_ori)-1:
                j+=1
#                print str(j+1)+':'+str(len(parametres_ori))
                try: nom,valor = parametres_ori[j].split(u'=',1)
                except: llista_parametres.append(self.traductor(parametres_ori[j]));continue
                nom = nom.strip()
                valor_trad = self.traductor(valor).replace('*','')
#                print nom

                llista_parametres.append(nom.strip()+u' = '+valor_trad)
            parametres_ca = llista_parametres
            parametres_ca = [x.strip() for x in parametres_ca if x.endswith('= ') == False]
            plant_ca = (plantilla_ca.titleWithoutNamespace(),parametres_ca)
            plantilla_txt_ca = self.plantillaAText(plant_ca)
        else:
            print 'Sembla que la plantilla en catala no existeix'
            plantilla_txt_ca = self.plantillaAText(plantilla)
            return plantilla_txt_ca
        plantilla_txt_ca = self.paginaRe(plantilla_txt_ca,prova)
        plantilla_txt_ori = plantillatxt
        print u"Plantilla original:\n"+plantilla_txt_ori
        print u"Plantilla en català:\n"+plantilla_txt_ca
        return plantilla_txt_ca

    def plantillaAText(self,plantilla):
        plantilla_txt = u"{{"+plantilla[0]
#        print plantilla
        for parametre in plantilla[1]:
            parametre = parametre.replace('\n','')
            plantilla_txt += u"\n|"+parametre
        plantilla_txt += u"}}"
        return plantilla_txt

    def textATupla(self,plantilla):
        print "****\n",plantilla,"\n****"
        if plantilla == None:
            return
        plantilla = plantilla[2:-2]
        plantilla = plantilla.replace('\n','')
        llista = plantilla.split(u'|')
        tupla = (llista[0],llista[1:])
        return tupla

class Gestio:

    def gestiona_commons(self, enllac):
        """Gestiona els fitxers de commons"""
        print u'* PROCESSANT UN FITXER DE COMMONS *'
        text_a_trad = re.search(r'[|]([^|]+)\]\]',enllac, re.UNICODE)
        if text_a_trad:
            text_traduit = self.traductor(text_a_trad.group(1))
            text_traduit = text_traduit.replace('*', '')
            enllac = enllac.replace(text_a_trad.group(1),text_traduit)
        return enllac

    def gestiona_enllac(self, enllac):
        """Gestiona els enllaços de text"""
        enllac = enllac
        if self.prova_enllacos == False: return enllac
        print u'** PROCESSANT UN ENLLAÇ DE TEXT **'
        print enllac
        if u':' in enllac:
            print 'És un enllaç especial, el mantindrem'
            return enllac
        enllac = enllac[2:-2]
        if u'|' in enllac:
            marca = enllac.split(u'|')
            enllac_ori = marca[0]
            text = marca[1]
            text_trad = self.traductor(text).strip()
        else:
            text = enllac
            enllac_ori = enllac
            text_trad = self.traductor(enllac).strip()
        if enllac_ori.startswith(u'#'): return text_trad
        iws = wikipedia.Page(self.idioma_original,enllac_ori)
        pagina_ca = self.cercaInterviquis(iws)
        if text.islower():
            text_trad = text_trad.lower()
        elif text.isupper():
            text_trad = text_trad.upper()
        elif text.istitle():
            text_trad = text_trad.title()
        if pagina_ca:
            text_trad = text_trad.replace("*","")
            if text_trad.lower() == pagina_ca.titleWithoutNamespace().lower():
                enllac_final = u'[['+text_trad+u']]'
            else:
                enllac_final = u'[['+pagina_ca.titleWithoutNamespace()+u'|'+text_trad+u']]'
        else:
            if self.tria_enllacos == True:
                enllac_final = u'[[:'+self.idioma_original+u':'+enllac_ori+u'|'+text_trad+u']]'
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
        taula = taula.replace(u'|', u' BARRUERAMENT ')
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
                canvi = self.gestionaPlantilles(self.refs[ref], ref)
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
        taula = taula.replace(u' BARRUERAMENT ' , u'|')
        taula = taula.replace(u' ADMIRACIO ' , u'!')
        return taula

class Diccionaris:

    def ordena_diccionari(self, dicc, count=0,finalc=0):
        """Repassa el diccionari self.refs per gestional el codi.
        Cada codi té una marca que es troba en el diccionari de tuples self.marques"""
        print u'*** PROCESSANT EL DICCIONARI DE REFERÈNCIES ***'
        claus = sorted(dicc.keys(), reverse=True)
        self.count = count
        for valor in claus:
            nou_text = dicc[valor]
            print valor, nou_text
            if valor.startswith(self.cerques[0][-1][:-4]):   # Comentaris
                print u'* PROCESSANT COMENTARI *'
                nou_text = u'<!--' + self.traductor(nou_text[4:-3]) + u'-->'
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[1][-1][:-4]): # Enllaços web
                print u'* PROCESSANT ENLLAÇ WEB *'
                inici = nou_text.find(u' ')
                nou_text = nou_text.replace(nou_text[inici:-1], self.traductor(nou_text[inici:-1]))
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[2][-1][:-4]): # Enllaços de text
                nou_enllac = self.gestiona_enllac(nou_text)
                dicc[valor] = nou_enllac
            elif valor.startswith(self.cerques[3][-1][:-4]): # Plantilles
                nou_text = self.gestionaPlantilles(nou_text)
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[4][-1][:-4]): #Codi entre <gallery></gallery>
                print u'* PROCESSANT FITXERS DE COMMONS DINS <gallery> *'
                print nou_text
                llista = nou_text.split('\n')
                text_final = u'<gallery'
                print llista
#                raw_input()
                for llista_text in llista:
                    if u'|' in llista_text:
                        veg = llista_text.count(u"|")
                        print veg
                        for a in range(veg):
                            print range(veg)
                            print a
                            if a != veg:
                                continue
                        inicic = llista_text.find(u'|')
                        text_peu = self.traductor(llista_text[inicic+1:])
                        text_final += llista_text.replace(llista_text[inicic+1:],text_peu+u"\n")
                text_final += u'</gallery>'
                dicc[valor] = text_final
            elif valor.startswith(self.cerques[5][-1][:-4]): # Referències úniques
                print u'* PROCESSANT REFERÈNCIES *'
                inici = nou_text.find(u'>')
                final = nou_text.find(u'</')
                nou_text = nou_text.replace(nou_text[inici+2:final-1], self.traductor(nou_text[inici+2:final-1]))
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[6][-1][:-4]): # Referències de grup (name o altres)
                print u'* PROCESSANT REFERÈNCIES DE GRUP *'
                inici = nou_text.find(u'>')
                final = nou_text.find(u'</')
                nou_text = nou_text.replace(nou_text[inici+2:final-1], self.traductor(nou_text[inici+2:final-1]))
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[7][-1][:-4]): # Següents ref name
                print u'* PROCESSANT REFERÈNCIES DE GRUP NAME *'
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[8][-1][:-4]): # Altre codi
                print u'* PROCESSANT ALTRE CODI *'
            elif valor.startswith(self.cerques[9][-1][:-4]): # Taules
                print u'*** PROCESSANT TAULES ***'
                nou_text = self.gestiona_taules(nou_text)
                dicc[valor] = nou_text
            elif valor.startswith(u' [REFZZ'): # Codi d'estils
                print u'* PROCESSANT ESTILS *'
            elif valor.startswith(u' [REFWM'): #Codi LaTex
                print u'* PROCESSANT CODI LaTex *'
            elif valor.startswith(u' [REFWY'): #Pàgines web
                print u'* PROCESSANT URLs *'
            elif valor.startswith(u' [REFWZ'): #Codi entre <code></code>
                print u'* PROCESSANT CODI *'
            elif valor.startswith(u' [REFRR'): #Caràcters estranys
                print u'* PROCESSANT CARÂCTERS ESTRANYS *'
            elif valor.startswith(u' [REFEC'): # Enllaços de commons
                nou_text = self.gestiona_commons(dicc[valor])
                dicc[valor] = nou_text
            elif valor.startswith(u" [REFSEG"): # segles en text anglès
                print u"* PROCESSANT SEGLES DINS EL TEXT EN ANGLÈS *"
            else:
                print u"Aqui no hauria d'arribar"
                print valor

    def muntaPlantilla(self, text):
        plantilla_wiki_ges = {}
#        print u'*****\n'+text+u'\n*****'
        text = text.replace(self.missatge_plantilla,u"")
        llista = text.split(u'\n')
#        print llista
        if '' in llista: llista.remove('')
        for x in llista:
#            print x
            if u';' not in x: continue
            diccionari = x.split(u';')
#            print diccionari
            valor,parametre = u" "+diccionari[0]+u" ",u" "+diccionari[1]+u" "
            plantilla_wiki_ges[valor] = parametre
        print plantilla_wiki_ges
        return plantilla_wiki_ges

    def muntaPaginaRE(self, re_en_pagina, idioma):
        pagina = u"Usuari:Anskarbot/"+idioma+u"/"+re_en_pagina
        titol = wikipedia.Page(u'ca',pagina)
        try: text = titol.get()
        except:
            print 'No hi ha pàgina regex a la wiki'
            return
        text = re.sub(r'','',text,flags=re.MULTILINE)
        llista = text.split(u'\n')
#        print llista
        if '' in llista: llista.remove('')
        for x in llista:
            if ';' not in x: continue
            diccionari = x.split(u';')
#            print diccionari
            valor,parametre = diccionari[0],diccionari[1]
            self.canvis_post[valor] = parametre
#        print self.canvis_post

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
                    ref = u' [REFEC%s] '
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
                    print valor
                    text = text.replace(valor, ref %(par), 1)
                    dicc_refs[ref %(par)] = valor
                par = int(par)
                par += 1
        print u'================================================================\n*'
        if dicc_refs != {}:
            print 40*"*"
            print 40*"*"
            print u"* DICCIONARI DE REFERÊNCIES *"
            for a in dicc_refs.keys():
                print 40*"*"
                print a , ":", dicc_refs[a]
            print 40*"*"
            print 40*"*"
        else:
            pass
#        raw_input()
        return text

class Interviqui:

    def cercaInterviquis(self,pagina,ca=True):
        print u"* CERCANT ELS ENLLAÇOS INTERVIQUI *"
        print 40 * '%'
        if " " in pagina.title():
            pagina = pagina.title().replace(" ","_")
            pagina = wikipedia.Page(self.idioma_original,pagina)
        if u'#' in pagina.title():
            pagina = wikipedia.Page(self.idioma_original,pagina.titleWithoutNamespace())
        try:
            print u"Primer intent"
            iws_pagina = pagina.interwiki()
            if iws_pagina == []:
                print u"no pot ser que no tingui enllaços"
                pagina = pagina.getRedirectTarget()
                iws_pagina = pagina.interwiki()

            print u"A la primera"
        except wikipedia.IsRedirectPage, arg:
            print u'És una redirecció'
            pagina = wikipedia.Page(self.idioma_original,arg[0])
            print pagina
            if u'#' in pagina.title():
                try: iws_pagina = wikipedia.Page(self.idioma_original,pagina.titleWithoutNamespace()).interwiki()
                except: pass
            else:
                iws_pagina = wikipedia.Page(self.idioma_original,arg[0]).interwiki()
        except:
            print u'Ja no sé què fer'
            print 40 * '%'
            return
        if iws_pagina == [] or iws_pagina == None:
            print u'Per ara no ha trobat enllaços'
            if self.titol_plantilles[self.idioma_original] in pagina.title():
                print u'És una plantilla'
                print pagina
                pagina_doc = wikipedia.Page(self.idioma_original,pagina.title()+self.us_plantilles[self.idioma_original])
                try:
                    text_pagina = pagina_doc.get()
                except wikipedia.IsRedirectPage, arg:
                    pagina_doc = wikipedia.Page(self.idioma,arg[0])
                    text_pagina = pagina_doc.get()
                except:
                    text_pagina = ''
                iws = re.search('\[\[ca:(.+)\]\]',text_pagina)
                if iws:
                    print u'No sé què fa aquí ?='
                    print 40 * '%'
                    return wikipedia.Page('ca',iws.group(1))
                else:
                    pass
            else:
                pass
        else:
            for iw in iws_pagina:
                if ca:
                    if iw.site().language() == 'ca':
                        print iw
                        print 40 * '%'
                        return iw
        try:
            iws_pagina = wikipedia.DataPage(pagina).interwiki()
        except wikipedia.IsRedirectPage, arg:
            iws_pagina = wikipedia.DataPage(self.idioma,arg[0]).interwiki()
        except:
            print u'Escaquejada'
            print 40 * '%'
            return
        '''
        except:
            print "Ha passat alguna cosa"
            print pagina.title()
            print sys.exc_info()[0]
            iws_pagina = self.interwikiLang2Lang(pagina)
            return
        '''
        for iw in iws_pagina:
            if ca:
                if iw.site().language() == 'ca':
                    print iw
                    print 40 * '%'
                    return iw
        print u"No s'ha trobat la pàgina en català"
        print 40 * '%'
        return

    def treuInterviquis(self,pagina,text,llista_iw=''):
        text = text
        if self.prova_interviqui == False: return text
        print "* NETEJANT INTERVIQUIS *"
        iws = pagina.interwiki()
        for iw in iws:
            iw = unicode(iw)
            text = text.replace(iw,'')
            llista_iw += iw+u"\n"
        llista_iw = llista_iw.split(u'\n')
        llista_iw.sort()
        self.llista_iw = u'\n'.join(llista_iw)
        print u"Interviquis trovades al text:\n"+self.llista_iw
        return text

    def interwikiLang2Lang(self,pagina):
        lang_origin=self.idioma_original
        lang_to='ca'
        urlData = 'http://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=sitelinks%2Furls&dir=ascending'
        variable = '&sites='+lang_origin+'wiki&titles='+pagina.title()
        dicc = urllib.urlopen(urlData+variable).read()
        site_origin = wikipedia.getSite(lang_origin,'wikipedia')
        site_to = wikipedia.getSite(lang_to,'wikipedia')
        item = json.JSONDecoder().raw_decode(dicc)[0]['entities'].keys()
        pagina = wikipedia.Page(site_origin,title)
        repo = pagina.data_repository()
        #iw = wikipedia.DataPage(repo,item[0]).interwiki()
        iw = [x for x in wikipedia.DataPage(repo,item[0]).interwiki() if x.site() == site_to]
        return iw[0]

class Text:

    def preTrad(self, pagina,text_final='',capi=0,refrep=0):
        llista_net = []
        capitol_trad = []
        llista_notrad = []
        text_final = u"{{Avís de traducció|plantilles}}\n{{Notes de traducció}}\n\n"
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
            return u"No he sabut trobar la pàgina demanada. Sembla que "\
            +self.titol_original+u" no existeix en la viqui demanada. --~~~~"
        text = self.treuInterviquis(pagina,text)
        text = self.treuCategories(pagina,text)
        text = re.sub(r'%s.+\}\}\n' %self.dicc_ordena[self.idioma_original],'',text)
        while u'\n\n\n' in text:
            text = text.replace(u'\n\n\n',u'\n\n')
        text = text.replace(u"==\n",u"==\n\n")
        text = text.replace(u"\n==",u"\n\n==")
        capitols = re.split(r'\n\n', text)
        if '' in capitols:
            capitols.remove('')
        for capitol in capitols:
            if capitol == '' or capitol == u'\n':
                print u'**************************\n* Aquest capítol és buit *\n**************************'
                continue
            if self.prova_gravar_viqui == False:
                self.pregunta('Seguim?',False)
            capitol_ori = capitol
            capi += 1
#            if capi != 1: # Opció de passar capítols quan
#                continue # es vol fer alguna prova sobre un capítol concret
            print u"********************\n********************\n* Capítol "+str(capi)+u"/"+str(len(capitols))+u" *\n********************\n********************"
            if capitol == '' or capitol == u'\n':
                print u'**************************\n* Aquest capítol és buit *\n**************************'
                continue
            print "&&&&&&&&&&&&&&&&&&&\n&& TEXT ORIGINAL &&\n&&&&&&&&&&&&&&&&&&&"
            print capitol
            print '&&&&&&&&&&&&&&&&&&&'
            cap = self.errorsPre(capitol)
            cap = re.sub(ur'\n\*', u'\n[*] ',cap) # La llista no numerada ha de contenir un espai entre l'asterisc i la frase...
            cap = re.sub(ur"'{3}", u"[''']", cap)
            cap = re.sub(u"(?<![\['])'{2}(?![\]'])", u"['']", cap)
            cap = re.sub(ur'\n#',u'\n[#] ', cap)
            cap = re.sub(ur'\$', u'[$]', cap)
            cap = re.sub(ur'(&\w+;)',ur'[\1]',cap)
            cap = cap.replace(u'<', u'[<')
            cap = cap.replace(u'>', u'>]')

            codi = re.findall(r'[\w]+=".+?"',cap)
            ncodi = 0
            for estil in codi:
                print '* CERCANT ESTILS DE TEXT *'
                ncodi = str(ncodi).zfill(4)
                valor = u' [REFZZ%s] ' %(ncodi)
                cap = cap.replace(estil, valor)
                print estil
                self.refs[valor] = estil
                ncodi = int(ncodi) + 1
            codi = re.findall(r'<[Mm]ath>.+?</[Mm]ath>',cap,flags=re.MULTILINE)
            ncodi = 0
            for mates in codi:
                print '* CERCANT CODI LaTex *'
                ncodi = str(ncodi).zfill(4)
                valor = u' [REFWM%s] ' %(ncodi)
                cap = cap.replace(mates, valor)
                print mates
                self.refs[valor] = mates
                ncodi = int(ncodi) + 1
            codi = re.findall(r'[^[](http://[\w./\~\+\-&=\?\d\#\%]+)',cap)
            ncodi = 0
            for webs in codi:
                print "* CERCANT URL's *"
                print webs
#                raw_input("No acaben d'estar be les webs")
                ncodi = str(ncodi).zfill(4)
                valor = u' [REFWY%s] ' %(ncodi)
                cap = cap.replace(webs, valor)
                self.refs[valor] = webs
                ncodi = int(ncodi) + 1
            if self.idioma_original == u'en' and cap.find(u'entur') != -1:
                cap = self.segles(cap)
            print "TEXT PRE_TRAD"
            print cap
            self.text_trad = self.cerca(cap)
#            print self.text_trad
            self.ordena_diccionari(self.refs)
            self.text_trad = self.text_trad.replace(u'{', u' [{] ' )
            self.text_trad = self.text_trad.replace(u'}', u' [}] ' )
            text_trad = self.traductor(self.text_trad)
            print u"* TEXT POST APERTIUM *"
            print self.text_trad
            text_trad = text_trad.replace(u'*REF',u'REF')
            text_trad = text_trad.replace(u'\n REF',u'\nREF')
#            print "TEXT POST_TRAD"
#            print text_trad
            no_trad = re.findall(r'\*\w+\s',text_trad)
            for paraula in no_trad:
                if paraula[1:].isupper:
                    pass
                else:
                    if paraula not in self.no_trad and paraula not in self.llista_marques:
                        self.no_trad.append(paraula)
            if u'REF' in text_trad:
                text = self.referText(text_trad)
            else:
                print u"* NO S'HAN TROBAT REF PER CANVIAR *"
                text = text_trad
            while u'REF' in text:
                refrep += 1
                text = text.replace(u'*', u' ')
                print '*** ENCARA HI HA REF PER CANVIAR ***'
                text = self.referText(text)
                if refrep > len(self.refs.keys()):
                    break
            text = text.replace(u'\n[*] ', u'\n*')
            text = text.replace(u'\n ', u'\n')
            text = text.replace(u'[ http:', u'[http:')
            text = text.replace(u'[$]', u'$')
            text = text.replace(u'[#]', u'\n#')
            text = text.replace(u"[#'#']", u"''")
            text = text.replace(u"[#'#'#']",u"'''")
            text = text.replace(u"['']", u"''")
            text = text.replace(u"[''']",u"'''")
            text = text.replace(u' ,', u',')
            text = text.replace(u' CLAUDATOROBERT ', u'{')
            text = text.replace(u' CLAUDATORTANCAT ', u'}')
            text = re.sub(ur'(\[&\w+;\])',ur'\1',text)
            text = text.replace(u'[ <',u'<')
            text = text.replace(u'> ]',u'>')
            text = text.replace(u'[<',u'<')
            text = text.replace(u'>]',u'>')
            text = text.replace(u'[{]',u'{')
            text = text.replace(u'[}]',u'}')

            text = text.lstrip()
            while u'  ' in text:
                text = text.replace(u'  ', u' ')
            text = self.postTrad(text)
            text_final += text + u'\n\n' + capitol_ori + u"\n\n"
            self.refs = {}
            self.dicc_enllac = {}
            print '**************\n*** ACABAT ***\n**************'
            print u'888888888888888888\n  88 Original 88  \n888888888888888888\n'+capitol_ori
            print u'8888888888888888888\n  88 Traducció 88  \n8888888888888888888\n'+text
            try:
                registre = open('registres/registre-%s.txt' %self.titol_original,'a')
                print u"Registre normal"
#                raw_input (u"Enter per seguir")
            except:
                registre = open('/registres/registre-001.txt', 'a')
                print u"Registre a 001"
#                raw_input (u"Enter per seguir")
            registre.write(text_final.encode('utf-8'))
            registre.close()
        while text_final.find(u'  ') != -1:
            text_final = text_final.replace(u'  ', u' ')
        categories = self.cercaCategories(pagina,text)
        text_final += self.cat_original+u"\n\n"+categories+u"\n\n"+self.llista_iw
        while text_final.find(u'\n\n\n') != -1:
            text_final = text_final.replace(u'\n\n\n',u'\n\n')
        text_final = text_final.replace(u'==\n\n',u'==\n')
        text_final = text_final+\
        u"\n\n==Notes de traducció==\n*Les plantilles en vermell són les \
que no s'han pogut trobar la corresponent plantilla en català. \
Això no vol dir que no existeixi, sino que no s'ha pogut trobar \
automàticament, ja sigui per que no hi ha el corresponent enllaç \
interviqui, o per que, realment, no existeix la plantilla en català. \
En cas que trobeu la plantilla corresponent us agrairia que li \
posesiu el seu enllaç interviqui a la plantilla en l'idioma original \
per poder trobar-la en properes traduccions. Gràcies. --~~~~\n\
*Podeu comentar possibles millores en el bot de traducció en \
[[Usuari:Anskarbot/Errors|aquesta pàgina]]. --~~~~\n\
*Les paraules que el programa [[Apertium]] encara no tradueix \
queden registrades automàticament. Si trobeu alguna millora en \
la traducció podeu expresar-ho a la mateixa \
[[Usuari:Anskarbot/Errors|pàgina d'errors]]. --~~~~"
        try:
            registre = open('registres/registre-%s.txt' %self.titol_original,'a')
            print u"Registre normal"
#            raw_input (u"Enter per seguir")
        except:
            registre = open('/registres/registre-001.txt', 'a')
            print u"Registre a 001"
#            raw_input (u"Enter per seguir")
        registre.write(text_final.encode('utf-8'))
        registre.close()
        return text_final

    def referText(self, text):
        """Canvia les referències de codi REF...... pel valor corresponent del diccionari self.refs"""
        print u'*** REFENT EL TEXT ***'
        marca = re.findall(r'\[REF\w+\d+\]', text)
        print text
        for ref in marca:
            print ref
            text = text.replace(ref, self.refs[u' '+ref+u' '])
        return text

    def postTrad(self,text):
        print "* GESTIONANT EL TEXT DESPRÉS DE LA TRADUCCIÓ *"
        enxel = re.findall(r'[eE]n (\d{1,4})',text)
        print enxel
        for data in enxel:
            text = text.replace(' en %s' %data, ' el %s' %data)
            text = text.replace(' En %s' %data, ' El %s' %data)
            text = text.replace('\nEn %s' %data, '\nEl %s' %data)
            text = text.replace('En %s' %data, 'El %s' %data)
        if self.canvis_post != {}:
            text = self.errorsPost(text)
        text = self.paginaRe(text,self.commons)
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
            text = re.sub(r'\[\['+categoria.title()+r'(.+)?\]\]' , u'',text,flags=re.DOTALL|re.UNICODE)
            categoria = u"\n[["+categoria.title()+u"]]"
            llista_cat += categoria
        llista_cat += u' -->'
        self.cat_original = llista_cat
        return text

    def cercaCategories(self,pagina,text,n=1,p=1,limit=3):
        cat_ca=''
        categories_ca=[]
        parents=[]
        categories_pare=[]
        text = text
        if self.prova_categories == False:
            self.cat_original = ''
            return text
        print "* CERCANT CATEGORIES *"
        wiki_ca = wikipedia.Site(u'ca')
        categories = pagina.categories()
        for categoria in categories:
            print str(n)+':'+str(limit)+'/'+str(p)+'-'+str(len(categories))
            y = self.cercaInterviquis(categoria)
            if y:
                if u"[[ca:"+y.title()+u']]\n' not in categories_ca:
                    if y.title() not in self.llista_parents:
                        if y.title().find(u' per ') == -1:
                            parents.append(y)
                            self.cercaCategoriesPare(parents)
                            categoria_print = u"** "+unicode(y)+u" **"
                            print 60*u"*"+u"\n*****     S'afegirà la següent categoria en català     *****\n*"+categoria_print.center(58)+u"*\n"+60*u"*"
                            categories_ca.append(u"[["+y.title()+u']]\n')
            supercategories = categoria.categories()
            if n <= limit:
                categories_pare.extend(supercategories)
            if p == len(categories):
                categories.extend(categories_pare)
                categories_pare = []
                if n == limit:
                    if categories_ca != []:
                        break
                    else:
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
#            plantilles = pagina.templatesWithParams()
            plana = mwparserfromhell.parse(pagina.get())
            plantilles = plana.filter_templates()
            for plant in plantilles:
                if u'etició de traducció' in plant.name:
                    if unicode(plant) == u'{{Petició de traducció|idioma|títol original|--~~~~ (signatura)|paràmetres opcionals}}':
                        continue
                    print plant
                    clau = unicode(pagina)+str(p).zfill(2)
                    print clau
                    print pagina
                    self.peticions[clau] = plant
                    p += 1
        if p > 1: peticions = u" peticions"
        else: peticions = u" petició"
        missatge =  u"*** S'ha trobat "+str(p)+ peticions+u" de traducció ***"
        print len(missatge)*u"*"+"\n"+missatge+u"\n"+len(missatge)*"*"

    def treuPeticio(self, pagina):
        if self.prova_gravar_viqui == False: return
        print u"* COMENÇA EL PROCÉS PER TREURE LA PLANTILLA JA PROCESSADA *"
        pagina_txt = re.findall(r'\[\[ca:(.+)\]\]',pagina)
        print pagina_txt
        print pagina
        text = wikipedia.Page('ca',unicode(pagina_txt[0])).get()
        plantilla = self.peticions[pagina]
        plantilla = plantilla.replace('\n','')
        print plantilla
#        print 'afsklfasdljkasldkfhasdklf'
#        text = text.replace(u'{{petició de traducció',u'{{Petició de traducció')
        text = text.replace(plantilla,'')
        wikipedia.Page('ca',unicode(pagina_txt[0])).put(text,u"Anskarbot traient la plantilla de traducció." ,minorEdit=False,force=True)

    def paginesClau(self,pagina,missatge=''):
        try:
            print self.peticions[pagina]
            parametres = self.peticions[pagina].params
            self.titol_escollit=False
            self.idioma_original = unicode(parametres[0])
            print 56*u"*"+u"\nIdioma de traducció: \n* "+self.idioma_original
            self.titol_original = unicode(parametres[1])
            if self.idioma_original not in self.dicc_ordena.keys():
                print u"Títol de la pàgina a traduir: \n* "+self.titol_original
            try:
                self.pagina_discussio_usuari = re.search(ur'Usuari Discussió:\w+[\s\w]+', unicode(parametres[2])).group()
            except:
                self.pagina_discussio_usuari = re.search(ur'Usuari_Discussió:\w+[\s\w]+', unicode(parametres[2])).group()
            self.usuari_peticio = re.findall(ur'Usuari:(\w+)', unicode(parametres[2]))[0]
            print u"Pàgina de discussió de l'usuari/a que demana la traducció: \n* "+self.pagina_discussio_usuari
            for n in range(len(parametres[1])):
                try:
                    parametres[n]
                    if u'títol=' in parametres[n]:
                        titol = unicode(parametres[n]).split('=')[1]
                        self.titol_escollit = titol.replace(titol[0],titol[0].upper())
                        missatge =  u"S'ha demanat aquest títol de pàgina provisional: \n* "
                    elif u'enllaços=' in parametres[n]:
                        self.tria_enllacos = True
                    elif u"regex=" in parametres[n]:
                        self.pagina_regex = unicode(parametres[n]).split(u'=')[1]
                        print u"S'ha demanat aquesta pàgina regex: \n* "+self.pagina_regex
                except: continue
            if self.titol_escollit:
                print missatge+self.titol_escollit
            else:
                print u"No s'ha demanat un títol específic"
            print u"S'ha demanat conservar els enllaços originals?: \n* "+str(self.tria_enllacos)+u"\n"+56*u"*"
            self.muntaPaginaRE(self.pagina_regex,u'ca')
            self.muntaPaginaRE(u'regex',self.idioma_original)
            if self.idioma_original not in self.idiomes_suportats:
                return 'ERROR'
        except:
            return "FATAL"
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

class Inici(Pregunta,Peticions,Text,Interviqui,PreCercaSubst,Diccionaris,Gestio,Categories,Apertium,Wiki,Maquillatge,Proves,Plantilles,Finestra):

    def main(self):
        print
        print u'///////////////////////////////'.center(80)
        print u'///*************************///'.center(80)
        print u'///* ARRENCA AMICAL-BOT II *///'.center(80)
        print u'///*        ANSCARBOT       ///'.center(80)
        print u'///*************************///'.center(80)
        print u'///////////////////////////////'.center(80)
        print
        self.variables()
        self.prova_gravar_viqui = self.pregunta(u'Gravem a la viqui?',False)
        if self.prova_gravar_viqui == False:
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
        print self.peticions
        for peticio in self.peticions.keys():
            print peticio
#            resposta = self.pregunta(u"Saltem aquesta peticio?",False)
#            if resposta == True:
#                continue
            self.netejaVariables()
            endavant = self.paginesClau(peticio)
            pagina_usuari = wikipedia.Page('ca',unicode(self.pagina_discussio_usuari))
            pagina_discusio = pagina_usuari.get()
            if endavant == 'ERROR':
                print "* DEIXANT L'AVÍS D'ERROR D'IDIOMA A LA PÀGINA DE L'USUARI *"
                missatge = u"[[Fitxer:Frog Bot - sad.gif]]\n* La vostra petició de traducció de l'article '''" + self.titol_original + u"''' no s'ha pogut dur a terme. Problemes amb el programa de traducció fa que de moment només es puguin fer traduccions de {{en}} i {{es}}. Perdoneu les molèsties. Gràcies."
                if missatge in pagina_discusio:
                    print u"Ja s'ha avisat a l'usuari de l'error en la plantilla"
                else:
                    pagina_discusio = pagina_discusio+u"\n== Problemes amb la traducció ==\n\n"+missatge+u" --~~~~\n"
                    pagina_usuari.put(pagina_discusio,u"Anscarbot deixant un missatge a la pàgina de discussió de l'usuari.",minorEdit=False, force=True)
                print u'*****************************************'
                print u'********** PETICIÓ CANCEL·LADA **********'
                print u'*****************************************'

                continue
            elif endavant == 'FATAL':
                print "* DEIXANT L'AVÍS D'ERROR D'IDIOMA A LA PÀGINA DE L'USUARI *"
                missatge = u"[[Fitxer:Frog Bot - sad.gif]]\n* La vostra petició de traducció de l'article '''" + self.titol_original + u"''' no s'ha pogut dur a terme. Repasseu que els paràmetres de la plantilla siguin correctes. Perdoneu les molèsties. Gràcies."
                if missatge in pagina_discusio:
                    print u"Ja s'ha avisat a l'usuari de l'error en la plantilla"
                else:
                    pagina_discusio = pagina_discusio+u"\n== Problemes amb la traducció ==\n\n"+missatge+u" --~~~~\n"
                    pagina_usuari.put(pagina_discusio,u"Anscarbot deixant un missatge a la pàgina de discussió de l'usuari.",minorEdit=False, force=True)
                print u'*****************************************'
                print u'********** PETICIÓ CANCEL·LADA **********'
                print u'*****************************************'

                continue
            else:
                self.muntaPlantillesProcessades()
                text = self.preTrad(peticio)
                if u"otes de traducc" not in text:
                    print text
                    print "* DEIXANT L'AVÍS D'ERROR DE PLANTILLA A LA PÀGINA DE L'USUARI *"
                    missatge = u"[[Fitxer:Frog Bot - sad.gif]]\n* La vostra petició de traducció de l'article '''" + self.titol_original + u"''' no s'ha pogut realitzar perque hi ha algun error en la configuració de la plantilla. Mireu que els paràmetres obligatoris estiguin ben posats <nowiki>{{Petició de traducció|idioma|títol original|--~~~~ (signatura)|paràmetres opcionals}}</nowiki>. Comproveu també que el títol correspon exactament a una pàgina existent a la viquipèdia de l'idioma de traducció (accents, majúscules, espais, caràcters no ASCII...). Gràcies."
                    if missatge in pagina_discusio:
                        print u"Ja s'ha avisat a l'usuari de l'error en la plantilla"
                    else:
                        pagina_discusio = pagina_discusio+u"\n== Problemes amb la traducció ==\n\n"+missatge+u" --~~~~\n"
                        pagina_usuari.put(pagina_discusio,u"Anscarbot deixant un missatge a la pàgina de discussió de l'usuari.",minorEdit=False, force=True)
                    print u'*****************************************'
                    print u'********** PETICIÓ CANCEL·LADA **********'
                    print u'*****************************************'

                    continue
            self.article(text,peticio)
            self.treuPeticio(peticio)
            print u'****************************************'
            print u'********** ACABADA LA PETICIÓ **********'
            print u'****************************************'
            if self.prova_gravar_viqui == False:
                self.pregunta(u'Seguim?',False)
        print u'\nOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
        print (u'OOOOO   ACABADES LES TRADUCCIONS   OOOOO').center(60)
        print u'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
        return 0

    def netejaVariables(self):
        self.llista_parents = []
        self.llista_iw = ''
        self.cat_original = []
        self.no_trad = []
        self.canvis_post = {u"Veu també":u'Vegeu també',
                            u'i.e.':u"per exemple",
                            u'NOTRADUIR002':u'Twentieth Century Fox',
                            u'NOTRADUIR001':u'The New York Times',
                            u" < ref":u"<ref",
                            u"< ref":u"<ref",
                            u" <ref ":u"<ref ",
                            u"( ":u"(",
                            u" )":u")",
                            u"{{Article de qualitat}}":u'',
                            u"{{Article bo}}":u'',
                            u"REFSOLA ":u"<references/>"}
        self.canvis_pre = {u"New York Times":u" NOTRADUIR001 ",
                           u"Twentieth Century Fox":u" NOTRADUIR002 ",
                           u"<references/>":u" REFSOLA "}


    def variables(self):
        # DICCIONARIS
        self.proves = False
        self.refs = {}
        self.peticions = {}
        self.dicc_plantilles = {}
        self.dicc_enllacos = {}
        self.dicc_altres = {}
        self.commons = {u'Image:' : u"Fitxer:",
                        u"Archivo:" : u"Fitxer:",
                        u"Imagen:" : u"Fitxer",
                        u"File:" : u"Fitxer:",
                        u"Arxiu:" : u"Fitxer:",
                        u"Fichier:" :u"Fitxer:",
                        u"Fichier:" :u"Fitxer:"}
        self.dicc_ordena = {u"en" : u"{{DEFAULTSORT:",
                            u"fr" : u"{{DEFAULTSORT:",
                            u"es" : u"{{DEFAULTSORT:",
                            u"pt" : u"{{DEFAULTSORT:",
                            u"oc" : u"{{DEFAULTSORT:",
                            u"it" : u"{{DEFAULTSORT:",}
        self.titol_plantilles = {u'en' : u'Template:',
                                 u'fr' : u'Modèle:',
                                 u'es' : u'Plantilla:',
                                 u'pt' : u'Predefinição:',
                                 u'oc' : u'Modèl:',
                                 u'it' : u'Template:'}
        self.us_plantilles = {u'en' : u"/doc",
                              u"fr" : u"/Documentation",
                              u"es" : u"/doc",
                              u"pt" : u"/doc",
                              u"oc" : u"/Documentacion",
                              u"it" : u"/man"}
        self.dicc_categories = {u"en" : u"Category:",
                                u"fr" : u"Catégorie",
                                u"es" : u"Categoría",
                                u"pt" : u"Categoria",
                                u"oc" : u"Categoria",
                                u"it" : u"Categoria"}
        # ALTRES VARIABLES
        self.cops_k_passa = 1
        self.tria_enllacos = False
        self.pagina_regex = ''
        self.plantilles_wiki = {}
        self.missatge_plantilla = u"Aquí es van afegint les traduccions dels paràmetres de les plantilles. Cada idioma de traducció té una plana diferent. En principi s'afegeixen automàticament quan el bot troba una plantilla en l'idioma original que existeix en català i no la troba en aquesta pàgina. Si voleu afegir alguna traducció de plantilla ho podeu fer seguint les següents recomanacions.\n\nEs pot editar la pàgina de la següent manera:\n\
*S'ha de posar com a títol de secció el nom de la plantilla en català sense redireccions. És a dir: Si la plantilla {{tl|FR}} redirigeix a {{tl|Falten referències}} el títol de secció ha ser '''<nowiki>==Falten referències==</nowiki>''' i no <s>'''<nowiki> ==FR== </nowiki>'''</s>\
*Els paràmetres es posaran de la mateixa manera que la resta d'expressions regulars:\
**paraula/frase mal escrita(o bé paraula/frase en l'idioma original);paraula/frase ben escrita\
*Noteu que en aquest cas les paraules a escriure han de ser les mateixes que indiquen els paràmetres de la plantilla, si el paràmetre és '''enllaçautor''' no podem escriure <s> '''enllaç autor''' </s>.\
<!-- Si us plau, no varieu aquesta introducció, ha de ser igual per totes les pàgines per construir els diccionaris de plantilles -->"

        # LLISTES
        self.idiomes_suportats = ('es', 'en', 'fr', 'pt', 'oc', 'it')
        self.cerques =[(u'<!--',u'-->', u' [REFCO%s] '), # Llista de tuples que ...
                       (u'[http:',u']', u' [REFEW%s] '),    # ... estableix el caràcter de cerca ...
                       (u'[[',u']]', u' [REFEA%s] '),       # ... i el relaciona amb la referència que substituirà.
                       (u'{{',u'}}', u' [REFPL%s] '),            # La tupla consta de tres paràmetres:
                       (u"[<gallery", u"</gallery>]", u" [REFGC%s] "),
                       (u'[<ref>' , u'</ref>]', u' [REFRE%s] '),   # 1: El primer terme de cerca, (p.e. {{ com a primer terme)
                       (u'[<ref', u'</ref>]', u' [REFRH%s] '),     # 2: El darrer terme de cerca, (ha de trobar }} com a darrer terme)
                       (u'[<ref name' , u'/>]' , u' [REFSR%s] '),  # 3: La referència que substitueix el codi trobat
#                       (u'<nowiki>' , u'</nowiki>' , u' REFSA%s '),    # És important que la marca REFxx segueixi un ordre alfabètic
#                       (u'<div' , u'</div>' , u' REFSA%s '),           # per gestionar el diccionari de referències en l'ordre correcte
                       (u'<' , u'>' , u' [REFWC%s] '),                   # de forma qualsevol codi inserit dins un altre codi es gestioni primer el que es troba dins un altre,
                       (u'{|',u'|}', u' [REFZT%s] ')]                   # per això el comentari <!-- --> és el primer en gestionar-se i les taules {| }| l'últim de tots.
        self.marques = [u' ASTR ',u' SIMBOLDOLLAR ',u' SOSTINGUT ',u" CURSIVA ", u" NEGRETA ",u' CLAUDATOROBERT ',u' CLAUDATORTANCAT ',u' UNIÓMOTS ']

if __name__ == '__main__':
    try:
        app = Inici()
        app.main()
    finally:
        wikipedia.stopme()

</source>
r escollir més d'un. En cas de que fos cap no té sentit demanar proves.
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
                durant = self.paginaRe(zero1,dicc_temporal)
                text_trad = durant+' segle '+self.romans(segon)+crist
            elif primer != '' and segon != '':
                durant = self.paginaRe(zero0,dicc_temporal)
                text_trad = durant+' segles '+self.romans(primer)+u'-'+self.romans(segon)+crist
            text = text.replace(segles.group(), text_trad,1)
        return text

    def errorsPre(self,text):
        text = text
        if self.prova_maquillatge == False: return text
        print "* PROCESSANT ELS ERRORS CONEGUTS ABANS DE LA TRADUCCIÓ *"
        if self.idioma_original == 'en': text = self.segles(text)
        text = self.paginaRe(text,self.canvis_pre)
        return text

    def paginaRe(self, text, dicc):
        """Reemplazo múltiple de cadenas en Python."""
        regex = re.compile("(%s)" % "|".join(map(re.escape, dicc.keys())))
        text = regex.sub(lambda x: unicode(dicc[x.string[x.start() :x.end()]]), text)
        return text

    def errorsPost(self,text):
        print "* PROCESSANT ELS ERRORS CONEGUTS DESPRÉS DE LA TRADUCCIÓ *"
        text = self.paginaRe(text,self.canvis_post)
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
        if self.titol_escollit:
            if u'/' in self.titol_escollit:
                pagina = self.titol_escollit
            else:
                pagina = u'Usuari:Anskarbot/Traduccions/'+self.titol_escollit
        else:
            pagina = u'Usuari:Anskarbot/Traduccions/'+self.titol_original
        enllac_pagina = u"[["+pagina+u"|aquesta pàgina de proves]]"
        pagina_final = wikipedia.Page('ca',pagina)
        pagina_final.put(text,u"Anskarbot editant un article traduït",minorEdit=False,force=True)

        print "* DEIXANT L'AVÍS A LA PÀGINA DE L'USUARI *"
        missatge = u"\n== Petició de traducció ==\n*La vostra petició de traducció de l'article '''" + self.titol_original + u"''' es troba en " + enllac_pagina + u".Fixeu-vos bé '''que no és la mateixa pàgina on havíeu posat la petició de traducció'''. Quan repasseu la traducció podeu fer suggeriments de millora a [[Usuari:Anskarbot/Errors|la pàgina de millores del bot]] per anar polint la traducció. Gràcies."+falta+u" --~~~~\n"
        pagina_usuari = wikipedia.Page('ca',unicode(self.pagina_discussio_usuari))
        p = re.compile(u'\n== Petició de traducció ==\n')
        pagina_discusio = pagina_usuari.get()
        if p.search(pagina_discusio):
            pagina_discusio = p.sub(missatge,pagina_discusio,1)
        else:
            pagina_discusio = pagina_discusio+missatge
        pagina_usuari.put(pagina_discusio,u"Anscarbot deixant un missatge a la pàgina de discussió de l'usuari.",minorEdit=False, force=True)

        print "* POSANT LA PLANTILLA {{Traduït de}} A LA PÀGINA DE DISCUSSIÓ DE L'ARTICLE TRADUÏT *"
        pagina_traduitde = u"Usuari Discussió:Anskarbot/Traduccions/"+self.titol_original
        urlversio =wikipedia.Page(self.idioma_original,self.titol_original).permalink()
        versio = re.findall(r'oldid=(\d+)',urlversio)
        pagina_traduitde = wikipedia.Page('ca', pagina_traduitde)
        pagina_traduitde.put(u'{{Traduït de|'+self.idioma_original+u'|'+self.titol_original+u'|{{subst:CURRENTDAY}}-{{subst:CURRENTMONTH}}-{{subst:CURRENTYEAR}}|'+versio[0]+u'}}\n --~~~~', u'Anskarbot incorporant la plantilla {{traduït de}} a la pàgina de discussió',minorEdit=False, force=True)

        print u"* AFEGINT LA TRADUCCIÓ A L'ÍNDEX DE TRADUCCIONS *"
        index = u'Usuari:Anskarbot/Traduccions'
        index = wikipedia.Page(u'ca',index)
        contingut_index = index.get()
        contingut_index = contingut_index.replace(u"|}",u'|-\n|* [['+pagina+']]||{{u|'+self.usuari_peticio+u'}}||{{subst:CURRENTDAY}}/{{subst:CURRENTMONTH}}/{{subst:CURRENTYEAR}}||{{subst:PAGESIZE:'+pagina+'|R}}||{{PAGESIZE:'+pagina+'|R}}\n|}')
        index.put(contingut_index, u"Anskarbot afegint la traducció a l'índex de les traduccions fetes", minorEdit=False, force=True)

        print u"* AFEGINT LES PARAULES NO TRADUIDES *"
        pagina_dicc = u"Usuari:Anskarbot/"+self.idioma_original
        pagina = wikipedia.Page('ca',pagina_dicc)
        text = pagina.get()
        for x in self.no_trad:
            text += u"*"+x+u"\n"
        pagina.put(text,u"Anskarbot afegint les paraules no traduïdes")

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
        print u'** GESTIONANT PLANTILLA **'
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
                nom = nom.strip()
                nom_trad = self.traductor(nom).replace('*','').strip()+' = '

                valor_trad = self.traductor(valor).replace('*','')
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
                    llista_parametres.append(nom.strip()+U' = '+valor)
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
        plantilla_txt = u"{{"+plantilla[0]
        print plantilla
        for parametre in plantilla[1]:
            parametre = parametre.replace('\n','')
            plantilla_txt += u"\n|"+parametre
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
        text_a_trad = re.search(r'[|]([^|]+)\]\]',enllac, re.UNICODE)
        if text_a_trad:
            text_traduit = self.traductor(text_a_trad.group(1))
            text_traduit = text_traduit.replace('*', '')
            enllac = enllac.replace(text_a_trad.group(1),text_traduit)
        return enllac

    def gestiona_enllac(self, enllac):
        """Gestiona els enllaços de text"""
        enllac = enllac
        if self.prova_enllacos == False: return enllac
        print u'** PROCESSANT UN ENLLAÇ DE TEXT **'
        print enllac
        if u':' in enllac:
            print 'És un enllaç especial, el mantindrem'
            return enllac
        enllac = enllac[2:-2]
        if u'|' in enllac:
            marca = enllac.split(u'|')
            enllac_ori = marca[0]
            text = marca[1]
            text_trad = self.traductor(text).strip()
        else:
            text = enllac
            enllac_ori = enllac
            text_trad = self.traductor(enllac).strip()
        if enllac_ori.startswith(u'#'): return text_trad
        iws = wikipedia.Page(self.idioma_original,enllac_ori)
        pagina_ca = self.cercaInterviquis(iws)
        if text.islower():
            text_trad = text_trad.lower()
        elif text.isupper():
            text_trad = text_trad.upper()
        elif text.istitle():
            text_trad = text_trad.title()
        if pagina_ca:
            if text_trad.lower() == pagina_ca.titleWithoutNamespace().lower():
                enllac_final = u'[['+text_trad+u']]'
            else:
                enllac_final = u'[['+pagina_ca.title()+u'|'+text_trad+u']]'
        else:
            if self.tria_enllacos == True:
                enllac_final = u'[[:'+self.idioma_original+u':'+enllac_ori+u'|'+text_trad+u']]'
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
        taula = taula.replace(u'|', u' BARRUERAMENT ')
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
        taula = taula.replace(u' BARRUERAMENT ' , u'|')
        taula = taula.replace(u' ADMIRACIO ' , u'!')
        return taula

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
            elif valor.startswith(self.cerques[1][-1][:-3]): # Enllaços web
                print u'* PROCESSANT ENLLAÇ WEB *'
                inici = nou_text.find(u' ')
                nou_text = nou_text.replace(nou_text[inici:-1], self.traductor(nou_text[inici:-1]))
                dicc[valor] = nou_text
            elif valor.startswith(self.cerques[2][-1][:-3]): # Enllaços de text
                nou_enllac = self.gestiona_enllac(nou_text)
                print nou_enllac
                dicc[valor] = nou_enllac
            elif valor.startswith(self.cerques[3][-1][:-3]): # Plantilles
                nou_text = self.gestionaPlantilles(nou_text)
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
            elif valor.startswith(self.cerques[8][-1][:-3]): # Taules
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
            elif valor.startswith(u' REFRR'): #Caràcters estranys
                print u'* PROCESSANT CARÂCTERS ESTRANYS *'
            elif valor.startswith(u' REFGC'): #Codi entre <gallery></gallery>
                print u'* PROCESSANT FITXERS DE COMMONS DINS <gallery> *'
                print nou_text
                llista = nou_text.split('\n')
                text_final = u'<gallery>\n'
                for llista_text in llista:
                    if '|' in llista_text:
                        inicic = llista_text.find('|',finalc)
                        finalc = llista_text.find('\n', inicic)
                        text_peu = self.traductor(llista_text[inicic+1:finalc])
                        text_final += llista_text.replace(llista_text[inicic+1:finalc],text_peu)
                text_final += u'</gallery>'
                dicc[valor] = text_final
            elif valor.startswith(u' REFEC'): # Enllaços de commons
                nou_text = self.gestiona_commons(dicc[valor])
                dicc[valor] = nou_text

    def muntaPaginaRE(self, re_en_pagina, idioma):
        pagina = u"Usuari:Anskarbot/"+idioma+u"/"+re_en_pagina
        titol = wikipedia.Page(u'ca',pagina)
        try: text = titol.get()
        except:
            print 'No hi ha pàgina regex a la wiki'
            return
        text = re.sub(r'<!--.+-->','',text)
        llista = text.split(u'\n')
        print llista
        if '' in llista: llista.remove('')
        for x in llista:
            if ';' not in x: continue
            diccionari = x.split(u';')
            print diccionari
            valor,parametre = diccionari[0],diccionari[1]
            self.canvis_post[valor] = parametre
        print self.canvis_post
        self.pregunta('Com?',False)

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
                    print valor
                    text = text.replace(valor, ref %(par), 1)
                    dicc_refs[ref %(par)] = valor
                par = int(par)
                par += 1
        print u'================================================================\n*'
        return text

class Interviqui:

    def cercaInterviquis(self,pagina,ca=True):
        print u"* CERCANT ELS ENLLAÇOS INTERVIQUI *"
        if u'#' in pagina.title():
            pagina = wikipedia.Page(self.idioma_original,pagina.titleWithoutNamespace())
        try:
            iws_pagina = pagina.interwiki()
            print 'Aquesta pagina esta a wikipedia'
        except wikipedia.IsRedirectPage, arg:
            pagina = pagina.getRedirectTarget()
            print pagina, arg[0]
            print type(arg[0])
            iws_pagina = wikipedia.Page(self.idioma_original,arg[0]).interwiki()
            print 'Es una redirecció'
        except:
            print 'Aquesta pàgina no existeix a wikipedia?'
            return
        if iws_pagina == [] or iws_pagina == None:
            print 'Pero sembla que no te els enllacos al text'
            if self.titol_plantilles[self.idioma_original] in pagina.title():
                pagina_doc = wikipedia.Page(self.idioma_original,pagina.title()+self.us_plantilles[self.idioma_original])
                print 'Busquem a la subpagina "/doc"'
                try:
                    text_pagina = pagina_doc.get()
                except wikipedia.IsRedirectPage, arg:
                    print 'Es una redirecció'
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
                print 'No és una plantilla :)'
        else:
            for iw in iws_pagina:
                if ca:
                    if iw.site().language() == 'ca':
                        print u"S'ha trobat la pàgina en català"
                        return iw
        print u"No s'ha trobat l'interviqui ca: a la viqui, buscarem a wikidata"
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
                    print u"S'ha trobat la pàgina en català"
                    return iw
            else:
                return iws_pagina
        print u"No s'ha trobat la pàgina en català"
        return

    def treuInterviquis(self,pagina,text,llista_iw=''):
        text = text
        if self.prova_interviqui == False: return text
        print "* NETEJANT INTERVIQUIS *"
        iws = pagina.interwiki()
        for iw in iws:
            iw = unicode(iw)
            text = text.replace(iw,'')
            llista_iw += iw+u"\n"
        llista_iw = llista_iw.split(u'\n')
        llista_iw.sort()
        self.llista_iw = u'\n'.join(llista_iw)
        print u"Interviquis trovades al text:\n"+self.llista_iw
        return text

class Text:

    def preTrad(self, pagina,text_final='',cap=0,refrep=0):
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
            return u"No he sabut trobar la pàgina demanada. Sembla que "+self.titol_original+u" no existeix en la viqui demanada. --~~~~"
        text = self.treuInterviquis(pagina,text)
        text = self.treuCategories(pagina,text)
        text = re.sub(r'%s.+\}\}\n' %self.dicc_ordena[self.idioma_original],'',text)
        text = self.errorsPre(text)
        while u'\n\n\n' in text:
            text = text.replace(u'\n\n\n',u'\n\n')
        text = text.replace(u"==\n",u"==\n\n")
        text = text.replace(u"\n==",u"\n\n==")
        capitols = re.split(r'\n\n', text)
        if '' in capitols:
            capitols.remove('')
        for capitol in capitols:
            if capitol == '' and capitol == u'\n':
                print u'**************************\n* Aquest capítol és buit *\n**************************'
                continue
            capitol_ori = capitol
            cap += 1
#            if cap < 12: # Opció de passar capítols quan
#                continue # es vol fer alguna prova sobre un capítol concret ;)
            print u"********************\n********************\n* Capítol "+str(cap)+u"/"+str(len(capitols))+u" *\n********************\n********************"
            print "&&&&&&&&&&&&&&&&&&&\n&& TEXT ORIGINAL &&\n&&&&&&&&&&&&&&&&&&&"
            print capitol
            capitol = capitol.replace(u'\n*', u'\n* ') # La llista no numerada ha de contenir un espai entre l'asterisc i la frase...
            capitol = capitol.replace('*', ' ASTR ')
            capitol = re.sub(r"'''", " NEGRETA ", capitol)
            capitol = re.sub(r"''", " CURSIVA ", capitol)
            capitol = re.sub(r'\n#',' SOSTINGUT ', capitol)
            capitol = re.sub(r'[$]', ' SIMBOLDOLLAR ', capitol)
            capitol = capitol.replace(u'&ndash;',u'–')
            capitol = capitol.replace(u'&mdash;', u'—')
            capitol = capitol.replace(u'&nbsp;', u' UNIÓMOTS ')
            codi = re.findall(r'[\w]+=".+?"',capitol)
            ncodi = 0
            for estil in codi:
                print '* CERCANT ESTILS DE TEXT *'
                ncodi = str(ncodi).zfill(4)
                valor = u' REFZZ%s ' %(ncodi)
                capitol = capitol.replace(estil, valor)
                self.refs[valor] = estil
                ncodi = int(ncodi) + 1
            codi = re.findall(r'<[Mm]ath>.+?</[Mm]ath>',capitol,flags=re.MULTILINE)
            ncodi = 0
            for mates in codi:
                print '* CERCANT CODI LaTex *'
                ncodi = str(ncodi).zfill(4)
                valor = u' REFWM%s ' %(ncodi)
                capitol = capitol.replace(mates, valor)
                print mates
                self.refs[valor] = mates
                ncodi = int(ncodi) + 1
            codi = re.findall(r'[^[](http://[\w./\~\+\-&=\?\d\#]+)',capitol)
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
            codi = re.findall(r'<[Cc]ode>.+?</[Cc]ode>',capitol,flags=re.MULTILINE)
            ncodi = 0
            for m_code in codi:
                print '* CERCANT CODI *'
                ncodi = str(ncodi).zfill(4)
                valor = u' REFWZ%s ' %(ncodi)
                capitol = capitol.replace(m_code, valor)
                self.refs[valor] = m_code
                ncodi = int(ncodi) + 1
            fitxers = re.findall(r'<gallery>.+</gallery>', capitol,flags=re.DOTALL)
            ncodi = 0
            for m_code in fitxers:
                print '* CERCANT FITXERS DE COMMONS DINS <gallery> *'
                ncodi = str(ncodi).zfill(4)
                valor = u' REFGC%s ' %(ncodi)
                capitol = capitol.replace(m_code, valor)
                self.refs[valor] = m_code
                ncodi = int(ncodi) + 1
            if self.idioma_original == u'en' and capitol.find(u'entur') != -1:
                capitol = self.segles(capitol)
            self.text_trad = self.cerca(capitol)
            rareses = re.findall(ur'(\w*[ĆćĹĺŃńŔŕŚśÝýŹźÌìÂâĈĉÊêĜĝĤĥÎîĴĵÔôŜŝÛûŴŵŶŷÄäËëÖöŸÿÃãẼẽĨĩÕõŨũỸỹÇçĢģĶķĻļŅņŖŗŞşŢţĐđǤǥĦħƟɵŦŧÅåŮůǍǎČčĎďĚěǏǐǨǩĽľŇňǑǒŘřŠšŤťǓǔŽžǮǯĀāĒēĪīŌōŪūȲȳǢǣǖǘǚǜĂăĔĕĞğĬĭŎŏŬŭĊċḂḃĊċḊḋĖėḞḟĠġİṖṗṠṡṪṫŻżĄąĘęĮįǪǫŲųḌḍẸẹḤḥỊịḶḷḸḹṂṃṆṇṚṛṜṝṢṣṬṭỤụŁłØøŐőŰűƁɓƊɗƘƙĿŀÐðÞþǷƿȜȝƎƏəƐɛıȢŊŋƩʃƷʒƒſÆæĲĳǶƕŒœß]\w*),?.?', self.text_trad,flags=re.UNICODE)
            ncodi = 0
            for m_code in rareses:
                print '* CERCANT CARÂCTERS ESTRANYS *'
                ncodi = str(ncodi).zfill(4)
                valor = u' REFRR%s ' %(ncodi)
                self.text_trad = self.text_trad.replace(m_code, valor)
                self.refs[valor] = m_code
                ncodi = int(ncodi) + 1
                print m_code
            self.ordena_diccionari(self.refs)
            self.text_trad = self.text_trad.replace(u'{', u' CLAUDATOROBERT ' )
            self.text_trad = self.text_trad.replace(u'}', u' CLAUDATORTANCAT ' )
            text_trad = self.traductor(self.text_trad)
            text_trad = text_trad.replace(u'*REF',u'REF')
            text_trad = text_trad.replace(u'\n REF',u'\nREF')
            no_trad = re.findall(r'\*\w+\s',text_trad)
            for paraula in no_trad:
                if paraula[1:].isupper:
                    pass
                else:
                    if paraula not in self.no_trad and paraula not in self.llista_marques:
                        self.no_trad.append(paraula)
            if u'REF' in text_trad:
                text = self.referText(text_trad)
            else:
                print u"* NO S'HAN TROBAT REF PER CANVIAR *"
                text = text_trad
            while u'REF' in text:
                refrep += 1
                text = text.replace(u'*', u' ')
                print '*** ENCARA HI HA REF PER CANVIAR ***'
                text = self.referText(text)
                if refrep > len(self.refs.keys()):
                    break
            print '**************\n*** ACABAT ***\n**************'
            text = text.replace(u'*', u'')
            text = text.replace(u' ASTR ', u'*')
            text = text.replace(u'\n *', u'\n*')
            text = text.replace(u'\n* *',u'\n**')
            text = text.replace(u'[ http:', u'[http:')
            text = text.replace(u' SIMBOLDOLLAR ', u'$')
            text = text.replace(u' SOSTINGUT ', u'\n#')
            text = text.replace(u" CURSIVA ", u"''")
            text = text.replace(u" NEGRETA ",u"'''")
            text = text.replace(u' ,', u',')
            text = text.replace(u' CLAUDATOROBERT ', u'{')
            text = text.replace(u' CLAUDATORTANCAT ', u'}')
            text = text.replace(u' UNIÓMOTS ', u'&nbsp;')
            text = text.lstrip()
            while text.find(u'  ') != -1:
                text = text.replace(u'  ', u' ')
            text = self.postTrad(text)
            text_final += text + u'\n\n' + capitol_ori + u"\n\n"
            self.refs = {}
            self.dicc_enllac = {}
            print u'888888888888888888\n  88 Original 88  \n888888888888888888\n'+capitol_ori
            print u'8888888888888888888\n  88 Traducció 88  \n8888888888888888888\n'+text
        while text_final.find(u'  ') != -1:
            text_final = text_final.replace(u'  ', u' ')
        categories = self.cercaCategories(pagina,text)
        text_final += self.cat_original+u"\n\n"+categories+u"\n\n"+self.llista_iw
        while text_final.find(u'\n\n\n') != -1:
            text_final = text_final.replace(u'\n\n\n',u'\n\n')
        text_final = text_final.replace(u'==\n\n',u'==\n')
        text_final = text_final+u"\n\n==Notes de traducció==\n*Les plantilles en vermell són les que no s'han pogut trobar la corresponent plantilla en català. Això no vol dir que no existeixi, sino que no s'ha pogut trobar automàticament, ja sigui per que no hi ha el corresponent enllaç interviqui, o per que, realment, no existeix la plantilla en català. En cas que trobeu la plantilla corresponent us agrairia que li posesiu el seu enllaç interviqui a la plantilla en l'idioma original per poder trobar-la en properes traduccions. Gràcies. --~~~~\n*He optat per posar totes els possibles paràmetres que admet la plantilla en català perque és complicat encertar els paràmetres coincidents en una traducció literal. Intenteré que almenys les plantills de referènciess quedin perfectament traduïdes i amb la resta anirem poc a poc. --~~~~\n*És possible que quan estigui implementat Wikidata sigui més fàcil saber la coincidència de paràmtres originals i en català, però per ara és força complicat. --~~~~\n*Podeu comentar possibles millores en el bot de traducció en [[Usuari:Anskarbot/Errors|aquesta pàgina]]. --~~~~\n*Les paraules que el programa [[Apertium]] encara no tradueix queden registrades automàticament. Si trobeu alguna millora en la traducció podeu expresar-ho a la mateixa [[Usuari:Anskarbot/Errors|pàgina d'errors]]. --~~~~"
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
            text = text.replace(ref, self.refs[u' '+ref])
        return text

    def postTrad(self,text):
        print "* GESTIONANT EL TEXT DESPRÉS DE LA TRADUCCIÓ *"
        enxel = re.findall(r'[eE]n (\d{1,4})',text)
        print enxel
        for data in enxel:
            text = text.replace(' en %s' %data, ' el %s' %data)
            text = text.replace(' En %s' %data, ' El %s' %data)
            text = text.replace('\nEn %s' %data, '\nEl %s' %data)
        if self.canvis_post != {}:
            text = self.errorsPost(text)
        text = self.paginaRe(text,self.commons)
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
            text = re.sub(r'\[\['+categoria.title()+r'(.+)?\]\]' , u'',text,flags=re.DOTALL|re.UNICODE)
            categoria = u"\n[["+categoria.title()+u"]]"
            llista_cat += categoria
        llista_cat += u' -->'
        self.cat_original = llista_cat
        return text

    def cercaCategories(self,pagina,text,n=1,p=1,limit=3):
        cat_ca=''
        categories_ca=[]
        parents=[]
        categories_pare=[]
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
        print u"*** S'ha trobat "+str(p)+ peticions+u" de traducció ***"

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

    def paginesClau(self,pagina,missatge=''):
        self.titol_escollit=False
        self.idioma_original = self.peticions[pagina][1][0]
        print 56*u"*"+u"\nIdioma de traducció: \n* "+self.idioma_original
        self.titol_original = self.peticions[pagina][1][1]
        print u"Títol de la pàgina a traduir: \n* "+self.titol_original
#        print self.peticions[pagina][1][2]
        self.pagina_discussio_usuari = re.search(ur'Usuari Discussió:\w+ ?(\w+)?', self.peticions[pagina][1][2]).group()
        self.usuari_peticio = re.findall(ur'Usuari:(\w+)', self.peticions[pagina][1][2])[0]
        print u"Pàgina de discussió de l'usuari/a que demana la traducció: \n* "+self.pagina_discussio_usuari
        for n in range(len(self.peticions[pagina][1])):
            try:
                self.peticions[pagina][1][n]
                if u'títol=' in self.peticions[pagina][1][n]:
                    titol = self.peticions[pagina][1][n].split('=')[1]
                    self.titol_escollit = titol.replace(titol[0],titol[0].upper())
                    missatge =  u"S'ha demanat aquest títol de pàgina provisional: \n* "
                elif u'enllaços=' in self.peticions[pagina][1][n]:
                    self.tria_enllacos = True
                elif u"regex=" in self.peticions[pagina][1][n]:
                    self.pagina_regex = self.peticions[pagina][1][n].split(u'=')[1]
                    print u"S'ha demanat aquesta pàgina regex: \n* "+self.pagina_regex
            except: continue
        if self.titol_escollit:
            print missatge+self.titol_escollit
        else:
            print u"No s'ha demanat un títol específic"
        print u"S'ha demanat conservar els enllaços originals?: \n* "+str(self.tria_enllacos)+u"\n"+56*u"*"
        self.muntaPaginaRE(self.pagina_regex,u'ca')
        self.muntaPaginaRE(u'regex',self.idioma_original)

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

class Inici(Pregunta,Peticions,Text,Interviqui,PreCercaSubst,Diccionaris,Gestio,Categories,Apertium,Wiki,Maquillatge,Proves,Plantilles):

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
            if u"otes de traducc" not in text:
                print text
                continue
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
        self.no_trad = []
        self.canvis_post = {u"Veu també":u'Vegeu també',
                            u'i.e.':u"per exemple",
                            u'NOTRADUIR002':u'Twentieth Century Fox',
                            u'NOTRADUIR001':u'New York Times',
                            u" < ref":u"<ref",
                            u"< ref":u"<ref",
                            u" <ref ":u"<ref ",
                            u"( ":u"(",
                            u" )":u")",
                            u"{{Article de qualitat}}":u'',
                            u"{{Article bo}}":u''}
        self.canvis_pre = {u"New York Times":u" NOTRADUIR001 ",
                           u"Twentieth Century Fox":u" NOTRADUIR002 "}



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
                        u"Arxiu:" : u"Fitxer:",
                        u"Fichier:" :u"Fitxer:"}
        self.dicc_ordena = {u"en" : u"{{DEFAULTSORT:",
                            u"fr" : u"{{DEFAULTSORT:",
                            u"es" : u"{{DEFAULTSORT:",
                            u"pt" : u"{{DEFAULTSORT:",
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
        # ALTRES VARIABLES
        self.cops_k_passa = 1
        self.tria_enllacos = False
        self.pagina_regex = ''

        # LLISTES
        self.cerques =[(u'<!--',u'-->', u' REFCO%s '), # Llista de tuples que ...
                       (u'[http:',u']', u' REFEW%s '),    # ... estableix el caràcter de cerca ...
                       (u'[[',u']]', u' REFEA%s '),       # ... i el relaciona amb la referència que substituirà.
                       (u'{{',u'}}', u' REFPL%s '),            # La tupla consta de tres paràmetres:
                       (u'<ref>' , u'</ref>', u' REFRE%s '),   # 1: El primer terme de cerca, (p.e. {{ com a primer terme)
                       (u'<ref', u'</ref>', u' REFRI%s '),     # 2: El darrer terme de cerca, (ha de trobar }} com a darrer terme)
                       (u'<ref name' , u'/>' , u' REFSR%s '),  # 3: La referència que substitueix el codi trobat
#                       (u'<nowiki>' , u'</nowiki>' , u' REFSA%s '),    # És important que la marca REFxx segueixi un ordre alfabètic
#                       (u'<div' , u'</div>' , u' REFSA%s '),           # per gestionar el diccionari de referències en l'ordre correcte
                       (u'<' , u'>' , u' REFWC%s '),                   # de forma qualsevol codi inserit dins un altre codi es gestioni primer el que es troba dins un altre,
                       (u'{|',u'|}', u' REFZT%s ')]                   # per això el comentari <!-- --> és el primer en gestionar-se i les taules {| }| l'últim de tots.
        self.marques = [u' ASTR ',u' SIMBOLDOLLAR ',u' SOSTINGUT ',u" CURSIVA ", u" NEGRETA ",u' CLAUDATOROBERT ',u' CLAUDATORTANCAT ',u' UNIÓMOTS ']

if __name__ == '__main__':
    try:
        app = Inici()
        app.main()
    finally:
        wikipedia.stopme()
