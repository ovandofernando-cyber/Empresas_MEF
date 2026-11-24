# Esquema de datos por empresa (`datos/empresas/<id>.json`)

Un archivo JSON por persona/estructura jurídica, con `id` igual al de `datos/empresas_base.csv`.
Todo dato extraído lleva su **fuente** (`archivo` relativo a la carpeta de la empresa dentro del zip del MEF, y `pagina`).
Los textos se transcriben tal como figuran; si algo es dudoso (OCR, manuscrito ilegible) se marca `"confianza": "baja"`.

```json
{
  "id": "ueno_bank",
  "razon_social": "UENO BANK S.A.",
  "ruc": "80026157-7",
  "tipo": "Sociedad Anónima | S.A.E.C.A. | S.R.L. | E.A.S. | Fideicomiso | Condominio | ...",
  "carpeta_mef": "UENO BANK S.A",
  "denominaciones_anteriores": [{"nombre": "...", "hasta": "AAAA-MM-DD", "fuente": {}}],
  "constitucion": {"fecha": "AAAA-MM-DD", "escritura": "N° ..", "escribano": "...", "inscripcion_registro_publico": "...", "fuente": {}},
  "domicilio": [{"direccion": "...", "fecha_dato": "AAAA-MM-DD", "fuente": {}}],
  "objeto_social": "resumen breve",
  "actividad_principal": "texto breve (banca, seguros, tecnología, inmobiliaria, turismo, agro, medios, etc.)",
  "plazo_duracion": "...",
  "capital": [{"tipo": "social|autorizado|suscripto|integrado", "monto": 0, "moneda": "PYG|USD", "valor_nominal_accion": 0, "cantidad_acciones": 0, "fecha_dato": "AAAA-MM-DD", "fuente": {}}],
  "accionistas": [{
      "nombre": "...", "tipo_persona": "fisica|juridica|desconocido",
      "documento": "CI 1234567 | RUC 80000000-0 | pasaporte ...", "nacionalidad": "...",
      "acciones": 0, "clase_acciones": "ordinarias/preferidas/...", "votos": 0,
      "porcentaje": 0.0, "porcentaje_calculado": false,
      "fecha_dato": "AAAA-MM-DD", "vigente": true,
      "fuente": {"archivo": "REGISTRO DE ACCIONISTAS.pdf", "pagina": 3}, "confianza": "alta|media|baja", "notas": ""
  }],
  "autoridades": [{
      "nombre": "...", "documento": "...", "cargo": "Presidente|Vicepresidente|Director titular|Director suplente|Síndico titular|Síndico suplente|Gerente|Administrador|Representante legal|Apoderado|Fiduciario|...",
      "fecha_asuncion": "AAAA-MM-DD", "vigencia": "...", "fecha_dato": "AAAA-MM-DD", "vigente": true,
      "fuente": {}, "confianza": "alta|media|baja"
  }],
  "beneficiarios_finales": [{
      "nombre": "...", "documento": "...", "nacionalidad": "...", "domicilio": "...",
      "porcentaje": 0.0, "tipo_control": "propiedad directa|propiedad indirecta|control por otros medios|...",
      "cadena_control": "texto: a través de qué sociedades", "fecha_dato": "AAAA-MM-DD", "fuente": {}, "confianza": "alta"
  }],
  "historial": [{"fecha": "AAAA-MM-DD", "evento": "constitucion|modificacion_estatutos|aumento_capital|transferencia_acciones|cambio_directorio|cambio_denominacion|fusion|otro", "detalle": "...", "fuente": {}}],
  "vinculos": [{"entidad_o_persona": "...", "tipo": "accionista_de|participada|director_comun|mismo_domicilio|mismo_solicitante|mismo_correo_dominio|mencion_en_documento|otro", "detalle": "...", "fuente": {}}],
  "declarantes_siara": [{"nombre": "...", "documento": "...", "correo": "...", "telefono": "...", "fecha": "AAAA-MM-DD", "fuente": {}}],
  "correos_dominios": ["uenoholding.com.py", "gvcorp.com.py"],
  "documentos": [{"archivo": "...", "tipo": "constancia_RA|constancia_BF|registro_accionistas|acta_asamblea|acta_directorio|escritura_constitucion|escritura_modificacion|contrato_fideicomiso|otro", "fecha": "AAAA-MM-DD", "paginas": 0, "legibilidad": "texto|ocr_bueno|ocr_malo|manuscrito", "resumen": "1-3 líneas"}],
  "observaciones": ["inconsistencias, documentos pendientes de aprobación, vacíos de información, etc."]
}
```

Reglas:
- Personas físicas: nombre completo en MAYÚSCULAS sin tildes en `nombre_normalizado` es opcional; el consolidado normaliza. Siempre que exista, registrar el número de CI: es la clave para cruzar personas entre empresas.
- Porcentajes: si el documento no lo trae, calcularlo sobre el total de acciones del mismo registro y marcar `porcentaje_calculado: true`.
- Si hay varias fechas (registros históricos), conservar todas las filas con su `fecha_dato` y marcar `vigente` en las más recientes.
- No inventar datos. Campo desconocido = `null`.
