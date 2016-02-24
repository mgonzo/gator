from ..commands import fetch
from bs4 import BeautifulSoup
import os
import sqlite3

def test_fetchHtml():
    assert fetch.fetchHtml('badrequest') == None

def test_hasNoResults():
    with open('./mocks/anchorage.html', 'r') as myfile:
        noresults = myfile.read().replace('\n', '')
    soup = BeautifulSoup(noresults, "html.parser")
    assert fetch.hasNoResults(soup) == True

    html = '<html><body></body></html>'
    soup = BeautifulSoup(html, "html.parser")
    assert fetch.hasNoResults(soup) == False

def test_addQuery():
    string = 'someurl/'
    query = 'myquery'
    assert fetch.addQuery(string, query, None) == "someurl/search/sss?query=myquery"

    category = 'CAT'
    assert fetch.addQuery(string, query, category) == "someurl/search/CAT?query=myquery"

# should test if a from tag is an object
def test_getUrl():
    html = '<div class="row"><a class="i" href="http://url"></a></div>'
    soup = BeautifulSoup(html, "html.parser")
    assert isinstance(fetch.getUrl(soup), str)
    assert fetch.getUrl(soup) == "http://url"
    assert fetch.getUrl(None) == None

    html = '<div class="row"></div>'
    soup = BeautifulSoup(html, "html.parser")
    assert fetch.getUrl(soup) == None

# should test if span from tag is an object
def test_getPrice():
    html = '<div class="row"><span class="price">$500</span></div>'
    soup = BeautifulSoup(html, "html.parser")
    assert isinstance(fetch.getPrice(soup), int)
    assert fetch.getPrice(soup) == 500
    assert fetch.getPrice(None) == None

    html = '<div class="row"></div>'
    soup = BeautifulSoup(html, "html.parser")
    assert fetch.getPrice(soup) == None

# should test if a from tag is an object
def test_getTitle():
    html = '<div class="row"><a class="hdrlnk">Old Bicycle</a></div>'
    soup = BeautifulSoup(html, "html.parser")
    assert isinstance(fetch.getTitle(soup), str)
    assert fetch.getTitle(soup) == "Old Bicycle"
    assert fetch.getTitle(None) == None

    html = '<div class="row"></div>'
    soup = BeautifulSoup(html, "html.parser")
    assert fetch.getUrl(soup) == None


def test_parseRows():

    # if next tag in list is empty return blank list
    empty = iter([])
    data = list()

    emptyTags = fetch.parseRows(empty, data)
    assert len(emptyTags) < 1

    h4Str = '<h4>some text here</h4>'
    h4Soup = BeautifulSoup(h4Str, "html.parser").find('h4')
    h4 = iter([h4Soup])
    assert len(fetch.parseRows(h4, data)) < 1

    newlineStr = '<p>\n</p>'
    newlineSoup = BeautifulSoup(newlineStr, "html.parser").find('p').children
    newline = iter([next(newlineSoup)])
    assert len(fetch.parseRows(newline, data)) < 1

    oneRowHtml = '''<span class="rows"><p class="row" data-pid="5372351858">
                <a href="/boa/5372351858.html" class="i"> <span class="price">$1000</span></a>
                <a class="hdrlnk">Sunfish Sailboat</a></p></span>'''

    oneSoup = BeautifulSoup(oneRowHtml, "html.parser")
    oneRow = oneSoup.find('span', class_="rows")
    oneTag = oneRow.children

    testOneRow = [{'url': '/boa/5372351858.html', 'price': 1000, 'title': 'Sunfish Sailboat'}]
    assert fetch.parseRows(oneTag, data) == testOneRow

    twoRowsHtml = '''<span class="rows"><p class="row" data-pid="5372351858">
                <a href="/boa/5372351858.html" class="i"> <span class="price">$1000</span></a>
                <a class="hdrlnk">Sunfish Sailboat</a></p><p class="row" data-pid="0000000000">
                <a href="/boa/0000000000.html" class="i"> <span class="price">$500</span></a>
                <a class="hdrlnk">Two Sunfish Sailboat</a></p></span>'''

    twoSoup = BeautifulSoup(twoRowsHtml, "html.parser")
    twoRows = twoSoup.find('span', class_="rows")
    twoTags = twoRows.children

    data = list()
    testTwoRows = [
        {'url': '/boa/5372351858.html', 'price': 1000, 'title': 'Sunfish Sailboat'},
        {'url': '/boa/0000000000.html', 'price': 500, 'title': 'Two Sunfish Sailboat'}
    ]

    assert fetch.parseRows(twoTags, data) == testTwoRows

    threeRowsHtml = '''<span class="rows"><p class="row" data-pid="5372351858">
                <a href="/boa/5372351858.html" class="i"> <span class="price">$1000</span></a>
                <a class="hdrlnk">Sunfish Sailboat</a></p><p class="row" data-pid="0000000000">
                <a href="/boa/0000000000.html" class="i"> <span class="price">$500</span></a>
                <a class="hdrlnk">Two Sunfish Sailboat</a></p><p class="row" data-pid="1111111111">
                <a href="/boa/1111111111.html" class="i"> <span class="price">$1500</span></a>
                <a class="hdrlnk">Three Sunfish Sailboat</a></p></span>'''

    threeSoup = BeautifulSoup(threeRowsHtml, "html.parser")
    threeRows = threeSoup.find('span', class_="rows")
    threeTags = threeRows.children

    data = list()
    testThreeRows = [
        {'url': '/boa/5372351858.html', 'price': 1000, 'title': 'Sunfish Sailboat'},
        {'url': '/boa/0000000000.html', 'price': 500, 'title': 'Two Sunfish Sailboat'},
        {'url': '/boa/1111111111.html', 'price': 1500, 'title': 'Three Sunfish Sailboat'}
    ]

    assert fetch.parseRows(threeTags, data) == testThreeRows


def test_getDataFromHtml():
    assert fetch.getDataFromHtml(None) == None

    noresults = '<html><body><div class="noresults"></div></body></html>'
    assert fetch.getDataFromHtml(noresults) == None

    twoRowsHtml = '''<span class="rows"><p class="row" data-pid="5372351858">
                <a href="/boa/5372351858.html" class="i"> <span class="price">$1000</span></a>
                <a class="hdrlnk">Sunfish Sailboat</a></p><p class="row" data-pid="0000000000">
                <a href="/boa/0000000000.html" class="i"> <span class="price">$500</span></a>
                <a class="hdrlnk">Two Sunfish Sailboat</a></p></span>'''

    twoSoup = BeautifulSoup(twoRowsHtml, "html.parser")
    twoRows = twoSoup.find('span', class_="rows")
    twoTags = twoRows.children

    testTwoRows = [
        {'url': '/boa/5372351858.html', 'price': 1000, 'title': 'Sunfish Sailboat'},
        {'url': '/boa/0000000000.html', 'price': 500, 'title': 'Two Sunfish Sailboat'}
    ]

    data = fetch.getDataFromHtml(twoRowsHtml)
    assert len(data) > 1
    assert data == testTwoRows

#
# takes data in
# stores in a sqlite file
# maybe pass in the sqlite filename at runtime
# assert that the data has been saved correctly
#   by retreiving expected results from db
# assert success message
# assert failure message
def test_storeData():
    db = 'tests/db/example.db'
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    nodata = None
    assert fetch.storeData(cursor, nodata) == None

    emptydata = list()
    assert fetch.storeData(cursor, emptydata) == None

    data = [
        {'url': '/boa/5372351858.html', 'price': 1000, 'title': 'Sunfish Sailboat'},
        {'url': '/boa/0000000000.html', 'price': 500, 'title': 'Two Sunfish Sailboat'}
    ]

    fetch.storeData(cursor, data)
    cursor.execute('select * from results')

    firstrow = cursor.fetchone()
    assert firstrow == ('/boa/5372351858.html', 1000.0, 'Sunfish Sailboat')

    secondrow = cursor.fetchone()
    assert secondrow == ('/boa/0000000000.html', 500.0, 'Two Sunfish Sailboat')

    # clean up
    if os.path.isfile(db):
        os.remove(db)
