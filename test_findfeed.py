import functions

def test_get_rss_nofeed():
    response = functions.get_rss_feed('http://google.com')
    assert response == 'End'

def test_get_rss_feed():
    response = functions.get_rss_feed('http://vox.com')
    assert response != None and response != 'No feed found on this site. Try another!'

def test_get_rss_badfeed():
    response = functions.get_rss_feed('http://kentuckysportsradio.com')
    assert response == 'Sorry! Not authorized to check for feeds on this site.'

def test_print_message():
    response = functions.print_message('title','url',['positives'],['negatives'],'sentiment')
    line1="---------------------------------------------------------------------------"
    line2="Title: title"
    line3="URL: url"
    line4="Positive Indicator Words:"
    line5="['positives']"
    line6="Negative Indicator Words:"
    line7="['negatives']"
    line8="The overall sentiment of this post is sentiment!"
    line9="---------------------------------------------------------------------------"
    message= line1+'\n'+line2+'\n\n'+line3+'\n\n'+line4+'\n\n'+line5+'\n\n'+line6+'\n'+line7+'\n\n'+line8+'\n'+line9
    assert response == message

def test_process_negsentiment():
    response = functions.process_sentiment('Bananas are disgusting fruits')
    assert response == 'negative'

def test_process_psossentiment():
    response = functions.process_sentiment('Bananas are wonderful fruits')
    assert response == 'positive'

def test_process_nutsentiment():
    response = functions.process_sentiment('Bananas are fruits')
    assert response == 'neutral'

def test_process_badindicators():
    response = functions.process_indicators('Bananas are disgusting fruits')
    assert response == {'p':[], 'n':[b'disgusting']}

def test_process_goodindicators():
    response = functions.process_indicators('Bananas are wonderful fruits')
    assert response == {'p':[b'wonderful'], 'n':[]}

def test_process_noindicators():
    response = functions.process_indicators('Bananas are fruits')
    assert response == {'p':[], 'n':[]}

def test_process_feed():
    response = functions.process_feed('https://mashable.com/category/rss/')
    assert response == 'End'