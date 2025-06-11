# Requisitos do App

## 1. Introdução

Este documento detalha os requisitos funcionais e não funcionais para o aplicativo Appoia, divididos pelos principais atores do sistema: o Pai/Cuidador e a Criança.

## 2. Atores e Usuários

Nesta seção, descrevemos os principais atores que interagem com o sistema Appoia.

* **Pai/Cuidador:**
  * **Descrição:** É o usuário principal do aplicativo, responsável por configurar e gerenciar o conteúdo para a criança. Geralmente é um adulto com diferentes níveis de familiaridade com tecnologia que busca organização e uma ferramenta para motivar seus filhos.
  * **Responsabilidades:** Cadastrar filhos, criar e gerenciar tarefas, eventos, recompensas e rotas. Acompanhar o progresso da criança.

* **Criança:**
  * **Descrição:** É o usuário final do aplicativo, com idade entre 5 e 12 anos. Interage com o sistema de forma mais passiva, consumindo o conteúdo criado pelos pais. O foco da sua interface é ser divertida, clara e motivadora.
  * **Responsabilidades:** Visualizar tarefas, eventos e rotas. Marcar tarefas como concluídas e resgatar recompensas.

## 3. Regras de Negócio

| ID   | Regra de Negócio                                                                                              |
| ---- | ------------------------------------------------------------------------------------------------------------- |
| RN01 | Uma criança só pode resgatar uma recompensa se seu saldo de pontos for maior ou igual ao custo da recompensa. |
| RN02 | Ao resgatar uma recompensa, os pontos correspondentes ao custo devem ser subtraídos do saldo da criança.      |
| RN03 | O valor em pontos de uma tarefa não pode ser um número negativo.                                              |
| RN04 | Uma tarefa marcada como "concluída" não pode ser marcada como "concluída" novamente.                          |

## 4. Requisitos Funcionais (RF)

### 4.1 Ator: Pais/Cuidador

Os Requisitos Funcionais definem as funcionalidades que o sistema deve oferecer. No contexto do Appoia, eles descrevem as **ações** que os usuários (Pai/Cuidador e Criança) podem realizar dentro do aplicativo. Isso inclui desde "criar uma nova tarefa" e "definir uma recompensa" por parte do pai, até "visualizar o calendário" e "marcar uma tarefa como concluída" por parte da criança.

| ID        | Requisito                                                                                                                                |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| RF-PAI-01 | O sistema deve exibir uma tela inicial com uma mensagem de boas-vindas e o nome do pai/cuidador.                                         |
| RF-PAI-02 | O sistema deve apresentar um menu de navegação lateral (☰) com acesso às seções principais da área de gerenciamento.                     |
| RF-PAI-03 | Na seção "Meus Filhos", o sistema deve exibir a lista de filhos associados à conta e permitir a adição de novos perfis de filhos.        |
| RF-PAI-04 | Na seção "Definir Tarefas", o sistema deve permitir ao pai/cuidador criar uma nova tarefa, definindo sua descrição e o valor em pontos.  |
| RF-PAI-05 | O sistema deve permitir que o pai/cuidador edite e exclua tarefas existentes.                                                            |
| RF-PAI-06 | O sistema deve permitir que o pai/cuidador marque manualmente uma tarefa como "concluída".                                               |
| RF-PAI-07 | Na seção "Definir Recompensas", o sistema deve permitir ao pai/cuidador criar uma nova recompensa, definindo seu nome e custo em pontos. |
| RF-PAI-08 | O sistema deve permitir que o pai/cuidador edite e exclua recompensas existentes.                                                        |
| RF-PAI-09 | Na seção "Definir Eventos", o sistema deve permitir que o pai/cuidador crie novos eventos para os filhos.                                |
| RF-PAI-10 | Na seção "Definir Rotas", o sistema deve permitir que o pai/cuidador crie novas rotas para os filhos visualizarem.                       |
| RF-PAI-11 | O sistema deve fornecer uma visualização em "Calendário" que exiba os eventos e tarefas agendados.                                       |
| RF-PAI-12 | Na seção "Notificações", o sistema deve exibir um histórico de recompensas que foram resgatadas pelos filhos.                            |
| RF-PAI-13 | O sistema deve fornecer relatórios simples para o acompanhamento do progresso dos filhos no cumprimento das tarefas.                     |

### 4.2 Ator: Criança

| ID        | Requisito                                                                                                                                                      |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RF-CRI-01 | O sistema deve exibir uma tela inicial com uma mensagem de boas-vindas e os dados do perfil da criança (nome e imagem).                                        |
| RF-CRI-02 | O sistema deve apresentar um menu de navegação lateral (☰) com acesso às seções: Início, Meus Eventos, Minhas Tarefas, Recompensas, Minhas Rotas e Calendário. |
| RF-CRI-03 | Na seção "Minhas Tarefas", o sistema deve exibir a lista de tarefas da criança, indicando seu status (ex: concluída, pendente).                                |
| RF-CRI-04 | O sistema deve permitir que a criança marque uma tarefa como "concluída".                                                                                      |
| RF-CRI-05 | Ao selecionar uma tarefa, o sistema deve exibir seus detalhes: status, pontos ganhos e prazo limite para realização.                                           |
| RF-CRI-06 | Na seção "Recompensas", o sistema deve exibir as recompensas, seu custo em pontos e seu status de disponibilidade (disponível ou não disponível).              |
| RF-CRI-07 | O sistema deve permitir que a criança resgate uma recompensa disponível utilizando seus pontos acumulados.                                                     |
| RF-CRI-08 | Na seção "Meus Eventos", o sistema deve permitir que a criança visualize os eventos futuros criados pelo pai/cuidador.                                         |
| RF-CRI-09 | Na seção "Minhas Rotas", o sistema deve exibir um mapa (via integração, ex: Google Maps) mostrando o trajeto de um local definido pelo pai/cuidador.           |
| RF-CRI-10 | O sistema deve fornecer uma visualização em "Calendário" que consolide as tarefas e eventos da criança por data.                                               |

## 5. Requisitos Não Funcionais (RNF)

Os Requisitos Não Funcionais descrevem as qualidades e restrições do sistema. Eles não se referem ao "que" o aplicativo faz, mas sim a "**como**" ele faz. Para o Appoia, essas são as características que definem a qualidade geral da experiência, como garantir que o aplicativo seja fácil de usar (Usabilidade), rápido (Desempenho) e que os dados das crianças estejam protegidos (Segurança).

| ID    | Categoria        | Requisito                                                                                                                                                                 |
| ----- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RNF01 | Usabilidade      | A interface do aplicativo deve ser simples, clara e intuitiva, adequada para usuários com diferentes níveis de familiaridade tecnológica.                                 |
| RNF02 | Acessibilidade   | O design e a apresentação da rotina devem ser visualmente claros para ajudar na antecipação e reduzir a ansiedade em crianças autistas.                                   |
| RNF03 | Desempenho       | As interações principais do usuário, como abrir uma tela ou marcar uma tarefa, devem ter um tempo de resposta inferior a 2 segundos para garantir uma experiência fluida. |
| RNF04 | Confiabilidade   | O sistema deve garantir a sincronização de dados entre os dispositivos dos pais e filhos sem perda de informações, quando conectado à internet.                           |
| RNF05 | Segurança        | Os dados dos usuários e das crianças devem ser armazenados de forma segura, e o acesso ao aplicativo deve ser protegido por um sistema de autenticação (login e senha).   |
| RNF06 | Portabilidade    | O sistema deve ser desenvolvido como um aplicativo móvel.                                                                                                                 |
| RNF07 | Conectividade    | O funcionamento completo do aplicativo, incluindo a sincronização de dados e o envio de notificações, depende de uma conexão ativa com a internet.                        |
| RNF08 | Manutenibilidade | O código-fonte deve seguir padrões de desenvolvimento claros para facilitar futuras atualizações e correções pela equipe.                                                 |

## 6. Glossário

* **Tarefa:** Uma atividade a ser realizada pela Criança, que pode gerar pontos ao ser concluída.
* **Recompensa:** Um prêmio que a Criança pode "comprar" utilizando os pontos acumulados.
* **Evento:** Um compromisso com data e hora definidos, como "Consulta médica" ou "Aula de natação".
* **Rotina:** Um conjunto de tarefas ou eventos que se repetem.
