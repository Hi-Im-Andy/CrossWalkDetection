const video = document.querySelector('video');

const startWebCam = () =>{
 if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => video.srcObject = stream).catch(error => console.log(error));
 }
}
startWebCam();

const StopWebCam = ()=>{
  let stream = video.srcObject;
  let tracks = stream.getTracks();
  tracks.forEach(track => track.stop());
  video.srcObject = null;
}