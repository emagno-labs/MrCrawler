Pacote core.controllers.analyze
============================

Este pacote contem módulos para a análise e auditoria do site _alvo_.

Funcionalidades implementadas:

- [ ] Busca por códigos _Ajax_.
- [ ] Análise de cookies de sessão nas respostas _(responses)_.
- [ ] Busca por respostas sem corpo, o que pode indicar erros ou falhas de configuração _(blank body)_.
- [ ] _Click Jacking_: Busca cada página por possibilidades deste ataque. Mais informações no site da [OWASP](https://www.owasp.org/index.php/Clickjacking).
- [ ] Código mal formado.
- [ ] Domínio cruzado _(cross domain)_ para recursos _javascript_.
- [ ] Varredura de páginas de erro (podem conter informações sensíveis do servidor web ou do _framework_ de programação.
- [ ] _Form autocomplete_: Busca em cada página por campos com tipo senha _(password-type)_ e o recurso _autocomplete_ habilitado.
- [ ] Relacionar todos os e-mails encontrados (esta informação pode ser considerada sensível por servir de base para ataques de força bruta).
- [ ] Avaliação de comentários no código HTML (senhas, nomes de usuário e correção de _bugs_ são considerados informações sensíveis).
- [ ] Detecção se o recurso _(url)_ análisada requer autenticação.
- [ ] Busca por respostas _(reponses)_ contendo outra resposta ou requisição _(request)_ em seu corpo.
- [ ] Identificação da linguagem em que o site foi desenvolvido.
- [ ] Análise de _meta tags_.
- [ ] Busca por IPs privados.
- [ ] Busca por URLs que possuem parametros que armazenam o ID de sessão.
