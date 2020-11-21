URLS = [
    'https://www.devoir.tn/secondaire/4-ème-années/Sciences-de-l’informatique/Bases-de-données/Devoirs/devoir-de-contrôle-n°3.html',
]

def get_subject(url):
    try:
        url = url[len('https://www.devoir.tn/'):]
        subject = url.split('/')[3]

        return subject
    except Exception as e:
        return None


def get_category(url):
    try:
        categories = ['devoirs', 'cours', 'séries']
        categories_ar = ['فــــروض', 'دروس', 'تمارين']
        url = url[len('https://www.devoir.tn/'):]

        for category in categories:
            if category in url.lower():
                return category

        # Search for arabic categories but return the convenient english category
        for i in range(len(categories_ar)):
            if categories_ar[i] in url.lower():
                return categories[i]

    except Exception as e:
        pass

    return None


def get_level(url):
    try:
        levels = ['7ème', '8ème', '9ème', '1ère', '2ème', '3ème', '4ème', 'bac']
        url = url[len('https://www.devoir.tn/'):]

        for level in levels:
            if level in url.lower().replace('-', ''):
                if level == levels[-2]: return levels[-1]
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