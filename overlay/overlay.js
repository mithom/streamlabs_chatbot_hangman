//--------------------------
// Variables
//--------------------------
var serviceUrl = "ws://127.0.0.1:3337/streamlabs";
var s = document.styleSheets[1];
var imageOrder = {
    1: [10],
    2: [3, 10],
    3: [3, 5, 10],
    4: [3, 4, 5, 10],
    5: [3, 4, 5, 7, 10],
    6: [3, 4, 5, 7, 8, 10],
    7: [3, 4, 5, 6, 7, 8, 10],
    8: [1, 3, 4, 5, 6, 7, 8, 10],
    9: [0, 1, 3, 4, 5, 6, 7, 8, 10],
    10: [0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
    11: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
};
var cutImages = [];
window.onload = doStuff;


function doStuff() {
    prepareImages();
    init_sockets();
}

function reload_settings(json_data) {
    settings = JSON.parse(json_data);
    prepareImages();
}

var turn = 0;
var image = new Image();
function prepareImages() {
    image.onload = _prepareImages;
    image.src = "hangman_images/10.png";
}
function _prepareImages() {
    cutImages = [];
    for (var y = 0; y < settings["nb_turns"]; ++y) {
        var canvas = document.createElement('canvas');
        canvas.width = image.width;
        canvas.height = image.height;
        var context = canvas.getContext('2d');
        context.drawImage(image, 0, image.height - Math.round(image.height * (y+1) / settings["nb_turns"]), image.width, Math.round(image.height * (y+1) / settings["nb_turns"]), 0,
            image.height - Math.round(image.height * (y+1) / settings["nb_turns"]), image.width, Math.round(image.height * (y+1) / settings["nb_turns"]) );
        cutImages.push(canvas.toDataURL());
    }
}

function init_sockets() {
    var socket = new WebSocket(serviceUrl);
    //--------------------------
    // Open Event
    //--------------------------
    socket.onopen = function () {
        // Format your Auth info
        var auth = {
            author: "mi_thom + mathiasAC",
            website: "https://www.twitch.tv/mi_thom",
            api_key: API_Key, //this is defined by right click insert api key
            events: [
                "EVENT_START_HANGMAN",
                "EVENT_END_HANGMAN",
                "EVENT_GUESSED_WORD_WRONG_HANGMAN",
                "EVENT_GUESSED_LETTER_WRONG_HANGMAN",
                "EVENT_RELOAD_SETTINGS_HANGMAN"
            ]
        };
        socket.send(JSON.stringify(auth));
    };

    //--------------------------
    // Error Event
    //--------------------------
    socket.onerror = function (error) {
        console.log("Error: " + error)
    };

    //--------------------------
    // Message Event
    //--------------------------
    socket.onmessage = function (message) {
        var data = JSON.parse(message.data);
        var main_body = document.getElementById("main_body");
        switch (data["event"]) {
            case "EVENT_RELOAD_SETTINGS_HANGMAN":
                reload_settings(data["data"]);
                break;
            case 'EVENT_START_HANGMAN':
                turn = 0;
                if(main_body.firstChild != null){
                    main_body.removeChild(main_body.firstChild);
                }
                break;
            case 'EVENT_END_HANGMAN_HANGMAN':
                setTimeout(function () {
                    if(main_body.firstChild != null){
                        main_body.removeChild(main_body.firstChild);
                    }
                }, settings["vanish_delay"]*1000);
                break;
            case 'EVENT_GUESSED_WORD_WRONG_HANGMAN':
                showNextImage();
                break;
            case 'EVENT_GUESSED_LETTER_WRONG_HANGMAN':
                showNextImage();
        }
    };

    //--------------------------
    // Close Event
    //--------------------------
    socket.onclose = function () {
        console.log("Connection closed")
    };
}

function showNextImage() {
    turn += 1;
    var src;
    if(settings["nb_turns"] in imageOrder){
        src ="hangman_images/" + imageOrder[settings["nb_turns"]][turn-1] + ".png"
    }else{
        src = cutImages[turn-1];
    }
    add_hangman_image(src)
}

function add_hangman_image(src) {
    var img = document.createElement("img");
    img.setAttribute("src", src);
    Caman(img, function () {
        this.newLayer(function () {
            this.setBlendingMode("normal");
            var rgba = getRGBA();
            var r = rgba[0];
            var g = rgba[1];
            var b = rgba[2];
            this.fillColor(r, g, b);
        });
        this.render();
    });
    var main_body = document.getElementById("main_body");
    if(main_body.firstChild != null){
        main_body.removeChild(main_body.firstChild);
    }
    main_body.appendChild(img);
}

function getRGBA() {
    return settings["hangman_color"].slice(5, -1).split(',').map(x => parseInt(x));
}

function changeStylesheetRule(stylesheet, selector, property, value) {
    selector = selector.toLowerCase();
    property = property.toLowerCase();
    value = value.toLowerCase();

    for (var i = 0; i < stylesheet.cssRules.length; i++) {
        var rule = stylesheet.cssRules[i];
        if (rule.selectorText === selector) {
            rule.style[property] = value;
            return;
        }
    }

    stylesheet.insertRule(selector + " { " + property + ": " + value + "; }", 0);
}

// changeStylesheetRule(s, "body", "color", "rebeccapurple");
