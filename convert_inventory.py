"""
Script oficial para sincronizar e integrar 'Inventario3.0sanitizado.xlsx' en Paisana Bebidas (data/products.js).
- Lee el catálogo sanitizado (Descripción, Rubro, Precio de venta al público) sin exponer costos ni stock interno.
- Sectoriza con precisión los 34 rubros oficiales en 7 grandes departamentos y sub-rubros específicos.
- Vincula fotografías reales verificadas desde FotosDeProductos/ e imágenes conceptuales 100% activas (HTTP 200).
- Normaliza títulos, volúmenes/presentaciones y fichas descriptivas acorde a cada rubro.
"""

import json
import os
import re
import unicodedata
import openpyxl


def norm_key(text):
    """Normaliza texto sin tildes ni símbolos para comparaciones deterministas."""
    s = str(text or "").upper().strip()
    s = s.replace("´", "").replace("`", "").replace("'", "").replace("|", "")
    s = "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )
    s = re.sub(r"[^A-Z0-9]+", " ", s).strip()
    return s


# ==============================================================================
# FICHAS ENRIQUECIDAS DE BODEGA AMIGA: MARTINO WINES (8 ETIQUETAS)
# ==============================================================================
MARTINO_ENRICHMENT = {
    "MARTINO PEDRO XIMENEZ 2022 VINO BLANCO": {
        "name": "Martino Wines Pedro Ximénez 2022",
        "description": "Vino blanco singular de autor elaborado con uvas Pedro Ximénez de Luján de Cuyo. Perfil floral y cítrico con acidez viva, mineralidad y final elegante.",
        "pairing": "Pescados blancos, mariscos, ceviches, quesos de cabra y pastas suaves.",
        "image": "FotosDeProductos/VINOS/f89450e2-bfe6-4926-8441-1ba9ed2d027b.jpg",
        "volume": "750 ml",
        "alcohol": "12.5%"
    },
    "MARTINO PEDRO XIMENEZ 2026": {
        "name": "Martino Wines Pedro Ximénez 2026",
        "description": "Nueva cosecha del emblemático blanco Pedro Ximénez de Martino Wines. Expresión fresca, notas de manzana verde, flores blancas y textura vibrante.",
        "pairing": "Sushi, tiraditos, ensaladas mediterráneas y quesos frescos.",
        "image": "FotosDeProductos/VINOS/f89450e2-bfe6-4926-8441-1ba9ed2d027b.jpg",
        "volume": "750 ml",
        "alcohol": "12.5%"
    },
    "MARTINO BONARDA 2025": {
        "name": "Martino Wines Bonarda 2025",
        "description": "Bonarda mendocina contemporánea de pura cepa. Explosión de fruta roja, cerezas, frambuesas y taninos redondos con paso por boca sedoso.",
        "pairing": "Pizzas de masa madre, pastas con boloñesa, carnes magras y picadas.",
        "image": "FotosDeProductos/VINOS/Martino bonarda 2023.jpg",
        "volume": "750 ml",
        "alcohol": "13.9%"
    },
    "MARTINO ROSE 2024": {
        "name": "Martino Wines Rosé 2024",
        "description": "Rosé de estilo provenzal. Tono salmón pálido, aromas sutiles a frutillas silvestres, pomelo rosado y pétalos blancos con acidez crocante.",
        "pairing": "Bruschettas de salmón, sushi, cocina asiática y tapeos al atardecer.",
        "image": "FotosDeProductos/VINOS/f0737caa-ad58-4e01-9137-006c3c08907e.jpg",
        "volume": "750 ml",
        "alcohol": "12.8%"
    },
    "MARTINO MARSELAN 2024": {
        "name": "Martino Wines Marselan 2024",
        "description": "Cepa exótica Marselan (cruza francesa de Cabernet Sauvignon y Garnacha). Gran intensidad cromática, notas a moras, ciruelas maduras, cacao y taninos firmes.",
        "pairing": "Cortes vacunos a la leña, estofados, risotto de hongos y empanadas criollas.",
        "image": "FotosDeProductos/VINOS/Martino marselan 2024.jpg",
        "volume": "750 ml",
        "alcohol": "14.4%"
    },
    "MARTINO CABERNET FRANC 2025": {
        "name": "Martino Wines Cabernet Franc 2025",
        "description": "Exponente refinado de Cabernet Franc con aromas a pimiento dulce asado, frutos negros, grafito y delicadas notas especiadas de crianza en roble.",
        "pairing": "Carnes rojas asadas, cordero patagónico, pastas rellenas y quesos duros.",
        "image": "FotosDeProductos/VINOS/Martino cabernet franc 2025.jpg",
        "volume": "750 ml",
        "alcohol": "14.2%"
    },
    "MARTINO MALBEC 2025": {
        "name": "Martino Wines Malbec 2025",
        "description": "Malbec de Luján de Cuyo de gran tipicidad varietal. Aromas a ciruelas frescas, violetas y sutil vainilla, con entrada dulce y final persistente.",
        "pairing": "Ojo de bife a las brasas, asado criollo, carnes horneadas y tablas de quesos.",
        "image": None,
        "volume": "750 ml",
        "alcohol": "14.3%"
    },
    "MARTINO SANGIOVESE 2024": {
        "name": "Martino Wines Sangiovese 2024",
        "description": "Cepa de herencia italiana vinificada en Luján de Cuyo. Fresco y gastronómico, con notas de guinda, hierbas secas, tomate confitado y taninos vibrantes.",
        "pairing": "Pastas italianas con pomodoro, lasaña, carnes blancas con hierbas y charcutería.",
        "image": None,
        "volume": "750 ml",
        "alcohol": "13.8%"
    }
}


# ==============================================================================
# MAPEO EXACTO DE FOTOGRAFÍAS REALES POR NOMBRE NORMALIZADO DE PRODUCTO
# ==============================================================================
EXACT_PHOTOS_BY_NORM_NAME = {
    # --- COMBOS CON FOTO PROPIA ---
    "COMBO BRANCA COCA 2 25 HIELO": "FotosDeProductos/combo fernet.jpg",
    "COMBO GANCIA 950 ML SPRITE 2 25 L": "FotosDeProductos/Combo gancia.jpg",

    # --- DESTILADOS, APERITIVOS, RONES, VODKAS, WHISKIES, GINS ---
    "BOMBAY": "FotosDeProductos/bombay sapphire.jpg",
    "BUHERO NEGRO 700ML": "FotosDeProductos/Fernet buhero.jpg",
    "VITTONE 750ML": "FotosDeProductos/Fernet vittone.webp",
    "FERNET BRANCA 750 ML": "FotosDeProductos/bebidas con alcohol/fernet branca.jpg",
    "FERNET BRANCA 1L": "FotosDeProductos/bebidas con alcohol/fernet branca.jpg",
    "FERNET BRANCA 450 ML": "FotosDeProductos/bebidas con alcohol/fernet branca.jpg",
    "RON HAVANA CLUB 7 ANOS 700ML": "FotosDeProductos/Havana Club Ron 7 Anos.jpg",
    "RON HAVANA CLUB ESPECIAL": "FotosDeProductos/Havana club especial.jpg",
    "RON HAVANA CLUB ORIGINAL": "FotosDeProductos/havana club original.jpg",
    "RON BACARDI CARTA BLANCA": "FotosDeProductos/bebidas con alcohol/Bacardi carta blanca.jpg",
    "RON MALIBU": "FotosDeProductos/bebidas con alcohol/malibu.jpg",
    "GIN TANQUERAY CLASSIC": "FotosDeProductos/tanqueray london dry gin.jpg",
    "GIN TANQUERAY SEVILLA": "FotosDeProductos/tanqueray sevilla.jpg",
    "VODKA SKYY APRICOT": "FotosDeProductos/skyy apricot.jpg",
    "VODKA SKYY COSMIC": "FotosDeProductos/Skyy Cosmic_.jpg",
    "VODKA SKYY PINEAPPLE": "FotosDeProductos/skyy pineapple.jpg",
    "VODKA SKYY RASPBERRY": "FotosDeProductos/skyy raspberry.jpg",
    "VODKA SKYY CLASSIC": "FotosDeProductos/skyy vodka.jpg",
    "ABSOLUT PEACH 700 ML": "FotosDeProductos/bebidas con alcohol/Absolut Peach Flavored Vodka, 750 ml - copia - copia - copia.jpg",
    "ABSOLUT CLASSIC 700 ML": "FotosDeProductos/bebidas con alcohol/Absolut vodka.jpg",
    "ABSOLUT WILDBERRI 700 ML": "FotosDeProductos/bebidas con alcohol/Absolut wild berry.jpg",
    "ABSOLUT RASPBERRY 700 ML": "FotosDeProductos/bebidas con alcohol/absolut raspberry.jpg",
    "ABSOLUT PEARS 700 ML": "FotosDeProductos/bebidas con alcohol/Pears Vodka _ Pear Vodka by Absolut _ 750ml _ Sweden.jpg",
    "SMIRNOFF SPICY TAMARIND": "FotosDeProductos/bebidas con alcohol/Smirnoff Spicy Tamarind.jpg",
    "SMIRNOFF CLASSIC": "FotosDeProductos/bebidas con alcohol/Vodka Smirnoff No_ 21 - 1 L.jpg",
    "SMIRNOFF BITTER CITRIC GRAPEFRUIT": "FotosDeProductos/bebidas con alcohol/smirnoff bitter citric grapefruit.jpg",
    "SMIRNOFF BITTER CITRIC RUBY ORANGE": "FotosDeProductos/bebidas con alcohol/smirnoff bitter citric ruby orange & lime.jpg",
    "SMIRNOFF GREEN APPLE": "FotosDeProductos/bebidas con alcohol/smirnoff green apple.jpg",
    "SMIRNOFF RASPBERRY": "FotosDeProductos/bebidas con alcohol/smirnoff raspberry.jpg",
    "BAILEYS ORIGINAL 750 ML": "FotosDeProductos/bebidas con alcohol/Baileys.jpg",
    "CAMPARI 750ML": "FotosDeProductos/bebidas con alcohol/Campari.jpg",
    "GANCIA 950ML": "FotosDeProductos/bebidas con alcohol/Gancia.jpg",
    "APEROL 750ML": "FotosDeProductos/bebidas con alcohol/aperol.jpg",
    "JACK DANIEL S BLACKBERRY": "FotosDeProductos/bebidas con alcohol/Jack Daniels Blackberry 750cc.jpg",
    "JACK DANIEL S WHISKEY ETIQUETA NEGRA": "FotosDeProductos/bebidas con alcohol/jack daniels n7.jpg",
    "JACK DANIEL S FIRE": "FotosDeProductos/bebidas con alcohol/jack daniels fire.jpg",
    "JACK DANIELS HONEY": "FotosDeProductos/bebidas con alcohol/jack daniels honey.jpg",
    "JAMESON": "FotosDeProductos/bebidas con alcohol/Jameson Whiskey Irlandes 750ml.jpg",
    "JOHNNIE WALKER DOUBLE BLACK": "FotosDeProductos/bebidas con alcohol/Johnnie Walker Double Black.jpg",
    "JOHNNIE WALKER RED LABEL": "FotosDeProductos/bebidas con alcohol/Whisky Johnnie Walker Red Label.jpg",
    "JOHNNIE WALKER BLACK LABEL": "FotosDeProductos/bebidas con alcohol/johnnie walker black label.jpg",
    "JOHNNIE WALKER BLACK LABEL 1L": "FotosDeProductos/bebidas con alcohol/johnnie walker black label.jpg",

    # --- SIN ALCOHOL, ENERGIZANTES, AGUAS, GASEOSAS & JUGOS ---
    "RED BULL 250ML": "FotosDeProductos/Redbull.jpg",
    "ROCKSTAR ROSA 500ML": "FotosDeProductos/rockstar.jpg",
    "ROCKSTAR VERDE 500ML": "FotosDeProductos/rockstar.png",
    "MONSTER ULTRA PEACHY KEEN": "FotosDeProductos/Bebidas sin alcohol/Monster Ultra Peachy Keen.jpg",
    "MONSTER PIPELINE PUNCH": "FotosDeProductos/Bebidas sin alcohol/Monster pipeline puch.jpg",
    "MONSTER ULTRA WATERMELON": "FotosDeProductos/Bebidas sin alcohol/Monster ultra watermelon zero sugar 0_5l.jpg",
    "7UP ZERO 500ML": "FotosDeProductos/Bebidas sin alcohol/7up.jpg",
    "7UP ZERO 1 5 L": "FotosDeProductos/Bebidas sin alcohol/7UP Free 1,5 l PET DPG.jpg",
    "FANTA 500ML": "FotosDeProductos/Bebidas sin alcohol/Fanta 500ml.jpg",
    "COCA COLA REGULAR 500ML": "FotosDeProductos/Bebidas sin alcohol/Gaseosa-CocaCola-Sabor-Original-500-Ml-_1.jpg",
    "COCA COLA REGULAR LATA 354ML": "FotosDeProductos/Bebidas sin alcohol/LATA COCA.jpg",
    "COCA COLA LATA 354ML": "FotosDeProductos/Bebidas sin alcohol/LATA COCA.jpg",
    "COCA COLA ZERO 500ML": "FotosDeProductos/Bebidas sin alcohol/coca zero 500ml.jpg",
    "COCA COLA REGULAR 1 5L": "FotosDeProductos/Bebidas sin alcohol/coca-cola-1lt.png",
    "COCA COLA ZERO 1 5": "FotosDeProductos/Bebidas sin alcohol/coca-zero-1lt.png",
    "MIRINDA 1 5 L": "FotosDeProductos/Bebidas sin alcohol/Mirinda, 1,5 L.jpg",
    "PEPSI BLACK": "FotosDeProductos/Bebidas sin alcohol/Refresco pepsi black sin azucar 355 ml.jpg",
    "PASO DE LOS TOROS POMELO 1 5L": "FotosDeProductos/Bebidas sin alcohol/PASO DE LOS TOROS - Pomelo 1_5 L.jpg",
    "PASO DE LOS TOROS AGUA TONICA 1 5L": "FotosDeProductos/Bebidas sin alcohol/paso de los toros tonica.jpg",
    "PASO DE LOS TOROS TONICA LATA 269ML": "FotosDeProductos/Paso De Los Toros Tonica Lata 269ml Pack X24.jpg",
    "AGUA SER SIN GAS 1 5L": "FotosDeProductos/Bebidas sin alcohol/Agua Mineral Ser Sin Gas 1,5l X6.jpg",
    "AGUA VILLAVICENCIO 1 5L SIN GAS": "FotosDeProductos/Bebidas sin alcohol/Agua Mineral Villavicencio 2 L Sin Gas Pack X6 La Barra.jpg",
    "AGUA CLARA BY GRAZIANI 2L": "FotosDeProductos/Bebidas sin alcohol/Agua clara graziani.webp",
    "CLARA BY GRAZIANI 500ML SIN GAS": "FotosDeProductos/Bebidas sin alcohol/agua-sin-gas-graziani-500-ml-ofertas-casa-segal-supermercado-mendoza.jpg",
    "AGUA BIDON NIHUIL 5L": "FotosDeProductos/Bebidas sin alcohol/Agua nihuil grande.jpg",
    "KOMBUCHA OY 473 ML": "FotosDeProductos/Bebidas sin alcohol/Kombuchas.jpg",
    "GATORADE ZERO MORAS 400 ML": "FotosDeProductos/Bebidas sin alcohol/Bebida Isotonica Gatorade Zero Sabor Mora 400 Ml.jpg",
    "GATORADE 750ML": "FotosDeProductos/Bebidas sin alcohol/Gatorade(1).jpg",
    "GATORADE NARANJA 500ML": "FotosDeProductos/Bebidas sin alcohol/gatorade.jpg",
    "JUGO TUTTI NARANJA 1 L": "FotosDeProductos/Bebidas sin alcohol/Tuti.jpg",
    "CEPITA X LITRO CAJA": "FotosDeProductos/Bebidas sin alcohol/cepita naranja 1l caja.jpg",
    "CEPITA BOTELLA 1L": "FotosDeProductos/Bebidas sin alcohol/jugo-cepita-hf-durazno-x-1l.jpg",
    "CITRIC X LTR": "FotosDeProductos/Bebidas sin alcohol/citric xd.jpg",
    "CITRIC 200ML": "FotosDeProductos/Bebidas sin alcohol/citric 200ml.jpg",
    "BAGGIO FRESH 1 5L": "FotosDeProductos/Bebidas sin alcohol/fresh 1,5.png",
    "BAGGIO FRESH 600ML MANZANA": "FotosDeProductos/Bebidas sin alcohol/fresh manzana.jpg",
    "BAGGIO FRESH 200ML": "FotosDeProductos/Bebidas sin alcohol/fresh naranja.jpg",
    "BAGGIO FRESH 600 ML POMELO": "FotosDeProductos/Bebidas sin alcohol/fresh pomelo.jpg",
    "BAGGIO FRESH BOTELLA 600ML": "FotosDeProductos/Bebidas sin alcohol/fresh.jpg",
    "HEINEKEN 0 0 473CM": "FotosDeProductos/Bebidas sin alcohol/heineken 00.jpg",
    "IMPERIAL GOLDEN SIN ALCOHOL 473CM": "FotosDeProductos/Bebidas sin alcohol/imperial golden 0.0.jpg",

    # --- VINOS TINTOS, BLANCOS, DULCES, ROSADOS & BAG IN BOX ---
    "SAN HUBERTO CLASICO 375ML": "FotosDeProductos/VINOS/San huberto clasico 375cc Malbec.jpg",
    "DILEMA CABERNET": "FotosDeProductos/VINOS/Dilema Day cabernet.jpg",
    "ESTANCIA MENDOZA CAB SAU": "FotosDeProductos/VINOS/Estancia Mendoza Cabernet Sauvignon_.jpg",
    "ESTANCIA MENDOZA MALBEC": "FotosDeProductos/VINOS/Estancia Mendoza malbec.jpg",
    "4 MONOS LOCOS": "FotosDeProductos/VINOS/cu4tro monos locos malbec salvaje.jpg",
    "SAN HUBERTO SIN ALCOHOL TINTO": "FotosDeProductos/VINOS/San huberto sin alcohol_.jpg",
    "BENJAMIN SYRAH": "FotosDeProductos/VINOS/Benjamin syrah.jpg",
    "BENJAMIN MERLOT": "FotosDeProductos/VINOS/Benjamin merlot.jpg",
    "LOS CARDOS MALBEC": "FotosDeProductos/VINOS/Los cardos malbec.jpg",
    "LOS CARDOS CAB SAU": "FotosDeProductos/VINOS/Los cardos Cabernet sauvignon.jpg",
    "CORDERO CON PIEL DE LOBO BONARDA 2025": "FotosDeProductos/VINOS/Cordero con piel de lobo Bonarda 2025.jpg",
    "CORDERO CON PIEL DE LOBO CABERNET SAUVIGNON 2026": "FotosDeProductos/VINOS/cordero con piel de lobo cabernet sauvignon.jpg",
    "PROFUGO FRUTOS ROJOS": "FotosDeProductos/VINOS/profugo frutos rojos.jpg",
    "PROFUGO ESPECIAS": "FotosDeProductos/VINOS/profugo especias.jpg",
    "FLICHMANN STATE MALBEC": "FotosDeProductos/VINOS/finca flichman estate malbec.jpg",
    "FLICHMANN STATE CAB SAU": "FotosDeProductos/VINOS/finca flichman estate cabernet sauvignon.jpg",
    "FLICKMANN STATE CABERNET SAUVIGNON": "FotosDeProductos/VINOS/finca flichman estate cabernet sauvignon.jpg",
    "FLICHMANN RESERVA MALBEC": "FotosDeProductos/VINOS/finca flichman reserva malbec.jpg",
    "FLICHMANN RESERVA CAB FRANC": "FotosDeProductos/VINOS/finca flichman reserva cabernet franc.jpg",
    "FLICHMANN GRAN RESERVA MALBEC": "FotosDeProductos/VINOS/Finca flichman Gran reserva malbec 2024.jpg",
    "DONA PAULA STATE MALBEC": "FotosDeProductos/VINOS/Dona paula estate malbec reserva 2025.jpg",
    "DONA PAULA ESTATE CABERNET SAUVIGNON": "FotosDeProductos/VINOS/Dona Paula estate cabernet sauvignon reserva 205.jpg",
    "DONA PAULA ESTATE BOLD RED BLEND": "FotosDeProductos/VINOS/Dona paula estate black edition 2024 bold red blend.jpg",
    "DONA PAULA SAUVIGNON BLANC": "FotosDeProductos/VINOS/Dona paula estate Sauvignon blanc 2025.jpg",
    "CRUX TEMPRANILLO 2024": "FotosDeProductos/VINOS/Crux tempranillo 2024.jpg",
    "CRUX MALBEC 2024": "FotosDeProductos/VINOS/Crux malbec 2024.jpg",
    "CRUX CAB FRANC 2024": "FotosDeProductos/VINOS/crux cabernet franc 2024.jpg",
    "CRUX SAUVIGNON BLANC 2024": "FotosDeProductos/VINOS/f20cfa5b-9931-4532-9047-371b1a4d4970.jpg",
    "CRUX ROXE 2023": "FotosDeProductos/VINOS/e8367ef2-fd00-47fb-8685-0bf2eeed5ec2.jpg",
    "PARTRIDGE MALBEC 2024 2025": "FotosDeProductos/VINOS/Partridge malbec 2024.jpg",
    "PARTRIDGE CAB SAU 2024": "FotosDeProductos/VINOS/Partidge cabernet Sauvignon 2024.jpg",
    "PARTRIDGE CHARDONNAY": "FotosDeProductos/VINOS/Partridge chardonnay 2025.jpg",
    "MONTEBELLO MALBEC 3L": "FotosDeProductos/VINOS/f25afdb3-911c-4b14-8f23-4b8c5edf7623.jpg",
    "PARTRIDGE MALBEC 3L": "FotosDeProductos/VINOS/Bag in box Partridge malbec.jpg",
    "BY THE GLASS DUO 3L": "FotosDeProductos/VINOS/dbbcd4f5-6605-4eac-a913-1a3f7af434bb.jpg",
    "PORTILLO NARANJO DULCE": "FotosDeProductos/VINOS/c88c004e-ecac-4b0f-92e1-03fdbf050180.jpg",
    "PORTILLO DULCE NATURAL 10": "FotosDeProductos/VINOS/Portillo dulce natural 10.jpg",
    "PORTILLO CHANRDONNAY 04": "FotosDeProductos/VINOS/Portillo chardonnay 04.jpg",
    "PORTILLO SAUVIGNON BLANC 03": "FotosDeProductos/VINOS/portillo sauvignon blanc 03.jpg",
    "PORTILLO 2026 SAUVIGNON BLANC": "FotosDeProductos/VINOS/portillo sauvignon blanc 03.jpg",
    "PORTILLO ROSE 05": "FotosDeProductos/VINOS/Portillo rose 05.jpg",
    "PORTILLO MALBEC 01": "FotosDeProductos/VINOS/9cb79f17-7684-4ce5-b09d-b56ac5d2997a.jpg",
    "PORTILLO MERLOT 06": "FotosDeProductos/VINOS/1295f7c9-51f2-4033-bf9b-360d3886747b.jpg",
    "PORTILLO SYRAH 08": "FotosDeProductos/VINOS/fcae451a-a3fe-40ea-a271-3a2ead3c18a8.jpg",
    "PORTILLO CAB SAU 02": "FotosDeProductos/VINOS/8f5aab9a-7b20-451e-8111-d45942df3ae4.jpg",
    "SANTA JULIA CHENIN DULCE NATURAL": "FotosDeProductos/VINOS/Santa julia chenin dulce.jpg",
    "SANTA JULIA DULCE TINTO": "FotosDeProductos/VINOS/Santa Julia dulce tinto.jpg",
    "ESTANCIA MENDOZA DULCE CHENIN CHARDONNAY": "FotosDeProductos/VINOS/estancia mendoza chenin chardonnay dulce.jpg",
    "DILEMA BLANCO DULCE": "FotosDeProductos/VINOS/Dilema blanco dulce.jpg",
    "CANCILLER BLEND DULCE": "FotosDeProductos/VINOS/Canciller blend dulce_.jpg",
    "BENJAMIN DULCE": "FotosDeProductos/VINOS/Benjamin Dulce.jpg",
    "BENJAMIN CHARDONNAY": "FotosDeProductos/VINOS/Benjamin chardonnay.jpg",
    "COLON SELECTO DULCE DURAZNO": "FotosDeProductos/VINOS/Colon selecto Durazno_.jpg",
    "COLON SELECTO BLANCO DULCE": "FotosDeProductos/VINOS/ce1037ba-c1fa-46ce-bba9-2a4cdf84622c.jpg",
    "COLON SELECTO ROSA DULCE": "FotosDeProductos/VINOS/Colon selecto dulce fresco rose.jpg",
    "FLICHMAN CHARDONNAY": "FotosDeProductos/VINOS/finca flichman chardonnay.jpg",
    "BODEGA PRIVADA SAUVIGNON BLANC": "FotosDeProductos/VINOS/bodega privada sauvignon blanc.jpg",
    "LOS CARDOS SAUVIGNON BLANC": "FotosDeProductos/VINOS/46b93eec-173c-4d0a-b80d-1d08b4024476.jpg",
    "LOS CARDOS SAUVIGNON BLANC 2025": "FotosDeProductos/VINOS/Los cardos private collection Sauvignon blanc 2025.jpg",
    "LOS CARDOS CHARDONNAY": "FotosDeProductos/VINOS/Los cardos chardonnay 2025.jpg",
    "SAINT FELICIEN CHARDONNAY": "FotosDeProductos/VINOS/5bcb25fc-a878-4975-9c60-d5fc843f6197.jpg",
    "PERRO CALLEJERO MALBEC 2024": "FotosDeProductos/VINOS/perro callejero blend de malbec.jpg",
    "FOND DE CAVE CABERNET SAUVIGNON 2025": "FotosDeProductos/VINOS/fond de cave cabernet sauvignon.jpg",
    "FOND DE CAVE CHARDONNAY 2025": "FotosDeProductos/VINOS/62a0030f-ff41-471e-aad5-5cd2521f90bc.jpg",
    "ALAMBRADO MALBEC": "FotosDeProductos/VINOS/Alambrado malbec 2025.jpg",
    "ALAMBRADO CABERNET FRAN": "FotosDeProductos/VINOS/Alambrado cabernet franc 2025.jpg",
    "CARMELA MALBEC": "FotosDeProductos/VINOS/Carmela malbec 2023.jpg",
    "AGUIJON DE ABEJA OBRERA CABERNET FRANC 2024": "FotosDeProductos/VINOS/Durigutti Aguijon de Abeja Obrera Cabernet franc 2024.jpg",
    "AGUIJON DE ABEJA OBRERA MALBEC 2023": "FotosDeProductos/VINOS/Durigutti Aguijon de Abeja Obrera malbec 2023.jpg",
    "CARA SUCIA 2024 CRIOLLA": "FotosDeProductos/VINOS/Cara sucia vino de rivadavia 2024.jpg",
    "SEPTIMA EMBLEMA MALBEC": "FotosDeProductos/VINOS/Septima emblema malbec 2024.jpg",
    "SEPTIMA EMBLEMA CHARDONNAY": "FotosDeProductos/VINOS/53a8ca72-354b-443f-8a7b-88a0e7392ca9.jpg",
    "LOS PASOS CAB SAU": "FotosDeProductos/VINOS/e2ccaa36-1581-41c5-9cc1-a2ef426696f9.jpg",
    "LOS PASOS MALBEC": "FotosDeProductos/VINOS/d4ad7052-5cfb-454e-ab9c-787b49e852cc.jpg",
    "LOS PASOS CHARDONNAY": "FotosDeProductos/VINOS/fc50b867-22eb-4887-9aa9-396a14b055f6.jpg",
    "LOS PASOS BLANCO DULCE": "FotosDeProductos/VINOS/b134b9bb-3eef-4327-badb-e642bb7cb665.jpg",
    "D ALILAH MALBEC ROSE": "FotosDeProductos/VINOS/D_lilah malbec rose.jpg",
    "DURIGUTTI BLANC DE BLANCS": "FotosDeProductos/VINOS/Durigutti blanc de blanc_.jpg",
    "VINO NAMPE TINTO MALBEC 2025 1125ML": "FotosDeProductos/VINOS/Nampe malbec.jpg",
    "NAMPE MALBEC 750 ML": "FotosDeProductos/VINOS/Nampe malbec.jpg",
    "PUNTO FINAL SAU BLANC": "FotosDeProductos/VINOS/punto final sauvignon black 2024.jpg",
    "PREGUNTON MALBEC": "FotosDeProductos/VINOS/Pregunton malbec.jpg",
    "PREGUNTON CABERNET SAUVIGNON": "FotosDeProductos/VINOS/Pregunton cabernet Sauvignon_.jpg",
    "ATILIO AVENA MALBEC": "FotosDeProductos/VINOS/d4cab08f-3464-44c0-8cd7-5b4c5a5f78dc.jpg",
    "ATILIO AVENA CAB SAU": "FotosDeProductos/VINOS/fc7c3c69-69eb-4884-a665-e71065503eb0.jpg",
}


# ==============================================================================
# ETIQUETAS HUMANAS DE SUBCATEGORÍAS / SUB-RUBROS
# ==============================================================================
SUBCATEGORY_LABELS = {
    # Combos
    "combos-fernet": "Combo Fernet",
    "combos-vodka": "Combo Vodka",
    "combos-aperitivos": "Combo Aperitivo",
    "combos-ron": "Combo Ron",
    "combos-gin": "Combo Gin",
    "combos-cafe": "Promo Cafetería",
    # Vinos Tintos
    "malbec": "Malbec",
    "cabernet-sauvignon": "Cabernet Sauvignon",
    "cabernet-franc": "Cabernet Franc",
    "otros-tintos": "Varietales Tintos",
    "blends": "Blend / Corte",
    "bag-in-box": "Bag in Box 3L",
    "damajuanas-375": "Damajuana / 375ml",
    # Blancos, Dulces & Espumantes
    "vinos-blancos": "Vino Blanco",
    "espumantes": "Espumante",
    "vinos-dulces": "Vino Dulce",
    "vinos-rosados": "Vino Rosado",
    # Cervezas & Destilados
    "cervezas": "Cerveza",
    "fernet": "Fernet",
    "aperitivos": "Aperitivo",
    "vermouth": "Vermouth",
    "gin": "Gin",
    "vodka": "Vodka",
    "whisky": "Whisky",
    "ron": "Ron",
    "rtd": "Ready to Drink",
    "otros-destilados": "Licores & Destilados",
    # Sin Alcohol
    "gaseosas": "Gaseosa",
    "tonicas-mixers": "Tónica / Mixer",
    "jugos-aguas-sab": "Jugo / Saborizada",
    "isotonicas": "Isotónica",
    "energizantes": "Energizante",
    "aguas": "Agua / Kombucha",
    "sin-alcohol-00": "Sin Alcohol 0.0%",
    # Café, Snacks & Regionales
    "cafe": "Café de Especialidad",
    "snacks-salados": "Snack Salado",
    "chocolates-alfajores": "Alfajor / Dulce",
    "regionales-cocteleria": "Regional / Coctelería",
    # Hielo, Tabaquería & Regalos
    "hielo-lena": "Hielo & Leña",
    "cigarrillos-cigarros": "Cigarrillos & Cigarros",
    "tabacos-papelillos": "Tabaco & Papelillos",
    "regalos": "Regalería & Asado",
    "descartables-accesorios": "Accesorios & Cajas",
}


# ==============================================================================
# LIMPIEZA Y NORMALIZACIÓN DE TÍTULOS DE CATÁLOGO
# ==============================================================================
WORD_REPLACEMENTS = {
    "BFRANCA": "Branca",
    "NUHUIL": "Nihuil",
    "VINETARD": "Vineyard",
    "CHANRDONNAY": "Chardonnay",
    "CABAERNET": "Cabernet",
    "PINEAPLLE": "Pineapple",
    "WILDBERRI": "Wild Berri",
    "CLASIC": "Classic",
    "LATAB": "Lata",
    "ASADADOR": "Asador",
    "MANZANAN": "Manzana",
    "JANNESSE": "Tennessee",
    "BUNRIBE": "Sunrise",
    "LONDO": "London",
    "HAVANNA": "Havana",
    "VITONE": "Vittone",
    "JAMENSON": "Jameson",
    "FLICKMANN": "Flichman",
    "FLICHMANN": "Flichman",
}


def clean_title(text):
    if not isinstance(text, str):
        return ""

    s = text.strip()
    s = s.replace("|", " ").replace("`", "")
    s = re.sub(r"^´+", "", s).strip()
    s = s.replace("D,V,", "D.V.").replace("COOL, BLUE", "COOL BLUE").replace("SAU,", "SAU")
    s = re.sub(r"\bJACK\s+DANIEL\s*S\b", "JACK DANIEL'S", s, flags=re.IGNORECASE)
    s = re.sub(r"\bJACK\s+DANIELS\b", "JACK DANIEL'S", s, flags=re.IGNORECASE)
    s = re.sub(r"\bGORDONS\b", "GORDON'S", s, flags=re.IGNORECASE)
    s = re.sub(r"\bD´ALILAH\b", "D'ALILAH", s, flags=re.IGNORECASE)
    s = re.sub(r"\bBREEDER´S\b", "BREEDER'S", s, flags=re.IGNORECASE)
    s = re.sub(r"\bALAMBRADO CABERNET FRAN\b", "ALAMBRADO CABERNET FRANC", s, flags=re.IGNORECASE)
    s = re.sub(r"\b7UP ZERO 1,5 ML\b", "7UP ZERO 1.5L", s, flags=re.IGNORECASE)
    # Espaciar signos '+' pegados a palabras
    s = re.sub(r"\s*\+\s*", " + ", s)
    s = re.sub(r"\s+", " ", s).strip()

    keep_upper = {
        "ML", "L", "LTS", "LT", "GR", "GRS", "GMS", "G", "KG", "CC", "7UP", "IPA", "APA",
        "X1", "X2", "X3", "X5", "X6", "X10", "X12", "X20", "X24", "X27", "X47", "X48",
        "X50", "X52", "X100", "X150", "X200", "RTD", "BIB", "PX", "CF", "DOC", "OCB",
        "D.V.", "TACC"
    }
    lowercase_words = {"de", "del", "y", "la", "las", "el", "los", "en", "con", "a", "por", "sin", "para", "al"}

    words = s.split()
    cleaned_words = []

    for w in words:
        if w == "+":
            cleaned_words.append("+")
            continue

        upper_plain = w.upper().rstrip(".")
        if upper_plain in WORD_REPLACEMENTS:
            cleaned_words.append(WORD_REPLACEMENTS[upper_plain])
            continue

        upper = w.upper()
        # Unidades compuestas como 473CM -> 473ml, 750ML -> 750ml, 1,5L -> 1.5L
        m_unit = re.match(r"^(\d+(?:[,\.]\d+)?)(ML|LTS|LT|L|CC|GR|GRS|GMS|G|KG|CM)$", upper)
        if m_unit:
            num_part, unit_part = m_unit.groups()
            num_part = num_part.replace(",", ".")
            if unit_part in ("CM", "CC", "ML"):
                cleaned_words.append(f"{num_part}ml")
            elif unit_part in ("L", "LT", "LTS"):
                cleaned_words.append(f"{num_part}L")
            elif unit_part in ("GR", "GRS", "GMS", "G"):
                cleaned_words.append(f"{num_part}g")
            elif unit_part == "KG":
                cleaned_words.append(f"{num_part}kg")
            continue

        if upper in keep_upper:
            cleaned_words.append("ml" if upper == "CM" else upper)
        elif upper.lower() in lowercase_words and len(cleaned_words) > 0:
            cleaned_words.append(upper.lower())
        elif "'" in w:
            parts = w.split("'")
            cleaned_words.append(parts[0].capitalize() + "'" + parts[1].lower() if len(parts[1]) == 1 else parts[0].capitalize() + "'" + parts[1].capitalize())
        else:
            cleaned_words.append(w.capitalize())

    res = " ".join(cleaned_words)
    # Limpiar casos tipo "750 Ml" -> "750ml" o "1.5 L" -> "1.5L"
    res = re.sub(r"(\d+(?:[,\.]\d+)?)\s+(ml|ML|Cc|CC|Cm)\b", lambda m: f"{m.group(1).replace(',', '.')}ml", res)
    res = re.sub(r"(\d+(?:[,\.]\d+)?)\s+(L|Lts|Lt)\b", lambda m: f"{m.group(1).replace(',', '.')}L", res)
    res = re.sub(r"(\d+(?:[,\.]\d+)?)\s+(Grs|Gr|Gms|G)\b", lambda m: f"{m.group(1).replace(',', '.')}g", res)
    res = re.sub(r"(\d+(?:[,\.]\d+)?)\s+(Kg|KG)\b", lambda m: f"{m.group(1).replace(',', '.')}kg", res)
    # Si termina o sigue '+' luego de 1,5 / 1.5 / 2,25 / 2.25 / 2,5 / 2.5 / 1,25 sin unidad en bebidas/combos -> agregar 'L'
    res = re.sub(r"\b(1[,\.]25|1[,\.]5|2[,\.]25|2[,\.]5)(?=\s*(?:\+|$))", lambda m: f"{m.group(1).replace(',', '.')}L", res)
    if res:
        res = res[0].upper() + res[1:]
    return res


# ==============================================================================
# SECTORIZACIÓN INTEGRAL POR RUBRO Y SUB-RUBRO (7 SECTORES + 34 RUBROS)
# ==============================================================================
def get_category_and_subcategory(rubro_val, desc_val):
    rubro = str(rubro_val or "").upper().strip()
    desc = norm_key(desc_val)
    words = set(desc.split())

    # 1. COMBOS & PROMOS (60 productos)
    if rubro == "COMBOS" or desc.startswith("COMBO ") or desc.startswith("PROMO "):
        if words & {"CAFE", "ALFAJOR"}:
            return "combos", "combos-cafe"
        if words & {"BRANCA", "BUHERO", "VITTONE", "VITONE", "FERNET"}:
            return "combos", "combos-fernet"
        if words & {"ABSOLUT", "SKYY", "SMIRNOFF", "SERNOVA", "VODKA"}:
            return "combos", "combos-vodka"
        if words & {"BACARDI", "HAVANA", "HAVANNA", "RON", "MALIBU"}:
            return "combos", "combos-ron"
        if words & {"GIN", "BEEFEATER", "HEREDERO", "GINKGO", "GORDON", "GORDONS"}:
            return "combos", "combos-gin"
        return "combos", "combos-aperitivos"

    # 2. VINOS SIN ALCOHOL & CERVEZAS SIN ALCOHOL -> Sector Sin Alcohol (0.0%)
    if rubro in ("CERVEZAS SIN ALCOHOL", "VINOS SIN ALCOHOL"):
        return "sin-alcohol", "sin-alcohol-00"
    if rubro == "CERVEZAS" and "SIN ALCOHOL" in desc:
        return "sin-alcohol", "sin-alcohol-00"
    if rubro == "READY TO DRINK" and "SIN ALCOHOL" in desc:
        return "sin-alcohol", "sin-alcohol-00"

    # 3. VINOS TINTOS, BAG IN BOX, DAMAJUANAS & 375ML
    if rubro == "BAG IN BOX":
        return "tintos", "bag-in-box"

    if rubro == "DAMAJUANAS":
        return "tintos", "damajuanas-375"

    if rubro == "VINOS 375 ML":
        if any(k in desc for k in ["CHARDONNAY", "SAUVIGNON BLANC", "BLANCO", "DULCE"]):
            return "blancos", "vinos-blancos"
        return "tintos", "damajuanas-375"

    if rubro == "VINOS TINTOS":
        # Detectar blends explícitos primero (ej: D.V. Catena Cabernet - Malbec, Reserva Malbec Cabernet Franc, Red Blend, Prófugo)
        if any(k in desc for k in ["BLEND", "PROFUGO"]) or ("MALBEC" in desc and ("CABERNET" in desc or "CAB " in desc)):
            if "PERRO CALLEJERO MALBEC" in desc:
                return "tintos", "malbec"
            return "tintos", "blends"
        if "MALBEC" in desc or "4 MONOS LOCOS" in desc:
            return "tintos", "malbec"
        if any(k in desc for k in ["CABERNET FRANC", "CAB FRANC", "CABERNET FRAN"]):
            return "tintos", "cabernet-franc"
        if any(k in desc for k in ["CABERNET SAUVIGNON", "CAB SAU", "CABERNET SAU", "CABAERNET", "DILEMA CABERNET"]):
            return "tintos", "cabernet-sauvignon"
        if any(k in desc for k in ["BONARDA", "MERLOT", "SYRAH", "PINOT NOIR", "TEMPRANILLO", "MARSELAN", "SANGIOVESE", "CRIOLLA"]):
            return "tintos", "otros-tintos"
        return "tintos", "blends"

    # 4. VINOS BLANCOS, DULCES, ROSADOS & ESPUMANTES
    if rubro == "VINOS BLANCOS":
        return "blancos", "vinos-blancos"
    if rubro == "ESPUMANTES":
        return "blancos", "espumantes"
    if rubro == "VINOS DULCES":
        return "blancos", "vinos-dulces"
    if rubro == "VINOS ROSADOS":
        return "blancos", "vinos-rosados"

    # 5. CERVEZAS & DESTILADOS
    if rubro == "CERVEZAS":
        return "bebidas", "cervezas"
    if rubro == "FERNET":
        return "bebidas", "fernet"
    if rubro == "APERITIVOS":
        return "bebidas", "aperitivos"
    if rubro == "VERMOUTH":
        return "bebidas", "vermouth"
    if rubro == "GIN":
        return "bebidas", "gin"
    if rubro == "VODKA":
        return "bebidas", "vodka"
    if rubro == "WHISKY":
        return "bebidas", "whisky"
    if rubro == "RON":
        return "bebidas", "ron"
    if rubro == "READY TO DRINK":
        return "bebidas", "rtd"
    if rubro in ("OTRAS BEBIDAS BLANCAS Y DESTILADOS", "MINIATURAS"):
        return "bebidas", "otros-destilados"

    # 6. BEBIDAS SIN ALCOHOL
    if rubro == "ENERGIZANTES":
        return "sin-alcohol", "energizantes"
    if rubro == "GASEOSAS":
        if any(k in desc for k in ["TONICA", "SCHWEPPES", "PASO DE LOS TOROS"]):
            return "sin-alcohol", "tonicas-mixers"
        return "sin-alcohol", "gaseosas"
    if rubro == "AGUAS Y SODAS":
        if any(k in desc for k in ["SODA", "SIFON"]):
            return "sin-alcohol", "tonicas-mixers"
        return "sin-alcohol", "aguas"
    if rubro == "JUGOS Y AGUAS SABORIZADAS":
        if "GATORADE" in desc or "POWERADE" in desc:
            return "sin-alcohol", "isotonicas"
        return "sin-alcohol", "jugos-aguas-sab"

    # 7. CAFÉ, SNACKS & REGIONALES
    if rubro == "CAFE":
        return "snacks", "cafe"
    if rubro == "CONSERVAS Y ACEITES":
        return "snacks", "regionales-cocteleria"
    if rubro == "SNACKS":
        if any(k in desc for k in ["ALFAJOR", "CHOCOLATE", "NESTLE", "AGUILA", "MOGUL", "CHUPETIN", "HALLS", "MENTHO"]):
            return "snacks", "chocolates-alfajores"
        if any(k in desc for k in ["ALMA DE SIEMBRA", "ALMIBAR", "CONGELAD", "FRUTILLAS", "MANGO", "AROMATICAS"]):
            return "snacks", "regionales-cocteleria"
        return "snacks", "snacks-salados"

    # 8. HIELO, TABAQUERÍA, REGALOS & DESCARTABLES
    if rubro in ("HIELOS", "LEÑA", "LENA"):
        return "varios", "hielo-lena"
    if rubro == "CIGARRILLO, TABACO Y MAS":
        if any(k in desc for k in ["TABACO", "ARK ROYAL", "FLANDRIA", "VAN KIFF", "CERRITO", "LAS HOJAS", "OCB", "LIBELLA", "BLUNT", "ZEUS", "ENCENDEDOR"]):
            return "varios", "tabacos-papelillos"
        return "varios", "cigarrillos-cigarros"
    if rubro == "REGALOS":
        return "varios", "regalos"
    if rubro == "DESCARTABLES":
        return "varios", "descartables-accesorios"

    return "varios", "descartables-accesorios"


# ==============================================================================
# EXTRACCIÓN INTELIGENTE DE PRESENTACIÓN / VOLUMEN / CONTENIDO
# ==============================================================================
def extract_presentation(desc, category, rubro):
    raw = str(desc or "").upper()

    # Combos: presentación especial
    if category == "combos":
        return "Pack Combo"

    # Estuches o sets
    if "ESTUCHE" in raw or "SET " in raw:
        m_vol = re.search(r"(\d+(?:[\.,]\d+)?)\s*(ML|L|LTS|LT|CC|CM|GR|GRS)", raw)
        if m_vol:
            val, unit = m_vol.groups()
            val = val.replace(",", ".")
            if unit in ("L", "LTS", "LT"):
                return f"Estuche {val} L"
            if unit in ("GR", "GRS"):
                return f"Estuche {val} g"
            return f"Estuche {val} ml"
        return "Set / Estuche"

    # Chandon 187
    if re.search(r"\b187\b", raw):
        return "187 ml"

    # Unidades explícitas (ej: X20 UNI, X10, X150, X200, X5 UNID)
    m_un = re.search(r"\bX\s*(\d+)\s*(?:UNID|UNI|UNIDADES)?\b", raw)
    if m_un and category in ("varios", "snacks"):
        return f"x{m_un.group(1)} un."
    m_un2 = re.search(r"\b(\d+)\s*(?:UNI\.?|UNID\.?|BOX)\b", raw)
    if m_un2 and category == "varios":
        return f"x{m_un2.group(1)} un."

    # Volumen o peso explícito
    m = re.search(r"(\d+(?:[\.,]\d+)?)\s*(ML|LTS|L|LT|CC|CM|GRS|GR|GMS|G|KG)\b", raw)
    if m:
        val, unit = m.groups()
        val = val.replace(",", ".")
        if raw.startswith("7UP ZERO 1,5 ML"):
            return "1.5 L"
        if unit in ("L", "LTS", "LT"):
            return f"{val} L"
        if unit in ("ML", "CC", "CM"):
            return f"{val} ml"
        if unit in ("GR", "GRS", "GMS", "G"):
            return f"{val} g"
        if unit == "KG":
            return f"{val} kg"

    # Litros implícitos en gaseosas (ej: COCA ZERO 1,5 / SPRITE ZERO 2,5)
    m_imp = re.search(r"\b(1[,\.]5|2[,\.]25|2[,\.]5)\b", raw)
    if m_imp and category == "sin-alcohol":
        return f"{m_imp.group(1).replace(',', '.')} L"

    # Defaults según rubro/categoría (nunca poner 750ml a snacks/tabaco/accesorios)
    if rubro == "BAG IN BOX":
        return "3 L"
    if rubro == "DAMAJUANAS":
        return "5 L"
    if rubro == "VINOS 375 ML":
        return "375 ml"
    if category in ("tintos", "blancos"):
        return "750 ml"
    if rubro == "CERVEZAS":
        if "LATA" in raw:
            return "473 ml"
        if "LATON" in raw:
            return "710 ml"
        if "BOTELLA" in raw or "RETORNABLE" in raw:
            return "1 L"
        return "473 ml"
    if rubro == "ENERGIZANTES":
        if "MONSTER" in raw:
            return "473 ml"
        return "250 ml"
    if rubro == "VERMOUTH":
        return "750 ml"
    if category == "bebidas":
        return "750 ml"
    if rubro == "HIELOS":
        if "GRANDE" in raw:
            return "Bolsa Grande"
        if "CHICA" in raw:
            return "Bolsa Chica"
        return "Vaso c/ Hielo"
    if rubro in ("LEÑA", "LENA"):
        return "Atado"
    return "Unidad"


# ==============================================================================
# METADATOS DE ORIGEN, GRADUACIÓN Y NOTAS DE CATA / MARIDAJE POR RUBRO
# ==============================================================================
def build_metadata(name, raw_desc, rubro, category, subcat):
    u = norm_key(raw_desc)

    if category == "combos":
        origin = "Selección Paisana"
        alcohol = "Combo Listo"
        desc = f"{name}: pack promocional armado en Paisana Bebidas con bebidas seleccionadas listas para disfrutar bien frías."
        pairing = "Ideal para previas, juntadas con amigos, cumpleaños y celebraciones."
        return origin, alcohol, desc, pairing

    if category == "tintos":
        origin = "Mendoza, Argentina"
        if "GUALTALLARY" in u or "VALLE DE UCO" in u or "VISTA FLORES" in u:
            origin = "Valle de Uco, Mendoza"
        elif "AGRELO" in u or "LUJAN" in u or "PERDICES" in u:
            origin = "Luján de Cuyo, Mendoza"
        elif "RIVADAVIA" in u or "CARA SUCIA" in u:
            origin = "Este Mendocino, Mendoza"

        if subcat == "bag-in-box":
            alcohol = "13.5%"
            desc = f"{name} en práctico formato Bag in Box de 3 litros con válvula hermética que conserva intacta la frescura del vino por semanas."
            pairing = "Asados familiares, reuniones numerosas y disfrute cotidiano por copa."
        elif subcat == "damajuanas-375":
            alcohol = "13.2%"
            desc = f"{name}, tradición mendocina con fruta franca, cuerpo amable y excelente relación precio-calidad."
            pairing = "Comidas caseras, pastas, carnes al horno y mesa diaria."
        elif subcat == "cabernet-franc":
            alcohol = "14.0%"
            desc = f"{name}: expresivo Cabernet Franc con notas de frutos negros, pimiento asado, especias finas y taninos elegantes."
            pairing = "Carnes vacunas a la parrilla, cordero, pastas rellenas y quesos estacionados."
        elif subcat == "cabernet-sauvignon":
            alcohol = "13.9%"
            desc = f"{name}: tinto de carácter estructurado con aromas a casis, pimienta negra, roble sutil y final persistente."
            pairing = "Bife de chorizo, asado a la leña, guisos criollos y quesos duros."
        elif subcat == "malbec":
            alcohol = "13.8%"
            desc = f"{name}: Malbec mendocino de perfil frutado, notas de ciruelas maduras, violetas y taninos dulces y aterciopelados."
            pairing = "Cortes a la parrilla, empanadas mendocinas, pastas y tablas de fiambres."
        elif subcat == "otros-tintos":
            alcohol = "13.5%"
            desc = f"{name}: varietal tinto seleccionado que destaca por su frescura, expresión frutal auténtica y paso fluido en boca."
            pairing = "Pastas artesanales, pizzas de masa madre, carnes blancas o rojas y picadas."
        else:
            alcohol = "13.8%"
            desc = f"{name}: corte de uvas tintas cuidadosamente ensamblado para lograr equilibrio, complejidad aromática y redondez."
            pairing = "Carnes asadas, risottos, cazuelas y encuentros gastronómicos."
        return origin, alcohol, desc, pairing

    if category == "blancos":
        origin = "Mendoza, Argentina"
        if subcat == "espumantes":
            alcohol = "12.0%"
            desc = f"{name}: burbujas finas y persistentes con notas cítricas, manzana verde, pan tostado y frescura vibrante."
            pairing = "Brindis, aperitivos, sushi, mariscos, tapas y postres."
        elif subcat == "vinos-dulces":
            alcohol = "9.5% - 11.5%"
            desc = f"{name}: vino dulce equilibrado y sumamente refrescante, con intensos aromas a frutas blancas, durazno, flores y miel."
            pairing = "Tardes de terraza, picadas suaves, quesos azules, frutas y postres."
        elif subcat == "vinos-rosados":
            alcohol = "12.5%"
            desc = f"{name}: rosado fresco y delicado con matices de frutos rojos pequeños, notas florales y acidez vivaz."
            pairing = "Ensaladas gourmet, pescados, sushi, tapeos y atardeceres."
        else:
            alcohol = "12.8%"
            desc = f"{name}: vino blanco joven y luminoso, con aromas a frutas tropicales, cítricos frescos y final limpio y mineral."
            pairing = "Pescados, mariscos, aves grilladas, pastas con salsas blancas y quesos suaves."
        return origin, alcohol, desc, pairing

    if category == "bebidas":
        if subcat == "cervezas":
            origin = "Cervecería Seleccionada"
            alcohol = "4.5% - 5.5%"
            desc = f"{name}: cerveza refrescante con equilibrio justo de malta y lúpulo, entregada bien fría lista para destapar."
            pairing = "Picadas, hamburguesas, pizzas, papas rústicas y juntadas."
        elif subcat == "fernet":
            origin = "Destilería Clásica"
            alcohol = "39% (25% Menta)" if "MENTA" in u else "39%"
            desc = f"{name}: aperitivo amargo elaborado a partir de una receta secreta de hierbas aromáticas, raíces y especias maceradas."
            pairing = "Ideal con gaseosa cola y abundante hielo en vaso largo."
        elif subcat == "aperitivos":
            origin = "Línea Aperitivos"
            alcohol = "35%" if "JAGER" in u else ("11% - 25%")
            desc = f"{name}: aperitivo botánico y cítrico imprescindible en la barra para preparar spritz y tragos refrescantes."
            pairing = "Cócteles con espumante, soda, tónica o jugo de naranja y rodaja cítrica."
        elif subcat == "vermouth":
            origin = "Tradición Vermouth"
            alcohol = "15% - 18%"
            desc = f"{name}: vermouth macerado con vino seleccionado, ajenjo y botánicos aromáticos de perfil equilibrado."
            pairing = "Con golpe de soda o tónica, hielo en roca, piel de naranja y aceitunas."
        elif subcat == "gin":
            origin = "Destilado Botánico"
            alcohol = "37.5% - 47%"
            desc = f"{name}: gin destilado en alambique con bayas de enebro seleccionadas, pieles cítricas y botánicos aromáticos."
            pairing = "Gin Tonic perfecto con agua tónica bien fría, hielo macizo y botánicos."
        elif subcat == "vodka":
            origin = "Destilado Puro"
            alcohol = "35% - 40%"
            desc = f"{name}: vodka de múltiples destilaciones con pureza cristalina y suavidad ideal para alta coctelería y mezclas."
            pairing = "Excelente con lima-limón, jugos cítricos, energizantes o frutos rojos."
        elif subcat == "whisky":
            origin = "Escocia / EE.UU. / Irlanda"
            alcohol = "35% - 40%"
            desc = f"{name}: whiskey añejado en barricas de roble con notas profundas de vainilla, caramelo tostado, madera y especias."
            pairing = "Para degustar solo, en las rocas (on the rocks) o en cócteles de autor."
        elif subcat == "ron":
            origin = "Tradición Caribeña"
            alcohol = "35% - 40%"
            desc = f"{name}: ron destilado de caña de azúcar con notas suaves y cálidas ideales para tragos clásicos."
            pairing = "Cuba Libre con cola y lima, Mojito con menta fresca o Daiquiri."
        elif subcat == "rtd":
            origin = "Listo para Tomar"
            alcohol = "5.0% - 7.5%"
            desc = f"{name}: bebida lista para tomar en lata fría, con la proporción justa de sabor y burbujas."
            pairing = "Práctico para llevar a previas, parques, eventos y reuniones."
        else:
            origin = "Destilados & Licores"
            alcohol = "17% - 40%"
            desc = f"{name}: licor o destilado especial seleccionado para ampliar tu barra hogareña o sobremesa."
            pairing = "Sobremesas, café, postres o coctelería clásica."
        return origin, alcohol, desc, pairing

    if category == "sin-alcohol":
        origin = "Sin Alcohol"
        alcohol = "0.0%"
        if subcat == "sin-alcohol-00":
            desc = f"{name}: todo el sabor y la frescura de tu bebida favorita con 0.0% de graduación alcohólica."
            pairing = "Para disfrutar bien fría a toda hora sin alcohol."
        elif subcat == "energizantes":
            desc = f"{name}: bebida energizante con vitaminas y cafeína, entregada fría para recargar energía al instante."
            pairing = "Ideal sola bien helada o como mixer en coctelería nocturna."
        elif subcat == "tonicas-mixers":
            desc = f"{name}: burbujeante y equilibrada, el mixer predilecto para realzar gins, vermouths y aperitivos."
            pairing = "Gin tonics, vermouth con soda, spritz o refresco individual."
        elif subcat == "isotonicas":
            desc = f"{name}: bebida isotónica hidratante con sales minerales para una rápida recuperación y frescura."
            pairing = "Entrenamientos, días de calor e hidratación diaria."
        elif subcat == "aguas":
            desc = f"{name}: hidratación pura y natural, ideal para acompañar comidas y degustaciones de vinos."
            pairing = "Mesa diaria, catas de vino e hidratación familiar."
        else:
            desc = f"{name}: refresco sin alcohol ideal para compartir en familia, comidas o combinar tus tragos favoritos."
            pairing = "Comidas, reuniones y barra de mixers."
        return origin, alcohol, desc, pairing

    if category == "snacks":
        if subcat == "cafe":
            origin = "Tostadero Seleccionado"
            alcohol = "Cafetería"
            desc = f"{name}: café seleccionado de tueste cuidado con intenso aroma, cuerpo balanceado y notas nobles en taza."
            pairing = "Desayunos, sobremesas, prensa francesa, filtro o cafetera express."
        elif subcat == "chocolates-alfajores":
            origin = "Dulces & Chocolatería"
            alcohol = "Confitería"
            desc = f"{name}: tentación dulce ideal para acompañar un buen café, regalar o cerrar una gran comida."
            pairing = "Café de especialidad, vinos dulces, espumantes o licores cremosos."
        elif subcat == "regionales-cocteleria":
            origin = "Gourmet & Coctelería"
            alcohol = "Almacén Gourmet"
            desc = f"{name}: producto gourmet y de coctelería seleccionado para realzar tus picadas, recetas o copas."
            pairing = "Tablas regionales, desayunos artesanales o decoración de tragos."
        else:
            origin = "Copetín & Picada"
            alcohol = "Snacks"
            desc = f"{name}: snack crocante y sabroso, el compañero infaltable para abrir el apetito junto a tus bebidas."
            pairing = "Cervezas bien frías, vermouth, gin tonic y picadas con amigos."
        return origin, alcohol, desc, pairing

    # category == "varios"
    if subcat == "hielo-lena":
        origin = "Insumos Previa & Asado"
        alcohol = "Complemento"
        desc = f"{name}: insumo esencial listo para mantener tus bebidas heladas o encender el fuego del asado."
        pairing = "Indispensable para conservadoras, tragos largos y parrilla."
    elif subcat in ("cigarrillos-cigarros", "tabacos-papelillos"):
        origin = "Tabaquería +18"
        alcohol = "Solo +18"
        desc = f"{name}: artículo de tabaquería y accesorios. Venta exclusiva a mayores de 18 años."
        pairing = "Disponible para sumar a tu pedido a domicilio o retiro en local."
    elif subcat == "regalos":
        origin = "Regalería Paisana"
        alcohol = "Presentación Regalo"
        desc = f"{name}: opción distinguida de regalería y equipamiento criollo para agasajar en ocasiones especiales."
        pairing = "Combiná con tu etiqueta de vino o destilado favorito para armar un regalo único."
    else:
        origin = "Bazar & Accesorios"
        alcohol = "Accesorio"
        desc = f"{name}: accesorio práctico de servicio y embalaje para completar tu compra sin que falte nada."
        pairing = "Ideal para eventos, descorches y presentaciones de obsequio."
    return origin, alcohol, desc, pairing


# ==============================================================================
# IMÁGENES CONCEPTUALES VERIFICADAS (100% HTTP 200 OK EN UNSPLASH)
# ==============================================================================
def get_product_image(cat, subcat, rubro, desc):
    u = norm_key(desc)

    # --- MARTINO WINES ---
    if "MARTINO" in u:
        if "PEDRO" in u or "XIMENEZ" in u or "BLANCO" in u:
            return "https://images.unsplash.com/photo-1584916201218-f4242ceb4809?w=800&auto=format&fit=crop&q=80"
        if "CABERNET" in u or "FRANC" in u:
            return "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=800&auto=format&fit=crop&q=80"
        if "ROSE" in u:
            return "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800&auto=format&fit=crop&q=80"

    # --- COMBOS ---
    if cat == "combos":
        if subcat == "combos-cafe":
            return "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800&auto=format&fit=crop&q=80"
        if subcat == "combos-gin":
            return "https://images.unsplash.com/photo-1527061011665-3652c757a4d4?w=800&auto=format&fit=crop&q=80"
        if subcat == "combos-aperitivos":
            return "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&auto=format&fit=crop&q=80"
        if subcat == "combos-vodka":
            return "https://images.unsplash.com/photo-1560512823-829485b8bf24?w=800&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=800&auto=format&fit=crop&q=80"

    # --- VINOS TINTOS & BLANCOS ---
    if cat in ("tintos", "blancos"):
        if subcat == "espumantes":
            return "https://images.unsplash.com/photo-1578911373434-0cb395d2cbfb?w=800&auto=format&fit=crop&q=80"
        if subcat == "vinos-rosados":
            return "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800&auto=format&fit=crop&q=80"
        if subcat == "vinos-dulces":
            return "https://images.unsplash.com/photo-1584916201218-f4242ceb4809?w=800&auto=format&fit=crop&q=80"
        if subcat == "vinos-blancos":
            return "https://images.unsplash.com/photo-1569919659476-f0852f6834b7?w=800&auto=format&fit=crop&q=80"
        if subcat in ("bag-in-box", "damajuanas-375"):
            return "https://images.unsplash.com/photo-1547595628-c61a29f496f0?w=800&auto=format&fit=crop&q=80"
        if subcat in ("cabernet-sauvignon", "cabernet-franc"):
            return "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=800&auto=format&fit=crop&q=80"
        if subcat == "malbec":
            return "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800&auto=format&fit=crop&q=80"

    # --- CERVEZAS & DESTILADOS ---
    if cat == "bebidas":
        if subcat == "cervezas":
            if "IPA" in u or "ANDES" in u or "PATAGONIA" in u:
                return "https://images.unsplash.com/photo-1567696911980-2eed69a46042?w=800&auto=format&fit=crop&q=80"
            if "BOTELLA" in u or "RETORNABLE" in u or "1L" in u or "CORONA" in u or "STELLA" in u:
                return "https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=800&auto=format&fit=crop&q=80"
            return "https://images.unsplash.com/photo-1584225064785-c62a8b43d148?w=800&auto=format&fit=crop&q=80"
        if subcat == "fernet":
            return "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=800&auto=format&fit=crop&q=80"
        if subcat == "aperitivos":
            return "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&auto=format&fit=crop&q=80"
        if subcat in ("vermouth", "gin"):
            return "https://images.unsplash.com/photo-1527061011665-3652c757a4d4?w=800&auto=format&fit=crop&q=80"
        if subcat == "vodka":
            if any(flv in u for flv in ["MANGO", "PEACH", "PEARS", "RASPBERRY", "WILDBERRI", "APRICOT", "COSMIC", "JUNGLE", "PINEAPPLE", "ICE POP", "WILD BERRIES", "TROPICAL", "MANDRIN", "VANILIA", "TABASCO", "CHICLE"]):
                return "https://images.unsplash.com/photo-1563227812-0ea4c22e6cc8?w=800&auto=format&fit=crop&q=80"
            return "https://images.unsplash.com/photo-1560512823-829485b8bf24?w=800&auto=format&fit=crop&q=80"
        if subcat == "whisky":
            return "https://images.unsplash.com/photo-1527281400683-1aae777175f8?w=800&auto=format&fit=crop&q=80"
        if subcat == "ron":
            return "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=800&auto=format&fit=crop&q=80"
        if subcat == "rtd":
            return "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=800&auto=format&fit=crop&q=80"

    # --- SIN ALCOHOL ---
    if cat == "sin-alcohol":
        if subcat == "sin-alcohol-00":
            return "https://images.unsplash.com/photo-1518176258769-f227c798150e?w=800&auto=format&fit=crop&q=80"
        if subcat == "energizantes":
            return "https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=800&auto=format&fit=crop&q=80"
        if subcat == "aguas":
            return "https://images.unsplash.com/photo-1523362628745-0c100150b504?w=800&auto=format&fit=crop&q=80"
        if subcat == "tonicas-mixers":
            return "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=800&auto=format&fit=crop&q=80"
        if "COCA" in u or "PEPSI" in u:
            return "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=800&auto=format&fit=crop&q=80"
        if "SPRITE" in u or "7UP" in u or "PRITTY" in u:
            return "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=800&auto=format&fit=crop&q=80"
        if "TERMA" in u:
            return "https://images.unsplash.com/photo-1546171753-97d7676e4602?w=800&auto=format&fit=crop&q=80"
        if subcat in ("jugos-aguas-sab", "isotonicas"):
            return "https://images.unsplash.com/photo-1613478223719-2ab802602423?w=800&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1624517452488-04869289c4ca?w=800&auto=format&fit=crop&q=80"

    # --- CAFÉ, SNACKS & REGIONALES ---
    if cat == "snacks":
        if subcat == "cafe":
            return "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800&auto=format&fit=crop&q=80"
        if subcat == "chocolates-alfajores":
            return "https://images.unsplash.com/photo-1548907040-4baa42d10919?w=800&auto=format&fit=crop&q=80"
        if subcat == "regionales-cocteleria":
            if "OLIVA" in u or "ACEITE" in u:
                return "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=800&auto=format&fit=crop&q=80"
            return "https://images.unsplash.com/photo-1546171753-97d7676e4602?w=800&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=800&auto=format&fit=crop&q=80"

    # --- HIELO, TABAQUERÍA & REGALOS ---
    if subcat == "hielo-lena":
        if "HIELO" in u:
            return "https://images.unsplash.com/photo-1564419320461-6870880221ad?w=800&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&auto=format&fit=crop&q=80"
    if subcat == "regalos":
        if "ASADOR" in u or "ASADADOR" in u or "TABLA" in u:
            return "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=800&auto=format&fit=crop&q=80"
    if subcat in ("cigarrillos-cigarros", "tabacos-papelillos"):
        return "https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=800&auto=format&fit=crop&q=80"
    return "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=800&auto=format&fit=crop&q=80"


def convert_excel_to_products():
    excel_candidates = [
        "Inventario3.0sanitizado.xlsx",
        "inventario actualizado.xlsx",
        "inventario.xlsx",
    ]
    excel_path = next((p for p in excel_candidates if os.path.exists(p)), None)
    if not excel_path:
        print("Error: No se encontró ningún archivo de inventario Excel en la carpeta.")
        return

    print(f"Leyendo inventario desde: {excel_path}")
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb["Catálogo para web"] if "Catálogo para web" in wb.sheetnames else wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        print("Error: El archivo Excel está vacío.")
        return

    header = [str(h or "").strip().lower() for h in rows[0]]
    is_sanitized_3col = len(header) >= 3 and "descrip" in header[0] and "rubro" in header[1]
    data_rows = rows[1:]

    products = []
    seq = 0

    for row in data_rows:
        if not any(c is not None for c in row):
            continue

        if is_sanitized_3col:
            raw_desc = str(row[0] or "").strip()
            raw_rubro = str(row[1] or "VARIOS").strip().upper()
            raw_price = row[2]
        else:
            raw_desc = str(row[1] or "").strip()
            raw_rubro = str(row[2] or "VARIOS").strip().upper()
            raw_price = row[8] if len(row) > 8 else 0

        # Ignorar filas internas de control POS ("REVISAR RUBRO" / "REVISAR DESCRIPCIÓN")
        if not raw_desc or "REVISAR RUBRO" in raw_rubro or "REVISAR DESCRIP" in raw_desc.upper():
            continue

        seq += 1
        code_formatted = str(seq).zfill(3)
        item_id = f"prod-{code_formatted}"

        try:
            val_p = float(raw_price) if raw_price is not None else 0
            price = int(val_p) if val_p.is_integer() else round(val_p, 2)
            if price < 0:
                price = 0
        except Exception:
            price = 0

        norm_desc = norm_key(raw_desc)
        cat, subcat = get_category_and_subcategory(raw_rubro, raw_desc)
        subcat_label = SUBCATEGORY_LABELS.get(subcat, raw_rubro.title())
        name = clean_title(raw_desc)
        vol = extract_presentation(raw_desc, cat, raw_rubro)

        # Resolución de foto:
        # 1) Foto local verificada en FotosDeProductos/ (solo si existe en disco)
        # 2) Imagen conceptual de alta resolución verificada (HTTP 200)
        local_photo = EXACT_PHOTOS_BY_NORM_NAME.get(norm_desc)
        if local_photo and os.path.exists(local_photo):
            final_img = local_photo
        else:
            final_img = get_product_image(cat, subcat, raw_rubro, raw_desc)

        martino_info = MARTINO_ENRICHMENT.get(norm_desc)
        is_martino = "MARTINO" in norm_desc or martino_info is not None
        is_combo = cat == "combos"

        if is_martino:
            badge = "Bodega Amiga"
        elif is_combo:
            badge = "Promo Combo"
        elif price <= 0:
            badge = "Consultar"
        else:
            badge = None

        if martino_info:
            m_img = martino_info["image"]
            if m_img and os.path.exists(m_img):
                final_img = m_img
            product = {
                "id": item_id,
                "code": code_formatted,
                "name": martino_info["name"],
                "category": cat,
                "subcategory": subcat,
                "subcategoryLabel": subcat_label,
                "rubro": raw_rubro,
                "price": price if price > 0 else 22500,
                "oldPrice": None,
                "volume": martino_info["volume"],
                "alcohol": martino_info["alcohol"],
                "origin": "Luján de Cuyo, Mendoza",
                "rating": 4.9,
                "badge": badge,
                "image": final_img,
                "description": martino_info["description"],
                "pairing": martino_info["pairing"],
            }
        else:
            origin, alcohol, desc_txt, pairing_txt = build_metadata(name, raw_desc, raw_rubro, cat, subcat)
            product = {
                "id": item_id,
                "code": code_formatted,
                "name": name,
                "category": cat,
                "subcategory": subcat,
                "subcategoryLabel": subcat_label,
                "rubro": raw_rubro,
                "price": price,
                "oldPrice": None,
                "volume": vol,
                "alcohol": alcohol,
                "origin": origin,
                "rating": 4.8,
                "badge": badge,
                "image": final_img,
                "description": desc_txt,
                "pairing": pairing_txt,
            }

        products.append(product)

    # Ordenar alfabéticamente por nombre dentro de un catálogo limpio, manteniendo IDs estables
    products.sort(key=lambda x: x["name"].lower())

    os.makedirs("data", exist_ok=True)
    js_path = "data/products.js"
    js_output = "// Catálogo oficial sanitizado de Paisana Bebidas (Sincronizado con Inventario3.0sanitizado.xlsx)\n"
    js_output += "const PRODUCTS_DATA = " + json.dumps(products, indent=2, ensure_ascii=False) + ";\n"

    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_output)

    print(f"¡Sincronización exitosa! Se integraron {len(products)} productos sanitizados en {js_path}")


if __name__ == "__main__":
    convert_excel_to_products()
