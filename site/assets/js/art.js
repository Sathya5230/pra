/*
 * Illustrated praline pieces, drawn as inline SVG. Product photography is real;
 * these drawings are used for flavour maps and the ballotin builder.
 * art.piece(tone, shape, deco) -> svg string.
 */
window.ART = (() => {
  let uid = 0;

  const TONES = {
    dark:  { base: "#4A2C1C", hi: "#74482F", sh: "#2B190F" },
    milk:  { base: "#8C5B3B", hi: "#B98458", sh: "#5C3923" },
    white: { base: "#EEDCBC", hi: "#FFF7E8", sh: "#CDB389" },
    caramel: { base: "#B47A43", hi: "#D7A46B", sh: "#7E4F28" },
  };
  const BG = { mixed: "#F5E6CC", dark: "#E7CFAE", milk: "#F5E6CC", white: "#F8EBD4", caramel: "#F5E6CC", truffle: "#E7CFAE", logo: "#F5E6CC" };

  function rng(seed) {
    let h = 2166136261;
    for (const ch of seed) h = Math.imul(h ^ ch.charCodeAt(0), 16777619);
    return () => {
      h ^= h << 13; h ^= h >>> 17; h ^= h << 5;
      return ((h >>> 0) % 10000) / 10000;
    };
  }

  function toneSet(palette) {
    if (palette === "dark" || palette === "truffle") return ["dark", "dark", "milk"];
    if (palette === "milk") return ["milk", "milk", "dark"];
    if (palette === "white") return ["white", "white", "milk"];
    if (palette === "caramel") return ["caramel", "milk", "dark"];
    return ["dark", "milk", "white", "milk", "caramel"];
  }

  function gradients(id) {
    return Object.entries(TONES).map(([k, t]) => `
      <radialGradient id="${id}-${k}" cx="35%" cy="30%" r="75%">
        <stop offset="0" stop-color="${t.hi}"/><stop offset=".55" stop-color="${t.base}"/><stop offset="1" stop-color="${t.sh}"/>
      </radialGradient>`).join("") + `
      <filter id="${id}-soft" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#2B190F" flood-opacity=".28"/></filter>
      <pattern id="${id}-dust" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#2B190F" opacity=".35"/><circle cx="4" cy="4" r=".6" fill="#B98458" opacity=".4"/></pattern>`;
  }

  /* One praline at (x, y) with radius r. */
  function praline(id, x, y, r, tone, shape, deco, rand) {
    const fill = `url(#${id}-${tone})`;
    const t = TONES[tone];
    let body;
    if (shape === "square") body = `<rect x="${x - r}" y="${y - r}" width="${2 * r}" height="${2 * r}" rx="${r * 0.28}" fill="${fill}"/>`;
    else if (shape === "heart") {
      const s = r / 10;
      body = `<path transform="translate(${x} ${y + s}) scale(${s})" d="M0 9C-12 0-11-9-5.5-9-2.5-9 0-6 0-4 0-6 2.5-9 5.5-9 11-9 12 0 0 9Z" fill="${fill}"/>`;
    } else if (shape === "drop") body = `<path d="M${x} ${y - r * 1.1}C${x + r * 0.9} ${y - r * 0.2} ${x + r} ${y + r} ${x} ${y + r}C${x - r} ${y + r} ${x - r * 0.9} ${y - r * 0.2} ${x} ${y - r * 1.1}Z" fill="${fill}"/>`;
    else body = `<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}"/>`;

    let top = "";
    const contrast = tone === "white" ? TONES.milk.base : tone === "dark" ? TONES.white.hi : TONES.dark.base;
    if (deco === "drizzle") {
      for (let i = -2; i <= 2; i++) top += `<path d="M${x - r * 0.75} ${y + i * r * 0.28}q${r * 0.37} ${-r * 0.18} ${r * 0.75} 0t${r * 0.75} 0" stroke="${contrast}" stroke-width="${r * 0.07}" fill="none" stroke-linecap="round" opacity=".85"/>`;
    } else if (deco === "nut") {
      top += `<ellipse cx="${x}" cy="${y - r * 0.1}" rx="${r * 0.32}" ry="${r * 0.24}" fill="#C89A63" stroke="#7E4F28" stroke-width="${r * 0.05}"/>`;
    } else if (deco === "ridge") {
      top += `<path d="M${x - r * 0.6} ${y}h${r * 1.2}M${x} ${y - r * 0.6}v${r * 1.2}" stroke="${t.sh}" stroke-width="${r * 0.08}" stroke-linecap="round" opacity=".6"/>`;
    } else if (deco === "dot") {
      top += `<circle cx="${x + r * 0.15}" cy="${y - r * 0.2}" r="${r * 0.16}" fill="${contrast}"/>`;
    } else if (deco === "dust") {
      top += shape === "square"
        ? `<rect x="${x - r}" y="${y - r}" width="${2 * r}" height="${2 * r}" rx="${r * 0.28}" fill="url(#${id}-dust)"/>`
        : `<circle cx="${x}" cy="${y}" r="${r}" fill="url(#${id}-dust)"/>`;
    } else if (deco === "logo") {
      top += `<circle cx="${x}" cy="${y}" r="${r * 0.55}" fill="none" stroke="${contrast}" stroke-width="${r * 0.07}"/><path d="M${x - r * 0.25} ${y + r * 0.22}l${r * 0.25}-${r * 0.5}l${r * 0.25} ${r * 0.5}" stroke="${contrast}" stroke-width="${r * 0.09}" fill="none" stroke-linejoin="round"/>`;
    }
    const gloss = `<ellipse cx="${x - r * 0.35}" cy="${y - r * 0.45}" rx="${r * 0.28}" ry="${r * 0.12}" fill="#fff" opacity="${tone === "white" ? 0.5 : 0.18}" transform="rotate(-25 ${x - r * 0.35} ${y - r * 0.45})"/>`;
    return `<g filter="url(#${id}-soft)">${body}</g>${top}${gloss}`;
  }

  function gridFor(n) {
    const map = { 4: [2, 2], 6: [3, 2], 9: [3, 3], 12: [4, 3], 16: [4, 4], 18: [6, 3], 20: [5, 4], 24: [6, 4], 30: [6, 5], 36: [6, 6], 64: [8, 8] };
    if (map[n]) return map[n];
    const c = Math.ceil(Math.sqrt(n));
    return [c, Math.ceil(n / c)];
  }

  function pickPraline(prod, rand) {
    const tones = toneSet(prod.palette);
    const tone = tones[Math.floor(rand() * tones.length)];
    const shapes = prod.palette === "truffle" ? ["circle"] : ["circle", "square", "circle", "heart", "drop", "square"];
    const decos = prod.palette === "truffle" ? ["dust"] : prod.palette === "logo" ? ["logo"] : ["drizzle", "nut", "ridge", "dot", "none", "drizzle"];
    return { tone, shape: shapes[Math.floor(rand() * shapes.length)], deco: decos[Math.floor(rand() * decos.length)] };
  }

  function openBox(id, prod, v, rand) {
    const n = Math.max(v.piece_count || 12, 4);
    const [cols, rows] = gridFor(Math.min(n, 64));
    const W = 300, H = Math.round(300 * (rows / cols) * 0.95 + 20);
    const x0 = 200 - W / 2, y0 = 200 - H / 2;
    const cw = (W - 24) / cols, ch = (H - 24) / rows;
    const r = Math.min(cw, ch) * 0.38;
    let cells = "";
    for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
      const cx = x0 + 12 + cw * (i + 0.5), cy = y0 + 12 + ch * (j + 0.5);
      const p = pickPraline(prod, rand);
      cells += `<rect x="${cx - cw / 2 + 3}" y="${cy - ch / 2 + 3}" width="${cw - 6}" height="${ch - 6}" rx="6" fill="#D9BC92" opacity=".55"/>`;
      cells += praline(id, cx, cy, r, p.tone, p.shape, p.deco, rand);
    }
    return `<rect x="${x0 - 8}" y="${y0 - 8}" width="${W + 16}" height="${H + 16}" rx="14" fill="${prod.lid}"/>
      <rect x="${x0}" y="${y0}" width="${W}" height="${H}" rx="9" fill="#EBD3AE"/>${cells}`;
  }

  function closedBox(id, prod) {
    const light = ["#FFF7E8", "#F5E6CC", "#E7CFAE", "#93B79B", "#E3A99A", "#B98458"].includes(prod.lid);
    const ink = light ? "#3D2617" : "#FFF7E8";
    return `<g transform="rotate(-6 200 200)">
      <rect x="70" y="95" width="260" height="210" rx="16" fill="#2B190F" opacity=".18" transform="translate(8 10)"/>
      <rect x="70" y="95" width="260" height="210" rx="16" fill="${prod.lid}"/>
      <rect x="70" y="236" width="260" height="30" fill="${prod.ribbon}"/>
      <rect x="262" y="95" width="30" height="210" fill="${prod.ribbon}"/>
      <path d="M277 251c-28-32-58-20-43 0 15 17 43 0 43 0zm0 0c28-32 58-20 43 0-15 17-43 0-43 0z" fill="${prod.ribbon}" stroke="#2B190F" stroke-opacity=".2" stroke-width="2"/>
      <circle cx="277" cy="251" r="8" fill="${prod.ribbon}" stroke="#2B190F" stroke-opacity=".25" stroke-width="2"/>
            <text x="166" y="180" text-anchor="middle" font-family="'Big Shoulders Display',sans-serif" font-weight="800" font-size="30" letter-spacing="2" fill="${ink}">PRALINE</text>
      <text x="166" y="214" text-anchor="middle" font-family="'Caveat Brush',cursive" font-size="20" fill="${ink}">Bruxelles</text>
    </g>`;
  }

  function cutView(id, prod, rand) {
    const p = pickPraline(prod, rand);
    const shell = TONES[p.tone];
    const fill = prod.filling_type.includes("Caramel") ? "#C9893F" : prod.filling_type.includes("Fruit") ? "#B5474A" : prod.filling_type.includes("Praliné") || prod.filling_type.includes("Nut") ? "#A87445" : "#5A3420";
    return `<ellipse cx="200" cy="300" rx="150" ry="22" fill="#2B190F" opacity=".14"/>
      <path d="M70 280 A130 130 0 0 1 330 280 Z" fill="url(#${id}-${p.tone})"/>
      <path d="M86 280 A114 114 0 0 1 314 280 Z" fill="${fill}"/>
      <path d="M100 280 A100 100 0 0 1 300 280" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="10"/>
      <rect x="70" y="276" width="260" height="14" rx="4" fill="${shell.sh}"/>
      ${[0, 1, 2, 3, 4].map((i) => `<circle cx="${130 + i * 34 + rand() * 10}" cy="${230 - (i % 2) * 30}" r="${4 + rand() * 4}" fill="#fff" opacity=".12"/>`).join("")}
      ${praline(id, 310, 120, 42, pickPraline(prod, rand).tone, "circle", "drizzle", rand)}`;
  }

  function scattered(id, prod, rand) {
    let out = `<ellipse cx="200" cy="215" rx="170" ry="130" fill="#E7CFAE" opacity=".6"/>`;
    for (let i = 0; i < 9; i++) {
      const a = rand() * Math.PI * 2, d = 40 + rand() * 120;
      const p = pickPraline(prod, rand);
      out += praline(id, 200 + Math.cos(a) * d, 210 + Math.sin(a) * d * 0.7, 26 + rand() * 12, p.tone, p.shape, p.deco, rand);
    }
    return out + `<path d="M40 340c60-20 120 10 180-4s110-24 150-8" stroke="#B98458" stroke-width="3" fill="none" stroke-dasharray="2 9" stroke-linecap="round"/>`;
  }

  function tablet(id, prod, view) {
    const tone = prod.chocolate_type.includes("White") ? "white" : prod.chocolate_type.includes("Milk") ? "milk" : "dark";
    const t = TONES[tone];
    let squares = "";
    for (let j = 0; j < 6; j++) for (let i = 0; i < 4; i++)
      squares += `<rect x="${118 + i * 42}" y="${62 + j * 46}" width="36" height="40" rx="4" fill="url(#${id}-${tone})" stroke="${t.sh}" stroke-width="2"/>`;
    const wrapY = view === 1 ? 62 : 200;
    const ink = ["#E3A99A", "#B98458"].includes(prod.lid) ? "#3D2617" : "#FFF7E8";
    return `<g transform="rotate(${view === 2 ? -14 : 8} 200 200)">
      <rect x="112" y="56" width="176" height="288" rx="8" fill="${t.sh}"/>${squares}
      ${view === 3 ? "" : `<rect x="104" y="${wrapY}" width="192" height="${352 - wrapY}" rx="6" fill="${prod.lid}"/>
      <rect x="104" y="${wrapY}" width="192" height="10" fill="#2B190F" opacity=".12"/>
      <text x="200" y="${wrapY + 70}" text-anchor="middle" font-family="'Big Shoulders Display',sans-serif" font-weight="800" font-size="30" fill="${ink}">${prod.title.split(" ")[0].toUpperCase()}</text>
      <text x="200" y="${wrapY + 102}" text-anchor="middle" font-family="'Caveat Brush',cursive" font-size="22" fill="${ink}">${prod.variants[0].net_weight}</text>`}
    </g>`;
  }

  function ballotin(id, prod, v, rand, open) {
    let pile = "";
    if (open) for (let i = 0; i < 16; i++) {
      const p = pickPraline(prod, rand);
      pile += praline(id, 130 + (i % 6) * 28 + rand() * 8, 150 - Math.floor(i / 6) * 22 + rand() * 6, 20, p.tone, p.shape, p.deco, rand);
    }
    return `<ellipse cx="200" cy="330" rx="140" ry="16" fill="#2B190F" opacity=".15"/>
      ${pile}
      <path d="M92 160h216l-22 168H114Z" fill="${prod.lid}" stroke="#B98458" stroke-width="3"/>
      <path d="M92 160h216l-8 22H100Z" fill="#E7CFAE"/>
      ${open ? "" : `<path d="M92 160l108-54 108 54Z" fill="#EBD3AE" stroke="#B98458" stroke-width="3"/>`}
      <rect x="92" y="238" width="216" height="22" fill="${prod.ribbon}"/>
      <text x="200" y="222" text-anchor="middle" font-family="'Big Shoulders Display',sans-serif" font-weight="800" font-size="24" letter-spacing="2" fill="#3D2617">${v.net_weight.toUpperCase()}</text>
      <text x="200" y="300" text-anchor="middle" font-family="'Caveat Brush',cursive" font-size="22" fill="#7B4B2A">ballotin</text>`;
  }

  function render(prod, view = 0, variantIndex = 0) {
    const id = `a${++uid}`;
    const v = prod.variants[variantIndex] || prod.variants[0];
    const rand = rng(prod.id + view + v.label);
    let body;
    if (prod.shape === "tablet") body = tablet(id, prod, view);
    else if (prod.shape === "ballotin" && view < 2) body = ballotin(id, prod, v, rand, view === 0);
    else if (view === 1) body = closedBox(id, prod);
    else if (view === 2) body = cutView(id, prod, rand);
    else if (view === 3) body = scattered(id, prod, rand);
    else body = openBox(id, prod, v, rand);
    return `<svg viewBox="0 0 400 400" role="img" aria-label="${prod.title} illustration" xmlns="http://www.w3.org/2000/svg">
      <defs>${gradients(id)}</defs><rect width="400" height="400" fill="${BG[prod.palette] || "#F5E6CC"}"/>${body}</svg>`;
  }

  /* A loose cluster of pralines for decorative hero use. */
  function cluster(seed = "hero", count = 7) {
    const id = `a${++uid}`;
    const rand = rng(seed);
    const fake = { palette: "mixed" };
    let out = "";
    const spots = [[150, 170, 70], [270, 140, 54], [235, 265, 62], [110, 290, 44], [330, 250, 40], [60, 180, 34], [190, 60, 30]];
    spots.slice(0, count).forEach(([x, y, r]) => {
      const p = pickPraline(fake, rand);
      out += praline(id, x, y, r, p.tone, p.shape === "heart" ? "circle" : p.shape, p.deco, rand);
    });
    return `<svg viewBox="0 0 400 360" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><defs>${gradients(id)}</defs>${out}</svg>`;
  }

  /* One praline as a small icon, for flavour maps and the ballotin builder. */
  function piece(tone = "milk", shape = "circle", deco = "none") {
    const id = `a${++uid}`;
    return `<svg viewBox="0 0 100 100" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><defs>${gradients(id)}</defs>${praline(id, 50, 52, 34, TONES[tone] ? tone : "milk", shape, deco, Math.random)}</svg>`;
  }

  return { render, cluster, piece };
})();
