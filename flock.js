function Block(x, y, s) {
	this.pos = createVector(x, y);
	this.rgb = createVector(floor(random(256)), floor(random(256)), floor(random(256)));
	this.rgbVel = createVector(0, 0, 0);
	this.rgbAcc = createVector(0, 0, 0);
	
	this.size = s;
	this.radius = 15;
	this.maxspeed = 1.5;
	this.maxforce = 0.01;
	
	this.randomizeColor = function() {
		this.rgb.set(floor(random(256)), floor(random(256)), floor(random(256)));
	}
	
	this.setToColor = function(r, g, b) {
		this.rgb.set(r, g, b);
	}
	
	this.applyForce = function(force) {
		this.rgbAcc.add(force);
	}
	
	this.flock = function(blocks) {
		var sep = this.separate(blocks);
		var ali = this.align(blocks);
		var coh = this.cohesion(blocks);
		
		sep.mult(sepSlider.value()); // 1.2
		ali.mult(aliSlider.value()); // 1
		coh.mult(cohSlider.value()); // 2
		
		this.applyForce(sep);
		this.applyForce(ali);
		this.applyForce(coh);
	}
	
	this.seek = function(target) {
		var desired = p5.Vector.sub(target, this.rgb);
		desired.normalize();
		desired.mult(this.maxspeed);
		var steer = p5.Vector.sub(desired, this.rgbVel);
		steer.limit(this.maxforce);
		return steer;
	}
	
	this.separate = function(blocks) {
		var sum = createVector(0, 0, 0);
		var count = 0;
		var steer = createVector(0, 0);
		for (var i = 0; i < blocks.length; i++) {
			if (blocks[i] !== null) {
				var diff = p5.Vector.sub(this.rgb, blocks[i].rgb);
				diff.normalize();
				sum.add(diff);
				count++;
			}
		}
		
		// for (var block in blocks) {
		// 	if (block !== null) {
		// 		var diff = p5.Vector.sub(this.rgb, block.rgb);
		// 		diff.normalize();
		// 		sum.add(diff);
		// 		count++;
		// 	}
		// }
		
		if (count > 0) {
			sum.div(count);
			sum.normalize();
			sum.mult(this.maxspeed);
			
			steer = p5.Vector.sub(sum, this.rgbVel);
			steer.limit(this.maxforce);
		}
		return steer;
	}
	
	this.align = function(blocks) {
		var sum = createVector(0, 0, 0);
		var count = 0;
		for (var i = 0; i < blocks.length; i++) {
			if (blocks[i] !== null) {
				sum.add(blocks[i].rgbVel);
				count++;
			}
		}
		
		// for (var block in blocks) {
		// 	if (block !== null) {
		// 		sum.add(block.rgbVel);
		// 		count++;
		// 	}
		// }
		if (count > 0) {
			sum.div(count);
			sum.normalize();
			sum.mult(this.maxspeed);
			var steer = p5.Vector.sub(sum, this.rgbVel);
			steer.limit(this.maxforce);
			return steer;
		} else {
			return createVector(0, 0, 0);
		}
	}
	
	this.cohesion = function(blocks) {
		var sum = createVector(0, 0, 0);
		var count = 0;
		for (var i = 0; i < blocks.length; i++) {
			if (blocks[i] !== null) {
				sum.add(blocks[i].rgb);
				count++;
			}
		}
		
		
		// for (var block in blocks) {
		// 	if (block !== null) {
		// 		console.log(block.rgbVel);
		// 		sum.add(block.rgb); // add location
		// 		count++;
		// 	}
		// }
		if (count > 0) {
			sum.div(count);
			return this.seek(sum);
		} else {
			return createVector(0, 0, 0);
		}
	}
	
	this.display = function() {
		noStroke();
		fill(this.rgb.x, this.rgb.y, this.rgb.z);
		rect(this.pos.x, this.pos.y, this.size, this.size);
	}
	
	this.update = function() {
		this.rgbVel.add(this.rgbAcc);
		this.rgbVel.limit(this.maxspeed);
		this.rgb.add(this.rgbVel);
		
		this.edges();
		
		this.rgbAcc.mult(0); // reset acceleration
	}
	
	this.edges = function() {
		if (this.rgb.x > 255) {
			this.rgb.x = 255;
			this.rgbVel.x *= -1;
		} else if (this.rgb.x < 0) {
			this.rgb.x = 0;
			this.rgbVel.x *= -1;
		}
		
		if (this.rgb.y > 255) {
			this.rgb.y = 255;
			this.rgbVel.y *= -1;
		} else if (this.rgb.y < 0) {
			this.rgb.y = 0;
			this.rgbVel.y *= -1;
		}
		
		if (this.rgb.z > 255) {
			this.rgb.z = 255;
			this.rgbVel.z *= -1;
		} else if (this.rgb.z < 0) {
			this.rgb.z = 0;
			this.rgbVel.z *= -1;
		}
	}
}