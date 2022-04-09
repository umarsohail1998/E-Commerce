var flag = false;
var r = document.getElementById("result");

function startConverting() {
    if ('webkitSpeechRecognition' in window) {
        var speechRecognizer = new webkitSpeechRecognition();
        speechRecognizer.continuous = true;
        speechRecognizer.interimResults = true;
        speechRecognizer.lang = "en-IN";
        speechRecognizer.start();

        var finalTranscripts = "";

        speechRecognizer.onresult = function(event) {
            var interimTranscripts = '';
            for (var i = event.resultIndex; i < event.results.length; i++) {
                var transcript = event.results[i][0].transcript;
                console.log(transcript);
                if (event.results[i].isFinal) {
                    finalTranscripts += transcript;
                } else {
                    interimTranscripts += transcript;
                }
                //console.log("interm" + interimTranscripts);
            }
            console.log("intermmmmm" + interimTranscripts);

            let k = finalTranscripts + interimTranscripts;
            r.value = k;
        };
        if (flag) {
            console.log("ending");
            speechRecognizer.stop();
            flag = false;
        }
        speechRecognizer.onerror = function(event) {
            console.log("error");
        };
    } else {
        r.value = "Your Browser is not supported\n";
    }
}

function ssearch() {
    var formBtn = document.getElementById("form-btn");
    flag = true;
    formBtn.click();
}
