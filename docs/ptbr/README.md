# Repositórios compatíveis para evoluir o projeto

## 1. MeshRight

- https://github.com/Huzy85/MeshRight
- forte foco em reparo de malha para impressão 3D
- útil para correção mais forte do modelo

## 2. MeshDoc

- https://github.com/Exulizer/MeshDoc
- app client-side para diagnóstico e reparo em navegador
- bom para validação sem upload para servidor

## 3. meshseal

- https://github.com/jkavalik/meshseal
- biblioteca moderna para reparar STL/3MF com foco em watertightness
- bom caminho para integração no backend

## 4. MeshRepair

- https://github.com/arnasdev/MeshRepair
- CLI e pipeline de automação para reparo de modelos
- excelente para fluxo de batch e linha de produção

## 5. PrusaSlicer

- https://github.com/prusa3d/PrusaSlicer
- slicer open-source muito robusto
- pode ser usado como referência para parsing e regras de slicing

## 6. Cura

- https://github.com/Ultimaker/Cura
- excelente ecossistema e suporte a workflows de impressão 3D
- útil para comparação de perfis e export

## Como combinar tudo

A melhor abordagem é usar o Agente 3D Pro como camadas de:

- validação
- classificação
- roteiro técnico
- revisão de risco

E usar os projetos listados acima como módulos específicos de:

- reparo de malha
- export em 3MF
- slicing final

Isso reduz o risco de manter uma solução excessivamente acoplada e aumenta a chance de trabalhar com ferramentas reconhecidas no ecossistema 3D.

