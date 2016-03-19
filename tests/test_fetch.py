import pytest
from ..commands import fetch
from bs4 import BeautifulSoup
import os
import sqlite3

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


def test_parseRows(oneRowHtml, twoRowsHtml):
    # if next tag in list is empty return blank list
    empty = iter([])
    data = list()

    emptyTags = fetch.parseRows(empty, data)
    assert len(emptyTags) < 1

    newlineStr = '<p>\n</p>'
    newlineSoup = BeautifulSoup(newlineStr, "html.parser").find('p').children
    newline = iter([next(newlineSoup)])
    assert len(fetch.parseRows(newline, data)) < 1

    oneSoup = BeautifulSoup(oneRowHtml, "html.parser")
    oneRow = oneSoup.find('div', class_="content")
    oneTag = oneRow.findAll('p', class_="row")
    testOneRow = [{'price': 75, 'title': 'Sunfish Sail Boat for Sale', 'url': '/boa/5473914599.html'}]
    assert fetch.parseRows(iter(oneTag), data) == testOneRow

    twoSoup = BeautifulSoup(twoRowsHtml, "html.parser")
    twoRows = twoSoup.find('div', class_="content")
    twoTags = twoRows.findAll('p', class_="row")
    data = list()
    testTwoRows = [
        {'price': 125, 'url': '/lac/boa/5454499053.html', 'title': 'Sunfish Sale Boat - great shape'},
        {'price': 550, 'title': 'Hydrasail small sailboat', 'url': '/lac/boa/5477174831.html'}
    ]
    assert fetch.parseRows(iter(twoTags), data) == testTwoRows

def test_getDataFromHtml(twoRowsHtml):
    assert fetch.getDataFromHtml(None) == None

    noresults = '<html><body><div class="noresults"></div></body></html>'
    assert fetch.getDataFromHtml(noresults) == None

    twoSoup = BeautifulSoup(twoRowsHtml, "html.parser")
    twoRows = twoSoup.find('div', class_="content")
    twoTags = twoRows.findAll('p', class_="row")

    testTwoRows = [
        {'price': 125, 'url': '/lac/boa/5454499053.html', 'title': 'Sunfish Sale Boat - great shape'},
        {'price': 550, 'title': 'Hydrasail small sailboat', 'url': '/lac/boa/5477174831.html'}
    ]

    data = fetch.getDataFromHtml(twoRowsHtml)
    assert next(data) == testTwoRows[0]
    assert next(data) == testTwoRows[1]

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

    #emptydata = list()
    #assert fetch.storeData(cursor, emptydata) == None

    data = [
        {'url': '/boa/5372351858.html', 'price': 1000, 'title': 'Sunfish Sailboat'},
        {'url': '/boa/0000000000.html', 'price': 500, 'title': 'Two Sunfish Sailboat'}
    ]

    cursor.execute('create table if not exists results (url text, price real, title text)')

    fetch.storeData(cursor, iter(data))
    cursor.execute('select * from results')

    firstrow = cursor.fetchone()
    print("FIRST ROW")
    print(firstrow)
    assert firstrow == ('/boa/5372351858.html', 1000.0, 'Sunfish Sailboat')

    secondrow = cursor.fetchone()
    assert secondrow == ('/boa/0000000000.html', 500.0, 'Two Sunfish Sailboat')

    # clean up
    #if os.path.isfile(db):
    #    os.remove(db)
