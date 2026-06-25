import json
from datetime import datetime
from itertools import combinations

def procesar_datos(json_bot1):
    # 1. Leer el JSON del Bot 1
    datos = json.loads(json_bot1)
    
    info_sistema = datos['informacion_sistema']
    ventas = datos['ventas_crudas_del_dia']
    inventario = datos['inventario_crudo_actual']
    
    # Obtener tasa BCV
    tasa_bcv = float(info_sistema.get('tasa_bcv_utilizada', 1.0))
    if tasa_bcv <= 0:
        tasa_bcv = 1.0

    # 2. Cajas vacías para acumular los datos
    venta_total_dia = 0.0
    costo_total_dia = 0.0
    total_articulos = 0.0
    clientes_globales = set()
    compras_por_cliente = {} 
    
    por_categoria = {}
    for item in inventario:
        cat_existente = item['categoria']
        if cat_existente not in por_categoria:
            por_categoria[cat_existente] = {"ventas_usd": 0.0, "costo_usd": 0.0, "ganancia_usd": 0.0}
    
    por_producto = {}
    
    bloques_horarios = {
        "Mañana": {"clientes": set(), "monto": 0.0, "productos": {}},
        "Tarde": {"clientes": set(), "monto": 0.0, "productos": {}},
        "Noche": {"clientes": set(), "monto": 0.0, "productos": {}}
    }

    # 3. Procesar cada venta una por una
    for v in ventas:
        nombre = v['nombre']
        cat = v['categoria']
        cant = float(v['cantidad_vendida'])
        
        precio = float(v['precio_venta_usd']) / tasa_bcv
        costo = float(v['costo_unidad_usd']) / tasa_bcv
        
        hora_str = v['hora_venta']
        cliente = v['id_cliente']
        factura = v.get('numero_factura', f"{cliente}_{hora_str}")

        subtotal_venta = cant * precio
        subtotal_costo = cant * costo
        
        venta_total_dia += subtotal_venta
        costo_total_dia += subtotal_costo
        total_articulos += cant
        
        if cliente:
            clientes_globales.add(cliente)
            
        if factura not in compras_por_cliente:
            compras_por_cliente[factura] = set()
        compras_por_cliente[factura].add(nombre)

        if cat not in por_categoria:
            por_categoria[cat] = {"ventas_usd": 0.0, "costo_usd": 0.0, "ganancia_usd": 0.0}
        por_categoria[cat]["ventas_usd"] += subtotal_venta
        por_categoria[cat]["costo_usd"] += subtotal_costo
        por_categoria[cat]["ganancia_usd"] += (subtotal_venta - subtotal_costo)

        if nombre not in por_producto:
            por_producto[nombre] = {
                "cantidad": 0.0, 
                "total_usd": 0.0,
                "precio_unidad": precio,
                "costo_unidad": costo
            }
        por_producto[nombre]["cantidad"] += cant
        por_producto[nombre]["total_usd"] += subtotal_venta

        try:
            hora_obj = datetime.strptime(hora_str, "%H:%M").time()
            if hora_obj < datetime.strptime("12:00", "%H:%M").time():
                bloque = "Mañana"
            elif hora_obj < datetime.strptime("18:00", "%H:%M").time():
                bloque = "Tarde"
            else:
                bloque = "Noche"
        except:
            bloque = "Noche"

        if cliente:
            bloques_horarios[bloque]["clientes"].add(cliente)
        bloques_horarios[bloque]["monto"] += subtotal_venta
        bloques_horarios[bloque]["productos"][nombre] = bloques_horarios[bloque]["productos"].get(nombre, 0) + cant

    # 4. Calcular KPIs Globales
    ganancia_usd = venta_total_dia - costo_total_dia
    ganancia_porc = (ganancia_usd / venta_total_dia * 100) if venta_total_dia > 0 else 0.0
    
    cant_clientes = len(clientes_globales)
    total_facturas = len(compras_por_cliente)
    ticket_promedio = (venta_total_dia / total_facturas) if total_facturas > 0 else 0.0
    articulos_por_factura = (total_articulos / total_facturas) if total_facturas > 0 else 0.0
    articulos_por_cliente = (total_articulos / cant_clientes) if cant_clientes > 0 else 0.0

    kpis_globales = {
        "venta_total_usd": round(venta_total_dia, 2),
        "ganancia_real_usd": round(ganancia_usd, 2),
        "ganancia_real_porcentaje": round(ganancia_porc, 2),
        "ticket_promedio_usd": round(ticket_promedio, 2),
        "total_clientes": cant_clientes,
        "total_facturas": total_facturas,
        "articulos_por_factura": round(articulos_por_factura, 2)
        "articulos_por_cliente": round(articulos_por_cliente, 2)
    }

    # 5. Construir Tabla de Categorías
    lista_categorias = []
    for c, v in por_categoria.items():
        part_porc = (v["ganancia_usd"] / ganancia_usd * 100) if ganancia_usd > 0 else 0.0
        lista_categorias.append({
            "categoria": c,
            "ventas_totales_usd": round(v["ventas_usd"], 2),
            "porcentaje_participacion": round(part_porc, 2)
        })
    lista_categorias = sorted(lista_categorias, key=lambda x: x["ventas_totales_usd"], reverse=True)

    # 6. Construir Tabla de Mix de Productos
    lista_mix_productos = []
    for p, v in por_producto.items():
        mix_porc = (v["total_usd"] / venta_total_dia * 100) if venta_total_dia > 0 else 0.0
        lista_mix_productos.append({
            "nombre": p,
            "cantidad_vendida": round(v["cantidad"], 2),
            "total_usd": round(v["total_usd"], 2),
            "porcentaje_mix_venta": round(mix_porc, 2)
        })
    lista_mix_productos = sorted(lista_mix_productos, key=lambda x: x["total_usd"], reverse=True)

    # Top 20 Más Vendidos
    prod_ordenados_cantidad = sorted(por_producto.items(), key=lambda x: x[1]["cantidad"], reverse=True)[:20]
    top_20_mas_vendidos = []
    for p, v in prod_ordenados_cantidad:
        top_20_mas_vendidos.append({
            "nombre": p,
            "unidades_vendidas": round(v["cantidad"], 2)
        })

    # Top 20 Más Rentables
    prod_ordenados_ganancia = sorted(
        por_producto.items(), 
        key=lambda x: (x[1]["precio_unidad"] - x[1]["costo_unidad"]), 
        reverse=True
    )[:20]
    
    top_20_mas_rentables = []
    for p, v in prod_ordenados_ganancia:
        gan_uni = v["precio_unidad"] - v["costo_unidad"]
        porc_gan = (gan_uni / v["precio_unidad"] * 100) if v["precio_unidad"] > 0 else 0.0
        top_20_mas_rentables.append({
            "nombre": p,
            "porcentaje_ganancia": round(porc_gan, 2),
            "ganancia_por_unidad_usd": round(gan_uni, 2)
        })

    # 7. Construir bloques de horarios
    comportamiento_temporal = {}
    for b, v in bloques_horarios.items():
        prod_ordenados = dict(sorted(v["productos"].items(), key=lambda x: x[1], reverse=True))
        prod_limpios = {p: round(c, 2) for p, c in prod_ordenados.items()}
        comportamiento_temporal[b] = {
            "facturas": len(v["clientes"]),
            "monto_total_usd": round(v["monto"], 2),
            "productos_vendidos": prod_limpios
        }
        
    # 8. NUEVO: Análisis de Patrones Frecuentes (Grupos de cualquier tamaño)
    # Paso A: Ver qué se vendió al menos 2 veces hoy
    conteo_individual = {}
    for productos in compras_por_cliente.values():
        for p in productos:
            conteo_individual[p] = conteo_individual.get(p, 0) + 1
            
    items_frecuentes = {p for p, c in conteo_individual.items() if c >= 2}

    # Paso B: Buscar patrones usando solo los productos frecuentes
    conteo_patrones = {}
    for productos in compras_por_cliente.values():
        canasta = [p for p in productos if p in items_frecuentes]
        canasta.sort() 
        
        if len(canasta) >= 2:
            max_tamano = min(len(canasta), 4) # Busca grupos de hasta 4 cosas para no saturarse
            for tamano in range(2, max_tamano + 1):
                for combo in combinations(canasta, tamano):
                    conteo_patrones[combo] = conteo_patrones.get(combo, 0) + 1

    # Desempate por tamaño de grupo
    patrones_ordenados = sorted(conteo_patrones.items(), key=lambda x: (x[1], len(x[0])), reverse=True)[:5]
    
    lista_productos_asociados = []
    for combo, cantidad in patrones_ordenados:
        lista_productos_asociados.append({
            "combo": " + ".join(combo),
            "veces_vendidos_juntos": cantidad
        })

    # Convertir el inventario a USD
    inventario_usd = []
    for item in inventario:
        nuevo_item = item.copy()
        nuevo_item['precio_venta_usd'] = round(float(item['precio_venta_usd']) / tasa_bcv, 2)
        nuevo_item['costo_unidad_usd'] = round(float(item['costo_unidad_usd']) / tasa_bcv, 2)
        inventario_usd.append(nuevo_item)

    # 9. Unir todo en el JSON de salida
    json_final = {
        "informacion_sistema": info_sistema,
        "kpis_globales": kpis_globales,
        "tabla_categorias": lista_categorias,
        "tabla_mix_productos": lista_mix_productos,
        "top_20_mas_vendidos": top_20_mas_vendidos,
        "top_20_mas_rentables": top_20_mas_rentables,
        "comportamiento_temporal": comportamiento_temporal,
        "productos_asociados": lista_productos_asociados, 
        "inventario_crudo_actual": inventario_usd
    }

    return json.dumps(json_final, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    with open("bot1.txt", "r", encoding="utf-8") as archivo:
        datos_reales = archivo.read()
    
    resultado = procesar_datos(datos_reales)
    print(resultado)
