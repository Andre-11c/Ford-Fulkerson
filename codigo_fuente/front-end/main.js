document.getElementById('fileInput').addEventListener('change', handleFileSelect, false);

function handleFileSelect(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
        const text = e.target.result;
        const { nodes, links } = parseFileContent(text);
        createGraph(nodes, links);
    };
    reader.readAsText(file);
}

function parseFileContent(text) {
    const lines = text.trim().split('\n');
    const nodes = [];
    const links = [];

    lines.forEach((line, index) => {
        const parts = line.split(' ').map(Number);
        nodes.push({ id: index });
        for (let i = 1; i < parts.length; i += 2) {
            links.push({ source: index, target: parts[i], value: parts[i + 1] });
        }
    });

    return { nodes, links };
}

function createGraph(nodes, links) {
    const svg = d3.select("svg");
    svg.selectAll("*").remove(); // Clear existing graph

    const width = +svg.attr("width");
    const height = +svg.attr("height");

    const color = d3.scaleOrdinal(d3.schemeCategory10);

    const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id).distance(d => d.value * 10))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    const link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(links)
        .enter().append("line")
        .attr("class", "link")
        .attr("stroke-width", d => Math.sqrt(d.value));

    const node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(nodes)
        .enter().append("circle")
        .attr("class", "node")
        .attr("r", 5)
        .attr("fill", d => color(d.id))
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    node.append("title")
        .text(d => d.id);

    simulation
        .on("tick", () => {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);
        });

    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
}
