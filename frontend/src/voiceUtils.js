export const getSpeechRecognitionCtor = (win = window) => {
  if (!win) return null;

  return win.SpeechRecognition || win.webkitSpeechRecognition || null;
};

export const resolveVoiceError = ({
  speechRecognitionSupported,
  navigatorSecure,
  permissionGranted,
  fallbackMessage,
  browserError,
}) => {
  if (!speechRecognitionSupported) {
    return 'Speech recognition is not supported in this browser. Please use Chrome or Edge on localhost or HTTPS.';
  }

  if (!navigatorSecure) {
    return 'Microphone access requires a secure context. Open the app on localhost or HTTPS and try again.';
  }

  if (permissionGranted === false) {
    return 'Microphone permission was blocked. Please allow microphone access and start voice again.';
  }

  if (browserError === 'network') {
    return 'Speech recognition service is temporarily unavailable. Try again in a moment on Chrome/Edge with microphone access enabled.';
  }

  return fallbackMessage || 'Voice input could not start in this browser. Please try again.';
};
