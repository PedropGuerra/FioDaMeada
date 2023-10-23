backlog
- fazer estatísticas públicas para os usuários compararem
- fazer com que o bot responda essas estatísticas para o usuário
- botão de compartilhar os resultados vs o global para que os usuários possam trocar com seus amigos e parentes
- receber os resultados do usuário todo mês/semana através do e-mail (relembrar usuário, inclusive)

problemas encontrados
- [ERROR] FakeNews não estão sendo criadas
- [TECNICAL] Remover bloqueio de scraping por data (fazer com que varra todos os dias)
- [DETAIL] Adicionar reconhecimento de qualquer fala e subir hub de opções (Henrique)
- [DETAIL] Retirar as mensagens "/report" e "/stop", pois não fazem nada... (Henrique)
- [DETAIL] Arrumar mensagens para que condizam com o dia "Olá, hoje é quarta..." (Henrique)
- [DETAIL] Adicionar um espaço entre o Autor e a Notícia (Henrique)

problemas resolvidos
- [BUG] SQL precisa liberar IP específico e GAE é dinâmico
    - Alocar uma rede privada Google Cloud
    - Implementar uma nova tentativa (ip interno e ip externo)

- [ERROR] CRON Jobs estão com falha
    - Não foi atualizado a requisição HTTP



soluções previstas