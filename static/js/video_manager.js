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
					say("Camera on!");
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
		processResponse(this.responseText);
		if(state == 3) {
			stopSending();
		}
	};
	const body = { image: imgData, width: videoWidth, height: videoHeight };
	console.log(imgData);
	xhttp.send(JSON.stringify(body));
}

setup();

// 0 means nothing detected
// 1 means crosswalk found, no news on sign yet
// 2 means light found but don't cross
// 3 means time to cross
let state = 0;
function processResponse(responseText) {
	if(state == 0) {
		// Response can be either "No crosswalk detected" or "Crosswalk detected"
		if(responseText == "Crosswalk detected") {
			state = 1;
			say("Crosswalk detected, hold for sign detection");
		} else if(responseText == "No crosswalk detected") {
			say("Crosswalk not detected, adjust camera");
		}
	} else if(state == 1 || state == 2) {
		// Response can be either "No light detected", "Not ready to cross", or "You can cross"
		if(responseText = "No light detected") {
			say("Crossing light not detected, adjust camera");
		} else if(responseText = "Not ready to cross") {
			state = 2;
			say("Crossing light red, maintain camera angle but don't cross yet");
		} else if(responseText = "You can cross") {
			state = 3;
			say("Crossing light changed, you can cross safely");
		}
	} else if(state == 3) {
		say("You're safe to cross");
	}
}

function say(text) {
	let utterance = new SpeechSynthesisUtterance(text);
	speechSynthesis.speak(utterance);
	console.log("Speaking", text);
}