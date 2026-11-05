#!/usr/bin/env python3
"""Lee Excel real, valida y genera JSON. pip install artifact-tool"""
import json, unicodedata, collections, argparse
from pathlib import Path
from artifact_tool import Blob,SpreadsheetFile
P=Path(__file__).resolve().parents[1]
def norm(s):
    return ' '.join(''.join(c for c in unicodedata.normalize('NFKD',str(s or '')) if not unicodedata.combining(c)).upper().split())
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--excel',default=str(P/'Areas_Inundadas_Municipios_Frente_Frio.xlsx'));args=parser.parse_args()
    source=Path(args.excel)
    if not source.exists(): raise SystemExit(f'ERROR: no existe {source}')
    wb=SpreadsheetFile.import_xlsx(Blob.load(str(source)))
    sh=wb.worksheets.get_item('Orden x dpto')
    rows=sh.get_range('A1:E1000').values
    expected=['Municipio','Departamento','Area_Municipio_ha','Area_Inundada_ha','%_Area_inundada']
    if rows[0]!=expected: raise ValueError('Encabezados inesperados: '+str(rows[0]))
    out=[]; warnings=[];keys=set()
    for idx,r in enumerate(rows[1:],2):
        if not r[0] and not r[1]:continue
        try: area=float(r[2]); flood=float(r[3]);pct=float(r[4]);
        except (ValueError,TypeError): warnings.append(f'Fila {idx}: dato numérico inválido');continue
        key=norm(r[1])+'|'+norm(r[0]);
        if key in keys:warnings.append(f'Fila {idx}: municipio repetido {key}')
        keys.add(key)
        if area<=0 or flood<0 or flood>area or not 0<=pct<=100:warnings.append(f'Fila {idx}: magnitudes fuera de rango')
        calculated=100*flood/area if area>0 else None
        if calculated is not None and abs(calculated-pct)>0.015:warnings.append(f'Fila {idx}: porcentaje inconsistente ({pct} vs {calculated})')
        out.append({'municipio':str(r[0]).strip(),'departamento':str(r[1]).strip(),'areaMunicipio':area,'areaInundada':flood,'porcentaje':pct,'porcentajeCalculado':calculated,'key':key})
    (P/'data').mkdir(exist_ok=True)
    (P/'data'/'inundaciones.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    validation={'registros':len(out),'departamentos':len(set(x['departamento'] for x in out)),'areaInundadaTotal':sum(x['areaInundada'] for x in out),'advertencias':warnings}
    (P/'data'/'validacion.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(validation,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
