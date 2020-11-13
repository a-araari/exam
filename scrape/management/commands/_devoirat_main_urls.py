URLS = [
    'https://www.devoirat.net/allemand/devoirs-allemand/4ème-année-bac/',
    'https://www.devoirat.net/anglais/cours-anglais/2ème-année/',
    'https://www.devoirat.net/anglais/devoirs-anglais/2ème-année/',
    'https://www.devoirat.net/arabe/devoirs-arabe/1ère-année/',
    'https://www.devoirat.net/arabe/devoirs-arabe/3ème-année/',
    'https://www.devoirat.net/arabe/devoirs-arabe/4ème-année-bac/',
    'https://www.devoirat.net/espagnol/devoirs-espagnol/3ème-lettre/',
    'https://www.devoirat.net/français/devoirs-français/3ème-année/',
    'https://www.devoirat.net/français/séries-français/1ère-année/',
    'https://www.devoirat.net/français/séries-français/2ème-année/',
    'https://www.devoirat.net/informatique/cours-informatique/bac-eco-gest/',
    'https://www.devoirat.net/informatique/devoirs-informatique/bac-sciences-exp/',
    'https://www.devoirat.net/informatique/devoirs-informatique/base-de-donnees/',
    'https://www.devoirat.net/informatique/devoirs-informatique/informatique-1/',
    'https://www.devoirat.net/informatique/devoirs-informatique/technique/',
    'https://www.devoirat.net/maths/cours-maths/eco-service/',
    'https://www.devoirat.net/maths/cours-maths/maths/',
    'https://www.devoirat.net/maths/cours-maths/science/',
    'https://www.devoirat.net/maths/cours-maths/sciences/',
    'https://www.devoirat.net/maths/devoirs-maths/2ème-trimestre-3/',
    'https://www.devoirat.net/maths/devoirs-maths/bac-info/',
    'https://www.devoirat.net/maths/devoirs-maths/bac-math/',
    'https://www.devoirat.net/maths/devoirs-maths/bac-sciences-exp/',
    'https://www.devoirat.net/maths/devoirs-maths/maths/',
    'https://www.devoirat.net/maths/devoirs-maths/sciences-1/',
    'https://www.devoirat.net/maths/séries-maths/1ère-année/',
    'https://www.devoirat.net/maths/séries-maths/2013-2014-2015/',
    'https://www.devoirat.net/maths/séries-maths/2015-2016/',
    'https://www.devoirat.net/maths/séries-maths/2018-2019-2020-1/',
    'https://www.devoirat.net/maths/séries-maths/bac-info/',
    'https://www.devoirat.net/maths/séries-maths/eco-services/',
    'https://www.devoirat.net/maths/séries-maths/info/',
    'https://www.devoirat.net/maths/séries-maths/sc-exp/',
    'https://www.devoirat.net/maths/séries-maths/sciences/',
    'https://www.devoirat.net/maths/séries-maths/technique/',
    'https://www.devoirat.net/pensée-islamique/devoirs-pensée-islamique/3ème-année/',
    'https://www.devoirat.net/physique/cours-physique-chimie/4ème-année-bac/',
    'https://www.devoirat.net/physique/devoirs-physique/1ère-année/',
    'https://www.devoirat.net/physique/devoirs-physique/2ème-trimestre/',
    'https://www.devoirat.net/physique/devoirs-physique/3ème-trimestre-1/',
    'https://www.devoirat.net/physique/devoirs-physique/bac-technique/',
    'https://www.devoirat.net/physique/devoirs-physique/sciences-exp/',
    'https://www.devoirat.net/physique/séries-physique-chimie/1ère-année/',
    'https://www.devoirat.net/physique/séries-physique-chimie/2014-2015/',
    'https://www.devoirat.net/physique/séries-physique-chimie/2017-2018/',
    'https://www.devoirat.net/physique/séries-physique-chimie/2ème-année/',
    'https://www.devoirat.net/physique/séries-physique-chimie/3ème-année/',
    'https://www.devoirat.net/physique/séries-physique-chimie/4ème-année-bac/',
    'https://www.devoirat.net/sciences-svt/séries-sciences-svt/1ère-année/',
    'https://www.devoirat.net/sciences-svt/séries-sciences-svt/4ème-année-bac/',
    'https://www.devoirat.net/technologie/cours-technologie/2ème-année/',
    'https://www.devoirat.net/technologie/cours-technologie/3ème-année/',
    'https://www.devoirat.net/technologie/cours-technologie/4ème-année-bac/',
    'https://www.devoirat.net/technologie/devoirs-technologie/1ère-année/',
    'https://www.devoirat.net/technologie/devoirs-technologie/3ème-année/',
    'https://www.devoirat.net/technologie/séries-technologie/1ère-année/',
    'https://www.devoirat.net/économie-gestion-1/devoirs-economie-gestion/2ème-année/',
    'https://www.devoirat.net/économie-gestion-1/séries-economie-gestion-1/3ème-economie-gestion/',
]

def get_subject(url):
    try:
        url = url[len('https://www.devoirat.net/'):]
        subject = url[:url.index('/')]
        if subject[-2:] == '-1': subject = subject[:-2]

        return subject
    except Exception as e:
        return None


def get_category(url):
    try:
        categories = ['devoirs', 'cours', 'séries']
        url = url[len('https://www.devoirat.net/'):]

        for category in categories:
            if category in url:
                return category

    except Exception as e:
        pass

    return None


def get_level(url):
    try:
        levels = ['1ère', '2ème', '3ème', 'bac']
        url = url[len('https://www.devoirat.net/'):]

        for level in levels:
            if level in url:
                return level

    except Exception as e:
        pass

    return None


# d = {}
# for url in URLS:
#     level = get_level(url)
#     d[level] = d.get(level, None) + 1 if d.get(level, None) is not None else 1

# for i, j in d.items():
#     print(i, j)