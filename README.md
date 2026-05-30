# ⚖️ CARP - Calculadora Auxiliar de Remição Penal

O **CARP** é um software desenvolvido para automatizar a extração e o cálculo de dados de remição penal a partir de documentos jurídicos não estruturados (PDFs). Utilizando técnicas de Processamento de Linguagem Natural (NLP) baseadas em Expressões Regulares (Regex) e uma interface gráfica interativa, o sistema localiza, contabiliza e converte dias de trabalho, horas de estudo e obras lidas em dias remidos, calculando a provável nova pena do indivíduo.

Este projeto foi desenvolvido como escopo acadêmico/prático para o **Instituto Federal do Piauí (IFPI) - Campus Teresina Central**.

---

## ✨ Funcionalidades

* **Extração Automatizada (PDF):** Leitura nativa de arquivos PDF de sentenças e relatórios judiciais.
* **Processamento via Regex:** Identificação inteligente de padrões de texto para localizar a pena original e as atividades de remição, ignorando falsos positivos (como artigos de lei ou numerações de processos).
* **Cálculo de Remição (LEP):** Aplicação automática das regras da Lei de Execução Penal:
  * 💼 **Trabalho:** 1 dia remido a cada 3 dias trabalhados.
  * 📚 **Estudo:** 1 dia remido a cada 12 horas de estudo.
  * 📖 **Leitura:** 4 dias remidos por obra literária lida (limitado a 12 obras anuais).
* **Auditoria Visual:** Interface gráfica que destaca as evidências exatas encontradas no documento original, codificadas por cores, garantindo transparência nos dados extraídos.
* **Conversão de Tempo Precisa:** Utilização do fator de conversão de `30.4375` dias por mês para cálculos judiciais exatos.


## 🚀 Tecnologias Utilizadas

* **Python
* **pdfplumber:** Extração confiável de texto a partir de arquivos PDF.
* **CustomTkinter:** Interface Gráfica de Usuário (GUI) moderna e reativa.
* **re (Regular Expressions):** Módulo nativo do Python para o motor de busca heurística.

---

## ⚙️ Pré-requisitos e Instalação

Certifique-se de ter o Python instalado em sua máquina. Para rodar o projeto localmente (seja em ambientes Windows ou Linux/Zorin OS), siga os passos abaixo:

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/alvaro-miguel/Projeto_extracao.git](https://github.com/alvaro-miguel/Projeto_extracao.git)