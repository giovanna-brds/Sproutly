# 🌱 Sproutly

## 📝 Descrição do Projeto
O Sproutly é uma aplicação desktop de produtividade desenvolvida em Python com o objetivo de transformar o tempo de foco em uma representação visual de progresso.

A ideia surgiu a partir da minha própria experiência estudando para o vestibular e praticando programação. Embora cronômetros ajudassem a acompanhar o tempo dedicado aos estudos, percebi que algumas ferramentas de produtividade também podiam incentivar uma comparação constante com outras pessoas.

A partir disso, o Sproutly foi pensado como uma alternativa mais pessoal: em vez de comparar horas estudadas, o usuário acompanha o próprio progresso por meio de um jardim que cresce conforme o tempo de foco aumenta.

---

## ⚙️ Funcionalidades do Projeto
* **Cronômetro de Foco:** Permite acompanhar o tempo de estudo em dois modos: Livre, com contagem progressiva, e Pomodoro, com períodos de foco predefinidos.
* **Jardim de Progresso:** O tempo de foco é convertido em progresso visual, fazendo com que as plantas passem por diferentes estágios de crescimento.
* **Lista de Tarefas:** Permite adicionar tarefas diretamente à interface e marcá-las como concluídas.
* **Acompanhamento de Tempo:** Exibe o tempo total de foco ativo durante as sessões.
* **Progresso Individual:** O aplicativo utiliza o crescimento do jardim como representação do progresso do próprio usuário, sem rankings ou comparação com outras pessoas.
* **Interface em Pixel Art:** Interface desenvolvida a partir de um protótipo criado no Figma, utilizando elementos visuais em pixel art para construir a identidade do aplicativo.
---

## 🧪 Testes de Software
* Teste de Funcionamento: Verificação do funcionamento dos controles de iniciar, pausar e reiniciar o cronômetro.
* Teste dos Modos de Foco: Validação do comportamento dos modos Livre e Pomodoro, incluindo a contagem progressiva e regressiva do tempo.
* Teste de Progressão: Verificação da alteração dos estágios das plantas conforme o tempo de foco aumenta.
* Teste de Interface: Validação dos eventos de interação, troca de abas, seleção de tarefas e atualização dos elementos visuais.
* Teste de Estados: Verificação das diferentes situações do cronômetro, como ativo, pausado e reiniciado.
---

## 🛠️ Tecnologias e Linguagens
- **Python**


---

## 📚 Bibliotecas e Frameworks
* **Tkinter** — Construção da interface gráfica e gerenciamento das interações.
* **Pillow (PIL)** — Manipulação de imagens, redimensionamento dos assets e renderização de elementos visuais.
* **Figma** — Prototipação e desenvolvimento da interface visual.

---


## 🌱 Estado Atual

O Sproutly está atualmente em desenvolvimento e sua versão disponível funciona como um protótipo funcional.

As principais funcionalidades da proposta já foram implementadas, incluindo o cronômetro, os modos Livre e Pomodoro, a evolução visual das plantas, a lista de tarefas e o acompanhamento do tempo ativo.

O projeto ainda possui espaço para evolução, principalmente na personalização do jardim, no sistema de tarefas e na relação entre o tempo de foco e o crescimento das plantas.

---

## 🚀 Próximos Passos

* Implementar um sistema mais completo de tarefas e progresso.
* Adicionar diferentes espécies e estágios de plantas.
* Permitir maior personalização do jardim.
* Criar novas interações com os elementos do ambiente.
* Implementar persistência dos dados do usuário.
* Adicionar um histórico de sessões de foco.
* Refinar animações e transições da interface.
* Explorar melhorias de acessibilidade e experiência do usuário.

---

##  📦 Pré-requisitos e Instalação

### Pré-requisitos

* Python 3.x
* pip

### Passo a passo para clonar e instalar
```bash
# 1. Clone o repositório
git clone https://github.com/SEU-USUARIO/sproutly.git
# 2. Acesse a pasta do projeto
cd sproutly
# 3. Instale as dependências
pip install -r requirements.txt
```
---

## 🚀 Instruções de Uso
```bash
 1. Execute o arquivo principal
python gui.py
```
Após iniciar o aplicativo, escolha entre os modos Livre ou Pomodoro, 
inicie uma sessão de foco e acompanhe o crescimento do seu jardim 
conforme o tempo passa.

---

## 📖 Documentação

Para a construção deste projeto, foram consultadas documentações e materiais de referência relacionados às tecnologias utilizadas, principalmente:

* Tkinter — Construção da interface gráfica e gerenciamento de eventos.
* Python — Estruturação da lógica da aplicação.
* Pillow — Manipulação e renderização de imagens.
* Figma — Prototipação e planejamento da interface.

---

## 📄 Licença

Este projeto possui Licença MIT e foi desenvolvido para fins educacionais e de portfólio. O código pode ser utilizado e modificado conforme os termos da licença, com a devida atribuição ao desenvolvedor original.
