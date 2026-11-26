# Paisana Bebidas - Tienda Online de Vinos de Autor, Combos & Bebidas Selectas 🍷🍺

Plataforma e-commerce moderna, rápida y responsive diseñada para **Paisana Bebidas** (Mendoza), con catálogo sanitizado y sectorizado integralmente por departamentos y rubros oficiales.

---

## 🎨 Identidad Visual y Diseño

- **Paleta de Marca Oficial**:
  - 🌿 **Turquesa Artesanal (Teal)**: `#3ca1a4` / `#58c6c9`
  - 🌾 **Oro Mostaza Cálido**: `#e5aa38` / `#f6be4e`
  - 🍷 **Borgoña & Lúpulo Tostado**: `#582029` / `#7b2a37`
  - 🌑 **Obsidian Slate**: `#0c1017` / `#151e2b`
- **Experiencia de Usuario**:
  - Glassmorphism, micro-animaciones y tipografía editorial (*Roboto Slab*).
  - Diseño Mobile-First con barra inferior tipo app, pestañas con contadores en vivo y drawer lateral táctil.

---

## 🌟 Arquitectura de Catálogo (7 Sectores y 34 Rubros Oficiales)

Sincronizado con `Inventario3.0sanitizado.xlsx` (**578 productos** sin exposición de costos ni datos internos):

1. 🍷 **Vinos Tintos**: *Malbec, Cabernet Sauvignon, Cabernet Franc, Bonarda/Merlot/Pinot Noir/Otros Varietales, Blends & Cortes, Bag in Box 3L, Damajuanas & 375ml*.
2. 🥂 **Blancos, Dulces & Espumantes**: *Vinos Blancos (Chardonnay, Sauvignon Blanc, Pedro Ximénez, Riesling), Espumantes, Vinos Dulces y Vinos Rosados*.
3. 🔥 **Combos & Promos**: *60 combos armados por familia (Fernet + Coca, Vodka + Sprite, Aperitivos & Spritz, Ron + Coca, Gin + Tónica, Promos Café + Alfajor)*.
4. 🍺 **Cervezas & Destilados**: *Cervezas, Fernet, Aperitivos, Vermouth, Gin, Vodka, Whisky, Ron, Ready to Drink (RTD), Licores & Miniaturas*.
5. 🥤 **Sin Alcohol**: *Gaseosas, Tónicas/Pomelos/Sodas, Jugos/Terma/Saborizadas, Isotónicas, Energizantes, Aguas & Kombucha, Cervezas & Vinos 0.0%*.
6. ☕ **Café, Snacks & Gourmet**: *Café de Especialidad (en grano y molido), Snacks Salados & Aceitunas, Alfajores Entre Dos & Chocolates, Aceites de Oliva, Conservas & Coctelería*.
7. 🧊 **Hielo, Tabaco & Regalos**: *Hielo & Leña, Cigarrillos/Cigarros/Vapers, Tabacos/Sedas/Encendedores, Regalería & Sets Asador, Sacacorchos, Cajas & Sorbetes*.

- **Comercio & Carrito Inteligente**:
  - **Índice Interactivo de Rubros**: acceso de 1 clic a cualquiera de los 34 rubros oficiales del inventario.
  - **Buscador Inteligente Sin Tildes**: búsqueda multi-palabra instantánea por nombre, marca, cepa o rubro.
  - **Control de Cantidad en Tarjeta**: stepper `- / +` directo en cada producto agregado.
  - Conmutador entre **Grilla Compacta** y **Lista Ordenada** con persistencia en `localStorage`.
  - **Checkout Desacoplado por WhatsApp** (`+54 9 2612 58-6004`) con referencia única `#COT-XXXXX`.

- **Cumplimiento Normativo Argentino**:
  - 🛡️ Control de acceso (+18) según **Ley Nacional N° 24.788**.
  - 🔄 **Botón de Arrepentimiento** según **Res. 424/2020 & Ley 24.240**.
  - 🔒 Tratamiento de datos local en navegador conforme a **Ley 25.326**.

---

## 🔄 Actualización de Inventario

1. Actualizar precios o productos en `Inventario3.0sanitizado.xlsx` (hoja `Catálogo para web`).
2. Ejecutar:
   ```bash
   python convert_inventory.py
   ```
3. Se regenerará automáticamente `data/products.js` sanitizado y clasificado por sector y rubro.
