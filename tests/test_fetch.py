import pytest
from ..commands import fetch
from bs4 import BeautifulSoup
import os
import sqlite3
from datetime import datetime

@pytest.fixture
def oneRowHtml():
    with open('./fixtures/oneRow.html', 'r') as oneRowHtmlFile:
        oneRowHtml = oneRowHtmlFile.read().replace('\n', '')
    return oneRowHtml

@pytest.fixture
def twoRowsHtml():
    with open('./fixtures/twoRows.html', 'r') as twoRowsHtmlFile:
        twoRowsHtml = twoRowsHtmlFile.read().replace('\n', '')
    return twoRowsHtml

@pytest.fixture
def metaData():
    return [
            'sunfish', 
            'boa', 
            'losangeles', 
            'http://losangeles.craigslist.com/search/boa?query=sunfish',
            '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.today())
            ]

@pytest.fixture
def oneRowData():
    return [{'price': 75, 
            'title': 'Sunfish Sail Boat for Sale', 
            'url': '/boa/5473914599.html',
            'query': 'sunfish', 
            'category': 'boa', 
            'city': 'losangeles',
            'link': 'http://losangeles.craigslist.com/search/boa?query=sunfish',
            'date': '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.today())
            }]

    return testOneRow

@pytest.fixture
def twoRowsData():
    return [{'price': 125, 
            'title': 'Sunfish Sale Boat - great shape',
            'url': '/lac/boa/5454499053.html',
            'query': 'sunfish', 
            'category': 'boa', 
            'city': 'losangeles',
            'link': 'http://losangeles.craigslist.com/search/boa?query=sunfish',
            'date': '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.today()) }, 

            {'price': 550,
            'title': 'Hydrasail small sailboat',
            'url': '/lac/boa/5477174831.html',
            'query': 'sunfish', 
            'category': 'boa', 
            'city': 'losangeles',
            'link': 'http://losangeles.craigslist.com/search/boa?query=sunfish',
            'date': '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.today()) }]

    return testTwoRows

def test_fetchHtml():
    assert fetch.fetchHtml('badrequest') == None

def test_getList():
    # should return an iter
    # assert False
    return

def test_hasNoResults():
    with open('./fixtures/noresults.html', 'r') as myfile:
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
    html = '<p class="row"><span class="price">$500</span></p>'
    soup = BeautifulSoup(html, "html.parser")
    assert isinstance(fetch.getPrice(soup), int)
    assert fetch.getPrice(soup) == 500
    assert fetch.getPrice(None) == None

    html = '<div class="row"></div>'
    soup = BeautifulSoup(html, "html.parser")
    assert fetch.getPrice(soup) == None

# should test if a from tag is an object
def test_getTitle(oneRowHtml):
    oneSoup = BeautifulSoup(oneRowHtml, "html.parser")
    oneRow = oneSoup.find('div', class_="content")
    oneTag = oneRow.find('p', class_="row")

    assert isinstance(fetch.getTitle(oneTag), str)
    assert fetch.getTitle(oneTag) == "Sunfish Sail Boat for Sale"
    assert fetch.getTitle(None) == None

    html = '<div class="row"></div>'
    soup = BeautifulSoup(html, "html.parser")
    assert fetch.getUrl(soup) == None


def test_parseRows(metaData, oneRowHtml, oneRowData, twoRowsHtml, twoRowsData):
    # if next tag in list is empty return blank list
    empty = iter([])
    data = list()
    emptyTags = fetch.parseRows(metaData, empty, data)
    assert len(emptyTags) < 1

    newlineStr = '<p>\n</p>'
    newlineSoup = BeautifulSoup(newlineStr, "html.parser").find('p').children
    newline = iter([next(newlineSoup)])
    assert len(fetch.parseRows(metaData, newline, data)) < 1

    oneSoup = BeautifulSoup(oneRowHtml, "html.parser")
    oneRow = oneSoup.find('div', class_="content")
    oneTag = oneRow.findAll('p', class_="row")
    assert fetch.parseRows(metaData, iter(oneTag), data) == oneRowData

    twoSoup = BeautifulSoup(twoRowsHtml, "html.parser")
    twoRows = twoSoup.find('div', class_="content")
    twoTags = twoRows.findAll('p', class_="row")
    data = list()
    assert fetch.parseRows(metaData, iter(twoTags), data) == twoRowsData

def test_parseMetaData():
    link = 'http://phoenix.craigslist.org/search/boa?query=sunfish'
    datenow = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.today())

    results = fetch.parseMetaData(link, datenow)
    assert isinstance(results, list)
    assert results[0] == 'sunfish'
    assert results[1] == 'boa'
    assert results[2] == 'phoenix'
    assert results[3] == 'http://phoenix.craigslist.org/search/boa?query=sunfish'
    assert results[4] == datenow
    # need to test that date returned is a date

def test_getDataFromHtml(twoRowsHtml, twoRowsData):
    link = 'http://losangeles.craigslist.com/search/boa?query=sunfish'
    datenow = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.today())

    assert fetch.getDataFromHtml(None, link, datenow) == None

    noresults = '<html><body><div class="noresults"></div></body></html>'
    assert fetch.getDataFromHtml(noresults, link, datenow) == None

    twoSoup = BeautifulSoup(twoRowsHtml, "html.parser")
    twoRows = twoSoup.find('div', class_="content")
    twoTags = twoRows.findAll('p', class_="row")

    data = fetch.getDataFromHtml(twoRowsHtml, link, datenow)
    assert next(data) == twoRowsData[0]
    assert next(data) == twoRowsData[1]

#
# takes data in
# stores in a sqlite file
# maybe pass in the sqlite filename at runtime
# assert that the data has been saved correctly
#   by retreiving expected results from db
# assert success message
# assert failure message
def test_storeData(twoRowsData):
    db = 'tests/db/example.db'
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    nodata = None
    assert fetch.storeData(cursor, nodata) == None

    cursor.execute('''
        create table if not exists results 
            (date text, 
            query text, 
            category text, 
            city text, 
            url text, 
            price real, 
            title text, 
            link text)''')

    fetch.storeData(cursor, iter(twoRowsData))
    connection.commit()

    cursor.execute('select * from results')

    firstrow = cursor.fetchone()
    print("FIRST ROW")
    print(firstrow)
    assert firstrow == ('{0:%Y-%m-%d %H:%M:%S}'.format(datetime.today()), 'sunfish', 'boa', 'losangeles', '/lac/boa/5454499053.html', 125.0, 'Sunfish Sale Boat - great shape', 'http://losangeles.craigslist.com/search/boa?query=sunfish')

    secondrow = cursor.fetchone()
    print("SECOND ROW")
    print(secondrow)
    assert secondrow == ('{0:%Y-%m-%d %H:%M:%S}'.format(datetime.today()), 'sunfish', 'boa', 'losangeles', '/lac/boa/5477174831.html', 550.0, 'Hydrasail small sailboat', 'http://losangeles.craigslist.com/search/boa?query=sunfish')

    # clean up
    if os.path.isfile(db):
        os.remove(db)
