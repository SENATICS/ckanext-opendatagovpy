/*
 * @author	Rodrigo Parra
 * @copyright	2014 Governance and Democracy Program USAID-CEAMSO
 * @license 	http://www.gnu.org/licenses/gpl-2.0.html
 *
 * USAID-CEAMSO
 * Copyright (C) 2014 Governance and Democracy Program
 * http://ceamso.org.py/es/proyectos/20-programa-de-democracia-y-gobernabilidad
 *
----------------------------------------------------------------------------
 * This file is part of the Governance and Democracy Program USAID-CEAMSO,
 * is distributed as free software in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. You can redistribute it and/or modify it under the
 * terms of the GNU Lesser General Public License version 2 as published by the
 * Free Software Foundation, accessible from <http://www.gnu.org/licenses/> or write
 * to Free Software Foundation (FSF) Inc., 51 Franklin St, Fifth Floor, Boston,
 * MA 02111-1301, USA.
 ---------------------------------------------------------------------------
 * Este archivo es parte del Programa de Democracia y Gobernabilidad USAID-CEAMSO,
 * es distribuido como software libre con la esperanza que sea de utilidad,
 * pero sin NINGUNA GARANTÍA; sin garantía alguna implícita de ADECUACION a cualquier
 * MERCADO o APLICACION EN PARTICULAR. Usted puede redistribuirlo y/o modificarlo
 * bajo los términos de la GNU Lesser General Public Licence versión 2 de la Free
 * Software Foundation, accesible en <http://www.gnu.org/licenses/> o escriba a la
 * Free Software Foundation (FSF) Inc., 51 Franklin St, Fifth Floor, Boston,
 * MA 02111-1301, USA.
 */

var cwidth = 470;
var cheight = 220;

var words_array = new Array();
var count_array = new Array();

var fill = d3.scale.category20();

function draw(words) {
    d3.select("#tag-cloud").append("svg")
    .attr("width", cwidth)
    .attr("height", cheight)
    .append("g")
    .attr("transform", "translate(215,110)")
    .selectAll("text")
    .data(words)
    .enter().append("text")
    //.style("class", "click")
    .style("font-size", function(d) { return d.size + "px"; })
    .style("font-family", "Impact")
    .style("fill", function(d, i) { return fill(i); })
    .attr("text-anchor", "middle")
    .on("click", function(d) {
         window.location.href="/"+"dataset?tags="+d.text;
         //alert(d.text);
     })
    .attr("transform", function(d) {
    	return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
    })
    .text(function(d) { return d.text; });
}

function createCloud(data) {

	for(var i = 0 ; i<data.length ; i++){
		words_array[i] = data[i].text;
		count_array[i] = data[i].size;
		//if(i>80) break;
	}

	var minCount = Math.min.apply(null, count_array);
	var maxCount = Math.max.apply(null, count_array);
	var minSize = 20;
	var maxSize = 100;

	d3.layout.cloud()
	.size([cwidth*0.9, cheight*0.9])
	.words(words_array
		.map(
			function(d) {
				var count = count_array[words_array.indexOf(d)];
				var factor = (maxSize-minSize)/(maxCount-minCount);
                var size = minSize + ((maxCount-(maxCount-(count-minCount)))*factor);
				return {text: d, size: size};
      		}
		)
	)
	.rotate(0)
    .font("Impact")
    .fontSize(function(d) { return d.size; })
    .on("end", draw)
	.start();
}

$(document).ready(function() {
   createCloud(frequencyList);
});