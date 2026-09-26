import test from 'node:test';
import assert from 'node:assert/strict';

import { getSpeechRecognitionCtor, resolveVoiceError } from './voiceUtils.js';

test('returns a browser speech-recognition constructor when available', () => {
  const fakeWindow = {
    SpeechRecognition: function FakeSpeechRecognition() {},
    webkitSpeechRecognition: undefined,
  };

  const ctor = getSpeechRecognitionCtor(fakeWindow);
  assert.equal(ctor, fakeWindow.SpeechRecognition);
});

test('reports a friendly message when voice is unsupported', () => {
  const err = resolveVoiceError({
    speechRecognitionSupported: false,
    navigatorSecure: false,
    permissionGranted: false,
  });

  assert.match(err, /supported|secure|microphone/i);
});

test('reports a helpful message when the speech service network fails', () => {
  const err = resolveVoiceError({
    speechRecognitionSupported: true,
    navigatorSecure: true,
    permissionGranted: true,
    browserError: 'network',
  });

  assert.match(err, /temporarily unavailable|Chrome|Edge|microphone/i);
});
