import sqlite3
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime

# Nome do aluno
nome_aluno = "Lucas Curtolo Belem - RA 2400206 e Marcelo Augusto - RA 2400507"
data_hoje = datetime.now().strftime("%d/%m/%Y")

# Estilos
titulo_font = Font(size=14, bold=True)
cabecalho_font = Font(bold=True)
centro = Alignment(horizontal="center")
fundo_azul = PatternFill("solid", fgColor="BDD7EE")
borda = Border(left=Side(style="thin"), right=Side(style="thin"),
               top=Side(style="thin"), bottom=Side(style="thin"))

def aplicar_estilo(ws, linha_inicio):
    for row in ws.iter_rows(min_row=linha_inicio, max_row=linha_inicio):
        for cell in row:
            cell.font = cabecalho_font
            cell.fill = fundo_azul
            cell.alignment = centro
            cell.border = borda

    for row in ws.iter_rows(min_row=linha_inicio+1):
        for cell in row:
            cell.border = borda

def ajustar_largura(ws):
    for i, col in enumerate(ws.columns, 1):
        max_length = 0
        col_letter = get_column_letter(i)
        for cell in col:
            try:
                if cell.value and isinstance(cell.value, str):
                    max_length = max(max_length, len(cell.value))
            except:
                pass
        ws.column_dimensions[col_letter].width = max_length + 2

# Criar planilha
wb = Workbook()
ws1 = wb.active
ws1.title = "Países"

# Conectar ao banco de países
conn_paises = sqlite3.connect("paises.db")
cursor_paises = conn_paises.cursor()
cursor_paises.execute("SELECT * FROM countries")
dados_paises = cursor_paises.fetchall()
colunas_paises = [desc[0] for desc in cursor_paises.description]
conn_paises.close()

# Título
ws1.merge_cells('A1:I1')
ws1['A1'] = f"Relatório de Países – Aluno: {nome_aluno} – Data: {data_hoje}"
ws1['A1'].font = titulo_font
ws1['A1'].alignment = centro

# Cabeçalhos e dados
linha_inicio_paises = 3
ws1.append([])
ws1.append(colunas_paises)

for linha in dados_paises:
    ws1.append(linha)

aplicar_estilo(ws1, linha_inicio_paises)
ajustar_largura(ws1)

# Nova aba – Livros
ws2 = wb.create_sheet("Livros")

conn_livros = sqlite3.connect("livraria.db")
cursor_livros = conn_livros.cursor()
cursor_livros.execute("SELECT * FROM livros")
dados_livros = cursor_livros.fetchall()
colunas_livros = [desc[0] for desc in cursor_livros.description]
conn_livros.close()

ws2.merge_cells('A1:E1')
ws2['A1'] = f"Relatório de Livros – Aluno: {nome_aluno} – Data: {data_hoje}"
ws2['A1'].font = titulo_font
ws2['A1'].alignment = centro

linha_inicio_livros = 3
ws2.append([])
ws2.append(colunas_livros)

for linha in dados_livros:
    ws2.append(linha)

aplicar_estilo(ws2, linha_inicio_livros)
ajustar_largura(ws2)

# Salvar arquivo na mesma pasta do script
wb.save("relatorio_final.xlsx")
print("Relatório estilizado salvo como: relatorio_final.xlsx")
