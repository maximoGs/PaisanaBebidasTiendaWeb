# Paisana Bebidas - Tienda Online de Vinos de Autor, Cervezas & Bebidas Selectas 🍷🍺

Plataforma e-commerce ultra moderna, rápida y responsive diseñada como **producto final listo para ser vendido y administrado** para vinotecas, cervecerías artesanales y tiendas de bebidas.

---

## 🎨 Identidad Visual y Diseño (Basado en Emblema Oficial)

- **Paleta de Marca Oficial**:
  - 🌿 **Turquesa Artesanal (Teal)**: `#3ca1a4` / `#58c6c9`
  - 🌾 **Oro Mostaza Cálido**: `#e5aa38` / `#f6be4e`
  - 🍷 **Borgoña & Lúpulo Tostado**: `#582029` / `#7b2a37`
  - 🌑 **Obsidian Slate**: `#0c1017` / `#151e2b`
- **Logo Vectorial Integrado**: Badge circular artesanal con flor de lúpulo, doble anillo y tipografía serif estilizada (`assets/logo.svg`).
- **Experiencia de Usuario**:
  - Glassmorphism, micro-animaciones y tipografía editorial (*Cinzel* y *Plus Jakarta Sans*).
  - Experiencia móvil nativa (Mobile-First) con *Bottom Nav Bar* y Drawer lateral táctil.
  
---

## 🌟 Características Principales del Producto

- **Estructura de Catálogo por Pestañas y Varietales**:
  - 🍷 **Vinos**: *Malbec, Cabernet Sauvignon, Blends, Blancos & Chardonnay, Rosados, Espumantes*.
  - 🍺 **Cervezas & Destilados**: *Cervezas & Lúpulos Artesanales (Session IPA, Bohemian, Roja), Fernet & Aperitivos, Gin Premium, Vodka, Whisky*.
  - 🥤 **Bebidas sin Alcohol**: *Gaseosas, Tónicas & Mixers, Energizantes, Aguas y Jugos*.
  - 🍿 **Snacks y Varios**: *Combos Previa, Snacks Salados, Chocolates / Dulces, Hielo & Descartables*.

- **Comercio & Carrito Inteligente**:
  - Buscador predictivo en tiempo real.
  - Ordenamiento dinámico por menor/mayor precio, destacados y orden alfabético.
  - Ficha modal de producto con notas de cata, maridaje sugerido, origen y graduación alcohólica.
  - Carrito persistente con `localStorage` y cálculo transparente de cadetería / retiro en local.
  - Conmutador de visualización entre **Grilla Compacta** (alta densidad) y **Lista Ordenada** (formato carta/menú horizontal).
  - **Checkout Desacoplado por WhatsApp**: Genera automáticamente solicitudes de cotización estructuradas con código de referencia (`#COT-XXXXX`).

- **Cumplimiento Normativo Local (Argentina)**:
  - 🛡️ Control de acceso (+18) según **Ley Nacional N° 24.788**.
  - 🔄 **Botón de Arrepentimiento** con generación de código de trámite según **Res. 424/2020 & Ley 24.240**.
  - 🔒 Política de privacidad y tratamiento de datos efímero en cliente conforme a la **Ley 25.326**.
  - ⚖️ Enlaces institucionales a Defensa de las y los Consumidores (**Res. 271/2020**).

---

## 🚀 Despliegue en Cloudflare Pages ($0 ARS)

El repositorio está optimizado con archivos `_headers` y `_redirects` para **Cloudflare Pages**:
1. Conectar este repositorio en el panel de **Cloudflare Pages**.
2. Configurar salida en `/` (raíz) sin comando de build.
3. Despliegue automático instantáneo con CDN ultra rápida en Argentina y ancho de banda sin límites.

Para ver el instructivo paso a paso de administración y venta, consultar [`CLOUDFLARE_ADMIN_GUIA.md`](file:///c:/Users/Usuario/Desktop/TiendaPlantilla/CLOUDFLARE_ADMIN_GUIA.md).


