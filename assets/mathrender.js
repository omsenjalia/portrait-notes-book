const katex=require('katex'),fs=require('fs');
const j=JSON.parse(fs.readFileSync(process.argv[2],'utf8')),o={};
for(const [k,[t,d]] of Object.entries(j)) o[k]=katex.renderToString(t,{displayMode:d,output:'html',throwOnError:true});
fs.writeFileSync(process.argv[3],JSON.stringify(o));
