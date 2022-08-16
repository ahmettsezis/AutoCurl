from urllib import response
import requests

url ="https://haberler.hacettepe.edu.tr/"

req = requests.get(url)
responsedata = req.text

print(responsedata)


if (responsedata.find('<div class="haber_card_baslik">') != -1):
    indexofresponsedata = responsedata.find('<div class="haber_card_baslik">')
    print("BULUNDU")
    print(indexofresponsedata)

    x = slice(indexofresponsedata,-300)
    slicedresponsedata = responsedata[x]
    slicedresponsedataindex = slicedresponsedata.find('</div>')

    y = slice(31,slicedresponsedataindex)
    slicedresponsedata = slicedresponsedata[y]
    
    print(slicedresponsedata)


else:
    print("maalesef bulunamadi")





