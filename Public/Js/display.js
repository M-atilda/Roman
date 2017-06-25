// file:    display.js
// author:  mi-na
// date:    17-06-25


var Cleature = function(search_str_l, body_structure_lll) {
    this.str_l = search_str_l;
    this.body_lll = body_structure_lll;
}

// global variables
var g_cleatures_l = [];

function setCleaturesInfo() {
    var step;
    for (step = 0; step < cleature_num; step++) {
        g_cleatures_l.push(new Cleature(next_search_words_l[step], body_structures_l[step]));
    }
}



window.addEventListener("load", function() {
    threeStart();
});

function threeStart() {
    setCleaturesInfo();
    var i;
    for (i = 0; i < cleature_num; i++) {
        initThree(i);
        initCamera(i);
        initObj(i);
        draw(i);
    }
}


// global instances
var g_renderers_l = [];
var g_scenes_l = [];
var g_canvas_frames_l = [];
var g_cameras_l = [];
var g_axis_l = [];

function initThree(num) {
    var dom_name = 'canvas-frame_' + (num + 1);
    g_canvas_frames_l.push(document.getElementById(dom_name));
    console.log(dom_name);
    g_renderers_l.push(new THREE.WebGLRenderer());
    if (!g_renderers_l[num]) alert("failed to initialize three-js");
    g_renderers_l[num].setSize(g_canvas_frames_l[num].clientWidth, g_canvas_frames_l[num].clientHeight);
    g_canvas_frames_l[num].appendChild(g_renderers_l[num].domElement);
    g_renderers_l[num].setClearColor(0x008b8b, 1.0);
    g_scenes_l.push(new THREE.Scene());
}

function initCamera(num) {
    g_cameras_l.push(new THREE.PerspectiveCamera(45, g_canvas_frames_l[num].clientWidth / g_canvas_frames_l[num].clientHeight, 1, 10000));
    g_cameras_l[num].position.set(50, 50, 100);
    g_cameras_l[num].up.set(0, 0, 1);
    g_cameras_l[num].lookAt({x:0,y:0,z:0});
}

function initObj(num) {
    g_axis_l.push(new THREE.AxisHelper(50));
    g_scenes_l[num].add(g_axis_l[num]);
    g_axis_l[num].position.set(0, 0, 0);
}

function draw(num) {
    g_renderers_l[num].render(g_scenes_l[num], g_cameras_l[num]);
}
