import translate

def cevir():
    metin = str(input("ÇEVİRMEK İSTEDİĞİNİZ KELİMEYİ GİRİNİZ: "))
    dil = int(input("Hangi dile çevirmek istiyorsunuz?\n1-Korece(ko)\n2-Özbekçe\n3-Japonca\n"))

    if dil == 1:
        translator = translate.Translator(from_lang="tr",to_lang="ko")
        translation = translator.translate(metin)
        print(translation)

    elif dil == 2:
        translator = translate.Translator(from_lang="tr",to_lang="uz")
        translation = translator.translate(metin)
        print(translation)

    elif dil == 3:
        translator = translate.Translator(from_lang="tr",to_lang="ja")
        translation = translator.translate(metin)
        print(translation)
cevir()
