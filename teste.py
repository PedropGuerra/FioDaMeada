from SQL.sql_fiodameada import SendPulse_Flows


SendPulse_Flows().insert("124", "TESTE", "2023-08-23")
SendPulse_Flows().delete("124/TESTE")
instancia = SendPulse_Flows()

SendPulse_Flows().insert()

resultado = instancia.confirm(ID_FLOW_DB="3")

print(resultado)
