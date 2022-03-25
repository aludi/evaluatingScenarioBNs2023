/**
Mesa Canvas Grid Visualization
====================================================================

This is JavaScript code to visualize a Mesa Grid or MultiGrid state using the
HTML5 Canvas. Here's how it works:

On the server side, the model developer will have assigned a portrayal to each
agent type. The visualization then loops through the grid, for each object adds
a JSON object to an inner list (keyed on layer) of lists to be sent to the
browser.

Each JSON object to be drawn contains the following fields: Shape (currently
only rectanges and circles are supported), x, y, Color, Filled (boolean),
Layer; circles also get a Radius, while rectangles get x and y sizes. The
latter values are all between [0, 1] and get scaled to the grid cell.

The browser (this code, in fact) then iteratively draws them in, one layer at a
time. Thus, it should be possible to turn different layers on and off.

Here's a sample input, for a 2x2 grid with one layer being cell colors and the
other agent locations, represented by circles:

{"Shape": "rect", "x": 0, "y": 0, "Color": ["#00aa00", "#aa00aa"], "stroke_color": "red", "Filled": "true", "Layer": 0}

{0:[
        {"Shape": "rect", "x": 0, "y": 0, "w": 1, "h": 1,"Color": ["#00aa00", "#aa00aa"], "stroke_color": "red", "Filled": "true", "Layer": 0},
        {"Shape": "rect", "x": 0, "y": 1, "w": 1, "h": 1, "Color": ["#00aa00", "#aa00aa"], "stroke_color": "red", "Filled": "true", "Layer": 0},
        {"Shape": "rect", "x": 1, "y": 0, "w": 1, "h": 1, "Color": ["#00aa00", "#aa00aa"], "stroke_color": "red", "Filled": "true", "Layer": 0},
        {"Shape": "rect", "x": 1, "y": 1, "w": 1, "h": 1, "Color": ["#00aa00", "#aa00aa"], "stroke_color": "red", "Filled": "true", "Layer": 0}
   ],
 1:[
        {"Shape": "circle", "x": 0, "y": 0, "r": 0.5, "Color": ["#00aa00", "#aa00aa"], "stroke_color": "red", "Filled": "true", "Layer": 1, "text": 'A', "text_color": "white"},
        {"Shape": "circle", "x": 1, "y": 1, "r": 0.5, "Color": ["#00aa00", "#aa00aa"], "stroke_color": "red", "Filled": "true", "Layer": 1, "text": 'B', "text_color": "white"}
        {"Shape": "arrowHead", "x": 1, "y": 0, "heading_x": -1, heading_y: 0, "scale": 0.5, "Color": ["#00aa00", "#aa00aa"], "stroke_color": "red", "Filled": "true", "Layer": 1, "text": 'C', "text_color": "white"}
   ]
}

*/

var GridVisualization = function(image, width, height, gridWidth, gridHeight, context) {


                var img = new Image();
                        img.src = "local/".concat("sun.jpg");

                // Calculate coordinates so the image is always centered

                console.log(img.src);

                img.onload = function() {
                        context.save();
                        context.globalCompositeOperation = 'destination-over';
                        context.drawImage(img, 0, 0, width, height);
                        context.restore();
                        // This part draws the text on the image

        }



};
