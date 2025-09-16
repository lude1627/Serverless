const canvas = document.getElementById('backgroundCanvas');
const ctx = canvas.getContext('2d');

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

const shapes = [];
const numShapes = 15;

for (let i = 0; i < numShapes; i++) {
  shapes.push({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    r: 20 + Math.random() * 30,
    dx: (Math.random() - 0.5) * 2,
    dy: (Math.random() - 0.5) * 2,
    color: `rgba(13, 110, 253, ${Math.random() * 0.3 + 0.1})`
  });
}

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  shapes.forEach(shape => {
    ctx.beginPath();
    ctx.arc(shape.x, shape.y, shape.r, 0, Math.PI * 2);
    ctx.fillStyle = shape.color;
    ctx.fill();

    shape.x += shape.dx;
    shape.y += shape.dy;

    if (shape.x + shape.r > canvas.width || shape.x - shape.r < 0) shape.dx *= -1;
    if (shape.y + shape.r > canvas.height || shape.y - shape.r < 0) shape.dy *= -1;
  });

  requestAnimationFrame(animate);
}

animate();
