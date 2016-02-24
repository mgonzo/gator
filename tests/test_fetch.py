from ..commands import fetch
from bs4 import BeautifulSoup

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


def test_parseRow():

    # if next tag in list is empty return blank list
    empty = iter([])
    data = list()

    emptyTags = fetch.parseRow(empty, data)
    assert len(emptyTags) < 1

    h4Str = '<h4>some text here</h4>'
    h4Soup = BeautifulSoup(h4Str, "html.parser").find('h4')
    h4 = iter([h4Soup])
    assert len(fetch.parseRow(h4, data)) < 1

    newlineStr = '<p>\n</p>'
    newlineSoup = BeautifulSoup(newlineStr, "html.parser").find('p').children
    newline = iter([next(newlineSoup)])
    assert len(fetch.parseRow(newline, data)) < 1

    oneRowHtml = '''<span class="rows"><p class="row" data-pid="5372351858">
                <a href="/boa/5372351858.html" class="i"> <span class="price">$1000</span></a>
                <a class="hdrlnk">Sunfish Sailboat</a></p></span>'''

    oneSoup = BeautifulSoup(oneRowHtml, "html.parser")
    oneRow = oneSoup.find('span', class_="rows")
    oneTag = oneRow.children

    testOneRow = [{'url': '/boa/5372351858.html', 'price': 1000, 'title': 'Sunfish Sailboat'}]
    assert fetch.parseRow(oneTag, data) == testOneRow

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

    assert fetch.parseRow(twoTags, data) == testTwoRows

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

    assert fetch.parseRow(threeTags, data) == testThreeRows


def test_getDataFromHtml():
    assert fetch.getDataFromHtml(None) == None

    noresults = '<html><body><div class="noresults"></div></body></html>'
    assert fetch.getDataFromHtml(noresults) == None

    html = ''
    data = fetch.getDataFromHtml(html)
    assert len(data) >= 1

def test_storeData():
    nodata = None
    assert fetch.storeData(nodata) == None

    emptydata= list()
    assert fetch.storeData(emptydata) == None

