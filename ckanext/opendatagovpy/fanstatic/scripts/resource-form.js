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