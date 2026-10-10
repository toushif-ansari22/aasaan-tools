const $=s=>document.querySelector(s);
const inr=n=>'₹'+Math.round(n).toLocaleString('en-IN');
const num=id=>parseFloat($('#'+id).value)||0;
const field=(id,label,val,extra='')=>`<div><label for="${id}">${label}</label><input id="${id}" type="number" min="0" step="any" value="${val}" ${extra}></div>`;
const out=(items)=>'<div class="out">'+items.map(([l,v,h])=>`<div class="${h?'hi':''}"><span>${l}</span><strong>${v}</strong></div>`).join('')+'</div>';
const calc=(fn)=>setTimeout(()=>{document.querySelectorAll('#tool input,#tool select').forEach(e=>e.addEventListener('input',fn));fn()},0);

const tools=[
{id:'emi',name:'EMI Calculator',title:'EMI Calculator',sub:'Home, car or personal loan ki monthly EMI nikalo.',
 html:()=>`<div class="grid">${field('p','Loan amount (₹)',1000000)}${field('r','Interest rate (% per year)',9)}${field('y','Tenure (years)',5)}</div><div id="o"></div>`,
 init:()=>calc(()=>{const P=num('p'),r=num('r')/1200,n=num('y')*12;let e=r?P*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1):(n?P/n:0);if(!isFinite(e))e=0;$('#o').innerHTML=out([['Monthly EMI',inr(e),1],['Total interest',inr(e*n-P)],['Total payment',inr(e*n)]])}),
 about:'EMI is calculated with the standard reducing-balance formula: EMI = P × r × (1+r)ⁿ / ((1+r)ⁿ − 1), where r is the monthly rate and n the number of months. Banks may add processing fees that are not included here.'},
{id:'gst',name:'GST Calculator',title:'GST Calculator',sub:'Price me GST add karo ya nikaalo.',
 html:()=>`<div class="grid">${field('a','Amount (₹)',1000)}<div><label for="g">GST rate</label><select id="g"><option>5</option><option>12</option><option selected>18</option><option>28</option></select></div><div><label for="m">Mode</label><select id="m"><option value="add">Add GST (price excludes GST)</option><option value="rem">Remove GST (price includes GST)</option></select></div></div><div id="o"></div>`,
 init:()=>calc(()=>{const a=num('a'),g=num('g')/100;const rem=$('#m').value==='rem';const base=rem?a/(1+g):a;const t=base*g;$('#o').innerHTML=out([['Base price',inr(base)],['GST amount',inr(t)],['CGST / SGST (each)',inr(t/2)],['Final price',inr(base+t),1]])}),
 about:'Use "Add GST" when your price is before tax and "Remove GST" when the MRP already includes it. For intra-state sales GST splits equally into CGST and SGST.'},
{id:'sip',name:'SIP Calculator',title:'SIP Calculator',sub:'Monthly SIP se kitna paisa banega, dekho.',
 html:()=>`<div class="grid">${field('p','Monthly investment (₹)',5000)}${field('r','Expected return (% per year)',12)}${field('y','Time (years)',10)}</div><div id="o"></div>`,
 init:()=>calc(()=>{const P=num('p'),i=num('r')/1200,n=num('y')*12;const fv=i?P*((Math.pow(1+i,n)-1)/i)*(1+i):P*n;const inv=P*n;$('#o').innerHTML=out([['Amount invested',inr(inv)],['Estimated gain',inr(fv-inv)],['Total value',inr(fv),1]])}),
 about:'Future value = P × [((1+i)ⁿ − 1) / i] × (1+i). Mutual fund returns are not guaranteed; this is an estimate for planning only, not financial advice.'},
{id:'age',name:'Age Calculator',title:'Age Calculator',sub:'Date of birth se exact age nikalo.',
 html:()=>`<div class="grid"><div><label for="d">Date of birth</label><input id="d" type="date" value="2008-01-01"></div></div><div id="o"></div>`,
 init:()=>calc(()=>{const v=$('#d').value;if(!v){$('#o').innerHTML='';return}const b=new Date(v),t=new Date();let y=t.getFullYear()-b.getFullYear(),m=t.getMonth()-b.getMonth(),d=t.getDate()-b.getDate();if(d<0){m--;d+=new Date(t.getFullYear(),t.getMonth(),0).getDate()}if(m<0){y--;m+=12}const days=Math.floor((t-b)/864e5);$('#o').innerHTML=y<0?'<p class="sub">Date of birth future me hai.</p>':out([['Your age',`${y}y ${m}m ${d}d`,1],['Total days lived',days.toLocaleString('en-IN')],['Total weeks',Math.floor(days/7).toLocaleString('en-IN')]])}),
 about:'Age is counted in completed years, months and days up to today.'},
{id:'percent',name:'Percentage Calculator',title:'Percentage Calculator',sub:'Marks, discount ya growth ka percentage.',
 html:()=>`<div class="grid">${field('a','X',20)}${field('b','Y',500)}</div><div id="o"></div>`,
 init:()=>calc(()=>{const a=num('a'),b=num('b');$('#o').innerHTML=out([[`${a}% of ${b}`,+(a*b/100).toFixed(4),1],[`${a} is what % of ${b}`,(b?+(a/b*100).toFixed(4):0)+'%'],[`${b} increased by ${a}%`,+(b*(1+a/100)).toFixed(4)],[`${b} decreased by ${a}%`,+(b*(1-a/100)).toFixed(4)]])}),
 about:'Change X and Y to get four common percentage answers at once: percent of a number, what percent one number is of another, and increase/decrease.'},
{id:'words',name:'Word Counter',title:'Word Counter',sub:'Words, characters, sentences aur reading time.',
 html:()=>`<label for="t">Paste or type your text</label><textarea id="t" placeholder="Yaha text paste karo..."></textarea><div id="o"></div>`,
 init:()=>calc(()=>{const t=$('#t').value,w=(t.trim().match(/\S+/g)||[]).length;$('#o').innerHTML=out([['Words',w,1],['Characters',t.length],['Without spaces',t.replace(/\s/g,'').length],['Sentences',(t.match(/[.!?।]+/g)||[]).length],['Reading time',Math.max(w?1:0,Math.round(w/200))+' min']])}),
 about:'Reading time assumes an average speed of 200 words per minute.'},
{id:'image',name:'Image Resizer',title:'Image Resizer',sub:'Photo ka size aur quality badlo, browser me hi.',
 html:()=>`<div class="grid"><div><label for="f">Choose image</label><input id="f" type="file" accept="image/*"></div>${field('w','Width (px)',800)}${field('h','Height (px)',600)}<div><label for="fm">Format</label><select id="fm"><option value="image/jpeg">JPG</option><option value="image/png">PNG</option><option value="image/webp">WebP</option></select></div><div><label for="q">Quality (JPG/WebP)</label><input id="q" type="number" min="10" max="100" value="85"></div></div><div class="row" style="margin-top:12px"><input type="checkbox" id="k" checked><label for="k">Keep aspect ratio</label></div><button class="btn" id="go">Resize image</button><div id="o"></div>`,
 init:()=>setTimeout(()=>{let img=null;const W=$('#w'),H=$('#h');
  $('#f').onchange=e=>{const f=e.target.files[0];if(!f)return;const i=new Image();i.onload=()=>{img=i;W.value=i.width;H.value=i.height;$('#o').innerHTML=out([['Original',`${i.width}×${i.height}`]])};i.src=URL.createObjectURL(f)};
  W.oninput=()=>{if(img&&$('#k').checked)H.value=Math.round(W.value*img.height/img.width)};
  H.oninput=()=>{if(img&&$('#k').checked)W.value=Math.round(H.value*img.width/img.height)};
  $('#go').onclick=()=>{if(!img){$('#o').innerHTML='<p class="sub">Pehle image choose karo.</p>';return}const c=document.createElement('canvas');c.width=+W.value;c.height=+H.value;c.getContext('2d').drawImage(img,0,0,c.width,c.height);const ft=$('#fm').value;c.toBlob(b=>{const u=URL.createObjectURL(b),ext=ft.split('/')[1].replace('jpeg','jpg');$('#o').innerHTML=out([['New size',`${c.width}×${c.height}`],['File size',(b.size/1024).toFixed(1)+' KB',1]])+`<a class="btn alt" style="display:inline-block;text-decoration:none" href="${u}" download="resized.${ext}">Download image</a>`},ft,num('q')/100)}},0),
 about:'Images are resized inside your browser using canvas. Nothing is uploaded to any server, so your photos stay private.'},
{id:'password',name:'Password Generator',title:'Password Generator',sub:'Strong random password, ek click me.',
 html:()=>`<div class="grid">${field('n','Length',16,'max="64"')}</div><div class="row" style="margin-top:12px"><input type="checkbox" id="u" checked><label for="u">A-Z</label><input type="checkbox" id="l" checked><label for="l">a-z</label><input type="checkbox" id="d" checked><label for="d">0-9</label><input type="checkbox" id="s" checked><label for="s">Symbols</label></div><button class="btn" id="go">Generate</button> <button class="btn alt" id="cp">Copy</button><div class="pw" id="pw" aria-live="polite">—</div>`,
 init:()=>setTimeout(()=>{const set={u:'ABCDEFGHIJKLMNOPQRSTUVWXYZ',l:'abcdefghijklmnopqrstuvwxyz',d:'0123456789',s:'!@#$%^&*()-_=+[]{}?'};
  const gen=()=>{const pool=Object.keys(set).filter(k=>$('#'+k).checked).map(k=>set[k]).join('');if(!pool){$('#pw').textContent='Kam se kam ek option select karo';return}const n=Math.min(64,Math.max(4,num('n')));const a=new Uint32Array(n);crypto.getRandomValues(a);$('#pw').textContent=[...a].map(x=>pool[x%pool.length]).join('')};
  $('#go').onclick=gen;$('#cp').onclick=()=>{navigator.clipboard&&navigator.clipboard.writeText($('#pw').textContent);$('#cp').textContent='Copied';setTimeout(()=>$('#cp').textContent='Copy',1200)};gen()},0),
 about:'Passwords are generated with your browser\'s cryptographic random number generator and are never sent anywhere.'}
];

