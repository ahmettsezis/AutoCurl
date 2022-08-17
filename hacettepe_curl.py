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
    requests.post('https://api.telegram.org/bot5754899324:AAFQ1q5lHQgAiVPsN9-qZpwgzuG16uVr8_k/sendMessage', json={'chat_id': -1001627563032, 'text': slicedresponsedata})


else:
    print("maalesef bulunamadi")





