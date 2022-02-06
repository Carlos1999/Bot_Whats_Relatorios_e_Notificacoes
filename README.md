# BOT do Whats - Relatórios e Notificações :robot:
### 📑 Descrição:

​	O bot do whatsapp utiliza o **whatsapp web** através do **selenium**, que é uma ferramenta de automação de tarefas utilizando o navegador, para poder automatizar a entrega via whats de alguns **relatórios** e também de **notificações**, ambos gerados através de scripts **python**, que pegam os dados de diversas fontes, realizam o tratamento e constroem de forma automática a estrutura das **notificações e os relatórios em PDF**, para posteriormente enviar para o destinatário correto.

Abaixo os scripts responsáveis pelo funcionamento geral:

* **Script - [classe_whats](https://github.com/SEPLAN-RN/BOT-Whats-e-Relatorios-Contratos/blob/main/classe_whats.py)**: Esse script possui a classe **Zapbot**, que é responsável por controlar toda a parte do **selenium**, com métodos que possibilitam toda a manipulação do **whatsapp web** através do navegador **firefox**, sendo possível transitar entre conversas, perceber e abrir novas mensagens recebidas, enviar mensagens e arquivos.

* **Script - [classe_comandos](https://github.com/SEPLAN-RN/BOT-Whats-e-Relatorios-Contratos/blob/main/classe_comandos.py):** A classe comandos é responsável por conter todos os **métodos** que serão chamados para executar os **comandos**, cada comando possui um método na classe Comandos, chamando outros scripts, que são importados no classe_comandos para poderem ser chamados quando necessário, e utilizando uma instância da classe **Zapbot** para enviar as **mensagens e arquivos.**

* **Script - [Bot_whats_geral](https://github.com/SEPLAN-RN/BOT-Whats-e-Relatorios-Contratos/blob/main/Bot_whats_geral.py):** O script que será executado para iniciar **todo o funcionamento** do bot, ele é responsável por gerenciar todo o **loop de funcionamento**, chamando os outros scripts sempre que necessário. Nele existe uma estrutura em loop que procura por **novas mensagens em suas conversas**, caso encontre uma nova mensagem ele irá ler para depois comparar com os comandos já existentes, caso aquela mensagem seja um comando será chamado um dos métodos da **classe_comandos** referente a aquele comando que foi dado.



 ![imagem](https://github.com/Carlos1999/Bot_Whats_Relatorios_e_Notificacoes/blob/main/Relatorios/figuras/WhatsApp%20-%20Opera%202022-02-04%2014-26-31.gif)

### :notebook_with_decorative_cover: Documentação e Tutoriais:

* Para mais informações a respeito do funcionamento dos scripts principais e sobre como utilizar todos em conjunto verifique o arquivo **[Documentação - Principais Scripts.pdf](https://github.com/SEPLAN-RN/BOT-Whats-e-Relatorios-Contratos/blob/main/Documentação%20-%20Principais%20Scripts.pdf)**.

* Para aprender a criar relatórios automáticos com **PDFKit** utilizando **python**, verifique o notebook **[Notebook_Tutorial_Criacao_de_Relatorios.ipynb](https://github.com/SEPLAN-RN/BOT-Whats-e-Relatorios-Contratos/blob/main/Notebook_Tutorial_Criacao_de_Relatorios.ipynb)**.
* Para aprender a utilizar a [classe_whats](https://github.com/SEPLAN-RN/BOT-Whats-e-Relatorios-Contratos/blob/main/classe_whats.py) para manipular o **whatsapp web** e criar um bot com respostas predefinidas, **notificações** e envio de arquivos automáticos ou através de **comandos,** verifique o notebook [**Notebook_Tutorial_Uso_da_classe_whats.ipynb**](https://github.com/SEPLAN-RN/BOT-Whats-e-Relatorios-Contratos/blob/main/Notebook_Tutorial_Uso_da_classe_whats.ipynb)

​	

### :hammer_and_wrench:Ferramentas Utilizadas:

​	Linguagem ***Python*** com as seguintes principais bibliotecas:

* ***Selenium***;

* ***PDFKit;***

* ***Pandas;***



### :fast_forward: Passo a Passo Para a Reprodução 

​	Instalar bibliotecas necessárias:

* **Selenium:** `!pip install selenium`;
* **PDFKit:** `!pip install pdfkit`;
* Instalar [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) versão 0.12.5-1;
* Abrir arquivo **inicia_bot_whats - servidor.bat** para definir caminho do Python que deseja utilizar;
* Executar arquivo **inicia_bot_whats - servidor.bat**.



## 👨‍💻 Autor:

* Carlos Vinícius dos Santos ([@Carlos1999](https://github.com/carlos1999)), email para contato cvcsantos14@gmail.com 

  

### :book: Sobre o Projeto:

​	O projeto foi desenvolvido enquanto atuei como estagiário na [Secretaria de Estado de Planejamento e das Finanças - SEPLAN](http://www.seplan.rn.gov.br), como parte do projeto [Governo Cidadão](http://www.governocidadao.rn.gov.br/?pg=sobre_o_projeto), no setor de monitoramento, no qual realizava atividades de criação de ferramentas para auxiliar a gerência no acompanhamento da execução e controle de prazos das atividades gerenciadas. 

​	O bot foi utilizado como uma das principais ferramentas de monitoramento, a partir do momento em que foi possível colocar em prática a entrega de notificações personalizadas automaticamente para cada destino necessário e também a criação de relatórios gerados a partir de dados atualizados no momento em que eram solicitados através de comandos no bot.





