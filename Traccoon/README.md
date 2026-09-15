# AutoTrans

Aplicacao web de estudos para a prova teorica de direcao (CNH), no estilo
Duolingo: o aluno escolhe uma categoria, estuda o material e faz simulados
com questoes de multipla escolha.

Projeto escolar em Flask (API) + HTML/CSS/JS puro (frontend), com
arquitetura Controller -> Service -> Model/Repository -> Banco de Dados.

---

## Funcionalidades Implementadas

1. Cadastro, login e autenticacao de alunos, com senha protegida por hash
   e token de acesso
2. Cadastro de categorias, questoes e alternativas de simulado (banco de
   questoes)
3. Cadastro de materiais de estudo, organizados por categoria
4. Geracao de simulados com correcao automatica, calculando a nota do
   aluno
5. Edicao e exclusao de dados do usuario
6. Edicao e exclusao de categorias, questoes e alternativas
7. Edicao e exclusao de materiais de estudo
8. Edicao do proprio perfil pelo usuario logado (PUT /auth/me)
9. Consulta do historico de simulados e estatisticas de evolucao (media,
   melhor e pior nota), usando um Repository para a consulta complexa
   (join Simulado + Resultado)
10. Garantia de que cada aluno so acessa os proprios simulados: ao abrir
    os detalhes de um simulado que nao seja seu (ex.: id manipulado), o
    sistema exibe uma tela de "Acesso negado" em vez dos dados de outro
    usuario (GET /simulados/<id> retorna 403 e o frontend mostra essa
    tela dedicada)
11. Paginacao nas listagens de administracao (usuarios, categorias,
    questoes, materiais, alternativas), via `?pagina=&por_pagina=`
12. Notificacoes toast no frontend para sucesso/erro/aviso, incluindo
    aviso automatico de falha de conexao com o servidor e de sessao
    expirada
13. Testes automatizados (pytest) cobrindo as regras de negocio dos
    services, rodando contra um banco SQLite em memoria
14. Ambiente com Docker (backend + frontend) via `docker-compose.yml`,
    pronto pra rodar em qualquer maquina do grupo sem instalar nada além
    do Docker

Cada funcionalidade acima esta implementada de ponta a ponta: Interface
-> API Flask -> Controller -> Service -> Model/Repository -> Banco de
Dados.

---

## Tecnologias

- Python 3 + Flask - API REST (so jsonify, sem Jinja/render_template)
- Flask-SQLAlchemy - ORM (banco SQLite)
- Flask-CORS - libera o frontend (outra origem) a chamar a API
- Werkzeug (werkzeug.security) - hash de senha
- itsdangerous - geracao e validacao do token de autenticacao
- HTML / CSS / JavaScript puro - frontend estatico, consome a API via fetch()

---

## Arquitetura

O backend e o frontend sao duas coisas separadas que rodam de forma
independente. O backend nao serve HTML nenhum: so devolve JSON. O
frontend e um conjunto de arquivos estaticos que qualquer navegador abre
direto, e que fala com o backend via fetch().

```
Backend (Flask, porta 5000)  <----  fetch()  ---->  Frontend (arquivos estaticos)
        API JSON                                     HTML + CSS + JS puro
```

### Padrao das camadas (backend)

```
Controller  ->  Service  ->  Repository  ->  Banco de dados
 (rota,         (regra de     Toda consulta e toda persistencia
  jsonify)       negocio,     (criar, listar, paginar, buscar_por_id,
                 validacao)   atualizar, deletar) de Usuario, Categoria,
                              Material, Questao e Alternativa passa por
                              um Repository dedicado da entidade.
```

Regras (atualizadas — ver nota historica abaixo):
- O Service nunca acessa `db.session` ou `Model.query` diretamente. Ele
  sempre chama um metodo do Repository da entidade
  (`UsuarioRepository`, `CategoriaRepository`, `MaterialRepository`,
  `QuestaoRepository`, `AlternativaRepository`).
- O Model guarda so a regra de campo (`atualizar(...)`, que so decide o
  que muda em memoria) e a regra de dominio de fato (`definir_senha`,
  `verificar_senha`, `alternativa_correta`, `to_dict`) — nunca `db.session`.
- `Simulado`, `ItemSimulado` e `Resultado` continuam Active Record
  (`.salvar()` direto no Model): o fluxo de "iniciar/responder/finalizar
  simulado" nao foi migrado pra Repository, so o CRUD administrativo das
  5 entidades acima.
- `HistoricoSimuladoRepository` continua existindo do mesmo jeito de
  antes, para a consulta especial que junta Simulado + Resultado.

> **Nota historica / ponto de atencao:** a versao original deste projeto
> usava Repository *so* para consultas especiais (como o historico),
> deixando o CRUD simples como Active Record na propria Model — essa
> distincao chegou a ser documentada aqui no README. Os Repositories de
> Usuario/Categoria/Material/Questao/Alternativa foram adicionados depois,
> a pedido, pra cobrir CRUD simples tambem, o que muda essa regra original.
> Se o enunciado do trabalho pede especificamente essa distincao (Model =
> CRUD simples, Repository = consulta complexa), vale conferir com o
> professor antes de entregar — pode fazer sentido reverter os
> repositories de CRUD simples e manter so o `HistoricoSimuladoRepository`.

---

## Autenticacao

O login e real: senha com hash (nunca guardada em texto puro) e token de
autenticacao.

Como funciona:

1. `POST /auth/registro` (nome, email, senha) cria o usuario com a senha
   ja criptografada (werkzeug.security.generate_password_hash) e devolve
   um token.
2. `POST /auth/login` (email, senha) confere a senha
   (check_password_hash) e devolve o mesmo tipo de token.
3. O frontend guarda esse token no localStorage do navegador e manda ele
   no cabecalho `Authorization: Bearer <token>` em toda chamada seguinte
   (isso ja e feito automaticamente pelo js/api.js).
4. Rotas protegidas (simulado, historico, edicao de perfil) usam o
   decorator `@login_obrigatorio` no backend: sem um token valido, a API
   responde 401 Unauthorized.
5. Cada simulado so pode ser visto/finalizado pelo proprio usuario dono
   dele - se o token for de outro usuario, a API responde 403 Forbidden.
6. `PUT /auth/me` deixa o usuario logado editar os proprios dados (nome,
   email, senha) - o id vem sempre do token, nunca da URL ou do corpo,
   entao ninguem consegue editar a conta de outra pessoa por essa rota.

Por que token em vez de cookie/sessao do Flask: o frontend roda em uma
origem separada do backend (Live Server em uma porta, API em outra), e
cookies entre origens diferentes em localhost sao inconsistentes entre
navegadores.

Limitacao conhecida: as telas de administracao (Gerir Usuarios, Gerir
Categorias etc.) ainda nao exigem login - qualquer pessoa com acesso ao
frontend consegue abri-las. Isso e proposital por enquanto (nao existe
ainda um conceito de "administrador" separado de "aluno").

---

## Estrutura do projeto

```
AutoTrans/
|-- backend/
|   |-- app.py                       -> cria a API Flask + CORS (sem Jinja)
|   |-- auth_utils.py                -> geracao/validacao de token, decorators login_obrigatorio / admin_obrigatorio
|   |-- seed_questoes_reais.py       -> popula categorias/questoes/alternativas reais
|   |-- seed_materiais_reais.py      -> popula materiais de estudo (com links oficiais)
|   |-- requirements.txt
|   |-- Dockerfile
|   |-- .dockerignore
|   |-- controllers/                 -> rotas (Blueprints), so devolvem JSON
|   |   |-- auth_controller.py            -> registro, login, logout, me (GET/PUT)
|   |   |-- usuario_controller.py         -> so admin; aceita ?pagina=&por_pagina=
|   |   |-- categoria_controller.py       -> GET aceita ?pagina=&por_pagina=
|   |   |-- questao_controller.py         -> GET aceita ?categoria_id= ou ?pagina=&por_pagina=
|   |   |-- alternativa_controller.py     -> GET aceita ?questao_id= ou ?pagina=&por_pagina=
|   |   |-- material_controller.py        -> GET aceita ?categoria_id= ou ?pagina=&por_pagina=
|   |   `-- simulado_controller.py        -> inclui /simulados/historico
|   |-- models/                      -> regra de campo + regra de dominio (sem tocar no banco)
|   |   |-- base.py                  -> ModeloBase (so o id)
|   |   |-- usuario.py               -> inclui senha_hash, definir_senha(), verificar_senha()
|   |   |-- categoria.py, material.py, questao.py,
|   |   |-- alternativa.py, simulado.py, item_simulado.py, resultado.py
|   |-- services/                    -> 1 pasta por entidade, 1 classe por operacao
|   |   |-- auth/  usuario/  categorias/  questoes/  alternativas/  materiais/
|   |   `-- simulados/  (inclui consultar_historico_service.py)
|   |-- repositories/                -> toda consulta e persistencia (ver nota no topo)
|   |   |-- usuario_repository.py, categoria_repository.py, material_repository.py,
|   |   |-- questao_repository.py, alternativa_repository.py
|   |   `-- historico_simulado_repository.py   -> consulta especial (join + estatisticas)
|   `-- tests/                       -> testes automatizados (pytest) das regras de negocio
|       |-- conftest.py                   -> fixtures (app, app_context, client) com banco em memoria
|       |-- test_auth_service.py, test_usuario_service.py, test_categoria_service.py,
|       `-- test_questao_service.py, test_material_service.py, test_alternativa_service.py,
|           test_simulado_service.py
|-- frontend/
|   |-- index.html                   -> tela de boas-vindas / onboarding / login / cadastro
|   |-- Dockerfile
|   |-- css/style.css
|   |-- js/
|   |   |-- api.js                    -> configuracao central da API + fetch() + token + toast de erro de rede
|   |   |-- toast.js                  -> sistema global de notificacoes (sucesso/erro/aviso)
|   |   |-- paginacao.js              -> helper compartilhado pelos admin_*.js (botoes anterior/proxima)
|   |   |-- script.js                 -> navegacao entre telas (SPA), modo escuro
|   |   |-- auth.js                   -> cadastro/login reais
|   |   |-- painel.js                 -> trilhas + simulado/quiz + historico (dados reais da API)
|   |   |-- materiais.js
|   |   `-- admin_*.js                -> 1 arquivo por CRUD de administracao (com paginacao)
|   `-- paginas/
|       |-- painel.html               -> painel principal (trilhas, quiz, perfil, historico...)
|       |-- materiais.html
|       `-- admin_usuarios.html, admin_categorias.html, admin_questoes.html,
|           admin_alternativas.html, admin_materiais.html
|-- docker-compose.yml
|-- requirements.txt
`-- README.md
```

---

## Como rodar

### 1. Backend (API)

```bash
git clone https://github.com/Pelissonn/AutoTrans.git
cd AutoTrans
pip install -r requirements.txt
cd backend
python app.py
```

A API sobe em http://127.0.0.1:5000. Teste abrindo esse link no navegador
- deve aparecer um JSON com a lista de rotas disponiveis.

Importante: se voce ja tinha um banco criado antes de uma mudanca no
schema (novo campo, nova tabela), apague `backend/autotrans.db` antes de
rodar de novo - o SQLite nao adiciona colunas automaticamente.

### 2. Popular o banco com conteudo real

O banco comeca vazio. Rode os dois scripts abaixo (nessa ordem) para
cadastrar categorias, questoes, alternativas e materiais de estudo reais:

```bash
cd backend
python seed_questoes_reais.py
python seed_materiais_reais.py
```

Rodar os scripts de novo nao duplica nada - eles pulam o que ja existe.

### 3. Administrador

O primeiro usuario que se cadastrar em `/auth/registro` (ou pela tela de
cadastro do site) vira administrador automaticamente. So administradores
podem cadastrar/editar/apagar categorias, questoes, alternativas,
materiais e outros usuarios - cadastre-se primeiro com sua propria conta
antes de pedir para outras pessoas se cadastrarem.

### 3. Frontend (arquivos estaticos)

O frontend nao precisa do Flask para rodar - e so abrir os arquivos .html
da pasta frontend/ no navegador. Recomendado usar a extensao Live Server
do VS Code:

1. Clique com o botao direito em frontend/index.html
2. Escolha "Open with Live Server"
3. O navegador abre em um endereco proprio (ex.: http://127.0.0.1:5500),
   diferente da porta do backend

Importante: o backend precisa estar rodando (passo 1) para o frontend
funcionar. O frontend nunca deve ser acessado pela porta 5000 - essa
porta e exclusiva da API.

Atencao (Live Server): se o VS Code estiver com a pasta inteira do
projeto aberta (backend + frontend juntos), o Live Server pode recarregar
a pagina sozinho toda vez que o arquivo `backend/autotrans.db` mudar. O
arquivo `.vscode/settings.json` do projeto ja configura o Live Server
para ignorar a pasta `backend/` - reabra o VS Code depois de clonar para
essa configuracao valer.

### 4. Criar uma conta e testar

1. Abra o frontend, clique em "Comecar a Aprender" e crie uma conta
2. Escolha uma trilha (categoria) e inicie um simulado
3. Responda todas as questoes e finalize - a nota aparece na tela de
   resultado, e o simulado passa a contar em "Meu Historico"

---

## Principais rotas da API

| Metodo | Rota | O que faz | Requer token? |
|---|---|---|---|
| POST | /auth/registro | Cria conta {nome, email, senha} | Nao |
| POST | /auth/login | Login {email, senha} | Nao |
| POST | /auth/logout | Encerra a sessao (no cliente) | Nao |
| GET | /auth/me | Dados do usuario logado | Sim |
| PUT | /auth/me | Edita os proprios dados {nome, email, senha} | Sim |
| GET | /usuarios/ | Lista usuarios (aceita ?pagina=&por_pagina=) | Sim (admin) |
| POST | /usuarios/ | Cadastra usuario (uso do admin) {nome, email, senha} | Sim (admin) |
| PUT / DELETE | /usuarios/<id> | Edita / remove usuario | Sim (admin) |
| GET / POST / PUT / DELETE | /categorias/ , /categorias/<id> | CRUD de categorias (GET aceita ?pagina=&por_pagina=) | Nao |
| GET / POST / PUT / DELETE | /questoes/ , /questoes/<id> | CRUD de questoes (aceita ?categoria_id= ou ?pagina=&por_pagina=) | Nao |
| GET / POST / PUT / DELETE | /alternativas/ , /alternativas/<id> | CRUD de alternativas (aceita ?questao_id= ou ?pagina=&por_pagina=) | Nao |
| GET / POST / PUT / DELETE | /materiais/ , /materiais/<id> | CRUD de materiais (aceita ?categoria_id= ou ?pagina=&por_pagina=) | Nao |
| POST | /simulados/ | Inicia simulado {categoria_id} (usuario vem do token) | Sim |
| GET | /simulados/<id> | Busca um simulado (so o dono ve; senao 403 "Acesso negado" na tela) | Sim |
| POST | /simulados/<id>/finalizar | Envia respostas e gera o resultado (so o dono) | Sim |
| GET | /simulados/historico | Lista simulados do usuario logado + estatisticas | Sim |

---

## Modelagem (models)

| Model | Campos principais | Observacao |
|---|---|---|
| Usuario | nome, email, senha_hash, data_criacao, data_atualizacao | senha nunca fica em texto puro |
| Categoria | nome, descricao | agrupa questoes e materiais |
| Material | categoria_id, conteudo, url | pertence a uma categoria |
| Questao | categoria_id, enunciado | pertence a uma categoria |
| Alternativa | questao_id, texto, correta | pertence a uma questao |
| Simulado | usuario_id, categoria_id, titulo, pontuacao_max, data_realizacao | criado ao iniciar um simulado |
| ItemSimulado | simulado_id, questao_id, alternativa_escolhida_id, acerto | uma linha por questao respondida |
| Resultado | simulado_id, nota, data_resultado | gerado ao finalizar o simulado |

Todos os models herdam de ModeloBase, que define apenas o campo id. Cada
model que precisa de data de criacao declara a propria coluna com o nome
que faz sentido para ele (ex.: Simulado.data_realizacao,
Resultado.data_resultado).

---

## Testes automatizados

Os testes cobrem as regras de negocio dos services (cadastro, edicao,
validacoes, calculo de nota do simulado, permissoes) rodando contra um
banco SQLite em memoria — nunca tocam no `autotrans.db` de verdade.

```bash
cd backend
pip install -r requirements.txt   # ja inclui o pytest
pytest
```

Para ver o nome de cada teste conforme roda: `pytest -v`.
Para rodar só um arquivo: `pytest tests/test_simulado_service.py`.

---

## Rodando com Docker

Sobe o backend (Flask, porta 5000) e o frontend (nginx servindo os
arquivos estaticos, porta 8080) com um comando so, sem precisar instalar
Python nem nada localmente — so o Docker:

```bash
docker compose up --build
```

Depois abra http://localhost:8080 no navegador. A API fica em
http://localhost:5000 (o `frontend/js/api.js` já aponta pra esse
endereço). O banco SQLite fica salvo em `backend/autotrans.db` no seu
computador (montado como volume), então os dados persistem mesmo se você
derrubar e subir os containers de novo.

Para popular o banco com conteúdo real (categorias/questões/materiais),
com os containers já rodando:

```bash
docker compose exec backend python seed_questoes_reais.py
docker compose exec backend python seed_materiais_reais.py
```

Para derrubar tudo: `docker compose down`.

---

## Proximos passos

- Papel de administrador separado do aluno, protegendo as telas de gestao
- Progresso real por categoria nas trilhas
- Ranking real com XP por usuario
- Justificativa da resposta apos a correcao automatica
- Conectar o quiz do painel principal ao banco de questoes real via API
