backlog
- fazer estatísticas públicas para os usuários compararem
- fazer com que o bot responda essas estatísticas para o usuário
- botão de compartilhar os resultados vs o global para que os usuários possam trocar com seus amigos e parentes
- receber os resultados do usuário todo mês/semana através do e-mail (relembrar usuário, inclusive)

problemas encontrados
- [DETAIL] Adicionar reconhecimento de qualquer fala e subir hub de opções (Henrique)
- [DETAIL] Retirar as mensagens "/report" e "/stop", pois não fazem nada... (Henrique)
- [DETAIL] Arrumar mensagens para que condizam com o dia "Olá, hoje é quarta..." (Henrique)
- [DETAIL] Adicionar um espaço entre o Autor e a Notícia (Henrique)

problemas resolvidos
- [ERROR] SQL precisa liberar IP específico e GAE é dinâmico
    - Alocar uma rede privada Google Cloud
    - Implementar uma nova tentativa (ip interno e ip externo)

- [ERROR] CRON Jobs estão com falha
    - Não foi atualizado a requisição HTTP

- [ERROR] Tags HTML no Script não estavam sendo lidas como dicionário
    - Alteração do desserializador para reconhecer

- [BUG] FakeNews não estão sendo criadas
    - A aleatorizacao gerava uma lista de apenas um elemento
    - Retirei a lista 