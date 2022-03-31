def get_country_image(country_name):
    if country_name not in get_country_map().keys():
        return "https://flagpedia.net/data/flags/w702/unknown.png"
    image_name = get_country_map()[country_name]
    return "https://flagpedia.net/data/flags/w702/" + image_name + ".png"


def get_country_map():
    table = {"China": "cn", "Japan": "jp", "Indonesia": "id", "Denmark": "dk", "Malaysia": "my",
             "Taiwan": "tw", "Thailand": "th", "India": "in", "Singapore": "sg",
             "U.S.A.": "us", "Sweden": "se", "England": "gb-eng", "Netherlands": "nl",
             "Russia": "ru", "Korea": "kr", "South Korea": "kr", "Canada": "ca", "Germany": "de", "Australia": "au",
             "Bulgaria": "bg", "Ukraine": "ua", "Finland": "fi", "Belarus": "by", "Cyprus": "cy",
             "Austria": "at", "Poland": "pl", "Scotland": "gb-sct", "Hong Kong": "hk",
             "Wales": "gb-wls", "Zealand": "nz", "Mexico": "mx", "Norway": "no", "France": "fr",
             "Switzerland": "ch", "Hungary": "hu", "Ireland": "ie", "Mauritius": "mu", "Tobago": "tt",
             "Philippines": "ph", "Slovenia": "si", "Uganda": "ug", "Republic": "cz", "Spain": "es",
             "Italy": "it", "Peru": "pe", "Iceland": "is", "Portugal": "pt", "Jamaica": "jm",
             "Belgium": "be", "Jersey": "je", "Vietnam": "vn", "Macau": "mo", "Africa": "za",
             "Greece": "gr", "Lanka": "lk", "Lithuania": "lt", "Slovakia": "sk", "Nigeria": "ng",
             "Egypt": "eg", "Turkey": "tr", "Estonia": "ee", "Israel": "il", "Brazil": "br",
             "Guatemala": "gt", "Iran": "ir", "Myanmar": "mm", "Sri Lanka": "lk",
             "Brunei Darussalem": "bn", "Chinese Taipei": "tw", "-": "unknown"}
    return table


def correct_country(country):
    if country == 'Taipei':
        return "Taiwan"
    if country == 'Kong':
        return "Hong Kong"
    return country
