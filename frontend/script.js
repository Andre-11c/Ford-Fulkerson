
//datos para el grafo (archivo .txt)
const graphData = {
    nodes: [
        { id: 'A' },
        { id: 'B' },
        { id: 'C' }
    ],
    links: [
        { source: 'A', target: 'B' },
        { source: 'B', target: 'C' },
        { source: 'C', target: 'A' }
    ]
};

//config para visualizacion 
const width = 800;
const height = 600;
// Crear el contenedor SVG
const svg = createSVGContainer('#graph-container', width, height)

// Definir la simulación de fuerzas para el layout del grafo
const simulation = d3.forceSimulation()
    .force('link', d3.forceLink().id(d => d.id))
    .force('charge', d3.forceManyBody().strength(-200))
    .force('center', d3.forceCenter(width / 2, height / 2));

// Agregar enlaces (aristas) al grafo
const links = svg.selectAll('line')
    .data(graphData.links)
    .enter().append('line')
    .attr('stroke', '#000')
    .attr('stroke-width', 2);

