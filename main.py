from requests_html import HTMLSession


def main():
    session = HTMLSession()
    r = session.get('https://pythonclock.org')
    print(r.html.search('Python 2.7 will retire in...{}Enable Guido Mode')[0])
    r.html.render()
    print(r.html.search('Python 2.7 will retire in...{}Enable Guido Mode')[0])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
