"""
Script para sincronizar e integrar 'inventario actualizado.xlsx' en Paisana Bebidas (data/products.js)
Asigna categorización precisa por rubro/categoría, imágenes conceptuales de alta calidad y metadatos robustos.
"""

import openpyxl
import json
import re
import os

MARTINO_ENRICHMENT = {
    "372": {
        "name": "Martino Wines Pedro Ximénez 2022",
        "description": "Vino blanco singular elaborado con uvas Pedro Ximénez. Perfil floral y cítrico con acidez viva, mineralidad y un final largo y elegante.",
        "pairing": "Pescados blancos, mariscos, ceviches, quesos de cabra y pastas con salsas suaves.",
        "image": "FotosDeProductos/VINOS/f89450e2-bfe6-4926-8441-1ba9ed2d027b.jpg",
        "volume": "750 ml",
        "alcohol": "12.5%"
    },
    "373": {
        "name": "Martino Wines Bonarda 2025",
        "description": "Bonarda argentina de pura cepa. Explosión de fruta roja, cerezas, frambuesas y taninos redondos con un paso por boca sedoso y envolvente.",
        "pairing": "Pizzas de masa madre, pastas con salsa boloñesa, carnes magras y picadas de fiambres.",
        "image": "FotosDeProductos/VINOS/Martino bonarda 2023.jpg",
        "volume": "750 ml",
        "alcohol": "13.9%"
    },
    "374": {
        "name": "Martino Wines Rosé 2024",
        "description": "Rosé contemporáneo de estilo provenzal. Tono salmón pálido, aromas sutiles a frutillas silvestres, pomelo rosado y flores blancas. Acidez crocante y refrescante.",
        "pairing": "Sushi, ensaladas mediterráneas, bruschettas de salmón y tapeos al atardecer.",
        "image": "FotosDeProductos/VINOS/f0737caa-ad58-4e01-9137-006c3c08907e.jpg",
        "volume": "750 ml",
        "alcohol": "12.8%"
    },
    "375": {
        "name": "Martino Wines Marselan 2024",
        "description": "Varietal no tradicional Marselan (cruce de Cabernet Sauvignon y Garnacha). Gran intensidad cromática, notas a moras, ciruelas maduras, chocolate y taninos firmes.",
        "pairing": "Cortes vacunos a la leña, estofados de caza, risotto de hongos y empanadas criollas.",
        "image": "FotosDeProductos/VINOS/Martino marselan 2024.jpg",
        "volume": "750 ml",
        "alcohol": "14.4%"
    },
    "376": {
        "name": "Martino Wines Cabernet Franc 2025",
        "description": "Exponente refinado de Cabernet Franc con aromas a pimiento dulce asado, frutos negros, grafito y sutiles notas especiadas de roble francés.",
        "pairing": "Carnes rojas asadas, cordero patagónico, pastas rellenas y quesos maduros.",
        "image": "FotosDeProductos/VINOS/Martino cabernet franc 2025.jpg",
        "volume": "750 ml",
        "alcohol": "14.2%"
    }
}

# Mapeo exhaustivo de fotos reales desde FotosDeProductos a códigos de producto del inventario
PRODUCT_PHOTOS_MAP = {
    # --- COMBOS Y BEBIDAS EN RAÍZ ---
    "435": "FotosDeProductos/bombay sapphire.jpg",                         # BOMBAY
    "479": "FotosDeProductos/combo fernet.jpg",                            # COMBO BRANCA + COCA 2,25 + HIELO
    "108": "FotosDeProductos/Fernet buhero.jpg",                           # BUHERO NEGRO 700ML
    "111": "FotosDeProductos/Fernet vittone.webp",                         # VITTONE 750ML
    "352": "FotosDeProductos/Havana Club Ron 7 Anos.jpg",                  # RON HAVANA CLUB 7 AÑOS 700ML
    "024": "FotosDeProductos/Havana club especial.jpg",                    # RON HAVANA CLUB ESPECIAL
    "023": "FotosDeProductos/havana club original.jpg",                    # RON HAVANA CLUB ORIGINAL
    "279": "FotosDeProductos/Paso De Los Toros Tonica Lata 269ml Pack X24.jpg", # PASO DE LOS TOROS TONICA LATA 269ML
    "096": "FotosDeProductos/Redbull.jpg",                                 # RED BULL 250ML
    "106": "FotosDeProductos/rockstar.jpg",                                # ROCKSTAR ROSA 500ML
    "107": "FotosDeProductos/rockstar.png",                                # ROCKSTAR VERDE 500ML
    "030": "FotosDeProductos/skyy apricot.jpg",                            # VODKA SKYY APRICOT
    "032": "FotosDeProductos/Skyy Cosmic_.jpg",                            # VODKA SKYY COSMIC
    "033": "FotosDeProductos/skyy pineapple.jpg",                          # VODKA SKYY PINEAPPLE
    "031": "FotosDeProductos/skyy raspberry.jpg",                          # VODKA SKYY RASPBERRY
    "029": "FotosDeProductos/skyy vodka.jpg",                              # VODKA SKYY CLASSIC
    "022": "FotosDeProductos/tanqueray london dry gin.jpg",                 # GIN TANQUERAY CLASSIC
    "021": "FotosDeProductos/tanqueray sevilla.jpg",                       # GIN TANQUERAY SEVILLA

    # --- BEBIDAS CON ALCOHOL (DESTILADOS & APERITIVOS) ---
    "012": "FotosDeProductos/bebidas con alcohol/Absolut Peach Flavored Vodka, 750 ml - copia - copia - copia.jpg", # ABSOLUT PEACH
    "010": "FotosDeProductos/bebidas con alcohol/Absolut vodka.jpg",       # ABSOLUT CLASSIC
    "009": "FotosDeProductos/bebidas con alcohol/Absolut wild berry.jpg",   # ABSOLUT WILDBERRI
    "007": "FotosDeProductos/bebidas con alcohol/absolut raspberry.jpg",   # ABSOLUT RASPBERRY 700 ML
    "025": "FotosDeProductos/bebidas con alcohol/Bacardi carta blanca.jpg", # RON BACARDI CARTA BLANCA
    "273": "FotosDeProductos/bebidas con alcohol/Baileys.jpg",             # BAILEYS ORIGINAL750 ML
    "118": "FotosDeProductos/bebidas con alcohol/Campari.jpg",             # CAMPARI 750ML
    "116": "FotosDeProductos/bebidas con alcohol/Gancia.jpg",              # GANCIA 950ML
    "203": "FotosDeProductos/bebidas con alcohol/Jack Daniels Blackberry 750cc.jpg", # JACK DANIEL S BLACKBERRY
    "207": "FotosDeProductos/bebidas con alcohol/Jameson Whiskey Irlandes 750ml.jpg", # JAMENSON
    "206": "FotosDeProductos/bebidas con alcohol/Johnnie Walker Double Black.jpg", # JOHNNIE WALKER DOUBLE BLACK
    "011": "FotosDeProductos/bebidas con alcohol/Pears Vodka _ Pear Vodka by Absolut _ 750ml _ Sweden.jpg", # ABSOLUT PEARS
    "013": "FotosDeProductos/bebidas con alcohol/Smirnoff Spicy Tamarind.jpg", # SMIRNOFF SPICY TAMARIND
    "016": "FotosDeProductos/bebidas con alcohol/Vodka Smirnoff No_ 21 - 1 L.jpg", # SMIRNOFF CLASSIC
    "204": "FotosDeProductos/bebidas con alcohol/Whisky Johnnie Walker Red Label.jpg", # JOHNNIE WALKER RED LABEL
    "117": "FotosDeProductos/bebidas con alcohol/aperol.jpg",              # APEROL 750ML
    "201": "FotosDeProductos/bebidas con alcohol/jack daniels n7.jpg",     # JACK DANIEL S WHISKEY ETIQUETA NEGRA
    "005": "FotosDeProductos/bebidas con alcohol/fernet branca.jpg",       # FERNET BRANCA 750 ml
    "202": "FotosDeProductos/bebidas con alcohol/jack daniels fire.jpg",   # JACK DANIEL S FIRE
    "346": "FotosDeProductos/bebidas con alcohol/jack daniels honey.jpg",  # JACK DANIELS HONEY
    "205": "FotosDeProductos/bebidas con alcohol/johnnie walker black label.jpg", # JOHNNIE WALKER BLACK LABEL
    "026": "FotosDeProductos/bebidas con alcohol/malibu.jpg",              # RON MALIBU
    "281": "FotosDeProductos/bebidas con alcohol/smirnoff bitter citric grapefruit.jpg", # SMIRNOFF BITTER CITRIC GRAPEFRUIT
    "282": "FotosDeProductos/bebidas con alcohol/smirnoff bitter citric ruby orange & lime.jpg", # SMIRNOFF BITTER CITRIC RUBY ORANGE
    "014": "FotosDeProductos/bebidas con alcohol/smirnoff green apple.jpg",# SMIRNOFF GREEN APPLE
    "015": "FotosDeProductos/bebidas con alcohol/smirnoff raspberry.jpg",  # SMIRNOFF RASPBERRY

    # --- BEBIDAS SIN ALCOHOL (GASEOSAS, AGUAS, ENERGIZANTES & JUGOS) ---
    "092": "FotosDeProductos/Bebidas sin alcohol/7up.jpg",                  # 7UP ZERO 500ML
    "079": "FotosDeProductos/Bebidas sin alcohol/Agua Mineral Ser Sin Gas 1,5l X6.jpg", # AGUA SER SIN GAS 1,5L
    "078": "FotosDeProductos/Bebidas sin alcohol/Agua Mineral Villavicencio 2 L Sin Gas Pack X6 La Barra.jpg", # AGUA VILLAVICENCIO 1.5L SIN GAS
    "421": "FotosDeProductos/Bebidas sin alcohol/Agua clara graziani.webp",# AGUA CLARA BY GRAZIANI 2L
    "288": "FotosDeProductos/Bebidas sin alcohol/Agua nihuil grande.jpg",  # AGUA BIDON  NIHUIL 5L
    "286": "FotosDeProductos/Bebidas sin alcohol/Bebida Isotonica Gatorade Zero Sabor Mora 400 Ml.jpg", # GATORADE ZERO MORAS 400 ML
    "091": "FotosDeProductos/Bebidas sin alcohol/Fanta 500ml.jpg",         # FANTA 500ML
    "087": "FotosDeProductos/Bebidas sin alcohol/Gaseosa-CocaCola-Sabor-Original-500-Ml-_1.jpg", # COCA COLA REGULAR 500ML
    "145": "FotosDeProductos/Bebidas sin alcohol/Gatorade(1).jpg",         # GATORADE 750ML
    "280": "FotosDeProductos/Bebidas sin alcohol/gatorade.jpg",            # GATORADE NARANJA 500ML
    "274": "FotosDeProductos/Bebidas sin alcohol/Kombuchas.jpg",           # KOMBUCHA OY 473 ML
    "275": "FotosDeProductos/Bebidas sin alcohol/LATA COCA.jpg",           # COCA COLA REGULAR LATA 354ML
    "326": "FotosDeProductos/Bebidas sin alcohol/Mirinda, 1,5 L.jpg",       # MIRINDA 1,5 L
    "361": "FotosDeProductos/Bebidas sin alcohol/Monster Ultra Peachy Keen.jpg", # MONSTER ULTRA PEACHY KEEN
    "360": "FotosDeProductos/Bebidas sin alcohol/Monster pipeline puch.jpg",# MONSTER PIPELINE PUNCH
    "365": "FotosDeProductos/Bebidas sin alcohol/Monster ultra watermelon zero sugar 0_5l.jpg", # MONSTER ULTRA WATERMELON
    "069": "FotosDeProductos/Bebidas sin alcohol/PASO DE LOS TOROS - Pomelo 1_5 L.jpg", # PASOS DE LOS TOROS POMELO 1,5L
    "081": "FotosDeProductos/Bebidas sin alcohol/paso de los toros tonica.jpg", # PASO DE LOS TOROS AGUA TONICA 1,5L
    "093": "FotosDeProductos/Bebidas sin alcohol/Refresco pepsi black sin azucar 355 ml.jpg", # PEPSI BLACK
    "299": "FotosDeProductos/Bebidas sin alcohol/Tuti.jpg",                # JUGO TUTTI NARANJA 1 L
    "076": "FotosDeProductos/Bebidas sin alcohol/agua-sin-gas-graziani-500-ml-ofertas-casa-segal-supermercado-mendoza.jpg", # CLARA BY GRAZIANI 500ML SIN GAS
    "070": "FotosDeProductos/Bebidas sin alcohol/cepita naranja 1l caja.jpg", # CEPITA X LITRO CAJA
    "071": "FotosDeProductos/Bebidas sin alcohol/citric xd.jpg",           # CITRIC X LTR
    "073": "FotosDeProductos/Bebidas sin alcohol/citric 200ml.jpg",        # CITRIC 200ML
    "088": "FotosDeProductos/Bebidas sin alcohol/coca zero 500ml.jpg",     # COCA COLA ZERO 500ML
    "086": "FotosDeProductos/Bebidas sin alcohol/coca-cola-1lt.png",       # COCA COLA REGULAR 1,5L
    "089": "FotosDeProductos/Bebidas sin alcohol/coca-zero-1lt.png",       # COCA COLA ZERO 1,5
    "102": "FotosDeProductos/Bebidas sin alcohol/fresh 1,5.png",           # BAGGIO FRESH 1,5L
    "283": "FotosDeProductos/Bebidas sin alcohol/fresh manzana.jpg",       # BAGGIO FRESH 600ML MANZANA
    "074": "FotosDeProductos/Bebidas sin alcohol/fresh naranja.jpg",       # BAGGIO FRESH 200ML
    "284": "FotosDeProductos/Bebidas sin alcohol/fresh pomelo.jpg",        # BAGGIO FRESH 600 ML POMELO
    "075": "FotosDeProductos/Bebidas sin alcohol/fresh.jpg",               # BAGGIO FRESH BOTELLA 600ML
    "130": "FotosDeProductos/Bebidas sin alcohol/heineken 00.jpg",         # HEINEKEN 0.0 473CM
    "131": "FotosDeProductos/Bebidas sin alcohol/imperial golden 0.0.jpg", # IMPERIAL GOLDEN SIN ALCOHOL 473CM
    "072": "FotosDeProductos/Bebidas sin alcohol/jugo-cepita-hf-durazno-x-1l.jpg", # CEPITA BOTELLA 1L

    # --- MARTINO WINES (BODEGA AMIGA) ---
    "372": "FotosDeProductos/VINOS/f89450e2-bfe6-4926-8441-1ba9ed2d027b.jpg",  # MARTINO PEDRO XIMÉNEZ 2022 VINO BLANCO
    "373": "FotosDeProductos/VINOS/Martino bonarda 2023.jpg",                   # MARTINO BONARDA 2025
    "374": "FotosDeProductos/VINOS/f0737caa-ad58-4e01-9137-006c3c08907e.jpg",  # MARTINO ROSÉ 2024
    "375": "FotosDeProductos/VINOS/Martino marselan 2024.jpg",                  # MARTINO MARSELAN 2024
    "376": "FotosDeProductos/VINOS/Martino cabernet franc 2025.jpg",           # MARTINO CABERNET FRANC 2025

    # --- VINOS TINTOS & BLANCOS ---
    "036": "FotosDeProductos/VINOS/San huberto clasico 375cc Malbec.jpg",       # SAN HUBERTO CLASICO 375 ML
    "039": "FotosDeProductos/VINOS/Dilema Day cabernet.jpg",                   # DILEMA CABERNET
    "040": "FotosDeProductos/VINOS/Estancia Mendoza Cabernet Sauvignon_.jpg",   # ESTANCIA MENDOZA CAB SAU
    "041": "FotosDeProductos/VINOS/Estancia Mendoza malbec.jpg",               # ESTANCIA MENDOZA MALBEC
    "043": "FotosDeProductos/VINOS/cu4tro monos locos malbec salvaje.jpg",     # 4 MONOS LOCOS
    "045": "FotosDeProductos/VINOS/San huberto sin alcohol_.jpg",              # SAN HUBERTO SIN ALCOHOL TINTO
    "047": "FotosDeProductos/VINOS/Benjamin syrah.jpg",                        # BENJAMIN SYRAH
    "048": "FotosDeProductos/VINOS/Benjamin merlot.jpg",                       # BENJAMIN MERLOT
    "050": "FotosDeProductos/VINOS/Los cardos malbec.jpg",                     # LOS CARDOS MALBEC
    "051": "FotosDeProductos/VINOS/Los cardos Cabernet sauvignon.jpg",         # LOS CARDOS CAB SAU
    "052": "FotosDeProductos/VINOS/Cordero con piel de lobo Bonarda 2025.jpg", # CORDERO CON PIEL DE LOBO BONARDA 2025
    "054": "FotosDeProductos/VINOS/profugo frutos rojos.jpg",                  # PROFUGO FRUTOS ROJOS
    "055": "FotosDeProductos/VINOS/profugo especias.jpg",                      # PROFUGO ESPECIAS
    "056": "FotosDeProductos/VINOS/finca flichman estate malbec.jpg",          # FLICHMANN STATE MALBEC
    "058": "FotosDeProductos/VINOS/finca flichman reserva malbec.jpg",         # FLICHMANN RESERVA MALBEC
    "059": "FotosDeProductos/VINOS/finca flichman reserva cabernet franc.jpg", # FLICHMANN RESERVA CAB FRANC
    "060": "FotosDeProductos/VINOS/Dona paula estate malbec reserva 2025.jpg", # DOÑA PAULA STATE MALBEC
    "061": "FotosDeProductos/VINOS/Crux tempranillo 2024.jpg",                 # CRUX TEMPRANILLO 2024
    "063": "FotosDeProductos/VINOS/Crux malbec 2024.jpg",                      # CRUX MALBEC 2024
    "064": "FotosDeProductos/VINOS/crux cabernet franc 2024.jpg",              # CRUX CAB FRANC 2024
    "065": "FotosDeProductos/VINOS/f20cfa5b-9931-4532-9047-371b1a4d4970.jpg", # CRUX SAUVIGNON BLANC 2024
    "066": "FotosDeProductos/VINOS/e8367ef2-fd00-47fb-8685-0bf2eeed5ec2.jpg", # CRUX ROXE 2023
    "067": "FotosDeProductos/VINOS/Partridge malbec 2024.jpg",                 # PARTRIDGE MALBEC 2024 2025
    "068": "FotosDeProductos/VINOS/Partidge cabernet Sauvignon 2024.jpg",      # PARTRIDGE CAB SAU 2024
    "112": "FotosDeProductos/VINOS/f25afdb3-911c-4b14-8f23-4b8c5edf7623.jpg", # MONTEBELLO MALBEC 3L
    "113": "FotosDeProductos/VINOS/Bag in box Partridge malbec.jpg",           # PARTRIDGE MALBEC 3L
    "114": "FotosDeProductos/VINOS/dbbcd4f5-6605-4eac-a913-1a3f7af434bb.jpg", # BY THE GLASS DUO 3L
    "147": "FotosDeProductos/VINOS/c88c004e-ecac-4b0f-92e1-03fdbf050180.jpg", # PORTILLO NARANJO DULCE
    "148": "FotosDeProductos/VINOS/Portillo dulce natural 10.jpg",             # PORTILLO DULCE NATURAL 10
    "149": "FotosDeProductos/VINOS/Santa julia chenin dulce.jpg",              # SANTA JULIA CHENIN DULCE NATURAL
    "150": "FotosDeProductos/VINOS/estancia mendoza chenin chardonnay dulce.jpg", # ESTANCIA MENDOZA DULCE CHENIN CHARDONNAY
    "151": "FotosDeProductos/VINOS/Dilema blanco dulce.jpg",                   # DILEMA BLANCO DULCE
    "152": "FotosDeProductos/VINOS/Canciller blend dulce_.jpg",                # CANCILLER BLEND DULCE
    "153": "FotosDeProductos/VINOS/Santa Julia dulce tinto.jpg",               # SANTA JULIA DULCE TINTO
    "155": "FotosDeProductos/VINOS/Benjamin Dulce.jpg",                        # BENJAMIN DULCE
    "156": "FotosDeProductos/VINOS/Colon selecto Durazno_.jpg",                 # COLON SELECTO DULCE DURAZNO
    "158": "FotosDeProductos/VINOS/ce1037ba-c1fa-46ce-bba9-2a4cdf84622c.jpg", # COLON SELECTO BLANCO DULCE
    "159": "FotosDeProductos/VINOS/Colon selecto dulce fresco rose.jpg",       # COLON SELECTO ROSA DULCE
    "160": "FotosDeProductos/VINOS/Portillo chardonnay 04.jpg",                # PORTILLO CHANRDONNAY 04
    "161": "FotosDeProductos/VINOS/portillo sauvignon blanc 03.jpg",           # PORTILLO SAUVIGNON BLANC 03
    "162": "FotosDeProductos/VINOS/Benjamin chardonnay.jpg",                   # BENJAMIN CHARDONNAY
    "163": "FotosDeProductos/VINOS/finca flichman chardonnay.jpg",             # FLICHMAN CHARDONNAY
    "164": "FotosDeProductos/VINOS/Partridge chardonnay 2025.jpg",             # PARTRIDGE CHARDONNAY
    "165": "FotosDeProductos/VINOS/bodega privada sauvignon blanc.jpg",         # BODEGA PRIVADA SAUVIGNON BLANC
    "166": "FotosDeProductos/VINOS/46b93eec-173c-4d0a-b80d-1d08b4024476.jpg", # LOS CARDOS SAUVIGNON BLANC
    "167": "FotosDeProductos/VINOS/Los cardos chardonnay 2025.jpg",            # LOS CARDOS CHARDONNAY
    "168": "FotosDeProductos/VINOS/5bcb25fc-a878-4975-9c60-d5fc843f6197.jpg", # SAINT FELICIEN CHARDONNAY
    "209": "FotosDeProductos/VINOS/perro callejero blend de malbec.jpg",       # PERRO CALLEJERO MALBEC 2024
    "213": "FotosDeProductos/VINOS/fond de cave cabernet sauvignon.jpg",       # FOND DE CAVE CABERNET SAUVIGNON 2025
    "217": "FotosDeProductos/VINOS/Alambrado malbec 2025.jpg",                 # ALAMBRADO MALBEC
    "227": "FotosDeProductos/VINOS/Carmela malbec 2023.jpg",                   # CARMELA MALBEC
    "228": "FotosDeProductos/VINOS/Durigutti Aguijon de Abeja Obrera Cabernet franc 2024.jpg", # AGUIJON DE ABEJA OBRERA CABERNET FRANC 2024
    "229": "FotosDeProductos/VINOS/Durigutti Aguijon de Abeja Obrera malbec 2023.jpg",         # AGUIJON DE ABEJA OBRERA MALBEC 2023
    "230": "FotosDeProductos/VINOS/Cara sucia vino de rivadavia 2024.jpg",     # CARA SUCIA 2024 CRIOLLA
    "245": "FotosDeProductos/VINOS/Septima emblema malbec 2024.jpg",           # SEPTIMA EMBLEMA MALBEC
    "249": "FotosDeProductos/VINOS/finca flichman estate cabernet sauvignon.jpg", # FLICHMANN STATE CAB SAU
    "250": "FotosDeProductos/VINOS/e2ccaa36-1581-41c5-9cc1-a2ef426696f9.jpg", # LOS PASOS CAB SAU
    "251": "FotosDeProductos/VINOS/d4ad7052-5cfb-454e-ab9c-787b49e852cc.jpg", # LOS PASOS MALBEC
    "253": "FotosDeProductos/VINOS/fc50b867-22eb-4887-9aa9-396a14b055f6.jpg", # LOS PASOS CHARDONNAY
    "254": "FotosDeProductos/VINOS/b134b9bb-3eef-4327-badb-e642bb7cb665.jpg", # LOS PASOS BLANCO DULCE
    "255": "FotosDeProductos/VINOS/D_lilah malbec rose.jpg",                   # D´ALILAH MALBEC ROSE
    "256": "FotosDeProductos/VINOS/53a8ca72-354b-443f-8a7b-88a0e7392ca9.jpg", # SEPTIMA EMBLEMA CHARDONNAY
    "257": "FotosDeProductos/VINOS/Portillo rose 05.jpg",                      # PORTILLO ROSE 05
    "259": "FotosDeProductos/VINOS/9cb79f17-7684-4ce5-b09d-b56ac5d2997a.jpg", # PORTILLO MALBEC 01
    "260": "FotosDeProductos/VINOS/1295f7c9-51f2-4033-bf9b-360d3886747b.jpg", # PORTILLO MERLOT 06
    "261": "FotosDeProductos/VINOS/fcae451a-a3fe-40ea-a271-3a2ead3c18a8.jpg", # PORTILLO SYRAH 08
    "262": "FotosDeProductos/VINOS/8f5aab9a-7b20-451e-8111-d45942df3ae4.jpg", # PORTILLO CAB SAU 02
    "317": "FotosDeProductos/VINOS/cordero con piel de lobo cabernet sauvignon.jpg", # CORDERO CON PIEL DE LOBO CABERNET SAUVIGNON 2026
    "318": "FotosDeProductos/VINOS/Durigutti blanc de blanc_.jpg",             # DURIGUTTI BLANC DE BLANCS
    "347": "FotosDeProductos/VINOS/Dona Paula estate cabernet sauvignon reserva 205.jpg", # DOÑA PAULA ESTATE CABERNET SAUVIGNON
    "368": "FotosDeProductos/VINOS/Nampe malbec.jpg",                          # VINO NAMPE TINTO MALBEC 2025 1125ML
    "393": "FotosDeProductos/VINOS/punto final sauvignon black 2024.jpg",      # PUNTO FINAL SAU BLANC
    "399": "FotosDeProductos/VINOS/Pregunton malbec.jpg",                      # PREGUNTON MALBEC
    "400": "FotosDeProductos/VINOS/Pregunton cabernet Sauvignon_.jpg",         # PREGUNTON CABERNET SAUVIGNON
    "411": "FotosDeProductos/Bebidas sin alcohol/7UP Free 1,5 l PET DPG.jpg",  # 7UP ZERO 1,5 ML
    "423": "FotosDeProductos/VINOS/Alambrado cabernet franc 2025.jpg",         # ALAMBRADO CABERNET FRAN
    "450": "FotosDeProductos/VINOS/Los cardos private collection Sauvignon blanc 2025.jpg", # LOS CARDOS SAUVIGNON BLANC 2025
    "451": "FotosDeProductos/VINOS/Dona paula estate Sauvignon blanc 2025.jpg",# DOÑA PAULA SAUVIGNON BLANC
    "453": "FotosDeProductos/VINOS/Dona paula estate black edition 2024 bold red blend.jpg", # DOÑA PAULA ESTATE BOLD RED BLEND
    "460": "FotosDeProductos/VINOS/62a0030f-ff41-471e-aad5-5cd2521f90bc.jpg", # FOND DE CAVE CHARDONNAY 2025
    "466": "FotosDeProductos/VINOS/d4cab08f-3464-44c0-8cd7-5b4c5a5f78dc.jpg", # ATILIO AVENA MALBEC
    "482": "FotosDeProductos/VINOS/Finca flichman Gran reserva malbec 2024.jpg",# FLICHMANN GRAN RESERVA MALBEC
}

def clean_title(text):
    if not isinstance(text, str):
        return ""
    
    text = text.replace("´", "").replace("`", "")
    words = text.strip().split()
    cleaned_words = []
    
    keep_upper = {
        "ML", "L", "LTS", "LT", "GR", "GRS", "KG", "CC", "7UP", "IPA", "APA", 
        "X1", "X2", "X3", "X6", "X12", "RTD", "BIB", "PX", "CF", "DOC", "OCB", "CM"
    }
    lowercase_words = {"de", "del", "y", "la", "las", "el", "los", "en", "con", "a", "por", "sin", "para"}

    for w in words:
        upper = w.upper()
        if upper in keep_upper:
            cleaned_words.append(upper)
        elif re.match(r'^\d+([,\.]\d+)?(ML|LTS|LT|L|CC|GR|GRS|KG|CM)$', upper):
            cleaned_words.append(upper)
        elif upper.lower() in lowercase_words and len(cleaned_words) > 0:
            cleaned_words.append(upper.lower())
        else:
            cleaned_words.append(w.capitalize())
    
    res = " ".join(cleaned_words)
    if res:
        res = res[0].upper() + res[1:]
    return res

def get_category_and_subcategory(rubro_val, desc_val):
    rubro = str(rubro_val or "").upper().strip()
    desc = str(desc_val or "").upper().strip()

    # 1. VINOS TINTOS & BLANCOS
    if "VINOS TINTOS" in rubro:
        cat = "tintos"
        if "MALBEC" in desc:
            subcat = "malbec"
        elif any(k in desc for k in ["CABERNET", "FRANC", "CAB SAU", "CAB."]):
            subcat = "cabernet-sauvignon"
        else:
            subcat = "blends"
        return cat, subcat

    if "VINOS BLANCOS" in rubro:
        return "blancos", "blancos-chardonnay"

    if "VINOS DULCES" in rubro:
        return "blancos", "dulces"

    if "VINOS ROSADOS" in rubro:
        return "blancos", "rosados"

    if "ESPUMANTES" in rubro:
        return "blancos", "espumantes"

    if "VINOS 375" in rubro or "BAG IN BOX" in rubro or "DAMAJUANAS" in rubro:
        if any(k in desc for k in ["CHARDONNAY", "BLANCO", "SAUVIGNON BLANC", "TORRONTES", "DULCE"]):
            return "blancos", "blancos-chardonnay"
        elif any(k in desc for k in ["ROSE", "ROSADO"]):
            return "blancos", "rosados"
        elif any(k in desc for k in ["ESPUMANTE", "EXTRA BRUT"]):
            return "blancos", "espumantes"
        else:
            cat = "tintos"
            if "MALBEC" in desc:
                subcat = "malbec"
            elif any(k in desc for k in ["CABERNET", "FRANC", "CAB SAU"]):
                subcat = "cabernet-sauvignon"
            else:
                subcat = "blends"
            return cat, subcat

    if "VINOS SIN ALCOHOL" in rubro:
        if any(k in desc for k in ["BLANCO", "CHARDONNAY", "DULCE"]):
            return "blancos", "blancos-chardonnay"
        return "tintos", "blends"

    # 2. BEBIDAS (CERVEZAS & DESTILADOS)
    if "CERVEZAS SIN ALCOHOL" in rubro or "CERVEZAS" in rubro:
        return "bebidas", "cervezas"

    if any(k in rubro for k in ["FERNET", "APERITIVOS", "VERMOUTH", "RON"]):
        return "bebidas", "fernet-aperitivos"

    if "READY TO DRINK" in rubro:
        if "ROSE" in desc:
            return "blancos", "rosados"
        if "TINTILLO" in desc:
            return "tintos", "blends"
        if "SMIRNOFF" in desc:
            return "bebidas", "vodka"
        return "bebidas", "fernet-aperitivos"

    if "GIN" in rubro:
        return "bebidas", "gin"

    if "VODKA" in rubro:
        return "bebidas", "vodka"

    if "WHISKY" in rubro:
        return "bebidas", "whisky"

    if "OTRAS BEBIDAS BLANCAS" in rubro:
        if "GIN" in desc or "GINEBRA" in desc:
            return "bebidas", "gin"
        if "VODKA" in desc:
            return "bebidas", "vodka"
        if "WHISKY" in desc:
            return "bebidas", "whisky"
        return "bebidas", "fernet-aperitivos"

    # 3. SIN ALCOHOL
    if "GASEOSAS" in rubro:
        if any(t in desc for t in ["TONICA", "TÓNICA", "SCHWEPPES", "PASO DE LOS TOROS"]):
            return "sin-alcohol", "tonicas-mixers"
        return "sin-alcohol", "gaseosas"

    if "ENERGIZANTES" in rubro:
        return "sin-alcohol", "energizantes"

    if "AGUAS Y SODAS" in rubro:
        if any(s in desc for s in ["SODA", "SIFON", "SIFÓN"]):
            return "sin-alcohol", "tonicas-mixers"
        return "sin-alcohol", "aguas-jugos"

    if "JUGOS Y AGUAS SABORIZADAS" in rubro:
        return "sin-alcohol", "aguas-jugos"

    # 4. SNACKS & COMBOS & VARIOS
    if "COMBOS" in rubro or "COMBO" in desc:
        return "snacks", "promos-combos"

    if any(k in rubro for k in ["CAFE", "CAFÉ", "CIGARRILLO", "TABACO"]):
        return "snacks", "chocolates-dulces"

    if any(k in rubro for k in ["HIELOS", "DESCARTABLES", "LEÑA", "LEA", "REGALOS"]):
        return "snacks", "hielo-descartables"

    if "SNACKS" in rubro:
        if any(d in desc for d in ["ALFAJOR", "CHOCOLATE", "CHUPETIN", "CHUPETÍN", "DULCE", "CONFITE", "CARAMELO"]):
            return "snacks", "chocolates-dulces"
        return "snacks", "snacks-salados"

    # Fallback si Rubro es None o no catalogado
    if any(w in desc for w in ["MALBEC", "CABERNET", "VINO", "FLICMANN", "CORDERO"]):
        return "tintos", "malbec" if "MALBEC" in desc else "cabernet-sauvignon"
    if any(w in desc for w in ["CHARDONNAY", "MOSCATO", "TORRONTES", "BLANCO"]):
        return "blancos", "blancos-chardonnay"
    if any(w in desc for w in ["IMPERIAL", "CERVEZA", "ANDES", "CORONA", "QUILMES"]):
        return "bebidas", "cervezas"
    if "JUGO" in desc:
        return "sin-alcohol", "aguas-jugos"
    if "SODA" in desc:
        return "sin-alcohol", "tonicas-mixers"
    if any(w in desc for w in ["CAJA", "SACACORCHOS", "DESTAPADOR", "VARIOS", "HIELO"]):
        return "snacks", "hielo-descartables"
    if any(w in desc for w in ["PHILLIES", "CIGARRO", "BLUNT", "TABACO"]):
        return "snacks", "chocolates-dulces"

    return "snacks", "snacks-salados"

def get_product_image(cat, subcat, rubro, desc):
    """Retorna una imagen conceptual de alta resolución según el producto específico."""
    u = str(desc or "").upper()
    r = str(rubro or "").upper()

    # --- MARTINO WINES ---
    if "MARTINO" in u:
        if "PEDRO" in u or "XIM" in u or "BLANCO" in u:
            return "https://images.unsplash.com/photo-1584916201218-f4242ceb4809?w=800&auto=format&fit=crop&q=80"
        if "CABERNET" in u or "FRANC" in u:
            return "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=800&auto=format&fit=crop&q=80"
        if "MARSELAN" in u:
            return "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=800&auto=format&fit=crop&q=80"
        if "BONARDA" in u:
            return "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800&auto=format&fit=crop&q=80"
        if "ROS" in u:
            return "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800&auto=format&fit=crop&q=80"

    # --- COMBOS ESPECÍFICOS ---
    if "COMBO" in u or subcat == "promos-combos":
        if "FERNET" in u or "BRANCA" in u or "VITTONE" in u or "BUHERO" in u:
            return "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=800&auto=format&fit=crop&q=80"
        if "GIN" in u or "GINKGO" in u or "BEEFEATER" in u or "GORDON" in u:
            return "https://images.unsplash.com/photo-1527061011665-3652c757a4d4?w=800&auto=format&fit=crop&q=80"
        if "APEROL" in u or "CAMPARI" in u or "CARPANO" in u:
            return "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&auto=format&fit=crop&q=80"
        if "SKYY" in u or "VODKA" in u or "SMIRNOFF" in u or "ABSOLUT" in u or "SERNOVA" in u:
            return "https://images.unsplash.com/photo-1560512823-829485b8bf24?w=800&auto=format&fit=crop&q=80"
        if "RON" in u or "HAVANA" in u or "HAVANNA" in u or "BACARDI" in u:
            return "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=800&auto=format&fit=crop&q=80"
        if "CAF" in u:
            return "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=800&auto=format&fit=crop&q=80"

    # --- VINOS TINTOS & BLANCOS ---
    if cat in ["tintos", "blancos", "vinos"]:
        if "MALBEC" in u:
            return "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800&auto=format&fit=crop&q=80"
        if "CABERNET" in u or "FRANC" in u:
            return "https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=800&auto=format&fit=crop&q=80"
        if "ESPUMANTE" in r or "BRUT" in u or "CHANDON" in u or "EXTRA BRUT" in u or "ESPUMANTE" in u or "PROSECCO" in u:
            return "https://images.unsplash.com/photo-1594142345550-949f57564d26?w=800&auto=format&fit=crop&q=80"
        if any(w in u for w in ["CHARDONNAY", "SAUVIGNON BLANC", "BLANCO", "BLANCS", "RIESLING", "TORRONTES", "TORRONTÉS"]):
            return "https://images.unsplash.com/photo-1569919659476-f0852f6834b7?w=800&auto=format&fit=crop&q=80"
        if "ROSE" in u or "ROSADO" in u or "ROXE" in u:
            return "https://images.unsplash.com/photo-1558001373-7b93ee48ffa0?w=800&auto=format&fit=crop&q=80"
        if "DULCE" in u or "DULCES" in r or "COSECHA TARDIA" in u:
            return "https://images.unsplash.com/photo-1584916201218-f4242ceb4809?w=800&auto=format&fit=crop&q=80"
        if "DAMAJUANA" in u or "BAG IN BOX" in u or "BIB" in u:
            return "https://images.unsplash.com/photo-1547595628-c61a29f496f0?w=800&auto=format&fit=crop&q=80"
        if cat == "blancos":
            return "https://images.unsplash.com/photo-1569919659476-f0852f6834b7?w=800&auto=format&fit=crop&q=80"
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
        if "BAILEYS" in u or "COGNAC" in u or "LICOR" in u or "HESPERIDINA" in u or "ANIS" in u or "ANÍS" in u:
            return "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=800&auto=format&fit=crop&q=80"
        
        # Gin
        if subcat == "gin" or "GIN" in u or "TANQUERAY" in u or "HEREDERO" in u or "GINGKO" in u or "BEEFEATER" in u or "BOMBAY" in u:
            return "https://images.unsplash.com/photo-1527061011665-3652c757a4d4?w=800&auto=format&fit=crop&q=80"
        
        # Vodka
        if subcat == "vodka" or "VODKA" in u or "ABSOLUT" in u or "SKYY" in u or "SERNOVA" in u or "SMIRNOFF" in u:
            if any(flv in u for flv in ["MANGO", "PEACH", "PEARS", "RASPBERRY", "WILDBERRI", "APRICOT", "COSMIC", "JUNGLE", "PINEAPPLE", "ICE POP", "WILD BERRIES", "TROPICAL"]):
                return "https://images.unsplash.com/photo-1563227812-0ea4c22e6cc8?w=800&auto=format&fit=crop&q=80"
            return "https://images.unsplash.com/photo-1560512823-829485b8bf24?w=800&auto=format&fit=crop&q=80"
        
        # Whisky
        if subcat == "whisky" or "WHISKY" in u or "WHISKEY" in u or "JACK DANIEL" in u or "JAMESON" in u or "JAMENSON" in u or "CRIADORES" in u:
            return "https://images.unsplash.com/photo-1527281400683-1aae777175f8?w=800&auto=format&fit=crop&q=80"
        
        # Ron
        if "RON" in u or "HAVANA" in u or "BACARDI" in u or "MALIBU" in u:
            return "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=800&auto=format&fit=crop&q=80"
        
        # Cervezas
        if "CORONA" in u or "STELLA" in u or "HEINEKEN" in u or "BOTELLA" in u:
            return "https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=800&auto=format&fit=crop&q=80"
        if "IPA" in u or "ANDES" in u or "PATAGONIA" in u:
            return "https://images.unsplash.com/photo-1567696911980-2eed69a46042?w=800&auto=format&fit=crop&q=80"
        if "LATA" in u or "LATON" in u or "LATÓN" in u or "BRAHMA" in u or "BUDWEISER" in u or "SCHNEIDER" in u or "QUILMES" in u or "IMPERIAL" in u:
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
        if "AGUA" in u or "SODA" in u or "VIDA" in u or "VILLAVICENCIO" in u or "GRAZIANI" in u or "NIHUIL" in u:
            return "https://images.unsplash.com/photo-1548839140-29a749e1bc4e?w=800&auto=format&fit=crop&q=80"
        if "0.0" in u or "SIN ALCOHOL" in u:
            return "https://images.unsplash.com/photo-1518176258769-f227c798150e?w=800&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=800&auto=format&fit=crop&q=80"

    # --- SNACKS, COMBOS & VARIOS ---
    if cat == "snacks":
        if any(d in u for d in ["ALFAJOR", "CHOCOLATE", "CHUPETIN", "CHUPETÍN", "DULCE", "CONFITES", "CARAMELOS"]):
            return "https://images.unsplash.com/photo-1548907040-4baa42d10919?w=800&auto=format&fit=crop&q=80"
        if "CAFE" in u or "CAFÉ" in u or "CAPSULA" in u:
            return "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800&auto=format&fit=crop&q=80"
        if "HIELO" in u:
            return "https://images.unsplash.com/photo-1548839140-29a749e1bc4e?w=800&auto=format&fit=crop&q=80"
        if any(t in u for t in ["TABACO", "CIGARRO", "BLUNT", "ENCENDEDOR", "SEDAS", "FILTROS", "OCB", "VAPER", "PHILLIES"]):
            return "https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=800&auto=format&fit=crop&q=80"
        if "LEÑA" in u or "LEA" in u or "CARBÓN" in u:
            return "https://images.unsplash.com/photo-1542838132-92c53300491e?w=800&auto=format&fit=crop&q=80"
        if any(s in u for s in ["PAPA", "SNACK", "ACEITUNA", "MANI", "MANÍ", "NACHO", "OLIVA", "AROMATICAS"]):
            return "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=800&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=800&auto=format&fit=crop&q=80"

    return "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800&auto=format&fit=crop&q=80"

def extract_volume(desc):
    match = re.search(r'(\d+[\.,]?\d*)\s*(ML|LTS|L|LT|CC|GRS|GR|KG|CM)', str(desc), re.IGNORECASE)
    if match:
        val, unit = match.groups()
        unit = unit.upper()
        if unit in ["L", "LTS", "LT"]:
            return f"{val} L"
        elif unit in ["ML", "CC", "CM"]:
            return f"{val} ml"
        elif unit in ["GR", "GRS"]:
            return f"{val} g"
        elif unit == "KG":
            return f"{val} kg"
    return "750 ml"

def convert_excel_to_products():
    excel_path = "inventario actualizado.xlsx"
    if not os.path.exists(excel_path):
        excel_path = "inventario.xlsx"
    
    if not os.path.exists(excel_path):
        print(f"Error: No se encontró ningún archivo Excel ({excel_path})")
        return

    print(f"Leyendo inventario desde: {excel_path}")
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        print("Error: Excel vacío")
        return

    data_rows = rows[1:]

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
                    print(f"Aviso lectura existente: {e}")

    products = []

    for idx, row in enumerate(data_rows, 1):
        raw_code = str(row[0]).strip() if row[0] is not None else str(idx)
        raw_desc = str(row[1]).strip() if row[1] is not None else "Producto"
        raw_rubro = str(row[2]).strip() if row[2] is not None else "VARIOS"
        
        # Precio venta
        try:
            val_p = float(row[8])
            price = int(val_p) if val_p.is_integer() else round(val_p, 2)
            if price < 0:
                price = 0
        except:
            price = 0

        # Precio costo
        try:
            val_c = float(row[7])
            cost = int(val_c) if val_c.is_integer() else round(val_c, 2)
            if cost < 0:
                cost = 0
        except:
            cost = 0

        # Stock actual
        try:
            stock = int(float(row[6]))
        except:
            stock = 0

        # Stock mínimo
        raw_stock_min = row[5] if len(row) > 5 and row[5] is not None else 0
        stock_min = str(raw_stock_min)

        clean_code_num = raw_code.lstrip("0")
        code_formatted = raw_code.zfill(3) if raw_code.isdigit() else raw_code
        item_id = f"prod-{code_formatted.lower().replace(' ', '-')}"

        name = clean_title(raw_desc)
        cat, subcat = get_category_and_subcategory(raw_rubro, raw_desc)
        vol = extract_volume(raw_desc)
        img = get_product_image(cat, subcat, raw_rubro, raw_desc)

        existing = (
            existing_by_code.get(clean_code_num) 
            or existing_by_name.get(name.lower()) 
            or existing_by_name.get(raw_desc.lower())
        )

        is_martino = "MARTINO" in raw_desc.upper() or raw_code in ["372", "373", "374", "375", "376"]
        is_combo = "COMBO" in raw_rubro.upper() or "COMBO" in raw_desc.upper() or "PROMO" in raw_desc.upper()

        if is_martino:
            badge = "Bodega Amiga"
        elif is_combo:
            badge = "Promo Combo"
        elif price <= 0:
            badge = "Consultar"
        elif stock <= 0:
            badge = "Sin Stock"
        elif stock <= 2:
            badge = "Últimas unidades"
        else:
            badge = None

        # Resolución de foto del producto:
        # 1. Foto real y verificada en FotosDeProductos
        # 2. Imagen previa si existía en catálogo
        # 3. Imagen conceptual generada por categoría
        local_photo = (
            PRODUCT_PHOTOS_MAP.get(code_formatted) 
            or PRODUCT_PHOTOS_MAP.get(raw_code) 
            or PRODUCT_PHOTOS_MAP.get(clean_code_num)
        )
        if local_photo:
            final_img = local_photo
        elif existing and existing.get("image") and not existing.get("image").startswith("FotosDeProductos/"):
            final_img = existing.get("image")
        else:
            final_img = img

        martino_enrich = MARTINO_ENRICHMENT.get(raw_code)

        if martino_enrich:
            product = {
                "id": f"prod-{raw_code}",
                "code": code_formatted,
                "name": martino_enrich["name"],
                "category": cat,
                "subcategory": subcat,
                "rubro": raw_rubro,
                "price": price if price > 0 else 22500,
                "oldPrice": None,
                "cost": cost if cost > 0 else 15000,
                "stock": max(stock, 6),
                "stockMin": stock_min,
                "volume": martino_enrich["volume"],
                "alcohol": martino_enrich["alcohol"],
                "origin": "Luján de Cuyo, Mendoza",
                "rating": 4.9,
                "badge": "Bodega Amiga",
                "image": martino_enrich["image"],
                "description": martino_enrich["description"],
                "pairing": martino_enrich["pairing"]
            }
        elif existing:
            product = {
                "id": existing.get("id", item_id),
                "code": code_formatted,
                "name": name if name else existing.get("name", "Producto"),
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
                "image": final_img,
                "description": existing.get("description", f"{name} disponible para entrega inmediata en Paisana Bebidas."),
                "pairing": existing.get("pairing", "Ideal para compartir y disfrutar en tus mejores momentos.")
            }
        else:
            default_origin = "Mendoza, Argentina" if cat in ["tintos", "blancos", "vinos"] else "Línea Oficial"
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
                "origin": default_origin,
                "rating": 4.8,
                "badge": badge,
                "image": final_img,
                "description": f"{name} de alta calidad, listo para disfrutar con entrega inmediata en Paisana Bebidas.",
                "pairing": "Ideal para compartir en reuniones, previas y eventos especiales."
            }

        products.append(product)

    os.makedirs("data", exist_ok=True)
    js_output = "// Catálogo oficial de productos para Paisana Bebidas (Sincronizado con inventario actualizado.xlsx)\n"
    js_output += "const PRODUCTS_DATA = " + json.dumps(products, indent=2, ensure_ascii=False) + ";\n"

    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_output)

    print(f"¡Sincronización exitosa! Se integraron {len(products)} productos categorizados en {js_path}")

if __name__ == "__main__":
    convert_excel_to_products()
