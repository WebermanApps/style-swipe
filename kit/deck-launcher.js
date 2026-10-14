/* RETIRED (R66 reworded by Max Oct 14 2026 19:30 ICT): the 'Open a New Deck' category picker is gone.
   Kept for backwards compat: any page still loading deck-launcher.js + data-launcher now gets the Ready Deck Shelf (deck-shelf.js),
   which shows the launcher.json ready deck + unfinished decks as shelf cards. New pages: use deck-shelf.js/.css + shelf.json. */
(()=>{const base='https://webermanapps.github.io/style-swipe/kit/';
if(!document.querySelector('link[href*="deck-shelf.css"]')){const l=document.createElement('link');l.rel='stylesheet';l.href=base+'deck-shelf.css?v=1';document.head.append(l)}
if(!window.DeckShelf){const s=document.createElement('script');s.src=base+'deck-shelf.js?v=1';document.head.append(s)}})();
