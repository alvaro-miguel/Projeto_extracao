import os
import pdfplumber
import customtkinter as ctk
from tkinter import filedialog, messagebox
from auxiliares import remicao_obras_lidas,remicao_estudo,remicao_trabalho,calcular_remicao,converter_dias
from padroes import padroes_estudo,padroes_leitura,padroes_trabalho,palavras_proibidas,padroes_pena
from extracao import contabilizar, obter_pena

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CARP - Calculadora Auxiliar de Remição Penal")
        self.geometry("1400x800")
        self.minsize(900, 600)

        self.cor_trabalho = "#A5D6A7"  
        self.cor_estudo = "#90CAF9"    
        self.cor_leitura = "#CE93D8"   
        self.cor_pena = "#FFE082"      
        self.cor_erro = "#F44336"
        self.cor_texto = "#000000"

        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)  
        self.grid_columnconfigure(1, weight=1)  
        self.grid_rowconfigure(0, weight=1)

        self.frame_esquerdo = ctk.CTkFrame(self, corner_radius=10)
        self.frame_esquerdo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_esquerdo.grid_rowconfigure(0, weight=1)
        self.frame_esquerdo.grid_columnconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(
            self.frame_esquerdo,
            wrap="word",
            font=("Courier", 13),
            corner_radius=10,
        )
        self.textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.textbox.insert("1.0", "Selecione um arquivo PDF para iniciar.")
        self.textbox.configure(state="disabled")

        self.frame_direito = ctk.CTkFrame(self, corner_radius=10)
        self.frame_direito.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.frame_direito.grid_columnconfigure(0, weight=1)

        self.btn_selecionar = ctk.CTkButton(
            self.frame_direito,
            text="Selecionar PDF",
            command=self.selecionar_pdf,
            height=40,
            corner_radius=10,
        )
        self.btn_selecionar.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        ctk.CTkLabel(self.frame_direito, text="Pena Original", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=20, sticky="w")
        self.lbl_pena_valor = ctk.CTkLabel(self.frame_direito, text="---", font=("Arial", 20, "bold"))
        self.lbl_pena_valor.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="w")

        ctk.CTkLabel(self.frame_direito, text="Detalhamento das Atividades", font=("Arial", 14, "bold")).grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.lbl_trabalho = ctk.CTkLabel(self.frame_direito, text="", text_color=self.cor_trabalho, anchor="w")
        self.lbl_trabalho.grid(row=4, column=0, padx=20, sticky="w")

        self.lbl_estudo = ctk.CTkLabel(self.frame_direito, text="", text_color=self.cor_estudo, anchor="w")
        self.lbl_estudo.grid(row=5, column=0, padx=20, sticky="w")

        self.lbl_leitura = ctk.CTkLabel(self.frame_direito, text="", text_color=self.cor_leitura, anchor="w")
        self.lbl_leitura.grid(row=6, column=0, padx=20, sticky="w")

        self.lbl_total_remido = ctk.CTkLabel(self.frame_direito, text="", font=("Arial", 14, "bold"))
        self.lbl_total_remido.grid(row=7, column=0, padx=20, pady=10, sticky="w")

        ctk.CTkLabel(self.frame_direito, text="Provável Nova Pena", font=("Arial", 14, "bold")).grid(row=8, column=0, padx=20, sticky="w")
        self.lbl_nova_pena_valor = ctk.CTkLabel(self.frame_direito, text="---", font=("Arial", 30, "bold"), text_color="#66BB6A")
        self.lbl_nova_pena_valor.grid(row=9, column=0, padx=20, pady=(0, 20), sticky="w")


    def extrair_e_mostrar_evidencias(self, texto, evidencias, cor, titulo):
        if not evidencias:
            return

        self.textbox.insert("end", f"\n>>> {titulo} <<<\n")
        
        posicoes_ordenadas = sorted(evidencias)
        inicio_janela = max(0, posicoes_ordenadas[0][0] - 100)
        fim_janela = min(len(texto), posicoes_ordenadas[-1][1] + 100)
        trecho = texto[inicio_janela:fim_janela]

        tag_name = f"tag_{cor}"
        self.textbox.tag_config(tag_name, background=cor, foreground=self.cor_texto)

        pos_referencia = self.textbox.index("end-1c")
        self.textbox.insert("end", trecho + "\n")

        for inicio, fim in evidencias:
            rel_inicio = inicio - inicio_janela
            rel_fim = fim - inicio_janela
            start_idx = f"{pos_referencia}+{rel_inicio}c"
            end_idx = f"{pos_referencia}+{rel_fim}c"
            self.textbox.tag_add(tag_name, start_idx, end_idx)


    def selecionar_pdf(self):
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        if not caminho:
            return

        self.btn_selecionar.configure(state="disabled", text="Processando...")
        self.update_idletasks()

        try:
            self.processar_pdf(caminho)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao processar arquivo: {str(e)}")
        finally:
            self.btn_selecionar.configure(state="normal", text="Selecionar PDF")


    def processar_pdf(self, caminho):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")

        texto = ''
        with pdfplumber.open(caminho) as arquivo:
            for pagina in arquivo.pages:
                texto += pagina.extract_text() + '\n'

        tempo_trab, evid_trab = contabilizar(texto, padroes_trabalho, palavras_proibidas)
        tempo_est, evid_est = contabilizar(texto, padroes_estudo, palavras_proibidas)
        leitura, evid_lei = contabilizar(texto, padroes_leitura, palavras_proibidas)
        resultado_pena = obter_pena(texto, padroes_pena)

        rem_trab = remicao_trabalho(tempo_trab)
        rem_est = remicao_estudo(tempo_est)
        rem_lei = remicao_obras_lidas(leitura)
        rem_total = calcular_remicao(rem_trab, rem_est, rem_lei)

        self.extrair_e_mostrar_evidencias(texto, evid_trab, self.cor_trabalho, "TRABALHO")
        self.extrair_e_mostrar_evidencias(texto, evid_est, self.cor_estudo, "ESTUDO")
        self.extrair_e_mostrar_evidencias(texto, evid_lei, self.cor_leitura, "LEITURA")

        if resultado_pena:
            pena, evid_pena = resultado_pena
            self.extrair_e_mostrar_evidencias(texto, evid_pena, self.cor_pena, "PENA")
            
            self.lbl_pena_valor.configure(text=f"{pena['anos']}a, {pena['meses']}m e {pena['dias']}d")
            
            dias_totais = pena['pena_dias_totais']
            nova_pena_dias = max(0, dias_totais - rem_total)
            an, mn, dn = converter_dias(nova_pena_dias)
            
            self.lbl_nova_pena_valor.configure(text=f"{an} anos, {mn} meses e {dn} dias")
        else:
            self.lbl_pena_valor.configure(text="Pena não localizada")

        self.lbl_trabalho.configure(text=f"Trabalho: {tempo_trab} dias → Remição: {rem_trab}d")
        self.lbl_estudo.configure(text=f"Estudo: {tempo_est} horas → Remição: {rem_est}d")
        self.lbl_leitura.configure(text=f"Leitura: {leitura} obras → Remição: {rem_lei}d")
        self.lbl_total_remido.configure(text=f"TOTAL REMIDO: {rem_total} dias")

        self.textbox.configure(state="disabled")


if __name__ == "__main__":
    app = App()
    app.mainloop()