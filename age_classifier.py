def classify_age(month):

    if month <= 12:
        return "0-1 Tahun"

    elif month <= 36:
        return "1-3 Tahun"

    else:
        return "Di Atas 3 Tahun"