#CRIADO E DESENVOLVIDO POR WELINGTON FERNANDES

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import json
import os
import hashlib

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Cores do tema
COLORS = {
    "primary": "#6366F1",
    "primary_hover": "#4F46E5",
    "success": "#22C55E",
    "success_hover": "#16A34A",
    "danger": "#EF4444",
    "danger_hover": "#DC2626",
    "aviso": "#F59E0B",
    "warning_hover": "#D97706",
    "bg_dark": "#0F172A",
    "bg_card": "#1E293B",
    "bg_card_alt": "#334155",
    "text": "#F8FAFC",
    "text_muted": "#94A3B8",
    "border": "#475569",
}

# Ícones
ICONES = {
    "dinheiro": "💰",
    "entrada": "📈",
    "despesa": "📉",
    "calendario": "📆",
    "adicionar": "➕",
    "lista": "📋",
    "grafico": "📊",
    "relatorio": "📑",
    "ano": "🗓️",
    "salvar": "💾",
    "excluir": "🗑️",
    "atualizar": "🔄",
    "sucesso": "✅",
    "aviso": "⚠️",
    "arquivo": "📁",
    "estatisticas": "📈",
    "usuario": "👤",
    "cadeado": "🔒",
    "entrar": "🚀",
    "cadastrar": "📝",
    "sair": "🚪",
}


class GerenciadorUsuarios:
    def __init__(self, arquivo="dados.json"):
        self.arquivo = arquivo
        self.dados = {"usuarios": [], "transacoes": []}
        self.usuario_logado = None
        self.carregar_dados()
        self.criar_usuario_padrao()

    def carregar_dados(self):
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    # Migrar dados antigos (lista de transações) para novo formato
                    if isinstance(dados, list):
                        self.dados = {"usuarios": [], "transacoes": dados}
                        self.salvar_dados()
                    else:
                        self.dados = dados
            except Exception:
                self.dados = {"usuarios": [], "transacoes": []}
        else:
            self.dados = {"usuarios": [], "transacoes": []}

    def salvar_dados(self):
        try:
            with open(self.arquivo, "w", encoding="utf-8") as f:
                json.dump(self.dados, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def hash_senha(self, senha):
        return hashlib.sha256(senha.encode()).hexdigest()

    def criar_usuario_padrao(self):
        # Criar usuário padrão se não existir nenhum usuário
        if not self.dados["usuarios"]:
            self.criar_usuario("w3ll", "301520")

    def criar_usuario(self, usuario, senha):
        # Verificar se usuário já existe
        for u in self.dados["usuarios"]:
            if u["usuario"].lower() == usuario.lower():
                return False, "Usuário já existe!"

        # Criar novo usuário
        novo_usuario = {
            "usuario": usuario,
            "senha": self.hash_senha(senha),
            "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        self.dados["usuarios"].append(novo_usuario)
        self.salvar_dados()
        return True, "Usuário criado com sucesso!"

    def validar_login(self, usuario, senha):
        senha_hash = self.hash_senha(senha)
        for u in self.dados["usuarios"]:
            if u["usuario"].lower() == usuario.lower() and u["senha"] == senha_hash:
                self.usuario_logado = u["usuario"]
                return True
        return False

    def obter_transacoes(self):
        return self.dados.get("transacoes", [])

    def adicionar_transacao(self, transacao):
        self.dados["transacoes"].append(transacao)
        self.salvar_dados()

    def excluir_transacao(self, indice):
        if 0 <= indice < len(self.dados["transacoes"]):
            self.dados["transacoes"].pop(indice)
            self.salvar_dados()
            return True
        return False


class TelaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"{ICONES['dinheiro']} Controle Financeiro - Entrar")
        self.geometry("500x720")
        self.configure(fg_color=COLORS["bg_dark"])
        self.resizable(False, False)

        self.gerenciador = GerenciadorUsuarios()

        # Centralizar janela
        self.center_window()

        # Container principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=(30, 10))

        self.criar_tela_login()

        # Créditos
        self.criar_creditos()

    def center_window(self):
        self.update_idletasks()
        width = 500
        height = 720
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def criar_creditos(self):
        creditos_frame = ctk.CTkFrame(self, fg_color="transparent")
        creditos_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            creditos_frame,
            text="Desenvolvido por: Welington Fernandes",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"]
        ).pack()

        ctk.CTkLabel(
            creditos_frame,
            text="📞 (11) 95316-4286",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"]
        ).pack()

    def limpar_tela(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def criar_tela_login(self):
        self.limpar_tela()

        # Logo
        ctk.CTkLabel(
            self.main_frame, text=ICONES["dinheiro"],
            font=ctk.CTkFont(size=64)
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            self.main_frame, text="Controle Financeiro",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=COLORS["text"]
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            self.main_frame, text="Gerencie suas finanças com facilidade",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_muted"]
        ).pack(pady=(0, 40))

        # Card de login
        card = ctk.CTkFrame(self.main_frame, fg_color=COLORS["bg_card"], corner_radius=20)
        card.pack(fill="x", pady=10)

        ctk.CTkLabel(
            card, text=f"{ICONES['entrar']} Entrar",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(25, 20))

        # Usuário
        user_frame = ctk.CTkFrame(card, fg_color="transparent")
        user_frame.pack(fill="x", padx=30, pady=(0, 10))

        ctk.CTkLabel(
            user_frame, text=f"{ICONES['usuario']} Usuário",
            font=ctk.CTkFont(size=13), text_color=COLORS["text_muted"]
        ).pack(anchor="w")

        self.login_user = ctk.CTkEntry(
            user_frame, placeholder_text="Digite seu usuário",
            height=48, corner_radius=12, font=ctk.CTkFont(size=14),
            border_width=2, border_color=COLORS["border"]
        )
        self.login_user.pack(fill="x", pady=(5, 0))

        # Senha
        pass_frame = ctk.CTkFrame(card, fg_color="transparent")
        pass_frame.pack(fill="x", padx=30, pady=(10, 0))

        ctk.CTkLabel(
            pass_frame, text=f"{ICONES['cadeado']} Senha",
            font=ctk.CTkFont(size=13), text_color=COLORS["text_muted"]
        ).pack(anchor="w")

        self.login_pass = ctk.CTkEntry(
            pass_frame, placeholder_text="Digite sua senha", show="●",
            height=48, corner_radius=12, font=ctk.CTkFont(size=14),
            border_width=2, border_color=COLORS["border"]
        )
        self.login_pass.pack(fill="x", pady=(5, 0))
        self.login_pass.bind("<Return>", lambda e: self.fazer_login())

        # Botão login
        ctk.CTkButton(
            card, text=f"{ICONES['entrar']}  Entrar", height=50,
            corner_radius=12, font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
            command=self.fazer_login
        ).pack(fill="x", padx=30, pady=25)

        # Separador
        sep_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        sep_frame.pack(fill="x", pady=20)

        ctk.CTkFrame(sep_frame, height=2, fg_color=COLORS["border"]).pack(side="left", fill="x", expand=True, padx=(0, 15))
        ctk.CTkLabel(sep_frame, text="ou", text_color=COLORS["text_muted"]).pack(side="left")
        ctk.CTkFrame(sep_frame, height=2, fg_color=COLORS["border"]).pack(side="left", fill="x", expand=True, padx=(15, 0))

        # Link para cadastro
        ctk.CTkButton(
            self.main_frame, text=f"{ICONES['cadastrar']}  Criar nova conta",
            height=50, corner_radius=12, font=ctk.CTkFont(size=15),
            fg_color="transparent", border_width=2, border_color=COLORS["primary"],
            hover_color=COLORS["bg_card_alt"], text_color=COLORS["primary"],
            command=self.criar_tela_cadastro
        ).pack(fill="x")

    def criar_tela_cadastro(self):
        self.limpar_tela()

        # Logo
        ctk.CTkLabel(
            self.main_frame, text=ICONES["cadastrar"],
            font=ctk.CTkFont(size=56)
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            self.main_frame, text="Criar Conta",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS["text"]
        ).pack(pady=(0, 30))

        # Card de cadastro
        card = ctk.CTkFrame(self.main_frame, fg_color=COLORS["bg_card"], corner_radius=20)
        card.pack(fill="x", pady=10)

        # Usuário
        user_frame = ctk.CTkFrame(card, fg_color="transparent")
        user_frame.pack(fill="x", padx=30, pady=(25, 10))

        ctk.CTkLabel(
            user_frame, text=f"{ICONES['usuario']} Usuário",
            font=ctk.CTkFont(size=13), text_color=COLORS["text_muted"]
        ).pack(anchor="w")

        self.reg_user = ctk.CTkEntry(
            user_frame, placeholder_text="Escolha um nome de usuário",
            height=48, corner_radius=12, font=ctk.CTkFont(size=14),
            border_width=2, border_color=COLORS["border"]
        )
        self.reg_user.pack(fill="x", pady=(5, 0))

        # Senha
        pass_frame = ctk.CTkFrame(card, fg_color="transparent")
        pass_frame.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(
            pass_frame, text=f"{ICONES['cadeado']} Senha",
            font=ctk.CTkFont(size=13), text_color=COLORS["text_muted"]
        ).pack(anchor="w")

        self.reg_pass = ctk.CTkEntry(
            pass_frame, placeholder_text="Crie uma senha", show="●",
            height=48, corner_radius=12, font=ctk.CTkFont(size=14),
            border_width=2, border_color=COLORS["border"]
        )
        self.reg_pass.pack(fill="x", pady=(5, 0))

        # Confirmar senha
        confirm_frame = ctk.CTkFrame(card, fg_color="transparent")
        confirm_frame.pack(fill="x", padx=30, pady=(10, 0))

        ctk.CTkLabel(
            confirm_frame, text=f"{ICONES['cadeado']} Confirmar Senha",
            font=ctk.CTkFont(size=13), text_color=COLORS["text_muted"]
        ).pack(anchor="w")

        self.reg_pass_confirm = ctk.CTkEntry(
            confirm_frame, placeholder_text="Digite a senha novamente", show="●",
            height=48, corner_radius=12, font=ctk.CTkFont(size=14),
            border_width=2, border_color=COLORS["border"]
        )
        self.reg_pass_confirm.pack(fill="x", pady=(5, 0))
        self.reg_pass_confirm.bind("<Return>", lambda e: self.fazer_cadastro())

        # Botão cadastrar
        ctk.CTkButton(
            card, text=f"{ICONES['sucesso']}  Criar Conta", height=50,
            corner_radius=12, font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=COLORS["success"], hover_color=COLORS["success_hover"],
            command=self.fazer_cadastro
        ).pack(fill="x", padx=30, pady=25)

        # Voltar para login
        ctk.CTkButton(
            self.main_frame, text="← Voltar para o login",
            height=45, corner_radius=12, font=ctk.CTkFont(size=13),
            fg_color="transparent", hover_color=COLORS["bg_card_alt"],
            text_color=COLORS["text_muted"],
            command=self.criar_tela_login
        ).pack(fill="x", pady=(15, 0))

    def fazer_login(self):
        usuario = self.login_user.get().strip()
        senha = self.login_pass.get()

        if not usuario:
            messagebox.showwarning(f"{ICONES['aviso']} Aviso", "Digite seu usuário!")
            return

        if not senha:
            messagebox.showwarning(f"{ICONES['aviso']} Aviso", "Digite sua senha!")
            return

        if self.gerenciador.validar_login(usuario, senha):
            self.destroy()
            app = InterfaceGrafica(self.gerenciador)
            app.mainloop()
        else:
            messagebox.showerror(f"{ICONES['aviso']} Erro", "Usuário ou senha incorretos!")

    def fazer_cadastro(self):
        usuario = self.reg_user.get().strip()
        senha = self.reg_pass.get()
        confirmar = self.reg_pass_confirm.get()

        if not usuario:
            messagebox.showwarning(f"{ICONES['aviso']} Aviso", "Digite um nome de usuário!")
            return

        if len(usuario) < 3:
            messagebox.showwarning(f"{ICONES['aviso']} Aviso", "O usuário deve ter pelo menos 3 caracteres!")
            return

        if not senha:
            messagebox.showwarning(f"{ICONES['aviso']} Aviso", "Digite uma senha!")
            return

        if len(senha) < 4:
            messagebox.showwarning(f"{ICONES['aviso']} Aviso", "A senha deve ter pelo menos 4 caracteres!")
            return

        if senha != confirmar:
            messagebox.showwarning(f"{ICONES['aviso']} Aviso", "As senhas não coincidem!")
            return

        sucesso, mensagem = self.gerenciador.criar_usuario(usuario, senha)

        if sucesso:
            messagebox.showinfo(f"{ICONES['sucesso']} Sucesso", f"{mensagem}\n\nFaça login para continuar.")
            self.criar_tela_login()
        else:
            messagebox.showerror(f"{ICONES['aviso']} Erro", mensagem)


class GerenciadorFinanceiro:
    def __init__(self, gerenciador_usuarios=None):
        self.gerenciador_usuarios = gerenciador_usuarios

    def obter_transacoes(self):
        if self.gerenciador_usuarios:
            return self.gerenciador_usuarios.obter_transacoes()
        return []

    def adicionar_transacao(self, tipo, descricao, valor, dia, mes, ano):
        transacao = {
            "tipo": tipo,
            "descricao": descricao,
            "valor": valor,
            "dia": dia,
            "mes": mes,
            "ano": ano,
        }
        if self.gerenciador_usuarios:
            self.gerenciador_usuarios.adicionar_transacao(transacao)

    def excluir_transacao(self, indice):
        if self.gerenciador_usuarios:
            return self.gerenciador_usuarios.excluir_transacao(indice)
        return False

    def calcular_resumo(self):
        transacoes = self.obter_transacoes()
        if not transacoes:
            return None

        total_entradas = sum(t["valor"] for t in transacoes if t["tipo"] == "E")
        total_gastos = sum(t["valor"] for t in transacoes if t["tipo"] == "G")
        meses_unicos = len(set((t["mes"], t["ano"]) for t in transacoes))

        return {
            "total_entradas": total_entradas,
            "total_gastos": total_gastos,
            "saldo_total": total_entradas - total_gastos,
            "num_meses": meses_unicos,
            "media_entradas": total_entradas / meses_unicos if meses_unicos > 0 else 0,
            "media_gastos": total_gastos / meses_unicos if meses_unicos > 0 else 0,
            "media_saldo": (
                (total_entradas - total_gastos) / meses_unicos
                if meses_unicos > 0
                else 0
            ),
        }

    def obter_transacoes_mes(self, mes, ano):
        transacoes = self.obter_transacoes()
        transacoes_filtradas = [
            t for t in transacoes if t["mes"] == mes and t["ano"] == ano
        ]

        if not transacoes_filtradas:
            return None

        entradas = sum(t["valor"] for t in transacoes_filtradas if t["tipo"] == "E")
        gastos = sum(t["valor"] for t in transacoes_filtradas if t["tipo"] == "G")

        return {
            "transacoes": transacoes_filtradas,
            "entradas": entradas,
            "gastos": gastos,
            "saldo": entradas - gastos,
        }

    def obter_resumo_anual(self, ano):
        transacoes = self.obter_transacoes()
        transacoes_ano = [t for t in transacoes if t["ano"] == ano]

        if not transacoes_ano:
            return None

        resumo_meses = {}
        for mes in range(1, 13):
            transacoes_mes = [t for t in transacoes_ano if t["mes"] == mes]
            if transacoes_mes:
                entradas = sum(t["valor"] for t in transacoes_mes if t["tipo"] == "E")
                gastos = sum(t["valor"] for t in transacoes_mes if t["tipo"] == "G")
                resumo_meses[mes] = {
                    "entradas": entradas,
                    "gastos": gastos,
                    "saldo": entradas - gastos,
                }

        total_entradas = sum(t["valor"] for t in transacoes_ano if t["tipo"] == "E")
        total_gastos = sum(t["valor"] for t in transacoes_ano if t["tipo"] == "G")

        return {
            "resumo_meses": resumo_meses,
            "total_entradas": total_entradas,
            "total_gastos": total_gastos,
            "saldo_anual": total_entradas - total_gastos,
            "meses_ativos": len(resumo_meses),
        }


class BotaoModerno(ctk.CTkButton):
    def __init__(self, master, icon="", **kwargs):
        text = kwargs.get("text", "")
        if icon:
            kwargs["text"] = f"{icon}  {text}"
        super().__init__(master, **kwargs)


class CardModerno(ctk.CTkFrame):
    def __init__(self, master, title, value, icon, color, **kwargs):
        super().__init__(master, corner_radius=16, fg_color=COLORS["bg_card"], **kwargs)

        # Ícone grande
        icon_label = ctk.CTkLabel(
            self, text=icon, font=ctk.CTkFont(size=36), text_color=color
        )
        icon_label.pack(pady=(20, 5))

        # Título
        title_label = ctk.CTkLabel(
            self, text=title, font=ctk.CTkFont(size=13), text_color=COLORS["text_muted"]
        )
        title_label.pack(pady=5)

        # Valor
        self.value_label = ctk.CTkLabel(
            self, text=value, font=ctk.CTkFont(size=26, weight="bold"), text_color=color
        )
        self.value_label.pack(pady=(5, 20))

    def update_value(self, value, color=None):
        self.value_label.configure(text=value)
        if color:
            self.value_label.configure(text_color=color)


class EntradaModerna(ctk.CTkFrame):
    def __init__(self, master, label, placeholder="", icon="", **kwargs):
        super().__init__(master, fg_color="transparent")

        # Label
        label_frame = ctk.CTkFrame(self, fg_color="transparent")
        label_frame.pack(fill="x")

        if icon:
            ctk.CTkLabel(label_frame, text=icon, font=ctk.CTkFont(size=14)).pack(
                side="left", padx=(0, 5)
            )

        ctk.CTkLabel(
            label_frame,
            text=label,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLORS["text_muted"],
        ).pack(side="left")

        # Entry
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            height=48,
            corner_radius=12,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color=COLORS["border"],
            fg_color=COLORS["bg_card"],
        )
        self.entry.pack(fill="x", pady=(8, 0))

    def get(self):
        return self.entry.get()

    def delete(self, start, end):
        self.entry.delete(start, end)


class InterfaceGrafica(ctk.CTk):
    def __init__(self, gerenciador_usuarios=None):
        super().__init__()

        self.title(f"{ICONES['dinheiro']} Controle Financeiro")
        self.configure(fg_color=COLORS["bg_dark"])

        # Centralizar janela
        self.centralizar_janela(1400, 900)

        # Usar gerenciador de usuários se fornecido
        self.gerenciador_usuarios = gerenciador_usuarios
        self.gerenciador = GerenciadorFinanceiro(gerenciador_usuarios)

        # Sidebar
        self.criar_sidebar()

        # Container principal
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(
            side="right", fill="both", expand=True, padx=20, pady=20
        )

        # Frames das páginas
        self.frames = {}
        self.criar_paginas()

        # Mostrar página inicial
        self.mostrar_pagina("adicionar")

    def centralizar_janela(self, largura, altura):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def criar_sidebar(self):
        sidebar = ctk.CTkFrame(
            self, width=280, corner_radius=0, fg_color=COLORS["bg_card"]
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo/Título
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent", height=120)
        logo_frame.pack(fill="x", pady=(30, 20))
        logo_frame.pack_propagate(False)

        ctk.CTkLabel(logo_frame, text=ICONES["dinheiro"], font=ctk.CTkFont(size=48)).pack()
        ctk.CTkLabel(
            logo_frame,
            text="Controle Financeiro",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text"],
        ).pack(pady=(5, 0))

        # Separador
        ctk.CTkFrame(sidebar, height=2, fg_color=COLORS["border"]).pack(
            fill="x", padx=20, pady=10
        )

        # Menu items
        menu_items = [
            (f"{ICONES['adicionar']}  Nova Transação", "adicionar", COLORS["primary"]),
            (f"{ICONES['lista']}  Transações", "listar", COLORS["text"]),
            (f"{ICONES['grafico']}  Resumo Geral", "resumo", COLORS["text"]),
            (f"{ICONES['relatorio']}  Relatório Mensal", "relatorio", COLORS["text"]),
            (f"{ICONES['ano']}  Resumo Anual", "anual", COLORS["text"]),
        ]

        self.menu_buttons = {}

        for text, page, color in menu_items:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                height=50,
                corner_radius=12,
                font=ctk.CTkFont(size=14),
                anchor="w",
                fg_color="transparent",
                hover_color=COLORS["bg_card_alt"],
                text_color=color,
                command=lambda p=page: self.mostrar_pagina(p),
            )
            btn.pack(fill="x", padx=15, pady=5)
            self.menu_buttons[page] = btn

        # Info na parte inferior
        info_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        info_frame.pack(side="bottom", fill="x", pady=20, padx=15)

        # Botão de logout
        ctk.CTkButton(
            info_frame, text=f"{ICONES['sair']}  Sair",
            height=40, corner_radius=10,
            fg_color=COLORS["danger"], hover_color=COLORS["danger_hover"],
            font=ctk.CTkFont(size=13),
            command=self.fazer_logout
        ).pack(fill="x", pady=(0, 15))

        # Créditos
        ctk.CTkLabel(
            info_frame,
            text="Desenvolvido por:",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["text_muted"],
        ).pack()

        ctk.CTkLabel(
            info_frame,
            text="Welington Fernandes",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLORS["text"],
        ).pack()

        ctk.CTkLabel(
            info_frame,
            text="📞 (11) 95316-4286",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["text_muted"],
        ).pack(pady=(2, 0))

        # Separador
        ctk.CTkFrame(info_frame, height=1, fg_color=COLORS["border"]).pack(fill="x", pady=15)

        # Usuário logado
        if self.gerenciador_usuarios and self.gerenciador_usuarios.usuario_logado:
            ctk.CTkLabel(
                info_frame,
                text=f"{ICONES['usuario']} {self.gerenciador_usuarios.usuario_logado}",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=COLORS["text"],
            ).pack()

        self.status_label = ctk.CTkLabel(
            info_frame,
            text=f"{ICONES['arquivo']} {len(self.gerenciador.obter_transacoes())} transações",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_muted"],
        )
        self.status_label.pack()

    def mostrar_pagina(self, pagina):
        # Atualizar botões do menu
        for page, btn in self.menu_buttons.items():
            if page == pagina:
                btn.configure(fg_color=COLORS["primary"], text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=COLORS["text"])

        # Esconder todas as páginas
        for frame in self.frames.values():
            frame.pack_forget()

        # Mostrar página selecionada
        self.frames[pagina].pack(fill="both", expand=True)

        # Atualizar dados se necessário
        if pagina == "listar":
            self.atualizar_lista()
        elif pagina == "resumo":
            self.mostrar_resumo()

    def criar_paginas(self):
        self.criar_pagina_adicionar()
        self.criar_pagina_listar()
        self.criar_pagina_resumo()
        self.criar_pagina_relatorio()
        self.criar_pagina_anual()

    def atualizar_status(self):
        self.status_label.configure(
            text=f"{ICONES['arquivo']} {len(self.gerenciador.obter_transacoes())} transações"
        )

    def fazer_logout(self):
        resposta = messagebox.askyesno(
            f"{ICONES['sair']} Sair",
            "Deseja realmente sair?"
        )
        if resposta:
            self.destroy()
            login = TelaLogin()
            login.mainloop()

    def criar_pagina_adicionar(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["adicionar"] = frame

        # Título da página
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 30))

        ctk.CTkLabel(
            header,
            text=f"{ICONES['adicionar']} Nova Transação",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS["text"],
        ).pack(side="left")

        # Card central
        card = ctk.CTkFrame(frame, corner_radius=20, fg_color=COLORS["bg_card"])
        card.pack(fill="both", expand=True, padx=100)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7)

        # Tipo de transação
        ctk.CTkLabel(
            inner,
            text="Tipo de Transação",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", pady=(0, 10))

        tipo_frame = ctk.CTkFrame(inner, fg_color="transparent")
        tipo_frame.pack(fill="x", pady=(0, 25))

        self.tipo_var = ctk.StringVar(value="E")

        self.btn_entrada = ctk.CTkButton(
            tipo_frame,
            text=f"{ICONES['entrada']}  Entrada",
            width=180,
            height=55,
            font=ctk.CTkFont(size=15, weight="bold"),
            corner_radius=12,
            fg_color=COLORS["success"],
            hover_color=COLORS["success_hover"],
            command=lambda: self.selecionar_tipo("E"),
        )
        self.btn_entrada.pack(side="left", padx=(0, 15))

        self.btn_gasto = ctk.CTkButton(
            tipo_frame,
            text=f"{ICONES['despesa']}  Despesa",
            width=180,
            height=55,
            font=ctk.CTkFont(size=15, weight="bold"),
            corner_radius=12,
            fg_color=COLORS["bg_card_alt"],
            hover_color=COLORS["danger_hover"],
            command=lambda: self.selecionar_tipo("G"),
        )
        self.btn_gasto.pack(side="left")

        # Descrição
        self.desc_input = EntradaModerna(
            inner, "Descrição", "Ex: Salário, Aluguel, Mercado...", "📝"
        )
        self.desc_input.pack(fill="x", pady=(0, 20))

        # Valor
        self.valor_input = EntradaModerna(inner, "Valor (R$)", "0,00", "💵")
        self.valor_input.pack(fill="x", pady=(0, 20))

        # Data
        ctk.CTkLabel(
            inner,
            text=f"{ICONES['calendario']} Data",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", pady=(0, 8))

        data_frame = ctk.CTkFrame(inner, fg_color="transparent")
        data_frame.pack(fill="x", pady=(0, 30))

        hoje = datetime.now()

        self.dia_var = ctk.StringVar(value=str(hoje.day))
        self.mes_var = ctk.StringVar(value=str(hoje.month))
        self.ano_var = ctk.StringVar(value=str(hoje.year))

        # Dia
        dia_frame = ctk.CTkFrame(data_frame, fg_color="transparent")
        dia_frame.pack(side="left", padx=(0, 20))
        ctk.CTkLabel(
            dia_frame,
            text="Dia",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_muted"],
        ).pack()
        ctk.CTkComboBox(
            dia_frame,
            values=[str(i) for i in range(1, 32)],
            variable=self.dia_var,
            width=90,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color=COLORS["border"],
        ).pack(pady=(5, 0))

        # Mês
        mes_frame = ctk.CTkFrame(data_frame, fg_color="transparent")
        mes_frame.pack(side="left", padx=(0, 20))
        ctk.CTkLabel(
            mes_frame,
            text="Mês",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_muted"],
        ).pack()
        ctk.CTkComboBox(
            mes_frame,
            values=[str(i) for i in range(1, 13)],
            variable=self.mes_var,
            width=90,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color=COLORS["border"],
        ).pack(pady=(5, 0))

        # Ano
        ano_frame = ctk.CTkFrame(data_frame, fg_color="transparent")
        ano_frame.pack(side="left")
        ctk.CTkLabel(
            ano_frame,
            text="Ano",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_muted"],
        ).pack()
        ctk.CTkComboBox(
            ano_frame,
            values=[str(i) for i in range(2020, 2031)],
            variable=self.ano_var,
            width=110,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color=COLORS["border"],
        ).pack(pady=(5, 0))

        # Botão salvar
        ctk.CTkButton(
            inner,
            text=f"{ICONES['salvar']}  Salvar Transação",
            height=55,
            corner_radius=12,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            command=self.salvar_transacao,
        ).pack(fill="x", pady=(10, 0))

    def selecionar_tipo(self, tipo):
        self.tipo_var.set(tipo)
        if tipo == "E":
            self.btn_entrada.configure(fg_color=COLORS["success"])
            self.btn_gasto.configure(fg_color=COLORS["bg_card_alt"])
        else:
            self.btn_entrada.configure(fg_color=COLORS["bg_card_alt"])
            self.btn_gasto.configure(fg_color=COLORS["danger"])

    def salvar_transacao(self):
        descricao = self.desc_input.get().strip()
        valor_str = self.valor_input.get().strip().replace(",", ".")

        if not descricao:
            messagebox.showwarning(f"{ICONES['aviso']} Aviso", "Digite uma descrição!")
            return

        try:
            valor = float(valor_str)
            if valor <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                f"{ICONES['aviso']} Aviso", "Digite um valor válido!"
            )
            return

        tipo = self.tipo_var.get()
        dia = int(self.dia_var.get())
        mes = int(self.mes_var.get())
        ano = int(self.ano_var.get())

        self.gerenciador.adicionar_transacao(tipo, descricao, valor, dia, mes, ano)

        tipo_str = "Entrada" if tipo == "E" else "Despesa"
        messagebox.showinfo(
            f"{ICONES['sucesso']} Sucesso", f"{tipo_str} de R$ {valor:.2f} adicionada!"
        )

        self.desc_input.delete(0, "end")
        self.valor_input.delete(0, "end")
        self.atualizar_status()

    def criar_pagina_listar(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["listar"] = frame

        # Header
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            header,
            text=f"{ICONES['lista']} Transações",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS["text"],
        ).pack(side="left")

        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right")

        ctk.CTkButton(
            btn_frame,
            text=f"{ICONES['atualizar']} Atualizar",
            width=130,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=13),
            fg_color=COLORS["bg_card"],
            hover_color=COLORS["bg_card_alt"],
            command=self.atualizar_lista,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text=f"{ICONES['excluir']} Excluir",
            width=130,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=13),
            fg_color=COLORS["danger"],
            hover_color=COLORS["danger_hover"],
            command=self.excluir_transacao,
        ).pack(side="left", padx=5)

        # Lista
        self.lista_scroll = ctk.CTkScrollableFrame(
            frame, corner_radius=16, fg_color=COLORS["bg_card"]
        )
        self.lista_scroll.pack(fill="both", expand=True)

        # Cabeçalho da tabela
        header_frame = ctk.CTkFrame(
            self.lista_scroll, fg_color=COLORS["primary"], corner_radius=12
        )
        header_frame.pack(fill="x", padx=10, pady=(10, 5))

        headers = ["#", "Tipo", "Descrição", "Valor", "Data"]
        widths = [60, 120, 350, 150, 130]

        for h, w in zip(headers, widths):
            ctk.CTkLabel(
                header_frame,
                text=h,
                width=w,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="white",
            ).pack(side="left", padx=15, pady=12)

        self.items_frame = ctk.CTkFrame(self.lista_scroll, fg_color="transparent")
        self.items_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.selected_index = None

    def atualizar_lista(self):
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        self.selected_index = None
        transacoes = self.gerenciador.obter_transacoes()

        if not transacoes:
            empty_frame = ctk.CTkFrame(
                self.items_frame, fg_color="transparent", height=200
            )
            empty_frame.pack(fill="x", pady=50)
            ctk.CTkLabel(
                empty_frame,
                text=f"{ICONES['lista']}\n\nNenhuma transação registrada",
                font=ctk.CTkFont(size=16),
                text_color=COLORS["text_muted"],
            ).pack()
            return

        self.item_frames = []

        for i, t in enumerate(transacoes):
            row_color = COLORS["bg_card_alt"] if i % 2 == 0 else COLORS["bg_card"]

            row = ctk.CTkFrame(
                self.items_frame, fg_color=row_color, corner_radius=10, height=50
            )
            row.pack(fill="x", pady=3)
            row.pack_propagate(False)

            row.bind("<Button-1>", lambda e, idx=i: self.selecionar_item(idx))

            # Tornar todos os labels clicáveis
            def bind_click(widget, idx):
                widget.bind("<Button-1>", lambda e: self.selecionar_item(idx))

            # ID
            id_label = ctk.CTkLabel(
                row, text=str(i + 1), width=60, font=ctk.CTkFont(size=13)
            )
            id_label.pack(side="left", padx=15)
            bind_click(id_label, i)

            # Tipo
            is_entrada = t["tipo"] == "E"
            tipo_icon = ICONES["entrada"] if is_entrada else ICONES["despesa"]
            tipo_text = "Entrada" if is_entrada else "Despesa"
            tipo_cor = COLORS["success"] if is_entrada else COLORS["danger"]

            tipo_label = ctk.CTkLabel(
                row,
                text=f"{tipo_icon} {tipo_text}",
                width=120,
                font=ctk.CTkFont(size=13),
                text_color=tipo_cor,
            )
            tipo_label.pack(side="left", padx=15)
            bind_click(tipo_label, i)

            # Descrição
            desc_label = ctk.CTkLabel(
                row,
                text=t["descricao"],
                width=350,
                font=ctk.CTkFont(size=13),
                anchor="w",
            )
            desc_label.pack(side="left", padx=15)
            bind_click(desc_label, i)

            # Valor
            valor_label = ctk.CTkLabel(
                row,
                text=f"R$ {t['valor']:.2f}",
                width=150,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=tipo_cor,
            )
            valor_label.pack(side="left", padx=15)
            bind_click(valor_label, i)

            # Data
            data_text = f"{t.get('dia', 1):02d}/{t['mes']:02d}/{t['ano']}"
            data_label = ctk.CTkLabel(
                row, text=data_text, width=130, font=ctk.CTkFont(size=13)
            )
            data_label.pack(side="left", padx=15)
            bind_click(data_label, i)

            self.item_frames.append(row)

    def selecionar_item(self, index):
        if hasattr(self, "item_frames"):
            for i, frame in enumerate(self.item_frames):
                if i == index:
                    frame.configure(fg_color=COLORS["primary"])
                    self.selected_index = index
                else:
                    row_color = (
                        COLORS["bg_card_alt"] if i % 2 == 0 else COLORS["bg_card"]
                    )
                    frame.configure(fg_color=row_color)

    def excluir_transacao(self):
        if self.selected_index is None:
            messagebox.showwarning(
                f"{ICONES['aviso']} Atenção", "Selecione uma transação para excluir!"
            )
            return

        transacoes = self.gerenciador.obter_transacoes()
        t = transacoes[self.selected_index]

        tipo_str = "Entrada" if t["tipo"] == "E" else "Despesa"
        resposta = messagebox.askyesno(
            f"{ICONES['excluir']} Confirmar Exclusão",
            f"Deseja excluir esta transação?\n\n"
            f"Tipo: {tipo_str}\n"
            f"Descrição: {t['descricao']}\n"
            f"Valor: R$ {t['valor']:.2f}",
        )

        if resposta:
            if self.gerenciador.excluir_transacao(self.selected_index):
                messagebox.showinfo(f"{ICONES['sucesso']} Sucesso", "Transação excluída!")
                self.atualizar_lista()
                self.atualizar_status()

    def criar_pagina_resumo(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["resumo"] = frame

        # Header
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 30))

        ctk.CTkLabel(
            header,
            text=f"{ICONES['grafico']} Resumo Geral",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS["text"],
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text=f"{ICONES['atualizar']} Atualizar",
            width=130,
            height=40,
            corner_radius=10,
            fg_color=COLORS["bg_card"],
            command=self.mostrar_resumo,
        ).pack(side="right")

        # Cards principais
        cards_frame = ctk.CTkFrame(frame, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))

        self.card_entradas = CardModerno(
            cards_frame, "Total Entradas", "R$ 0,00", ICONES["entrada"], COLORS["success"]
        )
        self.card_entradas.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.card_gastos = CardModerno(
            cards_frame, "Total Despesas", "R$ 0,00", ICONES["despesa"], COLORS["danger"]
        )
        self.card_gastos.pack(side="left", fill="both", expand=True, padx=10)

        self.card_saldo = CardModerno(
            cards_frame, "Saldo Total", "R$ 0,00", ICONES["dinheiro"], COLORS["primary"]
        )
        self.card_saldo.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # Cards secundários
        cards_frame2 = ctk.CTkFrame(frame, fg_color="transparent")
        cards_frame2.pack(fill="x")

        self.card_media_ent = CardModerno(
            cards_frame2,
            "Média Entradas/Mês",
            "R$ 0,00",
            ICONES["estatisticas"],
            COLORS["success"],
        )
        self.card_media_ent.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.card_media_gas = CardModerno(
            cards_frame2,
            "Média Despesas/Mês",
            "R$ 0,00",
            ICONES["estatisticas"],
            COLORS["danger"],
        )
        self.card_media_gas.pack(side="left", fill="both", expand=True, padx=10)

        self.card_meses = CardModerno(
            cards_frame2, "Meses Registrados", "0", ICONES["calendario"], COLORS["aviso"]
        )
        self.card_meses.pack(side="left", fill="both", expand=True, padx=(10, 0))

    def mostrar_resumo(self):
        resumo = self.gerenciador.calcular_resumo()

        if not resumo:
            self.card_entradas.update_value("R$ 0,00")
            self.card_gastos.update_value("R$ 0,00")
            self.card_saldo.update_value("R$ 0,00")
            self.card_media_ent.update_value("R$ 0,00")
            self.card_media_gas.update_value("R$ 0,00")
            self.card_meses.update_value("0")
            return

        self.card_entradas.update_value(f"R$ {resumo['total_entradas']:,.2f}")
        self.card_gastos.update_value(f"R$ {resumo['total_gastos']:,.2f}")

        cor_saldo = (
            COLORS["success"] if resumo["saldo_total"] >= 0 else COLORS["danger"]
        )
        self.card_saldo.update_value(f"R$ {resumo['saldo_total']:,.2f}", cor_saldo)

        self.card_media_ent.update_value(f"R$ {resumo['media_entradas']:,.2f}")
        self.card_media_gas.update_value(f"R$ {resumo['media_gastos']:,.2f}")
        self.card_meses.update_value(str(resumo["num_meses"]))

    def criar_pagina_relatorio(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["relatorio"] = frame

        # Header
        ctk.CTkLabel(
            frame,
            text=f"{ICONES['relatorio']} Relatório Mensal",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS["text"],
        ).pack(anchor="w", pady=(0, 20))

        # Seleção
        selecao_frame = ctk.CTkFrame(
            frame, fg_color=COLORS["bg_card"], corner_radius=16, height=80
        )
        selecao_frame.pack(fill="x", pady=(0, 20))
        selecao_frame.pack_propagate(False)

        inner = ctk.CTkFrame(selecao_frame, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        hoje = datetime.now()

        ctk.CTkLabel(inner, text="Mês:", font=ctk.CTkFont(size=14)).pack(
            side="left", padx=10
        )
        self.rel_mes_var = ctk.StringVar(value=str(hoje.month))
        ctk.CTkComboBox(
            inner,
            values=[str(i) for i in range(1, 13)],
            variable=self.rel_mes_var,
            width=90,
            height=42,
            corner_radius=10,
        ).pack(side="left", padx=5)

        ctk.CTkLabel(inner, text="Ano:", font=ctk.CTkFont(size=14)).pack(
            side="left", padx=10
        )
        self.rel_ano_var = ctk.StringVar(value=str(hoje.year))
        ctk.CTkComboBox(
            inner,
            values=[str(i) for i in range(2020, 2031)],
            variable=self.rel_ano_var,
            width=110,
            height=42,
            corner_radius=10,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            inner,
            text=f"{ICONES['grafico']} Gerar",
            height=42,
            width=120,
            corner_radius=10,
            fg_color=COLORS["primary"],
            command=self.gerar_relatorio,
        ).pack(side="left", padx=20)

        # Textbox
        self.relatorio_text = ctk.CTkTextbox(
            frame,
            corner_radius=16,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color=COLORS["bg_card"],
        )
        self.relatorio_text.pack(fill="both", expand=True)

    def gerar_relatorio(self):
        self.relatorio_text.delete("1.0", "end")

        mes = int(self.rel_mes_var.get())
        ano = int(self.rel_ano_var.get())

        resultado = self.gerenciador.obter_transacoes_mes(mes, ano)

        meses_nomes = [
            "",
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro",
        ]

        if not resultado:
            self.relatorio_text.insert(
                "1.0",
                f"\n   {ICONES['aviso']} Nenhuma transação encontrada para {meses_nomes[mes]} de {ano}.",
            )
            return

        texto = f"""
   ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃              {ICONES['relatorio']} RELATÓRIO - {meses_nomes[mes]} {ano}
   ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

   TRANSAÇÕES:
   ─────────────────────────────────────────────────────────────────────

"""

        for t in resultado["transacoes"]:
            icon = ICONES["entrada"] if t["tipo"] == "E" else ICONES["despesa"]
            tipo_str = "ENTRADA" if t["tipo"] == "E" else "DESPESA"
            data_info = f"{t.get('dia', 1):02d}/{t['mes']:02d}/{t['ano']}"
            texto += f"   {icon} [{tipo_str:7}]  {t['descricao']:<28}  R$ {t['valor']:>10.2f}   ({data_info})\n"

        texto += f"""
   ─────────────────────────────────────────────────────────────────────

   {ICONES['entrada']} Total Entradas:      R$ {resultado['entradas']:>12.2f}
   {ICONES['despesa']} Total Despesas:      R$ {resultado['gastos']:>12.2f}
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   {ICONES['dinheiro']} Saldo do Mês:        R$ {resultado['saldo']:>12.2f}
"""

        self.relatorio_text.insert("1.0", texto)

    def criar_pagina_anual(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frames["anual"] = frame

        # Header
        ctk.CTkLabel(
            frame,
            text=f"{ICONES['ano']} Resumo Anual",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS["text"],
        ).pack(anchor="w", pady=(0, 20))

        # Seleção
        selecao_frame = ctk.CTkFrame(
            frame, fg_color=COLORS["bg_card"], corner_radius=16, height=80
        )
        selecao_frame.pack(fill="x", pady=(0, 20))
        selecao_frame.pack_propagate(False)

        inner = ctk.CTkFrame(selecao_frame, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(inner, text="Ano:", font=ctk.CTkFont(size=14)).pack(
            side="left", padx=10
        )
        self.ano_resumo_var = ctk.StringVar(value=str(datetime.now().year))
        ctk.CTkComboBox(
            inner,
            values=[str(i) for i in range(2020, 2031)],
            variable=self.ano_resumo_var,
            width=120,
            height=42,
            corner_radius=10,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            inner,
            text=f"{ICONES['grafico']} Gerar Resumo",
            height=42,
            width=150,
            corner_radius=10,
            fg_color=COLORS["aviso"],
            hover_color=COLORS["warning_hover"],
            command=self.gerar_resumo_anual,
        ).pack(side="left", padx=20)

        # Textbox
        self.resumo_anual_text = ctk.CTkTextbox(
            frame,
            corner_radius=16,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color=COLORS["bg_card"],
        )
        self.resumo_anual_text.pack(fill="both", expand=True)

    def gerar_resumo_anual(self):
        self.resumo_anual_text.delete("1.0", "end")

        ano = int(self.ano_resumo_var.get())
        resultado = self.gerenciador.obter_resumo_anual(ano)

        if not resultado:
            self.resumo_anual_text.insert(
                "1.0",
                f"\n   {ICONES['aviso']} Nenhuma transação encontrada para o ano {ano}.",
            )
            return

        meses_nomes = [
            "",
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro",
        ]

        texto = f"""
   ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃                    {ICONES['ano']} RESUMO ANUAL - {ano}                              ┃
   ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

   DESEMPENHO MENSAL:
   ─────────────────────────────────────────────────────────────────────────────

    Mês              │   Entradas    │   Despesas    │     Saldo     │
   ──────────────────┼───────────────┼───────────────┼───────────────┤
"""

        for mes in range(1, 13):
            if mes in resultado["resumo_meses"]:
                dados = resultado["resumo_meses"][mes]
                icon = "✓" if dados["saldo"] >= 0 else "✗"
                texto += f"    {meses_nomes[mes]:<13}  │  R$ {dados['entradas']:>8.2f}   │  R$ {dados['gastos']:>8.2f}   │  R$ {dados['saldo']:>8.2f} {icon}\n"
            else:
                texto += f"    {meses_nomes[mes]:<13}  │       -        │       -        │       -        │\n"

        media_ent = (
            resultado["total_entradas"] / resultado["meses_ativos"]
            if resultado["meses_ativos"] > 0
            else 0
        )
        media_gas = (
            resultado["total_gastos"] / resultado["meses_ativos"]
            if resultado["meses_ativos"] > 0
            else 0
        )
        media_sal = (
            resultado["saldo_anual"] / resultado["meses_ativos"]
            if resultado["meses_ativos"] > 0
            else 0
        )

        texto += f"""
   ─────────────────────────────────────────────────────────────────────────────

   TOTAIS ANUAIS:
   ─────────────────────────────────────────────────────────────────────────────

    {ICONES['entrada']} Total Entradas:              R$ {resultado['total_entradas']:>15.2f}
    {ICONES['despesa']} Total Despesas:              R$ {resultado['total_gastos']:>15.2f}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {ICONES['dinheiro']} Saldo Anual:                 R$ {resultado['saldo_anual']:>15.2f}

   ESTATÍSTICAS:
   ─────────────────────────────────────────────────────────────────────────────

    {ICONES['calendario']} Meses com transações:        {resultado['meses_ativos']} de 12
    {ICONES['estatisticas']} Média mensal de entradas:    R$ {media_ent:>15.2f}
    {ICONES['estatisticas']} Média mensal de despesas:    R$ {media_gas:>15.2f}
    {ICONES['estatisticas']} Média mensal de saldo:       R$ {media_sal:>15.2f}

"""

        if resultado["saldo_anual"] > 0:
            texto += f"    {ICONES['sucesso']} ANÁLISE: Ano POSITIVO! Economia de R$ {resultado['saldo_anual']:.2f}\n"
        elif resultado["saldo_anual"] < 0:
            texto += f"    {ICONES['aviso']} ANÁLISE: Ano NEGATIVO. Déficit de R$ {abs(resultado['saldo_anual']):.2f}\n"
        else:
            texto += (
                f"    {ICONES['dinheiro']} ANÁLISE: Ano EQUILIBRADO (receitas = despesas)\n"
            )

        self.resumo_anual_text.insert("1.0", texto)


def main():
    login = TelaLogin()
    login.mainloop()


if __name__ == "__main__":
    main()
