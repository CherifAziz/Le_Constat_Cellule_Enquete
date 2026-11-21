"""Dessine le graphique en mémoire puis exporte un PNG. reportlab, pypdfium2."""
from pathlib import Path
import csv
import io
import pypdfium2 as pdfium
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.lib.colors import HexColor

ROOT=Path(__file__).resolve().parent
with (ROOT/"calculs/annuel.csv").open(encoding="utf-8-sig") as f:
    rows=list(csv.DictReader(f,delimiter=";"))
ink, blue, rust, muted, grid = map(HexColor,["#152538","#1B6177","#B7472D","#415669","#CBD5DB"])
drawing=Drawing(820,425)
drawing.add(Rect(0,0,820,425,fillColor=HexColor("#FFFFFF"),strokeColor=None))


def label(x,y,message,size=10,color=ink,bold=False,align="start"):
    drawing.add(String(x,y,message,fontName="Helvetica-Bold" if bold else "Helvetica",
                       fontSize=size,fillColor=color,textAnchor=align))


label(40,385,"La France a parfois couvert ses dépenses hors intérêts",23,bold=True)
label(40,360,"Administrations publiques, 1974–2025. Solde en % du PIB, positif en cas d’excédent.",12,muted)
chart=LinePlot()
chart.x,chart.y,chart.width,chart.height=58,81,720,240
chart.data=[[(int(r["annee"]),float(r[name])) for r in rows] for name in ("primaire_pct","b9_pct")]
chart.xValueAxis.valueMin=1974
chart.xValueAxis.valueMax=2025
chart.xValueAxis.valueSteps=[1974,1980,1990,2000,2010,2020,2025]
chart.yValueAxis.valueMin=-10
chart.yValueAxis.valueMax=3
chart.yValueAxis.valueSteps=[-10,-8,-6,-4,-2,0,2]
chart.yValueAxis.visibleGrid=1
chart.yValueAxis.gridStrokeColor=grid
chart.yValueAxis.gridStrokeWidth=.45
for axis in [chart.xValueAxis,chart.yValueAxis]:
    axis.strokeColor=grid
    axis.labels.fillColor=muted
    axis.labels.fontSize=9
chart.lines[0].strokeColor=blue
chart.lines[1].strokeColor=rust
chart.lines.strokeWidth=2
drawing.add(chart)
zero=chart.y+chart.height*10/13
drawing.add(Line(chart.x,zero,chart.x+chart.width,zero,strokeColor=muted,strokeWidth=.65,strokeDashArray=[3,3]))
for x,c,title in [(58,blue,"Solde primaire (intérêts D41 ajoutés)"),(340,rust,"Solde total")]:
    drawing.add(Line(x,333,x+21,333,strokeColor=c,strokeWidth=2.5))
    label(x+27,329,title,11,c,bold=True)
label(40,43,"9 exercices sur 51 en excédent primaire D41. Le solde total reste négatif de 1975 à 2025.",12,bold=True)
label(40,21,"Source : Insee, tableaux 3.201 et 3.106, comptes 2025 en base 2020. Calculs de la contre-enquête.",9,muted)
pdf=pdfium.PdfDocument(io.BytesIO(renderPDF.drawToString(drawing)))
pdf[0].render(scale=1.7).to_pil().save(ROOT/"soldes_1974_2025.png")
