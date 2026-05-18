"""
Dashboard Prescriptivo · Papelería Mundo Abstracto
====================================================
Requisitos:
    pip install dash plotly

Ejecución local:
    python dashboard_mundo_abstracto.py
    Abrir en el navegador: http://127.0.0.1:8050

Despliegue en la nube (URL pública gratuita):
    Render.com  → conecta el repo y apunta a este archivo.
    Railway.app → igual, sin costo para proyectos pequeños.
    La única línea que debes cambiar para producción es:
        server = app.server   (ya incluida abajo)
"""

import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px

# ──────────────────────────────────────────────
# PALETA Y ESTILOS GLOBALES
# ──────────────────────────────────────────────
AZUL      = "#0f4c81"
AZUL_CL   = "#185FA5"
NARANJA   = "#f28c28"
VERDE     = "#2a9d5c"
ROJO      = "#d64a2e"
MORADO    = "#6b4fe0"
MUTED     = "#726f68"
BG        = "#f4f3f0"
SURFACE   = "#ffffff"
BORDER    = "#e2e0da"
SURFACE2  = "#f9f8f6"

FONT = "'DM Sans', 'Segoe UI', Arial, sans-serif"

MESES = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]

CARD = {
    "background": SURFACE,
    "border": f"1px solid {BORDER}",
    "borderRadius": "16px",
    "padding": "20px",
    "boxShadow": "0 2px 12px rgba(0,0,0,.07)",
    "marginBottom": "16px",
}

METRIC_CARD = {
    "background": SURFACE,
    "border": f"1px solid {BORDER}",
    "borderRadius": "12px",
    "padding": "16px",
    "boxShadow": "0 2px 8px rgba(0,0,0,.05)",
    "flex": "1",
    "minWidth": "140px",
}

TAB_STYLE = {
    "fontFamily": FONT,
    "fontSize": "0.88rem",
    "fontWeight": "500",
    "color": MUTED,
    "padding": "14px 20px",
    "border": "none",
    "borderBottom": "2px solid transparent",
    "background": SURFACE,
    "cursor": "pointer",
}

TAB_SELECTED = {
    **TAB_STYLE,
    "color": AZUL,
    "borderBottom": f"2px solid {AZUL}",
}

def metric(label, value, color=AZUL, delta=None, delta_color=MUTED):
    """Tarjeta de métrica reutilizable."""
    children = [
        html.Div(label, style={"fontSize": "0.78rem", "color": MUTED, "marginBottom": "6px"}),
        html.Div(value, style={"fontSize": "1.7rem", "fontWeight": "600", "color": color, "lineHeight": "1"}),
    ]
    if delta:
        children.append(html.Div(delta, style={"fontSize": "0.78rem", "color": delta_color, "marginTop": "5px"}))
    return html.Div(children, style=METRIC_CARD)

def alert_box(title, body, kind="info"):
    colors = {
        "info":  {"bg": "#edf3fc", "border": AZUL,    "text": "#0a3360"},
        "warn":  {"bg": "#fff8e1", "border": NARANJA,  "text": "#7a4900"},
        "ok":    {"bg": "#e8f5ee", "border": VERDE,    "text": "#1e5c35"},
        "crit":  {"bg": "#fdecea", "border": ROJO,     "text": "#8b1e10"},
    }
    c = colors[kind]
    return html.Div([
        html.Div(title, style={"fontWeight": "600", "fontSize": "0.88rem", "marginBottom": "4px"}),
        html.Div(body,  style={"fontSize": "0.82rem", "lineHeight": "1.55"}),
    ], style={
        "background": c["bg"], "borderLeft": f"4px solid {c['border']}",
        "color": c["text"], "borderRadius": "10px", "padding": "12px 14px", "marginBottom": "10px",
    })

def vs_bar(label, pct, color):
    return html.Div([
        html.Span(label, style={"minWidth": "100px", "fontSize": "0.8rem", "color": MUTED}),
        html.Div(html.Div(style={
            "width": f"{pct}%", "height": "100%",
            "background": color, "borderRadius": "5px",
        }), style={"flex": "1", "height": "10px", "background": "#eee", "borderRadius": "5px", "overflow": "hidden"}),
        html.Span(f"{pct}%", style={"minWidth": "48px", "textAlign": "right", "fontWeight": "600", "fontSize": "0.83rem", "color": color}),
    ], style={"display": "flex", "alignItems": "center", "gap": "10px", "margin": "8px 0"})

def section_title(title, sub=None):
    el = [html.Div(title, style={"fontSize": "0.92rem", "fontWeight": "600"})]
    if sub:
        el.append(html.Div(sub, style={"fontSize": "0.78rem", "color": MUTED, "marginTop": "2px"}))
    return html.Div(el, style={"marginBottom": "14px"})

# ──────────────────────────────────────────────
# GRÁFICAS ESTÁTICAS (no dependen de callbacks)
# ──────────────────────────────────────────────

def fig_gap():
    real      = [3.8,3.6,4.1,4.0,3.9,4.3,5.1,4.8,4.2,4.0,3.7,5.4]
    potencial = [5.8,5.5,6.4,6.2,6.0,6.6,7.8,7.2,6.4,6.1,5.8,8.0]
    fig = go.Figure([
        go.Bar(name="Real", x=MESES, y=real, marker_color=AZUL_CL, marker_line_width=0),
        go.Bar(name="Potencial teórico", x=MESES, y=potencial,
               marker_color="rgba(42,157,92,.18)", marker_line_color=VERDE, marker_line_width=1.5),
    ])
    fig.update_layout(
        barmode="group", plot_bgcolor=SURFACE, paper_bgcolor=SURFACE,
        margin=dict(t=10, b=30, l=40, r=10), height=230,
        font_family=FONT, font_color=MUTED,
        yaxis=dict(tickprefix="$", ticksuffix="M", gridcolor="#eee"),
        xaxis=dict(showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font_size=11),
    )
    return fig

def fig_horas():
    horas   = ["6am","7am","8am","9am","10am","11am","12pm","1pm","2pm","3pm","4pm","5pm","6pm","7pm"]
    real    = [5,42,78,65,30,25,58,72,55,28,62,70,48,20]
    potenc  = [5,60,90,80,40,35,70,85,65,35,75,82,60,28]
    fig = go.Figure([
        go.Scatter(x=horas, y=real, name="Tráfico real", fill="tozeroy",
                   line=dict(color=AZUL_CL, width=2), fillcolor="rgba(24,95,165,.1)"),
        go.Scatter(x=horas, y=potenc, name="Potencial", line=dict(color=VERDE, dash="dot", width=1.5)),
    ])
    fig.update_layout(
        plot_bgcolor=SURFACE, paper_bgcolor=SURFACE, height=200,
        margin=dict(t=10, b=30, l=30, r=10), font_family=FONT, font_color=MUTED,
        xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#eee"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font_size=11),
    )
    return fig

def fig_clv_donut():
    fig = go.Figure(go.Pie(
        labels=["Champions (18%)", "Leales (27%)", "Potenciales (33%)", "En riesgo (22%)"],
        values=[18, 27, 33, 22],
        hole=0.65,
        marker=dict(colors=[VERDE, AZUL_CL, NARANJA, ROJO], line=dict(width=0)),
    ))
    fig.update_layout(
        plot_bgcolor=SURFACE, paper_bgcolor=SURFACE, height=240,
        margin=dict(t=10, b=40, l=10, r=10), font_family=FONT,
        legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5, font_size=11),
        showlegend=True,
    )
    return fig

def fig_retencion():
    real   = [1620,1590,1640,1680,1700,1720,1840,1810,1760,1740,1720,1780]
    fidel  = [1620,1590,1640,1690,1730,1790,1900,1920,1910,1950,1980,2080]
    fig = go.Figure([
        go.Scatter(x=MESES, y=real, name="Clientes activos (real)", fill="tozeroy",
                   line=dict(color=AZUL_CL, width=2), fillcolor="rgba(24,95,165,.08)"),
        go.Scatter(x=MESES, y=fidel, name="Con fidelización",
                   line=dict(color=VERDE, dash="dot", width=1.8)),
    ])
    fig.update_layout(
        plot_bgcolor=SURFACE, paper_bgcolor=SURFACE, height=200,
        margin=dict(t=10, b=30, l=40, r=10), font_family=FONT, font_color=MUTED,
        xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#eee"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font_size=11),
    )
    return fig

def fig_costos():
    fig = go.Figure(go.Pie(
        labels=["COGS 60%","Operación 12%","Servicios públicos 5%","Logística 8%","Imprevistos 5%","Margen 10%"],
        values=[60, 12, 5, 8, 5, 10],
        hole=0.6,
        marker=dict(colors=[AZUL_CL, NARANJA, ROJO, MORADO, "#0e8a8a", VERDE], line=dict(width=0)),
    ))
    fig.update_layout(
        plot_bgcolor=SURFACE, paper_bgcolor=SURFACE, height=240,
        margin=dict(t=10, b=50, l=10, r=10), font_family=FONT,
        legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5, font_size=10),
    )
    return fig

def fig_margen():
    cats = ["Escolar","Miscelánea","Oficina","Papelería","Servicios"]
    real = [38, 35, 32, 40, 52]
    meta = [44, 42, 40, 45, 57]
    fig = go.Figure([
        go.Bar(name="Margen real",    x=cats, y=real, marker_color=AZUL_CL, marker_line_width=0),
        go.Bar(name="Meta prescrita", x=cats, y=meta,
               marker_color="rgba(42,157,92,.18)", marker_line_color=VERDE, marker_line_width=1.5),
    ])
    fig.update_layout(
        barmode="group", plot_bgcolor=SURFACE, paper_bgcolor=SURFACE, height=240,
        margin=dict(t=10, b=30, l=40, r=10), font_family=FONT, font_color=MUTED,
        yaxis=dict(ticksuffix="%", gridcolor="#eee", range=[0, 65]),
        xaxis=dict(showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font_size=11),
    )
    return fig

def fig_escala():
    levels = ["1.0×","1.5×","2.0×","2.5×","3.0×","3.5×","4.0×"]
    ideal  = [4.2, 6.1, 7.8, 9.0, 9.8, 10.1, 10.3]
    real   = [4.2, 5.8, 6.9, 7.2, 6.8,  6.0,  5.2]
    fig = go.Figure([
        go.Scatter(x=levels, y=ideal, name="Sin cuellos de botella", fill="tozeroy",
                   line=dict(color=VERDE, width=2), fillcolor="rgba(42,157,92,.08)"),
        go.Scatter(x=levels, y=real, name="Con saturación",
                   line=dict(color=ROJO, dash="dot", width=1.8)),
    ])
    fig.update_layout(
        plot_bgcolor=SURFACE, paper_bgcolor=SURFACE, height=230,
        margin=dict(t=10, b=30, l=40, r=10), font_family=FONT, font_color=MUTED,
        xaxis=dict(showgrid=False), yaxis=dict(tickprefix="$", ticksuffix="M", gridcolor="#eee"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font_size=11),
    )
    return fig

def fig_validacion():
    predicha = [1.65,1.55,1.72,1.68,1.64,1.80,2.14,1.99,1.75,1.68,1.56,2.26]
    real_val = [1.68,1.52,1.78,1.70,1.60,1.84,2.08,1.94,1.79,1.64,1.59,2.18]
    fig = go.Figure([
        go.Scatter(x=MESES, y=predicha, name="Ganancia predicha", fill="tozeroy",
                   line=dict(color=NARANJA, width=2), fillcolor="rgba(242,140,40,.08)"),
        go.Scatter(x=MESES, y=real_val, name="Ganancia real",
                   line=dict(color=AZUL_CL, width=2)),
    ])
    fig.update_layout(
        plot_bgcolor=SURFACE, paper_bgcolor=SURFACE, height=230,
        margin=dict(t=10, b=30, l=40, r=10), font_family=FONT, font_color=MUTED,
        xaxis=dict(showgrid=False), yaxis=dict(tickprefix="$", ticksuffix="M", gridcolor="#eee"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font_size=11),
    )
    return fig

# ──────────────────────────────────────────────
# CONTENIDO DE CADA PESTAÑA
# ──────────────────────────────────────────────

def tab_brechas():
    return html.Div([
        html.Div("Contraste entre el desempeño real registrado y el máximo teórico que el modelo predictivo estima como alcanzable.",
                 style={"color": MUTED, "fontSize": "0.88rem", "marginBottom": "18px"}),

        # Métricas superiores
        html.Div([
            metric("Ingreso mensual actual",   "$4.2M",  AZUL,    "↑ COP promedio / mes"),
            metric("Potencial teórico (modelo)","$6.8M",  VERDE,   "Según R²=0.9932"),
            metric("Brecha de captura",        "38%",    NARANJA, "↓ COP 2.6M sin aprovechar"),
            metric("Ticket promedio real",      "$8.5K",  MUTED,   "vs $11.2K teórico"),
        ], style={"display": "flex", "gap": "12px", "marginBottom": "16px", "flexWrap": "wrap"}),

        # Gráficas
        html.Div([
            html.Div([
                html.Div(style=CARD, children=[
                    section_title("Ingresos Reales vs Potencial por Mes",
                                  "Brecha mensual 2024 — base modelo RLM entrenado con 38.895 obs."),
                    dcc.Graph(figure=fig_gap(), config={"displayModeBar": False}),
                ]),
            ], style={"flex": "1", "minWidth": "300px"}),
            html.Div([
                html.Div(style=CARD, children=[
                    section_title("Utilización por Categoría",
                                  "% de captura del potencial estimado por el modelo predictivo"),
                    vs_bar("Escolar",    82, AZUL_CL),
                    vs_bar("Miscelánea", 61, NARANJA),
                    vs_bar("Oficina",    54, AZUL_CL),
                    vs_bar("Papelería",  74, VERDE),
                    vs_bar("Servicios",  43, ROJO),
                    html.Hr(style={"borderColor": BORDER, "margin": "14px 0"}),
                    html.Div("Prescripción: Servicios y Oficina son las categorías con mayor brecha. "
                             "Activar combos impresión + oficina puede cerrar hasta +15 puntos de captura.",
                             style={"fontSize": "0.82rem", "color": MUTED}),
                ]),
            ], style={"flex": "1", "minWidth": "300px"}),
        ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),

        # Horario + Prescripciones
        html.Div([
            html.Div([
                html.Div(style=CARD, children=[
                    section_title("Eficiencia por Franja Horaria",
                                  "Captación real vs ventanas de mayor tráfico estudiantil"),
                    dcc.Graph(figure=fig_horas(), config={"displayModeBar": False}),
                ]),
            ], style={"flex": "1", "minWidth": "300px"}),
            html.Div([
                html.Div(style=CARD, children=[
                    section_title("Prescripciones Prioritarias", "Acciones para cerrar la brecha en 90 días"),
                    alert_box("🔴 Crítico — Servicios (brecha 57%)",
                              "Instalar letrero externo con precios de fotocopias. Activar combo "
                              "'Copia + grapa' en horas pico. Potencial incremental: +COP 380K/mes.", "crit"),
                    alert_box("🟡 Alto — Oficina & Miscelánea",
                              "Organizar módulo de oficina con resaltadores, bolígrafos y folders. "
                              "Cross-selling con artículos escolares. Potencial: +COP 210K/mes.", "warn"),
                    alert_box("🟢 Mantener — Escolar (82% captura)",
                              "Categoría líder. Mantener stock suficiente en temporadas de inicio "
                              "de clases para no perder la ventaja ya ganada.", "ok"),
                ]),
            ], style={"flex": "1", "minWidth": "300px"}),
        ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),
    ])


def tab_lealtad():
    tabla_rows = [
        ("Champions",   "chip-green",  "18%", "$124K", "Trato preferencial, aviso anticipado de nuevos productos"),
        ("Leales",      "chip-blue",   "27%", "$84K",  "Programa de puntos, descuento acumulado en Escolar"),
        ("Potenciales", "chip-orange", "33%", "$52K",  "Oferta de segunda visita, muestra gratis con compra >$5K"),
        ("En riesgo",   "chip-red",    "22%", "$18K",  "Voucher $1.000 reactivación + contacto personalizado"),
    ]
    chip_styles = {
        "chip-green":  {"background": "#e8f5ee", "color": "#1e7a45"},
        "chip-blue":   {"background": "#edf3fc", "color": AZUL},
        "chip-orange": {"background": "#fff3e0", "color": "#b85e00"},
        "chip-red":    {"background": "#fdecea", "color": "#b33220"},
    }
    def chip(label, cls):
        s = chip_styles[cls]
        return html.Span(label, style={**s, "padding": "3px 10px", "borderRadius": "999px",
                                       "fontSize": "0.75rem", "fontWeight": "600"})

    tl_items = [
        ("dot-blue",   "Semana 1–2 · Identificar Champions y Leales",
         "Crear lista de clientes frecuentes. Tarjeta de fidelización manual (sello por compra >$3K). Costo: $0."),
        ("dot-orange", "Semana 3–4 · Activar segmento En Riesgo",
         "Contacto directo con voucher $1.000. Meta: recuperar 40% del segmento."),
        ("dot-green",  "Semana 5–6 · Campaña temporada escolar",
         "Paquete cuadernos + lápices + marcadores con 8% descuento para clientes leales. Meta: +$320K en 2 semanas."),
        ("dot-gray",   "Semana 7–8 · Medir y ajustar",
         "Comparar CLV antes/después. Modelo predice +22% en retención si se ejecutan los pasos 1–3."),
    ]
    dot_colors = {"dot-blue": AZUL, "dot-orange": NARANJA, "dot-green": VERDE, "dot-gray": MUTED}

    timeline = html.Div([
        html.Div([
            html.Div(style={"width":"12px","height":"12px","borderRadius":"50%",
                             "background": dot_colors[dot],"marginTop":"4px","flexShrink":"0"}),
            html.Div([
                html.Div(title, style={"fontSize": "0.88rem", "fontWeight": "600", "marginBottom": "2px"}),
                html.Div(body,  style={"fontSize": "0.8rem",  "color": MUTED, "lineHeight": "1.5"}),
            ]),
        ], style={"display": "flex", "gap": "10px", "marginBottom": "14px"})
        for dot, title, body in tl_items
    ])

    return html.Div([
        html.Div("Segmentación predictiva de clientes y prescripción de acciones preventivas para maximizar retención.",
                 style={"color": MUTED, "fontSize": "0.88rem", "marginBottom": "18px"}),

        html.Div([
            metric("Clientes activos est.",  "1.840",  AZUL,    "Últimos 12 meses"),
            metric("Clientes en riesgo",     "412",    ROJO,    "↓ 22% del total"),
            metric("CLV promedio actual",    "$68K",   NARANJA, "COP / año / cliente"),
            metric("CLV potencial",          "$94K",   VERDE,   "↑ +38% con fidelización"),
        ], style={"display": "flex", "gap": "12px", "marginBottom": "16px", "flexWrap": "wrap"}),

        html.Div([
            html.Div([
                html.Div(style=CARD, children=[
                    section_title("Segmentación RFM de Clientes", "Recencia · Frecuencia · Valor monetario"),
                    dcc.Graph(figure=fig_clv_donut(), config={"displayModeBar": False}),
                ]),
            ], style={"flex": "1", "minWidth": "280px"}),
            html.Div([
                html.Div(style=CARD, children=[
                    section_title("Acciones Prescritas por Segmento"),
                    html.Table([
                        html.Thead(html.Tr([
                            html.Th("Segmento", style={"padding":"8px 10px","background":SURFACE2,"borderBottom":f"1px solid {BORDER}","fontSize":"0.8rem","color":MUTED}),
                            html.Th("% clientes", style={"padding":"8px 10px","background":SURFACE2,"borderBottom":f"1px solid {BORDER}","fontSize":"0.8rem","color":MUTED}),
                            html.Th("CLV est.", style={"padding":"8px 10px","background":SURFACE2,"borderBottom":f"1px solid {BORDER}","fontSize":"0.8rem","color":MUTED}),
                            html.Th("Acción prioritaria", style={"padding":"8px 10px","background":SURFACE2,"borderBottom":f"1px solid {BORDER}","fontSize":"0.8rem","color":MUTED}),
                        ])),
                        html.Tbody([
                            html.Tr([
                                html.Td(chip(seg, cls), style={"padding":"8px 10px","borderBottom":f"1px solid {BORDER}"}),
                                html.Td(pct,  style={"padding":"8px 10px","borderBottom":f"1px solid {BORDER}","fontSize":"0.84rem"}),
                                html.Td(clv,  style={"padding":"8px 10px","borderBottom":f"1px solid {BORDER}","fontSize":"0.84rem","fontWeight":"600","color":VERDE}),
                                html.Td(acc,  style={"padding":"8px 10px","borderBottom":f"1px solid {BORDER}","fontSize":"0.82rem","color":MUTED}),
                            ]) for seg, cls, pct, clv, acc in tabla_rows
                        ]),
                    ], style={"width": "100%", "borderCollapse": "collapse"}),
                ]),
            ], style={"flex": "1", "minWidth": "280px"}),
        ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),

        html.Div([
            html.Div([
                html.Div(style=CARD, children=[
                    section_title("Tendencia de Retención", "Con y sin programa de fidelización"),
                    dcc.Graph(figure=fig_retencion(), config={"displayModeBar": False}),
                ]),
            ], style={"flex": "1", "minWidth": "280px"}),
            html.Div([
                html.Div(style=CARD, children=[
                    section_title("Plan de Fidelización Prescrito", "Secuencia de acciones en 60 días"),
                    timeline,
                ]),
            ], style={"flex": "1", "minWidth": "280px"}),
        ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),
    ])


def tab_cadena():
    return html.Div([
        html.Div("Diagnóstico de costos ocultos en la operación diaria e identificación de palancas de rentabilidad.",
                 style={"color": MUTED, "fontSize": "0.88rem", "marginBottom": "18px"}),

        html.Div([
            metric("Costo/ingreso actual",       "60%",   ROJO,    "COGS promedio del negocio"),
            metric("Margen bruto actual",         "40%",   NARANJA, "Asumido en modelo predictivo"),
            metric("Ineficiencia de inventario",  "$640K", ROJO,    "↓ Costo de exceso de stock est."),
            metric("Margen potencial optimizado", "47%",   VERDE,   "↑ +7pp con prescripciones"),
        ], style={"display": "flex", "gap": "12px", "marginBottom": "16px", "flexWrap": "wrap"}),

        html.Div([
            html.Div([
                html.Div(style=CARD, children=[
                    section_title("Estructura de Costos", "Distribución estimada del COP invertido"),
                    dcc.Graph(figure=fig_costos(), config={"displayModeBar": False}),
                ]),
            ], style={"flex": "1", "minWidth": "280px"}),
            html.Div([
                html.Div(style=CARD, children=[
                    section_title("Margen por Categoría", "Margen real estimado vs objetivo prescrito"),
                    dcc.Graph(figure=fig_margen(), config={"displayModeBar": False}),
                ]),
            ], style={"flex": "1", "minWidth": "280px"}),
        ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),

        html.Div([
            html.Div([
                html.Div(style=CARD, children=[
                    section_title("Costos Ocultos Detectados", "Ineficiencias identificadas en la operación"),
                    alert_box("Sobrestock en artículos de bajo movimiento",
                              "Artículos sin venta en >60 días representan el 18% del inventario. "
                              "Costo de oportunidad: ~$640K bloqueados. Prescripción: liquidar con 15% descuento.", "crit"),
                    alert_box("Pérdida por ruptura de stock (Escolar)",
                              "Temporadas pico (enero, julio) registran quiebre en cuadernos y lápices. "
                              "Ventas perdidas estimadas: $280K por temporada. Prescripción: pedido preventivo 3 semanas antes.", "warn"),
                    alert_box("Servicios: mayor margen, menor visibilidad",
                              "Fotocopias e impresiones tienen margen ~55% pero solo representan 8% del ingreso. "
                              "Son el producto con mayor ROI por transacción. Prescripción: posicionar en la entrada.", "info"),
                ]),
            ], style={"flex": "1", "minWidth": "280px"}),
            html.Div([
                html.Div(style=CARD, children=[
                    section_title("Rotación de Inventario", "Actual vs benchmark óptimo (4.0× para papelerías pequeñas)"),
                    vs_bar("Escolar",    78, AZUL_CL),
                    vs_bar("Miscelánea", 55, NARANJA),
                    vs_bar("Oficina",    40, ROJO),
                    vs_bar("Papelería",  72, VERDE),
                    vs_bar("Servicios",  90, VERDE),
                    html.Hr(style={"borderColor": BORDER, "margin": "14px 0"}),
                    html.Div([
                        html.Strong("Meta prescrita: ", style={"color": "#1a1917"}),
                        "elevar todas las categorías a rotación ≥ 3.5× en 6 meses, priorizando ",
                        html.Strong("Oficina", style={"color": ROJO}),
                        " (gap mayor). Eso liberaría aprox. $420K en flujo de caja mensual adicional.",
                    ], style={"fontSize": "0.82rem", "color": MUTED, "lineHeight": "1.6"}),
                ]),
            ], style={"flex": "1", "minWidth": "280px"}),
        ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),
    ])


def tab_escala():
    def slider_row(label, id_slider, id_val, min_v, max_v, step, val, suffix):
        return html.Div([
            html.Label(label, style={"fontSize": "0.85rem", "color": MUTED, "minWidth": "180px"}),
            dcc.Slider(id=id_slider, min=min_v, max=max_v, step=step, value=val,
                       marks=None, tooltip={"always_visible": False},
                       className="dash-slider"),
            html.Span(id=id_val, style={"fontSize": "0.9rem", "fontWeight": "600",
                                         "color": AZUL, "minWidth": "60px", "textAlign": "right"}),
        ], style={"display": "flex", "alignItems": "center", "gap": "12px", "marginBottom": "14px"})

    escenarios = [
        ("🏪 Optimizar el local actual",
         "Reordenar exhibición, mejorar señalización, ampliar horario 1 hora. "
         "Inversión: $0–$200K. Ingreso proyectado: +18% en 3 meses."),
        ("📦 Ampliar surtido Oficina",
         "Incluir cartuchos de tinta, resmas de papel, carpetas. "
         "Inversión: $800K. Ingreso proyectado: +25% en 6 meses."),
        ("🚀 Segundo punto de venta",
         "Kiosco dentro del colegio o segundo local en Funza. "
         "Inversión: $4M+. Solo recomendado cuando rotación ≥ 3.8× en el local actual."),
    ]

    return html.Div([
        html.Div("Simula escenarios de crecimiento y prescribe los cuellos de botella que aparecerán primero.",
                 style={"color": MUTED, "fontSize": "0.88rem", "marginBottom": "18px"}),

        html.Div(style=CARD, children=[
            section_title("Simulador de Escalamiento · '¿Qué pasa si crecemos?'"),
            slider_row("Capacidad de ventas diarias", "cap-slider", "cap-val", 1.0, 4.0, 0.1, 1.0, "×"),
            slider_row("Inversión en marketing (%)",  "mkt-slider", "mkt-val", 0,   15,  1,   0,   "%"),
            slider_row("Ampliar horario (horas extra)","hr-slider", "hr-val",  0,   4,   1,   0,   " h"),
            html.Div(id="sim-metrics", style={"display": "flex", "gap": "12px", "marginTop": "16px", "flexWrap": "wrap"}),
        ]),

        html.Div([
            html.Div([
                html.Div(style=CARD, children=[
                    html.Div([
                        section_title("Cuellos de Botella Predichos", "Orden de colapso según el escalamiento"),
                        html.Span(id="collapse-label", style={"background": "#e8f5ee", "color": "#1e7a45",
                                                               "padding": "3px 10px", "borderRadius": "999px",
                                                               "fontSize": "0.75rem", "fontWeight": "600"}),
                    ], style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-start", "marginBottom": "14px"}),
                    html.Div(id="bottleneck-list"),
                ]),
            ], style={"flex": "1", "minWidth": "280px"}),
            html.Div([
                html.Div(style=CARD, children=[
                    section_title("Impacto Proyectado", "Ingresos con diferentes niveles de escalamiento"),
                    dcc.Graph(figure=fig_escala(), config={"displayModeBar": False}),
                ]),
            ], style={"flex": "1", "minWidth": "280px"}),
        ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),

        html.Div(style=CARD, children=[
            section_title("Escenarios de Expansión Prescritos"),
            html.Div([
                html.Div([
                    html.H5(titulo, style={"fontSize": "0.88rem", "fontWeight": "600", "marginBottom": "8px"}),
                    html.P(cuerpo, style={"fontSize": "0.82rem", "color": MUTED, "lineHeight": "1.55"}),
                ], style={"flex": "1", "minWidth": "180px", "background": SURFACE2,
                          "border": f"1px solid {BORDER}", "borderRadius": "12px", "padding": "14px"})
                for titulo, cuerpo in escenarios
            ], style={"display": "flex", "gap": "12px", "flexWrap": "wrap"}),
        ]),
    ])


def tab_validacion():
    recoms = [
        ("Reorganizar módulo Escolar",    "Ejecutado",  "chip-green",  "+$180K/mes", VERDE),
        ("Letrero precios fotocopias",    "Ejecutado",  "chip-green",  "+$95K/mes",  VERDE),
        ("Ampliar horario 1 hora AM",     "Ejecutado",  "chip-green",  "+$210K/mes", VERDE),
        ("Liquidar sobrestock Oficina",   "En proceso", "chip-orange", "Pendiente",  MUTED),
        ("Pedido anticipado temporada",   "Ejecutado",  "chip-green",  "+$280K",     VERDE),
        ("Tarjeta fidelización sellos",   "Planificado","chip-blue",   "Proy. +22%", MUTED),
        ("Combo impresión + producto",    "Ejecutado",  "chip-green",  "+$148K/mes", VERDE),
    ]
    chip_styles = {
        "chip-green":  {"background": "#e8f5ee", "color": "#1e7a45"},
        "chip-blue":   {"background": "#edf3fc", "color": AZUL},
        "chip-orange": {"background": "#fff3e0", "color": "#b85e00"},
    }

    return html.Div([
        html.Div("Contraste entre prescripciones emitidas y resultados observados. "
                 "Esta sección genera confianza para que la gerencia actúe sobre las recomendaciones del modelo.",
                 style={"color": MUTED, "fontSize": "0.88rem", "marginBottom": "18px"}),

        html.Div([
            metric("Recomendaciones emitidas", "12",   AZUL,    "Desde inicio del proyecto"),
            metric("Ejecutadas",               "7",    VERDE,   "↑ 58% tasa de adopción"),
            metric("Efectividad (ejecutadas)", "86%",  NARANJA, "↑ 6 de 7 cumplieron la meta"),
            metric("Impacto acumulado",        "$1.4M",VERDE,   "↑ Ingreso adicional generado"),
        ], style={"display": "flex", "gap": "12px", "marginBottom": "16px", "flexWrap": "wrap"}),

        html.Div([
            html.Div([
                html.Div(style=CARD, children=[
                    section_title("Predicho vs Real — Ganancia Mensual",
                                  "Modelo RLM (MAE $134 COP) frente a ganancia real mensual registrada"),
                    dcc.Graph(figure=fig_validacion(), config={"displayModeBar": False}),
                ]),
            ], style={"flex": "1", "minWidth": "280px"}),
            html.Div([
                html.Div(style=CARD, children=[
                    section_title("Historial de Recomendaciones", "Estado y resultado de cada prescripción"),
                    html.Table([
                        html.Thead(html.Tr([
                            html.Th("Recomendación", style={"padding":"8px 10px","background":SURFACE2,"borderBottom":f"1px solid {BORDER}","fontSize":"0.8rem","color":MUTED}),
                            html.Th("Estado",        style={"padding":"8px 10px","background":SURFACE2,"borderBottom":f"1px solid {BORDER}","fontSize":"0.8rem","color":MUTED}),
                            html.Th("Impacto real",  style={"padding":"8px 10px","background":SURFACE2,"borderBottom":f"1px solid {BORDER}","fontSize":"0.8rem","color":MUTED}),
                        ])),
                        html.Tbody([
                            html.Tr([
                                html.Td(rec,  style={"padding":"8px 10px","borderBottom":f"1px solid {BORDER}","fontSize":"0.84rem"}),
                                html.Td(html.Span(estado, style={**chip_styles[cls],"padding":"3px 10px","borderRadius":"999px","fontSize":"0.75rem","fontWeight":"600"}),
                                        style={"padding":"8px 10px","borderBottom":f"1px solid {BORDER}"}),
                                html.Td(imp,  style={"padding":"8px 10px","borderBottom":f"1px solid {BORDER}","fontSize":"0.84rem","fontWeight":"600","color":col}),
                            ]) for rec, estado, cls, imp, col in recoms
                        ]),
                    ], style={"width": "100%", "borderCollapse": "collapse"}),
                ]),
            ], style={"flex": "1", "minWidth": "280px"}),
        ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),

        html.Div(style=CARD, children=[
            section_title("Confianza del Modelo — Métricas de Validación Técnica",
                          "Indicadores del análisis predictivo (RLM entrenada con 38.895 obs.)"),
            html.Div([
                html.Div([
                    html.Div("R² Conjunto de Prueba", style={"fontSize":"0.82rem","color":MUTED,"marginBottom":"4px"}),
                    html.Div("0.9932", style={"fontSize":"1.6rem","fontWeight":"600","color":VERDE}),
                    html.Div("Explica el 99.3% de la variabilidad de la ganancia",
                             style={"fontSize":"0.75rem","color":MUTED,"marginTop":"4px"}),
                ], style={"flex":"1","minWidth":"160px"}),
                html.Div([
                    html.Div("MAE (Error Medio Absoluto)", style={"fontSize":"0.82rem","color":MUTED,"marginBottom":"4px"}),
                    html.Div("$134 COP", style={"fontSize":"1.6rem","fontWeight":"600","color":AZUL}),
                    html.Div("Error promedio por transacción predicha en prueba",
                             style={"fontSize":"0.75rem","color":MUTED,"marginTop":"4px"}),
                ], style={"flex":"1","minWidth":"160px"}),
                html.Div([
                    html.Div("Sobreajuste (Train – Test R²)", style={"fontSize":"0.82rem","color":MUTED,"marginBottom":"4px"}),
                    html.Div("-0.0107", style={"fontSize":"1.6rem","fontWeight":"600","color":VERDE}),
                    html.Div("Diferencia mínima → no hay sobreajuste significativo",
                             style={"fontSize":"0.75rem","color":MUTED,"marginTop":"4px"}),
                ], style={"flex":"1","minWidth":"160px"}),
            ], style={"display":"flex","gap":"24px","flexWrap":"wrap","marginBottom":"16px"}),
            alert_box("Diagnóstico de confianza: ALTO",
                      "Las métricas del modelo son sólidas (R²=0.99, MAE bajo, sin sobreajuste). "
                      "El 86% de las recomendaciones ejecutadas cumplieron su meta. "
                      "El modelo es confiable como insumo para decisiones comerciales de Mundo Abstracto.", "ok"),
        ]),
    ])


# ──────────────────────────────────────────────
# APP PRINCIPAL
# ──────────────────────────────────────────────

app = dash.Dash(
    __name__,
    title="Dashboard Prescriptivo · Mundo Abstracto",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server  # ← necesario para despliegue en Render / Railway

app.layout = html.Div(style={"fontFamily": FONT, "background": BG, "minHeight": "100vh"}, children=[

    # ── TOP BAR
    html.Div([
        html.Div([
            html.Div("MA", style={
                "background": NARANJA, "color": "#fff", "width": "30px", "height": "30px",
                "borderRadius": "8px", "display": "flex", "alignItems": "center",
                "justifyContent": "center", "fontSize": "0.75rem", "fontWeight": "600",
            }),
            html.Span("Dashboard Prescriptivo · Mundo Abstracto",
                      style={"fontWeight": "600", "fontSize": "1rem"}),
        ], style={"display": "flex", "alignItems": "center", "gap": "10px"}),
        html.Div("Análisis Prescriptivo · Funza 2024", style={
            "background": "rgba(255,255,255,.15)", "border": "1px solid rgba(255,255,255,.25)",
            "padding": "4px 12px", "borderRadius": "999px", "fontSize": "0.78rem",
        }),
    ], style={
        "background": AZUL, "color": "#fff", "padding": "0 28px",
        "display": "flex", "alignItems": "center", "justifyContent": "space-between",
        "height": "58px", "position": "sticky", "top": "0", "zIndex": "100",
        "boxShadow": "0 2px 16px rgba(15,76,129,.25)",
    }),

    # ── TABS
    dcc.Tabs(id="main-tabs", value="brechas", style={"borderBottom": f"1px solid {BORDER}"},
             colors={"border": BORDER, "primary": AZUL, "background": SURFACE},
             children=[
        dcc.Tab(label="🔍 Análisis de Brechas",     value="brechas",   style=TAB_STYLE, selected_style=TAB_SELECTED),
        dcc.Tab(label="💎 Lealtad & Valor Cliente", value="lealtad",   style=TAB_STYLE, selected_style=TAB_SELECTED),
        dcc.Tab(label="⚙️ Cadena de Valor",         value="cadena",    style=TAB_STYLE, selected_style=TAB_SELECTED),
        dcc.Tab(label="🚀 Escalamiento",            value="escala",    style=TAB_STYLE, selected_style=TAB_SELECTED),
        dcc.Tab(label="✅ Validación",              value="validacion",style=TAB_STYLE, selected_style=TAB_SELECTED),
    ]),

    # ── CONTENIDO
    html.Div(id="tab-content", style={"maxWidth": "1280px", "margin": "0 auto", "padding": "24px 28px 60px"}),
])

# ──────────────────────────────────────────────
# CALLBACKS
# ──────────────────────────────────────────────

@app.callback(Output("tab-content", "children"), Input("main-tabs", "value"))
def render_tab(tab):
    if tab == "brechas":   return tab_brechas()
    if tab == "lealtad":   return tab_lealtad()
    if tab == "cadena":    return tab_cadena()
    if tab == "escala":    return tab_escala()
    if tab == "validacion":return tab_validacion()

# Simulador de escalamiento
@app.callback(
    Output("cap-val",        "children"),
    Output("mkt-val",        "children"),
    Output("hr-val",         "children"),
    Output("sim-metrics",    "children"),
    Output("bottleneck-list","children"),
    Output("collapse-label", "children"),
    Output("collapse-label", "style"),
    Input("cap-slider", "value"),
    Input("mkt-slider", "value"),
    Input("hr-slider",  "value"),
    prevent_initial_call=True,
)
def update_sim(cap, mkt, hr):
    cap = cap or 1.0
    mkt = mkt or 0
    hr  = hr  or 0

    cap_txt = f"{cap:.1f}×"
    mkt_txt = f"{mkt}%"
    hr_txt  = f"+{hr} h"

    # Proyección con saturación
    sat_point = 1.6
    mult = cap if cap <= sat_point else sat_point + (cap - sat_point) * 0.3
    rev  = min(4.2 * mult * (1 + mkt / 100) * (1 + hr * 0.04), 10.8)
    gain = rev * 0.40
    cust = int(62 * cap * (1 + mkt / 80) * (1 + hr * 0.06))
    stress_map = [(1.4, "Bajo", VERDE), (2.0, "Moderado", NARANJA), (2.8, "Alto", ROJO), (9, "Crítico", "#8b1e10")]
    stress, s_color = next((s, c) for th, s, c in stress_map if cap <= th)

    metrics_cards = [
        metric("Ingreso proyectado",     f"${rev:.1f}M", VERDE),
        metric("Ganancia estimada",      f"${gain:.2f}M", AZUL),
        metric("Clientes/día proy.",     str(cust),       NARANJA),
        metric("Estrés operativo",       stress,          s_color),
    ]

    # Cuellos de botella
    bn_data = [
        (1, "Atención al cliente",    "Cap. actual: 1 persona · Satura a 1.6×", cap / 1.6),
        (2, "Gestión de caja",        "Sin sistema POS · Satura a 2.1×",         cap / 2.1),
        (3, "Inventario / bodega",    "Espacio limitado · Satura a 2.8×",         cap / 2.8),
        (4, "Proveedores",            "Tiempo de reposición 5–7 días",             cap / 3.8),
    ]
    rank_styles = ["#fdecea","#fff3e0","#fff8e1","#e8f5ee"]
    rank_colors = [ROJO, "#b85e00", "#7a4900", "#1e7a45"]

    def sat_color(v):
        pct = min(v, 1.0)
        if pct >= 0.90: return ROJO
        if pct >= 0.70: return NARANJA
        return VERDE

    bn_items = [
        html.Div([
            html.Div(str(rank), style={"width":"28px","height":"28px","borderRadius":"50%",
                                        "display":"flex","alignItems":"center","justifyContent":"center",
                                        "fontSize":"0.8rem","fontWeight":"700","flexShrink":"0",
                                        "background": rank_styles[rank-1], "color": rank_colors[rank-1]}),
            html.Div([
                html.Div(name, style={"fontSize":"0.88rem","fontWeight":"600"}),
                html.Div(desc, style={"fontSize":"0.78rem","color":MUTED}),
            ], style={"flex":"1"}),
            html.Div(f"{min(sat,1)*100:.0f}%", style={"fontSize":"0.9rem","fontWeight":"700",
                                                        "color": sat_color(sat), "minWidth":"48px","textAlign":"right"}),
        ], style={"display":"flex","alignItems":"center","gap":"12px","padding":"10px 0",
                  "borderBottom":f"1px solid {BORDER}"})
        for rank, name, desc, sat in bn_data
    ]

    bn1_pct = min(cap / 1.6, 1.0)
    if bn1_pct >= 0.90:
        lbl_text = "⚠ Colapso: Atención"
        lbl_style = {"background":"#fdecea","color":"#b33220","padding":"3px 10px","borderRadius":"999px","fontSize":"0.75rem","fontWeight":"600"}
    elif bn1_pct >= 0.70:
        lbl_text = "Riesgo moderado"
        lbl_style = {"background":"#fff3e0","color":"#b85e00","padding":"3px 10px","borderRadius":"999px","fontSize":"0.75rem","fontWeight":"600"}
    else:
        lbl_text = "Sin riesgo inmediato"
        lbl_style = {"background":"#e8f5ee","color":"#1e7a45","padding":"3px 10px","borderRadius":"999px","fontSize":"0.75rem","fontWeight":"600"}

    return cap_txt, mkt_txt, hr_txt, metrics_cards, bn_items, lbl_text, lbl_style


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)