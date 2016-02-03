from ..commands import fetch
from bs4 import BeautifulSoup

def test_fetchHtml_Error():
    assert fetch.fetchHtml('badrequest') == None
 
def test_hasNoResults():
    html = '<html><body><div class="noresults"></div></body></html>'
    soup = BeautifulSoup(html, "html.parser")
    assert fetch.hasNoResults(soup) == True

def test_hasNoResults_Fail():
    html = '<html><body></body></html>'
    soup = BeautifulSoup(html, "html.parser")
    assert fetch.hasNoResults(soup) == False

def test_addQuery():
    string = 'someurl/'
    query = 'myquery'
    assert fetch.addQuery(string, query, None) == "someurl/search/sss?query=myquery"

def test_addQuery_WithCategory():
    string = 'someurl/'
    query = 'myquery'
    category = 'CAT'
    assert fetch.addQuery(string, query, category) == "someurl/search/CAT?query=myquery"

def test_getDataFromHtml_NoHtml():
    html = None
    assert fetch.getDataFromHtml(html) == None

def test_getDataFromHtml_NoResults():
    html = '<html><body><div class="noresults"></div></body></html>'
    assert fetch.getDataFromHtml(html) == None

def test_getDataFromHtml():
    html = '<html><body><div></div></body></html>'
    data = fetch.getDataFromHtml(html)
    assert len(data) >= 1

def test_storeData_NoData():
    data = None
    assert fetch.storeData(data) == None 

def test_storeData_NoDataLen():
    data = list()
    assert fetch.storeData(data) == None 
