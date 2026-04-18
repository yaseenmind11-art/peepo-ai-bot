<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <script src="https://cesium.com/downloads/cesiumjs/releases/1.104/Build/Cesium/Cesium.js"></script>
  <link href="https://cesium.com/downloads/cesiumjs/releases/1.104/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
  <style>
    #cesiumContainer { width: 100%; height: 100vh; margin: 0; background: #000; }
    body { margin: 0; overflow: hidden; }
    #hud {
      position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
      width: 400px; height: 300px; border: 2px solid #00ff00; pointer-events: none;
      color: #00ff00; font-family: monospace; display: flex; justify-content: space-between; padding: 20px;
    }
    #ui { position: absolute; top: 10px; left: 10px; z-index: 100; }
    #search { padding: 10px; width: 250px; border-radius: 5px; border: 1px solid #00ff00; background: rgba(0,0,0,0.8); color: white; }
  </style>
</head>
<body>
  <div id="ui"><input type="text" id="search" placeholder="Enter Airport or City..."></div>
  <div id="hud">
    <div id="speed">SPD: 0 kn</div>
    <div id="crosshair">+</div>
    <div id="alt">ALT: 0 ft</div>
  </div>
  <div id="cesiumContainer"></div>

  <script>
    Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJjNDM2YzA1OS1jNzFjLTRmNzAtYWRlNC0wODAwYzUzMmJiZWQiLCJpZCI6NDE3NTMxLCJpYXQiOjE3NzYwODA0ODZ9.MYY2-6pFSiV00YlGiEp5TX_Ic2cp8kn4ifbzdQgyFbs';

    const viewer = new Cesium.Viewer('cesiumContainer', {
      terrainProvider: Cesium.createWorldTerrain(),
      animation: false, timeline: false, baseLayerPicker: false
    });

    // 1. Load HD 3D World
    async function initWorld() {
      const buildings = await Cesium.createGooglePhotorealistic3DTileset();
      viewer.scene.primitives.add(buildings);
    }
    initWorld();

    // 2. Load the F-16 Model
    const jetPosition = Cesium.Cartesian3.fromDegrees(31.405, 30.121, 500);
    const jetEntity = viewer.entities.add({
      name: 'F-16 Fighting Falcon',
      position: jetPosition,
      model: {
        uri: 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Duck/glTF/Duck.gltf', // PLACEHOLDER: Swap with F-16 .glb URL
        minimumPixelSize: 128,
        maximumScale: 20000
      }
    });

    viewer.trackedEntity = jetEntity; // Camera follows the jet

    // 3. Flight Controls
    let speed = 0.0001; 
    let pitch = 0;
    let heading = 0;

    window.addEventListener('keydown', (e) => {
      if (e.key === 'w') pitch += 0.01; // Nose Up
      if (e.key === 's') pitch -= 0.01; // Nose Down
      if (e.key === 'a') heading -= 0.01; // Turn Left
      if (e.key === 'd') heading += 0.01; // Turn Right
      if (e.key === 'Shift') speed += 0.0001; // Afterburner
    });

    function flightLoop() {
      const position = jetEntity.position.getValue(viewer.clock.currentTime);
      if (position) {
        // Update position based on heading and speed
        const cartographic = Cesium.Cartographic.fromCartesian(position);
        const newLon = cartographic.longitude + (Math.sin(heading) * speed);
        const newLat = cartographic.latitude + (Math.cos(heading) * speed);
        const newAlt = cartographic.height + (pitch * 10);

        jetEntity.position = Cesium.Cartesian3.fromRadians(newLon, newLat, newAlt);
        
        // Update HUD
        document.getElementById('alt').innerText = "ALT: " + Math.round(newAlt * 3.28) + " ft";
        document.getElementById('speed').innerText = "SPD: " + Math.round(speed * 100000) + " kn";
      }
      requestAnimationFrame(flightLoop);
    }
    flightLoop();
  </script>
</body>
</html>
