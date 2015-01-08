"""Generates a html page showing numbers of FNAL preprints written by
   type, FNAL Division and date."""
import datetime
import pytz
import re

from invenio.search_engine import perform_request_search
CHICAGO_TIMEZONE = pytz.timezone('America/Chicago')

from lxml import etree
import lxml.html
from lxml.html import builder as E
from StringIO import StringIO

YEAR = int(CHICAGO_TIMEZONE.fromutc(datetime.datetime.utcnow()).strftime('%Y'))
YEAR_1 = str(YEAR - 1)
YEAR_2 = str(YEAR - 2)
YEAR = str(YEAR)

MONTH = int(CHICAGO_TIMEZONE.fromutc(datetime.datetime.utcnow()) \
.strftime('%m'))
MONTH_1 = MONTH - 1
MONTH_2 = MONTH - 2

if MONTH == 1:
    MONTH = YEAR + '-01'
    MONTH_1 = YEAR_1 + '-12'
    MONTH_2 = YEAR_1 + '-11'
elif MONTH == 2:
    MONTH = YEAR + '-02'
    MONTH_1 = YEAR + '-01'
    MONTH_2 = YEAR_1 + '-12'
else:
    FMONTH = lambda x: '-0' + str(x) if x < 10 else '-' + str(x)
    MONTH = YEAR + FMONTH(MONTH)
    MONTH_1 = YEAR + FMONTH(MONTH_1)
    MONTH_2 = YEAR + FMONTH(MONTH_2)

DATE_TIME_STAMP = \
CHICAGO_TIMEZONE.fromutc(datetime.datetime.utcnow()).strftime('%Y-%m-%d \
 %H:%M:%S')
DATE_STAMP = \
CHICAGO_TIMEZONE.fromutc(datetime.datetime.utcnow()).strftime('%Y-%m-%d')


def create_table():
    """HTML generation by lxml.html tree."""
    divisions = ['All', 'E', 'CMS', 'T', 'A', 'AE', 'PPD', 'AD/APC']
    divisions += ['TD', 'CD', 'Other']
    pubtypes = ['All', 'PUB', 'THESIS', 'CONF', 'TM', 'FN']
    dates = [YEAR_2, YEAR_1, YEAR, MONTH_2, MONTH_1, MONTH]
    years = [YEAR_2, YEAR_1, YEAR]
    months = [MONTH_2, MONTH_1, MONTH]

    #This is a doctype work around for a lxml.etree bug
    doctype_wa = etree.parse(StringIO('''<!DOCTYPE html>\n<html xmlns= \
"http://www.w3.org/1999/xhtml" lang="en" xml:lang="en"></html>'''))
    head_tag = E.HEAD(E.META(charset="utf-8"), E.TITLE("FERMILAB RESEARCH AT A \
GLANCE"), E.STYLE("td {text-align: right;}td.l {text-align: left;padding: \
7px;}"))
    body = E.BODY(E.P(E.A("Fermilab Technical Publications", \
href="http://ccd.fnal.gov/techpubs/fermilab_spires.html")))
    tag_h3 = E.H3("FERMILAB RESEARCH AT A GLANCE")
    tag_p = E.P("Glossary at end.")
    tag_p_and_i = E.P(E.I("Updated: " + DATE_TIME_STAMP))

    body.append(tag_h3)
    body.append(tag_p)
    body.append(tag_p_and_i)
    table = E.TABLE()

    tag_tr_td = E.TR(E.TD, E.TD("Date"))
    for division in divisions:
        if division == 'A':
            division = 'AT'
        tag_tr_td.append(E.TD(division))
    table.append(tag_tr_td)

    pub_table_row = E.TR()
    for pubtype in pubtypes:
        pub_table_row.append(E.TD(pubtype))
        pub_type_datelist = E.TD()
        year_list = E.UL()
        month_list = E.UL()
        for year in years:
            year_list.append(E.LI(year))
        for month in months:
            month_list.append(E.LI(month))
        pub_type_datelist.append(year_list)
        pub_type_datelist.append(month_list)
        pub_type_datelist.append(E.UL())
        pub_table_row.append(pub_type_datelist)
        pub_type_datelist = E.TD()

        for division in divisions:
            tdg = E.TD()
            list_of_searches = E.UL()
            for date in dates:
                if division == 'All':
                    division = ''
                if pubtype == 'All':
                    pubtype = ''
                search = 'find r fermilab ' + pubtype
                if division == 'Other':
                    for good_division in divisions[1:len(divisions)-1]:
                        if good_division == 'AD/APC':
                            search += ' not  (r AD or APC)'
                        else:
                            search += ' not r ' + good_division
                elif division == 'AD/APC':
                    search = 'find r fermilab ' + pubtype + \
                              ' and (r AD or APC)'
                else:
                    search += ' ' + division
                search += ' and d ' + date
#                search += ' and de ' + date
                search = re.sub(r'\s+', ' ', search)
                result = perform_request_search(p=search, cc="HEP")
                result = len(result)
                if result == 0:
                    hit_number = E.LI()
                else:
                    link = search.replace(' ', '+')
                    link = 'http://inspirehep.net/search?p=' + link
                    link += '&rg=100&sf=earliestdate'
                    hit_number = E.LI(E.A(str(result), href=link))
                list_of_searches.append(hit_number)
                if date == YEAR or date == MONTH:
                    tdg.append(list_of_searches)
                    list_of_searches = E.UL()

            pub_table_row.append(tdg)

        table.append(pub_table_row)
        pub_table_row = E.TR()
    glos = E.H4('Glossary')
    table2 = E.TABLE()
    glos_tr_td = E.TR(E.TD({'class': 'l'}, "E: Experimental papers"), \
E.TD({'class': 'l'}, "PPD: Particle Physics Division papers"))
    table2.append(glos_tr_td)
    glos_tr_td = E.TR(E.TD({'class': 'l'}, "T: Particle Physics Division \
Theoretical Physics Department papers"), E.TD({'class': 'l'}, "AD/APC: \
Accelerator Division and Accelerator Physics Center papers"))
    table2.append(glos_tr_td)
    glos_tr_td = E.TR(E.TD({'class': 'l'}, "AT: Fermilab Center for Particle \
Astrophysics theoretical papers"), E.TD({'class': 'l'}, "TD: Technical \
Division papers"))
    table2.append(glos_tr_td)
    glos_tr_td = E.TR(E.TD({'class': 'l'}, "AE: Fermilab Center for Particle \
Astrophysics experimental papers"), E.TD({'class': 'l'}, "CD: Computing \
Sector papers"))
    table2.append(glos_tr_td)
    glos_tr_td = E.TR(E.TD({'class': 'l'}, " "), E.TD({'class': 'l'}, " "))
    table2.append(glos_tr_td)
    glos_tr_td = E.TR(E.TD({'class': 'l'}, " "), E.TD({'class': 'l'}, " "))
    table2.append(glos_tr_td)
    glos_tr_td = E.TR(E.TD({'class': 'l'}, " "), E.TD({'class': 'l'}, " "))
    table2.append(glos_tr_td)
    glos_tr_td = E.TR(E.TD({'class': 'l'}, "PUB: Paper intended for \
publication in a journal"), E.TD({'class': 'l'}, "TM: Technical memo"))
    table2.append(glos_tr_td)
    glos_tr_td = E.TR(E.TD({'class': 'l'}, "CONF: Paper written as part of a \
conference"), E.TD({'class': 'l'}, "FN: Physics note - short paper not \
fitting the other categories"))
    table2.append(glos_tr_td)
    glos_tr_td = E.TR(E.TD({'class': 'l'}, "THESIS: Ph.D. thesis based on \
work done at Fermilab"), E.TD({'class': 'l'}, ""))
    table2.append(glos_tr_td)

    body.append(table)
    body.append(glos)
    body.append(table2)
    doctype_wa.getroot().append(head_tag)
    doctype_wa.getroot().append(body)
    out = lxml.html.tostring(doctype_wa, encoding='UTF-8', pretty_print=True, \
method='html').rstrip('\n')
    return out

def main():
    """Writes html product to file with extension html."""
    filename = 'fermilab_research_glance.html'
    #filename_w = 'www/' + filename
    filename_w = filename
    output = open(filename_w, 'w')
    table = create_table()
    output.write(table)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'Exiting'
