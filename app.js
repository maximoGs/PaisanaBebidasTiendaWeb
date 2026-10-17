/**
 * PAISANA BEBIDAS - LÓGICA DE APLICACIÓN Y COMERCIO
 * Autor: Antigravity AI
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
  bodegaAmigaNumber: "5492617094195" // Martino Wines (solo para reservas y promoción de Martino)
};

// ==========================================================================
// CONFIGURACIÓN DE CATEGORÍAS Y VARIETALES / SUB-PESTAÑAS
// ==========================================================================
const SUBCATEGORIES_MAP = {
  tintos: {
    title: "Vinos Tintos",
    icon: "fa-solid fa-wine-glass",
    subtitle: "Explorá nuestras mejores etiquetas tintas: Malbec, Cabernet Sauvignon, Blends y variedades de autor",
    subchips: [
      { id: "all", label: "🍷 Todos los Tintos" },
      { id: "malbec", label: "🍇 Malbec" },
      { id: "cabernet-sauvignon", label: "🍷 Cabernet Sauvignon" },
      { id: "blends", label: "✨ Blends & Otros Tintos" }
    ]
  },
  blancos: {
    title: "Vinos Blancos & Espumantes",
    icon: "fa-solid fa-champagne-glasses",
    subtitle: "Chardonnay, cepas blancas, dulces de cosecha tardía, rosados y espumantes",
    subchips: [
      { id: "all", label: "🥂 Todos los Blancos" },
      { id: "blancos-chardonnay", label: "🥂 Blancos & Chardonnay" },
      { id: "dulces", label: "🍯 Dulces Cosecha Tardía" },
      { id: "espumantes", label: "🍾 Espumantes" },
      { id: "rosados", label: "🌸 Rosados" }
    ]
  },
  bebidas: {
    title: "Cervezas & Destilados",
    icon: "fa-solid fa-beer-mug-empty",
    subtitle: "Cervezas con lúpulos seleccionados, aperitivos, gin premium y espirituosas",
    subchips: [
      { id: "all", label: "🍺 Todas las Bebidas" },
      { id: "cervezas", label: "🌿 Cervezas & Lúpulos" },
      { id: "fernet-aperitivos", label: "🦅 Fernet & Aperitivos" },
      { id: "gin", label: "🌿 Gin Premium" },
      { id: "vodka", label: "🧊 Vodka" },
      { id: "whisky", label: "🥃 Whisky" }
    ]
  },
  "sin-alcohol": {
    title: "Bebidas sin Alcohol",
    icon: "fa-solid fa-bottle-water",
    subtitle: "Gaseosas, mixers especiales, tónicas, energizantes y aguas",
    subchips: [
      { id: "all", label: "🥤 Todo Sin Alcohol" },
      { id: "gaseosas", label: "🥤 Gaseosas" },
      { id: "tonicas-mixers", label: "🫧 Tónicas & Mixers" },
      { id: "energizantes", label: "⚡ Energizantes" },
      { id: "aguas-jugos", label: "💧 Aguas & Jugos" }
    ]
  },
  snacks: {
    title: "Snacks & Combos",
    icon: "fa-solid fa-bowl-food",
    subtitle: "Snacks crocantes, chocolates, hielo, descartables y super combos",
    subchips: [
      { id: "all", label: "🍿 Todos los Snacks" },
      { id: "promos-combos", label: "🔥 Combos & Promos" },
      { id: "snacks-salados", label: "🥨 Snacks Salados" },
      { id: "chocolates-dulces", label: "🍫 Chocolates & Dulces" },
      { id: "hielo-descartables", label: "🧊 Hielo & Descartables" }
    ]
  }
};

// ==========================================================================
// ESTADO GLOBAL DE LA APLICACIÓN
// ==========================================================================
const AppState = {
  currentCategory: "tintos",
  currentSubcategory: "all",
  searchQuery: "",
  currentSort: "default",
  cart: [],
  deliveryMethod: "envio", // 'envio' o 'retiro'
  viewMode: localStorage.getItem("paisana_view_mode") || "grid"
};

// ==========================================================================
// INICIALIZACIÓN
// ==========================================================================
document.addEventListener("DOMContentLoaded", () => {
  initAgeGate();
  loadCartFromStorage();
  setupEventListeners();
  renderSubcategoryChips();
  renderProducts();
  updateCartUI();
  initPromoCarousel();
});

// ==========================================================================
// CONTROL DE EDAD (+18)
// ==========================================================================
function initAgeGate() {
  const isVerified = sessionStorage.getItem("paisana_age_verified");
  const ageModal = document.getElementById("ageGateModal");
  const confirmBtn = document.getElementById("confirmAgeBtn");

  if (!isVerified && ageModal) {
    ageModal.classList.add("active");
    document.body.style.overflow = "hidden";
  }

  if (confirmBtn && ageModal) {
    confirmBtn.addEventListener("click", () => {
      sessionStorage.setItem("paisana_age_verified", "true");
      ageModal.classList.remove("active");
      document.body.style.overflow = "";
      showToast("Acceso verificado: Mayor de 18 años");
    });
  }
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
  if (viewGridBtn) {
    viewGridBtn.addEventListener("click", () => setViewMode("grid"));
  }
  if (viewListBtn) {
    viewListBtn.addEventListener("click", () => setViewMode("list"));
  }
  applyViewModeUI();

  // Carrito Drawer Trigger (Desktop & Mobile)
  const desktopCartBtn = document.getElementById("desktopCartBtn");
  const mobileCartBtn = document.getElementById("mobileCartBtn");
  const closeCartBtn = document.getElementById("closeCartBtn");
  const cartBackdrop = document.getElementById("cartBackdrop");

  if (desktopCartBtn) desktopCartBtn.addEventListener("click", openCart);
  if (mobileCartBtn) mobileCartBtn.addEventListener("click", openCart);
  if (closeCartBtn) closeCartBtn.addEventListener("click", closeCart);
  if (cartBackdrop) cartBackdrop.addEventListener("click", closeCart);

  // Modal Detalle de Producto
  const productModal = document.getElementById("productModal");
  const closeProductModalBtn = document.getElementById("closeProductModalBtn");
  if (closeProductModalBtn) {
    closeProductModalBtn.addEventListener("click", closeProductModal);
  }
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

  if (closeCheckoutModalBtn) {
    closeCheckoutModalBtn.addEventListener("click", closeCheckoutModal);
  }
  if (checkoutModal) {
    checkoutModal.addEventListener("click", (e) => {
      if (e.target === checkoutModal) closeCheckoutModal();
    });
  }

  if (checkoutForm) {
    checkoutForm.addEventListener("submit", handleCheckoutSubmit);
  }

  // Modal Botón de Arrepentimiento (Res. 424/2020)
  const openRegretBtn = document.getElementById("openRegretBtn");
  const closeRegretModalBtn = document.getElementById("closeRegretModalBtn");
  const regretModal = document.getElementById("regretModal");
  const regretForm = document.getElementById("regretForm");

  if (openRegretBtn) {
    openRegretBtn.addEventListener("click", openRegretModal);
  }
  if (closeRegretModalBtn) {
    closeRegretModalBtn.addEventListener("click", closeRegretModal);
  }
  if (regretModal) {
    regretModal.addEventListener("click", (e) => {
      if (e.target === regretModal) closeRegretModal();
    });
  }
  if (regretForm) {
    regretForm.addEventListener("submit", handleRegretSubmit);
  }

  // Modal Términos y Privacidad (Ley 25.326)
  const openPrivacyBtn = document.getElementById("openPrivacyBtn");
  const closePrivacyModalBtn = document.getElementById("closePrivacyModalBtn");
  const privacyModal = document.getElementById("privacyModal");

  if (openPrivacyBtn) {
    openPrivacyBtn.addEventListener("click", openPrivacyModal);
  }
  if (closePrivacyModalBtn) {
    closePrivacyModalBtn.addEventListener("click", closePrivacyModal);
  }
  if (privacyModal) {
    privacyModal.addEventListener("click", (e) => {
      if (e.target === privacyModal) closePrivacyModal();
    });
  }

  // Efecto Header Scroll
  window.addEventListener("scroll", () => {
    const header = document.getElementById("mainHeader");
    if (header) {
      if (window.scrollY > 30) {
        header.classList.add("scrolled");
      } else {
        header.classList.remove("scrolled");
      }
    }
  });
}

// Sincronizar inputs de búsqueda
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
  AppState.searchQuery = query.trim().toLowerCase();
  renderProducts();
}

// ==========================================================================
// CAMBIO DE CATEGORÍAS & SUB-VARIETALES
// ==========================================================================
function switchCategory(categoryKey) {
  if (categoryKey === "vinos") {
    categoryKey = "tintos";
  }
  if (!SUBCATEGORIES_MAP[categoryKey]) return;

  AppState.currentCategory = categoryKey;
  AppState.currentSubcategory = "all";

  // Actualizar Tabs Header
  document.querySelectorAll(".category-tab-btn").forEach((btn) => {
    if (btn.getAttribute("data-category") === categoryKey) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });

  // Actualizar Bottom Nav Móvil
  document.querySelectorAll(".bottom-nav-item").forEach((btn) => {
    btn.classList.remove("active");
  });
  const activeBnav = document.getElementById(`bnav-${categoryKey}`);
  if (activeBnav) activeBnav.classList.add("active");

  // Actualizar Títulos de Sección
  const meta = SUBCATEGORIES_MAP[categoryKey];
  const titleEl = document.getElementById("currentSectionTitle");
  const subEl = document.getElementById("currentSectionSubtitle");
  if (titleEl) {
    titleEl.innerHTML = `<i class="${meta.icon}" style="color: var(--gold-primary);"></i> ${meta.title}`;
  }
  if (subEl) {
    subEl.textContent = meta.subtitle;
  }

  renderSubcategoryChips();
  renderProducts();

  // Scroll suave al catálogo si está arriba
  const catalogoEl = document.getElementById("catalogo");
  if (catalogoEl && window.scrollY > 300) {
    catalogoEl.scrollIntoView({ behavior: "smooth" });
  }
}

function filterBySubcategory(subcatId) {
  AppState.currentSubcategory = subcatId;

  document.querySelectorAll(".subchip-btn").forEach((chip) => {
    if (chip.getAttribute("data-subcat") === subcatId) {
      chip.classList.add("active");
    } else {
      chip.classList.remove("active");
    }
  });

  renderProducts();
}

function filterByPromoCombos() {
  switchCategory("snacks");
  setTimeout(() => {
    filterBySubcategory("promos-combos");
  }, 50);
}

function filterMartinoWines() {
  switchCategory("tintos");
  AppState.searchQuery = "martino";
  syncSearchInputs("Martino", "none");
  renderProducts();
  const catEl = document.getElementById("catalogo");
  if (catEl) catEl.scrollIntoView({ behavior: "smooth" });
  showToast("Explorando varietales de Bodega Martino 🍷");
}

function addComboToCart(code) {
  const codeStr = String(code).trim();
  const product = PRODUCTS_DATA.find((p) => {
    const pCode = String(p.code || "").trim();
    return pCode === codeStr || pCode.padStart(3, "0") === codeStr.padStart(3, "0") || p.id === `prod-${codeStr}`;
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
  const msg = `Hola Paisana Bebidas! Quería consultar disponibilidad y precio de: ${product.name} (${product.volume || "750 ml"}).`;
  const url = `https://wa.me/${STORE_CONFIG.whatsappNumber}?text=${encodeURIComponent(msg)}`;
  window.open(url, "_blank");
}

// ==========================================================================
// CARRUSEL PROMOCIONAL (Bodega Amiga + 3 Combos)
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
  const slideDuration = 6500; // 6.5 segundos por slide

  function goToSlide(index) {
    currentSlide = (index + totalSlides) % totalSlides;

    slides.forEach((slide, i) => {
      if (i === currentSlide) {
        slide.classList.add("active");
      } else {
        slide.classList.remove("active");
      }
    });

    dots.forEach((dot, i) => {
      if (i === currentSlide) {
        dot.classList.add("active");
      } else {
        dot.classList.remove("active");
      }
    });

    if (counter) {
      counter.textContent = `${currentSlide + 1} / ${totalSlides}`;
    }
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

    // Gestos táctiles / Swipe en móviles y tablets
    let touchStartX = 0;
    let touchEndX = 0;

    wrapper.addEventListener("touchstart", (e) => {
      if (e.changedTouches && e.changedTouches[0]) {
        touchStartX = e.changedTouches[0].screenX;
      }
      stopAutoPlay();
    }, { passive: true });

    wrapper.addEventListener("touchend", (e) => {
      if (e.changedTouches && e.changedTouches[0]) {
        touchEndX = e.changedTouches[0].screenX;
        const diff = touchEndX - touchStartX;
        if (Math.abs(diff) > 40) {
          if (diff < 0) {
            nextSlide();
          } else {
            prevSlide();
          }
        }
      }
      startAutoPlay();
    }, { passive: true });
  }

  goToSlide(0);
  startAutoPlay();
}

// Renderizar Sub-pestañas / Chips
function renderSubcategoryChips() {
  const container = document.getElementById("subcategoryChips");
  if (!container) return;

  const currentMap = SUBCATEGORIES_MAP[AppState.currentCategory];
  if (!currentMap) return;

  container.innerHTML = currentMap.subchips
    .map(
      (chip) => `
    <button class="subchip-btn ${AppState.currentSubcategory === chip.id ? "active" : ""}" 
            data-subcat="${chip.id}" 
            onclick="filterBySubcategory('${chip.id}')">
      ${chip.label}
    </button>
  `
    )
    .join("");
}

// ==========================================================================
// RENDERIZADO DE PRODUCTOS
// ==========================================================================
function renderProducts() {
  const grid = document.getElementById("productsGrid");
  const countEl = document.getElementById("itemsCount");
  if (!grid) return;

  // Filtrado
  let filtered = PRODUCTS_DATA.filter((item) => {
    // Si hay búsqueda global, busca en todo el catálogo
    if (AppState.searchQuery) {
      const matchSearch =
        item.name.toLowerCase().includes(AppState.searchQuery) ||
        item.description.toLowerCase().includes(AppState.searchQuery) ||
        item.origin.toLowerCase().includes(AppState.searchQuery) ||
        item.subcategory.toLowerCase().includes(AppState.searchQuery);
      return matchSearch;
    }

    // Filtro por categoría principal
    if (item.category !== AppState.currentCategory) {
      return false;
    }

    // Filtro por subcategoría / varietal
    if (AppState.currentSubcategory !== "all" && item.subcategory !== AppState.currentSubcategory) {
      return false;
    }

    return true;
  });

  // Ordenamiento
  if (AppState.currentSort === "price-asc") {
    filtered.sort((a, b) => a.price - b.price);
  } else if (AppState.currentSort === "price-desc") {
    filtered.sort((a, b) => b.price - a.price);
  } else if (AppState.currentSort === "name-asc") {
    filtered.sort((a, b) => a.name.localeCompare(b.name));
  }

  // Actualizar Contador
  if (countEl) {
    countEl.textContent = `${filtered.length} producto${filtered.length !== 1 ? "s" : ""}`;
  }

  // Estado Vacío
  if (filtered.length === 0) {
    grid.innerHTML = `
      <div class="empty-catalog">
        <i class="fa-solid fa-wine-bottle"></i>
        <h3>No encontramos productos</h3>
        <p>Probá con otro término de búsqueda o seleccioná otra categoría.</p>
        <button class="btn-primary" onclick="resetFilters()">
          <i class="fa-solid fa-arrow-rotate-left"></i> Restablecer filtros
        </button>
      </div>
    `;
    return;
  }

  // Renderizar tarjetas
  grid.innerHTML = filtered
    .map((product) => {
      const formatPrice = formatMoney(product.price);
      const formatOldPrice = product.oldPrice ? formatMoney(product.oldPrice) : null;

      let badgeHtml = "";
      if (product.badge) {
        const isOffer = product.badge.toLowerCase().includes("oferta") || product.badge.toLowerCase().includes("promo");
        badgeHtml = `<span class="badge-tag ${isOffer ? "offer" : ""}">${product.badge}</span>`;
      }

      return `
      <article class="product-card" data-id="${product.id}">
        <div class="product-media" onclick="openProductModal('${product.id}')">
          <img src="${product.image}" alt="${product.name}" class="product-img" loading="lazy" onerror="handleProductImgError(this, '${product.category}')">
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
              <span class="product-category-tag">${product.subcategory.replace("-", " ")}</span>
              <span class="product-vol-tag">${product.volume}</span>
            </div>

            <h3 class="product-name" onclick="openProductModal('${product.id}')" title="${product.name}">
              ${product.name}
            </h3>

            <p class="product-details-brief">${product.origin} • ${product.alcohol}</p>
          </div>

          <div class="product-footer">
            <div class="price-box">
              ${formatOldPrice ? `<span class="old-price">${formatOldPrice}</span>` : ""}
              <span class="current-price">${formatPrice}</span>
            </div>

            ${
              product.price > 0
                ? `<button class="btn-add-cart" onclick="addToCart('${product.id}', 1)" title="Agregar al pedido" aria-label="Agregar ${product.name}">
                     <i class="fa-solid fa-plus"></i>
                   </button>`
                : `<button class="btn-add-cart btn-consultar-wa" onclick="consultProduct('${product.id}')" title="Consultar por WhatsApp" aria-label="Consultar ${product.name}">
                     <i class="fa-brands fa-whatsapp"></i>
                   </button>`
            }
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
  AppState.currentSubcategory = "all";
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

  modalBody.innerHTML = `
    <div class="modal-image-col">
      <img src="${product.image}" alt="${product.name}" onerror="handleProductImgError(this, '${product.category}')">
      ${product.badge ? `<div style="position: absolute; top: 14px; left: 14px;"><span class="badge-tag">${product.badge}</span></div>` : ""}
    </div>

    <div class="modal-info-col">
      <div class="modal-category-badge">${product.category.toUpperCase()} • ${product.subcategory.toUpperCase()}</div>
      <h2 class="modal-product-title">${product.name}</h2>
      
      <div class="price-box" style="margin-bottom: 12px;">
        ${formatOldPrice ? `<span class="old-price" style="font-size: 0.85rem;">${formatOldPrice}</span>` : ""}
        <span class="current-price" style="font-size: 1.4rem;">${formatPrice}</span>
      </div>

      <p class="modal-description">${product.description}</p>

      <div class="modal-specs-list">
        <div class="spec-item">
          <span class="spec-label">Origen</span>
          <span class="spec-val">${product.origin}</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Graduación</span>
          <span class="spec-val">${product.alcohol}</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Contenido</span>
          <span class="spec-val">${product.volume}</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">Calificación</span>
          <span class="spec-val">⭐ ${product.rating} / 5.0</span>
        </div>
      </div>

      ${
        product.pairing
          ? `
        <div class="modal-pairing-box">
          <i class="fa-solid fa-utensils"></i> <strong>Sugerencia de maridaje:</strong> ${product.pairing}
        </div>
      `
          : ""
      }

      <div class="modal-action-row">
        ${
          product.price > 0
            ? `
          <div class="quantity-controller">
            <button class="qty-btn" onclick="changeModalQty(-1)"><i class="fa-solid fa-minus"></i></button>
            <span class="qty-display" id="modalQtyDisplay">1</span>
            <button class="qty-btn" onclick="changeModalQty(1)"><i class="fa-solid fa-plus"></i></button>
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
  document.body.style.overflow = "hidden";
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
  document.body.style.overflow = "";
}

// ==========================================================================
// CARRITO DE COMPRAS & STORAGE
// ==========================================================================
function loadCartFromStorage() {
  try {
    const saved = localStorage.getItem("paisana_cart");
    if (saved) {
      AppState.cart = JSON.parse(saved);
    }
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
  showToast(`¡${product.name} agregado! 🍷`);
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
}

function removeFromCart(productId) {
  AppState.cart = AppState.cart.filter((i) => i.id !== productId);
  saveCartToStorage();
  updateCartUI();
}

function clearCart() {
  AppState.cart = [];
  saveCartToStorage();
  updateCartUI();
}

function openCart() {
  const drawer = document.getElementById("cartDrawer");
  const backdrop = document.getElementById("cartBackdrop");
  if (drawer) drawer.classList.add("active");
  if (backdrop) backdrop.classList.add("active");
  document.body.style.overflow = "hidden";
  updateCartUI();
}

function closeCart() {
  const drawer = document.getElementById("cartDrawer");
  const backdrop = document.getElementById("cartBackdrop");
  if (drawer) drawer.classList.remove("active");
  if (backdrop) backdrop.classList.remove("active");
  document.body.style.overflow = "";
}

function updateCartUI() {
  const totalItems = AppState.cart.reduce((sum, item) => sum + item.quantity, 0);
  const subtotal = AppState.cart.reduce((sum, item) => sum + (item.price > 0 ? item.price * item.quantity : 0), 0);

  // Header badges & Mobile badges
  const headerBadge = document.getElementById("headerCartBadge");
  const mobileBadge = document.getElementById("mobileCartBadge");
  const headerTotal = document.getElementById("headerCartTotal");

  if (headerBadge) headerBadge.textContent = totalItems;
  if (mobileBadge) mobileBadge.textContent = totalItems;
  if (headerTotal) headerTotal.textContent = subtotal > 0 ? formatMoney(subtotal) : (totalItems > 0 ? "A consultar" : "$0");

  // Drawer list
  const cartList = document.getElementById("cartItemsList");
  const cartSubtotalEl = document.getElementById("cartSubtotal");
  const cartShippingFeeEl = document.getElementById("cartShippingFee");
  const cartTotalSumEl = document.getElementById("cartTotalSum");

  // Lista de items en Drawer
  if (cartList) {
    if (AppState.cart.length === 0) {
      cartList.innerHTML = `
        <div class="cart-empty-view">
          <i class="fa-solid fa-basket-shopping"></i>
          <h4>Tu carrito está vacío</h4>
          <p style="font-size: 0.8rem; margin-top: 4px;">Explorá nuestro catálogo de vinos y bebidas para comenzar tu pedido.</p>
        </div>
      `;
    } else {
      cartList.innerHTML = AppState.cart
        .map((item) => {
          const itemTotalStr = item.price > 0 ? formatMoney(item.price * item.quantity) : "A consultar";
          return `
          <div class="cart-item-row">
            <img src="${item.image}" alt="${item.name}" class="cart-item-img" onerror="handleProductImgError(this, '')">
            <div class="cart-item-info">
              <span class="cart-item-title">${item.name}</span>
              <span class="cart-item-price">${itemTotalStr}</span>
              
              <div class="cart-item-actions">
                <div class="cart-qty-ctrl">
                  <button class="cart-qty-btn" onclick="updateCartQuantity('${item.id}', -1)">-</button>
                  <span>${item.quantity}</span>
                  <button class="cart-qty-btn" onclick="updateCartQuantity('${item.id}', 1)">+</button>
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

  // Totales y Costo de Envío / Retiro
  const isDelivery = AppState.deliveryMethod === "envio";
  const shippingCost = isDelivery && subtotal > 0 ? STORE_CONFIG.deliveryFee : 0;
  const finalTotal = subtotal + shippingCost;

  if (cartSubtotalEl) cartSubtotalEl.textContent = formatMoney(subtotal);
  if (cartShippingFeeEl) {
    if (AppState.deliveryMethod === "retiro") {
      cartShippingFeeEl.textContent = "Retiro en local ($0)";
    } else if (subtotal === 0) {
      cartShippingFeeEl.textContent = "$0";
    } else {
      cartShippingFeeEl.textContent = `${formatMoney(shippingCost)} (Cadetería)`;
    }
  }
  if (cartTotalSumEl) cartTotalSumEl.textContent = formatMoney(finalTotal);
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
    if (AppState.viewMode === "list") {
      gridEl.classList.add("list-view");
    } else {
      gridEl.classList.remove("list-view");
    }
  }

  if (gridBtn && listBtn) {
    if (AppState.viewMode === "list") {
      listBtn.classList.add("active");
      gridBtn.classList.remove("active");
    } else {
      gridBtn.classList.add("active");
      listBtn.classList.remove("active");
    }
  }
}

// Fallback de imagen para productos que no posean foto específica
function handleProductImgError(img, category) {
  img.onerror = null;
  img.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 160" width="160" height="160"><rect width="160" height="160" fill="%230d1117"/><circle cx="80" cy="80" r="50" fill="%2317202e"/><path d="M72 35h16v20l12 25v45H60V80l12-25V35z" fill="none" stroke="%233ca1a4" stroke-width="3.5" stroke-linecap="round"/><circle cx="80" cy="98" r="10" fill="%23e5aa38" opacity="0.8"/><path d="M68 132h24" stroke="%23e5aa38" stroke-width="3" stroke-linecap="round"/></svg>';
}

// ==========================================================================
// CHECKOUT & GENERACIÓN DE PEDIDO WHATSAPP
// ==========================================================================
function openCheckoutModal() {
  const modal = document.getElementById("checkoutModal");
  if (modal) modal.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeCheckoutModal() {
  const modal = document.getElementById("checkoutModal");
  if (modal) modal.classList.remove("active");
  document.body.style.overflow = "";
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
    if (pickupBox) pickupBox.style.display = "block";
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
  const address = document.getElementById("customerAddress") ? document.getElementById("customerAddress").value.trim() : "";
  const payment = document.getElementById("paymentMethod").value;
  const notes = document.getElementById("orderNotes").value.trim();

  const subtotal = AppState.cart.reduce((sum, item) => sum + (item.price > 0 ? item.price * item.quantity : 0), 0);
  const isDelivery = AppState.deliveryMethod === "envio";
  const shippingCost = isDelivery ? STORE_CONFIG.deliveryFee : 0;
  const total = subtotal + shippingCost;
  const inquiryCode = `COT-${Date.now().toString().slice(-5)}`;

  // Armar Mensaje para WhatsApp con encuadre legal de cotización/disponibilidad
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
    const lineTotalStr = item.price > 0 ? formatMoney(item.price * item.quantity) : "A consultar";
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

  // Abrir WhatsApp
  const phone = STORE_CONFIG.whatsappNumber;
  const encoded = encodeURIComponent(message);
  const whatsappUrl = `https://wa.me/${phone}?text=${encoded}`;

  window.open(whatsappUrl, "_blank");

  // Limpiar y cerrar
  clearCart();
  closeCheckoutModal();
  showToast("¡Consulta de stock enviada por WhatsApp! 📲");
}

// ==========================================================================
// CONTROLADORES: BOTÓN DE ARREPENTIMIENTO (Res. 424/2020)
// ==========================================================================
function openRegretModal() {
  const modal = document.getElementById("regretModal");
  if (modal) modal.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeRegretModal() {
  const modal = document.getElementById("regretModal");
  if (modal) modal.classList.remove("active");
  document.body.style.overflow = "";
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

  const phone = STORE_CONFIG.whatsappNumber;
  const encoded = encodeURIComponent(message);
  const whatsappUrl = `https://wa.me/${phone}?text=${encoded}`;

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
  document.body.style.overflow = "hidden";
}

function closePrivacyModal() {
  const modal = document.getElementById("privacyModal");
  if (modal) modal.classList.remove("active");
  document.body.style.overflow = "";
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
