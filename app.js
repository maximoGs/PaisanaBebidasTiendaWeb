/**
 * PAISANA BEBIDAS - MOTOR DE CATÁLOGO SECTORIZADO POR RUBROS Y COMERCIO
 * Sincronizado con Inventario 3.0 Sanitizado (7 Sectores • 34 Rubros)
 */

// ==========================================================================
// CONFIGURACIÓN GENERAL DE LA TIENDA
// ==========================================================================
const STORE_CONFIG = {
  whatsappNumber: "5492612586004", // +54 9 2612 58-6004
  whatsappDisplay: "+54 9 2612 58-6004",
  deliveryFee: 2500,
  storeName: "Paisana Bebidas",
  storeAddress: "C. Tapón Moyano 1745, M5523 Mendoza",
  mapsUrl: "https://maps.app.goo.gl/JSEvWcQvFY8zpxcH9",
  bodegaAmigaNumber: "5492617094195" // Martino Wines (reservas experiencia en finca)
};

// ==========================================================================
// ARQUITECTURA DE 7 SECTORES Y SUB-RUBROS
// ==========================================================================
const SUBCATEGORIES_MAP = {
  tintos: {
    title: "Vinos Tintos",
    icon: "fa-solid fa-wine-glass",
    subtitle: "Malbec, Cabernet Sauvignon, Cabernet Franc, varietales de autor, Bag in Box 3L y Damajuanas",
    subchips: [
      { id: "all", label: "🍷 Todos los Tintos" },
      { id: "malbec", label: "🍇 Malbec" },
      { id: "cabernet-sauvignon", label: "🍷 Cabernet Sauvignon" },
      { id: "cabernet-franc", label: "🌿 Cabernet Franc" },
      { id: "otros-tintos", label: "🍒 Bonarda, Merlot, Pinot & Más" },
      { id: "blends", label: "✨ Blends & Cortes" },
      { id: "bag-in-box", label: "📦 Bag in Box 3L" },
      { id: "damajuanas-375", label: "🍶 Damajuanas & 375ml" }
    ]
  },
  blancos: {
    title: "Blancos, Dulces & Espumantes",
    icon: "fa-solid fa-champagne-glasses",
    subtitle: "Chardonnay, Sauvignon Blanc, Pedro Ximénez, dulces naturales, rosados y espumantes Extra Brut",
    subchips: [
      { id: "all", label: "🥂 Todos" },
      { id: "vinos-blancos", label: "🥂 Vinos Blancos" },
      { id: "espumantes", label: "🍾 Espumantes" },
      { id: "vinos-dulces", label: "🍯 Vinos Dulces" },
      { id: "vinos-rosados", label: "🌸 Vinos Rosados" }
    ]
  },
  combos: {
    title: "Combos & Promos",
    icon: "fa-solid fa-fire",
    subtitle: "Packs armados para previas, juntadas y meriendas con ahorro especial",
    subchips: [
      { id: "all", label: "🔥 Todos los Combos" },
      { id: "combos-fernet", label: "🦅 Fernet + Coca" },
      { id: "combos-vodka", label: "🧊 Vodka + Sprite" },
      { id: "combos-aperitivos", label: "🍊 Aperitivos & Spritz" },
      { id: "combos-ron", label: "🥃 Ron + Coca" },
      { id: "combos-gin", label: "🌿 Gin + Tónica" },
      { id: "combos-cafe", label: "☕ Café + Alfajor" }
    ]
  },
  bebidas: {
    title: "Cervezas & Destilados",
    icon: "fa-solid fa-beer-mug-empty",
    subtitle: "Cervezas frías, fernet, aperitivos, vermouth, gin, vodka, whisky, ron, RTD y licores",
    subchips: [
      { id: "all", label: "🍺 Todo Cervezas & Destilados" },
      { id: "cervezas", label: "🍺 Cervezas" },
      { id: "fernet", label: "🦅 Fernet" },
      { id: "aperitivos", label: "🍊 Aperitivos" },
      { id: "vermouth", label: "🍷 Vermouth" },
      { id: "gin", label: "🌿 Gin" },
      { id: "vodka", label: "🧊 Vodka" },
      { id: "whisky", label: "🥃 Whisky" },
      { id: "ron", label: "🏴‍☠️ Ron" },
      { id: "rtd", label: "🥫 Ready to Drink" },
      { id: "otros-destilados", label: "🧪 Licores & Miniaturas" }
    ]
  },
  "sin-alcohol": {
    title: "Bebidas sin Alcohol",
    icon: "fa-solid fa-bottle-water",
    subtitle: "Gaseosas, tónicas y mixers, jugos, isotónicas, energizantes, aguas y línea 0.0% alcohol",
    subchips: [
      { id: "all", label: "🥤 Todo Sin Alcohol" },
      { id: "gaseosas", label: "🥤 Gaseosas" },
      { id: "tonicas-mixers", label: "🫧 Tónicas, Pomelos & Sodas" },
      { id: "jugos-aguas-sab", label: "🍊 Jugos, Terma & Saborizadas" },
      { id: "isotonicas", label: "🏃 Isotónicas (Gatorade)" },
      { id: "energizantes", label: "⚡ Energizantes" },
      { id: "aguas", label: "💧 Aguas & Kombucha" },
      { id: "sin-alcohol-00", label: "🍺 Cervezas & Vinos 0.0%" }
    ]
  },
  snacks: {
    title: "Café, Snacks & Gourmet",
    icon: "fa-solid fa-mug-hot",
    subtitle: "Café de especialidad en grano y molido, snacks salados, alfajores Entre Dos, chocolates, oliva y conservas",
    subchips: [
      { id: "all", label: "☕ Todo Café, Snacks & Gourmet" },
      { id: "cafe", label: "☕ Café en Grano & Molido" },
      { id: "snacks-salados", label: "🥨 Snacks Salados & Aceitunas" },
      { id: "chocolates-alfajores", label: "🍫 Alfajores, Chocolates & Dulces" },
      { id: "regionales-cocteleria", label: "🫒 Aceites, Conservas & Coctelería" }
    ]
  },
  varios: {
    title: "Hielo, Tabaco & Regalos",
    icon: "fa-solid fa-cubes-stacked",
    subtitle: "Bolsas de hielo, leña, tabaquería y papelillos, sets de asador, cajas de regalo y sacacorchos",
    subchips: [
      { id: "all", label: "🧊 Todo Hielo, Tabaco & Varios" },
      { id: "hielo-lena", label: "🧊 Hielo & Leña" },
      { id: "cigarrillos-cigarros", label: "🚬 Cigarrillos, Cigarros & Vapers" },
      { id: "tabacos-papelillos", label: "🍂 Tabacos, Sedas & Encendedores" },
      { id: "regalos", label: "🎁 Regalería & Sets Asador" },
      { id: "descartables-accesorios", label: "🍾 Sacacorchos, Cajas & Sorbetes" }
    ]
  }
};

// Iconos amigables para los 34 rubros oficiales del inventario
const RUBRO_ICONS = {
  "VINOS TINTOS": "fa-solid fa-wine-glass",
  "BAG IN BOX": "fa-solid fa-box-open",
  "DAMAJUANAS": "fa-solid fa-wine-bottle",
  "VINOS 375 ML": "fa-solid fa-wine-bottle",
  "VINOS BLANCOS": "fa-solid fa-wine-glass-empty",
  "ESPUMANTES": "fa-solid fa-champagne-glasses",
  "VINOS DULCES": "fa-solid fa-droplet",
  "VINOS ROSADOS": "fa-solid fa-seedling",
  "COMBOS": "fa-solid fa-fire",
  "CERVEZAS": "fa-solid fa-beer-mug-empty",
  "FERNET": "fa-solid fa-bottle-droplet",
  "APERITIVOS": "fa-solid fa-martini-glass-citrus",
  "VERMOUTH": "fa-solid fa-martini-glass",
  "GIN": "fa-solid fa-leaf",
  "VODKA": "fa-solid fa-snowflake",
  "WHISKY": "fa-solid fa-whiskey-glass",
  "RON": "fa-solid fa-anchor",
  "READY TO DRINK": "fa-solid fa-bolt",
  "OTRAS BEBIDAS BLANCAS Y DESTILADOS": "fa-solid fa-flask",
  "MINIATURAS": "fa-solid fa-vial",
  "GASEOSAS": "fa-solid fa-glass-water",
  "JUGOS Y AGUAS SABORIZADAS": "fa-solid fa-lemon",
  "ENERGIZANTES": "fa-solid fa-bolt-lightning",
  "AGUAS Y SODAS": "fa-solid fa-bottle-water",
  "CERVEZAS SIN ALCOHOL": "fa-solid fa-circle-check",
  "VINOS SIN ALCOHOL": "fa-solid fa-circle-check",
  "CAFE": "fa-solid fa-mug-hot",
  "SNACKS": "fa-solid fa-bowl-food",
  "CONSERVAS Y ACEITES": "fa-solid fa-jar",
  "HIELOS": "fa-solid fa-icicles",
  "LEÑA": "fa-solid fa-fire-flame-curved",
  "CIGARRILLO, TABACO Y MAS": "fa-solid fa-smoking",
  "REGALOS": "fa-solid fa-gift",
  "DESCARTABLES": "fa-solid fa-utensils"
};

// ==========================================================================
// ESTADO GLOBAL DE LA APLICACIÓN
// ==========================================================================
const AppState = {
  currentCategory: "tintos",
  currentSubcategory: "all",
  currentRubro: null, // Filtro directo por Rubro oficial del Excel cuando se elige en el Índice
  searchQuery: "",
  rawSearchInput: "",
  currentSort: "default",
  cart: [],
  deliveryMethod: "envio",
  viewMode: localStorage.getItem("paisana_view_mode") || "grid"
};

// Pre-indexar texto normalizado de cada producto para búsquedas instantáneas sin tildes
function normalizeText(str) {
  if (!str) return "";
  return String(str)
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9.\s+]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function prepareProductsSearchIndex() {
  if (typeof PRODUCTS_DATA === "undefined" || !Array.isArray(PRODUCTS_DATA)) return;
  PRODUCTS_DATA.forEach((p) => {
    p._searchBlob = normalizeText(
      `${p.name} ${p.rubro || ""} ${p.subcategoryLabel || ""} ${p.subcategory || ""} ${p.origin || ""} ${p.volume || ""} ${p.description || ""}`
    );
  });
}

// ==========================================================================
// INICIALIZACIÓN
// ==========================================================================
document.addEventListener("DOMContentLoaded", () => {
  prepareProductsSearchIndex();
  initAgeGate();
  loadCartFromStorage();
  updateCategoryTabCounts();
  setupEventListeners();
  renderSubcategoryChips();
  renderProducts();
  updateCartUI();
  initPromoCarousel();
  initEventsCalendar();
});

// ==========================================================================
// CONTROL DE BLOQUEO DE SCROLL EN MODALES / DRAWER
// ==========================================================================
function syncBodyScrollLock() {
  const anyModalOpen = document.querySelector(".modal-backdrop.active") !== null;
  const cartOpen = document.getElementById("cartDrawer")?.classList.contains("active");
  document.body.style.overflow = anyModalOpen || cartOpen ? "hidden" : "";
}

// ==========================================================================
// CONTROL DE EDAD (+18)
// ==========================================================================
function initAgeGate() {
  const isVerified = sessionStorage.getItem("paisana_age_verified");
  const ageModal = document.getElementById("ageGateModal");
  const confirmBtn = document.getElementById("confirmAgeBtn");

  if (!isVerified && ageModal) {
    ageModal.classList.add("active");
    syncBodyScrollLock();
  }

  if (confirmBtn && ageModal) {
    confirmBtn.addEventListener("click", () => {
      sessionStorage.setItem("paisana_age_verified", "true");
      ageModal.classList.remove("active");
      syncBodyScrollLock();
      showToast("Acceso verificado: Mayor de 18 años");
    });
  }
}

// ==========================================================================
// CONTEO DINÁMICO DE PRODUCTOS POR SECTOR Y SUB-RUBRO
// ==========================================================================
function updateCategoryTabCounts() {
  const counts = {};
  Object.keys(SUBCATEGORIES_MAP).forEach((k) => {
    counts[k] = 0;
  });

  PRODUCTS_DATA.forEach((p) => {
    if (counts[p.category] !== undefined) {
      counts[p.category]++;
    }
  });

  document.querySelectorAll("[data-count-cat]").forEach((el) => {
    const cat = el.getAttribute("data-count-cat");
    if (counts[cat] !== undefined) {
      el.textContent = counts[cat];
    }
  });
}

function getSubcategoryCount(categoryKey, subcatId) {
  if (subcatId === "all") {
    return PRODUCTS_DATA.filter((p) => p.category === categoryKey).length;
  }
  return PRODUCTS_DATA.filter(
    (p) => p.category === categoryKey && p.subcategory === subcatId
  ).length;
}

// ==========================================================================
// CONFIGURACIÓN DE LISTENERS
// ==========================================================================
function setupEventListeners() {
  // Pestañas principales de categoría
  document.querySelectorAll(".category-tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const cat = btn.getAttribute("data-category");
      switchCategory(cat);
    });
  });

  // Buscador Desktop
  const desktopInput = document.getElementById("desktopSearchInput");
  const desktopClear = document.getElementById("desktopSearchClear");
  if (desktopInput) {
    desktopInput.addEventListener("input", (e) => {
      handleSearch(e.target.value);
      syncSearchInputs(e.target.value, "desktop");
    });
  }
  if (desktopClear) {
    desktopClear.addEventListener("click", () => {
      handleSearch("");
      syncSearchInputs("", "none");
    });
  }

  // Buscador Móvil
  const mobileInput = document.getElementById("mobileSearchInput");
  const mobileClear = document.getElementById("mobileSearchClear");
  if (mobileInput) {
    mobileInput.addEventListener("input", (e) => {
      handleSearch(e.target.value);
      syncSearchInputs(e.target.value, "mobile");
    });
  }
  if (mobileClear) {
    mobileClear.addEventListener("click", () => {
      handleSearch("");
      syncSearchInputs("", "none");
    });
  }

  // Ordenamiento
  const sortSelect = document.getElementById("sortSelect");
  if (sortSelect) {
    sortSelect.addEventListener("change", (e) => {
      AppState.currentSort = e.target.value;
      renderProducts();
    });
  }

  // Conmutador de vista (Grid vs List)
  const viewGridBtn = document.getElementById("viewGridBtn");
  const viewListBtn = document.getElementById("viewListBtn");
  if (viewGridBtn) viewGridBtn.addEventListener("click", () => setViewMode("grid"));
  if (viewListBtn) viewListBtn.addEventListener("click", () => setViewMode("list"));
  applyViewModeUI();

  // Botones de Índice de Rubros
  const openRubrosHeaderBtn = document.getElementById("openRubrosHeaderBtn");
  const openRubrosCatalogBtn = document.getElementById("openRubrosCatalogBtn");
  const closeRubrosModalBtn = document.getElementById("closeRubrosModalBtn");
  const rubrosModal = document.getElementById("rubrosModal");

  if (openRubrosHeaderBtn) openRubrosHeaderBtn.addEventListener("click", openRubrosModal);
  if (openRubrosCatalogBtn) openRubrosCatalogBtn.addEventListener("click", openRubrosModal);
  if (closeRubrosModalBtn) closeRubrosModalBtn.addEventListener("click", closeRubrosModal);
  if (rubrosModal) {
    rubrosModal.addEventListener("click", (e) => {
      if (e.target === rubrosModal) closeRubrosModal();
    });
  }

  // Carrito Drawer Trigger (Desktop & Mobile)
  const desktopCartBtn = document.getElementById("desktopCartBtn");
  const mobileCartBtn = document.getElementById("mobileCartBtn");
  const closeCartBtn = document.getElementById("closeCartBtn");
  const cartBackdrop = document.getElementById("cartBackdrop");
  const clearCartBtn = document.getElementById("clearCartBtn");

  if (desktopCartBtn) desktopCartBtn.addEventListener("click", openCart);
  if (mobileCartBtn) mobileCartBtn.addEventListener("click", openCart);
  if (closeCartBtn) closeCartBtn.addEventListener("click", closeCart);
  if (cartBackdrop) cartBackdrop.addEventListener("click", closeCart);
  if (clearCartBtn) {
    clearCartBtn.addEventListener("click", () => {
      clearCart();
      showToast("Carrito vaciado");
    });
  }

  // Modal Detalle de Producto
  const productModal = document.getElementById("productModal");
  const closeProductModalBtn = document.getElementById("closeProductModalBtn");
  if (closeProductModalBtn) closeProductModalBtn.addEventListener("click", closeProductModal);
  if (productModal) {
    productModal.addEventListener("click", (e) => {
      if (e.target === productModal) closeProductModal();
    });
  }

  // Modal Checkout
  const openCheckoutModalBtn = document.getElementById("openCheckoutModalBtn");
  const closeCheckoutModalBtn = document.getElementById("closeCheckoutModalBtn");
  const checkoutModal = document.getElementById("checkoutModal");
  const checkoutForm = document.getElementById("checkoutForm");

  if (openCheckoutModalBtn) {
    openCheckoutModalBtn.addEventListener("click", () => {
      if (AppState.cart.length === 0) {
        showToast("Tu carrito está vacío 🛒");
        return;
      }
      closeCart();
      openCheckoutModal();
    });
  }
  if (closeCheckoutModalBtn) closeCheckoutModalBtn.addEventListener("click", closeCheckoutModal);
  if (checkoutModal) {
    checkoutModal.addEventListener("click", (e) => {
      if (e.target === checkoutModal) closeCheckoutModal();
    });
  }
  if (checkoutForm) checkoutForm.addEventListener("submit", handleCheckoutSubmit);

  // Modal Botón de Arrepentimiento (Res. 424/2020)
  const openRegretBtn = document.getElementById("openRegretBtn");
  const closeRegretModalBtn = document.getElementById("closeRegretModalBtn");
  const regretModal = document.getElementById("regretModal");
  const regretForm = document.getElementById("regretForm");

  if (openRegretBtn) openRegretBtn.addEventListener("click", openRegretModal);
  if (closeRegretModalBtn) closeRegretModalBtn.addEventListener("click", closeRegretModal);
  if (regretModal) {
    regretModal.addEventListener("click", (e) => {
      if (e.target === regretModal) closeRegretModal();
    });
  }
  if (regretForm) regretForm.addEventListener("submit", handleRegretSubmit);

  // Modal Términos y Privacidad (Ley 25.326)
  const openPrivacyBtn = document.getElementById("openPrivacyBtn");
  const closePrivacyModalBtn = document.getElementById("closePrivacyModalBtn");
  const privacyModal = document.getElementById("privacyModal");

  if (openPrivacyBtn) openPrivacyBtn.addEventListener("click", openPrivacyModal);
  if (closePrivacyModalBtn) closePrivacyModalBtn.addEventListener("click", closePrivacyModal);
  if (privacyModal) {
    privacyModal.addEventListener("click", (e) => {
      if (e.target === privacyModal) closePrivacyModal();
    });
  }

  // Botón Volver Arriba & Header Scroll
  const backToTopBtn = document.getElementById("backToTopBtn");
  if (backToTopBtn) {
    backToTopBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  window.addEventListener("scroll", () => {
    const header = document.getElementById("mainHeader");
    if (header) {
      header.classList.toggle("scrolled", window.scrollY > 30);
    }
    if (backToTopBtn) {
      backToTopBtn.classList.toggle("visible", window.scrollY > 520);
    }
  });

  // Cerrar modales / carrito con tecla Escape (excepto control de edad +18)
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    const ageGate = document.getElementById("ageGateModal");
    if (ageGate && ageGate.classList.contains("active")) return;

    closeProductModal();
    closeRubrosModal();
    closeCheckoutModal();
    closeRegretModal();
    closePrivacyModal();
    closeCart();
  });
}

// ==========================================================================
// BÚSQUEDA INTELIGENTE (SIN TILDES Y MULTI-PALABRA)
// ==========================================================================
function syncSearchInputs(value, source) {
  const desktopInput = document.getElementById("desktopSearchInput");
  const mobileInput = document.getElementById("mobileSearchInput");
  const desktopClear = document.getElementById("desktopSearchClear");
  const mobileClear = document.getElementById("mobileSearchClear");

  if (source !== "desktop" && desktopInput) desktopInput.value = value;
  if (source !== "mobile" && mobileInput) mobileInput.value = value;

  if (desktopClear) desktopClear.style.display = value ? "block" : "none";
  if (mobileClear) mobileClear.style.display = value ? "block" : "none";
}

function handleSearch(query) {
  AppState.rawSearchInput = query.trim();
  AppState.searchQuery = normalizeText(query);
  renderProducts();
}

// ==========================================================================
// CAMBIO DE SECTORES, SUB-RUBROS E ÍNDICE COMPLETO DE RUBROS
// ==========================================================================
function switchCategory(categoryKey, options = {}) {
  if (categoryKey === "vinos") categoryKey = "tintos";
  if (!SUBCATEGORIES_MAP[categoryKey]) return;

  AppState.currentCategory = categoryKey;
  AppState.currentSubcategory = options.subcategory || "all";
  AppState.currentRubro = options.rubro || null;

  if (!options.preserveSearch && AppState.searchQuery) {
    AppState.searchQuery = "";
    AppState.rawSearchInput = "";
    syncSearchInputs("", "none");
  }

  // Actualizar Tabs Header y centrar la pestaña activa en vista móvil/tablet
  document.querySelectorAll(".category-tab-btn").forEach((btn) => {
    const isActive = btn.getAttribute("data-category") === categoryKey;
    btn.classList.toggle("active", isActive);
    if (isActive && typeof btn.scrollIntoView === "function") {
      btn.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
    }
  });

  // Actualizar Bottom Nav Móvil
  document.querySelectorAll(".bottom-nav-item").forEach((btn) => {
    btn.classList.remove("active");
  });
  const navKey = categoryKey === "blancos" ? "tintos" : categoryKey;
  const activeBnav = document.getElementById(`bnav-${navKey}`);
  if (activeBnav) {
    activeBnav.classList.add("active");
  } else {
    const rubrosBnav = document.getElementById("bnav-rubros");
    if (rubrosBnav) rubrosBnav.classList.add("active");
  }

  // Actualizar Títulos de Sección
  const meta = SUBCATEGORIES_MAP[categoryKey];
  const titleEl = document.getElementById("currentSectionTitle");
  const subEl = document.getElementById("currentSectionSubtitle");
  if (titleEl) {
    titleEl.innerHTML = `<i class="${meta.icon}" style="color: var(--gold-primary);"></i> ${escapeHTML(meta.title)}`;
  }
  if (subEl) {
    subEl.textContent = meta.subtitle;
  }

  renderSubcategoryChips();
  renderProducts();

  if (options.scrollToCatalog || window.scrollY > 300) {
    const catalogoEl = document.getElementById("catalogo");
    if (catalogoEl) catalogoEl.scrollIntoView({ behavior: "smooth" });
  }
}

function filterBySubcategory(subcatId) {
  AppState.currentSubcategory = subcatId;
  AppState.currentRubro = null;

  document.querySelectorAll(".subchip-btn").forEach((chip) => {
    chip.classList.toggle("active", chip.getAttribute("data-subcat") === subcatId);
  });

  renderProducts();
}

function filterByExactRubro(rubroName, targetCategory = null) {
  closeRubrosModal();
  closeProductModal();

  // Determinar el sector principal más representativo para ese rubro si no fue provisto
  let cat = targetCategory;
  if (!cat) {
    const sample = PRODUCTS_DATA.find((p) => p.rubro === rubroName);
    cat = sample ? sample.category : AppState.currentCategory;
  }

  AppState.searchQuery = "";
  AppState.rawSearchInput = "";
  syncSearchInputs("", "none");

  switchCategory(cat, {
    subcategory: "all",
    rubro: rubroName,
    scrollToCatalog: true
  });
}

function clearActiveRubroOrSearch() {
  AppState.currentRubro = null;
  AppState.searchQuery = "";
  AppState.rawSearchInput = "";
  syncSearchInputs("", "none");
  renderSubcategoryChips();
  renderProducts();
}

function filterByPromoCombos() {
  switchCategory("combos", { scrollToCatalog: true });
}

function filterMartinoWines() {
  AppState.currentRubro = null;
  AppState.rawSearchInput = "Martino";
  AppState.searchQuery = "martino";
  syncSearchInputs("Martino", "none");
  renderProducts();
  const catEl = document.getElementById("catalogo");
  if (catEl) catEl.scrollIntoView({ behavior: "smooth" });
  showToast("Mostrando las 8 etiquetas de Bodega Martino 🍷");
}

function addComboToCart(identifier) {
  const raw = String(identifier || "").trim();
  const normId = normalizeText(raw);

  const product = PRODUCTS_DATA.find((p) => {
    if (p.id === raw || p.code === raw) return true;
    const pNorm = normalizeText(p.name);
    return pNorm === normId || pNorm.includes(normId);
  });

  if (product) {
    addToCart(product.id, 1);
    openCart();
  } else {
    filterByPromoCombos();
  }
}

function consultProduct(productId) {
  const product = PRODUCTS_DATA.find((p) => p.id === productId);
  if (!product) return;
  const msg = `Hola Paisana Bebidas! Quería consultar disponibilidad y precio de: ${product.name} (${product.volume || "Unidad"}).`;
  const url = `https://wa.me/${STORE_CONFIG.whatsappNumber}?text=${encodeURIComponent(msg)}`;
  window.open(url, "_blank");
}

// ==========================================================================
// MODAL: ÍNDICE INTERACTIVO DE LOS 34 RUBROS DEL INVENTARIO
// ==========================================================================
function openRubrosModal() {
  const modal = document.getElementById("rubrosModal");
  const body = document.getElementById("rubrosDirectoryBody");
  if (!modal || !body) return;

  // Agrupar rubros reales dentro de cada uno de los 7 sectores (y también conteo global por rubro)
  const totalRubroCounts = {};
  const sectorRubrosMap = {};
  Object.keys(SUBCATEGORIES_MAP).forEach((k) => {
    sectorRubrosMap[k] = new Map();
  });

  PRODUCTS_DATA.forEach((p) => {
    const r = p.rubro || "VARIOS";
    totalRubroCounts[r] = (totalRubroCounts[r] || 0) + 1;
    if (sectorRubrosMap[p.category]) {
      const m = sectorRubrosMap[p.category];
      m.set(r, (m.get(r) || 0) + 1);
    }
  });

  body.innerHTML = Object.entries(SUBCATEGORIES_MAP)
    .map(([catKey, meta]) => {
      const catTotal = PRODUCTS_DATA.filter((p) => p.category === catKey).length;
      const rubrosEntries = Array.from(sectorRubrosMap[catKey].entries()).sort(
        (a, b) => b[1] - a[1]
      );

      const rubrosHtml = rubrosEntries
        .map(([rubroName, countInCat]) => {
          const totalForRubro = totalRubroCounts[rubroName] || countInCat;
          const iconClass = RUBRO_ICONS[rubroName] || "fa-solid fa-tag";
          const safeRubroAttr = escapeHTML(rubroName).replace(/'/g, "\\'");
          const isCurrent = AppState.currentRubro === rubroName;
          return `
            <button class="rubro-dir-btn ${isCurrent ? "active" : ""}" onclick="filterByExactRubro('${safeRubroAttr}', '${catKey}')">
              <i class="${iconClass}"></i>
              <span class="rubro-dir-name">${escapeHTML(rubroName)}</span>
              <span class="rubro-dir-count">${totalForRubro}</span>
            </button>
          `;
        })
        .join("");

      return `
        <div class="rubros-sector-group">
          <div class="rubros-sector-header">
            <div class="rubros-sector-title">
              <i class="${meta.icon}"></i>
              <strong>${escapeHTML(meta.title)}</strong>
              <span class="rubros-sector-badge">${catTotal} prod.</span>
            </div>
            <button class="rubros-sector-jump" onclick="closeRubrosModal(); switchCategory('${catKey}', { scrollToCatalog: true });">
              Ver sector <i class="fa-solid fa-arrow-right"></i>
            </button>
          </div>
          <div class="rubros-chips-grid">
            ${rubrosHtml}
          </div>
        </div>
      `;
    })
    .join("");

  modal.classList.add("active");
  syncBodyScrollLock();
}

function closeRubrosModal() {
  const modal = document.getElementById("rubrosModal");
  if (modal) modal.classList.remove("active");
  syncBodyScrollLock();
}

// ==========================================================================
// CARRUSEL PROMOCIONAL
// ==========================================================================
function initPromoCarousel() {
  const wrapper = document.getElementById("promoCarouselWrapper");
  const slides = document.querySelectorAll(".carousel-slide");
  const dots = document.querySelectorAll(".carousel-dot");
  const counter = document.getElementById("carouselCounterBadge");
  const prevBtn = document.getElementById("carouselPrevBtn");
  const nextBtn = document.getElementById("carouselNextBtn");

  if (!slides || slides.length === 0) return;

  let currentSlide = 0;
  const totalSlides = slides.length;
  let autoPlayTimer = null;
  const slideDuration = 6500;

  function goToSlide(index) {
    currentSlide = (index + totalSlides) % totalSlides;
    slides.forEach((slide, i) => slide.classList.toggle("active", i === currentSlide));
    dots.forEach((dot, i) => dot.classList.toggle("active", i === currentSlide));
    if (counter) counter.textContent = `${currentSlide + 1} / ${totalSlides}`;
  }

  function nextSlide() {
    goToSlide(currentSlide + 1);
  }

  function prevSlide() {
    goToSlide(currentSlide - 1);
  }

  function startAutoPlay() {
    stopAutoPlay();
    autoPlayTimer = setInterval(nextSlide, slideDuration);
  }

  function stopAutoPlay() {
    if (autoPlayTimer) {
      clearInterval(autoPlayTimer);
      autoPlayTimer = null;
    }
  }

  if (prevBtn) {
    prevBtn.addEventListener("click", () => {
      prevSlide();
      startAutoPlay();
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      nextSlide();
      startAutoPlay();
    });
  }

  dots.forEach((dot) => {
    dot.addEventListener("click", () => {
      const targetIdx = parseInt(dot.getAttribute("data-slide-to"), 10);
      if (!isNaN(targetIdx)) {
        goToSlide(targetIdx);
        startAutoPlay();
      }
    });
  });

  if (wrapper) {
    wrapper.addEventListener("mouseenter", stopAutoPlay);
    wrapper.addEventListener("mouseleave", startAutoPlay);

    let touchStartX = 0;
    wrapper.addEventListener(
      "touchstart",
      (e) => {
        if (e.changedTouches && e.changedTouches[0]) {
          touchStartX = e.changedTouches[0].screenX;
        }
        stopAutoPlay();
      },
      { passive: true }
    );

    wrapper.addEventListener(
      "touchend",
      (e) => {
        if (e.changedTouches && e.changedTouches[0]) {
          const diff = e.changedTouches[0].screenX - touchStartX;
          if (Math.abs(diff) > 40) {
            if (diff < 0) nextSlide();
            else prevSlide();
          }
        }
        startAutoPlay();
      },
      { passive: true }
    );
  }

  goToSlide(0);
  startAutoPlay();
}

// ==========================================================================
// RENDERIZADO DE SUB-CHIPS CON CONTEO EN VIVO
// ==========================================================================
function renderSubcategoryChips() {
  const container = document.getElementById("subcategoryChips");
  if (!container) return;

  const currentMap = SUBCATEGORIES_MAP[AppState.currentCategory];
  if (!currentMap) return;

  container.innerHTML = currentMap.subchips
    .map((chip) => {
      const count = getSubcategoryCount(AppState.currentCategory, chip.id);
      if (chip.id !== "all" && count === 0) return "";
      const isActive = !AppState.currentRubro && AppState.currentSubcategory === chip.id;
      return `
        <button class="subchip-btn ${isActive ? "active" : ""}" 
                data-subcat="${chip.id}" 
                onclick="filterBySubcategory('${chip.id}')">
          <span>${chip.label}</span>
          <span class="subchip-count">${count}</span>
        </button>
      `;
    })
    .join("");
}

// ==========================================================================
// RENDERIZADO DE PRODUCTOS Y FILTROS
// ==========================================================================
function renderActiveFilterBar(resultCount) {
  const bar = document.getElementById("activeFilterBar");
  if (!bar) return;

  if (AppState.searchQuery) {
    bar.style.display = "flex";
    bar.innerHTML = `
      <div class="active-filter-info">
        <i class="fa-solid fa-magnifying-glass"></i>
        <span>Búsqueda en todo el catálogo: <strong>"${escapeHTML(AppState.rawSearchInput)}"</strong> (${resultCount} resultado${resultCount !== 1 ? "s" : ""})</span>
      </div>
      <button class="active-filter-clear" onclick="clearActiveRubroOrSearch()">
        <i class="fa-solid fa-xmark"></i> Limpiar búsqueda
      </button>
    `;
  } else if (AppState.currentRubro) {
    bar.style.display = "flex";
    bar.innerHTML = `
      <div class="active-filter-info">
        <i class="fa-solid fa-tag"></i>
        <span>Rubro seleccionado: <strong>${escapeHTML(AppState.currentRubro)}</strong> (${resultCount} producto${resultCount !== 1 ? "s" : ""})</span>
      </div>
      <button class="active-filter-clear" onclick="clearActiveRubroOrSearch()">
        <i class="fa-solid fa-xmark"></i> Ver todo el sector
      </button>
    `;
  } else {
    bar.style.display = "none";
    bar.innerHTML = "";
  }
}

function getCartQtyForProduct(productId) {
  const found = AppState.cart.find((i) => i.id === productId);
  return found ? found.quantity : 0;
}

function renderProducts() {
  const grid = document.getElementById("productsGrid");
  const countEl = document.getElementById("itemsCount");
  if (!grid) return;

  const queryTokens = AppState.searchQuery ? AppState.searchQuery.split(" ").filter(Boolean) : [];

  // Filtrado
  const filtered = PRODUCTS_DATA.filter((item) => {
    // 1. Búsqueda global multi-palabra sin tildes en todo el catálogo
    if (queryTokens.length > 0) {
      const blob = item._searchBlob || "";
      return queryTokens.every((tok) => blob.includes(tok));
    }

    // 2. Filtro directo por Rubro oficial del inventario
    if (AppState.currentRubro) {
      return item.rubro === AppState.currentRubro;
    }

    // 3. Filtro por sector principal y sub-rubro
    if (item.category !== AppState.currentCategory) return false;
    if (AppState.currentSubcategory !== "all" && item.subcategory !== AppState.currentSubcategory) {
      return false;
    }
    return true;
  });

  // Ordenamiento (en "default" prioriza fotos reales / destacados sutilmente o mantiene orden curado)
  if (AppState.currentSort === "price-asc") {
    filtered.sort((a, b) => (a.price || 9999999) - (b.price || 9999999));
  } else if (AppState.currentSort === "price-desc") {
    filtered.sort((a, b) => (b.price || 0) - (a.price || 0));
  } else if (AppState.currentSort === "name-asc") {
    filtered.sort((a, b) => a.name.localeCompare(b.name, "es"));
  } else {
    // En Destacados: Bodega Amiga y productos con fotografía propia primero, luego alfabético
    filtered.sort((a, b) => {
      const scoreA = (a.badge === "Bodega Amiga" ? 4 : 0) + (a.image.startsWith("FotosDeProductos/") ? 2 : 0) + (a.price > 0 ? 1 : 0);
      const scoreB = (b.badge === "Bodega Amiga" ? 4 : 0) + (b.image.startsWith("FotosDeProductos/") ? 2 : 0) + (b.price > 0 ? 1 : 0);
      if (scoreB !== scoreA) return scoreB - scoreA;
      return a.name.localeCompare(b.name, "es");
    });
  }

  if (countEl) {
    countEl.textContent = `${filtered.length} producto${filtered.length !== 1 ? "s" : ""}`;
  }

  renderActiveFilterBar(filtered.length);

  if (filtered.length === 0) {
    grid.innerHTML = `
      <div class="empty-catalog">
        <i class="fa-solid fa-wine-bottle"></i>
        <h3>No encontramos productos</h3>
        <p>Probá con otro término, revisá el Índice de Rubros o restablecé los filtros.</p>
        <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
          <button class="btn-primary" onclick="resetFilters()">
            <i class="fa-solid fa-arrow-rotate-left"></i> Restablecer filtros
          </button>
          <button class="btn-secondary" onclick="openRubrosModal()">
            <i class="fa-solid fa-layer-group"></i> Ver todos los Rubros
          </button>
        </div>
      </div>
    `;
    return;
  }

  grid.innerHTML = filtered
    .map((product) => {
      const formatPrice = formatMoney(product.price);
      const formatOldPrice = product.oldPrice ? formatMoney(product.oldPrice) : null;
      const inCartQty = getCartQtyForProduct(product.id);

      let badgeHtml = "";
      if (product.badge) {
        const bLower = product.badge.toLowerCase();
        const isOffer = bLower.includes("oferta") || bLower.includes("promo");
        badgeHtml = `<span class="badge-tag ${isOffer ? "offer" : ""}">${escapeHTML(product.badge)}</span>`;
      }

      const tagLabel = product.subcategoryLabel || product.rubro || product.subcategory;
      const isAlcoholicSector = ["tintos", "blancos", "bebidas"].includes(product.category);
      const briefLine = isAlcoholicSector
        ? `${escapeHTML(product.origin)} • ${escapeHTML(product.alcohol)}`
        : `${escapeHTML(product.rubro)} • ${escapeHTML(product.origin)}`;

      let actionHtml = "";
      if (product.price <= 0) {
        actionHtml = `
          <button class="btn-add-cart btn-consultar-wa" onclick="consultProduct('${product.id}')" title="Consultar disponibilidad por WhatsApp" aria-label="Consultar ${escapeHTML(product.name)}">
            <i class="fa-brands fa-whatsapp"></i>
          </button>
        `;
      } else if (inCartQty > 0) {
        actionHtml = `
          <div class="card-qty-stepper" data-stepper-id="${product.id}">
            <button class="card-step-btn" onclick="updateCartQuantity('${product.id}', -1)" aria-label="Quitar una unidad">-</button>
            <span class="card-step-val">${inCartQty}</span>
            <button class="card-step-btn" onclick="updateCartQuantity('${product.id}', 1)" aria-label="Sumar una unidad">+</button>
          </div>
        `;
      } else {
        actionHtml = `
          <button class="btn-add-cart" onclick="addToCart('${product.id}', 1)" title="Agregar al pedido" aria-label="Agregar ${escapeHTML(product.name)}">
            <i class="fa-solid fa-plus"></i>
          </button>
        `;
      }

      return `
      <article class="product-card ${inCartQty > 0 ? "in-cart" : ""}" data-id="${product.id}">
        <div class="product-media" onclick="openProductModal('${product.id}')">
          <img src="${encodeURI(product.image)}" alt="${escapeHTML(product.name)}" class="product-img" loading="lazy" onerror="handleProductImgError(this, '${product.category}')">
          <div class="product-badges-wrap">
            ${badgeHtml}
          </div>
          <button class="quick-view-trigger" title="Ver detalles" aria-label="Ver detalles">
            <i class="fa-solid fa-eye"></i>
          </button>
        </div>

        <div class="product-body">
          <div class="product-info-col">
            <div class="product-meta-row">
              <span class="product-category-tag" title="Rubro: ${escapeHTML(product.rubro)}">${escapeHTML(tagLabel)}</span>
              <span class="product-vol-tag">${escapeHTML(product.volume)}</span>
            </div>

            <h3 class="product-name" onclick="openProductModal('${product.id}')" title="${escapeHTML(product.name)}">
              ${escapeHTML(product.name)}
            </h3>

            <p class="product-details-brief">${briefLine}</p>
          </div>

          <div class="product-footer">
            <div class="price-box">
              ${formatOldPrice ? `<span class="old-price">${formatOldPrice}</span>` : ""}
              <span class="current-price">${formatPrice}</span>
            </div>
            ${actionHtml}
          </div>
        </div>
      </article>
    `;
    })
    .join("");

  applyViewModeUI();
}

function resetFilters() {
  AppState.searchQuery = "";
  AppState.rawSearchInput = "";
  AppState.currentSubcategory = "all";
  AppState.currentRubro = null;
  AppState.currentSort = "default";
  syncSearchInputs("", "none");
  const sortEl = document.getElementById("sortSelect");
  if (sortEl) sortEl.value = "default";
  renderSubcategoryChips();
  renderProducts();
}

// ==========================================================================
// MODAL DE DETALLE DE PRODUCTO
// ==========================================================================
let modalQuantity = 1;

function openProductModal(productId) {
  const product = PRODUCTS_DATA.find((p) => p.id === productId);
  if (!product) return;

  modalQuantity = 1;
  const modalBody = document.getElementById("modalProductBody");
  const modal = document.getElementById("productModal");
  if (!modalBody || !modal) return;

  const formatPrice = formatMoney(product.price);
  const formatOldPrice = product.oldPrice ? formatMoney(product.oldPrice) : null;
  const isLocalPhoto = product.image && product.image.startsWith("FotosDeProductos/");
  const isAlcoholicSector = ["tintos", "blancos", "bebidas"].includes(product.category);
  const secondSpecLabel = isAlcoholicSector ? "Graduación" : "Clasificación";
  const safeRubroJs = escapeHTML(product.rubro || "").replace(/'/g, "\\'");

  modalBody.innerHTML = `
    <div class="modal-image-col ${isLocalPhoto ? "local-photo" : ""}">
      <img src="${encodeURI(product.image)}" alt="${escapeHTML(product.name)}" onerror="handleProductImgError(this, '${product.category}')">
      ${product.badge ? `<div style="position: absolute; top: 14px; left: 14px;"><span class="badge-tag">${escapeHTML(product.badge)}</span></div>` : ""}
    </div>

    <div class="modal-info-col">
      <div class="modal-category-badge">
        <button class="modal-rubro-link" onclick="filterByExactRubro('${safeRubroJs}', '${product.category}')" title="Ver todos los productos de este rubro">
          <i class="fa-solid fa-tag"></i> ${escapeHTML(product.rubro)}
        </button>
        <span>• ${escapeHTML(product.subcategoryLabel || product.subcategory)}</span>
      </div>
      <h2 class="modal-product-title">${escapeHTML(product.name)}</h2>
      
      <div class="price-box" style="margin-bottom: 12px;">
        ${formatOldPrice ? `<span class="old-price" style="font-size: 0.85rem;">${formatOldPrice}</span>` : ""}
        <span class="current-price" style="font-size: 1.4rem;">${formatPrice}</span>
      </div>

      <p class="modal-description">${escapeHTML(product.description)}</p>

      <div class="modal-specs-list">
        <div class="spec-item">
          <span class="spec-label">Origen / Línea</span>
          <span class="spec-val">${escapeHTML(product.origin)}</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">${secondSpecLabel}</span>
          <span class="spec-val">${escapeHTML(product.alcohol)}</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Presentación</span>
          <span class="spec-val">${escapeHTML(product.volume)}</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Rubro Oficial</span>
          <span class="spec-val">${escapeHTML(product.rubro)}</span>
        </div>
      </div>

      ${
        product.pairing
          ? `
        <div class="modal-pairing-box">
          <i class="fa-solid fa-utensils"></i> <strong>Sugerencia:</strong> ${escapeHTML(product.pairing)}
        </div>
      `
          : ""
      }

      <div class="modal-action-row">
        ${
          product.price > 0
            ? `
          <div class="quantity-controller">
            <button class="qty-btn" onclick="changeModalQty(-1)" aria-label="Disminuir cantidad"><i class="fa-solid fa-minus"></i></button>
            <span class="qty-display" id="modalQtyDisplay">1</span>
            <button class="qty-btn" onclick="changeModalQty(1)" aria-label="Aumentar cantidad"><i class="fa-solid fa-plus"></i></button>
          </div>

          <button class="btn-primary" style="flex: 1; justify-content: center;" onclick="addModalProductToCart('${product.id}')">
            <i class="fa-solid fa-cart-shopping"></i> Agregar al Pedido
          </button>
        `
            : `
          <button class="btn-primary" style="flex: 1; justify-content: center; background: #25d366; color: #000; border-color: #25d366;" onclick="consultProduct('${product.id}')">
            <i class="fa-brands fa-whatsapp"></i> Consultar Disponibilidad
          </button>
        `
        }
      </div>
    </div>
  `;

  modal.classList.add("active");
  syncBodyScrollLock();
}

function changeModalQty(delta) {
  modalQuantity += delta;
  if (modalQuantity < 1) modalQuantity = 1;
  if (modalQuantity > 99) modalQuantity = 99;

  const display = document.getElementById("modalQtyDisplay");
  if (display) display.textContent = modalQuantity;
}

function addModalProductToCart(productId) {
  addToCart(productId, modalQuantity);
  closeProductModal();
}

function closeProductModal() {
  const modal = document.getElementById("productModal");
  if (modal) modal.classList.remove("active");
  syncBodyScrollLock();
}

// ==========================================================================
// CARRITO DE COMPRAS & SINCRONIZACIÓN DE PRECIOS
// ==========================================================================
function loadCartFromStorage() {
  try {
    const saved = localStorage.getItem("paisana_cart");
    if (!saved) {
      AppState.cart = [];
      return;
    }
    const rawItems = JSON.parse(saved);
    if (!Array.isArray(rawItems)) {
      AppState.cart = [];
      return;
    }

    // Reconciliar contra el nuevo catálogo 3.0 para mantener precios e IDs siempre actualizados
    const reconciled = [];
    rawItems.forEach((savedItem) => {
      if (!savedItem || savedItem.quantity <= 0) return;
      const savedNorm = normalizeText(savedItem.name);
      const match =
        PRODUCTS_DATA.find((p) => p.id === savedItem.id && normalizeText(p.name) === savedNorm) ||
        PRODUCTS_DATA.find((p) => normalizeText(p.name) === savedNorm);

      if (match && match.price > 0) {
        const existing = reconciled.find((r) => r.id === match.id);
        if (existing) {
          existing.quantity += savedItem.quantity;
        } else {
          reconciled.push({
            id: match.id,
            name: match.name,
            price: match.price,
            image: match.image,
            volume: match.volume,
            quantity: savedItem.quantity
          });
        }
      }
    });

    AppState.cart = reconciled;
    saveCartToStorage();
  } catch (err) {
    AppState.cart = [];
  }
}

function saveCartToStorage() {
  try {
    localStorage.setItem("paisana_cart", JSON.stringify(AppState.cart));
  } catch (err) {
    console.error("Error al guardar carrito", err);
  }
}

function addToCart(productId, quantity = 1) {
  const product = PRODUCTS_DATA.find((p) => p.id === productId);
  if (!product) return;

  const existing = AppState.cart.find((item) => item.id === productId);
  if (existing) {
    existing.quantity += quantity;
  } else {
    AppState.cart.push({
      id: product.id,
      name: product.name,
      price: product.price,
      image: product.image,
      volume: product.volume,
      quantity: quantity
    });
  }

  saveCartToStorage();
  updateCartUI();
  renderProducts();
  showToast(`¡${product.name} agregado! 🛍️`);
}

function updateCartQuantity(productId, delta) {
  const item = AppState.cart.find((i) => i.id === productId);
  if (!item) return;

  item.quantity += delta;
  if (item.quantity <= 0) {
    removeFromCart(productId);
    return;
  }

  saveCartToStorage();
  updateCartUI();
  renderProducts();
}

function removeFromCart(productId) {
  AppState.cart = AppState.cart.filter((i) => i.id !== productId);
  saveCartToStorage();
  updateCartUI();
  renderProducts();
}

function clearCart() {
  AppState.cart = [];
  saveCartToStorage();
  updateCartUI();
  renderProducts();
}

function openCart() {
  const drawer = document.getElementById("cartDrawer");
  const backdrop = document.getElementById("cartBackdrop");
  if (drawer) drawer.classList.add("active");
  if (backdrop) backdrop.classList.add("active");
  syncBodyScrollLock();
  updateCartUI();
}

function closeCart() {
  const drawer = document.getElementById("cartDrawer");
  const backdrop = document.getElementById("cartBackdrop");
  if (drawer) drawer.classList.remove("active");
  if (backdrop) backdrop.classList.remove("active");
  syncBodyScrollLock();
}

function updateCartUI() {
  const totalItems = AppState.cart.reduce((sum, item) => sum + item.quantity, 0);
  const subtotal = AppState.cart.reduce(
    (sum, item) => sum + (item.price > 0 ? item.price * item.quantity : 0),
    0
  );

  const headerBadge = document.getElementById("headerCartBadge");
  const mobileBadge = document.getElementById("mobileCartBadge");
  const headerTotal = document.getElementById("headerCartTotal");
  const clearCartBtn = document.getElementById("clearCartBtn");

  if (headerBadge) headerBadge.textContent = totalItems;
  if (mobileBadge) mobileBadge.textContent = totalItems;
  if (headerTotal) {
    headerTotal.textContent =
      subtotal > 0 ? formatMoney(subtotal) : totalItems > 0 ? "A consultar" : "$0";
  }
  if (clearCartBtn) {
    clearCartBtn.style.display = AppState.cart.length > 0 ? "inline-flex" : "none";
  }

  const cartList = document.getElementById("cartItemsList");
  const cartSubtotalEl = document.getElementById("cartSubtotal");
  const cartShippingFeeEl = document.getElementById("cartShippingFee");
  const cartTotalSumEl = document.getElementById("cartTotalSum");

  if (cartList) {
    if (AppState.cart.length === 0) {
      cartList.innerHTML = `
        <div class="cart-empty-state">
          <i class="fa-solid fa-basket-shopping"></i>
          <h4>Tu carrito está vacío</h4>
          <p style="font-size: 0.8rem; margin-top: 6px;">Explorá nuestros sectores de vinos, combos, cervezas y más para armar tu pedido.</p>
        </div>
      `;
    } else {
      cartList.innerHTML = AppState.cart
        .map((item) => {
          const itemTotalStr =
            item.price > 0 ? formatMoney(item.price * item.quantity) : "A consultar";
          return `
          <div class="cart-item-row">
            <img src="${encodeURI(item.image)}" alt="${escapeHTML(item.name)}" class="cart-item-img" onerror="handleProductImgError(this, '')">
            <div class="cart-item-info">
              <span class="cart-item-title">${escapeHTML(item.name)}</span>
              <span class="cart-item-price">${itemTotalStr} <small style="color: var(--text-dim); font-weight: 500;">(${escapeHTML(item.volume)})</small></span>
              
              <div class="cart-item-actions">
                <div class="cart-qty-ctrl">
                  <button class="cart-qty-btn" onclick="updateCartQuantity('${item.id}', -1)" aria-label="Restar">-</button>
                  <span>${item.quantity}</span>
                  <button class="cart-qty-btn" onclick="updateCartQuantity('${item.id}', 1)" aria-label="Sumar">+</button>
                </div>
              </div>
            </div>

            <button class="cart-delete-item" onclick="removeFromCart('${item.id}')" title="Eliminar">
              <i class="fa-solid fa-trash-can"></i>
            </button>
          </div>
        `;
        })
        .join("");
    }
  }

  const isDelivery = AppState.deliveryMethod === "envio";
  const shippingCost = isDelivery && subtotal > 0 ? STORE_CONFIG.deliveryFee : 0;
  const finalTotal = subtotal + shippingCost;

  if (cartSubtotalEl) cartSubtotalEl.textContent = subtotal > 0 ? formatMoney(subtotal) : "$0";
  if (cartShippingFeeEl) {
    if (AppState.deliveryMethod === "retiro") {
      cartShippingFeeEl.textContent = "Retiro en local ($0)";
    } else if (subtotal === 0) {
      cartShippingFeeEl.textContent = "$0";
    } else {
      cartShippingFeeEl.textContent = `${formatMoney(shippingCost)} (Cadetería)`;
    }
  }
  if (cartTotalSumEl) cartTotalSumEl.textContent = finalTotal > 0 ? formatMoney(finalTotal) : "$0";
}

// Control de Vista (Grilla vs Lista)
function setViewMode(mode) {
  AppState.viewMode = mode;
  try {
    localStorage.setItem("paisana_view_mode", mode);
  } catch (e) {}
  applyViewModeUI();
}

function applyViewModeUI() {
  const gridEl = document.getElementById("productsGrid");
  const gridBtn = document.getElementById("viewGridBtn");
  const listBtn = document.getElementById("viewListBtn");

  if (gridEl) {
    gridEl.classList.toggle("list-view", AppState.viewMode === "list");
  }

  if (gridBtn && listBtn) {
    listBtn.classList.toggle("active", AppState.viewMode === "list");
    gridBtn.classList.toggle("active", AppState.viewMode !== "list");
  }
}

// Fallback vectorial de imagen en caso de error de red
function handleProductImgError(img, category) {
  img.onerror = null;
  img.src =
    'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 160" width="160" height="160"><rect width="160" height="160" fill="%230d1117"/><circle cx="80" cy="80" r="50" fill="%2317202e"/><path d="M72 35h16v20l12 25v45H60V80l12-25V35z" fill="none" stroke="%233ca1a4" stroke-width="3.5" stroke-linecap="round"/><circle cx="80" cy="98" r="10" fill="%23e5aa38" opacity="0.8"/><path d="M68 132h24" stroke="%23e5aa38" stroke-width="3" stroke-linecap="round"/></svg>';
}

// ==========================================================================
// CHECKOUT & GENERACIÓN DE PEDIDO WHATSAPP
// ==========================================================================
function openCheckoutModal() {
  const modal = document.getElementById("checkoutModal");
  if (modal) modal.classList.add("active");
  syncBodyScrollLock();
}

function closeCheckoutModal() {
  const modal = document.getElementById("checkoutModal");
  if (modal) modal.classList.remove("active");
  syncBodyScrollLock();
}

function toggleDeliveryMethod(method) {
  AppState.deliveryMethod = method;
  const addressGroup = document.getElementById("addressFieldGroup");
  const addressInput = document.getElementById("customerAddress");
  const radioDelivery = document.getElementById("radioDeliveryLabel");
  const radioPickup = document.getElementById("radioPickupLabel");
  const pickupBox = document.getElementById("pickupLocationBox");

  if (method === "retiro") {
    if (addressGroup) addressGroup.style.display = "none";
    if (addressInput) addressInput.required = false;
    if (pickupBox) pickupBox.style.display = "flex";
    if (radioDelivery) radioDelivery.classList.remove("selected");
    if (radioPickup) radioPickup.classList.add("selected");
  } else {
    if (addressGroup) addressGroup.style.display = "block";
    if (addressInput) addressInput.required = true;
    if (pickupBox) pickupBox.style.display = "none";
    if (radioDelivery) radioDelivery.classList.add("selected");
    if (radioPickup) radioPickup.classList.remove("selected");
  }

  updateCartUI();
}

function handleCheckoutSubmit(e) {
  e.preventDefault();

  if (AppState.cart.length === 0) {
    showToast("Tu carrito está vacío");
    return;
  }

  const name = document.getElementById("customerName").value.trim();
  const address = document.getElementById("customerAddress")
    ? document.getElementById("customerAddress").value.trim()
    : "";
  const payment = document.getElementById("paymentMethod").value;
  const notes = document.getElementById("orderNotes").value.trim();

  const subtotal = AppState.cart.reduce(
    (sum, item) => sum + (item.price > 0 ? item.price * item.quantity : 0),
    0
  );
  const isDelivery = AppState.deliveryMethod === "envio";
  const shippingCost = isDelivery ? STORE_CONFIG.deliveryFee : 0;
  const total = subtotal + shippingCost;
  const inquiryCode = `COT-${Date.now().toString().slice(-5)}`;

  let message = `🍷 *SOLICITUD DE DISPONIBILIDAD & COTIZACIÓN*\n`;
  message += `*Paisana Bebidas* | Ref: #${inquiryCode}\n`;
  message += `━━━━━━━━━━━━━━━━━━━━━\n`;
  message += `👤 *Cliente:* ${name}\n`;
  message += `🛵 *Modalidad:* ${isDelivery ? "Envío a Domicilio" : "Retiro en Local"}\n`;

  if (isDelivery) {
    message += `📍 *Dirección de Entrega:* ${address}\n`;
  }
  message += `💳 *Medio de Pago Propuesto:* ${payment}\n`;
  if (notes) {
    message += `📝 *Aclaraciones:* ${notes}\n`;
  }
  message += `━━━━━━━━━━━━━━━━━━━━━\n`;
  message += `📋 *PRODUCTOS SELECCIONADOS DEL CATÁLOGO:*\n\n`;

  AppState.cart.forEach((item, index) => {
    const unitPriceStr = item.price > 0 ? formatMoney(item.price) : "A consultar";
    const lineTotalStr =
      item.price > 0 ? formatMoney(item.price * item.quantity) : "A consultar";
    message += `${index + 1}. *${item.name}* (${item.volume})\n`;
    message += `   ${item.quantity} un. x ${unitPriceStr} = *${lineTotalStr}*\n`;
  });

  message += `━━━━━━━━━━━━━━━━━━━━━\n`;
  message += `💰 *Subtotal Estimado:* ${formatMoney(subtotal)}\n`;
  if (isDelivery) {
    message += `🚚 *Envío a Domicilio:* ${formatMoney(shippingCost)} (Cadetería en moto)\n`;
  } else {
    message += `🏪 *Retiro en Local:* Sin costo\n`;
    message += `📍 *Punto de Retiro:* ${STORE_CONFIG.storeAddress}\n`;
    message += `🗺️ *Ubicación Maps:* ${STORE_CONFIG.mapsUrl}\n`;
  }
  message += `💎 *TOTAL ESTIMADO:* ${formatMoney(total)}\n`;
  message += `━━━━━━━━━━━━━━━━━━━━━\n`;
  message += `⚖️ *Aviso Legal:* Solicitud generada desde catálogo web informativo. Operación y entrega sujeta a confirmación de stock y acreditación de mayoría de edad (+18) según Ley Nac. 24.788. Beber con moderación.`;

  const whatsappUrl = `https://wa.me/${STORE_CONFIG.whatsappNumber}?text=${encodeURIComponent(message)}`;
  window.open(whatsappUrl, "_blank");

  clearCart();
  closeCheckoutModal();
  showToast("¡Consulta de pedido enviada por WhatsApp! 📲");
}

// ==========================================================================
// CONTROLADORES: BOTÓN DE ARREPENTIMIENTO (Res. 424/2020)
// ==========================================================================
function openRegretModal() {
  const modal = document.getElementById("regretModal");
  if (modal) modal.classList.add("active");
  syncBodyScrollLock();
}

function closeRegretModal() {
  const modal = document.getElementById("regretModal");
  if (modal) modal.classList.remove("active");
  syncBodyScrollLock();
}

function handleRegretSubmit(e) {
  e.preventDefault();

  const name = document.getElementById("regretCustomerName").value.trim();
  const contact = document.getElementById("regretContact").value.trim();
  const orderCode = document.getElementById("regretOrderCode").value.trim();
  const reason = document.getElementById("regretReason").value.trim();
  const revocationCode = `REV-${Date.now().toString().slice(-6)}`;

  let message = `🔄 *NOTIFICACIÓN DE REVOCACIÓN / ARREPENTIMIENTO*\n`;
  message += `*Conforme Art. 34 Ley 24.240 y Res. 424/2020*\n`;
  message += `━━━━━━━━━━━━━━━━━━━━━\n`;
  message += `🎫 *Código de Trámite:* ${revocationCode}\n`;
  message += `👤 *Titular:* ${name}\n`;
  message += `📞 *Contacto:* ${contact}\n`;
  message += `📦 *Referencia/Pedido:* ${orderCode}\n`;
  if (reason) {
    message += `💬 *Motivo:* ${reason}\n`;
  }
  message += `━━━━━━━━━━━━━━━━━━━━━\n`;
  message += `Solicito la revocación formal de la solicitud/compra conforme al plazo legal establecido por la normativa vigente.`;

  const whatsappUrl = `https://wa.me/${STORE_CONFIG.whatsappNumber}?text=${encodeURIComponent(message)}`;
  window.open(whatsappUrl, "_blank");

  closeRegretModal();
  const form = document.getElementById("regretForm");
  if (form) form.reset();
  showToast(`Revocación generada: Código ${revocationCode}`);
}

// ==========================================================================
// CONTROLADORES: TÉRMINOS Y PRIVACIDAD (Ley 25.326)
// ==========================================================================
function openPrivacyModal() {
  const modal = document.getElementById("privacyModal");
  if (modal) modal.classList.add("active");
  syncBodyScrollLock();
}

function closePrivacyModal() {
  const modal = document.getElementById("privacyModal");
  if (modal) modal.classList.remove("active");
  syncBodyScrollLock();
}

// ==========================================================================
// UTILIDADES, SEGURIDAD & TOAST
// ==========================================================================
function formatMoney(amount) {
  const num = Number(amount);
  if (isNaN(num) || num <= 0) return "Consultar";
  return `$${num.toLocaleString("es-AR")}`;
}

function escapeHTML(str) {
  if (typeof str !== "string") return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function showToast(message) {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = "toast-msg";

  const icon = document.createElement("i");
  icon.className = "fa-solid fa-circle-check";

  const textSpan = document.createElement("span");
  textSpan.textContent = String(message);

  toast.appendChild(icon);
  toast.appendChild(textSpan);
  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3000);
}

// ==========================================================================
// APARTADO DE CALENDARIO DE EVENTOS (DICIEMBRE 2026)
// ==========================================================================
const DECEMBER_EVENTS = {
  5: {
    day: 5,
    dateLabel: "Sábado 5 de Diciembre",
    tag: "Lanzamiento Oficial",
    icon: "fa-solid fa-wand-magic-sparkles",
    title: "Reinauguración de la Tienda Web",
    schedule: "Desde las 10:00 hs • Todo el día",
    location: "Tienda Online Paisana & Local (C. Tapón Moyano 1745)",
    description:
      "Estrenamos nuestra tienda web renovada con más de 570 productos sectorizados por rubro, 60 combos previa, buscador inteligente y pedidos express directo por WhatsApp. ¡Celebralo recorriendo el nuevo catálogo con beneficios especiales de apertura!",
    ctaLabel: "Explorar Nuevo Catálogo",
    ctaAction: "exploreCatalog",
    waText:
      "Hola Paisana Bebidas! Vi en el calendario la Reinauguración de la Web del 5 de diciembre y quería consultar por las novedades y promos del día."
  },
  12: {
    day: 12,
    dateLabel: "Sábado 12 de Diciembre",
    tag: "Experiencia Presencial +18",
    icon: "fa-solid fa-martini-glass-citrus",
    title: "Degustación de Gin",
    schedule: "19:30 a 22:30 hs",
    location: "Local Paisana Bebidas • C. Tapón Moyano 1745, Mendoza",
    description:
      "Sumate a una noche dedicada al mundo del gin: degustación guiada de etiquetas seleccionadas, botánicos aromáticos, cítricos y tónicas premium para descubrir tu Gin Tonic ideal junto a nuestro equipo.",
    ctaLabel: "Ver Gins en Tienda",
    ctaAction: "exploreGin",
    waText:
      "Hola Paisana Bebidas! Quiero consultar y reservar mi lugar para la Degustación de Gin del sábado 12 de diciembre (19:30 a 22:30 hs)."
  }
};

let activeCalendarDay = null;

function initEventsCalendar() {
  const grid = document.getElementById("miniCalendarGrid");
  if (!grid) return;

  // Diciembre 2026 (mes 11 en JS, 0-indexado)
  const year = 2026;
  const month = 11;
  const firstDayJs = new Date(year, month, 1).getDay(); // 0=Dom, 1=Lun...
  const startOffset = (firstDayJs + 6) % 7; // Lunes = 0
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  let html = "";
  for (let i = 0; i < startOffset; i++) {
    html += `<span class="mini-cal-empty" aria-hidden="true"></span>`;
  }

  for (let day = 1; day <= daysInMonth; day++) {
    const ev = DECEMBER_EVENTS[day];
    if (ev) {
      html += `
        <button type="button"
                class="mini-cal-day has-event"
                data-event-day="${day}"
                aria-expanded="false"
                title="${escapeHTML(ev.title)} (${escapeHTML(ev.schedule)})"
                onclick="toggleCalendarEvent(${day})">
          <span>${day}</span>
          <span class="mini-cal-dot" aria-hidden="true"></span>
        </button>
      `;
    } else {
      html += `<span class="mini-cal-day">${day}</span>`;
    }
  }

  grid.innerHTML = html;
}

function toggleCalendarEvent(day) {
  const expandBox = document.getElementById("calendarEventExpand");
  const contentBox = document.getElementById("calendarEventContent");
  if (!expandBox || !contentBox) return;

  const ev = DECEMBER_EVENTS[day];
  if (!ev) return;

  // Si se vuelve a clickear el mismo día activo, contraer
  if (activeCalendarDay === day) {
    activeCalendarDay = null;
    expandBox.classList.remove("expanded");
    updateCalendarActiveStates(null);
    return;
  }

  activeCalendarDay = day;
  updateCalendarActiveStates(day);

  const secondaryBtnHtml =
    ev.ctaAction === "exploreGin"
      ? `<button type="button" class="btn-secondary calendar-cta-btn" onclick="goToGinSection()">
           <i class="fa-solid fa-leaf"></i> ${escapeHTML(ev.ctaLabel)}
         </button>`
      : `<button type="button" class="btn-secondary calendar-cta-btn" onclick="scrollToCatalogSection()">
           <i class="fa-solid fa-compass"></i> ${escapeHTML(ev.ctaLabel)}
         </button>`;

  const waUrl = `https://wa.me/${STORE_CONFIG.whatsappNumber}?text=${encodeURIComponent(ev.waText)}`;

  contentBox.innerHTML = `
    <div class="calendar-event-card">
      <div class="calendar-event-header">
        <div class="calendar-event-badges">
          <span class="event-date-pill">
            <i class="fa-regular fa-calendar-check"></i> ${escapeHTML(ev.dateLabel)}
          </span>
          <span class="event-type-pill">${escapeHTML(ev.tag)}</span>
        </div>
        <button type="button" class="event-close-btn" onclick="toggleCalendarEvent(${day})" aria-label="Cerrar detalle del evento" title="Contraer">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <h3 class="calendar-event-title">
        <i class="${ev.icon}"></i> ${escapeHTML(ev.title)}
      </h3>

      <div class="calendar-event-meta">
        <span class="event-meta-chip event-meta-time">
          <i class="fa-regular fa-clock"></i> <strong>Horario:</strong> ${escapeHTML(ev.schedule)}
        </span>
        <span class="event-meta-chip">
          <i class="fa-solid fa-location-dot"></i> ${escapeHTML(ev.location)}
        </span>
      </div>

      <p class="calendar-event-desc">${escapeHTML(ev.description)}</p>

      <div class="calendar-event-actions">
        <a href="${waUrl}" target="_blank" rel="noopener noreferrer" class="btn-primary calendar-cta-btn">
          <i class="fa-brands fa-whatsapp"></i> Consultar / Agendar por WhatsApp
        </a>
        ${secondaryBtnHtml}
      </div>
    </div>
  `;

  expandBox.classList.add("expanded");
}

function updateCalendarActiveStates(selectedDay) {
  document.querySelectorAll("[data-event-day]").forEach((el) => {
    const isMatch = Number(el.getAttribute("data-event-day")) === selectedDay;
    el.classList.toggle("active", isMatch);
    el.setAttribute("aria-expanded", isMatch ? "true" : "false");
  });
}

function goToGinSection() {
  switchCategory("bebidas", { subcategory: "gin", scrollToCatalog: true });
}

function scrollToCatalogSection() {
  const cat = document.getElementById("catalogo");
  if (cat) cat.scrollIntoView({ behavior: "smooth" });
}

