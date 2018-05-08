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
 * Header Image roll effect
 * Author: Samuele Santi
 * Date: 2012-11-21
 * Time: 11:17 AM
 *
 * Updated to align image footer
 * to the bottom right corner
 * of the background image
 *
 * Author: Rodrigo Parra
 * Date: 2014-06-14
 */

$(document).ready(function(){

    var conf = {
        fadeTime: 800,
        rollTime: 6000
    };

    var rollImageInit = function(imgroll) {
        imgroll.children().each(function(idx,item){
            if (idx==0) {
                $(item).show();
            }
            else {
                $(item).hide();
            }
        });
    };

    var rollImageNext = function(imgroll) {

        var imgidx = imgroll.data('rollimg-idx') || 0,
            imgcount = imgroll.children().length,
            nextidx = (imgidx + 1) % imgcount,
            oldimg = $(imgroll.children()[imgidx]);

        imgroll.children().each(function(idx,item){
            if (idx==imgidx) {
                $(item).show().css('z-index', '2');
            }
            else if (idx==nextidx) {
                $(item).show().css('z-index', '1');
            }
            else {
                $(item).hide();
            }
        });

        // To allow attaching extra handlers
        $(imgroll).trigger('roll-start', {
            target: $(imgroll.children()[nextidx]),
            conf: conf
        });

        oldimg.fadeOut(conf.fadeTime);
        imgroll.data('rollimg-idx', nextidx);
    };

    var updateImageMargin = function(imgroll) {


        $('.footer-container').each(function( index ) {
            var img = new Image;
            /*img.src = $(this).parent().css('background-image').replace(/url\(|\)$/ig, "");
            var footer = $(this);

            $(img).on('load', function(){
                var bgImgWidth = img.width;
                var margin = 0;
                if(bgImgWidth < $(window).width() && bgImgWidth > 0){
                    margin = ($(window).width() - bgImgWidth)/2;
                }
                footer.css('margin-right', margin);
            });*/

        });
    }

    $('.homepage-slider-ng .images-wrapper').each(function(){
        var imgroll = $(this);

        updateImageMargin(imgroll);
        rollImageInit(imgroll);
        setInterval(function(){
            updateImageMargin(imgroll);
            rollImageNext(imgroll);
        }, conf.rollTime);
    });

});