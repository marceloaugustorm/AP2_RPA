import sqlite3
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime

# Nome do aluno e data
nome_aluno = "Eduardo Omena - RA:2400882"
data_hoje = datetime.now().strftime("%d/%m/%Y")

# Estilo do título
titulo_font = Font(size=14, bold=True, color="FFFFFF")
titulo_fill = PatternFill("solid", fgColor="002060")
titulo_alinhamento = Alignment(horizontal="center", vertical="center")

# Estilo dos cabeçalhos
cabecalho_font = Font(bold=True, color="1F1F1F")
cabecalho_fill = PatternFill("solid", fgColor="D9D9D9")
cabecalho_alinhamento = Alignment(horizontal="center", vertical="center")

# Estilo de borda e alinhamento dos dados
borda = Border(left=Side(style="thin", color="A6A6A6"),
               right=Side(style="thin", color="A6A6A6"),
               top=Side(style="thin", color="A6A6A6"),
               bottom=Side(style="thin", color="A6A6A6"))

alinhamento_celula = Alignment(horizontal="center", vertical="center")

def aplicar_estilo(ws, linha_inicio):
    for row in ws.iter_rows(min_row=linha_inicio, max_row=linha_inicio):
        for cell in row:
            cell.font = cabecalho_font
            cell.fill = cabecalho_fill
            cell.alignment = cabecalho_alinhamento
            cell.border = borda

    for row in ws.iter_rows(min_row=linha_inicio + 1):
        for cell in row:
            cell.border = borda
            cell.alignment = alinhamento_celula

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
ws1['A1'].fill = titulo_fill
ws1['A1'].alignment = titulo_alinhamento

# Cabeçalhos e dados
linha_inicio_paises = 3
ws1.append([])  # linha em branco
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

# Título
ws2.merge_cells('A1:E1')
ws2['A1'] = f"Relatório de Livros – Aluno: {nome_aluno} – Data: {data_hoje}"
ws2['A1'].font = titulo_font
ws2['A1'].fill = titulo_fill
ws2['A1'].alignment = titulo_alinhamento

linha_inicio_livros = 3
ws2.append([])
ws2.append(colunas_livros)

for linha in dados_livros:
    ws2.append(linha)

aplicar_estilo(ws2, linha_inicio_livros)
ajustar_largura(ws2)

# Salvar planilha
wb.save("relatorio_final.xlsx")
print("Relatório com nova estilização salvo como: relatorio_final.xlsx")
