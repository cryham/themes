#!/usr/bin/python3
# -*- coding: utf-8 -*-

#  Script creates a im.cvs file for import to table of movies
#  on my website: https://cryham.tuxfamily.org/movies/
#  From im.html file, as exported bookmarks from Firefox.
#  Only bookmarks containing ** in name, and following syntax:
#  Title (year) - rate **tags

import os
import re
import datetime
from operator import itemgetter, attrgetter
import string


#  const dict  bookmark tag shorcuts
#-------------------------------------
sh_tag = {
'sf':'SciFi',
'act':'Action','cmd':'Comedy','rom':'Romance',
'crm':'Crime','drm':'Drama','prd':'Parody',
'wst':'Western','hor':'Horror','mst':'Mystery',
'adv':'Adventure','fan':'Fantasy',
'3d':'3D','gam':'Game','drw':'Drawing', # style
'cmc':'Comic','bok':'Book','sph':'SuperHero', # based
'spc':'Space','ftr':'Future','tmt':'Time', # scifi
'mgc':'Magic','zmb':'Zombie','aln':'Alien', # theme
'hs':'School','drg':'Drugs','war':'War',  # topic
}

#------------------------------------------------
class Tag:
    def __init__(self, short, long, count):
        self.short = short
        self.long = long
        self.count = count
    

class Movie:
    def __init__(self, year, movie, url, rate, tags):
        self.year = year
        self.movie = movie
        self.url = url
        self.rate = rate
        self.tags = tags


#  open file  ------------------------
file = open('im.html', 'r')
lines = file.readlines()

movies = 0
errors = 0
all = []
tagset = set()
tagcnt = dict()

for line in lines:
    # line e.g.:
    # HREF="https://www.imdb.com/title/tt0848537/" ADD_DATE="  " LAST_MODIFIED="  "
    # ICON_URI="   " ICON="   ">Epic (2013) - 6.6 **3d</A>

    r = re.match(r'.*HREF="(.*)" ADD.*>(.*\*\*.*)</A>', line)
    if r:
        url = r.groups()[0]
        title = r.groups()[1]

        rt = re.match(r'(.*)\s+\(+(\d{4})\)*\s*-\s*(.*)\s*\*\*(.*)', title)
        if not rt:
            print('error in: '+title)
            errors += 1
        else:
            movie = rt.groups()[0]
            if movie[0] in '-`~^+':
                movie = movie[1:]
            year = rt.groups()[1]
            
            rate = rt.groups()[2]
            rate = re.sub(' |-|`','',rate)
            rate = rate.replace(',','.')
            tags = rt.groups()[3]
            
            st = ''
            tt = str.split(tags)
            for t in tt:
                t = t.replace('-','')
                t = t.replace('`','')
                tagset.add(t)
                tagcnt[t] = tagcnt.get(t, 0) + 1
                st = st + sh_tag.get(t, t) + ' '

            print(year+' | '+movie+' | '+ rate +' | '+st)  # test
            movies += 1
            all.append(Movie(year, movie, url, rate, st))


#  tags set  ------------------------
print('---- tags:')

#  sort by count
Tags = []
for t in tagset:
    if not t in sh_tag:
        print('error: unknown tag: '+t)
        errors += 1
    else:
        #print(t +' '+ sh_tag[t] +' '+ str(tagcnt.get(t, '-')))
        Tags.append(Tag(t, sh_tag[t], tagcnt.get(t, '-') ))

sTags = sorted(Tags, key=attrgetter('count'))
for t in sTags:
    print(t.short +' '+ t.long +' '+ str(t.count))


#  ----
if errors > 0:
    print('ERRORS: '+str(errors))


#  end print  ------------------------
date_str = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')

print('\nTotal movies: {}'.format(movies))
print('Last updated on: {}'.format(date_str))


#  export to file  ------------------------
sAll = sorted(all, key=attrgetter('year'))

expfile = open('im.csv', 'w')
expfile.write('year,movie title with link,rate,tags\n')
for m in sAll:
    expfile.write(m.year+',' #+m.movie+','+
    '"<a href=""'+m.url+'"" rel=""noopener"" target=""_blank"">'+m.movie+'</a>"'
    +','+m.rate+','+m.tags+'\n')

expfile.close()
