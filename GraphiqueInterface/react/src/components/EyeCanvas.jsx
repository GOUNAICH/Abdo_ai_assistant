import React, { useEffect, useRef, useState } from 'react';

const EyeWidget = () => {
  const canvasRef = useRef(null);
  const [eyeState, setEyeState] = useState("normal");
  const [isBlinking, setIsBlinking] = useState(false);
  const [pupilOffset, setPupilOffset] = useState({ x: 0, y: 0 });
  const [mouthState, setMouthState] = useState("normal");

  // Blink timer
  useEffect(() => {
    const blinkInterval = setInterval(() => {
      setIsBlinking(true);
      setTimeout(() => setIsBlinking(false), 150);
    }, 4000);

    return () => clearInterval(blinkInterval);
  }, []);

  // Random eye movement
  useEffect(() => {
    const moveInterval = setInterval(() => {
      setPupilOffset({
        x: Math.random() * 20 - 10,
        y: Math.random() * 10 - 5
      });
    }, 2000);

    return () => clearInterval(moveInterval);
  }, []);

  // Drawing function
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    // Drawing settings
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    // Draw eyes
    const eyeWidth = 80;
    const eyeHeight = isBlinking ? 10 : 50;
    const gap = 40;
    
    const leftEyeX = (width - (2 * eyeWidth + gap)) / 2;
    const leftEyeY = height / 2 - eyeHeight / 2;
    const rightEyeX = leftEyeX + eyeWidth + gap;
    const rightEyeY = leftEyeY;

    // Eye color
    ctx.fillStyle = '#00CED1';
    
    // Draw eye shapes
    ctx.beginPath();
    ctx.ellipse(leftEyeX + eyeWidth/2, leftEyeY + eyeHeight/2, eyeWidth/2, eyeHeight/2, 0, 0, 2 * Math.PI);
    ctx.fill();
    ctx.beginPath();
    ctx.ellipse(rightEyeX + eyeWidth/2, rightEyeY + eyeHeight/2, eyeWidth/2, eyeHeight/2, 0, 0, 2 * Math.PI);
    ctx.fill();

    if (!isBlinking) {
      // Draw pupils
      const pupilSize = 20;
      ctx.fillStyle = '#000000';

      let pupilOffsetX = pupilOffset.x;
      let pupilOffsetY = pupilOffset.y;

      if (eyeState === "thinking") {
        pupilOffsetY = -10;
      } else if (eyeState === "listening") {
        pupilOffsetX = pupilOffset.x * 2;
      } else if (eyeState === "speaking") {
        pupilOffsetY = 5;
      }

      ctx.beginPath();
      ctx.arc(leftEyeX + eyeWidth/2 + pupilOffsetX, leftEyeY + eyeHeight/2 + pupilOffsetY, pupilSize/2, 0, 2 * Math.PI);
      ctx.fill();
      ctx.beginPath();
      ctx.arc(rightEyeX + eyeWidth/2 + pupilOffsetX, rightEyeY + eyeHeight/2 + pupilOffsetY, pupilSize/2, 0, 2 * Math.PI);
      ctx.fill();
    }

    // Draw mouth
    const mouthWidth = 60;
    const mouthHeight = 10;
    const mouthX = (width - mouthWidth) / 2;
    const mouthY = height / 2 + 50;

    ctx.fillStyle = '#000000';
    if (mouthState === "happy") {
      ctx.beginPath();
      ctx.arc(mouthX + mouthWidth/2, mouthY, mouthWidth/2, 0, Math.PI);
      ctx.fill();
    } else if (mouthState === "sad") {
      ctx.beginPath();
      ctx.arc(mouthX + mouthWidth/2, mouthY + mouthHeight, mouthWidth/2, Math.PI, 2 * Math.PI);
      ctx.fill();
    } else {
      ctx.fillRect(mouthX, mouthY, mouthWidth, mouthHeight);
    }
  }, [isBlinking, eyeState, pupilOffset, mouthState]);

  return (
    <canvas 
      ref={canvasRef}
      width={400}
      height={300}
      className="w-full max-w-[400px] h-[300px]"
      style={{
        
        //backgroundColor: "yellow",
        
      }}
    />
  );
};

export default EyeWidget;