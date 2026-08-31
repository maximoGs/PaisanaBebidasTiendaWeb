"""
Script para sincronizar e integrar inventario.xlsx en Paisana Bebidas (data/products.js)
Asigna imágenes conceptuales/producto de alta calidad y metadatos acordes a cada ítem.
"""

import pandas as pd
import json
import re
import os

def clean_title(text):
    if not isinstance(text, str):
        return ""
    words = text.strip().split()
    cleaned_words = []
    for w in words:
        upper = w.upper()
        if upper in ["ML", "L", "LTS", "LT", "GR", "GRS", "KG", "CC", "7UP", "IPA", "APA", "X1", "X2", "X3", "X6", "X12", "X130GR", "RTD", "BIB"]:
            cleaned_words.append(upper)
        elif upper.startswith("750") or upper.startswith("500") or upper.startswith("473") or upper.startswith("710") or upper.startswith("355") or upper.startswith("187"):
            cleaned_words.append(upper)
        elif upper in ["DE", "DEL", "Y", "LA", "EN", "CON", "A", "POR", "SIN"]:
            cleaned_words.append(w.lower())
        else:
            cleaned_words.append(w.capitalize())
    
    res = " ".join(cleaned_words)
    if res:
        res = res[0].upper() + res[1:]
    return res

def get_category_and_subcategory(rubro, desc):
    rubro = str(rubro).upper().strip()
    desc_upper = str(desc).upper().strip()

    cat = "bebidas"
    subcat = "cervezas"

    if "VINOS TINTOS" in rubro:
        cat = "vinos"
        if "MALBEC" in desc_upper:
            subcat = "malbec"
        elif "CABERNET" in desc_upper:
            subcat = "cabernet-sauvignon"
        else:
            subcat = "blends"
    elif "VINOS BLANCOS" in rubro:
        cat = "vinos"
        subcat = "blancos-chardonnay"
    elif "VINOS DULCES" in rubro:
        cat = "vinos"
        subcat = "blancos-chardonnay"
    elif "ESPUMANTES" in rubro:
        cat = "vinos"
        subcat = "espumantes"
    elif "VINOS ROSADOS" in rubro:
        cat = "vinos"
        subcat = "rosados"
    elif "VINOS 375" in rubro:
        cat = "vinos"
        subcat = "blends"
    elif "BAG IN BOX" in rubro or "DAMAJUANAS" in rubro:
        cat = "vinos"
        subcat = "blends"
    elif "VINOS SIN ALCOHOL" in rubro:
        cat = "sin-alcohol"
        subcat = "aguas-jugos"
    elif "CERVEZAS SIN ALCOHOL" in rubro:
        cat = "sin-alcohol"
        subcat = "gaseosas"
    elif "CERVEZAS" in rubro:
        cat = "bebidas"
        subcat = "cervezas"
    elif "VODKA" in rubro:
        cat = "bebidas"
        subcat = "vodka"
    elif "WHISKY" in rubro:
        cat = "bebidas"
        subcat = "whisky"
    elif "GIN" in rubro:
        cat = "bebidas"
        subcat = "gin"
    elif "FERNET" in rubro or "APERITIVOS" in rubro or "VERMOUTH" in rubro or "RON" in rubro or "READY TO DRINK" in rubro:
        cat = "bebidas"
        subcat = "fernet-aperitivos"
    elif "OTRAS BEBIDAS BLANCAS" in rubro:
        cat = "bebidas"
        if "VODKA" in desc_upper:
            subcat = "vodka"
        elif "GIN" in desc_upper:
            subcat = "gin"
        elif "WHISKY" in desc_upper:
            subcat = "whisky"
        else:
            subcat = "fernet-aperitivos"
    elif "GASEOSAS" in rubro:
        cat = "sin-alcohol"
        subcat = "gaseosas"
    elif "JUGOS" in rubro or "AGUAS" in rubro or "SODAS" in rubro:
        cat = "sin-alcohol"
        subcat = "aguas-jugos"
    elif "ENERGIZANTES" in rubro:
        cat = "sin-alcohol"
        subcat = "energizantes"
    elif "SNACKS" in rubro:
        cat = "snacks"
        subcat = "snacks-salados"
    elif "COMBOS" in rubro:
        cat = "snacks"
        subcat = "promos-combos"
    elif "CAFE" in rubro or "CIGARRILLO" in rubro:
        cat = "snacks"
        subcat = "chocolates-dulces"
    elif "HIELOS" in rubro or "LEÑA" in rubro or "LEA" in rubro:
        cat = "snacks"
        subcat = "hielo-descartables"
    else:
        if "VINO" in desc_upper or "MALBEC" in desc_upper or "CABERNET" in desc_upper:
            cat = "vinos"
            subcat = "malbec" if "MALBEC" in desc_upper else "blends"
        elif "CERVEZA" in desc_upper or "CORONA" in desc_upper or "HEINEKEN" in desc_upper:
            cat = "bebidas"
            subcat = "cervezas"
        elif "COCA" in desc_upper or "SPRITE" in desc_upper or "FANTA" in desc_upper:
            cat = "sin-alcohol"
            subcat = "gaseosas"
        elif "COMBO" in desc_upper:
            cat = "snacks"
            subcat = "promos-combos"
        else:
            cat = "snacks"
            subcat = "snacks-salados"

    return cat, subcat

def get_product_image(cat, subcat, rubro, desc):
    """Retorna una imagen conceptual de alta resolución y fidelidad según el producto específico."""
    u = desc.upper()
    r = rubro.upper()

    # --- VINOS ---
    if cat == "vinos":
        if "MALBEC" in u:
            return "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800&auto=format&fit=crop&q=80"
        if "CABERNET" in u or "FRANC" in u:
            return "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=800&auto=format&fit=crop&q=80"
        if "ESPUMANTE" in r or "BRUT" in u or "CHANDON" in u or "EXTRA BRUT" in u or "ESPUMANTE" in u:
            return "https://images.unsplash.com/photo-1594142345550-949f57564d26?w=800&auto=format&fit=crop&q=80"
        if "CHARDONNAY" in u or "SAUVIGNON BLANC" in u or "BLANCO" in u or "BLANCS" in u:
            return "https://images.unsplash.com/photo-1569919659476-f0852f6834b7?w=800&auto=format&fit=crop&q=80"
        if "ROSE" in u or "ROSADO" in u or "ROXE" in u:
            return "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800&auto=format&fit=crop&q=80"
        if "DULCE" in u or "DULCES" in r:
            return "https://images.unsplash.com/photo-1584916201218-f4242ceb4809?w=800&auto=format&fit=crop&q=80"
        if "DAMAJUANA" in u or "BAG IN BOX" in u or "BIB" in u:
            return "https://images.unsplash.com/photo-1547595628-c61a29f496f0?w=800&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800&auto=format&fit=crop&q=80"

    # --- BEBIDAS ALCOHÓLICAS / CERVEZAS / DESTILADOS ---
    if cat == "bebidas":
        # Fernet & Aperitivos
        if "FERNET" in u or "BRANCA" in u or "BUHERO" in u or "VITTONE" in u:
            return "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=800&auto=format&fit=crop&q=80"
        if "CAMPARI" in u or "APEROL" in u or "GANCIA" in u or "BITTER" in u:
            return "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&auto=format&fit=crop&q=80"
        if "CARPANO" in u or "CINZANO" in u or "MARTINI" in u or "VERMOUTH" in u:
            return "https://images.unsplash.com/photo-1527061011665-3652c757a4d4?w=800&auto=format&fit=crop&q=80"
        if "BAILEYS" in u or "COGNAC" in u or "LICOR" in u or "HESPERIDINA" in u or "ANIS" in u:
            return "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=800&auto=format&fit=crop&q=80"
        
        # Gin
        if subcat == "gin" or "GIN" in u or "TANQUERAY" in u or "HEREDERO" in u or "GINGKO" in u:
            return "https://images.unsplash.com/photo-1527061011665-3652c757a4d4?w=800&auto=format&fit=crop&q=80"
        
        # Vodka
        if subcat == "vodka" or "VODKA" in u or "ABSOLUT" in u or "SKYY" in u or "SERNOVA" in u or "SMIRNOFF" in u:
            if any(flv in u for flv in ["MANGO", "PEACH", "PEARS", "RASPBERRY", "WILDBERRI", "APRICOT", "COSMIC", "JUNGLE", "PINEAPPLE", "ICE POP", "WILD BERRIES"]):
                return "https://images.unsplash.com/photo-1563227812-0ea4c22e6cc8?w=800&auto=format&fit=crop&q=80"
            return "https://images.unsplash.com/photo-1560512823-829485b8bf24?w=800&auto=format&fit=crop&q=80"
        
        # Whisky
        if subcat == "whisky" or "WHISKY" in u or "WHISKEY" in u or "JACK DANIEL" in u or "JAMESON" in u or "JAMENSO" in u or "CRIADORES" in u:
            return "https://images.unsplash.com/photo-1527281400683-1aae777175f8?w=800&auto=format&fit=crop&q=80"
        
        # Ron
        if "RON" in u or "HAVANA" in u or "BACARDI" in u or "MALIBU" in u:
            return "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=800&auto=format&fit=crop&q=80"
        
        # Cervezas
        if "CORONA" in u or "STELLA" in u or "HEINEKEN" in u or "BOTELLA" in u:
            return "https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=800&auto=format&fit=crop&q=80"
        if "IPA" in u or "ANDES" in u or "PATAGONIA" in u:
            return "https://images.unsplash.com/photo-1567696911980-2eed69a46042?w=800&auto=format&fit=crop&q=80"
        if "LATA" in u or "LATON" in u or "BRAHMA" in u or "BUDWEISER" in u or "SCHNEIDER" in u or "QUILMES" in u:
            return "https://images.unsplash.com/photo-1584225064785-c62a8b43d148?w=800&auto=format&fit=crop&q=80"
        
        return "https://images.unsplash.com/photo-1608270586620-248524c67de9?w=800&auto=format&fit=crop&q=80"

    # --- SIN ALCOHOL ---
    if cat == "sin-alcohol":
        if "COCA" in u or "COLA" in u:
            return "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=800&auto=format&fit=crop&q=80"
        if "SPRITE" in u or "7UP" in u or "LIMA" in u:
            return "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=800&auto=format&fit=crop&q=80"
        if "FANTA" in u or "POMELO" in u or "CITRUS" in u or "PASO DE LOS TOROS" in u or "TALCA" in u or "MANZANA" in u or "NARANJA" in u:
            return "https://images.unsplash.com/photo-1624517452488-04869289c4ca?w=800&auto=format&fit=crop&q=80"
        if "SCHWEPPES" in u or "TONICA" in u or "TÓNICA" in u:
            return "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=800&auto=format&fit=crop&q=80"
        if "MONSTER" in u or "RED BULL" in u or "ROCKSTAR" in u or "SPEED" in u or "ENERGIZANTE" in u:
            return "https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=800&auto=format&fit=crop&q=80"
        if "TERMA" in u:
            return "https://images.unsplash.com/photo-1546171753-97d7676e4602?w=800&auto=format&fit=crop&q=80"
        if "ADES" in u or "BAGGIO" in u or "CEPITA" in u or "JUGO" in u:
            return "https://images.unsplash.com/photo-1613478223719-2ab802602423?w=800&auto=format&fit=crop&q=80"
        if "AGUA" in u or "SODA" in u or "VIDA" in u or "VILLAVICENCIO" in u or "BONAFONT" in u:
            return "https://images.unsplash.com/photo-1548839140-29a749e1bc4e?w=800&auto=format&fit=crop&q=80"
        if "0.0" in u or "SIN ALCOHOL" in u:
            return "https://images.unsplash.com/photo-1518176258769-f227c798150e?w=800&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=800&auto=format&fit=crop&q=80"

    # --- SNACKS, COMBOS & VARIOS ---
    if cat == "snacks":
        if "COMBO" in u or "COMBOS" in r:
            return "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=800&auto=format&fit=crop&q=80"
        if "ALFAJOR" in u or "CHOCOLATE" in u or "CHUPETIN" in u or "DULCE" in u or "CONFITES" in u or "CARAMELOS" in u:
            return "https://images.unsplash.com/photo-1548907040-4baa42d10919?w=800&auto=format&fit=crop&q=80"
        if "CAFE" in u or "CAFÉ" in u or "CAPSULA" in u:
            return "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800&auto=format&fit=crop&q=80"
        if "HIELO" in u:
            return "https://images.unsplash.com/photo-1548839140-29a749e1bc4e?w=800&auto=format&fit=crop&q=80"
        if "TABACO" in u or "CIGARRO" in u or "BLUNT" in u or "ENCENDEDOR" in u or "SEDAS" in u or "FILTROS" in u or "OCB" in u:
            return "https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=800&auto=format&fit=crop&q=80"
        if "LEÑA" in u or "CARBÓN" in u:
            return "https://images.unsplash.com/photo-1542838132-92c53300491e?w=800&auto=format&fit=crop&q=80"
        if "PAPA" in u or "SNACK" in u or "ACEITUNA" in u or "MANI" in u or "MANÍ" in u or "NACHO" in u:
            return "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=800&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=800&auto=format&fit=crop&q=80"

    return "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800&auto=format&fit=crop&q=80"

def extract_volume(desc):
    match = re.search(r'(\d+[\.,]?\d*)\s*(ML|LTS|L|LT|CC|GRS|GR|KG)', str(desc), re.IGNORECASE)
    if match:
        val, unit = match.groups()
        unit = unit.upper()
        if unit in ["L", "LTS", "LT"]:
            return f"{val} L"
        elif unit in ["ML", "CC"]:
            return f"{val} ml"
        elif unit in ["GR", "GRS"]:
            return f"{val} g"
        elif unit == "KG":
            return f"{val} kg"
    return "750 ml"

def convert_excel_to_products():
    excel_path = "inventario.xlsx"
    if not os.path.exists(excel_path):
        print(f"Error: No se encontró {excel_path}")
        return

    df = pd.read_excel(excel_path)

    # Cargar datos existentes si los hay para enriquecer descripciones específicas
    existing_by_code = {}
    existing_by_name = {}
    
    js_path = "data/products.js"
    if os.path.exists(js_path):
        with open(js_path, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'const PRODUCTS_DATA = (\[.*\]);', content, re.DOTALL)
            if match:
                try:
                    existing_list = json.loads(match.group(1))
                    for item in existing_list:
                        c = str(item.get("code", "")).strip().lstrip("0")
                        if c:
                            existing_by_code[c] = item
                        n = str(item.get("name", "")).strip().lower()
                        if n:
                            existing_by_name[n] = item
                except Exception as e:
                    print(f"Nota: {e}")

    products = []

    for idx, row in df.iterrows():
        raw_code = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else str(idx + 1)
        raw_desc = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else "Producto"
        raw_rubro = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else "VARIOS"
        
        # Columna I: Precio venta
        raw_price = row.iloc[8] if pd.notna(row.iloc[8]) else 0
        try:
            price = float(raw_price)
            if price.is_integer():
                price = int(price)
        except:
            price = 0

        # Columna H: Precio costo
        raw_cost = row.iloc[7] if pd.notna(row.iloc[7]) else 0
        try:
            cost = float(raw_cost)
            if cost.is_integer():
                cost = int(cost)
        except:
            cost = 0.0

        # Columna G: Stock actual
        raw_stock = row.iloc[6] if pd.notna(row.iloc[6]) else 0
        try:
            stock = int(raw_stock)
        except:
            stock = 0

        # Columna F: Stock mínimo
        raw_stock_min = row.iloc[5] if pd.notna(row.iloc[5]) else 0
        stock_min = str(raw_stock_min)

        clean_code_num = raw_code.lstrip("0")
        code_formatted = raw_code.zfill(3) if raw_code.isdigit() else raw_code
        item_id = f"prod-{code_formatted.lower().replace(' ', '-')}"

        name = clean_title(raw_desc)
        cat, subcat = get_category_and_subcategory(raw_rubro, raw_desc)
        vol = extract_volume(raw_desc)
        img = get_product_image(cat, subcat, raw_rubro, raw_desc)

        existing = existing_by_code.get(clean_code_num) or existing_by_name.get(name.lower()) or existing_by_name.get(raw_desc.lower())

        badge = None
        if stock <= 0:
            badge = "Sin Stock"
        elif "COMBO" in raw_rubro or "combo" in name.lower():
            badge = "Promo"
        elif stock <= 2:
            badge = "Últimas unidades"

        if existing:
            product = {
                "id": existing.get("id", item_id),
                "code": code_formatted,
                "name": name,
                "category": cat,
                "subcategory": subcat,
                "rubro": raw_rubro,
                "price": price,
                "oldPrice": existing.get("oldPrice", None),
                "cost": cost,
                "stock": stock,
                "stockMin": stock_min,
                "volume": vol if vol != "750 ml" else existing.get("volume", "750 ml"),
                "alcohol": existing.get("alcohol", "0.0%" if cat == "sin-alcohol" else "Graduación estándar"),
                "origin": existing.get("origin", "Línea Oficial"),
                "rating": existing.get("rating", 4.8),
                "badge": badge,
                "image": img,
                "description": existing.get("description", f"{name} disponible para entrega inmediata en Paisana Bebidas."),
                "pairing": existing.get("pairing", "Ideal para acompañar tus mejores momentos y reuniones.")
            }
        else:
            product = {
                "id": item_id,
                "code": code_formatted,
                "name": name,
                "category": cat,
                "subcategory": subcat,
                "rubro": raw_rubro,
                "price": price,
                "oldPrice": None,
                "cost": cost,
                "stock": stock,
                "stockMin": stock_min,
                "volume": vol,
                "alcohol": "0.0%" if cat == "sin-alcohol" else "Graduación estándar",
                "origin": "Línea Oficial",
                "rating": 4.8,
                "badge": badge,
                "image": img,
                "description": f"{name} de alta calidad, listo para disfrutar en Paisana Bebidas.",
                "pairing": "Ideal para compartir en reuniones y eventos."
            }

        products.append(product)

    # Guardar en data/products.js
    os.makedirs("data", exist_ok=True)
    js_output = "// Catálogo oficial de productos para Paisana Bebidas (Sincronizado con inventario.xlsx)\n"
    js_output += "const PRODUCTS_DATA = " + json.dumps(products, indent=2, ensure_ascii=False) + ";\n"

    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_output)

    print(f"¡Sincronización exitosa! Se integraron {len(products)} productos con imágenes conceptuales en {js_path}")

if __name__ == "__main__":
    convert_excel_to_products()
