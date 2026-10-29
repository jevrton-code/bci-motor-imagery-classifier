# BCI Motor Imagery Classifier: documento de contexto para o LinkedIn

> **Idioma:** Português (Brasil) · English version: [`LINKEDIN_CONTEXT.en.md`](LINKEDIN_CONTEXT.en.md)
> **Última atualização:** 2026-10-29
> **Versão do projeto coberta:** v1.0.0 (commit `beba3ba`, 2026-06-08)
> **Repositório:** https://github.com/jevrton-code/bci-motor-imagery-classifier

---

## 0. Para que serve este documento

Este arquivo é a **fonte única de contexto** para tudo o que for publicado sobre
este projeto no LinkedIn: posts, carrosséis (posts de documento em PDF),
comentários, atualizações de versão e a seção "Projetos" do perfil. Ele pode
ser usado por você ou entregue inteiro a um assistente de IA.

Tudo aqui foi conferido contra o repositório (código, CSVs de resultados,
relatório, figuras e histórico do git) em 2026-10-29. Onde um número foi
calculado a partir dos dados e não aparece escrito no README, isso está
indicado.

**Como usar**

- **Para escrever um post:** leia §1 (resumos prontos), §5 (o que os resultados
  significam) e §6 (o que não afirmar), e escolha um ângulo em §12.
- **Para pedir a um assistente de IA:** entregue este arquivo e diga qual
  ângulo da §12 você quer, o idioma e o tamanho. Instrua-o a usar **apenas** os
  números da §4 e a respeitar a §6.
- **Quando o projeto mudar:** atualize primeiro a §4 (ficha técnica), a §8
  (linha do tempo) e a §20 (registro de alterações). O resto deriva delas.

**Regras inegociáveis para qualquer texto público**

1. Números só da ficha técnica (§4), sempre com o contexto "avaliação
   within-session, sujeitos 1–10".
2. Nunca sugerir uso clínico, diagnóstico, "leitura de mente" ou controle em
   tempo real.
3. Toda vez que citar uma média, citar também a variação entre sujeitos.
4. Creditar o dataset e as ferramentas (§15).
5. Não dizer que o projeto tem "testes automatizados": hoje os 4 testes são
   placeholders pulados (§18).

---

## 1. Resumos prontos (do mais curto ao mais longo)

**Uma linha (bio, legenda de imagem, título de carrossel)**

> Benchmark reprodutível de interface cérebro-computador (BCI): classificação
> de imagética motora em EEG com baselines clássicos e avaliação transparente.

**Gancho (cabe antes do "ver mais", cerca de 150 caracteres)**

> Uma média de ROC-AUC 0,65 parece um bom resultado para um BCI. Até você olhar
> sujeito por sujeito: no mesmo benchmark, um ficou em 1,00 e outro em 0,23.

**Resumo curto (cerca de 510 caracteres, para post rápido ou comentário)**

> Construí um benchmark reprodutível de interface cérebro-computador (BCI) para
> classificar imagética motora (imaginar mover a mão esquerda ou a direita) a
> partir de EEG público (PhysioNet, 10 sujeitos, 64 canais). Comparei três
> pipelines sob o mesmo protocolo MOABB: CSP+LDA, um baseline simples de
> log-variância + LDA e um classificador aleatório como referência de acaso. Os
> dois métodos reais ficaram acima do acaso em média (ROC-AUC 0,653 e 0,658),
> mas a variação entre sujeitos foi enorme: de 0,23 a 1,00.

**Descrição para a seção "Projetos" do perfil (cerca de 1.470 caracteres;
limite do LinkedIn: 2.000)**

```text
Benchmark reprodutível de classificação de imagética motora (mão esquerda × mão direita) a partir de EEG, uma tarefa clássica de interface cérebro-computador (BCI).

O que fiz
• Usei dados públicos do PhysioNet EEG Motor Movement/Imagery Dataset via MOABB (sujeitos 1–10, 64 canais, 160 Hz, banda de 8–32 Hz).
• Comparei três pipelines numa única avaliação within-session, com as mesmas divisões de treino e teste e semente fixa: CSP+LDA, LogVariance+LDA e um baseline aleatório (Dummy) como referência de acaso.
• Mantive o CSP dentro do pipeline de validação cruzada para evitar vazamento de dados, e não ajustei hiperparâmetros olhando o teste.
• Gerei resultados por sujeito, estatísticas agregadas (média, mediana, desvio-padrão, IQR), três figuras e um relatório de metodologia.

Resultados (ROC-AUC; acaso = 0,5)
• CSP+LDA: média 0,653, variando de 0,23 a 1,00 entre sujeitos
• LogVariance+LDA: média 0,658, variando de 0,46 a 0,80
• Dummy: média 0,530, confirmando que a avaliação se comporta como esperado

A principal lição: a média esconde quem o sistema não atende. Três dos dez sujeitos ficaram abaixo do acaso com CSP+LDA, e o baseline simples empatou com o método clássico na média, com metade da dispersão.

Escopo honesto: é um benchmark offline, within-session, com 10 sujeitos. Não é um BCI em tempo real, não testa generalização entre pessoas e não tem finalidade clínica.

Stack: Python, MOABB, MNE-Python, scikit-learn, pandas, Matplotlib, seaborn.
```

**Campos sugeridos da seção "Projetos"**

| Campo | Sugestão |
| --- | --- |
| Nome do projeto | BCI Motor Imagery Classifier: benchmark reprodutível de imagética motora em EEG |
| Data | jun. de 2026 (v1.0 publicada em 2026-06-08) |
| Competências | Python · Aprendizado de máquina · Processamento de sinais · Eletroencefalografia (EEG) · scikit-learn |
| Mídia | Link do repositório + `figures/score_distribution.png` (ver §10) |
| Associado a | [A PREENCHER: experiência, curso ou "projeto pessoal"] |

---

## 2. O problema e a motivação

### Em linguagem simples

Uma **interface cérebro-computador (BCI)** tenta transformar atividade
cerebral em comandos para uma máquina. Um dos paradigmas mais estudados é a
**imagética motora**: a pessoa apenas *imagina* mover a mão esquerda ou a
direita, e esse ato muda o padrão dos ritmos elétricos registrados sobre o
córtex motor. Um classificador tenta descobrir, só pelo EEG, qual das duas mãos
foi imaginada.

### Por que fazer isso "com cuidado" importa

A área de BCI atrai manchetes exageradas. Na prática, os resultados dependem de
detalhes que raramente aparecem num post:

- **Como a avaliação foi feita.** Testar em trechos da mesma sessão
  (within-session) é muito mais fácil do que funcionar numa pessoa nova
  (cross-subject).
- **Vazamento de dados.** Técnicas supervisionadas como o CSP, se ajustadas
  com os dados de teste, inflam o resultado.
- **Referência de acaso.** Com poucas tentativas por pessoa, um classificador
  aleatório pode parecer bom por sorte.
- **Variação entre pessoas.** Uma média bonita pode esconder pessoas para quem
  o sistema simplesmente não funciona.

O projeto foi desenhado para tratar cada um desses pontos explicitamente, com
dados públicos e ferramentas de benchmark estabelecidas, priorizando
transparência em vez de um número de destaque.

### Motivação pessoal do autor

[A PREENCHER: por que você quis construir isto, de onde vem seu interesse em
BCI/neurotecnologia, o que queria provar ou aprender. Ver §19.]

---

## 3. O que foi construído

### Visão geral do fluxo

```text
PhysioNet EEG Motor Movement/Imagery Dataset (109 sujeitos)
  └─ MOABB PhysionetMI — sujeitos 1–10, 64 canais, 160 Hz
      └─ Paradigma LeftRightImagery — mão esquerda × direita, filtro 8–32 Hz, tentativas de 3 s
          └─ 3 pipelines avaliados numa ÚNICA chamada WithinSessionEvaluation
             (mesmas divisões de treino/teste, semente 42, métrica ROC-AUC)
               ├─ CSP+LDA          (principal)
               ├─ Dummy            (referência de acaso)
               └─ LogVariance+LDA  (baseline simples)
          └─ results/baseline_results.csv  (30 linhas = 10 sujeitos × 3 pipelines)
              └─ scripts/run_analysis.py
                  ├─ results/aggregate_scores.csv
                  ├─ figures/per_subject_scores.png
                  ├─ figures/pipeline_comparison.png
                  └─ figures/score_distribution.png
                      └─ reports/bci_motor_imagery_report.md
```

### Os três pipelines

| Pipeline | O que faz | Papel no benchmark |
| --- | --- | --- |
| **CSP+LDA** | *Common Spatial Patterns* (6 componentes, log-variância, sem regularização) extrai filtros espaciais supervisionados; *Linear Discriminant Analysis* classifica. | Baseline clássico de referência em imagética motora. |
| **Dummy** | `DummyClassifier` estratificado do scikit-learn (precedido de um achatamento das épocas). Ignora o sinal. | Prova de sanidade: deve ficar perto de 0,5. |
| **LogVariance+LDA** | Log da variância de cada canal (potência de banda) + LDA. Sem filtros espaciais aprendidos. | Baseline transparente para comparar com o CSP. |

### Organização do código

- `src/bci_mi_classifier/`: pacote com `config` (fonte única das escolhas
  fixas), `datasets`, `pipelines`, `evaluation`, `results` e `visualization`.
- `scripts/run_baseline.py`: roda o benchmark (baixa os dados na primeira vez).
- `scripts/run_analysis.py`: lê o CSV salvo e gera estatísticas e figuras (não
  baixa nada).
- `reports/bci_motor_imagery_report.md`: metodologia, resultados, limitações e
  reprodução.

### Reprodução em dois comandos

```bash
python3 scripts/run_baseline.py   # benchmark (MOABB baixa o PhysionetMI na 1ª vez)
python3 scripts/run_analysis.py   # tabelas agregadas + figuras
```

---

## 4. Ficha técnica (números verificados)

### Dataset, protocolo e configuração

| Item | Valor | Fonte no repositório |
| --- | --- | --- |
| Dataset | PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0, via MOABB `PhysionetMI` | `README.md`, `config.py` |
| Tamanho do dataset completo | 109 sujeitos, 1 sessão, 64 canais EEG, 160 Hz, tentativas de 3,0 s | `README.md` |
| Sujeitos usados na v1 | 1 a 10 | `config.SUBJECTS` |
| Tarefa | Binária: mão esquerda × mão direita (imagética) | `config.PARADIGM` |
| Banda de frequência | 8–32 Hz | `config.FMIN/FMAX` |
| Avaliação | Within-session (`WithinSessionEvaluation`), todos os pipelines numa só chamada | `README.md`, relatório |
| Tentativas por sujeito | 45 (cerca de 9 no conjunto de teste por fold) | colunas `samples` e `samples_test` do CSV |
| Métrica principal | ROC-AUC (acaso = 0,5) | `config.PRIMARY_METRIC` |
| Semente | 42 | `config.RANDOM_STATE` |
| Componentes CSP | 6 (fixo, não ajustado no teste) | `config.N_CSP_COMPONENTS` |
| Licença do código | MIT | `LICENSE` |
| Licença do dataset | ODC-By 1.0 (separada; dados não redistribuídos) | `CITATION.md` |

### Resultados agregados (ROC-AUC, 10 sujeitos)

| Pipeline | Média | Mediana | Desvio-padrão | IQR | Mín. | Máx. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CSP+LDA | 0,653 | 0,665 | 0,234 | 0,283 | 0,23 | 1,00 |
| Dummy | 0,530 | 0,510 | 0,076 | 0,103 | 0,46 | 0,695 |
| LogVariance+LDA | 0,658 | 0,670 | 0,117 | 0,173 | 0,46 | 0,80 |

Fonte: `results/aggregate_scores.csv`.

### Resultados por sujeito (ROC-AUC)

| Sujeito | CSP+LDA | LogVariance+LDA | Dummy |
| ---: | ---: | ---: | ---: |
| 1 | 0,81 | 0,80 | 0,46 |
| 2 | 0,95 | 0,79 | 0,595 |
| 3 | 0,57 | 0,58 | 0,46 |
| 4 | 0,67 | 0,66 | 0,55 |
| 5 | 0,45 | 0,77 | 0,47 |
| 6 | 0,48 | 0,60 | 0,515 |
| 7 | 1,00 | 0,68 | 0,505 |
| 8 | 0,66 | 0,52 | 0,58 |
| 9 | 0,23 | 0,46 | 0,695 |
| 10 | 0,71 | 0,72 | 0,47 |

Fonte: `results/baseline_results.csv`.

### Fatos derivados (calculados a partir do CSV em 2026-10-29)

Estes números não estão escritos no README, mas saem diretamente dos dados
versionados. Podem ser usados em posts.

- **CSP+LDA ficou abaixo do acaso em 3 de 10 sujeitos** (5: 0,45; 6: 0,48;
  9: 0,23). O README diz "pelo menos um"; o número exato é 3.
- **LogVariance+LDA ficou abaixo do acaso em 1 de 10** (sujeito 9: 0,46).
- **Confronto direto CSP+LDA × LogVariance+LDA: 5 a 5.** Cada método foi
  melhor em cinco sujeitos.
- **Sujeitos com ROC-AUC ≥ 0,70:** 4 para CSP+LDA (1, 2, 7, 10) e 4 para
  LogVariance+LDA (1, 2, 5, 10).
- **O Dummy superou o CSP+LDA em 3 sujeitos** (5, 6 e 9).
- **O Dummy chegou a 0,695** (sujeito 9): com cerca de 9 tentativas de teste
  por fold, o acaso oscila bastante.
- **O desvio-padrão do LogVariance+LDA (0,117) é metade do CSP+LDA (0,234).**
- A coluna `time` do MOABB registra cerca de 0,49 s para o CSP+LDA, 0,016 s
  para o LogVariance+LDA e 0,004 s para o Dummy (média entre sujeitos).
  Depende da máquina, então **não use como argumento de desempenho**.

### Tamanho do projeto

- Cerca de 1.200 linhas de Python (pacote, scripts e testes).
- 6 módulos no pacote, 2 scripts, 3 figuras, 2 CSVs de resultados e 1 relatório.
- 4 arquivos de teste, todos placeholders marcados como `skip` (verificado em
  2026-10-29: `4 skipped`).

---

## 5. Resultados e interpretação (as histórias que os números contam)

### 5.1 Acima do acaso na média, mas só na média

Os dois métodos reais ficaram acima de 0,5 em média (0,653 e 0,658), e o Dummy
ficou perto do acaso (0,530). Isso mostra que **métodos clássicos podem
funcionar para alguns sujeitos em condições within-session**, e o relatório não
vai além disso.

### 5.2 A média esconde quem o sistema não atende

O CSP+LDA foi de 0,23 a 1,00. Três sujeitos ficaram abaixo do acaso. É uma
ilustração concreta de um fenômeno conhecido na literatura de BCI (às vezes
chamado de *BCI inefficiency*): uma parte das pessoas não obtém bom desempenho
com as abordagens padrão. **Esta é a mensagem mais forte do projeto para o
LinkedIn**, porque vale para qualquer sistema de IA avaliado só pela média.

### 5.3 O baseline simples empatou com o método clássico

O LogVariance+LDA, que não aprende nenhum filtro espacial, teve média
praticamente igual à do CSP+LDA (0,658 × 0,653), metade da dispersão e um
placar direto de 5 a 5. Com apenas 10 sujeitos e sem teste estatístico,
**não há vencedor**. A lição é metodológica: sem o baseline simples, o CSP
pareceria "o método que funciona".

*Hipótese (não testada no projeto):* com 64 canais, cerca de 36 tentativas de
treino por fold e CSP sem regularização, as matrizes de covariância são
estimadas com poucos dados, o que pode explicar a instabilidade do CSP em
alguns sujeitos. Testar CSP regularizado ou métodos Riemannianos seria o
próximo passo natural. Se usar isso num post, apresente como hipótese.

### 5.4 O Dummy como prova de sanidade, e como alerta

A média do Dummy (0,530) confirma que a avaliação está sã. Mas o mesmo Dummy
chegou a 0,695 num sujeito. Com tão poucas tentativas de teste, **um 0,70
isolado não prova nada**. Por isso a linha de acaso aparece tracejada em todas
as figuras.

### 5.5 O 1,00 do sujeito 7 não é manchete

ROC-AUC perfeito com cerca de 9 tentativas de teste por fold é possível e não
generaliza. Nunca use esse número sozinho.

---

## 6. O que pode e o que não pode ser dito

| ✅ Pode dizer | ❌ Não diga | Por quê |
| --- | --- | --- |
| "Benchmark offline, within-session, em 10 sujeitos de um dataset público" | "Meu modelo lê a mente" / "decodifica pensamentos" | É classificação binária de imagética motora, offline. |
| "ROC-AUC médio de 0,653 (CSP+LDA) e 0,658 (LogVariance+LDA), com grande variação entre sujeitos" | "65% de acurácia" | A métrica é ROC-AUC, não acurácia. |
| "Acima do acaso na média para os sujeitos selecionados" | "Funciona para qualquer pessoa" / "generaliza" | Não houve teste cross-subject nem cross-session. |
| "Base para trabalhos futuros em BCI" | "BCI pronto para produção" / "controle em tempo real" | Não há decodificação online nem integração com hardware. |
| "Projeto educacional e de pesquisa, sem finalidade clínica" | Qualquer menção a diagnóstico, reabilitação ou tratamento como resultado do projeto | O README exclui explicitamente usos clínicos. |
| "LogVariance+LDA teve média comparável e metade da dispersão" | "LogVariance+LDA é melhor que CSP" | n = 10, sem teste estatístico. |
| "Reprodutível com dois comandos, dados baixados sob demanda" | "Testado com suíte de testes automatizados" | Os testes atuais são placeholders. |
| "Código aberto sob licença MIT" | "Dataset próprio" / "coletei os dados" | Os dados são do PhysioNet (ODC-By 1.0). |

---

## 7. Decisões de engenharia (bastidores que viram conteúdo)

Cada decisão abaixo pode virar um post curto no formato "problema → decisão →
por que importa".

1. **Baselines clássicos antes de deep learning.** A v1 exclui deep learning de
   propósito. Primeiro se estabelece uma avaliação confiável; depois se compara
   qualquer modelo novo contra ela.
2. **Within-session primeiro, cross-subject depois.** O snapshot do MOABB tem
   uma sessão por sujeito, então within-session é o protocolo mais limpo para a
   v1. Cross-subject fica como experimento separado, com interpretação
   separada.
3. **CSP dentro do pipeline.** O CSP é supervisionado; ficar dentro do
   `Pipeline` do scikit-learn garante que ele seja ajustado só nos folds de
   treino. Isso evita vazamento de dados.
4. **Hiperparâmetros fixos e documentados.** Seis componentes CSP, escolhidos
   antes de ver resultados. Se houver ajuste no futuro, será com validação
   cruzada aninhada.
5. **Uma única chamada de avaliação para todos os pipelines.** Garante que os
   três sejam comparados exatamente nas mesmas divisões de treino e teste.
6. **Um classificador aleatório como referência obrigatória.** O Dummy mostra
   onde está o acaso *neste* dataset, com *este* número de tentativas.
7. **ROC-AUC como métrica principal.** Não depende de limiar e tem um acaso
   bem definido (0,5) em tarefas binárias.
8. **Higiene de dados.** EEG bruto e caches do MOABB/MNE nunca entram no git;
   só CSVs e figuras curados são versionados. A licença do código (MIT) é
   separada da licença dos dados (ODC-By 1.0).
9. **Subconjunto pequeno de propósito.** Dez sujeitos permitem inspecionar
   cada resultado e reproduzir tudo rapidamente.
10. **Uma fonte única de verdade.** Todas as escolhas fixas vivem em
    `config.py`, com comentários explicando o porquê.
11. **Entregas incrementais.** v0.1 (estrutura e protocolo, sem rodar nada) →
    v0.2 (primeiro benchmark) → v0.3 (análise e figuras) → v0.4 (baselines
    extras) → v1.0 (relatório e polimento), com itens de backlog `BCI-xxx` no
    `ROADMAP.md`.

---

## 8. Linha do tempo

| Data | Versão | Commit | O que entrou |
| --- | --- | --- | --- |
| 2026-06-08 | v0.1 | `a64fbd7` | Estrutura do repositório, protocolo de avaliação, escopo, citações, licença |
| 2026-06-08 | v0.2 | `4321add` | Primeiro benchmark MOABB within-session com CSP+LDA |
| 2026-06-08 | v0.3 | `8e9ef25` | Análise de resultados, resumo agregado e figuras |
| 2026-06-08 | v0.4 | `d604e9f` | Baselines Dummy e LogVariance+LDA |
| 2026-06-08 | v1.0 | `beba3ba` | Relatório, README e documentação finais |

Não há tag nem *release* criada no GitHub (ver §18).

---

## 9. Stack e competências

**Tecnologias:** Python 3.11+, MOABB (≥ 1.0), MNE-Python (≥ 1.6),
scikit-learn (≥ 1.3), pandas, NumPy, Matplotlib, seaborn, pytest.

**Competências para marcar no LinkedIn** (escolha as mais relevantes para a
vaga que você busca):

- Python
- Aprendizado de máquina (Machine Learning)
- Processamento de sinais (Signal Processing)
- Eletroencefalografia (EEG)
- Interfaces cérebro-computador (Brain-Computer Interfaces)
- scikit-learn
- Avaliação de modelos / Validação cruzada
- Ciência de dados
- Pesquisa reprodutível
- Neurotecnologia

**Competências demonstradas, em linguagem de recrutador**

- Desenho de protocolo experimental antes de escrever o modelo.
- Prevenção de vazamento de dados e comparação justa entre modelos.
- Comunicação honesta de resultados, incluindo os casos de falha.
- Organização de projeto científico como software (pacote, scripts,
  configuração central, licenças).

---

## 10. Ativos visuais disponíveis

| Arquivo | O que mostra | Melhor uso | Cuidados |
| --- | --- | --- | --- |
| `figures/score_distribution.png` (1039×680) | Boxplot por pipeline com os pontos de cada sujeito e a linha de acaso | **Imagem principal.** Mostra média e variação de uma vez. | Explique que cada ponto é uma pessoa. |
| `figures/per_subject_scores.png` (1039×680) | Barras por sujeito e pipeline, com acaso tracejado | Posts sobre variação entre pessoas | **A legenda cobre as barras dos sujeitos 7 a 10** (a barra do CSP no sujeito 9 fica parcialmente escondida). Regere com a legenda fora do gráfico antes de usar como imagem principal. |
| `figures/pipeline_comparison.png` (1039×680) | Média ± desvio-padrão por pipeline | Comparação geral | Sozinha, reforça "a média". Use junto com uma das outras duas. |

**Formato no LinkedIn:** as figuras são paisagem (cerca de 3:2). No feed,
imagens verticais (1080×1350, 4:5) ocupam mais tela. Para um post com várias
imagens, o melhor formato é um **carrossel** (post de documento em PDF).

**Roteiro sugerido de carrossel (7 slides, 1080×1350)**

1. Capa: "Uma média de 0,65 esconde um 0,23" + nome do projeto.
2. O que é imagética motora e BCI, em duas frases.
3. O protocolo: dataset público, 10 sujeitos, within-session, 3 pipelines,
   mesmas divisões.
4. Resultado agregado (`pipeline_comparison.png`).
5. A virada: cada ponto é uma pessoa (`score_distribution.png`).
6. O que este projeto NÃO prova (lista da §6).
7. Próximos passos + link do GitHub + créditos do dataset.

**Ativo que falta:** uma imagem de capa do repositório (*social preview* do
GitHub, 1280×640), que aparece quando o link é compartilhado no LinkedIn.

---

## 11. Público, posicionamento e tom

### Para quem os posts falam

| Público | O que procura | O que destacar |
| --- | --- | --- |
| Recrutadores e gestores técnicos | Sinais de rigor, autonomia e comunicação | Escopo bem definido, entregas incrementais, limitações explícitas |
| Pessoas de ML e ciência de dados | Metodologia | Vazamento de dados, baselines, ROC-AUC, variação entre sujeitos |
| Comunidade de neurotecnologia e BCI | Domínio técnico | MOABB, CSP, within-session × cross-subject, PhysionetMI |
| Estudantes e academia | Material de aprendizado | Reprodução em dois comandos, relatório de metodologia |
| Público geral curioso | Entender o que é BCI | Explicações simples e sem exagero |

### Posicionamento sugerido

> Engenharia de software aplicada à neurotecnologia: projetos com dados
> públicos reais, avaliação transparente e limitações escritas antes dos
> resultados.

### Tom de voz

- Primeira pessoa, direto, técnico mas acessível.
- Mostrar o que **não** funcionou é parte da mensagem, não um problema.
- Evitar palavras como "revolucionário", "leitura de mente" ou "o futuro
  chegou".
- Parágrafos curtos, uma ideia por parágrafo, no máximo 2 ou 3 emojis
  funcionais (por exemplo, → ou ✅), se usar algum.

### Notas de formato do LinkedIn (confira, os limites mudam)

- Post: até 3.000 caracteres. Só as primeiras linhas (cerca de 200
  caracteres) aparecem antes do "ver mais", então o gancho precisa estar ali.
- Descrição na seção "Projetos": até 2.000 caracteres.
- Título do perfil: até 220 caracteres. Seção "Sobre": até 2.600 caracteres.
- Carrossel: post de documento em PDF, slides verticais (1080×1350) ou
  quadrados.
- Hashtags: 3 a 5 relevantes funcionam melhor do que listas longas.

---

## 12. Banco de ângulos para posts

Cada ângulo traz gancho, pontos-chave, visual e chamada para ação. São
roteiros, não posts prontos.

### A. Lançamento do projeto (visão geral)
- **Gancho:** "Construí um benchmark de interface cérebro-computador. O
  resultado mais importante não foi a média."
- **Pontos:** o que é imagética motora; dataset público; 3 pipelines; médias
  0,653 e 0,658; variação de 0,23 a 1,00; o que o projeto não é.
- **Visual:** `score_distribution.png` ou carrossel da §10.
- **CTA:** link do GitHub; "o que você olharia primeiro num benchmark de BCI?"

### B. A média esconde pessoas
- **Gancho:** "Média de 0,65. Três de dez pessoas abaixo do acaso."
- **Pontos:** tabela por sujeito; *BCI inefficiency*; paralelo com qualquer
  sistema de IA avaliado só pela média.
- **Visual:** `per_subject_scores.png` (com a legenda corrigida).
- **Público:** ML em geral, recrutadores.

### C. O baseline simples empatou
- **Gancho:** "O método 'clássico' e o método 'simples' empataram. 5 a 5."
- **Pontos:** CSP+LDA × LogVariance+LDA; metade da dispersão; n = 10, sem
  vencedor; hipótese da covariância com poucos dados (como hipótese).
- **Público:** ML e neurotecnologia.

### D. Por que eu treinei um classificador aleatório
- **Gancho:** "O modelo mais importante do meu benchmark não olha para os
  dados."
- **Pontos:** Dummy com média 0,530; chegou a 0,695 num sujeito; por que
  poucas tentativas tornam o acaso instável; linha de acaso em todas as
  figuras.

### E. Within-session não é o mesmo que funcionar em outra pessoa
- **Gancho:** "Quando ler '90% num BCI', pergunte: testado em quem?"
- **Pontos:** diferença entre within-session, cross-session e cross-subject;
  por que este projeto declara o protocolo; roadmap do cross-subject.
- **Público:** público geral e recrutadores (educativo).

### F. Vazamento de dados em EEG
- **Gancho:** "Um detalhe de uma linha que infla resultados de BCI."
- **Pontos:** CSP é supervisionado; precisa ser ajustado só no treino;
  `Pipeline` do scikit-learn; hiperparâmetros fixos antes de ver o teste.
- **Público:** ML.

### G. O que meu projeto NÃO faz
- **Gancho:** "Escrevi as limitações antes dos resultados."
- **Pontos:** lista da §6; por que escopo explícito aumenta a credibilidade.

### H. Bastidores: de v0.1 a v1.0
- **Gancho:** "A v0.1 do meu benchmark não rodava nenhum modelo, e isso foi de
  propósito."
- **Pontos:** v0.1 só com protocolo e estrutura; backlog `BCI-xxx`; entregas
  incrementais.

### I. Ciência aberta e licenças
- **Gancho:** "Meu código é MIT. Os dados não são meus."
- **Pontos:** ODC-By 1.0; dados não redistribuídos; atribuição; caches fora do
  git.

### J. Série com os outros projetos
- **Gancho:** "Antes de classificar EEG, eu precisei entender o sinal."
- **Pontos:** ligação com o EEG Signal Processing Lab (§17).

---

## 13. Glossário para linguagem acessível

| Termo | Explicação simples |
| --- | --- |
| **EEG** | Registro da atividade elétrica do cérebro por eletrodos no couro cabeludo. |
| **BCI (interface cérebro-computador)** | Sistema que tenta transformar sinais cerebrais em comandos. |
| **Imagética motora** | Imaginar um movimento sem executá-lo. Muda ritmos do EEG sobre o córtex motor. |
| **CSP (Common Spatial Patterns)** | Técnica que aprende combinações de eletrodos que mais diferenciam duas classes. |
| **LDA** | Classificador linear simples que separa duas classes com uma reta (ou plano). |
| **Log-variância** | Medida da "energia" do sinal em cada canal, usada como característica. |
| **ROC-AUC** | Nota de 0 a 1 de quanto o modelo ordena bem os exemplos; 0,5 é acaso, 1,0 é perfeito. |
| **Nível de acaso** | O resultado esperado de um "chute". Aqui, 0,5. |
| **Within-session** | Treinar e testar com dados da mesma sessão da mesma pessoa. |
| **Cross-subject** | Treinar com algumas pessoas e testar em outra. É bem mais difícil. |
| **Vazamento de dados** | Quando informação do teste "vaza" para o treino e infla o resultado. |
| **Validação cruzada (fold)** | Dividir os dados em partes e alternar qual parte é o teste. |
| **MOABB** | Biblioteca de benchmark de BCI que padroniza datasets, paradigmas e avaliações. |
| **Baseline** | Modelo de referência, geralmente simples, para comparar os outros. |

---

## 14. Hashtags e palavras-chave

**Hashtags (escolha de 3 a 5 por post)**

- Núcleo: `#BCI` `#EEG` `#Neurotecnologia` `#MachineLearning` `#Python`
- Alcance em português: `#InterfaceCérebroComputador` `#CiênciaDeDados`
  `#AprendizadoDeMáquina` `#Neurociência`
- Alcance em inglês: `#BrainComputerInterface` `#Neurotechnology`
  `#SignalProcessing` `#OpenScience` `#ReproducibleResearch`

**Palavras-chave para busca e SEO do perfil:** interface cérebro-computador,
BCI, EEG, imagética motora, motor imagery, CSP, LDA, MOABB, MNE-Python,
scikit-learn, PhysioNet, avaliação reprodutível, neurotecnologia.

---

## 15. Créditos e citações

**Linha curta para colocar no fim de um post**

> Dados: PhysioNet EEG Motor Movement/Imagery Dataset (Schalk et al., 2004;
> Goldberger et al., 2000), licença ODC-By 1.0. Ferramentas: MOABB, MNE-Python
> e scikit-learn.

**Referências completas** (detalhes e BibTeX em `CITATION.md`)

- Schalk, G. et al. (2004). BCI2000: A General-Purpose Brain-Computer
  Interface (BCI) System. *IEEE Trans. Biomed. Eng.*, 51(6), 1034–1043.
- Goldberger, A. L. et al. (2000). PhysioBank, PhysioToolkit, and PhysioNet.
  *Circulation*, 101(23), e215–e220.
- Jayaram, V. & Barachant, A. (2018). MOABB: Trustworthy Algorithm
  Benchmarking for BCIs. *J. Neural Eng.*, 15(6), 066011.
- Gramfort, A. et al. (2013). MEG and EEG Data Analysis with MNE-Python.
  *Front. Neurosci.*, 7, 267.
- Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python.
  *JMLR*, 12, 2825–2830.

**Links úteis**

- Dataset: https://physionet.org/content/eegmmidb/1.0.0/
- MOABB: https://moabb.neurotechx.com/docs/index.html

---

## 16. Roadmap e gatilhos de atualização

O que está planejado (`ROADMAP.md`, seção "Future") e o post que cada entrega
permitiria:

| Entrega futura | Post que ela permite |
| --- | --- |
| Benchmark com os 109 sujeitos | "A variação entre pessoas se mantém em escala?" (comparar com os números da v1) |
| Avaliação cross-subject | "O que acontece quando o modelo encontra uma pessoa nova" (provavelmente o post mais forte da série) |
| Ajuste com validação cruzada aninhada | "Como ajustar hiperparâmetros sem trapacear" |
| Pipelines Riemannianos (Covariance+MDM, TangentSpace+LR) | "Geometria de matrizes de covariância em BCI": testa a hipótese da §5.3 |
| Deep learning (EEGNet, Braindecode) | "Deep learning contra baselines honestos" |
| Dashboard de biossinais em tempo real / BrainFlow (projeto separado) | Mudança de escopo: de benchmark offline para sistema online |

**Regra:** cada atualização deve comparar com os números da v1 (§4) usando o
mesmo protocolo, ou declarar com clareza o que mudou.

---

## 17. Conexão com o portfólio

Este é um de três projetos públicos que formam uma narrativa coerente:

| Projeto | Pergunta que responde | Data |
| --- | --- | --- |
| [EEG Signal Processing Lab](https://github.com/jevrton-code/eeg-signal-processing-lab) | Como carregar, inspecionar, pré-processar e analisar EEG de forma responsável? | jun. 2026 |
| **BCI Motor Imagery Classifier** (este) | Dá para classificar imagética motora, e como avaliar isso com honestidade? | jun. 2026 |
| [FlyWire Propagation Sim](https://github.com/jevrton-code/flywire-propagation-sim) | Como a atividade se espalha por um circuito neural real, mapeado sinapse a sinapse? | ago. 2026 |

**O fio condutor:** dados públicos reais, reprodutibilidade, engenharia de
software disciplinada e honestidade sobre os limites. O EEG Lab e este projeto
usam o **mesmo dataset** (PhysioNet EEGMMIDB): o primeiro entende o sinal, o
segundo constrói classificadores sobre ele. O FlyWire sai do sinal medido no
couro cabeludo e vai para o diagrama de fiação do cérebro, com uma aplicação
full-stack.

**Post de portfólio possível:** "Três projetos, uma regra: escrever o que o
modelo não faz antes de mostrar o que ele faz."

---

## 18. Pendências encontradas antes de divulgar

Pontos do repositório que um visitante vindo do LinkedIn pode notar. Vale
corrigir antes de um post de lançamento.

1. **URLs de exemplo no `pyproject.toml`:** `Homepage` e `Repository` apontam
   para `github.com/your-org/...`. Trocar por `jevrton-code`.
2. **Versão desatualizada no `CITATION.md`:** a citação do repositório diz
   "Version 0.1.0"; o pacote está em 1.0.0.
3. **Testes são placeholders:** os 4 testes estão marcados como `skip`
   (verificado: `4 skipped`). Implementar testes reais de configuração,
   esquema de resultados e resumo de métricas daria um post de "v1.1".
4. **Links para `docs/`, que não está no repositório:** o README cita
   `docs/evaluation_protocol.md` e o relatório cita `docs/limitations.md`, mas
   `docs/` está no `.gitignore` (documentos locais). Para quem visita, são
   links quebrados.
5. **Legenda sobreposta** em `figures/per_subject_scores.png` (§10).
6. **Pasta `notebooks/` vazia** (notebooks marcados como planejados).
7. **Sem tag nem release no GitHub.** Criar a release `v1.0.0` dá um link
   estável e um marco para anunciar.
8. **Sem imagem de *social preview*** configurada no GitHub (§10).

---

## 19. Contexto pessoal a preencher (o que o repositório não sabe)

Posts com contexto pessoal costumam soar mais autênticos. Preencha o que fizer
sentido:

- **Por que este projeto:** [A PREENCHER]
- **Sua formação e trajetória até aqui:** [A PREENCHER]
- **Tempo dedicado e contexto** (projeto pessoal, curso, transição de
  carreira): [A PREENCHER]
- **O que foi mais difícil ou mais surpreendente:** [A PREENCHER]
- **Ferramentas usadas no processo**, incluindo assistentes de IA, se quiser
  mencionar: [A PREENCHER]
- **Objetivo profissional** (tipo de vaga, área, empresas de interesse):
  [A PREENCHER]
- **Pessoas ou comunidades para agradecer ou marcar:** [A PREENCHER]
- **URL do seu perfil no LinkedIn:** [A PREENCHER]

---

## 20. Registro de alterações deste documento

| Data | Alteração |
| --- | --- |
| 2026-10-29 | Versão inicial, cobrindo o projeto na v1.0.0 (`beba3ba`). Números conferidos contra `results/*.csv`; testes executados localmente (`4 skipped`). |
