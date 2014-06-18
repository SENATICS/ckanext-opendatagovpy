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

/**
Merge resource form extra fields into a unique
hidden 'schema' field.

Se supone que el nombre del atributo SIEMPRE
está primero.

Author: Rodrigo Parra
*/

/**
Añade un atributo al JSON de inputs de serializeObject.
@param elem El form input a procesar.
@param re Una expresión regular para determinar si el value del input corresponde al atributo.
@param o El JSON donde se añade el value del input.
@param attr Un string que identifica al atributo.

*/
function addAttribute(elem, re, o, attr){
    var found = elem.name.match(re);
    if(found && elem.value){
        var key = found[1];
        if(!o[key]) o[key]={};
        o[key][attr]= elem.value;
    }
    return o;
}

/**
@this {Form}
@return Retorna un JSON de los inputs del form que invoca la función.
El JSON que se retorna tiene el siguiente formato:
{
    0:{
    "name": "edad",
    "type": "integer",
    "description": "Cantidad de meses desde el nacimiento."
    },
    1:{
    "name": "apellido",
    "type": "string",
    "description": "Apellido de la persona."
    }
}
*/
$.fn.serializeObject = function()
{
    var o = {};
    var indexToValue = {}
    var a = this.serializeArray();
    var reAttr = /schema__(\d*)__attr/;
    var reType = /schema__(\d*)__type/;
    var reDescription = /schema__(\d*)__description/;

    $.each(a, function() {
        addAttribute(this, reAttr, o, 'name');
        addAttribute(this, reType, o, 'type');
        addAttribute(this, reDescription, o, 'description');
    });
    return o;
};

/**
@this {Form}
Retorna un JSON de los inputs extras del form que invoca la función, en formato JSON Table Schema.
*/
$.fn.jsonTableSchema = function(){
    var dict = $(this).serializeObject();
    var fields = [];
    for(var key in dict){
        var field_dict = {'name': dict[key]['name'], 'type': dict[key]['type'] , 'description': dict[key]['description']}
        fields.push(field_dict);
    }
    //console.log(JSON.stringify({'fields': fields}));
    return {'fields': fields};
}

$.fn.getExtras = function()
{
    var o = {};
    var indexToValue = {}
    var a = this.serializeArray();
    var reKey = /extras__(\d*)__key/;
    var reValue = /extras__(\d*)__value/;

    $.each(a, function() {
        addAttribute(this, reKey, o, 'key');
        addAttribute(this, reValue, o, 'value');
    });

    var result = [];
    for(var key in o){
        result.push({
                key: o[key]['key'],
                value:o[key]['value']
        });
    }
    return result;
};


$(function() {
    $('.dataset-resource-form').submit(function() {
        $(".disabled :input").attr("disabled", true);
        var schema = $('.dataset-resource-form').jsonTableSchema();
        if(schema['fields'].length === 0){
             $('#field-schema').prop('disabled', true);
        }else{
             $('#field-schema').val(JSON.stringify(schema));
        }

        var extras = $('.dataset-resource-form').getExtras();
        if(extras.length === 0){
             $('#field-extras').prop('disabled', true);
        }else{
             $('#field-extras').val(JSON.stringify(extras));
        }

        //console.log($('#field-extras').val());
        $("div[data-module='custom-fields'] :input").attr("disabled", true);

        return true;
    });
});