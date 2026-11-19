// sewcraftly-uploader v2
// POST /            {code, a4, letter, overwrite}  -> copies the A4 + US Letter zips into #SCxxxx/ (R2 sewcraftly-files)
// PUT  /tmp/<name>  (body = file)                  -> stores a temporary file at _tmp/<name>
// DELETE /tmp/<name>                               -> removes it
const CORS = {'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'content-type,x-key','Access-Control-Allow-Methods':'POST,PUT,DELETE,OPTIONS'};
const json = (o, s = 200) => new Response(JSON.stringify(o), {status: s, headers: {...CORS, 'content-type': 'application/json'}});

function direct(u) {
  const m = u.match(/drive\.google\.com\/(?:file\/d\/|open\?id=|uc\?(?:.*&)?id=)([\w-]+)/);
  if (m) return 'https://drive.usercontent.google.com/download?id=' + m[1] + '&export=download&confirm=t';
  if (/dropbox\.com/.test(u)) return /dl=0/.test(u) ? u.replace('dl=0', 'dl=1') : (/dl=1/.test(u) ? u : u + (u.includes('?') ? '&' : '?') + 'dl=1');
  return u;
}

export default {
  async fetch(req, env) {
    if (req.method === 'OPTIONS') return new Response(null, {headers: CORS});
    if (req.method === 'GET') return json({ok: true});
    if (req.headers.get('x-key') !== env.UPLOAD_KEY) return json({error: 'forbidden'}, 403);

    const path = new URL(req.url).pathname;
    const tmp = path.match(/^\/tmp\/([\w.-]{1,120})$/);
    if (tmp) {
      const key = '_tmp/' + tmp[1];
      if (req.method === 'PUT') {
        await env.BUCKET.put(key, req.body, {httpMetadata: {contentType: req.headers.get('content-type') || 'application/octet-stream'}});
        const obj = await env.BUCKET.head(key);
        return json({size: obj.size, url: 'https://files.sewcraftlypatterns.com/' + key});
      }
      if (req.method === 'DELETE') { await env.BUCKET.delete(key); return json({deleted: key}); }
      return json({error: 'use PUT or DELETE'}, 405);
    }

    if (req.method !== 'POST') return json({error: 'use POST'}, 405);
    const {code, a4, letter, overwrite} = await req.json();
    if (!/^SC\d{4,5}$/.test(code || '')) return json({error: 'bad code, use SC1042'}, 400);
    const out = {};
    for (const [name, src] of [['A4 SIZES.zip', a4], ['US LETTER SIZES.zip', letter]]) {
      if (!src) continue;
      const key = '#' + code + '/' + name;
      if (!overwrite && await env.BUCKET.head(key)) { out[name] = {error: 'already exists'}; continue; }
      const r = await fetch(direct(src), {redirect: 'follow'});
      const type = r.headers.get('content-type') || '';
      if (!r.ok) { out[name] = {error: 'fetch ' + r.status}; continue; }
      if (type.includes('text/html')) { out[name] = {error: 'source gave an HTML page, not a file (link not public or not direct)'}; continue; }
      const len = Number(r.headers.get('content-length') || 0);
      let body;
      if (len) { const f = new FixedLengthStream(len); r.body.pipeTo(f.writable); body = f.readable; }
      else body = await r.arrayBuffer();
      await env.BUCKET.put(key, body, {httpMetadata: {contentType: 'application/zip'}});
      const obj = await env.BUCKET.head(key);
      out[name] = {size: obj.size, url: 'https://files.sewcraftlypatterns.com/' + encodeURIComponent('#' + code) + '/' + encodeURIComponent(name)};
    }
    return json(out);
  }
};
