import boto3
import requests
import time
import os
telegramlink = os.environ['telegramlink']
telegramchatid = os.environ['telegramchatid']
requesturl = os.environ['requesturl']
requestpart = os.environ['requestpart']
requestpartlink = os.environ['requestpartlink']

url = requesturl # url değişkenine değer atanıyor 
req = requests.get(url)
req.encoding = req.apparent_encoding  
responsedata = req.text # responsedata değişkenine req.text içeriği atanıyor

# Eğer responsedata değişkeninde <div class="haber_card_baslik"> stringini bulursan:
if (responsedata.find('') != -1):

    indexofresponsedata = responsedata.find(requestpartlink)
    x = slice(indexofresponsedata,-50) # slice objesi oluştur
    slicedresponsedatalink = responsedata[x] # responsedata değişkeni içeriğini slice objesi olan x ile böl ve slicedresponsedata değişkenine aktar
    slicedresponsedataindex = slicedresponsedatalink.find('onclick') # bölünmüş içerikte </div> stringini ara ve indexini slicedresponsedataindex değişkenine aktar
    y = slice(len(requestpartlink)+10,slicedresponsedataindex-2) # html kodunun başlangıç ve bitiş noktalarına kadar sil)
    slicedresponsedatalink = slicedresponsedatalink[y] # slicedresponsedata değişkenine div gibi html kodlarından temizlenmiş div içeriği datayı aktar

    indexofresponsedata = responsedata.find(requestpart) # <div class="haber_card_baslik"> stringinin başlangıç indexini indexofresponsedata değişkenine aktar
    x = slice(indexofresponsedata,-50) # slice objesi oluştur
    slicedresponsedata = responsedata[x] # responsedata değişkeni içeriğini slice objesi olan x ile böl ve slicedresponsedata değişkenine aktar
    slicedresponsedataindex = slicedresponsedata.find('">') # bölünmüş içerikte </div> stringini ara ve indexini slicedresponsedataindex değişkenine aktar
    y = slice(len(requestpart),slicedresponsedataindex) # html kodunun başlangıç ve bitiş noktalarına kadar sil)
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
    
    slicedresponsedata = slicedresponsedata.replace("&#039;", "'") 
    slicedresponsedata = slicedresponsedata.replace("&quot;", '"')

    if selectedTitle != slicedresponsedata: # selectedTitle'ın değeri slicedresponsedata ile aynı değilse: (yani urlden son çektiğim verinin işlenmiş hali, en son çektiğim ve işlenip db'ye yazılmış verim ile aynı değilse)
        response = table.put_item( # dynamodb tabloya ekle
        Item = { 
            'partitionKey': nowString, # partitionKey kısmına UNIX zamanın stringe çevrilmiş hali olan nowString değerini aktar
            'Name': slicedresponsedata, # Name kısmına slicedresponse data yani url den çekip işlediğim veriyi aktar
                }
        )
        requests.post(telegramlink, json={'chat_id': telegramchatid, 'text': slicedresponsedata + "\n" + "\n" + slicedresponsedatalink}) # telegram botuna söyle de yeni datayı paylaşsın
else:
    print("maalesef bulunamadi") # URL'de aranan kısım yok
