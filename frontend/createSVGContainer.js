// Crear el contenedor SVG
export function createSVGContainer(selector, wigth, height){
    return d3.select(selector)
    .append('svg')
    .attr('width', width)
    .attr('height', height);
}