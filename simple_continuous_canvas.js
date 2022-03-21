var ContinuousVisualization = function(width, height, context) {
	var height = height;
	var width = width;
	var context = context;


	this.draw = function(objects) {
        for (let it = 0; it < 3 ; it++) {
            for (var i in objects) {
                console.log("hello");
                var p = objects[i];
                if (p.Layer == it){
                    console.log(p.Shape)
                    if (p.Shape == "rect")
                        //context.globalCompositeOperation = 'destination-over';

                        this.drawRectange(p.x, p.y, p.w, p.h, p.Color, p.Filled);
                    if (p.Shape == "circle")
                        this.drawCircle(p.x, p.y, p.r, p.Color, p.Filled);
                    else
                        //context.globalCompositeOperation = 'destination-over';
                        this.drawCustomImage(p.Shape, p.x, p.y, p.scale, p.text, p.text_color, height, width)

            };
            };
           };

	};

	this.drawCustomImage = function (shape, x, y, scale, text, text_color_, height, width) {
                var img = new Image();
                        img.src = "local/".concat(shape);
                if (scale === undefined) {
                        var scale = 1
                }
                //document.write("what")

                // Calculate coordinates so the image is always centered
                console.log("hieght en widht")

                console.log(height, width)

                var dWidth = width;
                var dHeight = height;
                var cx = x ;
                var cy = y;

                //document.write(dWidth)
                //document.write(dHeight);



                // Coordinates for the text
                var tx = (x + 0.5);
                var ty = (y + 0.5) ;


                img.onload = function() {
                        context.drawImage(img, cx, cy, dWidth, dHeight);
                        // This part draws the text on the image
                        if (text !== undefined) {
                                // ToDo: Fix fillStyle
                                // context.fillStyle = text_color;
                                context.textAlign = 'center';
                                context.textBaseline= 'middle';
                                context.fillText(text, tx, ty);
                        }
                }
        }


	this.drawCircle = function(x, y, radius, color, fill) {
		var cx = x * width;
		var cy = y * height;
		var r = radius;

		context.beginPath();
		context.arc(cx, cy, r, 0, Math.PI * 2, false);
		context.closePath();

		context.strokeStyle = color;
		context.stroke();

		if (fill) {
			context.fillStyle = color;
			context.fill();
		}

	};

	this.drawRectange = function(x, y, w, h, color, fill) {
		context.beginPath();
		var dx = w * width;
		var dy = h * height;

		// Keep the drawing centered:
		var x0 = (x*width) - 0.5*dx;
		var y0 = (y*height) - 0.5*dy;

		context.strokeStyle = color;
		context.fillStyle = color;
		if (fill)
			context.fillRect(x0, y0, dx, dy);
		else
			context.strokeRect(x0, y0, dx, dy);
	};

	this.resetCanvas = function() {
		context.clearRect(0, 0, width, height);
		context.beginPath();
	};
};

var Simple_Continuous_Module = function(canvas_width, canvas_height) {
	// Create the element
	// ------------------

	// Create the tag:
	var canvas_tag = "<canvas width='" + canvas_width + "' height='" + canvas_height + "' ";
	canvas_tag += "style='border:1px dotted'></canvas>";
	console.log(canvas_width, canvas_height);
	// Append it to body:
	var canvas = $(canvas_tag)[0];
	$("#elements").append(canvas);

	// Create the context and the drawing controller:
	var context = canvas.getContext("2d");
	var canvasDraw = new ContinuousVisualization(canvas_width, canvas_height, context);

	this.render = function(data) {
		canvasDraw.resetCanvas();
		canvasDraw.draw(data);
	};

	this.reset = function() {
		canvasDraw.resetCanvas();
	};

};