/**
 * Created by Mark Verschuuren on 31-5-2017.
 */

var phrases = [];

$('.phrase').each(function codeAddress(){
    var phrase = '';
    $(this).find('li').each(function(){
        var current = $(this);
        if(current.children().size() > 0) {return true;}
        phrase += $(this).text();
    });
    phrases.push(phrase);
});
// note the comma to separate multiple phrases

var res = phrases[0].split("'");
var res = res.join("");
var res = res.split(")").join();
var res = res.split("(").join();
var res = res.split(",").join(" ");
var res = res.split(" ");

var Results = []
for (i = 1; i < res.length; i += 2) {
    Results.push(res[i])
};

console.log(Results)

var cy = cytoscape({

  container: document.getElementById('cy'), // container to render in


  style: [ // the stylesheet for the graph
    {
      selector: 'node',
      style: {
        'background-color': '#666',
        'label': 'data(id)'
      }
    },

    {
      selector: 'edge',
      style: {
        'width': 3,
        'line-color': '#ccc',
        'target-arrow-color': '#ccc',
        'target-arrow-shape': 'triangle',
          'label': 'data(id)'
      }
    }
  ],
  layout: {
    name: 'grid',
    rows: 1
  }

});

for(var i = 0; i < res.length; i += 2){
    console.log(Results[i])
    if( typeof Results[i] != "undefined")
        var eles = cy.add([
            {group : "nodes",
            data: {id: Results[i]},
            position : {x:200, y: 200}}
        ]
    )
    if(Results[0] != Results[i])
    var eles = cy.add([
        {group: "edges", data:{id: Results[i+1], source: Results[0], target: Results[i]} }
    ])

}



