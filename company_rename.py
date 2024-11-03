def rename_company(value):
    if value in ['YODY', 'YGG','YOKIDS']:
        return 'YODY'
    elif value in ['GREENSPEED_GS', 'GREENSPEED_HN','GREENSPEED_HGX']:
        return 'GREENSPEED'
    elif value in ['SHYNHBEAUTY', 'SHYNHHOUSE']:
        return 'SHYNHGROUP'
    elif value in ['PHAMNGUYEN']:
        return 'PHAMNGUYEN'
    elif value in ['TDECO','TDP','TDHY']:
        return 'TDP'
    elif value in ['GDT']:
        return 'GODUCTHANH'
    elif value in ['TLC']:
        return 'TLC'
    elif value in ['AGR']:
        return 'AGR'
    elif value in ['HASECA']:
        return 'HASECA'
    elif value in ['VUANEM']:
        return 'VUANEM'
    elif value in ['GRGR']:
        return 'GRGR'
    elif value in ['MTP']:
        return 'MTP'
    elif value in ['TWEDU_VHSG']:
        return 'TWEDU'
    elif value in ['NANO']:
        return 'NANO'
    else:
        return 'unkown'