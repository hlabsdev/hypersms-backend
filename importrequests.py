
import requests
import urllib

text = "Bonsoir AIR.NET vos SMS nominatif on étés activées avec succès. Ils seront envoyés avec l'entete AIR.NET Merci pour votre confiance"
params = {
    "access-token": "OVW2qZYivGzZUH3Hh7JDaK0jaoFC6lPc",
    "sender": "HLABS SMS",
    "receiver": "22891025263",
    "text": text
}
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




suc = b'{"state":"success"}'
fai = urllib.parse.unquote(suc)
print(suc)
print(fai)
# res=dict(fai)
print(fai)
print(res[1])

# print(suc[1].to_bytes(3, "big"))
# print(fai[1].to_bytes(3, "big"))