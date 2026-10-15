/* v2 (Max 13:21): 72/56px logo, text beside icon, 2px divider via dash-theme.css. Renders .mw-cc-header[data-cc-name] from data attributes: data-cc-name, data-cc-desc, data-cc-logo (image URL). */
(function(){function r(){document.querySelectorAll('.mw-cc-header[data-cc-name]').forEach(function(h){if(h.dataset.ccDone)return;h.dataset.ccDone=1;
var t=document.createElement('div');t.className='mw-cc-text';var h1=document.createElement('h1');h1.className='mw-cc-title';h1.textContent=h.dataset.ccName+' Command Center';t.appendChild(h1);
if(h.dataset.ccDesc){var p=document.createElement('p');p.className='mw-cc-desc';p.textContent=h.dataset.ccDesc;t.appendChild(p);}
if(h.dataset.ccLogo&&!h.querySelector('.mw-cc-logo')){var l=document.createElement('div');l.className='mw-cc-logo';var i=document.createElement('img');i.src=h.dataset.ccLogo;i.alt='';l.appendChild(i);h.appendChild(l);}
h.appendChild(t);});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',r);else r();})();
