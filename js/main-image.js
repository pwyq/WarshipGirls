// <!-- images resolution 1600 x 1200 -->
var box_images = [
  "images/uss_navy.jpg",
  "images/US_fleet_at_Majuro_Atoll_1944.jpg"
];

var size = box_images.length
var x = Math.floor(size*Math.random())
document.getElementById('box-lineup').src=box_images[x];