from SCRIPTS.integracao import Auth_SendPulse


API = Auth_SendPulse()
preferencias = API.get_preferencias("6500e99d564ffa8cf10d994f")

print(preferencias["data"]["tags"])


# print(API.get_preferencias("6500e99d564ffa8cf10d994f"))
