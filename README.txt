REINO DE CENIZA — VERSIÓN 5 MAPAS

Contenido:
- index.html: juego completo.
- assets/: modelos y texturas usados únicamente por los 4 mapas nuevos.

Mapas:
1. Reino de Ceniza — mapa original, sin reconstruir.
2. Montaña Helada — Orcos/Chamán/Yeti + Yeti Glacial + Yeti Alfa.
3. Valle de los Dragones — criaturas de basalto/voladoras + Dragón Antiguo + Dragón Corrupto.
4. Reino de los Muertos — Espectros/Guerreros Profanados + Señor de las Almas + Caudillo No-muerto.
5. Ruinas Corruptas — Orcos/Hongos/Gólems + Coloso de las Ruinas + Demonio del Velo.

Uso:
- Mantener index.html y la carpeta assets juntos, respetando la estructura.
- Para GitHub Pages/Netlify: subir todo el contenido de esta carpeta.
- Los 4 mapas nuevos se cargan la primera vez que se viaja a ellos para reducir la carga inicial.
- Abrir index.html directamente con file:// puede impedir que algunos navegadores carguen glTF; probar desde GitHub Pages, Netlify o un servidor local.

Optimización:
- Solo se incluyeron los modelos realmente usados.
- Las texturas de escenario se redujeron a un máximo de 1024 px para mejorar memoria/carga en celular.


VERSIÓN 2 — escenarios más llenos:
- Caminos marcados, lagos helados, bosques, cementerios con mausoleos, ruinas, hongos gigantes, cristales, huesos de dragón, nidos, obeliscos con runas, antorchas y fogatas, luna enorme en el Reino de los Muertos.
- Todo se dibuja con instancias y brillos aditivos (sin luces extra) para que corra bien en celular.
