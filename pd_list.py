#!/usr/bin/env python3
"""
Copyright (C) 2021 alchimista alchimistawp@gmail.com
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pywikibot
from datetime import date
from pywikibot import pagegenerators as pg

# pd_year = date.today().year - 70
pd_year_today = 2025
pd_year = pd_year_today - 71
pd_year_1 = (pd_year + 1)
print(pd_year)
QUERY = ('''SELECT DISTINCT ?item (year(?birthdate) as ?birthyear) ?deathdate WHERE {
  ?item wdt:P31 wd:Q5.
  ?item wdt:P27 wd:Q45.
  ?item wdt:P570 ?time0. hint:Prior hint:rangeSafe true.
  OPTIONAL{?item wdt:P569 ?birthdate .}
  OPTIONAL{?item wdt:P570 ?deathdate .}
  FILTER((?time0 >= "''' + str(pd_year) + '''-01-01"^^xsd:dateTime) && (?time0 < "''' + str(
    pd_year_1) + '''-01-01"^^xsd:dateTime))}''')

wikidata_site = pywikibot.Site("wikidata", "wikidata")
generator = pg.WikidataSPARQLPageGenerator(QUERY, site=wikidata_site)

author_qlist = (
"Q36180", "Q6625963", "Q36834", "Q49757", "Q214917", "Q4853732", "Q201788", "Q1930187", "Q6051619", "Q1028181",
"Q1281618", "Q10800557", "Q2259451", "Q2500638", "Q2526255", "Q333634", "Q33999",
"Q4853732", "Q486748", "Q6051619", "Q6625963", "Q42973")

authors = dict()
wikitext = """Quando o [[direito autoral]] de uma obra expira, ela entra em '''[[domínio público]]'''.
Em Portugal, uma obra entra em [[domínio público]] 70 anos após a morte do autor.<ref>{{citar web|url=http://www.pgdlisboa.pt/leis/lei_mostra_articulado.php?artigo_id=484A0031&nid=484&tabela=leis&pagina=1&ficha=1&so_miolo=&nversao=#artigo |título=CÓDIGO DO DIREITO DE AUTOR E DOS DIREITOS CONEXOS| acessodata=2018-12-29}}</ref>
Segue-se uma '''lista de autores Portugueses cujas obras entram em domínio público em """ + str(pd_year_today) + """'''.
{| class="wikitable sortable" border="1" style="border-spacing:0; style="width:100%;"
! Nome
! Data de Nascimento
! Data de Morte
! Item no Wikidata"""


wikisource = """Quando o [[w:direito autoral|]] de uma obra expira, ela entra em '''[[w:domínio público]]'''.
Em Portugal, uma obra entra em [[w:domínio público]] 70 anos após a morte do autor.<ref>{{citar web|url=temp |título=CÓDIGO DO DIREITO DE AUTOR E DOS DIREITOS CONEXOS| acessodata=2018-12-29}}</ref>
Segue-se uma '''lista de autores Portugueses cujas obras entram em domínio público em """ + str(pd_year_today) + """'''.
{| class="wikitable sortable" border="1" style="border-spacing:0; style="width:100%;"
! Nome
! Data de Nascimento
! Data de Morte
! Item no Wikidata"""

for item in generator:
    # print(item)
    item_dict = item.get(get_redirect= True)  # Get the item dictionary
    # print (item_dict["labels"])
    print(type(item))
    print (item)

    try:
        a_name = item.getSitelink('ptwiki')
    except pywikibot.exceptions.NoSiteLinkError:

        a_name = item_dict["labels"]['pt']

    except:
        a_name = item_dict["labels"]['en']

        print("no pt label")

    # Falta obter página no wikisource
    # try:
    #     ws_name = item.getSitelink('ptwikisource')
    # except pywikibot.exceptions.NoSiteLinkError:
    #
    #     ws_name = item_dict["labels"]['pt']
    #
    # except:
    #     ws_name = item_dict["labels"]['en']

    clm_dict = item_dict["claims"]  # Get the claim dictionary
    # print(clm_dict)
    try:

        clm_list = clm_dict["P106"]
        # print(clm_list)
        # date_of_death = str()

        author = False
        for clm in clm_list:
            clm_trgt = clm.getTarget()
            # print("--", clm_trgt.title())
            if clm_trgt.title() in author_qlist:
                author = True
        if author:
            print(item)
            print("name: ", a_name)
            date_of_birth = None
            date_of_death = None

            clm_death = clm_dict["P570"]
            for clm2 in clm_death:
                death = clm2.getTarget()
                if death.day != 0 and death.month != 0:
                    date_of_death = "{}-{}-{}".format(death.day, death.month, death.year)
                else:
                    date_of_death = death.year

                print("death: ", date_of_death)
            clm_born = clm_dict['P569']
            for clm_b in clm_born:
                born = clm_b.getTarget()
                if born.day != 0 and born.month != 0:

                    date_of_birth = "{}-{}-{}".format(born.day, born.month, born.year)
                else:
                    date_of_birth = born.year

            print("--", a_name, date_of_death, date_of_birth, item.title())

            wikitext = (wikitext + """
|-
|| [[""" + a_name + """]]
|| """ + str(date_of_birth) + """
|| """ + str(date_of_death) + """
|| {{Q|""" + item.title() + """}}""")
            print(wikitext)

            wikisource = (wikisource + """
|-
|| [[author:"""+ a_name + """|]]
|| """ + str(date_of_birth) + """
|| """ + str(date_of_death) + """
|| {{Q|""" + item.title() + """}}""")

            # break
    except Exception as e:
        print("error: ", a_name, e)

    # except:
    #     print ("error with")
    #     pass
wikitext = wikitext + """\n|}

==Referências==
{{reflist}}

[[Categoria:Listas sobre domínio público]]
[[Categoria:%s]]""" % (pd_year_today)
print(wikitext)


wikisource = wikisource + """"\n|}

==Referências==
{{reflist}}

[[Categoria:Listas sobre domínio público]]
[[Categoria:%s]]""" % (pd_year_today)

site = pywikibot.Site('pt', 'wikipedia')
page = pywikibot.Page(site, "User:Aleth Bot/PD{}".format(pd_year_today))
page.text = wikitext
page.save(summary="[[wp:BOT|BOT]]: Lista de autores que entram em domínio Público")

print (wikisource)


wsite = pywikibot.Site('pt', 'wikisource')
ws_page = pywikibot.Page(wsite, "User:Aleth Bot/PD{}".format(pd_year_today))
ws_page.text = wikisource
#ws_page.save(summary="[[wp:BOT|BOT]]: Lista de autores que entram em domínio Público")
