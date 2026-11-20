// Vuelve a exportar láminas desde su código de diseño, con el Taller de Lacería actual.
// Útil si cambia la aplicación (por ejemplo, la exportación por capas) y hay que regenerar los SVG.
//
// Uso: node herramientas/reexportar.js laminas/hilo/04-lazo-de-8 [otra carpeta …]
// Cada carpeta debe tener un diseno.txt con el código LAC1…; se reescriben lamina.svg, ficha.txt y vista.png.
// Exporta en A4 vertical con margen de 10 mm. Necesita Node y Playwright.
const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
const APP=path.resolve(__dirname,'..','taller','index.html');
const dirs=process.argv.slice(2).map(d=>path.resolve(d));
if(!dirs.length){ console.error('Indica al menos una carpeta de lámina.'); process.exit(1); }
(async()=>{
  const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1000,height:800}});
  await p.goto('file://'+APP); await p.waitForTimeout(1000);
  const vista=await b.newPage({viewport:{width:794,height:1123}});
  for(const d of dirs){
    const code=fs.readFileSync(path.join(d,'diseno.txt'),'utf8').trim();
    const r=await p.evaluate((code)=>{
      applyDesign(decodeDesign(code));
      Object.assign(state,{expMargin:true,expSize:"A4",expOrient:"p"});
      return {svg:exportSVG(), ficha:provenance().full()};
    },code);
    fs.writeFileSync(path.join(d,'lamina.svg'),r.svg);
    fs.writeFileSync(path.join(d,'ficha.txt'),r.ficha+'\n');
    await vista.goto('file://'+path.join(d,'lamina.svg')); await vista.screenshot({path:path.join(d,'vista.png')});
    console.log('reexportada',path.basename(d));
  }
  await b.close();
})();
