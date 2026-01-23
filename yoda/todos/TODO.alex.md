# TODO-alex

Este arquivo e o TODO em Markdown (substituto temporario do `TODO.<dev>.yaml`) para esta implementacao do YODA Framework.
project/specs/ e a fonte da verdade do framework futuro; yoda/ e a implementacao em construcao.
Enquanto os scripts nao existem, usamos Markdown para TODOs e logs nesta meta-implementacao.
Leia REPO_INTENT.md para o contexto do repositorio.

## Backlog (ordem de execucao)

### alex-001 - Criar yoda/yoda.md (entrada do agente)
- Descricao: definir as instrucoes do agente YODA para este repositorio.
- Status: done
- Prioridade: 10
- Dependencias: nenhuma

### alex-002 - Formalizar template de issue (normal e lightweight)
- Descricao: garantir que os templates em yoda/templates/ estejam alinhados com as specs.
- Status: done
- Prioridade: 9
- Dependencias: alex-001

### alex-003 - Estrutura minima do YODA Framework
- Descricao: documentar a estrutura base do YODA (pastas e arquivos padrao).
- Status: done
- Prioridade: 8
- Dependencias: alex-001

### alex-004 - Definir comandos e scripts v1 (especificacao)
- Descricao: listar a interface dos scripts minimos (init.py, manutencao TODO, logs, resolucao de pendencia).
- Status: done
- Prioridade: 8
- Dependencias: alex-001

### alex-005 - Template de issue (regras e uso)
- Descricao: documentar como o agente deve criar e preencher issues a partir dos templates.
- Status: done
- Prioridade: 7
- Dependencias: alex-002

### alex-006 - Consolidar README.md e summary.md com esta implementacao
- Descricao: alinhar README e summary com o estado final das specs e do TODO.
- Status: done
- Prioridade: 6
- Dependencias: alex-001, alex-003

### alex-007 - Schema formal do `TODO.<dev>.yaml`
- Descricao: definir schema validavel do `TODO.<dev>.yaml` (tipos, obrigatorios, enums, constraints) com exemplos.
- Status: done
- Prioridade: 9
- Dependencias: nenhuma

### alex-008 - Schema formal do metadata da issue
- Descricao: definir schema do metadata de issue (front matter ou equivalente) com exemplos.
- Status: done
- Prioridade: 9
- Dependencias: nenhuma

### alex-009 - Contrato CLI dos scripts v1
- Descricao: definir interface CLI (args, outputs, exit codes, dry-run, erros).
- Status: done
- Prioridade: 8
- Dependencias: alex-004

### alex-010 - Regras deterministicas de ordenacao e selecao
- Descricao: consolidar regras de prioridade, ordem, pending e depends_on.
- Status: done
- Prioridade: 8
- Dependencias: alex-004

### alex-011 - Validacao e checks minimos
- Descricao: definir yoda validate e checks basicos para YAML/Markdown.
- Status: to-do
- Prioridade: 7
- Dependencias: alex-007, alex-008

### alex-012 - Versionamento e migracoes de schema
- Descricao: definir schema_version e politica de migracao.
- Status: to-do
- Prioridade: 7
- Dependencias: alex-007, alex-008

### alex-013 - Colaboracao multi-dev
- Descricao: regras de conflitos YAML, dependencias cruzadas e convencao de branches.
- Status: to-do
- Prioridade: 6
- Dependencias: alex-007

### alex-014 - Logs e resultados auditaveis
- Descricao: definir campos obrigatorios no log e referencias bidirecionais.
- Status: to-do
- Prioridade: 6
- Dependencias: alex-007

### alex-015 - Resolver decisoes em aberto do summary
- Descricao: desdobrado em alex-019..alex-025 para resolver cada decisao em aberto separadamente.
- Status: done
- Prioridade: 8
- Dependencias: nenhuma

### alex-016 - Alinhar entrada do agente com TODO no bootstrap
- Descricao: explicitar nas specs a regra de fallback para `TODO.<dev>.md` no bootstrap e a transicao para YAML.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-017 - Definir formato de logs no bootstrap vs framework
- Descricao: documentar nas specs a excecao de logs em Markdown no bootstrap e a regra canonica de YAML.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-018 - Definir politica de edicao de TODO sem scripts
- Descricao: definir a excecao para edicao manual de TODO no bootstrap, mantendo scripts como regra futura.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-019 - Definir politica de tooling (obrigatorio vs opcional)
- Descricao: definir se o tooling do YODA e mandatorio ou recomendado e registrar nas specs.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-020 - Definir audiencia e posicionamento oficial
- Descricao: decidir a audiencia primaria (solo, equipes, consultorias, SaaS) e refletir nas specs.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-021 - Definir entregaveis minimos por fase do YODA Flow
- Descricao: especificar artefatos minimos de Study, Document, Implement, Evaluate.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-022 - Definir campos adicionais do schema de metadados
- Descricao: decidir campos obrigatorios adicionais alem do baseline e atualizar as specs.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-023 - Definir limites de escopo (out-of-scope)
- Descricao: listar explicitamente o que o framework nao cobre (CI/CD, arquitetura, RH etc.).
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-024 - Definir politicas de stack profiles
- Descricao: decidir entre modelo generico unico vs perfis por stack e documentar.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-025 - Definir brand voice e terminologia
- Descricao: estabelecer tom e termos oficiais do framework nas docs.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

## Observacoes

- Cada item acima deve gerar um arquivo de issue em yoda/project/issues/.
- A partir da primeira issue, seguir o YODA Flow.
- Este TODO.md sera substituido por `TODO.<dev>.yaml` quando os scripts existirem.
