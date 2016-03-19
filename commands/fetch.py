#!/usr/bin/python3

from urllib.request import urlopen
from urllib import error
import http
from bs4 import BeautifulSoup
import re

#
def fetchHtml(url):
    print('Fetching '+ url)
    try:
        response = urlopen(url)

    except error.HTTPError as e:
        print('HTTPError = ' + str(e.code))
        return None

    except error.URLError as e:
        print('URLError = ' + str(e.reason))
        return None

    except http.client.HTTPException as e:
        print('HTTPException')
        return None

    except Exception as e:
        import traceback
        print('generic exception: ' + traceback.format_exc())
        return None

    return response.read()

#
def getList(query, category):
    sites = 'http://www.craigslist.org/about/sites'
    html = fetchHtml(sites)
    htmlParsed = BeautifulSoup(html, 'html.parser')
    h1 = htmlParsed.find('a', attrs={'name':'US'}).parent
    div = h1.next_sibling.next_sibling
    links = list()
    for link in div.find_all('a', href = re.compile('org')):
        # skip mobile
        if (link.get('href') == "//mobile.craigslist.org/"):
            continue
        links.append(addQuery('http:' + link.get('href'), query, category))
    return iter(links)

#
def hasNoResults(soup):
    noresults = len(soup.find_all('div', class_="noresults"))
    if (noresults > 0):
        print('No Results')
        return True
    return False

#
def addQuery(string, query, category):
    if (category == None):
        category = 'sss'
    return string + 'search/{0!s}?query={1!s}'.format(category, query)

# url is a string
# return None if no url
def getUrl(tag):
    if (tag == None):
        return None

    a = tag.find('a', class_="i")
    if (a == None):
        return None

    url = a.attrs['href']
    return url

# price is an int
# return None if no price
def getPrice(tag):
    if(tag == None):
        return None

    span = tag.find('span', class_="price")
    if (span == None):
        return None

    price = int(span.contents[0][1:])
    return price

# title is a string
# return None if no title
def getTitle(tag):
    if(tag == None):
        return None

    span = tag.find('span', id="titletextonly")
    if (span == None):
        return None

    title = span.contents[0]
    return title

#
# should pass in only the iterator
# and call next(iter) on first line
# instead of calling next(iter) before
# calling this function
def parseRows(tags, data):
    try:
        tag = next(tags)
        row = dict()
        row['url'] = getUrl(tag)
        row['price'] = getPrice(tag)
        row['title'] = getTitle(tag)

        if (not isinstance(row['url'], str)):
            return []

        # full urls are non local results
        if (len(row['url'].split('/')) > 4):
            return []

        print(row)
        data.append(row)
        parseRows(tags, data)

    except StopIteration:
        return []

    except TypeError:
        return []

    except NameError:
        return []

    except AttributeError:
        return []

    return data

#
# get the tags list
# call parseRows
# return data
def getDataFromHtml(html):
    if(html == None):
        return None

    soup = BeautifulSoup(html, 'html.parser')

    if (hasNoResults(soup)):
        return None

    content = soup.find('div', class_="content")
    tags = content.findAll('p', class_="row")
    data = parseRows(iter(tags), [])
    return iter(data)

#
# recursively store each row
# use supplied db cursor to act on db
# store data from list
def storeData(cursor, data):
    try:
        row = next(data)
        cursor.execute('''insert into results (url, price, title) 
            values(:url, :price, :title)''', row)

        storeData(cursor, data)

    except StopIteration:
        return None

    except TypeError:
        return None
