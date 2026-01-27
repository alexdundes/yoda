# TODO-alex

Este arquivo e o TODO em Markdown (substituto temporario do `TODO.<dev>.yaml`) para esta implementacao do YODA Framework.
project/specs/ e a fonte da verdade do framework futuro; yoda/ e a implementacao em construcao.
Enquanto os scripts nao existem, usamos Markdown para TODOs e logs nesta meta-implementacao.
Leia REPO_INTENT.md para o contexto do repositorio.

## Backlog (ordem de execucao)

### alex-0001 - Criar yoda/yoda.md (entrada do agente)
- Descricao: definir as instrucoes do agente YODA para este repositorio.
- Status: done
- Prioridade: 10
- Dependencias: nenhuma

### alex-0002 - Formalizar template de issue (normal e lightweight)
- Descricao: garantir que os templates em yoda/templates/ estejam alinhados com as specs.
- Status: done
- Prioridade: 9
- Dependencias: alex-0001

### alex-0003 - Estrutura minima do YODA Framework
- Descricao: documentar a estrutura base do YODA (pastas e arquivos padrao).
- Status: done
- Prioridade: 8
- Dependencias: alex-0001

### alex-0004 - Definir comandos e scripts v1 (especificacao)
- Descricao: listar a interface dos scripts minimos (init.py, manutencao TODO, logs, resolucao de pendencia).
- Status: done
- Prioridade: 8
- Dependencias: alex-0001

### alex-0005 - Template de issue (regras e uso)
- Descricao: documentar como o agente deve criar e preencher issues a partir dos templates.
- Status: done
- Prioridade: 7
- Dependencias: alex-0002

### alex-0006 - Consolidar README.md e summary.md com esta implementacao
- Descricao: alinhar README e summary com o estado final das specs e do TODO.
- Status: done
- Prioridade: 6
- Dependencias: alex-0001, alex-0003

### alex-0007 - Schema formal do `TODO.<dev>.yaml`
- Descricao: definir schema validavel do `TODO.<dev>.yaml` (tipos, obrigatorios, enums, constraints) com exemplos.
- Status: done
- Prioridade: 9
- Dependencias: nenhuma

### alex-0008 - Schema formal do metadata da issue
- Descricao: definir schema do metadata de issue (front matter ou equivalente) com exemplos.
- Status: done
- Prioridade: 9
- Dependencias: nenhuma

### alex-0009 - Contrato CLI dos scripts v1
- Descricao: definir interface CLI (args, outputs, exit codes, dry-run, erros).
- Status: done
- Prioridade: 8
- Dependencias: alex-0004

### alex-0010 - Regras deterministicas de ordenacao e selecao
- Descricao: consolidar regras de prioridade, ordem, pending e depends_on.
- Status: done
- Prioridade: 8
- Dependencias: alex-0004

### alex-0011 - Validacao e checks minimos
- Descricao: definir yoda validate e checks basicos para YAML/Markdown.
- Status: done
- Prioridade: 7
- Dependencias: alex-0007, alex-0008

### alex-0012 - Versionamento e migracoes de schema
- Descricao: definir schema_version e politica de migracao.
- Status: done
- Prioridade: 7
- Dependencias: alex-0007, alex-0008

### alex-0013 - Colaboracao multi-dev
- Descricao: regras de conflitos YAML, dependencias cruzadas e convencao de branches.
- Status: done
- Prioridade: 6
- Dependencias: alex-0007

### alex-0014 - Logs e resultados auditaveis
- Descricao: definir campos obrigatorios no log e referencias bidirecionais.
- Status: done
- Prioridade: 6
- Dependencias: alex-0007

### alex-0015 - Resolver decisoes em aberto do summary
- Descricao: desdobrado em alex-0019..alex-0025 para resolver cada decisao em aberto separadamente.
- Status: done
- Prioridade: 8
- Dependencias: nenhuma

### alex-0016 - Alinhar entrada do agente com TODO no bootstrap
- Descricao: explicitar nas specs a regra de fallback para `TODO.<dev>.md` no bootstrap e a transicao para YAML.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-0017 - Definir formato de logs no bootstrap vs framework
- Descricao: documentar nas specs a excecao de logs em Markdown no bootstrap e a regra canonica de YAML.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-0018 - Definir politica de edicao de TODO sem scripts
- Descricao: definir a excecao para edicao manual de TODO no bootstrap, mantendo scripts como regra futura.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-0019 - Definir politica de tooling (obrigatorio vs opcional)
- Descricao: definir se o tooling do YODA e mandatorio ou recomendado e registrar nas specs.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-0020 - Definir audiencia e posicionamento oficial
- Descricao: decidir a audiencia primaria (solo, equipes, consultorias, SaaS) e refletir nas specs.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-0021 - Definir entregaveis minimos por fase do YODA Flow
- Descricao: especificar artefatos minimos de Study, Document, Implement, Evaluate.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-0022 - Definir campos adicionais do schema de metadados
- Descricao: decidir campos obrigatorios adicionais alem do baseline e atualizar as specs.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-0023 - Definir limites de escopo (out-of-scope)
- Descricao: listar explicitamente o que o framework nao cobre (CI/CD, arquitetura, RH etc.).
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-0024 - Definir politicas de stack profiles
- Descricao: decidir entre modelo generico unico vs perfis por stack e documentar.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-0025 - Definir brand voice e terminologia
- Descricao: estabelecer tom e termos oficiais do framework nas docs.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-0026 - Revisar yoda/yoda.md com foco no bootstrap
- Descricao: revisar e ajustar yoda/yoda.md para refletir as regras de bootstrap e evitar ambiguidades.
- Status: done
- Prioridade: 6
- Dependencias: nenhuma

### alex-0027 - Resolver ambiguidades de entrada e atualizacao de TODO
- Descricao: alinhar regras de fallback e edicao do TODO entre yoda/yoda.md e specs, removendo conflitos.
- Status: done
- Prioridade: 6
- Dependencias: nenhuma

### alex-0028 - Revisar README e summary com specs atuais
- Descricao: revisar README.md e project/specs/summary.md para garantir sincronizacao com project/specs e issues concluidas.
- Status: done
- Prioridade: 6
- Dependencias: nenhuma

### alex-0029 - Padronizar id canonico e naming de arquivos
- Descricao: alinhar id canonico com naming de issues e logs nas specs.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-0030 - Corrigir inconsistencias no Study do YODA Flow
- Descricao: ajustar texto do Study para remover ambiguidade sobre deliverables.
- Status: done
- Prioridade: 6
- Dependencias: nenhuma

### alex-0031 - Ajustar exemplos de issue templates para id canonico
- Descricao: atualizar exemplos de commit e paths no guia de templates.
- Status: done
- Prioridade: 5
- Dependencias: nenhuma

### alex-0032 - Explicitar path default do TODO nas specs
- Descricao: padronizar referencias a yoda/todos/TODO.<dev>.yaml e bootstrap.
- Status: done
- Prioridade: 6
- Dependencias: nenhuma

### alex-0033 - Revisar regra de timezone em conventions
- Descricao: ajustar MUST/SHOULD para timezone explicita e UTC/configuravel.
- Status: done
- Prioridade: 5
- Dependencias: nenhuma

### alex-0034 - Clarificar validacao vs comandos v1
- Descricao: explicitar se validacao e embutida ou via validate.py.
- Status: done
- Prioridade: 5
- Dependencias: nenhuma

### alex-0035 - Revisar bootstrap e meta-implementation nas specs
- Descricao: decidir como tratar bootstrap dentro de project/specs.
- Status: done
- Prioridade: 5
- Dependencias: nenhuma

### alex-0036 - Definir estrutura Python dos scripts YODA
- Descricao: criar spec base para estrutura, dependencias e organizacao dos scripts em yoda/scripts.
- Status: done
- Prioridade: 6
- Dependencias: nenhuma

### alex-0037 - Especificar script de inclusao de issue (issue_add.py)
- Descricao: especificar o script de inclusao de issues e criar a spec em project/specs/18-issue-add-script.md.
- Status: done
- Prioridade: 3
- Dependencias: alex-0036

### alex-0048 - Implementar script de inclusao de issue (issue_add.py)
- Descricao: implementar o issue_add.py conforme a spec project/specs/18-issue-add-script.md.
- Status: done
- Prioridade: 3
- Dependencias: alex-0037

### alex-0049 - Especificar script de log (log_add.py)
- Descricao: especificar o log_add.py e criar a spec em project/specs/19-log-add-script.md.
- Status: done
- Prioridade: 3
- Dependencias: alex-0014

### alex-0050 - Implementar script de log (log_add.py)
- Descricao: implementar o log_add.py conforme a spec project/specs/19-log-add-script.md.
- Status: done
- Prioridade: 3
- Dependencias: alex-0049

### alex-0038 - Corrigir links quebrados em project/specs
- Descricao: padronizar links para repo-root (ex.: /yoda/..., /AGENTS.md, /gemini.md) em arquivos de project/specs para evitar caminhos invalidos.
- Status: done
- Prioridade: 7
- Dependencias: nenhuma

### alex-0039 - Ajustar padrao de logs no repo.intent.yaml
- Descricao: alinhar target.logs.pattern para yoda/logs/<id>-<slug>.yaml, removendo duplicacao de dev no nome.
- Status: done
- Prioridade: 6
- Dependencias: nenhuma

### alex-0040 - Clarificar texto sobre corpo livre vs front matter
- Descricao: atualizar 04-todo-dev-yaml-issues.md para explicitar que o corpo e livre e o metadata fica no YAML front matter.
- Status: done
- Prioridade: 6
- Dependencias: nenhuma

### alex-0041 - Resolver inconsistencias de front matter nas issues antigas
- Descricao: escolher entre backfill de front matter em alex-0001..alex-0026 ou documentar excecao de bootstrap no 15-bootstrap.md.
- Status: done
- Prioridade: 6
- Dependencias: nenhuma

### alex-0042 - Padronizar criterio de selecao sem dependencias
- Descricao: substituir "without dependencies" por "with all dependencies resolved" em yoda/yoda.md e specs.
- Status: done
- Prioridade: 5
- Dependencias: nenhuma

### alex-0043 - Corrigir formatacao de caminho TODO.<slug>.md
- Descricao: ajustar trecho em yoda/yoda.md para manter `yoda/todos/TODO.<slug>.md` sem backticks no meio.
- Status: done
- Prioridade: 4
- Dependencias: nenhuma

### alex-0044 - Adicionar placeholder para yoda/scripts
- Descricao: criar yoda/scripts/ com README.md (ou .gitkeep) explicando que e placeholder ate scripts v1.
- Status: done
- Prioridade: 4
- Dependencias: nenhuma

### alex-0045 - Corrigir trechos em portugues nos influences
- Descricao: substituir trechos em portugues por ingles nos influences para alinhar com a politica de idioma.
- Status: done
- Prioridade: 4
- Dependencias: nenhuma

### alex-0046 - Corrigir espaco apos inline code no yoda.md
- Descricao: adicionar espaco apos inline-code em yoda/yoda.md para melhorar legibilidade.
- Status: done
- Prioridade: 4
- Dependencias: nenhuma

### alex-0047 - Remover links Markdown em project/specs
- Descricao: substituir links Markdown por inline code em project/specs para reduzir ruido para agentes.
- Status: done
- Prioridade: 4
- Dependencias: nenhuma

## Observacoes

- Cada item acima deve gerar um arquivo de issue em yoda/project/issues/.
- A partir da primeira issue, seguir o YODA Flow.
- Este TODO.md sera substituido por `TODO.<dev>.yaml` quando os scripts existirem.
