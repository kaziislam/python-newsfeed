
def format_date(date):
    return date.strftime('%m/%d/%y')

from datetime import datetime
print(format_date(datetime.now()))

def format_url(url):
    return url.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]

# print(format_url('http://google.com/test/'))
# print(format_url('https://www.google.com?q=test'))

def format_plural(amount, word):
    if amount != 1:
        return word + 's'
    return word

# print(format_plural(2, 'cat'))
# print(format_plural(1, 'dog'))

