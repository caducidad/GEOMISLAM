// Convierte las páginas SVG de una carpeta en PNG de vista previa y un PDF A4 con todas ellas.
// Uso: node a_pdf.js <carpeta> <nombre.pdf> [página1 página2 …]
const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
const dir=path.resolve(process.argv[2]), pdf=process.argv[3];
const pags=process.argv.slice(4).length?process.argv.slice(4):fs.readdirSync(dir).filter(f=>f.endsWith('.svg')).map(f=>f.slice(0,-4)).sort();
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:794,height:1123}});
for(const n of pags){ await p.goto('file://'+path.join(dir,n+'.svg')); await p.screenshot({path:path.join(dir,n+'.png')}); }
const html='<!doctype html><meta charset="utf-8"><style>@page{size:A4;margin:0}body{margin:0}img{width:210mm;height:297mm;display:block;page-break-after:always}</style>'
  +pags.map(n=>`<img src="file://${path.join(dir,n+'.svg')}">`).join('');
const tmp=path.join(dir,'_todo.html'); fs.writeFileSync(tmp,html);
await p.goto('file://'+tmp); await p.waitForTimeout(500);
await p.pdf({path:path.join(dir,pdf),format:'A4',printBackground:true}); fs.unlinkSync(tmp);
await b.close();})();
