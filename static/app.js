/**
 * Merchant Intelligence Router — Frontend Logic & Interactive Simulation
 */

// Initialize Lucide Icons
document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }
  selectDomain("analytics");
});

// View Mode Toggle (Simple View vs. Technical View)
function setViewMode(mode) {
  const body = document.body;
  const simpleBtn = document.getElementById("simpleViewBtn");
  const techBtn = document.getElementById("techViewBtn");

  if (mode === "tech") {
    body.classList.remove("simple-mode");
    body.classList.add("tech-mode");
    techBtn.className = "px-3 py-1.5 rounded-lg transition-all bg-white text-blue-700 shadow-sm flex items-center space-x-1.5";
    simpleBtn.className = "px-3 py-1.5 rounded-lg transition-all text-slate-600 hover:text-slate-900 flex items-center space-x-1.5";
  } else {
    body.classList.remove("tech-mode");
    body.classList.add("simple-mode");
    simpleBtn.className = "px-3 py-1.5 rounded-lg transition-all bg-white text-blue-700 shadow-sm flex items-center space-x-1.5";
    techBtn.className = "px-3 py-1.5 rounded-lg transition-all text-slate-600 hover:text-slate-900 flex items-center space-x-1.5";
  }
}

// Preset Query Helpers
function setHeroQuery(query) {
  const heroInput = document.getElementById("heroInput");
  if (heroInput) {
    heroInput.value = query;
    heroInput.focus();
  }
}

function setSimQuery(query) {
  const simInput = document.getElementById("simInput");
  if (simInput) {
    simInput.value = query;
    runLiveSimulation();
  }
}

function runSimulationFromHero() {
  const heroInput = document.getElementById("heroInput");
  const simInput = document.getElementById("simInput");
  if (heroInput && simInput) {
    simInput.value = heroInput.value;
    document.getElementById("live-demo").scrollIntoView({ behavior: "smooth" });
    setTimeout(() => {
      runLiveSimulation();
    }, 600);
  }
}

// Domain Tab Explorer
const DOMAIN_DATA = {
  analytics: {
    title: "📊 Analytics Intelligence",
    scope: "Tracks sales volumes, revenue fluctuations, average order values, and day-over-day growth trends.",
    questions: [
      "Why were my sales low yesterday?",
      "How much did I sell today?",
      "Compare revenue between yesterday and today"
    ],
    mockPreview: `
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
          <div class="text-xs text-slate-500 font-medium">Yesterday's Revenue</div>
          <div class="text-2xl font-bold text-slate-900 mt-1">₹31,200</div>
          <div class="text-xs text-rose-600 font-semibold mt-1">📉 -44.68% vs previous day</div>
        </div>
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
          <div class="text-xs text-slate-500 font-medium">Total Orders Yesterday</div>
          <div class="text-2xl font-bold text-slate-900 mt-1">41 orders</div>
          <div class="text-xs text-rose-600 font-semibold mt-1">📉 -47.44% volume drop</div>
        </div>
        <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
          <div class="text-xs text-slate-500 font-medium">Average Order Value</div>
          <div class="text-2xl font-bold text-slate-900 mt-1">₹760.98</div>
          <div class="text-xs text-emerald-600 font-semibold mt-1">📈 +5.2% basket size</div>
        </div>
      </div>
    `
  },
  products: {
    title: "📦 Product Performance Intelligence",
    scope: "Ranks catalog SKUs strictly by units sold, margin profitability, and customer satisfaction ratings.",
    questions: [
      "Show me my top 5 products",
      "Which product sells the most?",
      "What is my highest-rated item?"
    ],
    mockPreview: `
      <div class="space-y-2 text-xs">
        <div class="p-3 bg-white border border-slate-200 rounded-xl flex items-center justify-between">
          <div><span class="font-bold text-slate-900">1. Organic Green Tea (250g)</span> <span class="text-slate-500">(Beverages)</span></div>
          <div class="font-mono font-bold text-blue-600">1,240 units sold | ₹450 | ⭐ 4.8</div>
        </div>
        <div class="p-3 bg-white border border-slate-200 rounded-xl flex items-center justify-between">
          <div><span class="font-bold text-slate-900">2. Cold-Pressed Mustard Oil (1L)</span> <span class="text-slate-500">(Cooking)</span></div>
          <div class="font-mono font-bold text-blue-600">980 units sold | ₹280 | ⭐ 4.6</div>
        </div>
        <div class="p-3 bg-white border border-slate-200 rounded-xl flex items-center justify-between">
          <div><span class="font-bold text-slate-900">3. Whole Wheat Atta (5kg)</span> <span class="text-slate-500">(Staples)</span></div>
          <div class="font-mono font-bold text-blue-600">850 units sold | ₹310 | ⭐ 4.5</div>
        </div>
      </div>
    `
  },
  customers: {
    title: "👥 Customer Retention & VIP Intelligence",
    scope: "Identifies repeat buyers, total lifetime spend, geographic clustering, and customer segments.",
    questions: [
      "Who are my best customers?",
      "Which customers bought from me most?",
      "Show repeat customer accounts"
    ],
    mockPreview: `
      <div class="space-y-2 text-xs">
        <div class="p-3 bg-white border border-slate-200 rounded-xl flex items-center justify-between">
          <div><span class="font-bold text-slate-900">1. Aarav Sharma</span> <span class="text-slate-500">(Mumbai)</span></div>
          <div class="font-mono font-bold text-emerald-600">₹42,500 spent | 28 orders [VIP]</div>
        </div>
        <div class="p-3 bg-white border border-slate-200 rounded-xl flex items-center justify-between">
          <div><span class="font-bold text-slate-900">2. Priya Patel</span> <span class="text-slate-500">(Ahmedabad)</span></div>
          <div class="font-mono font-bold text-emerald-600">₹31,800 spent | 22 orders [VIP]</div>
        </div>
        <div class="p-3 bg-white border border-slate-200 rounded-xl flex items-center justify-between">
          <div><span class="font-bold text-slate-900">3. Rohan Gupta</span> <span class="text-slate-500">(Delhi)</span></div>
          <div class="font-mono font-bold text-emerald-600">₹19,400 spent | 15 orders [Regular]</div>
        </div>
      </div>
    `
  },
  inventory: {
    title: "📋 Inventory Health & Stock Warnings",
    scope: "Monitors real-time warehouse quantities against reorder thresholds to prevent stockouts.",
    questions: [
      "Which products are low in stock?",
      "How much inventory do I have?",
      "What should I reorder today?"
    ],
    mockPreview: `
      <div class="space-y-2 text-xs">
        <div class="p-3 bg-rose-50 border border-rose-200 rounded-xl flex items-center justify-between text-rose-900">
          <div><span class="font-bold">🔴 Alphonso Mango Pulp (850g)</span></div>
          <div class="font-mono font-bold">0 units left (OUT OF STOCK) | Reorder: 10</div>
        </div>
        <div class="p-3 bg-amber-50 border border-amber-200 rounded-xl flex items-center justify-between text-amber-900">
          <div><span class="font-bold">⚠️ Whole Wheat Atta (5kg)</span></div>
          <div class="font-mono font-bold">4 units left (CRITICAL) | Reorder: 20</div>
        </div>
        <div class="p-3 bg-amber-50 border border-amber-200 rounded-xl flex items-center justify-between text-amber-900">
          <div><span class="font-bold">⚠️ Organic Green Tea (250g)</span></div>
          <div class="font-mono font-bold">18 units left (LOW STOCK) | Reorder: 30</div>
        </div>
      </div>
    `
  },
  support: {
    title: "🆘 Support & Ambiguity Clarification",
    scope: "Intercepts general troubleshooting, dashboard tutorials, and low-confidence inputs with guided options.",
    questions: [
      "Help me use the dashboard",
      "How does this assistant work?",
      "Tell me about my business (Ambiguous input)"
    ],
    mockPreview: `
      <div class="p-4 bg-white border border-slate-200 rounded-2xl text-xs space-y-2">
        <div class="font-bold text-slate-900">Guided Capabilities Menu:</div>
        <div class="text-slate-600">• 📊 <strong>Analytics</strong>: Period-over-period sales and revenue fluctuations</div>
        <div class="text-slate-600">• 📦 <strong>Products</strong>: Best-selling SKU rankings and volume performance</div>
        <div class="text-slate-600">• 👥 <strong>Customers</strong>: VIP buyer retention and purchase history</div>
        <div class="text-slate-600">• 📋 <strong>Inventory</strong>: Low stock alerts and reorder thresholds</div>
      </div>
    `
  }
};

function selectDomain(domainKey) {
  const tabs = document.querySelectorAll(".domain-tab");
  tabs.forEach((tab) => {
    tab.className = "domain-tab p-3.5 rounded-2xl border border-slate-200 text-slate-700 hover:bg-slate-50 font-bold text-sm transition-all";
  });

  const activeTab = document.getElementById(`tab-${domainKey}`);
  if (activeTab) {
    activeTab.className = "domain-tab p-3.5 rounded-2xl border text-center transition-all bg-blue-600 text-white font-bold text-sm shadow-md";
  }

  const container = document.getElementById("domainContent");
  const data = DOMAIN_DATA[domainKey];
  if (container && data) {
    container.innerHTML = `
      <div class="mb-6">
        <h3 class="text-xl font-bold text-slate-900">${data.title}</h3>
        <p class="text-sm text-slate-600 mt-1">${data.scope}</p>
      </div>

      <div class="mb-6">
        <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Representative Merchant Inquiries:</div>
        <div class="flex flex-wrap gap-2">
          ${data.questions.map(q => `<span class="px-3 py-1.5 bg-white border border-slate-200 rounded-xl text-xs text-slate-700 font-medium">"${q}"</span>`).join("")}
        </div>
      </div>

      <div>
        <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Live Deterministic Data Preview:</div>
        ${data.mockPreview}
      </div>
    `;
  }
}

// Live Interactive Pipeline Simulation
async function runLiveSimulation() {
  const inputEl = document.getElementById("simInput");
  const btn = document.getElementById("simRunBtn");
  const query = inputEl ? inputEl.value.trim() : "";
  if (!query) return;

  btn.disabled = true;
  btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Running...</span>`;
  if (window.lucide) window.lucide.createIcons();

  resetStepUI();

  try {
    // 1. Ingestion Step
    await highlightStep(1, "processing", "Normalizing & Expanding...");
    await new Promise(r => setTimeout(r, 200));
    await highlightStep(1, "complete", "✓ Normalized");

    // Try backend API call first
    let result = null;
    try {
      const response = await fetch("/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: query })
      });
      if (response.ok) {
        result = await response.json();
      }
    } catch (e) {
      console.warn("Backend API not reachable, falling back to local simulation engine", e);
    }

    // Fallback simulation if running standalone static
    if (!result) {
      result = simulateLocalPipeline(query);
    }

    // 2. Classifier Step
    await highlightStep(2, "processing", "Computing Cosine Sim...");
    await new Promise(r => setTimeout(r, 250));
    await highlightStep(2, "complete", `✓ ${result.intent.toUpperCase()} (${Math.round(result.confidence * 100)}%)`);

    // 3. Confidence Gate Step
    await highlightStep(3, "processing", "Comparing vs 0.70...");
    await new Promise(r => setTimeout(r, 200));
    if (result.passes_threshold) {
      await highlightStep(3, "complete", "✓ &ge; 0.70 (Accepted)");
    } else {
      await highlightStep(3, "warning", "⚠️ &lt; 0.70 (Diverted to Support)");
    }

    // 4. LangGraph Transition Step
    await highlightStep(4, "processing", `Routing to ${result.routed_node}...`);
    await new Promise(r => setTimeout(r, 200));
    await highlightStep(4, "complete", `✓ Node: ${result.routed_node}`);

    // 5. Business Logic Step
    await highlightStep(5, "processing", "Executing Deterministic Math...");
    await new Promise(r => setTimeout(r, 250));
    await highlightStep(5, "complete", "✓ Calculated");

    // Update Output Panels
    renderSimulationResult(result);

  } catch (err) {
    console.error("Simulation error:", err);
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<i data-lucide="play" class="w-4 h-4"></i><span>Simulate</span>`;
    if (window.lucide) window.lucide.createIcons();
  }
}

function resetStepUI() {
  for (let i = 1; i <= 5; i++) {
    const el = document.getElementById(`step-${i}`);
    if (el) {
      el.className = "step-node p-3.5 bg-white border border-slate-200 rounded-2xl flex items-center justify-between transition-all";
      const status = el.querySelector(".step-status");
      if (status) {
        status.className = "step-status text-xs font-mono text-slate-400";
        status.textContent = "Pending";
      }
    }
  }
}

async function highlightStep(stepNum, status, label) {
  const el = document.getElementById(`step-${stepNum}`);
  if (!el) return;
  const statusSpan = el.querySelector(".step-status");
  const badge = el.querySelector(".step-badge");

  if (status === "processing") {
    el.className = "step-node p-3.5 bg-blue-50 border border-blue-400 rounded-2xl flex items-center justify-between active-pulse transition-all";
    if (badge) badge.className = "step-badge w-7 h-7 rounded-full bg-blue-600 text-white font-mono text-xs flex items-center justify-center font-bold animate-spin";
    if (statusSpan) {
      statusSpan.className = "step-status text-xs font-mono text-blue-600 font-bold";
      statusSpan.textContent = label;
    }
  } else if (status === "complete") {
    el.className = "step-node p-3.5 bg-emerald-50/70 border border-emerald-300 rounded-2xl flex items-center justify-between transition-all";
    if (badge) badge.className = "step-badge w-7 h-7 rounded-full bg-emerald-600 text-white font-mono text-xs flex items-center justify-center font-bold";
    if (statusSpan) {
      statusSpan.className = "step-status text-xs font-mono text-emerald-700 font-bold";
      statusSpan.textContent = label;
    }
  } else if (status === "warning") {
    el.className = "step-node p-3.5 bg-amber-50 border border-amber-400 rounded-2xl flex items-center justify-between transition-all";
    if (badge) badge.className = "step-badge w-7 h-7 rounded-full bg-amber-600 text-white font-mono text-xs flex items-center justify-center font-bold";
    if (statusSpan) {
      statusSpan.className = "step-status text-xs font-mono text-amber-700 font-bold";
      statusSpan.textContent = label;
    }
  }
}

function renderSimulationResult(result) {
  const replyEl = document.getElementById("simReplyText");
  const intentBadge = document.getElementById("simBadgeIntent");
  const confVal = document.getElementById("simConfidenceVal");
  const confBar = document.getElementById("simConfidenceBar");
  const jsonTrace = document.getElementById("simJsonTrace");

  if (replyEl) replyEl.textContent = result.reply;
  if (intentBadge) {
    intentBadge.textContent = `intent: ${result.intent}`;
    if (result.passes_threshold) {
      intentBadge.className = "text-xs font-mono px-2.5 py-1 bg-blue-500/20 text-blue-300 rounded border border-blue-500/30";
    } else {
      intentBadge.className = "text-xs font-mono px-2.5 py-1 bg-amber-500/20 text-amber-300 rounded border border-amber-500/30";
    }
  }
  if (confVal) confVal.textContent = `${result.confidence.toFixed(2)} / 1.00`;
  if (confBar) {
    confBar.style.width = `${Math.min(100, Math.round(result.confidence * 100))}%`;
    if (result.passes_threshold) {
      confBar.className = "bg-gradient-to-r from-blue-500 to-emerald-400 h-full transition-all duration-500";
    } else {
      confBar.className = "bg-gradient-to-r from-amber-500 to-rose-400 h-full transition-all duration-500";
    }
  }
  if (jsonTrace) {
    jsonTrace.textContent = JSON.stringify(result, null, 2);
  }
}

// Deterministic Local Fallback Engine for instant offline simulation
function simulateLocalPipeline(msg) {
  const lower = msg.toLowerCase();
  
  if (lower.includes("business") || lower.includes("useful") || lower.includes("update") || lower.includes("history")) {
    return {
      message: msg,
      intent: "support",
      confidence: 0.45,
      threshold: 0.70,
      passes_threshold: false,
      routed_node: "support",
      reply: "🤔 I'm not entirely sure how to handle your query (Confidence: 45%).\nHere are the specific areas I can help you with:\n\n1. 📊 Analytics: Ask 'Why were sales low yesterday?' or 'Show my revenue trend'.\n2. 📦 Products: Ask 'What are my top 5 products?' or 'Show best sellers'.\n3. 👥 Customers: Ask 'Who are my best customers?' or 'Show repeat buyers'.\n4. 📋 Inventory: Ask 'How much stock do I have?' or 'Show low inventory items'.\n5. ❓ Support: Ask 'How do I use this dashboard?' for system navigation.",
      structured_query: { metric: null, time_period: "current_period", entity: "overall_business" }
    };
  }

  if (lower.includes("sale") || lower.includes("revenue") || lower.includes("yesterday") || lower.includes("sell")) {
    return {
      message: msg,
      intent: "analytics",
      confidence: 0.94,
      threshold: 0.70,
      passes_threshold: true,
      routed_node: "analytics",
      reply: "📊 Sales Analytics Summary:\n• Yesterday (2026-10-01), your revenue was ₹31,200 across 41 orders.\n• Compared to the previous day (2026-09-30 at ₹56,400), revenue saw a drop of 44.7%.\n• Order volume also saw a drop of 47.4% (Avg order value: ₹760.98).",
      structured_query: { metric: "sales_revenue", time_period: "yesterday", entity: "underperforming_or_alerts" },
      data: { revenue_pct_change: -44.68, orders_pct_change: -47.44 }
    };
  }

  if (lower.includes("product") || lower.includes("item") || lower.includes("sku") || lower.includes("catalog")) {
    return {
      message: msg,
      intent: "products",
      confidence: 0.93,
      threshold: 0.70,
      passes_threshold: true,
      routed_node: "products",
      reply: "📦 Top Best-Selling Products:\n  1. Organic Green Tea (250g) (Beverages): 1,240 units sold | Price: ₹450 | Rating: ⭐ 4.8\n  2. Cold-Pressed Mustard Oil (1L) (Cooking): 980 units sold | Price: ₹280 | Rating: ⭐ 4.6\n  3. Whole Wheat Atta (5kg) (Staples): 850 units sold | Price: ₹310 | Rating: ⭐ 4.5\n  4. Raw Wildflower Honey (500g) (Sweeteners): 620 units sold | Price: ₹520 | Rating: ⭐ 4.9\n  5. Alphonso Mango Pulp (850g) (Preserves): 410 units sold | Price: ₹390 | Rating: ⭐ 4.7",
      structured_query: { metric: "products", time_period: "current_period", entity: "top_performers" }
    };
  }

  if (lower.includes("customer") || lower.includes("buyer") || lower.includes("repeat") || lower.includes("client")) {
    return {
      message: msg,
      intent: "customers",
      confidence: 0.91,
      threshold: 0.70,
      passes_threshold: true,
      routed_node: "customers",
      reply: "👥 Top Customers by Total Spend:\n  1. Aarav Sharma (Mumbai) - ₹42,500 across 28 orders [VIP]\n  2. Priya Patel (Ahmedabad) - ₹31,800 across 22 orders [VIP]\n  3. Rohan Gupta (Delhi) - ₹19,400 across 15 orders [Regular]\n  4. Sneha Iyer (Bengaluru) - ₹14,200 across 12 orders [Regular]\n  5. Vikram Singh (Jaipur) - ₹3,100 across 3 orders [New]",
      structured_query: { metric: "customers", time_period: "current_period", entity: "top_performers" }
    };
  }

  if (lower.includes("stock") || lower.includes("inventory") || lower.includes("reorder") || lower.includes("quantity")) {
    return {
      message: msg,
      intent: "inventory",
      confidence: 0.92,
      threshold: 0.70,
      passes_threshold: true,
      routed_node: "inventory",
      reply: "📋 Inventory Status Overview:\n• Total catalog items: 5 (149 total units in stock).\n• Items requiring attention:\n  ⚠️ Organic Green Tea (250g): 18 units left (Reorder threshold: 30)\n  ⚠️ Whole Wheat Atta (5kg): 4 units left (Reorder threshold: 20)\n  🔴 Alphonso Mango Pulp (850g): OUT OF STOCK (Reorder threshold: 10)\n\n💡 Action needed: Please reorder items marked with 🔴 and ⚠️ promptly.",
      structured_query: { metric: "inventory", time_period: "current_period", entity: "underperforming_or_alerts" }
    };
  }

  return {
    message: msg,
    intent: "support",
    confidence: 0.88,
    threshold: 0.70,
    passes_threshold: true,
    routed_node: "support",
    reply: "👋 VyaparMitra Merchant Assistant Help Center:\nI can analyze your business data and answer questions across these areas:\n\n1. 📊 Analytics: Ask 'Why were sales low yesterday?' or 'Show my revenue trend'.\n2. 📦 Products: Ask 'What are my top 5 products?' or 'Show best sellers'.\n3. 👥 Customers: Ask 'Who are my best customers?' or 'Show repeat buyers'.\n4. 📋 Inventory: Ask 'How much stock do I have?' or 'Show low inventory items'.\n5. ❓ Support: Ask 'How do I use this dashboard?' for system navigation."
  };
}
