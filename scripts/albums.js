var nodes = null;
var edges = null;
var network = null;

function draw() {
  nodes = [
    {id: 1, shape: 'image', image: '../images/big_lift.jpg'},
    {id: 2, shape: 'image', image: '../images/ngt1.jpg'},
    {id: 3, shape: 'image', image: '../images/oadlt.jpg'},
    {id: 4, shape: 'image', image: '../images/deepnight.jpg'},
    {id: 5, shape: 'image', image: '../images/pearl.jpg'},
    {id: 6, shape: 'image', image: '../images/ngt2.jpg'}
    ];
  edges = [
    {from: 1, to: 2, title: 'Darren Johnston', labelHighlightBold: true},
    {from: 2, to: 6, title: 'Darren Johnston', labelHighlightBold: true},
    {from: 2, to: 6, title: 'Daniel Fabricant'},
    {from: 2, to: 6, title: 'Rob Reich'},
    {from: 1, to: 3, title: 'Darren Johnston'},
    {from: 2, to: 3, title: 'Darren Johnston'},
    {from: 6, to: 3, title: 'Darren Johnston'},
    {from: 4, to: 5, title: 'Rob Reich'},
    {from: 4, to: 6, title: 'Rob Reich'},
    {from: 4, to: 5, title: 'Dave Ricketts'},
    {from: 4, to: 5, title: 'Ari Munkres'},
    {from: 4, to: 5, title: 'Ralph Carney'},
    {from: 4, to: 5, title: 'Michael Groh'},
    {from: 4, to: 5, title: 'Pete Devine'},
    {from: 5, to: 6, title: 'Rob Reich'},
    {from: 2, to: 5, title: 'Rob Reich'},
    {from: 2, to: 4, title: 'Rob Reich'},
    ];
  var container = document.getElementById('mynetwork');
  var data = {
    nodes: nodes,
    edges: edges
  };
  var options = {
    nodes: {
      borderWidht:10,
      size:30,
      color: {
        border: '#000000',
        background: '#666666'
      },
      font:{color:'#aaaaaa'}
    },
    edges: {
      color: 'lightgray'
    }
  };
  network = new vis.Network(container, data, options);
}
