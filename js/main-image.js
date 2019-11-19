// <!-- images resolution 1600 x 1200 -->
var box_lineup_images = [
  "images/uss_navy.jpg",
  "images/US_fleet_at_Majuro_Atoll_1944.jpg"
];
var lineup_size = box_lineup_images.length
var lineup_x = Math.floor(lineup_size*Math.random())
document.getElementById('box-lineup').src=box_lineup_images[lineup_x];

var box_ordance_images = [
  "images/BB-57.jpg",
  "images/BB-63.jpg"
];
var ordance_size = box_ordance_images.length
var ordance_x = Math.floor(ordance_size*Math.random())
document.getElementById('box-ordance').src=box_ordance_images[ordance_x];