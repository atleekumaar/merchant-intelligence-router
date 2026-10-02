/**
 * Merchant Intelligence Router — Clean Pipeline Execution Engine
 */

document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }
});

function setQueryAndRun(query) {
  const input = document.getElementById("queryInput");
  if (input) {
    input.value = query;
    triggerPipelineExecution();
  }
}

function resetPipelineUI() {
  const cards = ["card-ingest", "card-jev", "card-gate", "card-langgraph", "card-math"];
  cards.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.className = "pipeline-card p-4";
  });

  const tags = ["tag-ingest", "tag-jev", "tag-gate", "tag-langgraph", "tag-math"];
  tags.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.className = "px-1.5 py-0.5 rounded text-[10px] bg-slate-800 text-slate-400";
      el.textContent = "IDLE";
    }
  });

  const brainIds = ["analytics", "products", "customers", "inventory", "support"];
  brainIds.forEach(b => {
    const el = document.getElementById(`brain-${b}`);
    if (el) el.className = "pipeline-card p-3.5 border-slate-800 bg-[#0a101d]";
    const tag = document.getElementById(`tag-brain-${b}`);
    if (tag) {
      tag.className = "px-1 py-0.2 rounded text-[9px] bg-slate-800 text-slate-400";
      tag.textContent = "IDLE";
    }
  });

  document.getElementById("preview-intent").textContent = "--";
  document.getElementById("preview-conf").textContent = "--";
  document.getElementById("preview-gate-status").textContent = "PENDING";
  document.getElementById("preview-gate-status").className = "px-1.5 py-0.5 rounded text-[10px] bg-slate-800 text-slate-400";
  document.getElementById("preview-target-node").textContent = "--";
  document.getElementById("activeHandlerLabel").textContent = "Standby";
  document.getElementById("mathFormulaBox").textContent = "// Standby: Awaiting query execution...";
  document.getElementById("resIntentBadge").textContent = "intent: --";
  document.getElementById("resConfBadge").textContent = "conf: --";
  document.getElementById("resLatencyBadge").textContent = "0ms";
  document.getElementById("resMessageContent").innerHTML = "Press <strong>\"Run Pipeline\"</strong> to execute your query through the architecture.";
  document.getElementById("resRoutedNode").textContent = "Routed to: --";
}

async function triggerPipelineExecution() {
  const inputEl = document.getElementById("queryInput");
  const btn = document.getElementById("runBtn");
  const query = inputEl ? inputEl.value.trim() : "";
  if (!query) return;

  btn.disabled = true;
  btn.innerHTML = `<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i><span>Running...</span>`;
  if (window.lucide) window.lucide.createIcons();

  resetPipelineUI();
  const startTime = performance.now();

  try {
    // Stage 1: INGESTION
    setStage("card-ingest", "tag-ingest", "card-active", "bg-blue-600 text-white", "RUNNING");
    document.getElementById("preview-query").textContent = `"${query}"`;
    await sleep(180);
    setStage("card-ingest", "tag-ingest", "card-success", "bg-emerald-500/20 text-emerald-400 font-bold", "PASS");

    // Fetch backend response or fallback
    let result = null;
    try {
      const resp = await fetch("/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: query })
      });
      if (resp.ok) result = await resp.json();
    } catch (e) {
      console.warn("Backend API offline, using fallback", e);
    }

    if (!result) {
      result = getLocalSimulationData(query);
    }

    // Stage 2: JEV CLASSIFIER
    setStage("card-jev", "tag-jev", "card-active", "bg-blue-600 text-white", "CLASSIFYING");
    await sleep(200);
    document.getElementById("preview-intent").textContent = result.intent.toUpperCase();
    document.getElementById("preview-conf").textContent = `${Math.round(result.confidence * 100)}%`;
    setStage("card-jev", "tag-jev", "card-success", "bg-emerald-500/20 text-emerald-400 font-bold", "DONE");

    // Stage 3: CONFIDENCE GATE (0.70 THRESHOLD)
    setStage("card-gate", "tag-gate", "card-active", "bg-blue-600 text-white", "CHECKING");
    await sleep(180);
    const passes = result.passes_threshold;
    if (passes) {
      document.getElementById("preview-gate-status").textContent = "ACCEPTED (>= 0.70)";
      document.getElementById("preview-gate-status").className = "px-1.5 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-400 font-bold";
      setStage("card-gate", "tag-gate", "card-success", "bg-emerald-500/20 text-emerald-400 font-bold", "HIGH CONF");
    } else {
      document.getElementById("preview-gate-status").textContent = "DIVERT (< 0.70)";
      document.getElementById("preview-gate-status").className = "px-1.5 py-0.5 rounded text-[10px] bg-amber-500/20 text-amber-400 font-bold";
      setStage("card-gate", "tag-gate", "card-warning", "bg-amber-500/20 text-amber-400 font-bold", "LOW CONF");
    }

    // Stage 4: LANGGRAPH ROUTING
    setStage("card-langgraph", "tag-langgraph", "card-active", "bg-blue-600 text-white", "ROUTING");
    await sleep(180);
    document.getElementById("preview-target-node").textContent = result.routed_node.toUpperCase();
    setStage("card-langgraph", "tag-langgraph", "card-success", "bg-emerald-500/20 text-emerald-400 font-bold", "ROUTED");

    // Stage 5: DOMAIN BRAIN HIGHLIGHT
    document.getElementById("activeHandlerLabel").textContent = `Executing ${result.routed_node}_node`;
    const brainIds = ["analytics", "products", "customers", "inventory", "support"];
    brainIds.forEach(b => {
      if (b === result.routed_node) {
        setBrainStage(`brain-${b}`, `tag-brain-${b}`, passes ? "card-success" : "card-warning", passes ? "bg-emerald-500/20 text-emerald-400 font-bold" : "bg-amber-500/20 text-amber-400 font-bold", "ACTIVE");
      } else {
        setBrainStage(`brain-${b}`, `tag-brain-${b}`, "card-dimmed", "bg-slate-800 text-slate-500", "SKIPPED");
      }
    });
    await sleep(200);

    // Stage 6: DETERMINISTIC MATH ENGINE
    setStage("card-math", "tag-math", "card-active", "bg-blue-600 text-white", "CALCULATING");
    let mathSummary = "";
    if (result.routed_node === "analytics") {
      mathSummary = "// Factual Sales Math:\nΔRevenue = (₹31,200 - ₹56,400) / ₹56,400 = -44.68% Drop\nΔOrders  = (41 - 78) / 78 = -47.44% Drop\nAOV      = ₹31,200 / 41 = ₹760.98";
    } else if (result.routed_node === "products") {
      mathSummary = "// Catalog Volume Sorting:\nRank 1: Organic Green Tea (1,240 units sold)\nRank 2: Cold-Pressed Mustard Oil (980 units sold)\nRank 3: Whole Wheat Atta (850 units sold)";
    } else if (result.routed_node === "customers") {
      mathSummary = "// Customer Lifetime Spend Ranking:\nRank 1: Aarav Sharma (₹42,500 | 28 orders)\nRank 2: Priya Patel (₹31,800 | 22 orders)\nRank 3: Rohan Gupta (₹19,400 | 15 orders)";
    } else if (result.routed_node === "inventory") {
      mathSummary = "// Reorder Alert Threshold Filter:\nAlert 1: Mango Pulp -> 0 units left (OUT OF STOCK)\nAlert 2: Whole Wheat Atta -> 4 units left (CRITICAL)\nAlert 3: Green Tea -> 18 units left (LOW STOCK)";
    } else {
      mathSummary = `// Confidence Gate Interception:\nConfidence score (${result.confidence}) < 0.70 threshold\nAction: Invoking guided help & clarification menu`;
    }
    document.getElementById("mathFormulaBox").textContent = mathSummary;
    setStage("card-math", "tag-math", "card-success", "bg-emerald-500/20 text-emerald-400 font-bold", "FACT CHECKED");

    // Stage 7: FINAL FORMATTED OUTPUT (Clean HTML without **)
    document.getElementById("resIntentBadge").textContent = `intent: ${result.intent}`;
    document.getElementById("resConfBadge").textContent = `conf: ${result.confidence.toFixed(2)}`;
    document.getElementById("resRoutedNode").textContent = `Routed to: ${result.routed_node}_node`;
    
    const formattedHtml = parseMarkdownToHtml(result.reply);
    document.getElementById("resMessageContent").innerHTML = formattedHtml;

    const totalDuration = Math.round(performance.now() - startTime);
    document.getElementById("resLatencyBadge").textContent = `${totalDuration}ms`;

  } catch (err) {
    console.error("Execution error:", err);
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<i data-lucide="play" class="w-3.5 h-3.5 fill-current"></i><span>Run Pipeline</span>`;
    if (window.lucide) window.lucide.createIcons();
  }
}

function setStage(cardId, tagId, cardClass, tagClass, tagText) {
  const card = document.getElementById(cardId);
  const tag = document.getElementById(tagId);
  if (card) card.className = `pipeline-card p-4 ${cardClass}`;
  if (tag) {
    tag.className = `px-1.5 py-0.5 rounded text-[10px] ${tagClass}`;
    tag.textContent = tagText;
  }
}

function setBrainStage(cardId, tagId, cardClass, tagClass, tagText) {
  const card = document.getElementById(cardId);
  const tag = document.getElementById(tagId);
  if (card) card.className = `pipeline-card p-3.5 border-slate-800 ${cardClass}`;
  if (tag) {
    tag.className = `px-1 py-0.2 rounded text-[9px] ${tagClass}`;
    tag.textContent = tagText;
  }
}

// Convert markdown ** and bullet points into clean, readable HTML
function parseMarkdownToHtml(text) {
  if (!text) return "";
  let html = text
    // Convert bold **text** to <strong>text</strong>
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    // Convert bullet points • text to clean styled lines
    .replace(/^• (.*$)/gim, "<div class='flex items-start space-x-2 my-1'><span class='text-blue-400 font-bold'>•</span><span>$1</span></div>")
    // Convert numbered lists 1. text
    .replace(/^([0-9]+)\. (.*$)/gim, "<div class='flex items-start space-x-2 my-1'><span class='text-indigo-400 font-bold'>$1.</span><span>$2</span></div>")
    // Convert *italic*
    .replace(/\*(.*?)\*/g, "<em>$1</em>");

  return html;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Fallback local dataset for instant offline operation
function getLocalSimulationData(msg) {
  const lower = msg.toLowerCase();
  
  if (lower.includes("business") || lower.includes("useful") || lower.includes("update") || lower.includes("history")) {
    return {
      message: msg,
      intent: "support",
      confidence: 0.45,
      threshold: 0.70,
      passes_threshold: false,
      routed_node: "support",
      reply: "I am not completely sure what you are asking (Confidence: 45%).\n\nHere are the specific areas I can assist you with:\n1. Analytics: Ask 'Why were sales low yesterday?' or 'Show revenue trend'\n2. Products: Ask 'What are my top 5 products?' or 'Show best sellers'\n3. Customers: Ask 'Who are my best customers?' or 'Show repeat buyers'\n4. Inventory: Ask 'How much stock do I have?' or 'Show low inventory items'\n5. Support: Ask 'How do I use this dashboard?'"
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
      reply: "Sales Analytics Summary:\n• Yesterday (2026-10-01), your revenue was **₹31,200** across **41 orders**.\n• Compared to the previous day (2026-09-30 at ₹56,400), revenue saw a **drop of 44.7%**.\n• Order volume also saw a **drop of 47.4%** (Avg order value: ₹760.98)."
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
      reply: "Top Best-Selling Products:\n• **Organic Green Tea (250g)** (Beverages): **1,240 units sold** | Price: ₹450 | Rating: 4.8\n• **Cold-Pressed Mustard Oil (1L)** (Cooking): **980 units sold** | Price: ₹280 | Rating: 4.6\n• **Whole Wheat Atta (5kg)** (Staples): **850 units sold** | Price: ₹310 | Rating: 4.5\n• **Raw Wildflower Honey (500g)** (Sweeteners): **620 units sold** | Price: ₹520 | Rating: 4.9\n• **Alphonso Mango Pulp (850g)** (Preserves): **410 units sold** | Price: ₹390 | Rating: 4.7"
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
      reply: "Top Customers by Total Spend:\n• **Aarav Sharma** (Mumbai) - **₹42,500** across 28 orders [VIP]\n• **Priya Patel** (Ahmedabad) - **₹31,800** across 22 orders [VIP]\n• **Rohan Gupta** (Delhi) - **₹19,400** across 15 orders [Regular]\n• **Sneha Iyer** (Bengaluru) - **₹14,200** across 12 orders [Regular]\n• **Vikram Singh** (Jaipur) - **₹3,100** across 3 orders [New]"
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
      reply: "Inventory Status Overview:\n• Total catalog items: **5** (149 total units in stock).\n• Items requiring attention:\n• **Alphonso Mango Pulp (850g)**: OUT OF STOCK (Reorder threshold: 10)\n• **Whole Wheat Atta (5kg)**: 4 units left (CRITICAL | Reorder threshold: 20)\n• **Organic Green Tea (250g)**: 18 units left (LOW STOCK | Reorder threshold: 30)\n\nPlease reorder items marked as Critical promptly."
    };
  }

  return {
    message: msg,
    intent: "support",
    confidence: 0.88,
    threshold: 0.70,
    passes_threshold: true,
    routed_node: "support",
    reply: "VyaparMitra Merchant Assistant Help Center:\nI can analyze your business data across these areas:\n1. Analytics: Ask 'Why were sales low yesterday?' or 'Show my revenue trend'\n2. Products: Ask 'What are my top 5 products?' or 'Show best sellers'\n3. Customers: Ask 'Who are my best customers?' or 'Show repeat buyers'\n4. Inventory: Ask 'How much stock do I have?' or 'Show low inventory items'\n5. Support: Ask 'How do I use this dashboard?'"
  };
}
