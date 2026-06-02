---
schema_version: '2.00'
status: done
title: Adicionar fluxo antecipado de Study e Document
description: Criar um fluxo alternativo ao YODA Flow para executar apenas o trabalho
  de Study e Document de uma issue, sem implementar nada, deixando a issue pronta
  para entrar posteriormente no YODA Flow diretamente em Implement.
priority: 5
extern_issue_file: ../extern_issues/github-006.json
created_at: '2026-06-01T17:52:26-03:00'
updated_at: '2026-06-01T18:30:53-03:00'
---

# yoda-0062 - Adicionar fluxo antecipado de Study e Document

## Summary
Criar o **YODA Prep Flow**, um fluxo operacional alternativo ao YODA Flow para
antecipar apenas as fases de Study e Document de uma issue. Esse fluxo deve
preparar uma issue especifica sem executar implementacao, manter a issue como
`to-do` e registrar no front matter que ela deve iniciar em Implement quando for
selecionada posteriormente pelo YODA Flow normal.

## Context
O YODA Flow atual segue a sequencia Study, Document, Implement e Evaluate. Em
alguns casos, a documentacao de uma issue precisa ser refinada antes do momento
de implementacao, mas entrar no Flow normal pode misturar preparacao documental
com execucao tecnica.

A issue externa GitHub #6 solicita um "Flow antecipado" que trate somente a
documentacao da issue, sem implementar nada. Depois desse preparo, o Flow normal
deve reconhecer que Study e Document ja foram feitos e deve iniciar em Implement.

## Objective
Definir e implementar `yoda/scripts/yoda_prep_flow.py` para executar o preparo
documental de uma issue especifica, independente da ordem de execucao e das
precedencias do backlog, persistindo `flow_prepared_until: document` para
retomada posterior diretamente em Implement no YODA Flow.

## Scope
- Adicionar o script `yoda/scripts/yoda_prep_flow.py`.
- Definir a entrada CLI principal como `--dev <slug> --issue <id>`.
- Permitir que o YODA Prep Flow atue sobre uma issue especifica,
  independente da ordem de selecao do backlog e das precedencias.
- Persistir o marcador opcional `flow_prepared_until: document` no front matter.
- Manter a issue preparada com `status: to-do`.
- Garantir que o YODA Flow reconheca `flow_prepared_until: document` e inicie a
  issue em `doing/implement` quando ela for selecionada.
- Atualizar `yoda/yoda.md` para mencionar o YODA Prep Flow, explicar
  minimamente o novo script e orientar o agente a chamar `--help` para obter o
  runbook completo.
- Adicionar testes para preparo, selecao normal e retomada em Implement.

## Out of scope
- Executar qualquer implementacao de produto dentro da issue preparada.
- Alterar a ordem padrao do YODA Flow para issues nao preparadas.
- Fazer o YODA Prep Flow obedecer precedencias do backlog para escolher issues.
- Migrar retroativamente issues historicas.
- Fechar ou atualizar automaticamente a issue externa no GitHub.

## Requirements
- `yoda_prep_flow.py` deve exigir `--dev` e `--issue`.
- `--issue` deve apontar para uma issue existente do mesmo dev.
- O script deve rejeitar issues `done`.
- O script deve operar independentemente de dependencias, prioridade e ordem
  seletiva do YODA Flow.
- O script deve emitir runbooks compactos para Study e Document, sem orientar
  Implement ou Evaluate.
- O script deve esperar autorizacao humana entre Study e Document, seguindo a
  mesma disciplina de uma etapa por chamada.
- Ao concluir Document, o script deve manter `status: to-do`, remover `phase` se
  existir, persistir `flow_prepared_until: document` e registrar linha no
  `## Flow log`.
- `flow_prepared_until` deve ser campo opcional; aceitar `study` como marco
  intermediario do Prep Flow e `document` como marco final. Quando ausente, o
  comportamento atual permanece inalterado.
- `yoda_flow_next.py` deve interpretar `status: to-do` +
  `flow_prepared_until: document` como entrada direta em `doing/implement`.
- A interface deve seguir os padroes atuais dos scripts YODA: `--dev`, saida
  markdown/json, `--dry-run` para mutacoes e help com Agent guidance.
- `yoda/yoda.md` deve conter uma secao curta do YODA Prep Flow, sem duplicar o
  runbook detalhado do script.
- A orientacao em `yoda/yoda.md` deve pedir explicitamente para executar
  `python3 yoda/scripts/yoda_prep_flow.py --help` antes de usar o fluxo.
- A mudanca de layout/schema deve ser classificada como `subtle`.

## Acceptance criteria
- [x] Existe `yoda/scripts/yoda_prep_flow.py` com `--dev`, `--issue`,
      `--format/json`, `--dry-run` e Agent guidance no `--help`.
- [x] O YODA Prep Flow retorna runbook claro para Study/Document sem orientar
      implementacao.
- [x] O YODA Prep Flow trabalha sobre a issue indicada por `--issue`, sem
      depender da ordem de selecao ou precedencias do backlog.
- [x] Ao concluir Document, a issue markdown permanece `to-do` e persiste
      `flow_prepared_until: document`.
- [x] `yoda_flow_next.py` inicia issues preparadas diretamente em
      `doing/implement`.
- [x] Issues que nao passaram pelo fluxo antecipado continuam seguindo Study ->
      Document -> Implement -> Evaluate.
- [x] `yoda/yoda.md` menciona `yoda_prep_flow.py` e orienta consultar
      `python3 yoda/scripts/yoda_prep_flow.py --help` para detalhes.
- [x] Testes cobrem o caminho antecipado, o caminho normal e o comportamento de
      `--dry-run` se houver mutacao.

## Entry points
- yoda/yoda.md
- yoda/scripts/yoda_prep_flow.py
- yoda/scripts/yoda_flow_next.py
- yoda/scripts/todo_update.py
- yoda/scripts/lib/issue_index.py
- yoda/scripts/lib/issue_metadata.py
- yoda/scripts/tests/test_yoda_prep_flow.py
- yoda/scripts/tests/test_yoda_flow_next.py
- yoda/project/extern_issues/github-006.json

## Implementation notes
Nome canonico do fluxo: **YODA Prep Flow**.

Script canonico: `yoda_prep_flow.py`.

Campo canonico: `flow_prepared_until`. Valores aceitos: `study` e `document`.

Semantica aprovada:

- `flow_prepared_until: document` significa que Study e Document ja foram
  executados no YODA Prep Flow.
- `flow_prepared_until: study` e usado somente como marco intermediario para
  permitir uma etapa por chamada antes de Document.
- A issue preparada continua `status: to-do`, porque ainda nao entrou no Flow de
  implementacao.
- Quando selecionada pelo YODA Flow normal, a transicao inicial deve ser
  `to-do -> doing/implement`.
- Campo ausente significa comportamento normal.
- Mudanca classificada como `subtle`, por ser campo opcional compativel com
  issues existentes.

Evitar inferencias por texto livre no corpo da issue. A retomada em Implement
deve depender exclusivamente do front matter validado.

## Tests
Adicionar ou atualizar testes em `yoda/scripts/tests/` para validar:

- `yoda_prep_flow.py --help` contem Agent guidance;
- `yoda_prep_flow.py --dev <slug> --issue <id>` inicia o preparo da issue
  indicada, mesmo que outra issue tenha maior prioridade;
- conclusao de Document persiste `flow_prepared_until: document` e mantem
  `status: to-do`;
- `yoda_flow_next.py` retoma issue preparada em `doing/implement`;
- preservacao do fluxo normal para issues nao preparadas;
- rejeicao de issue `done` no YODA Prep Flow;
- ausencia de transicao para Implement/Evaluate/Done no YODA Prep Flow;
- saida/runbook esperado para agente;
- comportamento sem escrita com `--dry-run`.

## Risks and edge cases
- O novo campo deve entrar na ordem canonica de metadados para evitar diffs
  instaveis.
- Dois fluxos capazes de alterar fase/status podem divergir se nao houver uma
  unica regra de transicao.
- Uma issue parcialmente preparada pode ficar ambigua se o fluxo for interrompido
  entre Study e Document.
- O Flow normal nao deve pular Study/Document por acidente em issues antigas ou
  em issues editadas manualmente sem marcador valido.
- Como o Prep Flow ignora precedencias, o playbook deve deixar claro que ele nao
  autoriza implementacao antecipada.
- A documentacao embarcada deve permanecer resumida; detalhes de execucao devem
  viver no `--help` do script para evitar drift entre manual e CLI.

## Result log
feat: add YODA Prep Flow

Implemented `yoda_prep_flow.py` for explicit issue Study/Document preparation without implementation. Added `flow_prepared_until` metadata support, integrated prepared issues into `yoda_flow_next.py` so `to-do` issues prepared through Document start at `doing/implement`, and documented the new flow in `yoda/yoda.md` with guidance to consult the script `--help`.

- **GitHub Issue** :   #006

- **Issue**: `yoda-0062`

- **Path**: `yoda/project/issues/yoda-0062-adicionar-fluxo-antecipado-de-study-e-document.md`

## Flow log
- 2026-06-01T17:52:26-03:00 issue_add created title=Adicionar fluxo antecipado de Study e Document; priority=5
- 2026-06-01T18:07:49-03:00 transition to-do->doing/study
- 2026-06-01T18:15:39-03:00 transition doing/study->doing/document | Study approved: new yoda_prep_flow.py, explicit flow_prepared_until field, subtle schema change, keep prepared issue to-do, canonical name YODA Prep Flow
- 2026-06-01T18:22:29-03:00 transition doing/document->doing/implement | Document approved: implement YODA Prep Flow script, flow_prepared_until marker, yoda_flow_next integration, yoda.md note, and tests
- 2026-06-01T18:29:36-03:00 transition doing/implement->doing/evaluate | Implement completed: added yoda_prep_flow.py, flow_prepared_until support, yoda_flow_next prepared issue handling, docs, and tests
- 2026-06-01T18:30:53-03:00 transition doing/evaluate->done | Evaluate approved: acceptance criteria checked, Result log filled, full script test suite passed
