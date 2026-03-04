import numpy as np
import plotly.graph_objects as go
from PIL import Image
import io

# Configurações
np.random.seed(42)
SLA = 500
meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
cores = {'bom': '#27ae60', 'medio': '#f39c12', 'ruim': '#e74c3c', 'fundo': 'rgba(250,251,252,0.95)'}

# Perfil de carga realista: picos em períodos de provas
perfil_carga = {
    'Jan': (0.6, 'Recesso'), 'Fev': (1.0, 'Matrículas'), 'Mar': (0.8, 'Início aulas'),
    'Abr': (1.8, 'Provas 1º Bim'), 'Mai': (2.2, 'Notas 1º Bim'), 'Jun': (2.5, 'Provas 2º Bim'),
    'Jul': (0.5, 'Férias'), 'Ago': (0.9, 'Retorno aulas'), 'Set': (1.1, 'Período letivo'),
    'Out': (1.9, 'Provas 3º Bim'), 'Nov': (2.3, 'Notas 3º Bim'), 'Dez': (2.6, 'Notas Finais')
}

# Simulação de dados
dados_meses = []
for mes in meses:
    carga, desc = perfil_carga[mes]
    num_req = int(500 + carga * 1000)
    tempos = np.clip(np.random.normal(250 + carga * 180, 40 + carga * 50, num_req), 100, 1500)
    dados_meses.append({
        'mes': mes, 'tempos': tempos, 'media': tempos.mean(),
        'pct_sla': (tempos > SLA).mean() * 100, 'desc': desc, 'req': num_req
    })

print("\nGerando frames para MP4...")
frames_img = []

for i, d in enumerate(dados_meses):
    # Cores dinâmicas
    cor = cores['bom'] if d['media'] < SLA else cores['medio'] if d['media'] < SLA * 1.2 else cores['ruim']
    cor_borda = cores['bom'] if d['pct_sla'] < 10 else cores['medio'] if d['pct_sla'] < 30 else cores['ruim']
    
    # Criar figura
    fig = go.Figure(go.Histogram(x=d['tempos'], nbinsx=35, marker_color=cor,
                                 marker_line_color='white', marker_line_width=1.5, opacity=0.9))
    
    fig.add_vline(x=SLA, line_dash="dash", line_color=cores['ruim'], line_width=3,
                  annotation_text="<b>SLA: 500ms</b>", annotation_position="top right")
    
    fig.update_layout(
        title={'text': f"<b>Evolução do Tempo de Resposta da API - {d['mes']} ({d['desc']})</b>", 
               'x': 0.5},
        xaxis_title="<b>Tempo de Resposta (ms)</b>", yaxis_title="<b>Frequência</b>",
        bargap=0.03, plot_bgcolor=cores['fundo'], paper_bgcolor='white',
        font=dict(family="Segoe UI", size=12, color="#2c3e50"),
        title_font=dict(size=22), height=600, width=1200,
        xaxis=dict(showgrid=True, gridcolor="rgba(200,205,210,0.25)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(200,205,210,0.25)"),
        shapes=[
            dict(type='line', x0=d['media'], x1=d['media'], y0=0, y1=1, xref='x', yref='paper',
                 line=dict(color=cor, width=3, dash='dot')),
            dict(type='rect', x0=SLA, x1=2000, y0=0, y1=1, xref='x', yref='paper',
                 fillcolor='rgba(231,76,60,0.08)', line_width=0, layer='below')
        ],
        annotations=[
            dict(x=0.02, y=0.98, xref='paper', yref='paper', text=f"<b>{d['mes']}</b>",
                 showarrow=False, bgcolor=cor, bordercolor='white', borderwidth=3, 
                 borderpad=12, font=dict(size=18, color='white')),
            dict(x=0.02, y=0.82, xref='paper', yref='paper', text=f"<i>{d['desc']}</i>",
                 showarrow=False, bgcolor='rgba(255,255,255,0.85)', bordercolor=cor,
                 borderwidth=2, borderpad=8, font=dict(size=12, color='#34495e')),
            dict(x=d['media'], y=1.08, xref='x', yref='paper', text=f"<b>Média: {d['media']:.0f}ms</b>",
                 showarrow=True, arrowhead=2, arrowcolor=cor, ax=0, ay=-35, bgcolor='white',
                 bordercolor=cor, borderwidth=2.5, borderpad=8, font=dict(size=14, color='#2c3e50')),
            dict(x=0.98, y=0.96, xref='paper', yref='paper',
                 text=f"<b>{d['pct_sla']:.1f}%</b> acima SLA<br>{d['req']:,} requisições",
                 showarrow=False, bgcolor='white', bordercolor=cor_borda, borderwidth=2.5,
                 borderpad=10, font=dict(size=12, color='#2c3e50')),
            dict(x=0.5, y=-0.08, xref='paper', yref='paper', text=f"<b>Mês: {d['mes']}</b>",
                 showarrow=False, bgcolor=cor, bordercolor='white', borderwidth=3,
                 borderpad=10, font=dict(size=16, color='white'))
        ]
    )
    
    # Converter para imagem
    img = Image.open(io.BytesIO(fig.to_image(format="png", width=1200, height=600)))
    frames_img.append(np.array(img))
    print(f"  Frame {i+1}/12 ({d['mes']})")

# Gerar MP4
try:
    import imageio
    imageio.mimsave("animacao_api.mp4", frames_img, fps=1, codec='libx264', quality=8)
    print("\n✓ Arquivo 'animacao_api.mp4' criado com sucesso!")
except ImportError:
    print("\n⚠ Instalando imageio...")
    import subprocess
    subprocess.run(["pip", "install", "imageio[ffmpeg]"], check=True)
    import imageio
    imageio.mimsave("animacao_api.mp4", frames_img, fps=1, codec='libx264', quality=8)
    print("✓ Arquivo 'animacao_api.mp4' criado!")

# Estatísticas
pior = max(dados_meses, key=lambda x: x['media'])
melhor = min(dados_meses, key=lambda x: x['media'])
print(f"\nPior: {pior['mes']} ({pior['desc']}) - {pior['media']:.0f}ms")
print(f"Melhor: {melhor['mes']} ({melhor['desc']}) - {melhor['media']:.0f}ms\n")