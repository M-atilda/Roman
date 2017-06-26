// file:    display.js
// author:  mi-na
// date:    17-06-25


var Cleature = function(search_str_l, body_structure_lll) {
    this.str_l = search_str_l;
    this.body_lll = body_structure_lll;
}

// global variables
var g_cleatures_l = [];
// for debug
var none_zero_counter;

function setCleaturesInfo() {
    var step;
    for (step = 0; step < cleature_num; step++) {
        g_cleatures_l.push(new Cleature(next_search_words_l[step], body_structures_l[step]));
    }
}



window.addEventListener("load", function() {
    threeStart();
    console.log(none_zero_counter);
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
var g_cubes_ll = [];

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
    g_cameras_l[num].position.set(60, 60, 60);
    g_cameras_l[num].up.set(0, 0, 1);
    g_cameras_l[num].lookAt({x:0,y:0,z:0});
}



function initObj(num) {
    var cubes_l = [];
    var i;
    var j;
    var k;
    for (i = 0; i < box_length; i++) {
        for (j = 0; j < box_length; j++) {
            for (k = 0; k < box_length; k++) {
                if (g_cleatures_l[num].body_lll[i][j][k] != 0) {
                    var color_num = parseInt(g_cleatures_l[num].body_lll[i][j][k].slice(1), 16);
                    none_zero_counter++;
                    var geo = new THREE.SphereGeometry(1);
                    var mat = new THREE.MeshBasicMaterial({ color: color_num });
                    var cubeObj = new THREE.Mesh(geo, mat);
                    cubeObj.position.set(10+i, 10+j, 10+k);
                    g_scenes_l[num].add(cubeObj);
                    cubes_l.push(cubeObj);
                }
            }
        }
    }
    g_cubes_ll.push(cubes_l);
}

function draw(num) {
    g_renderers_l[num].render(g_scenes_l[num], g_cameras_l[num]);
}
