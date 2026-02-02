from azure.identity import ClientSecretCredential

tenant_id = "c2300418-fe50-4604-9e83-4dcf643ec7b6"
client_id = "f568d40f-b2d5-42cf-b023-982c4d3c48a4"
client_secret = "kNd8Q~4~4Kn674ps_zUNP~Xr2Vl2npGXsAu39bGx"

credential = ClientSecretCredential(tenant_id, client_id, client_secret)
token = credential.get_token("https://ai.azure.com/.default")

print("Token:", token.token[:50], "...")
print("Expires:", token.expires_on)

