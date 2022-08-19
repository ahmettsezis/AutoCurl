import boto3
from urllib import response
import requests
import time


url ="https://www.webtekno.com/haber" # url değişkenine değer atanıyor 
req = requests.get(url)
req.encoding = req.apparent_encoding  
responsedata = req.text # responsedata değişkenine req.text içeriği atanıyor 

# Eğer responsedata değişkeninde <div class="haber_card_baslik"> stringini bulursan:
if (responsedata.find('class="content-timeline__link clearfix" title="') != -1): 
    indexofresponsedata = responsedata.find('class="content-timeline__link clearfix" title="') # <div class="haber_card_baslik"> stringinin başlangıç indexini indexofresponsedata değişkenine aktar

    x = slice(indexofresponsedata,-200) # slice objesi oluştur
    slicedresponsedata = responsedata[x] # responsedata değişkeni içeriğini slice objesi olan x ile böl ve slicedresponsedata değişkenine aktar
    slicedresponsedataindex = slicedresponsedata.find('">') # bölünmüş içerikte </div> stringini ara ve indexini slicedresponsedataindex değişkenine aktar

    y = slice(47,slicedresponsedataindex) # slice objesi oluştur (31'in sebebi <div class="haber_card_baslik"> stringini silmek)
    slicedresponsedata = slicedresponsedata[y] # slicedresponsedata değişkenine div gibi html kodlarından temizlenmiş div içeriği datayı aktar

    unixtime = time.time() # unixtime
    nowString = str(unixtime) # unixtime'ı stringe çevir ve nowstring değişkenine aktar

    dynamodb = boto3.resource('dynamodb') # boto3 resource
    table = dynamodb.Table('News') # dynamodb tablosu seç
    response = table.scan() # tabloyu tara ve response içine aktar
    data = response['Items'] # response'un items kısmını data değişkenine aktar

    while 'LastEvaluateKey' in response: 
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])  

    counter = 0 # sayaç değişkeni tanımla
    lastBIGGESTpartitionkey = 0.0 # en büyük unixtime'ı atamak için kullanılacak değişken

    for item in data: # datadaki her item için
        lastpartitionkey = float(item['partitionKey']) # datadaki partition kısmını floata çevirip, lastpartition değişkenine aktar

        if  lastpartitionkey > lastBIGGESTpartitionkey: # lastpartitionkey lastBIGGESTpartitionkey'den büyük ise:
            lastBIGGESTpartitionkey = lastpartitionkey # lastpartitionkey değerini lastBIGGESTpartitionkey' aktar

    for item in data: # datadaki her item için
        if item['partitionKey'] == str(lastBIGGESTpartitionkey): # item'ın partitionkey değeri lastBIGGESTpartitionkey'in stringe çevirilmiş haliyle aynı ise:
            selectedTitle = item['Name'] # selectedTitle değişkenine item'ın Name değerinim aktar

    if selectedTitle != slicedresponsedata: # selectedTitle'ın değeri slicedresponsedata ile aynı değilse: (yani urlden son çektiğim verinin işlenmiş hali, en son çektiğim ve işlenip db'ye yazılmış verim ile aynı değilse)
        response = table.put_item( # dynamodb tabloya ekle
        Item = { 
            'partitionKey': nowString, # partitionKey kısmına UNIX zamanın stringe çevrilmiş hali olan nowString değerini aktar
            'Name': slicedresponsedata, # Name kısmına slicedresponse data yani url den çekip işlediğim veriyi aktar
                }
        )
        requests.post('https://api.telegram.org/bot5754899324:AAFQ1q5lHQgAiVPsN9-qZpwgzuG16uVr8_k/sendMessage', json={'chat_id': -1001627563032, 'text': 'BOTUN ROTASI WEBTEKNO HABERLER SAYFASINA ÇEVRİLDİ'}) # telegram botuna söyle de yeni datayı paylaşsın
    
else:
    print("maalesef bulunamadi") # URL'de aranan kısım yok
