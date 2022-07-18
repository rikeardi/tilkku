
var home = [env.HOME_LAT, env.HOME_LON];
var mobile_home = [home[0] + 0.001, home[1] - 0.009];
var home_zoom = env.HOME_ZOOM;
var map_zoom = true;

var map_background = map_servers[settings.map.server].layer.addTo(map);
var map_grid = null;
var opened_area = null;
var opened_marker = null;
var user_marker = null;
var map_locator = null;

map_zoom = true;
if(mobile) map_zoom = false;

map = L.map('map', {
    zoomControl: map_zoom,
    center: settings.map.center,
    zoom: settings.map.zoom,
});

map_scale = L.control.scale({
    imperial: false,
    metric: true,
    position: 'bottomleft'
});

const forwarder = L.eventForwarder({
    map: map,
    events: {
        click: true,
        mousemove: false,
    },
}).enable();

map_servers.forEach(function(server) {
    server.layer = L.tileLayer(server.url, {
        attribution: server.attribution,
    });
});

function map_set_bg() {
    map_background.remove();
    map_background = map_servers[settings.map.server].layer.addTo(map);
}

function map_set_wms() {
    var wms_layer = L.tileLayer.wms(wms_servers[0].url, {
        layers: wms_servers[0].layer,
        format: 'image/png',
        transparent: true,
    }).addTo(map);
}

function toRad(x) {
    return x * Math.PI / 180;
}

function toDeg(x) {
    return x * 180 / Math.PI;
}

function map_calculate_grid() {
    env.GRID_SIZE = parseFloat(env.GRID_SIZE);
    env.GRID_LAT = parseFloat(env.GRID_LAT);
    env.GRID_LON = parseFloat(env.GRID_LON);
    env.GRID_COLS = parseInt(env.GRID_COLS);
    env.GRID_ROWS = parseInt(env.GRID_ROWS);

    var earth_radius = 6378137;
    var dist = env.GRID_SIZE / earth_radius;

    var lat = toRad(env.GRID_LAT);
    var lon = toRad(env.GRID_LON);

    var brng_x = toRad(180);
    var brng_y = toRad(90);

    var lat_x = Math.asin(Math.sin(lat) * Math.cos(dist) + Math.cos(lat) * Math.sin(dist) * Math.cos(brng_x));
    var lon_x = lon + Math.atan2(Math.sin(brng_y) * Math.sin(dist) * Math.cos(lat), Math.cos(dist) - Math.sin(lat) * Math.sin(lat_x));

    var grid_cols = [];
    if(env.GRID_COLS > 99) {
        for(var i = 0; i < env.GRID_COLS; i++) {
            grid_cols.push(("00" + (i+1)).slice(-3));
        }
    } else if(env.GRID_COLS > 9) {
        for(var i = 0; i < env.GRID_COLS; i++) {
            grid_cols.push(("0" + (i+1)).slice(-2));
        }
    } else {
        for(var i = 0; i < env.GRID_COLS; i++) {
            grid_cols.push(i+1);
        }
    }

    var grid_rows = [];
    var pre_letter = "";
    var letter = "A";
    for(var i = 0; i < env.GRID_ROWS; i++) {
        grid_rows.push(pre_letter + letter);
        letter = String.fromCharCode(letter.charCodeAt(0) + 1);
        if(letter == "[") {
            pre_letter = "A";
            letter = "A";
        }
    }

    map_grid = {
        x: env.GRID_LAT,
        y: env.GRID_LON,
        inv_x: false,
        inv_y: false,
        move_x: toDeg(lat_x) - env.GRID_LAT,
        move_y: toDeg(lon_x) - env.GRID_LON,
        cols: grid_cols,
        rows: grid_rows,
        end: [],
        layer: null,
    };

    grid_end = [map_grid.x + map_grid.rows.length * map_grid.move_x, map_grid.y + map_grid.cols.length * map_grid.move_y];

    if(grid_end[0] < env.GRID_LAT) {
        map_grid.min_x = grid_end[0];
        map_grid.max_x = env.GRID_LAT;
        map_grid.inv_x = true;
    } else {
        map_grid.min_x = env.GRID_LAT;
        map_grid.max_x = grid_end[0];
    }

    if(grid_end[1] < env.GRID_LON) {
        map_grid.min_y = grid_end[1];
        map_grid.max_y = env.GRID_LON;
        map_grid.inv_y = true;
    } else {
        map_grid.min_y = env.GRID_LON;
        map_grid.max_y = grid_end[1];
    }
}

function map_set_grid() {
    map_grid.layer = L.layerGroup().addTo(map);

    if(!settings.map.grid) {
        if(map_grid.layer != null) {
            map_grid.layer.eachLayer(function(layer) {
                map.removeLayer(layer);
            });
        }
    } else {
        var row = 0;
        var col = 0;
        for(var row = 0; row <= map_grid.rows.length; row++) {
            var rowLine = L.polyline([
                [map_grid.x + row * map_grid.move_x, map_grid.y],
                [map_grid.x + row * map_grid.move_x, map_grid.y + map_grid.cols.length * map_grid.move_y],
            ], {
                className: 'grid-line',
                interactive: false,
            }).addTo(map_grid.layer);
        }
        for (var col = 0; col <= map_grid.cols.length; col++) {
            var colLine = L.polyline([
                [map_grid.x, map_grid.y + col * map_grid.move_y],
                [map_grid.x + map_grid.rows.length * map_grid.move_x, map_grid.y + col * map_grid.move_y],
            ], {
                className: 'grid-line',
                interactive: false,
            }).addTo(map_grid.layer);
        }

        var tooltip_style = {
            permanent: true,
            direction: "center",
        }

        var lefttop_x = map_grid.min_x;
        var lefttop_y = map_grid.min_y;
        if(map_grid.inv_x) {
            lefttop_x = map_grid.max_x;
        }
        if(map_grid.inv_y) {
            lefttop_y = map_grid.max_y;
        }

        for(var i = 0; i < map_grid.rows.length; i++) {
            var startpoint = [lefttop_x + i * map_grid.move_x, lefttop_y];
            var endpoint = [lefttop_x + (i+1) * map_grid.move_x, lefttop_y - map_grid.move_y];
            var rowHeader = L.rectangle([startpoint, endpoint], {
                opacity: 0,
                fillOpacity: 0,
                interactive: false,
            });
            rowHeader.bindTooltip("<div class='grid-header'>" + map_grid.rows[i] + "</div>", tooltip_style);
            map_grid.layer.addLayer(rowHeader);
        }

        for(var i = 0; i < map_grid.cols.length; i++) {
            var startpoint = [lefttop_x, lefttop_y + i * map_grid.move_y];
            var endpoint = [lefttop_x - map_grid.move_x, lefttop_y + (i+1) * map_grid.move_y];
            var colHeader = L.rectangle([startpoint, endpoint], {
                opacity: 0,
                fillOpacity: 0,
                interactive: false,
            });
            colHeader.bindTooltip("<div class='grid-header'>" + map_grid.cols[i] + "</div>", tooltip_style);
            map_grid.layer.addLayer(colHeader);
        }
    }

    var gridbox = L.rectangle([[map_grid.min_x, map_grid.min_y], [map_grid.max_x, map_grid.max_y]], {
        weight: 1,
        fillOpacity: 0,
        stroke: false,
        cursor: 'none',
    }).addTo(map_grid.layer);

    gridbox.on("mousemove", function(e) {
        map_show_coords(e.latlng);
    });

    gridbox.on("mouseout", function(e) {
        $("#map-coordinates").addClass("is-hidden");
    });
}

function map_set_scale() {
    if(settings.map.scale == 1) {
        map_scale.addTo(map);
    } else {
        map_scale.remove();
    }
}

function map_set_names() {
    var zoom = map.getZoom();
    map_layers.forEach(function(layer) {

        if(layer.active) {
            layer.layer.eachLayer(function(layer2) {
                var tooltip = layer2.getTooltip();
                if(tooltip) {
                    this.map.closeTooltip(tooltip);
                }
                if(tooltip && zoom >= layer.style.min_zoom && zoom <= layer.style.max_zoom && settings.map.names) {
                    this.map.addLayer(tooltip);
                }
            });

        }
    });
}

map_layers.forEach(function(layer) {
    layer.areas.forEach(function(area) {
        for(var i = 0; i < area.coordinates.length; i++) {
            area.coordinates[i] = [area.coordinates[i][1], area.coordinates[i][0]];
        }
    });
    layer.markers.forEach(function(marker) {
        marker.coordinates = [marker.coordinates[1], marker.coordinates[0]];
    });
});

function map_set_layers() {
    for(var i = 0; i < map_layers.length; i++) {
        var layer = map_layers[i];
        if(layer.layer) {
            layer.layer.remove();
        }

        var style = {
            color: layer.style.stroke,
            fillColor: layer.style.fill,
            opacity: layer.style.opacity + 0.2,
            fillOpacity: layer.style.opacity,
            'stroke-width': layer.style.stroke_width,
        }

        var tooltip_style = {
            opacity: layer.style.opacity + 0.2,
            permanent: true,
            direction: "center",
        }

        var marker_style = {
            opacity: 0,
        }

        layer.active = false;

        if(settings.map.layers.includes(i)) {
            layer.layer = L.featureGroup();
            layer.active = true;

            layer.areas.forEach(function(area) {
                var polydata = style;
                polydata.id = area.id;
                area_layer = L.polygon(area.coordinates, polydata);
                area_layer.bindTooltip("<div style='color: " + layer.style.stroke + "; font-size: " + layer.style.font_size + "px'>" + area.name + "</div>", tooltip_style);
                area_layer.addTo(layer.layer);
                area_layer.on("click", function(e) {
                    e.originalEvent._stopped = true;
                    open_area(e.target.options.id);
                });

                area.active = true;
            });

            layer.markers.forEach(function(marker) {
                var marker_layer = L.marker(marker.coordinates, marker_style)
                marker_layer.bindTooltip("<div style='color: " + layer.style.stroke + "; font-size: " + layer.style.font_size + "px'>" + marker.name + "</div>", tooltip_style);
                marker_layer.addTo(layer.layer);
                marker_layer.on("click", function(e) {
                    open_marker(e.target.options.id);
                });

                marker.active = true;
            });

            layer.layer.addTo(map);
        } else {
            layer.active = false;
            layer.layer = L.featureGroup();

            layer.areas.forEach(function(area) {
                area.active = false;
            });

            layer.markers.forEach(function(marker) {
                marker.active = false;
            });
        }
    }
}

function map_get_layer(id) {
    var correct_layer = null;
    map.eachLayer(function(layer) {
        if(layer.options.id == id) {
            correct_layer = layer;
            return;
        }
    });
    return correct_layer;
}

function open_area(id) {
    map_layers.forEach(function(layer) {
        layer.areas.forEach(function(area) {
            if(area.id == id) {
                opened_area = area;
                return;
            }
        });
    });
    open_site_modal(opened_area.id, null);
}

function open_marker(id) {
    map_layers.forEach(function(layer) {
        layer.markers.forEach(function(marker) {
            if(marker.id == id) {
                opened_marker = marker;
                return;
            }
        });
    });
    open_site_modal(null, opened_marker.id);
}

function map_show_coords(latlng) {
    var min_x = map_grid.min_x;
    if(map_grid.inv_x) {
        min_x = map_grid.max_x;
    }
    var min_y = map_grid.min_y;
    if(map_grid.inv_y) {
        min_y = map_grid.max_y;
    }
    var coord = [Math.floor((latlng.lat - min_x) / map_grid.move_x), Math.floor((latlng.lng - min_y) / map_grid.move_y)];
    var row = map_grid.rows[coord[0]];
    var col = map_grid.cols[coord[1]];
    $("#map-coordinates p").text(row + col);
    $("#map-coordinates").removeClass("is-hidden");
}

function search_coords(coords, center=true) {
    var row = coords.substring(0, 1).toUpperCase();
    var col = coords.substring(1, 3);
    var min_x = map_grid.min_x;
    if(map_grid.inv_x) {
        min_x = map_grid.max_x;
    }
    var min_y = map_grid.min_y;
    if(map_grid.inv_y) {
        min_y = map_grid.max_y;
    }
    var coord = [map_grid.rows.indexOf(row), map_grid.cols.indexOf(col)];
    var lat_0 = min_x + coord[0] * map_grid.move_x;
    var lng_0 = min_y + coord[1] * map_grid.move_y;
    var lat_1 = lat_0 + map_grid.move_x;
    var lng_1 = lng_0 + map_grid.move_y;
    var highlight_layer = L.featureGroup().addTo(map);
    var highlight = L.rectangle([[lat_0, lng_0], [lat_1, lng_1]], {
        color: '#ff0000',
        fillColor: '#ff0000',
        fillOpacity: 0.2,
        weight: 1,
    }).addTo(highlight_layer);
    highlight.bindTooltip("<div style='color: #ff0000; font-size: " + map_grid.font_size + "px'>" + row + col + "</div>", {
        permanent: true,
        direction: "center",
    });
    if(center) {
        map.fitBounds(highlight_layer.getBounds());
    }
    if(mobile && settings.menu == "visible") {
        toolbox_menu();
    }
    setTimeout(function() {
        highlight_layer.removeLayer(highlight);
    }, 3000);
}

function map_user_coords(latlng) {
    var min_x = map_grid.min_x;
    if(map_grid.inv_x) {
        min_x = map_grid.max_x;
    }
    var min_y = map_grid.min_y;
    if(map_grid.inv_y) {
        min_y = map_grid.max_y;
    }
    var coord = [Math.floor((latlng.lat - min_x) / map_grid.move_x), Math.floor((latlng.lng - min_y) / map_grid.move_y)];
    var row = map_grid.rows[coord[0]];
    var col = map_grid.cols[coord[1]];
    search_coords(row + col, false);
}

function map_user_update() {
    if(navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude;
            var lng = position.coords.longitude;
            var latlng = L.latLng(lat, lng);
            user_marker.setLatLng(latlng);
        });
    }
}

function map_user_location() {
    if(settings.map.location == 1) {
        user_marker = L.marker([0, 0], {
            icon: L.icon({
                iconUrl: "{% static 'img/user.png' %}",
                iconSize: [32, 32],
                iconAnchor: [16, 16],
            }),
            draggable: false,
            opacity: 0.8,
        }).addTo(map);
        user_marker.on("click", function() {
            map_user_coords(user_marker.getLatLng());
        });
        user_marker.on("tap", function() {
            map_user_coords(user_marker.getLatLng());
        });
        map_locator = navigator.geolocation.watchPosition(function(position) {
            var lat = position.coords.latitude;
            var lng = position.coords.longitude;
            var latlng = L.latLng(lat, lng);
            user_marker.setLatLng(latlng);
        });
    } else {
        if(map_locator) {
            navigator.geolocation.clearWatch(map_locator);
        }
        if(user_marker) {
            map.removeLayer(user_marker);
            user_marker = null;
        }
    }
}

function map_init() {
    map_set_bg();
    map_calculate_grid();
    map_set_scale();
    map_set_layers();
    map_set_grid();
    map_set_names();
    map_user_location();
    //map_set_wms();
}

map.on('zoomend', function() {
    map_set_names();
});

map.on("moveend", function() {
    settings.map.center = map.getCenter();
    settings.map.zoom = map.getZoom();
    refresh_settings();
});

$(document).ready(function() {
    map_init();
});