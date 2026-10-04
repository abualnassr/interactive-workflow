// Layout audit for an interactive workflow page (see SKILL.md section 7).
// Evaluate this whole file in the rendered page: it runs itself and returns a list of findings, empty on a pass.
// It works at any window size: every box is converted to the canvas's own unscaled coordinates first.
// scripts/wf_check.py runs it in headless Chromium; any browser tool that can evaluate JavaScript can run it too.
(() => {
  const C = document.getElementById('c'), cr = C.getBoundingClientRect();
  const k = cr.width / C.offsetWidth;                       // page scale set by fit()
  const W = C.clientWidth, H = C.clientHeight;              // canvas size in its own px (inside the border)
  const box = el => { const r = el.getBoundingClientRect(); const x = v => (v - cr.left) / k - C.clientLeft, y = v => (v - cr.top) / k - C.clientTop;
    return {l:x(r.left), t:y(r.top), r:x(r.right), b:y(r.bottom)}; };
  const bad = [];
  // schema: ids unique, arrows reference real cards, every card connected, stage key known
  const ids = N.map(n => n[0]); ids.forEach((id,i) => { if (ids.indexOf(id) !== i) bad.push('duplicate id '+id); if (!STAGE[id[0]]) bad.push('unknown stage key for '+id); });
  E.forEach(e => { if (!byId[e.f]) bad.push('arrow from unknown '+e.f); if (!byId[e.t]) bad.push('arrow to unknown '+e.t); if (e.pts.length < 2) bad.push('arrow '+e.f+'>'+e.t+' needs 2+ points'); });
  ids.forEach(id => { if (!E.some(e => e.f===id || e.t===id)) bad.push('unconnected '+id); });
  // cards: inside the canvas, not overlapping
  const nodes = [...document.querySelectorAll('.node')].map(e => ({id:e.id.slice(2), ...box(e)}));
  nodes.forEach(n => { if (n.l < -0.5 || n.t < -0.5 || n.r > W+0.5 || n.b > H+0.5) bad.push('outside canvas '+n.id); });
  nodes.forEach((a,i) => nodes.slice(i+1).forEach(b => { if (a.l < b.r && b.l < a.r && a.t < b.b && b.t < a.b) bad.push('card-card '+a.id+' / '+b.id); }));
  // arrows: outside the canvas, or running on top of each other (unless they share a bus id)
  edges.forEach(e => { const r = box(e.path); if (r.l < -0.5 || r.t < -0.5 || r.r > W+0.5 || r.b > H+0.5) bad.push('arrow outside canvas '+e.f+'>'+e.t); });
  const segs = E.map(e => e.pts.slice(1).map((q,i) => [e.pts[i], q]));
  const span = (a,b,c2,d) => Math.min(Math.max(a,b),Math.max(c2,d)) - Math.max(Math.min(a,b),Math.min(c2,d));
  E.forEach((a,i) => E.forEach((b,j) => { if (j <= i || (a.bus && a.bus === b.bus)) return;
    segs[i].forEach(([p,q]) => segs[j].forEach(([r,t]) => {
      if (p[1]===q[1] && r[1]===t[1] && Math.abs(p[1]-r[1]) < 3 && span(p[0],q[0],r[0],t[0]) > 6) bad.push('arrow-overlap '+a.f+'>'+a.t+' / '+b.f+'>'+b.t);
      if (p[0]===q[0] && r[0]===t[0] && Math.abs(p[0]-r[0]) < 3 && span(p[1],q[1],r[1],t[1]) > 6) bad.push('arrow-overlap '+a.f+'>'+a.t+' / '+b.f+'>'+b.t); })); }));
  // vertical arrow runs on or beside a dashed stage divider
  STAGES.forEach(st => { if (!st.x) return; E.forEach((e,i) => segs[i].forEach(([p,q]) => { if (p[0]===q[0] && Math.abs(p[0]-st.x) < 10) bad.push('arrow-on-divider '+e.f+'>'+e.t+' / '+st.label); })); });
  // arrow ends: the first point exactly on the source card's edge and the last exactly on the target's edge, each segment meeting
  // its edge at right angles from outside (not running along it, not starting or ending inside the card), 12 px or more from a corner
  const side = ([x,y], n) => { const T = 2, inX = x >= n.l-T && x <= n.r+T, inY = y >= n.t-T && y <= n.b+T;
    const s = [];
    if (Math.abs(x-n.l) <= T && inY) s.push('left'); if (Math.abs(x-n.r) <= T && inY) s.push('right');
    if (Math.abs(y-n.t) <= T && inX) s.push('top'); if (Math.abs(y-n.b) <= T && inX) s.push('bottom');
    return s.length === 1 ? s[0] : (s.length ? 'corner' : null); };
  const inside = (x,y,n,pad=0) => x>n.l-pad && x<n.r+pad && y>n.t-pad && y<n.b+pad;
  const fromOutside = (sd, [x,y], [qx,qy]) => ({left: qx < x && qy === y, right: qx > x && qy === y, top: qy < y && qx === x, bottom: qy > y && qx === x})[sd];
  const nearCorner = (sd, [x,y], n) => (sd === 'left' || sd === 'right') ? (y - n.t < 12 || n.b - y < 12) : (x - n.l < 12 || n.r - x < 12);
  E.forEach(e => { const f = nodes.find(n => n.id === e.f), t = nodes.find(n => n.id === e.t); if (!f || !t || e.pts.length < 2) return;
    const P = e.pts, a = P[0], z = P[P.length-1], id = e.f+'>'+e.t;
    [['start', a, P[1], f], ['end', z, P[P.length-2], t]].forEach(([k, pt, nb, n]) => { const sd = side(pt, n);
      if (!sd) bad.push(k+' off the edge of '+n.id+' '+id);
      else if (sd === 'corner' || nearCorner(sd, pt, n)) bad.push(k+' at a corner of '+n.id+' '+id);
      else if (k === 'end' && Math.hypot(pt[0]-nb[0], pt[1]-nb[1]) < 16) bad.push('end segment of '+id+' is shorter than 16 px, too short for the arrowhead');
      else if (!fromOutside(sd, pt, nb)) bad.push(k+(inside(nb[0],nb[1],n,-1) ? ' comes from inside ' : (nb[0]===pt[0] || nb[1]===pt[1]) ? ' runs along the edge of ' : ' meets the edge of ')+n.id+(inside(nb[0],nb[1],n,-1) || nb[0]===pt[0] || nb[1]===pt[1] ? '' : ' at an angle (the next waypoint is not lined up with it)')+' '+id); }); });
  // arrows cross no card, including their own source and target (path points are already in canvas px)
  edges.forEach(e => { const L = e.path.getTotalLength(); const own = new Set([e.f, e.t]);
    const crossed = new Set(); for (let s=4; s<L-4; s+=3){ const p = e.path.getPointAtLength(s); nodes.forEach(n => { if (inside(p.x,p.y,n,own.has(n.id) ? -2 : -1)) crossed.add(n.id); }); }
    if (crossed.size) bad.push('cross '+e.f+'>'+e.t+':'+[...crossed]); });
  // arrow labels: inside the canvas, off cards, off each other, and no line runs through them
  const labs = [...document.querySelectorAll('.lbl')].map(g => { const r = box(g); return {t:g.textContent, l:r.l, top:r.t, r:r.r, b:r.b}; });
  const ov = (a,b) => a.l < b.r && b.l < a.r && a.top < b.b && b.top < a.b;
  labs.forEach((a,i) => { if (a.l < -0.5 || a.top < -0.5 || a.r > W+0.5 || a.b > H+0.5) bad.push('label outside canvas '+a.t);
    nodes.forEach(n => { if (ov(a,{l:n.l-4,r:n.r+4,top:n.t-4,b:n.b+4})) bad.push('label-on-card '+a.t+' / '+n.id+' (labels keep 4 px clear of cards)'); });
    labs.slice(i+1).forEach(b => { if (ov(a,b)) bad.push('label-label '+a.t+' / '+b.t); }); });
  edges.forEach(e => { const L = e.path.getTotalLength(); for (let s=0; s<L; s+=4){ const p = e.path.getPointAtLength(s); labs.forEach(a => { if (a.t !== e.label && !(e.bus && edges.some(o=>o.bus===e.bus && o.label===a.t)) && p.x>a.l && p.x<a.r && p.y>a.top && p.y<a.b) bad.push('line-through-label '+e.f+'>'+e.t+' / '+a.t); }); } });
  // stage, lane and group titles: no line through them, no label or card on them
  [...document.querySelectorAll('.lane-label,.stage-label,.group-label')].forEach(el => { const r = box(el); const tb = {l:r.l, top:r.t, r:r.r, b:r.b};
    edges.forEach(e => { const L = e.path.getTotalLength(); for (let s=0; s<L; s+=4){ const p = e.path.getPointAtLength(s); if (p.x>tb.l && p.x<tb.r && p.y>tb.top && p.y<tb.b) { bad.push('line-through-text '+e.f+'>'+e.t+' / '+el.textContent); break; } } });
    labs.forEach(a => { if (ov(a,tb)) bad.push('label-on-text '+a.t+' / '+el.textContent); });
    nodes.forEach(n => { if (ov(tb,{l:n.l,r:n.r,top:n.t,b:n.b})) bad.push('text-on-card '+el.textContent+' / '+n.id); }); });
  // card text clipped at the bottom or the side
  [...document.querySelectorAll('.node')].forEach(e => { if (e.scrollHeight > e.clientHeight+1 || e.scrollWidth > e.clientWidth+1) bad.push('clipped '+e.id.slice(2)); });
  return [...new Set(bad)];
})()
