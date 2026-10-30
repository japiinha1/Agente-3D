# Agente 3D Pro

Sistema web de pré-processamento e validação para modelos 3D, com foco em fluxo de impressão 3D e compatibilidade com Bambu Studio.

## Visão geral

O Agente 3D Pro nasceu para ser uma camada de preparação antes do fatiamento final. Ele ajuda a:

- validar a geometria do modelo 3D
- detectar falhas de malha e volume
- avaliar risco de overhang, warping e aderência
- sugerir perfil de material para PLA, PETG, ABS e ASA
- gerar um manifesto técnico para revisão antes do envio ao slicer
- exportar pacote preparado em 3MF quando o mesh suporta o formato

## O que ele não substitui

Este projeto não é um slicer oficial completo e não substitui a etapa final do Bambu Studio.

O fluxo real e seguro continua sendo:

1. validar a peça
2. reparar a malha, quando necessário
3. ajustar material e nozzle
4. revisar suporte, warping e aderência
5. abrir no Bambu Studio
6. ajustar slicing final
7. gerar G-code
8. testar a impressão real

## O que já existe no projeto

- upload de STL, OBJ e 3MF
- análise de watertightness e manifold
- cálculo de volume e dimensões da peça
- indicadores de risco de suporte e aderência
- regras por material para Bambu-like workflows
- painel web em português
- manifesto técnico em JSON
- export de arquivo preparado em 3MF quando possível

## Estrutura do repositório

```text
Agente-3D/
├── app.py
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   └── mesh_validator.py
├── static/
│   ├── app.js
│   └── styles.css
├── templates/
│   └── index.html
├── docs/
│   ├── repositorios-compativeis.md
│   ├── fluxo-profissional.md
│   └── checklist-impressao.md
├── output/
│   └── uploads/
└── .gitignore
```

## Como rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Acesse:

- http://localhost:8000

## API

### Processar um arquivo

```bash
curl -X POST "http://localhost:8000/api/process" \
  -F "file=@modelo.stl" \
  -F "material=PLA" \
  -F "nozzle_mm=0.4" \
  -F "profile_name=Bambu X1C"
```

### Obter o manifesto gerado

```bash
curl http://localhost:8000/api/manifest/modelo
```

## Checklist de revisão antes da impressão

- malha fechada e sólida
- sem corpos desconectados
- volume válido
- suporte necessário revisado
- risco de warping e aderência avaliado
- material e nozzle coerentes
- peça orientada corretamente no slicer
- camada inicial revisada
- fluxo e temperatura confirmados

## Regras por material

### PLA
- temperatura do bico: 215°C
- temperatura da mesa: 60°C
- boa opção para prototipagem detalhada

### PETG
- temperatura do bico: 240°C
- temperatura da mesa: 80°C
- menos agressivo em detalhes finos, atenção ao resfriamento

### ABS
- temperatura do bico: 250°C
- temperatura da mesa: 100°C
- exige bom controle térmico e aderência

### ASA
- temperatura do bico: 255°C
- temperatura da mesa: 100°C
- bom para uso externo, mas exige atenção ao encolhimento

## Documentação útil

A documentação detalhada está em:

- `docs/checklist-impressao.md`
- `docs/fluxo-profissional.md`
- `docs/repositorios-compativeis.md`

## Repositórios relevantes para evolução deste projeto

Os melhores pontos de partida para complementar e evoluir o Agente 3D Pro são:

- MeshRight: https://github.com/Huzy85/MeshRight
- MeshDoc: https://github.com/Exulizer/MeshDoc
- meshseal: https://github.com/jkavalik/meshseal
- MeshRepair: https://github.com/arnasdev/MeshRepair
- PrusaSlicer: https://github.com/prusa3d/PrusaSlicer
- Cura: https://github.com/Ultimaker/Cura

Esses projetos são úteis para:

- reparo de malha mais robusto
- validação de volume e watertightness
- export de 3MF/OBJ/STL
- pipeline de preparação para slicing final

## Recomendação de arquitetura futura

Para evoluir de um pré-flight para um pipeline industrial, o ideal é combinar:

- Agente 3D Pro para validação e classificação
- MeshRight ou meshseal para reparo de malha forte
- export final em 3MF
- integração com PrusaSlicer ou Cura como slicer de referência
- arquivo de configuração por máquina/material
- checklist de revisão em português

## Observações finais

O projeto já está em um bom nível de base funcional para validar modelos antes da impressão. Ele é especialmente útil para reduzir erros geométricos e orientar a revisão do modelo antes de mandar para o Bambu Studio.

A evolução mais forte continua sendo a combinação de:

- validação inteligente
- reparo de malha em camada robusta
- export de pacote final em 3MF
- revisão humana final no slicer oficial


