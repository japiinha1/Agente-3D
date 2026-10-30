# AGENTS.md

Este arquivo define a arquitetura, a ordem correta de execução e as regras de operação do projeto Agente 3D.

Objetivo:
- construir um ecossistema de geração, validação e preparo de peças 3D para impressão
- separar responsabilidades por módulo
- garantir que cada etapa execute em ordem e com contrato claro
- evitar correções aleatórias e loops de debugging

## Estrutura obrigatória do projeto

O repositório deve manter esta organização:

- app/
  - app/__init__.py
  - app/main.py
  - app/api/__init__.py
  - app/api/routes.py
- agents/
  - agents/__init__.py
  - agents/coordinator.py
  - agents/model_agent.py
  - agents/mesh_validator.py
  - agents/repair_agent.py
  - agents/printer_profile_agent.py
  - agents/print_manifest_agent.py
- core/
  - core/__init__.py
  - core/config.py
- services/
  - services/__init__.py
  - services/mesh_service.py
- static/
- templates/
- output/
  - output/uploads/
  - output/repaired/
  - output/manifests/
- tests/
- requirements.txt
- app.py

## Responsabilidade de cada área

### 1) app/
Responsável por:
- arrancar a aplicação FastAPI
- montar rotas da API
- expor endpoints web
- servir o frontend

Não deve conter lógica de validação de malha nem regras de impressora.

### 2) agents/
Responsável por módulos especializados.

- coordinator.py
  - orquestra o fluxo completo
  - define ordem de execução
- model_agent.py
  - gera ou prepara a peça a partir de prompt ou regras de modelagem
- mesh_validator.py
  - valida watertightness, manifold, tamanho, risco e integridade
- repair_agent.py
  - corrige malha quebrada
- printer_profile_agent.py
  - aplica perfil da impressora e regras de preflight
- print_manifest_agent.py
  - gera relatórios e manifestos finais

### 3) core/
Responsável por:
- configurações gerais
- paths do projeto
- parâmetros oficiais da impressora
- extensões permitidas

### 4) services/
Responsável por:
- serviços utilitários e pontes entre módulos
- orquestrações mais altas
- helpers para mesh, output e gestão de artefatos

### 5) templates/ e static/
Responsável por:
- UI HTML/CSS/JS do dashboard
- elementos visuais
- upload e apresentação dos resultados

Nunca colocar regra de negócio aqui.

### 6) output/
Responsável por:
- guardar uploaded files
- arquivos reparados
- manifests gerados
- artefatos finais de entrega

## Regras de arquitetura que devem ser seguidas

1. Não misturar HTML, backend e lógica 3D em um único arquivo.
2. Não criar funções globais que substituem módulos.
3. Não inventar parâmetros de impressora sem fonte oficial.
4. Respeitar o contrato entre módulos:
   - entrada
   - processamento
   - saída
5. Todos os artefatos de processamento devem ir para output/
6. O app web deve apenas consumir a API e exibir resultados.
7. O coordinator deve decidir a ordem do fluxo.
8. O cliente e a API devem receber JSON válido, nunca HTML/texto em resposta de processamento.
9. A estrutura do projeto deve permanecer estável. Não refazer a arquitetura em patches aleatórios.
10. Qualquer alteração deve ser validada por etapa, não por tentativa e erro aleatória.

## Parâmetros oficiais da impressora X2D

Os valores oficiais devem ser usados como base de verdade do perfil da máquina.

Importante:
- build volume principal: 256 x 256 x 260 mm
- dual nozzle: 235.5 x 256 x 256 mm
- nozzle default: 0.4 mm
- nozzles suportados: 0.2, 0.4, 0.6, 0.8 mm
- temperatura máxima do bocal: 300 °C
- materiais relevantes: PLA, PETG, ABS, ASA, TPU, PA, PET, PC, PVA, reforçados

Esses valores devem estar em core/config.py e serem consumidos pelos agentes, não inventados em UI.

## Ordem correta de execução do fluxo

### Etapa 1 - ambiente local
1. Criar venv
2. Instalar requirements.txt
3. Rodar a aplicação
4. Confirmar /health

### Etapa 2 - base web
1. Abrir http://localhost:10000/
2. Validar que a dashboard HTML aparece
3. Confirmar que não há Python sendo exibido como texto bruto

### Etapa 3 - upload e processamento
1. Selecionar arquivo STL/OBJ/3MF
2. Escolher material
3. Informar nozzle_mm
4. Informar profile_name
5. Chamar /api/process

### Etapa 4 - validadora e reparo
1. MeshValidatorAgent analisa o arquivo
2. Confirma watertightness e manifold
3. Se falhar, RepairAgent tenta corrigir
4. Revalida a malha

### Etapa 5 - perfil e preflight
1. PrinterProfileAgent aplica X2D
2. Verifica envelope da impressora
3. Calcula risco de warping/overhang/support/adhesion
4. Produce report de preflight

### Etapa 6 - manifest final
1. PrintManifestAgent cria JSON de manifest
2. Salva em output/uploads
3. Entrega arquivo final e recomendação do processo

### Etapa 7 - entrega ao usuário
1. O usuário recebe o arquivo processado
2. Pode baixar a solução final
3. Pode abrir em Bambu Studio para slicer final

## Como rodar localmente

### Windows
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 10000 --reload
```

### Linux/macOS
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 10000 --reload
```

## URLs esperadas

- http://localhost:10000/health
- http://localhost:10000/
- http://localhost:10000/api/process
- http://localhost:10000/api/manifest/<nome>
- http://localhost:10000/api/download/<nome>

## Respostas esperadas

### health
```json
{"status":"ok","service":"Agente 3D"}
```

### processo válido
```json
{
  "status": "processed",
  "file_name": "arquivo.stl",
  "material": "PLA",
  "profile": { ... },
  "analysis": { ... },
  "checks": { ... },
  "recommendations": [ ... ],
  "is_ready": true
}
```

## Critérios de aceite do sistema

O projeto está pronto quando:
- /health responde OK
- / responde HTML da dashboard
- upload de STL simples funciona
- /api/process retorna JSON válido
- manifest é gerado em output/
- arquivo reparado, quando necessário, é salvo
- perfil Bambu X2D é usado como base da máquina
- sistema não depende de valores inventados

## Regras para agentes/helpers (como Antigravity, Copilot, Cursor)

Quando um agente auxiliar for usado, ele deve obedecer estas instruções:

1. Ler este arquivo primeiro.
2. Não mexer em estrutura de pastas sem necessidade.
3. Validar a aplicação por etapas, na ordem correta.
4. Não fazer patches aleatórios.
5. Respeitar separação de módulos.
6. Usar X2D como máquina-base oficial.
7. Não misturar frontend com backend.
8. Não tentar resolver tudo em um único ajuste.
9. Se houver erro, identificar a etapa que falhou e corrigir apenas a etapa.
10. Validar depois de cada ajuste.

## Uso com Blender e Bambu Studio

### Blender
Pode ser usado para:
- geração procedural de geometria
- análise de malha
- exportação para STL/OBJ/3MF
- reparo visual e de topologia

Precisará de integração por script ou export via diretório output/.

### Bambu Studio
Pode ser usado para:
- slicar arquivo final
- visual check do print
- validar o material e qualidade de impressão final

Não deve substituir a lógica do backend. É ferramenta final de slicer/visualização.

## Resumo executivo

Este projeto é um ecossistema de peças 3D, não um script único.
Ele precisa funcionar em camadas:
- UI
- API
- orquestração
- validação
- reparo
- perfil da impressora
- manifesto final

Cada camada deve ter uma função.
Cada etapa deve ser testada e validada.
Cada dado real deve vir de fonte confiável.

Se qualquer coisa falhar, a correção deve acontecer na etapa certa.

---

Arquivo de guia operacional para agentes e execução local.
