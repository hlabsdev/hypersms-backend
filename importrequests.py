
import requests
import urllib

# text = "Bonsoir AIR.NET vos SMS nominatif on étés activées avec succès. Ils seront envoyés avec l'entete AIR.NET Merci pour votre confiance"
# params = {
#     "access-token": "OVW2qZYivGzZUH3Hh7JDaK0jaoFC6lPc",
#     "sender": "HLABS SMS",
#     "receiver": "22891025263",
#     "text": text
# }
# params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote, safe="", encoding="utf-8")

# response = requests.get("http://www.wassasms.com/wassasms/api/web/v3/sends", params=params)
# print(response.content)

# text = urllib.parse.quote(text, safe='')
# # text =urllib.request.pathname2url(text)
# urllib.parse.quote_from_bytes(bytes(text, encoding="utf-8"))
# print(f"Text ==> {text}")
# print(f"Text with utf-8 ==> {text.encode('utf-8')}")
# print(f"Text with bytes ==> {urllib.parse.quote_from_bytes(bytes(text, encoding='utf-8'))}")
# print(f"With Quote ==> {urllib.parse.quote(text)}")
# print(f"Parms with Quote ==> {urllib.parse.urlencode(params, quote_via=urllib.parse.quote)}")
# print(f"Parms with Quote_plus ==> {urllib.parse.urlencode(params, quote_via=urllib.parse.quote_plus)}")




# suc = b'{"state":"success"}'
# fai = urllib.parse.unquote(suc)
# print(suc)
# print(fai)
# # res=dict(fai)
# print(fai)
# print(res[1])

# print(suc[1].to_bytes(3, "big"))
# print(fai[1].to_bytes(3, "big"))



def sendSms(numero:str, text:str):
    wassa_key = "OVW2qZYivGzZUH3Hh7JDaK0jaoFC6lPc"
    wassa_url = "http://www.wassasms.com/wassasms/api/web/v3/sends"

    params = {
        "access-token": wassa_key,
        "sender": "OLUX PROMO",
        "receiver": numero,
        "text": text.encode("utf-8")
    }
    params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote, safe="", encoding="utf-8")

    response = requests.get(wassa_url, params=params)
    print(f"Response ==> {response.request}")
    print(f"Response decoded ==> {(response.json())}")
    print(f"Response status code ==> {response.status_code}")
    print(f"Response content ==> {response.content}")
    if response.status_code == 200:
        # if response.content[1].to == "success":
        return 1
        # elif response.content[1].__str__() == "failed " or response.content[1].__str__() == "error":
            #  return 2
        # else:
            # return 3
    return 2

list_contact = (
    22892403116,
    22890324373,
    22890635810,
    22892618778,
    22899522790,
    22890640111,
    22870085689,
    22899838665,
    22897232478,
    22890033671,
    22892406656,
    22898079595,
    22890856566,
    22890025887,
    22898517884,
    22891343054,
    22898887288,
    22892440658,
    22898086781,
    22890139802,
    22892650749,
    22899874787,
    22890529573,
    22893102050,
    22897243405,
    22896425090,
    22899938464,
    22899429496,
    22896257158,
    22898956418,
    22890334191,
    22879809508,
    22898122697,
    22897560994,
    22891494762,
    22899353528,
    22870803717,
    22892057282,
    22892746454,
    22898779202,
    22890761707,
    22896652929,
    22899122817,
    22899181848,
    22892451040,
    22897329358,
    22890314123,
    22892369764,
    22890947601,
    22891490372,
    22899890080,
    22892302545,
    22890512445,
    22892406656) 
text1 = "GRAND PROMO 33CL Pils, Lager, Djama a 800F seulement. Lieu: Grand Carrefour Agbavi. Date: Demain soir a partir de 20h. AVEC NOUS SAVOUREZ DE LA BONNE BIÈRE!"
text2 = "GRAND PROMO 33CL Pils, Lager, Djama a 800F seulement. Lieu: Grand Carrefour Agbavi. Date: Ce soir a partir de 20h. AVEC NOUS SAVOUREZ DE LA BONNE BIÈRE!"

for contact in list_contact:
    sendSms(numero=contact, text=text1)