/* markdown.js — compact Markdown renderer shared by admin preview + live site (hydrate/render).
   Supported: # ## ### headings, **bold**, *italic*, `code`, [links](url),
   - lists, 1. lists, > quotes, | tables |, --- dividers,
   ::: type Title / body / ::: callouts (warning|danger|tip|note), paragraphs. */
window.MD = (function () {
  function esc(s) { var d = document.createElement('div'); d.textContent = s == null ? '' : s; return d.innerHTML; }
  function inline(s) {
    s = esc(s);
    s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
    s = s.replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
    s = s.replace(/\*([^*\n]+)\*/g, '<i>$1</i>');
    s = s.replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g, '<a href="$2" rel="noopener">$1</a>');
    return s;
  }
  var CALLOUT = { warning: 'amber', danger: 'red', red: 'red', tip: 'green', success: 'green', note: 'amber' };
  function table(lines) {
    var rows = lines.filter(l => /^\s*\|/.test(l)).map(l => l.trim().replace(/^\||\|$/g, '').split('|').map(c => c.trim()));
    if (rows.length < 2) return '';
    var head = rows[0], body = rows.slice(2); // row[1] is the |---| separator
    return '<div class="figure"><table class="tbl"><thead><tr>' + head.map(c => '<th>' + inline(c) + '</th>').join('') +
      '</tr></thead><tbody>' + body.map(r => '<tr>' + r.map(c => '<td>' + inline(c) + '</td>').join('') + '</tr>').join('') +
      '</tbody></table></div>';
  }
  function render(src) {
    var lines = String(src || '').split('\n'), out = [], i = 0;
    function flushPara(start) {
      var buf = [];
      while (start < lines.length && lines[start].trim() !== '' && !/^(#{1,3}\s|[-*]\s|\d+\.\s|>|:::|\||---+\s*$)/.test(lines[start])) { buf.push(lines[start]); start++; }
      if (buf.length) out.push('<p>' + inline(buf.join(' ')) + '</p>');
      return start;
    }
    while (i < lines.length) {
      var L = lines[i];
      if (/^###\s/.test(L)) { out.push('<h3>' + inline(L.slice(4)) + '</h3>'); i++; }
      else if (/^##\s/.test(L)) { out.push('<h2>' + inline(L.slice(3)) + '</h2>'); i++; }
      else if (/^#\s/.test(L)) { out.push('<h2>' + inline(L.slice(2)) + '</h2>'); i++; }
      else if (/^---+\s*$/.test(L)) { out.push('<hr class="divider">'); i++; }
      else if (/^\s*[-*]\s+/.test(L)) {
        var items = [];
        while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) { items.push('<li>' + inline(lines[i].replace(/^\s*[-*]\s+/, '')) + '</li>'); i++; }
        out.push('<ul>' + items.join('') + '</ul>');
      }
      else if (/^\s*\d+\.\s+/.test(L)) {
        var oi = [];
        while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) { oi.push('<li>' + inline(lines[i].replace(/^\s*\d+\.\s+/, '')) + '</li>'); i++; }
        out.push('<ol>' + oi.join('') + '</ol>');
      }
      else if (/^>\s?/.test(L)) {
        var qs = [];
        while (i < lines.length && /^>\s?/.test(lines[i])) { qs.push(inline(lines[i].replace(/^>\s?/, ''))); i++; }
        out.push('<blockquote>' + qs.join('<br>') + '</blockquote>');
      }
      else if (/^\s*\|/.test(L)) {
        var tl = [];
        while (i < lines.length && /^\s*\|/.test(lines[i])) { tl.push(lines[i]); i++; }
        out.push(table(tl));
      }
      else if (/^:::\s*(\w*)\s*(.*)$/.test(L)) {
        var m = L.match(/^:::\s*(\w*)\s*(.*)$/);
        var bodyLines = [];
        i++;
        while (i < lines.length && !/^:::\s*$/.test(lines[i])) { bodyLines.push(lines[i]); i++; }
        i++; // closing :::
        var cls = CALLOUT[(m[1] || 'note').toLowerCase()] || 'amber';
        out.push('<div class="callout ' + cls + '"><b>' + inline(m[2] || 'Note') + '</b>' +
          bodyLines.map(function (b) { return '<p>' + inline(b) + '</p>'; }).join('') + '</div>');
      }
      else if (L.trim() === '') { i++; }
      else { i = flushPara(i); }
    }
    return out.join('\n');
  }
  return { render: render };
})();
