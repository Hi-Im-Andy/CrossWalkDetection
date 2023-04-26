let videoWidth, videoHeight, video, streaming;
function setup() {
	video = document.querySelector("#videoElement");
	if (navigator.mediaDevices.getUserMedia) {
		navigator.mediaDevices
			.getUserMedia({ video: true })
			.then(function (stream) {
				video.srcObject = stream;
			})
			.catch(function (error) {
				console.log("an error has occured!");
			});
		videoWidth = video.videoWidth;
		videoHeight = video.videoHeight;

		video.addEventListener(
			"canplay",
			(ev) => {
				if (!streaming) {
					videoWidth = 720;
					videoHeight = video.videoHeight / (video.videoWidth / videoWidth);
					if (isNaN(videoHeight)) {
						videoHeight = videoWidth / (4 / 3);
					}

					video.setAttribute("width", videoWidth);
					video.setAttribute("height", videoHeight);
					canvas.setAttribute("width", videoWidth);
					canvas.setAttribute("height", videoHeight);

					startSending();
					streaming = true;
				}
			},
			false
		);
	} else {
		console.log("getUserMedia not supported ");
	}
}

let intervalID = null;
function startSending() {
	if (intervalID == null) {
		intervalID = setInterval(sendFrame, 4000); // send a frame every 4 seconds
	}
}
function stopSending() {
	if (intervalID != null) {
		clearInterval(intervalID);
		intervalID = null;
	}
}

function sendFrame() {
	const canvas = document.getElementById("canvas");
	const context = canvas.getContext("2d");
	canvas.width = videoWidth;
	canvas.height = videoHeight;
	context.drawImage(video, 0, 0, videoWidth, videoHeight);

	const base64 = canvas.toDataURL("image/jpeg");
	const imgData = base64.slice(22);

	var xhttp = new XMLHttpRequest();
	xhttp.open("POST", "http://127.0.0.1:5000/process_frame");
	xhttp.setRequestHeader("Content-Type", "application/json");
	xhttp.onload = function () {
		console.log(this.responseText);
		if(this.responseText == "Cross light detected") {
			stopSending();
		}
	};
	const body = { image: imgData, width: videoWidth, height: videoHeight };
	console.log(imgData);
	xhttp.send(JSON.stringify(body));
}

setup();
