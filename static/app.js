var jsonData = {
    "nodes": [],
    "edges": []
};

// Function to fetch JSON data
function fetchJsonData(initialMatrix, finalMatrix) {
    // Send a GET request with initial and final matrix values
    var xhr = new XMLHttpRequest();
    var url = '/get_json_data?initialMatrix=' + initialMatrix + '&finalMatrix=' + finalMatrix;
    xhr.open('GET', url, true);

    // Add an error handler
    xhr.onerror = function () {
        alert('An error occurred while fetching JSON data. Status code: ' + xhr.status);
    };

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                jsonData = JSON.parse(xhr.responseText);
                var vis_json = visual(); // Call the visualization function after data is fetched
            } else {
                // Handle other status codes if needed
                alert('Error: ' + xhr.status + '. Maximum recursion depth exceeded.');
            }
        }
    };
    xhr.send();

}

function checkUniqueDigits() {
    const initialDigits = document.getElementById('initial-digits').value;
    const finalDigits = document.getElementById('final-digits').value;

    // Regular expression to match digits from 0 to 8 only
    const regex = /^[0-8]{9}$/;

    if (!regex.test(initialDigits) || !regex.test(finalDigits)) {
        alert('Please enter exactly 9 digits from 0 to 8 in both the initial and final input.');
        return;
    }

    const initialDigitsSet = new Set(initialDigits);
    if (initialDigitsSet.size !== 9) {
        alert('Please ensure that all initial digits are unique.');
        return;
    }

    const finalDigitsSet = new Set(finalDigits);
    if (finalDigitsSet.size !== 9) {
        alert('Please ensure that all final digits are unique.');
        return;
    }

    // Call the fetchJsonData function with the entered matrix values
    fetchJsonData(initialDigits, finalDigits);
}

document.getElementById("fetchData").addEventListener('click', function () {
    checkUniqueDigits();
});

function visual() {
    // create an array with nodes
    var nodes = new vis.DataSet(jsonData.nodes);

    // create an array with edges
    var edges = new vis.DataSet(jsonData.edges);

    // create a network
    var container = document.getElementById('mynetwork');

    // provide the data in the vis format
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {
        width: "100%",
        height: "100%",
        layout: {
            hierarchical: {
                enabled: true,
                levelSeparation: 150,
                nodeSpacing: 100,
                direction: 'UD',
                sortMethod: 'directed',
                shakeTowards: 'roots'
            }
        },
        interaction: {
            hover: true,
        }
    };

    var interaction = { dragNodes: false, hover: true };
    var physics = { enabled: false }

    // initialize your network!
    var network = new vis.Network(container, data, options, interaction, physics);


    // Set up event handlers to display node information when hovering
    network.on('hoverNode', function (properties) {
        var nodeId = properties.node;
        var node = nodes.get(nodeId);

        if (node) {
            // Update the node information section
            // document.getElementById('node-id').textContent = nodeId;
            document.getElementById('node-label').textContent = node.label || '-';
            document.getElementById('node-cost').textContent = node.cost || '0';
            document.getElementById('node-empty-pos').textContent = node.empty_tile_pos || '-';
            document.getElementById('node-level').textContent = node.level || '0';
            // document.getElementById('node-description').textContent = node.title || '-';
        }
        // Handle the case when no node is hovered
        else {
            // document.getElementById('node-id').textContent = '-';
            document.getElementById('node-label').textContent = '-';
            document.getElementById('node-cost').textContent = '-';
            document.getElementById('node-empty-pos').textContent = '-';
            document.getElementById('node-level').textContent = '-';
            // document.getElementById('node-description').textContent = '-';
        }
    });

    return ({ "nodes": nodes, "edges": edges, "network": network })
}


new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        darkTheme: false,
        sideMenuActive: false
    },
    methods: {
        toggleTheme() {
            this.darkTheme = !this.darkTheme;
            document.body.classList.toggle('dark', this.darkTheme);
        },
        toggleSideMenu() {
            this.sideMenuActive = !this.sideMenuActive;
        }
    }
});
