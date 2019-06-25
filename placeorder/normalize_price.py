def normalize(symbol:str, price:float):
    if symbol == 'SPX' or symbol == 'RUT' or symbol == 'NDX':
        return round(price, 1)
    elif symbol == 'ES':
        return round(4*price, 0) /4
    else:
        return round(price, 2)
