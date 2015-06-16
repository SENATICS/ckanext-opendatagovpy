/* Star ratings have gorgeous HTML tooltips */
$('.star-rating').each(function(i,el) {
el = $(el);
el.tooltip({
  title: el.find('.tooltip').html(),
  html: true,
  placement: 'right',
  template: '<div class="tooltip star-rating-tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>',
  delay: 0,
  animation: false
});
});